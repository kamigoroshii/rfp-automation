"""
Sales Agent - Discovers RFPs from various sources and creates summaries
"""
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional, Any
import uuid

from shared.models import RFPSummary
import imaplib
import email
import os
import json
from email.header import decode_header
from orchestrator.config import settings

logger = logging.getLogger(__name__)


class SalesAgent:
    """Agent responsible for discovering and summarizing RFPs"""
    
    def __init__(self):
        self.name = "SalesAgent"
        self.version = "1.0.0"
        
        # Initialize Redis
        self.redis = None
        try:
            from shared.cache.redis_manager import RedisManager
            self.redis = RedisManager()
            if not self.redis.connected:
                 logger.warning("RedisManager initialized but not connected.")
        except ImportError:
            logger.warning("RedisManager import failed. Redis features disabled.")
        except Exception as e:
            logger.warning(f"Redis initialization failed: {e}")
            
        logger.info(f"{self.name} v{self.version} initialized")
    
    def discover_rfps_from_url(self, url: str) -> List[RFPSummary]:
        """
        Discover RFPs from a given URL
        
        Args:
            url: URL to scrape for RFPs
            
        Returns:
            List of RFPSummary objects
        """
        try:
            logger.info(f"Discovering RFPs from URL: {url}")
            
            # Fetch webpage
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract RFP listings (this is a simplified example)
            rfps = []
            rfp_elements = soup.find_all('div', class_='rfp-listing')
            
            for element in rfp_elements:
                try:
                    rfp = self._parse_rfp_element(element)
                    if rfp:
                        # Qualification Check (Go/No-Go)
                        if self._evaluate_rfp(rfp):
                            rfps.append(rfp)
                            self._push_to_queue(rfp)
                        else:
                            logger.info(f"RFP {rfp.rfp_id} rejected by Go/No-Go filter")
                            
                except Exception as e:
                    logger.error(f"Error parsing RFP element: {str(e)}")
                    continue
            
            logger.info(f"Discovered {len(rfps)} qualified RFPs from {url}")
            return rfps
            
        except Exception as e:
            import traceback
            logger.error(f"Error discovering RFPs from URL: {str(e)}")
            return []

    def check_emails_imap(self) -> List[RFPSummary]:
        """
        Check IMAP email for new RFPs
        """
        try:
            host = settings.EMAIL_HOST
            user = settings.EMAIL_USER
            password = settings.EMAIL_PASSWORD

            if not host or not user or not password:
                logger.warning("Email settings not configured. Skipping email check.")
                return []

            logger.info(f"Connecting to IMAP server: {host}")
            mail = imaplib.IMAP4_SSL(host)
            mail.login(user, password)
            mail.select("inbox")

            # Search for ALL emails (including read ones)
            # To fetch only recent emails, you can add date filter
            # Example: status, messages = mail.search(None, '(SINCE "01-Jan-2025")')
            status, messages = mail.search(None, "ALL")
            
            rfps = []
            if status == "OK":
                email_ids = messages[0].split()
                # Process latest emails first
                for e_id in reversed(email_ids):
                    try:
                        # Fetch email body
                        res, msg_data = mail.fetch(e_id, "(RFC822)")
                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                msg = email.message_from_bytes(response_part[1])
                                
                                # Decode subject
                                subject_header = msg["Subject"]
                                if subject_header:
                                    subject, encoding = decode_header(subject_header)[0]
                                    if isinstance(subject, bytes):
                                        subject = subject.decode(encoding if encoding else "utf-8")
                                else:
                                    subject = "(No Subject)"
                                
                                sender = msg.get("From", "Unknown")
                                
                                # Get body and attachments
                                body = ""
                                attachments = []
                                
                                if msg.is_multipart():
                                    for part in msg.walk():
                                        content_type = part.get_content_type()
                                        content_disposition = str(part.get("Content-Disposition"))
                                        
                                        if content_type == "text/plain" and "attachment" not in content_disposition:
                                            try:
                                                part_payload = part.get_payload(decode=True)
                                                if part_payload:
                                                    body = part_payload.decode(errors='ignore')
                                            except:
                                                pass
                                        
                                        elif "attachment" in content_disposition:
                                            filename = part.get_filename()
                                            if filename:
                                                # Decode filename
                                                header_filename = decode_header(filename)[0]
                                                filename_bytes = header_filename[0]
                                                encoding = header_filename[1]
                                                if isinstance(filename_bytes, bytes):
                                                    filename = filename_bytes.decode(encoding if encoding else "utf-8")
                                                else:
                                                    filename = filename_bytes
                                                
                                                # Save only PDFs or relevant docs
                                                if filename.lower().endswith(('.pdf', '.doc', '.docx')):
                                                    save_dir = settings.UPLOAD_DIR
                                                    os.makedirs(save_dir, exist_ok=True)
                                                    
                                                    # Create unique filename
                                                    file_id = str(uuid.uuid4())[:8]
                                                    safe_filename = f"{file_id}_{filename}"
                                                    filepath = os.path.join(save_dir, safe_filename)
                                                    
                                                    with open(filepath, "wb") as f:
                                                        f.write(part.get_payload(decode=True))
                                                        
                                                    attachments.append({
                                                        "filename": filename,
                                                        "path": filepath,
                                                        "size": os.path.getsize(filepath)
                                                    })
                                                    logger.info(f"Downloaded attachment: {filepath}")
                                
                                else:
                                    payload = msg.get_payload(decode=True)
                                    if payload:
                                        body = payload.decode(errors='ignore')
                                
                                # Ingest
                                email_content = {
                                    "subject": subject,
                                    "sender": sender,
                                    "body": body,
                                    "attachments": attachments
                                }
                                
                                # Save email to database ALWAYS (for visibility in Inbox)
                                email_id = self._save_email_to_db(email_content)
                                
                                # Try to create RFP if valid
                                rfp = self.ingest_email_rfp(email_content, email_id)
                                if rfp:
                                    rfps.append(rfp)
                                    # Update email status to processed
                                    self._update_email_status(email_id, 'processed', rfp.rfp_id)
                    except Exception as inner_e:
                        logger.error(f"Error processing individual email {e_id}: {inner_e}")
                        continue
                                
            mail.close()
            mail.logout()
            return rfps
            
        except Exception as e:
            logger.error(f"Error checking IMAP: {str(e)}")
            return []
    
    def _save_email_to_db(self, email_content: Dict[str, Any]) -> str:
        """Save email to database"""
        try:
            from shared.database.connection import get_db_manager
            
            email_id = f"email-{str(uuid.uuid4())}"
            
            db = get_db_manager()
            if db:
                with db.get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO emails (email_id, subject, sender, received_at, body, attachments, status)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            RETURNING email_id
                        """, (
                            email_id,
                            email_content.get('subject', ''),
                            email_content.get('sender', ''),
                            datetime.now(),
                            email_content.get('body', ''),
                            json.dumps(email_content.get('attachments', [])),
                            'pending'
                        ))
                        conn.commit()
                        logger.info(f"Saved email to database: {email_id}")
            
            return email_id
        except Exception as e:
            logger.error(f"Error saving email to database: {str(e)}")
            return f"email-{str(uuid.uuid4())}"
    
    def _update_email_status(self, email_id: str, status: str, rfp_id: Optional[str] = None):
        """Update email processing status"""
        try:
            from shared.database.connection import get_db_manager
            
            db = get_db_manager()
            if db:
                with db.get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("""
                            UPDATE emails 
                            SET status = %s, processed_at = %s, rfp_id = %s
                            WHERE email_id = %s
                        """, (status, datetime.now(), rfp_id, email_id))
                        conn.commit()
                        logger.info(f"Updated email status: {email_id} -> {status}")
        except Exception as e:
            logger.error(f"Error updating email status: {str(e)}")

    def ingest_email_rfp(self, email_content: Dict[str, Any], email_id: str = None) -> Optional[RFPSummary]:
        """
        Ingest RFP from email content (Simulated)
        
        Args:
            email_content: Dict with 'subject', 'body', 'sender', 'attachments'
            
        Returns:
            RFPSummary object if qualified
        """
        try:
            logger.info(f"Ingesting email RFP: {email_content.get('subject')}")
            
            rfp_id = f"RFP-EMAIL-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"
            
            # Extract deadline (simulated logic)
            deadline = self._parse_deadline(email_content.get('body', ''))
            
            rfp = RFPSummary(
                rfp_id=rfp_id,
                title=email_content.get('subject', 'Untitled Email RFP'),
                source=f"Email: {email_content.get('sender')}",
                deadline=deadline,
                scope=email_content.get('body', '')[:500], # First 500 chars as scope preview
                testing_requirements=[],
                discovered_at=datetime.now(),
                status='new',
                client_tier=self._determine_client_tier(email_content.get('sender')),
                project_value=0.0,
                attachments=email_content.get('attachments', [])
            )
            
            if self._evaluate_rfp(rfp):
                self._push_to_queue(rfp)
                return rfp
            
            return None
            
        except Exception as e:
            logger.error(f"Error ingesting email RFP: {str(e)}")
            return None

    def _parse_rfp_element(self, element) -> Optional[RFPSummary]:
        """Parse RFP information from HTML element"""
        try:
            rfp_id = f"RFP-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"
            
            title = element.find('h3', class_='rfp-title')
            title_text = title.text.strip() if title else "Unknown RFP"
            
            source = element.find('a', class_='rfp-link')
            source_url = source.get('href', '') if source else ''
            
            deadline = element.find('span', class_='deadline')
            deadline_text = deadline.text.strip() if deadline else ''
            deadline_date = self._parse_deadline(deadline_text)
            
            scope = element.find('p', class_='scope')
            scope_text = scope.text.strip() if scope else ''
            
            # Estimate Project Value from text (Mock logic)
            project_value = 0.0
            value_text = element.find('span', class_='value')
            if value_text:
                import re
                nums = re.findall(r'\d+', value_text.text.replace(',', ''))
                if nums:
                    project_value = float(nums[0])

            rfp = RFPSummary(
                rfp_id=rfp_id,
                title=title_text,
                source=source_url,
                deadline=deadline_date,
                scope=scope_text,
                testing_requirements=[],
                discovered_at=datetime.now(),
                status='new',
                client_tier="Standard", # Default from web
                project_value=project_value
            )
            return rfp
        except Exception as e:
            logger.error(f"Error parsing RFP element: {str(e)}")
            return None
    
    def _parse_deadline(self, text: str) -> datetime:
        """Parse deadline text to datetime"""
        try:
            # Try various date formats
            formats = [
                "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"
            ]
            
            # Simple regex to find date-like strings
            import re
            date_patterns = [
                r'\d{4}-\d{2}-\d{2}',
                r'\d{2}/\d{2}/\d{4}',
                r'\d{2}-\d{2}-\d{4}'
            ]
            
            potential_dates = []
            for pattern in date_patterns:
                matches = re.findall(pattern, text)
                potential_dates.extend(matches)
                
            for date_str in potential_dates:
                for fmt in formats:
                    try:
                        return datetime.strptime(date_str, fmt)
                    except ValueError:
                        continue
            
            # Default to 45 days if not found
            from datetime import timedelta
            return datetime.now() + timedelta(days=45)
            
        except Exception:
            from datetime import timedelta
            return datetime.now() + timedelta(days=45)
            
    def _determine_client_tier(self, sender: str) -> str:
        """Determine client tier based on sender domain/name"""
        if not sender:
            return "Standard"
        sender_lower = sender.lower()
        if any(x in sender_lower for x in ['gov', 'energy', 'power', 'public']):
            return "Tier-1"
        if any(x in sender_lower for x in ['infra', 'build', 'construct']):
            return "Tier-2"
        return "Standard"

    def _evaluate_rfp(self, rfp: RFPSummary) -> bool:
        """
        Evaluate RFP for Go/No-Go decision
        Criteria:
        1. Deadline > 90 days NO-GO (too far)
        2. Deadline < 3 days NO-GO (too urgent, unless High Value)
        3. Score calculation
        """
        try:
            # 1. Check Deadline Window (Target: Next 3 months = 90 days)
            days_until = (rfp.deadline - datetime.now()).days
            
            if days_until > 90:
                logger.info(f"RFP {rfp.rfp_id} Rejected: Deadline > 90 days ({days_until})")
                return False
            
            if days_until < 0:
                 logger.info(f"RFP {rfp.rfp_id} Rejected: Expired")
                 return False

            # Calculate Qualification Score (0-100)
            score = 0.0
            
            # Keyword Relevance (Basic check)
            keywords = ['cable', 'wire', 'conductor', 'supply', 'tender']
            if any(k in rfp.title.lower() for k in keywords):
                score += 30
            if any(k in rfp.scope.lower() for k in keywords):
                score += 20
                
            # Client Tier Bonus
            if rfp.client_tier == "Tier-1":
                score += 30
            elif rfp.client_tier == "Tier-2":
                score += 15
                
            # Project Value Bonus (if known)
            if rfp.project_value > 1000000:
                score += 20
            elif rfp.project_value > 100000:
                score += 10
                
            rfp.go_no_go_score = score
            
            # Threshold
            if score >= 40:
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error evaluating RFP: {str(e)}")
            return False # Fail safe

    def _push_to_queue(self, rfp: RFPSummary):
        """Push qualified RFP to Redis queue"""
        if self.redis and self.redis.connected:
            self.redis.push_rfp(json.loads(rfp.to_json()))
            logger.info(f"Pushed RFP {rfp.rfp_id} to processing queue")
        else:
            logger.warning("Redis not available, skipping queue push")

    def summarize_rfp(self, rfp_text: str) -> Dict[str, any]:
        """
        Create a summary of RFP text
        
        Args:
            rfp_text: Full RFP text content
            
        Returns:
            Dictionary with summary information
        """
        try:
            logger.info("Generating RFP summary")
            
            # Simple extraction (in production, use NLP/LLM)
            summary = {
                'word_count': len(rfp_text.split()),
                'key_points': self._extract_key_points(rfp_text),
                'entities': self._extract_entities(rfp_text),
                'requirements_count': rfp_text.lower().count('requirement'),
                'technical_terms': self._extract_technical_terms(rfp_text)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error summarizing RFP: {str(e)}")
            return {}
    
    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from text"""
        # Simplified - in production use NLP
        sentences = text.split('.')
        key_points = []
        
        keywords = ['requirement', 'specification', 'must', 'shall', 'deadline']
        
        for sentence in sentences[:10]:  # Take first 10 sentences
            if any(keyword in sentence.lower() for keyword in keywords):
                key_points.append(sentence.strip())
        
        return key_points[:5]  # Return top 5
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract named entities from text"""
        # Simplified - in production use spaCy or similar
        entities = []
        
        # Extract numbers with units (voltages, currents, etc.)
        import re
        voltage_pattern = r'\d+\.?\d*\s*[kK]?[vV]'
        current_pattern = r'\d+\.?\d*\s*[mM]?[aA]'
        
        entities.extend(re.findall(voltage_pattern, text))
        entities.extend(re.findall(current_pattern, text))
        
        return list(set(entities))[:10]
    
    def _extract_technical_terms(self, text: str) -> List[str]:
        """Extract technical terms from text"""
        # Common cable/wire technical terms
        technical_terms = [
            'XLPE', 'PVC', 'conductor', 'insulation', 'voltage',
            'current', 'cable', 'wire', 'conductor', 'sheath',
            'armoured', 'IEC', 'IS', 'testing', 'routine test'
        ]
        
        found_terms = []
        text_lower = text.lower()
        
        for term in technical_terms:
            if term.lower() in text_lower:
                found_terms.append(term)
        
        return found_terms
    
    def validate_rfp(self, rfp: RFPSummary) -> bool:
        """
        Validate if RFP has minimum required information
        
        Args:
            rfp: RFPSummary object to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            if not rfp.title or len(rfp.title) < 5:
                return False
            
            if not rfp.source:
                return False
                
            # Note: deadline check is now done in _evaluate_rfp with Go/No-Go logic
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating RFP: {str(e)}")
            return False
