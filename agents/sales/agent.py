"""
Sales Agent - Discovers RFPs from various sources and creates summaries
"""
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import uuid

from shared.models import RFPSummary

logger = logging.getLogger(__name__)


class SalesAgent:
    """Agent responsible for discovering and summarizing RFPs"""
    
    def __init__(self):
        self.name = "SalesAgent"
        self.version = "1.0.0"
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
                        rfps.append(rfp)
                except Exception as e:
                    logger.error(f"Error parsing RFP element: {str(e)}")
                    continue
            
            logger.info(f"Discovered {len(rfps)} RFPs from {url}")
            return rfps
            
        except Exception as e:
            logger.error(f"Error discovering RFPs from URL: {str(e)}")
            return []
    
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
            
            return RFPSummary(
                rfp_id=rfp_id,
                title=title_text,
                source=source_url,
                deadline=deadline_date,
                scope=scope_text,
                testing_requirements=[],
                discovered_at=datetime.now(),
                status='new'
            )
        except Exception as e:
            logger.error(f"Error parsing RFP element: {str(e)}")
            return None
    
    def _parse_deadline(self, deadline_text: str) -> datetime:
        """Parse deadline text to datetime"""
        try:
            # Try various date formats
            formats = [
                "%Y-%m-%d",
                "%d/%m/%Y",
                "%m/%d/%Y",
                "%d-%m-%Y"
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(deadline_text, fmt)
                except ValueError:
                    continue
            
            # Default to 30 days from now if parsing fails
            from datetime import timedelta
            return datetime.now() + timedelta(days=30)
            
        except Exception:
            from datetime import timedelta
            return datetime.now() + timedelta(days=30)
    
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
            
            if not rfp.deadline or rfp.deadline < datetime.now():
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating RFP: {str(e)}")
            return False
