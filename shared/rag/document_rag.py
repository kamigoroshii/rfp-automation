"""
Document RAG Service - Ingest PDFs into Qdrant for RAG queries
"""
import logging
import os
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class DocumentRAGService:
    """Service for ingesting documents into Qdrant and querying them"""
    
    def __init__(self):
        self.collection_name = "rfp_documents"
        self.chunk_size = 500  # characters per chunk
        self.chunk_overlap = 100  # overlap between chunks
        
        # Initialize Qdrant client
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http import models
            from sentence_transformers import SentenceTransformer
            
            self.client = QdrantClient(host="localhost", port=6333)
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.models = models
            
            # Create collection if it doesn't exist
            self._ensure_collection()
            
            logger.info("DocumentRAGService initialized successfully")
        except ImportError as e:
            logger.error(f"Missing dependencies: {e}")
            logger.error("Install: pip install qdrant-client sentence-transformers")
            self.client = None
        except Exception as e:
            logger.error(f"Error initializing DocumentRAGService: {e}")
            self.client = None
    
    def _ensure_collection(self):
        """Create Qdrant collection if it doesn't exist"""
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=self.models.VectorParams(
                        size=384,  # all-MiniLM-L6-v2 embedding size
                        distance=self.models.Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error ensuring collection: {e}")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            import PyPDF2
            
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            
            logger.info(f"Extracted {len(text)} characters from {pdf_path}")
            return text
        except ImportError:
            logger.error("PyPDF2 not installed. Install: pip install PyPDF2")
            return ""
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return ""
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > 0:
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - self.chunk_overlap
        
        logger.info(f"Created {len(chunks)} chunks from text")
        return chunks
    
    def ingest_document(
        self, 
        pdf_path: str, 
        rfp_id: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Ingest a PDF document into Qdrant
        
        Args:
            pdf_path: Path to PDF file
            rfp_id: RFP ID for reference
            metadata: Additional metadata (title, source, etc.)
        
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.error("Qdrant client not initialized")
            return False
        
        try:
            # Extract text from PDF
            text = self.extract_text_from_pdf(pdf_path)
            if not text:
                logger.warning(f"No text extracted from {pdf_path}")
                return False
            
            # Split into chunks
            chunks = self.chunk_text(text)
            
            # Generate embeddings and store in Qdrant
            points = []
            for i, chunk in enumerate(chunks):
                # Generate embedding
                embedding = self.embedding_model.encode(chunk).tolist()
                
                # Create point
                point_id = str(uuid.uuid4())
                point = self.models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "rfp_id": rfp_id,
                        "chunk_index": i,
                        "text": chunk,
                        "pdf_path": pdf_path,
                        "ingested_at": datetime.now().isoformat(),
                        **(metadata or {})
                    }
                )
                points.append(point)
            
            # Upload to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Ingested {len(chunks)} chunks from {pdf_path} for RFP {rfp_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error ingesting document: {e}")
            return False
    
    def query_documents(
        self, 
        query: str, 
        rfp_id: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Query documents using semantic search
        
        Args:
            query: User query
            rfp_id: Optional RFP ID to filter results
            limit: Number of results to return
        
        Returns:
            List of relevant document chunks with metadata
        """
        if not self.client:
            logger.error("Qdrant client not initialized")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Build filter
            query_filter = None
            if rfp_id:
                query_filter = self.models.Filter(
                    must=[
                        self.models.FieldCondition(
                            key="rfp_id",
                            match=self.models.MatchValue(value=rfp_id)
                        )
                    ]
                )
            
            # Search in Qdrant
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=query_filter,
                limit=limit
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "text": result.payload.get("text", ""),
                    "score": result.score,
                    "rfp_id": result.payload.get("rfp_id", ""),
                    "chunk_index": result.payload.get("chunk_index", 0),
                    "metadata": {
                        k: v for k, v in result.payload.items() 
                        if k not in ["text", "rfp_id", "chunk_index"]
                    }
                })
            
            logger.info(f"Found {len(formatted_results)} relevant chunks for query: {query}")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error querying documents: {e}")
            return []
    
    def delete_document(self, rfp_id: str) -> bool:
        """Delete all chunks for a specific RFP"""
        if not self.client:
            logger.error("Qdrant client not initialized")
            return False
        
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=self.models.FilterSelector(
                    filter=self.models.Filter(
                        must=[
                            self.models.FieldCondition(
                                key="rfp_id",
                                match=self.models.MatchValue(value=rfp_id)
                            )
                        ]
                    )
                )
            )
            logger.info(f"Deleted document chunks for RFP {rfp_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False
    
    def get_document_stats(self, rfp_id: str) -> Dict[str, Any]:
        """Get statistics about ingested document"""
        if not self.client:
            return {"error": "Qdrant client not initialized"}
        
        try:
            # Count chunks for this RFP
            results = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=self.models.Filter(
                    must=[
                        self.models.FieldCondition(
                            key="rfp_id",
                            match=self.models.MatchValue(value=rfp_id)
                        )
                    ]
                ),
                limit=1000
            )
            
            chunks = results[0]
            
            return {
                "rfp_id": rfp_id,
                "total_chunks": len(chunks),
                "ingested": len(chunks) > 0,
                "chunks_preview": [
                    {
                        "index": c.payload.get("chunk_index", 0),
                        "text_preview": c.payload.get("text", "")[:100] + "..."
                    }
                    for c in chunks[:3]
                ]
            }
        except Exception as e:
            logger.error(f"Error getting document stats: {e}")
            return {"error": str(e)}


# Global instance
_rag_service = None

def get_rag_service() -> DocumentRAGService:
    """Get or create RAG service instance"""
    global _rag_service
    if _rag_service is None:
        _rag_service = DocumentRAGService()
    return _rag_service
