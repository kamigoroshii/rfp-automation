"""
Document Agent - Parses RFP documents and extracts specifications
"""
import logging
import pdfplumber
import re
from typing import Dict, List, Optional, Any
from pathlib import Path

from shared.models import Specification

logger = logging.getLogger(__name__)


class DocumentAgent:
    """Agent responsible for parsing documents and extracting specifications"""
    
    def __init__(self):
        self.name = "DocumentAgent"
        self.version = "1.0.0"
        logger.info(f"{self.name} v{self.version} initialized")
    
    def extract_specifications_from_text(self, text: str) -> Specification:
        """
        Extract technical specifications from raw text
        
        Args:
            text: Raw RFP text
            
        Returns:
            Specification object
        """
        try:
            logger.info("Extracting specifications from raw text")
            
            # Extract specifications
            specifications = {
                'voltage': self._extract_voltage(text),
                'current': self._extract_current(text),
                'conductor_material': self._extract_conductor_material(text),
                'insulation_material': self._extract_insulation_material(text),
                'conductor_size': self._extract_conductor_size(text),
                'cable_type': self._extract_cable_type(text),
                'length': self._extract_length(text),
                'standards': self._extract_standards(text),
                'raw_text_sample': text[:500]
            }
            
            # Extract testing requirements
            testing_requirements = self._extract_testing_requirements(text)
            
            # Calculate confidence score
            confidence = self._calculate_confidence(specifications, testing_requirements)
            
            # Create a dummy ID for text-based extraction if not provided context
            rfp_id = "TEXT-EXTRACT"
            
            return Specification(
                rfp_id=rfp_id,
                specifications=specifications,
                testing_requirements=testing_requirements,
                confidence_score=confidence
            )
            
        except Exception as e:
            logger.error(f"Error extracting specifications from text: {str(e)}")
            raise

    def parse_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Parse PDF document and extract text
        
        Args:
            pdf_path: Path to PDF file (can be None)
            
        Returns:
            Dictionary with extracted content
        """
        try:
            logger.info(f"Parsing PDF: {pdf_path}")
            
            # Check if pdf_path is None or empty
            if not pdf_path:
                logger.warning("PDF path is None or empty - cannot parse")
                raise ValueError("PDF path cannot be None or empty")
            
            if not Path(pdf_path).exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            content = {
                'text': '',
                'pages': 0,
                'tables': [],
                'metadata': {}
            }
            
            with pdfplumber.open(pdf_path) as pdf:
                content['pages'] = len(pdf.pages)
                content['metadata'] = pdf.metadata
                
                # Extract text from all pages
                text_parts = []
                for page in pdf.pages:
                    text_parts.append(page.extract_text() or '')
                    
                    # Extract tables
                    tables = page.extract_tables()
                    if tables:
                        content['tables'].extend(tables)
                
                content['text'] = '\n\n'.join(text_parts)
            
            logger.info(f"Parsed PDF: {content['pages']} pages, {len(content['text'])} characters")
            return content
            
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            raise
    
    def extract_specifications(self, rfp_id: str, pdf_path: str) -> Specification:
        """
        Extract technical specifications from RFP document
        
        Args:
            rfp_id: RFP identifier
            pdf_path: Path to PDF file
            
        Returns:
            Specification object
        """
        try:
            logger.info(f"Extracting specifications from: {pdf_path}")
            
            # Parse PDF
            content = self.parse_pdf(pdf_path)
            text = content['text']
            
            # Extract specifications
            specifications = {
                'voltage': self._extract_voltage(text),
                'current': self._extract_current(text),
                'conductor_material': self._extract_conductor_material(text),
                'insulation_material': self._extract_insulation_material(text),
                'conductor_size': self._extract_conductor_size(text),
                'cable_type': self._extract_cable_type(text),
                'length': self._extract_length(text),
                'standards': self._extract_standards(text),
                'raw_text_sample': text[:500]  # First 500 chars for reference
            }
            
            # Extract testing requirements
            testing_requirements = self._extract_testing_requirements(text)
            
            # Calculate confidence score
            confidence = self._calculate_confidence(specifications, testing_requirements)
            
            return Specification(
                rfp_id=rfp_id,
                specifications=specifications,
                testing_requirements=testing_requirements,
                confidence_score=confidence
            )
            
        except Exception as e:
            logger.error(f"Error extracting specifications: {str(e)}")
            raise
    
    def _extract_voltage(self, text: str) -> Optional[str]:
        """Extract voltage specification"""
        patterns = [
            r'(\d+\.?\d*)\s*[kK][vV]',
            r'voltage[:\s]+(\d+\.?\d*)\s*[kK]?[vV]',
            r'rated voltage[:\s]+(\d+\.?\d*)\s*[kK]?[vV]'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_current(self, text: str) -> Optional[str]:
        """Extract current rating"""
        patterns = [
            r'(\d+\.?\d*)\s*[aA]',
            r'current[:\s]+(\d+\.?\d*)\s*[aA]',
            r'rated current[:\s]+(\d+\.?\d*)\s*[aA]'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_conductor_material(self, text: str) -> Optional[str]:
        """Extract conductor material"""
        materials = ['copper', 'aluminium', 'aluminum', 'cu', 'al']
        
        text_lower = text.lower()
        for material in materials:
            if f'conductor' in text_lower and material in text_lower:
                return material.upper() if len(material) <= 2 else material.capitalize()
        
        return None
    
    def _extract_insulation_material(self, text: str) -> Optional[str]:
        """Extract insulation material"""
        materials = ['XLPE', 'PVC', 'EPR', 'PE', 'rubber']
        
        for material in materials:
            if material.lower() in text.lower():
                return material
        
        return None
    
    def _extract_conductor_size(self, text: str) -> Optional[str]:
        """Extract conductor cross-section size"""
        patterns = [
            r'(\d+\.?\d*)\s*[sS][qQ]\s*[mM][mM]',
            r'(\d+\.?\d*)\s*mm[²2]',
            r'cross[- ]section[:\s]+(\d+\.?\d*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_cable_type(self, text: str) -> Optional[str]:
        """Extract cable type"""
        cable_types = [
            'single core', 'multi-core', 'multicore', '3 core', '4 core',
            'armoured', 'unarmoured', 'aerial', 'underground'
        ]
        
        text_lower = text.lower()
        found_types = []
        
        for cable_type in cable_types:
            if cable_type in text_lower:
                found_types.append(cable_type)
        
        return ', '.join(found_types) if found_types else None
    
    def _extract_length(self, text: str) -> Optional[str]:
        """Extract cable length requirement"""
        patterns = [
            r'(\d+\.?\d*)\s*[kK]?[mM]',
            r'length[:\s]+(\d+\.?\d*)',
            r'quantity[:\s]+(\d+\.?\d*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and 'length' in text[max(0, match.start()-20):match.end()+20].lower():
                return match.group(0)
        
        return None
    
    def _extract_standards(self, text: str) -> List[str]:
        """Extract applicable standards"""
        standards_patterns = [
            r'IEC\s*\d+[-/]?\d*',
            r'IS\s*\d+',
            r'BS\s*\d+',
            r'ASTM\s*[A-Z]\d+',
            r'IEEE\s*\d+'
        ]
        
        standards = []
        for pattern in standards_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            standards.extend(matches)
        
        return list(set(standards))
    
    def _extract_testing_requirements(self, text: str) -> Dict[str, List[str]]:
        """Extract testing requirements"""
        testing_requirements = {
            'type_tests': [],
            'routine_tests': [],
            'sample_tests': []
        }
        
        # Type tests
        type_test_keywords = [
            'type test', 'voltage test', 'impulse test', 'partial discharge',
            'thermal test', 'flame test'
        ]
        
        # Routine tests
        routine_test_keywords = [
            'routine test', 'conductor resistance', 'voltage test',
            'continuity test', 'insulation resistance'
        ]
        
        text_lower = text.lower()
        
        for keyword in type_test_keywords:
            if keyword in text_lower:
                testing_requirements['type_tests'].append(keyword)
        
        for keyword in routine_test_keywords:
            if keyword in text_lower:
                testing_requirements['routine_tests'].append(keyword)
        
        return testing_requirements
    
    def _calculate_confidence(
        self,
        specifications: Dict[str, Any],
        testing_requirements: Dict[str, List[str]]
    ) -> float:
        """Calculate confidence score for extracted specifications"""
        score = 0.0
        total_fields = 8  # Total number of specification fields
        
        # Count filled specification fields
        filled_fields = sum(1 for v in specifications.values() if v)
        score += (filled_fields / total_fields) * 0.7
        
        # Add points for testing requirements
        total_tests = sum(len(tests) for tests in testing_requirements.values())
        if total_tests > 0:
            score += min(total_tests / 10, 0.3)
        
        return min(score, 1.0)
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters
        text = re.sub(r'[^\w\s\-.,;:()\[\]{}]', '', text)
        
        # Normalize line breaks
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        return text.strip()
