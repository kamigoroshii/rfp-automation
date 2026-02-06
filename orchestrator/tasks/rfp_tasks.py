"""
Celery tasks for RFP processing
"""
import asyncio
import logging
from celery import Celery
import os
from dotenv import load_dotenv
from datetime import datetime

# Load env vars
load_dotenv()

from orchestrator.config import settings
from orchestrator.workflow import RFPWorkflow
from shared.database.connection import get_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    "rfp_tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

# Workflow instance (will be initialized per worker process)
workflow = None

def get_workflow():
    """Get or initialize workflow instance"""
    global workflow
    if workflow is None:
        workflow = RFPWorkflow()
        # Initialize agents (TechnicalAgent needs DB connection)
        workflow.technical_agent.initialize_vector_db()
        workflow.technical_agent.initialize_embedding_model()
    return workflow

def update_rfp_status_sync(rfp_id: str, status: str):
    """Update RFP status (synchronous for Celery)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE rfps SET status = %s, updated_at = %s WHERE rfp_id = %s",
            (status, datetime.now(), rfp_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error updating status for {rfp_id}: {e}")

@celery_app.task(name="process_rfp_task")
def process_rfp_task(rfp_id: str, url: str = None, pdf_path: str = None):
    """
    Celery task to process RFP
    """
    logger.info(f"Starting background task for RFP {rfp_id}")
    
    try:
        wf = get_workflow()
        
        # Since workflow methods are async, we need to run them in an event loop
        loop = asyncio.get_event_loop()
        
        result = None
        if url:
            result = loop.run_until_complete(
                wf.process_rfp_from_url(url=url)
            )
        elif pdf_path:
            # For PDF, we need metadata
            # Fetch metadata from DB first
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT title, deadline, source FROM rfps WHERE rfp_id = %s", (rfp_id,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            
            metadata = {
                'rfp_id': rfp_id,
                'title': row[0] if row else "Unknown",
                'deadline': row[1],
                'buyer': row[2]
            }
            
            result = loop.run_until_complete(
                wf.process_rfp_from_pdf(pdf_path=pdf_path, rfp_metadata=metadata)
            )
        
        if result and result.get('status') == 'success':
            logger.info(f"RFP {rfp_id} processed successfully")
            update_rfp_status_sync(rfp_id, 'completed')
            
            # Save results to DB (matches, pricing)
            # Note: Ideally this saving logic should be inside the workflow or helper
            # But currently the workflow returns a dict. 
            # We should probably save it here or ensure workflow saves it.
            # Looking at existing code, workflow does NOT save to DB, it just returns dict.
            # So we must save implementation here or in a service.
            
            # Since we are in a Celery task, let's call a sync save function
            save_results_sync(rfp_id, result)
            
        else:
            logger.error(f"RFP {rfp_id} processing failed: {result}")
            update_rfp_status_sync(rfp_id, 'failed')
            
    except Exception as e:
        logger.error(f"Error in background task for {rfp_id}: {e}", exc_info=True)
        update_rfp_status_sync(rfp_id, 'failed')

def save_results_sync(rfp_id: str, result: dict):
    """Save processing results to DB"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Update RFP with summary stats
        matches = result.get('matches', [])
        pricing = result.get('pricing', [])
        recommendation = result.get('recommendation', {})
        
        top_match_score = matches[0]['match_score'] if matches else 0.0
        rec_sku = recommendation.get('sku')
        # Calculate total from all pricing items
        total_est = sum(p.get('total', 0) for p in pricing)
        
        cursor.execute("""
            UPDATE rfps 
            SET match_score = %s, 
                total_estimate = %s,
                recommended_sku = %s,
                specifications = %s
            WHERE rfp_id = %s
        """, (
            top_match_score, 
            total_est, 
            rec_sku, 
            json.dumps(result.get('specifications', [])),
            rfp_id
        ))
        
        # 2. Save Matches
        import json
        for m in matches:
            cursor.execute("""
                INSERT INTO product_matches
                (rfp_id, sku, product_name, match_score, specification_alignment)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                rfp_id,
                m['sku'],
                m['name'],
                m['match_score'],
                json.dumps(m['matched_specs'])
            ))
            
        # 3. Save Pricing
        for p in pricing:
            # Breakdown is in p['breakdown'] dict
            bd = p['breakdown']['breakdown'] # nested from agent
            
            cursor.execute("""
                INSERT INTO pricing_breakdown
                (rfp_id, sku, unit_price, quantity, subtotal, 
                 testing_cost, delivery_cost, urgency_adjustment, total)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                rfp_id,
                p['sku'],
                p['unit_price'],
                p['quantity'],
                bd['material_cost']['amount'],
                bd['testing_cost']['amount'],
                bd['delivery_cost']['amount'],
                bd['urgency_premium']['amount'],
                p['total']
            ))
            
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Results saved for RFP {rfp_id}")
        
    except Exception as e:
        logger.error(f"Error saving results: {e}", exc_info=True)
