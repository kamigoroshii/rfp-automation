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
            from qdrant_client import QdrantClient
            import os
            
            host = os.getenv("QDRANT_HOST", "localhost")
            port = int(os.getenv("QDRANT_PORT", 6333))
            
            self.vector_db = QdrantClient(host=host, port=port)
            logger.info(f"Vector database initialized at {host}:{port}")
        except Exception as e:
            logger.error(f"Error initializing vector DB: {str(e)}")
    
    
    def initialize_embedding_model(self):
        """Initialize sentence embedding model"""
        try:
            from sentence_transformers import SentenceTransformer
            import os
            
            model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
            self.embedding_model = SentenceTransformer(model_name)
            logger.info(f"Embedding model initialized: {model_name}")
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
            
            # Perform semantic search (hybrid approach)
            matches = []
            
            # 1. Try Vector Search first if DB initialized
            if self.vector_db and self.embedding_model:
                try:
                    matches = self.semantic_search(query, top_k)
                except Exception as e:
                    logger.warning(f"Vector search failed, falling back to rules: {e}")
            
            # 2. Fallback or augmentation with rules
            if not matches:
                matches = self._rule_based_matching(specifications, top_k)
            
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
        """
        Calculate equal-weight SpecMatch%
        Score = (Matched Params / Total Params Found) * 100
        """
        match_count = 0
        total_params = 0
        
        # Keys to check
        check_keys = [
            'voltage', 'conductor_size', 'conductor_material', 
            'insulation_material', 'cable_type'
        ]
        
        for key in check_keys:
            rfp_val = rfp_specs.get(key)
            if rfp_val:
                total_params += 1
                prod_val = product_specs.get(key)
                
                if self._specs_match_normalized(rfp_val, prod_val):
                    match_count += 1
                    
        if total_params == 0:
            return 0.0
            
        return (match_count / total_params) # Returns 0.0 to 1.0 (multiply by 100 for percent later)

    def _normalize_unit(self, value: str) -> str:
        """
        Normalize technical values
        e.g. '11 kV' -> '11000', '185sqmm' -> '185'
        """
        if not value: return ""
        val = str(value).lower().replace(" ", "")
        
        # KV -> V
        if 'kv' in val:
            import re
            nums = re.findall(r'(\d+\.?\d*)', val)
            if nums:
                try:
                    return str(float(nums[0]) * 1000)
                except: pass
                
        # MM2/SQMM -> Raw number
        if 'mm' in val or 'sq' in val:
            import re
            nums = re.findall(r'(\d+\.?\d*)', val)
            if nums:
                return nums[0]
                
        return val

    def _specs_match_normalized(self, rfp_val: str, prod_val: str) -> bool:
        """Match using normalized values"""
        if not rfp_val or not prod_val: return False
        
        # Try direct match first
        if str(rfp_val).lower() == str(prod_val).lower(): return True
        
        # Try normalized match
        norm_rfp = self._normalize_unit(rfp_val)
        norm_prod = self._normalize_unit(prod_val)
        
        if norm_rfp and norm_prod and norm_rfp == norm_prod:
            return True
            
        # Fallback to substring for non-numeric (materials)
        if norm_rfp in norm_prod or norm_prod in norm_rfp:
            return True
            
        return False

    def _specs_match(self, rfp_value: str, product_value: str) -> bool:
        """Legacy match wrapper"""
        return self._specs_match_normalized(rfp_value, product_value)
    
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
            
            if not self.vector_db or not self.embedding_model:
                logger.warning("Vector DB or Model not initialized")
                return []
                
            import os
            collection_name = os.getenv("QDRANT_COLLECTION", "products")
            
            # Generate embedding
            vector = self.embedding_model.encode(query).tolist()
            
            # Search Qdrant
            search_result = self.vector_db.search(
                collection_name=collection_name,
                query_vector=vector,
                limit=top_k
            )
            
            results = []
            for hit in search_result:
                payload = hit.payload
                # Add match score to payload for consistency
                payload['relevance_score'] = hit.score
                # Add dummy datasheet if missing
                if 'datasheet_url' not in payload:
                    payload['datasheet_url'] = ''
                    
                results.append(payload)
                
            return results
            
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            return []
