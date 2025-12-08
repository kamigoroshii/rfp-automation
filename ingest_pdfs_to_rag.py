"""
Ingest Existing PDFs into RAG System
Run this script to index all existing PDF attachments for the chatbot
"""
import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from shared.rag import get_rag_service
from shared.database.connection import get_db_connection
from orchestrator.config import settings

def ingest_existing_pdfs():
    """Ingest all existing PDF attachments from RFPs"""
    logger.info("=" * 60)
    logger.info("  INGESTING EXISTING PDFs INTO RAG SYSTEM")
    logger.info("=" * 60)
    
    # Initialize RAG service
    rag_service = get_rag_service()
    if not rag_service.client:
        logger.error("❌ Qdrant client not initialized!")
        logger.error("   Make sure Qdrant is running on localhost:6333")
        return
    
    logger.info("✅ RAG service initialized")
    
    # Get all RFPs with attachments from database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT rfp_id, title, source, deadline, attachments
            FROM rfps
            WHERE attachments IS NOT NULL 
            AND attachments::text != '[]'
            ORDER BY discovered_at DESC
        """)
        
        rfps = cursor.fetchall()
        logger.info(f"📊 Found {len(rfps)} RFPs with attachments")
        
        upload_dir = getattr(settings, 'UPLOAD_DIR', 'data/uploads')
        
        total_ingested = 0
        total_pdfs = 0
        
        for rfp in rfps:
            rfp_id, title, source, deadline, attachments = rfp
            
            # Parse attachments JSON
            import json
            if isinstance(attachments, str):
                try:
                    attachments = json.loads(attachments)
                except:
                    continue
            
            if not isinstance(attachments, list):
                continue
            
            logger.info(f"\n📁 Processing RFP: {rfp_id} - {title}")
            
            for attachment in attachments:
                # Get file path
                if isinstance(attachment, dict):
                    file_path = attachment.get('path') or attachment.get('filename', '')
                elif isinstance(attachment, str):
                    file_path = attachment
                else:
                    continue
                
                # Check if it's a PDF
                if not file_path.lower().endswith('.pdf'):
                    continue
                
                total_pdfs += 1
                
                # Build full path
                if not os.path.isabs(file_path):
                    full_path = os.path.join(upload_dir, os.path.basename(file_path))
                else:
                    full_path = file_path
                
                # Ingest if file exists
                if os.path.exists(full_path):
                    logger.info(f"   📄 Ingesting: {os.path.basename(full_path)}")
                    
                    success = rag_service.ingest_document(
                        pdf_path=full_path,
                        rfp_id=rfp_id,
                        metadata={
                            'title': title,
                            'source': source,
                            'deadline': deadline.isoformat() if deadline else None
                        }
                    )
                    
                    if success:
                        total_ingested += 1
                        logger.info(f"   ✅ Successfully ingested!")
                    else:
                        logger.warning(f"   ⚠️  Failed to ingest")
                else:
                    logger.warning(f"   ❌ File not found: {full_path}")
        
        cursor.close()
        conn.close()
        
        logger.info("\n" + "=" * 60)
        logger.info("  ✅ INGESTION COMPLETE!")
        logger.info("=" * 60)
        logger.info(f"📊 Summary:")
        logger.info(f"   • Total RFPs processed: {len(rfps)}")
        logger.info(f"   • Total PDFs found: {total_pdfs}")
        logger.info(f"   • Successfully ingested: {total_ingested}")
        logger.info(f"   • Failed: {total_pdfs - total_ingested}")
        logger.info("=" * 60)
        logger.info("\n🤖 Chatbot is now ready to answer questions about the PDFs!")
        logger.info("   Try asking: 'What are the technical specifications?'")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Error ingesting PDFs: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ingest_existing_pdfs()
