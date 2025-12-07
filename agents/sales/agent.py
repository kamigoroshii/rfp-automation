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
        except ImportError:
            logger.warning("RedisManager not found. Redis features disabled.")
            
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
            logger.error(f"Error discovering RFPs from URL: {str(e)}")
            return []

    def check_emails_imap(self) -> List[RFPSummary]:
        """
        Check configured IMAP account for new RFPs (Real-time integration)
        Requires EMAIL_HOST, EMAIL_USER, EMAIL_PASSWORD env vars.
        """
        import os
        host = os.getenv("EMAIL_HOST")
        user = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASSWORD")
        
        if not (host and user and password):
            logger.info("IMAP credentials not found. Real-time email monitoring disabled.")
            return []

        try:
            import imaplib
            import email
            from email.header import decode_header

            logger.info(f"Connecting to IMAP server: {host}")
            mail = imaplib.IMAP4_SSL(host)
            mail.login(user, password)
            mail.select("inbox")

            # Search for all emails (or specific subjects)
            status, messages = mail.search(None, "UNSEEN")
            
            rfps = []
            if status == "OK":
                email_ids = messages[0].split()
                for e_id in email_ids:
                    # Fetch email body
                    res, msg_data = mail.fetch(e_id, "(RFC822)")
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            
                            # Decode subject
                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding if encoding else "utf-8")
                            
                            sender = msg.get("From")
                            
                            # Get body
                            body = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                        break
                            else:
                                body = msg.get_payload(decode=True).decode()
                            
                            # Ingest
                            email_content = {
                                "subject": subject,
                                "sender": sender,
                                "body": body
                            }
                            
                            rfp = self.ingest_email_rfp(email_content)
                            if rfp:
                                rfps.append(rfp)
                                
            mail.close()
            mail.logout()
            return rfps
            
        except Exception as e:
            logger.error(f"Error checking IMAP: {str(e)}")
            return []

    def ingest_email_rfp(self, email_content: Dict[str, Any]) -> Optional[RFPSummary]:
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
                project_value=0.0  # Unknown initially
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
