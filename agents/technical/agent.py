"""
Technical Agent - Matches RFP specifications with product catalog
"""
import logging
from typing import List, Dict, Any, Optional
import json

from shared.models import ProductMatch, Specification

logger = logging.getLogger(__name__)


class TechnicalAgent:
    """Agent responsible for matching RFP specs with products"""
    
    def __init__(self):
        self.name = "TechnicalAgent"
        self.version = "1.0.0"
        self.embedding_model = None
        self.vector_db = None
        logger.info(f"{self.name} v{self.version} initialized")
    
    def initialize_vector_db(self):
        """Initialize vector database connection (Qdrant)"""
        try:
            # TODO: Initialize Qdrant client
            # from qdrant_client import QdrantClient
            # self.vector_db = QdrantClient(host="localhost", port=6333)
            logger.info("Vector database initialized")
        except Exception as e:
            logger.error(f"Error initializing vector DB: {str(e)}")
    
    def initialize_embedding_model(self):
        """Initialize sentence embedding model"""
        try:
            # TODO: Initialize embedding model
            # from sentence_transformers import SentenceTransformer
            # self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Embedding model initialized")
        except Exception as e:
            logger.error(f"Error initializing embedding model: {str(e)}")
    
    def match_products(
        self,
        rfp_id: str,
        specifications: Specification,
        top_k: int = 10
    ) -> List[ProductMatch]:
        """
        Find best matching products for RFP specifications
        
        Args:
            rfp_id: RFP identifier
            specifications: Specification object
            top_k: Number of top matches to return
            
        Returns:
            List of ProductMatch objects
        """
        try:
            logger.info(f"Matching products for RFP: {rfp_id}")
            
            # Create search query from specifications
            query = self._create_search_query(specifications)
            
            # Perform semantic search (using rule-based matching for now)
            matches = self._rule_based_matching(specifications, top_k)
            
            # For production: use vector search
            # matches = self._vector_search(query, top_k)
            
            logger.info(f"Found {len(matches)} product matches")
            return matches
            
        except Exception as e:
            logger.error(f"Error matching products: {str(e)}")
            return []
    
    def _create_search_query(self, specifications: Specification) -> str:
        """Create search query from specifications"""
        query_parts = []
        
        specs = specifications.specifications
        
        if specs.get('voltage'):
            query_parts.append(f"voltage {specs['voltage']}")
        
        if specs.get('cable_type'):
            query_parts.append(specs['cable_type'])
        
        if specs.get('conductor_material'):
            query_parts.append(f"{specs['conductor_material']} conductor")
        
        if specs.get('insulation_material'):
            query_parts.append(f"{specs['insulation_material']} insulation")
        
        if specs.get('conductor_size'):
            query_parts.append(f"{specs['conductor_size']} cross section")
        
        return ' '.join(query_parts)
    
    def _rule_based_matching(
        self,
        specifications: Specification,
        top_k: int
    ) -> List[ProductMatch]:
        """
        Rule-based product matching (fallback when vector DB not available)
        """
        matches = []
        specs = specifications.specifications
        
        # Mock product catalog
        mock_products = self._get_mock_products()
        
        for product in mock_products:
            score = self._calculate_match_score(specs, product['specifications'])
            
            if score > 0.3:  # Threshold
                alignment = self._get_specification_alignment(specs, product['specifications'])
                
                match = ProductMatch(
                    sku=product['sku'],
                    product_name=product['product_name'],
                    match_score=score,
                    specification_alignment=alignment,
                    datasheet_url=product.get('datasheet_url', '')
                )
                matches.append(match)
        
        # Sort by match score
        matches.sort(key=lambda x: x.match_score, reverse=True)
        
        return matches[:top_k]
    
    def _calculate_match_score(
        self,
        rfp_specs: Dict[str, Any],
        product_specs: Dict[str, Any]
    ) -> float:
        """Calculate match score between RFP and product specifications"""
        score = 0.0
        total_weight = 0.0
        
        # Define weights for different specifications
        weights = {
            'voltage': 0.25,
            'current': 0.20,
            'conductor_material': 0.15,
            'insulation_material': 0.15,
            'conductor_size': 0.15,
            'cable_type': 0.10
        }
        
        for spec_key, weight in weights.items():
            rfp_value = rfp_specs.get(spec_key)
            product_value = product_specs.get(spec_key)
            
            if rfp_value and product_value:
                total_weight += weight
                
                # Check if values match
                if self._specs_match(rfp_value, product_value):
                    score += weight
        
        # Normalize score
        if total_weight > 0:
            score = score / total_weight
        
        return score
    
    def _specs_match(self, rfp_value: str, product_value: str) -> bool:
        """Check if two specification values match"""
        if not rfp_value or not product_value:
            return False
        
        rfp_lower = str(rfp_value).lower().strip()
        product_lower = str(product_value).lower().strip()
        
        # Exact match
        if rfp_lower == product_lower:
            return True
        
        # Partial match
        if rfp_lower in product_lower or product_lower in rfp_lower:
            return True
        
        # Extract numbers and compare
        import re
        rfp_nums = re.findall(r'\d+\.?\d*', rfp_lower)
        product_nums = re.findall(r'\d+\.?\d*', product_lower)
        
        if rfp_nums and product_nums:
            # Compare first number (often the most important)
            return rfp_nums[0] == product_nums[0]
        
        return False
    
    def _get_specification_alignment(
        self,
        rfp_specs: Dict[str, Any],
        product_specs: Dict[str, Any]
    ) -> Dict[str, str]:
        """Get detailed alignment between RFP and product specifications"""
        alignment = {}
        
        for key in rfp_specs:
            if key in product_specs:
                rfp_val = rfp_specs[key]
                prod_val = product_specs[key]
                
                if rfp_val and prod_val:
                    if self._specs_match(rfp_val, prod_val):
                        alignment[key] = "exact_match"
                    else:
                        alignment[key] = "partial_match"
                else:
                    alignment[key] = "missing"
        
        return alignment
    
    def _get_mock_products(self) -> List[Dict[str, Any]]:
        """Get mock product catalog for testing"""
        return [
            {
                'sku': 'XLPE-11KV-185',
                'product_name': '11kV XLPE Cable 185 sq mm',
                'specifications': {
                    'voltage': '11kV',
                    'conductor_material': 'Copper',
                    'insulation_material': 'XLPE',
                    'conductor_size': '185 sq mm',
                    'cable_type': '3 core, armoured',
                    'standards': ['IEC 60502', 'IS 7098']
                },
                'datasheet_url': 'http://example.com/datasheets/xlpe-11kv-185.pdf'
            },
            {
                'sku': 'XLPE-11KV-240',
                'product_name': '11kV XLPE Cable 240 sq mm',
                'specifications': {
                    'voltage': '11kV',
                    'conductor_material': 'Copper',
                    'insulation_material': 'XLPE',
                    'conductor_size': '240 sq mm',
                    'cable_type': '3 core, armoured',
                    'standards': ['IEC 60502', 'IS 7098']
                },
                'datasheet_url': 'http://example.com/datasheets/xlpe-11kv-240.pdf'
            },
            {
                'sku': 'XLPE-33KV-185',
                'product_name': '33kV XLPE Cable 185 sq mm',
                'specifications': {
                    'voltage': '33kV',
                    'conductor_material': 'Copper',
                    'insulation_material': 'XLPE',
                    'conductor_size': '185 sq mm',
                    'cable_type': '3 core, armoured',
                    'standards': ['IEC 60502', 'IS 7098']
                },
                'datasheet_url': 'http://example.com/datasheets/xlpe-33kv-185.pdf'
            },
            {
                'sku': 'PVC-1.1KV-50',
                'product_name': '1.1kV PVC Cable 50 sq mm',
                'specifications': {
                    'voltage': '1.1kV',
                    'conductor_material': 'Copper',
                    'insulation_material': 'PVC',
                    'conductor_size': '50 sq mm',
                    'cable_type': '4 core',
                    'standards': ['IEC 60227', 'IS 694']
                },
                'datasheet_url': 'http://example.com/datasheets/pvc-1.1kv-50.pdf'
            },
            {
                'sku': 'XLPE-11KV-300',
                'product_name': '11kV XLPE Cable 300 sq mm',
                'specifications': {
                    'voltage': '11kV',
                    'conductor_material': 'Aluminium',
                    'insulation_material': 'XLPE',
                    'conductor_size': '300 sq mm',
                    'cable_type': '3 core, armoured',
                    'standards': ['IEC 60502', 'IS 7098']
                },
                'datasheet_url': 'http://example.com/datasheets/xlpe-11kv-300-al.pdf'
            }
        ]
    
    def semantic_search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Perform semantic search in product catalog
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of matching products
        """
        try:
            logger.info(f"Performing semantic search: {query}")
            
            # TODO: Implement vector search with Qdrant
            # For now, return mock results
            mock_products = self._get_mock_products()
            
            # Simple keyword matching
            results = []
            query_lower = query.lower()
            
            for product in mock_products:
                score = 0.0
                
                # Check if query terms appear in product
                if query_lower in product['product_name'].lower():
                    score += 0.5
                
                for spec_val in product['specifications'].values():
                    if isinstance(spec_val, str) and query_lower in spec_val.lower():
                        score += 0.1
                
                if score > 0:
                    product['relevance_score'] = score
                    results.append(product)
            
            # Sort by relevance
            results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            return []
