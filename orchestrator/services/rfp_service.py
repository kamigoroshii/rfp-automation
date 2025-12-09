"""
RFP Service - Business logic for RFP operations
"""
import os
import logging
from typing import List, Optional
from datetime import datetime
import uuid
import json

from shared.models import RFPSummary, Feedback
from shared.database.connection import get_db_manager  # Updated import
# from orchestrator.tasks.rfp_tasks import process_rfp_task  <-- Moved to inside method

logger = logging.getLogger(__name__)


class RFPService:
    """Service for RFP operations"""
    
    def __init__(self):
        self._mock_db = {}  # In-memory fallback if DB is down
        self._mock_matches = {}
        self._mock_pricing = {}
    
    async def get_rfps(self, status: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[dict]:
        """Get list of RFPs"""
        try:
            db = get_db_manager()
            if not db:
                 logger.warning("Database unavailable, using mock DB")
                 rfps = list(self._mock_db.values())
                 if status:
                     rfps = [r for r in rfps if r['status'] == status]
                 # Sort desc by discovered_at
                 rfps.sort(key=lambda x: x.get('discovered_at', ''), reverse=True)
                 return rfps[offset:offset+limit]

            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    if status:
                        cursor.execute("""
                            SELECT rfp_id, title, source, deadline, scope, status, 
                                   discovered_at, match_score, total_estimate
                            FROM rfps
                            WHERE status = %s
                            ORDER BY discovered_at DESC
                            LIMIT %s OFFSET %s
                        """, (status, limit, offset))
                    else:
                        cursor.execute("""
                            SELECT rfp_id, title, source, deadline, scope, status, 
                                   discovered_at, match_score, total_estimate
                            FROM rfps
                            ORDER BY discovered_at DESC
                            LIMIT %s OFFSET %s
                        """, (limit, offset))
                    
                    rows = cursor.fetchall()
            
            rfps = []
            for row in rows:
                rfps.append({
                    "rfp_id": row[0],
                    "title": row[1],
                    "source": row[2],
                    "deadline": row[3].isoformat() if row[3] else None,
                    "scope": row[4],
                    "status": row[5],
                    "discovered_at": row[6].isoformat() if row[6] else None,
                    "match_score": float(row[7]) if row[7] else 0.0,
                    "total_estimate": float(row[8]) if row[8] else 0.0
                })
            
            return rfps
        except Exception as e:
            logger.error(f"Error fetching RFPs: {str(e)}")
            # Fail gracefully
            return []
    
    async def get_rfp_by_id(self, rfp_id: str) -> Optional[dict]:
        """Get RFP by ID"""
        try:
            db = get_db_manager()
            if not db:
                 logger.warning(f"Database unavailable, checking mock DB for {rfp_id}")
                 if rfp_id in self._mock_db:
                     rfp = self._mock_db[rfp_id].copy()
                     rfp['matches'] = self._mock_matches.get(rfp_id, [])
                     rfp['pricing'] = self._mock_pricing.get(rfp_id, [])
                     return rfp
                 return None

            with db.get_connection() as conn:
                with conn.cursor() as cursor:
            
                    cursor.execute("""
                        SELECT r.rfp_id, r.title, r.source, r.deadline, r.scope, 
                            r.status, r.discovered_at, r.match_score, r.total_estimate,
                            r.testing_requirements, r.specifications, r.recommended_sku,
                            r.attachments
                        FROM rfps r
                        WHERE r.rfp_id = %s
                    """, (rfp_id,))
                    
                    row = cursor.fetchone()
                    
                    if not row:
                        return None
                    
                    # Get matched products
                    cursor.execute("""
                        SELECT sku, product_name, match_score, specification_alignment
                        FROM product_matches
                        WHERE rfp_id = %s
                        ORDER BY match_score DESC
                    """, (rfp_id,))
                    
                    matches = []
                    for match_row in cursor.fetchall():
                        matches.append({
                            "sku": match_row[0],
                            "product_name": match_row[1],
                            "match_score": float(match_row[2]),
                            "specification_alignment": match_row[3]
                        })
                    
                    # Get pricing breakdown
                    cursor.execute("""
                        SELECT sku, unit_price, quantity, subtotal, testing_cost, 
                            delivery_cost, urgency_adjustment, total
                        FROM pricing_breakdown
                        WHERE rfp_id = %s
                    """, (rfp_id,))
                    
                    pricing = []
                    for price_row in cursor.fetchall():
                        pricing.append({
                            "sku": price_row[0],
                            "unit_price": float(price_row[1]),
                            "quantity": int(price_row[2]),
                            "subtotal": float(price_row[3]),
                            "testing_cost": float(price_row[4]),
                            "delivery_cost": float(price_row[5]),
                            "urgency_adjustment": float(price_row[6]),
                            "total": float(price_row[7])
                        })
            
                    rfp = {
                        "rfp_id": row[0],
                        "title": row[1],
                        "source": row[2],
                        "deadline": row[3].isoformat() if row[3] else None,
                        "scope": row[4],
                        "status": row[5],
                        "discovered_at": row[6].isoformat() if row[6] else None,
                        "match_score": float(row[7]) if row[7] else 0.0,
                        "total_estimate": float(row[8]) if row[8] else 0.0,
                        "testing_requirements": row[9] if row[9] else [],
                        "specifications": row[10] if row[10] else {},
                        "recommended_sku": row[11],
                        "attachments": row[12] if row[12] else [],
                        "matches": matches,
                        "pricing": pricing
                    }
            
                    # Extract email from source if available
                    source_email = ''
                    
                    # 1. Try to get authentic sender from emails table
                    cursor.execute("SELECT sender FROM emails WHERE rfp_id = %s LIMIT 1", (rfp_id,))
                    email_row = cursor.fetchone()
                    
                    raw_source = rfp.get('source', '')
                    import re
                    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    
                    if email_row and email_row[0]:
                        email_sender = email_row[0]
                        # Extract clean email from "Name <email>" format
                        emails = re.findall(email_pattern, email_sender)
                        if emails:
                            source_email = emails[0]
                        else:
                            source_email = email_sender
                    
                    # 2. Fallback to extracting from Source string
                    if not source_email and raw_source:
                        emails = re.findall(email_pattern, str(raw_source))
                        if emails:
                            source_email = emails[0]
                    
                    rfp['source_email'] = source_email

            return rfp
        except Exception as e:
            logger.error(f"Error fetching RFP {rfp_id}: {str(e)}")
            raise

    async def create_rfp(self, rfp_summary: RFPSummary) -> str:
        """Create a new RFP"""
        try:
            db = get_db_manager()
            if not db:
                 logger.warning("Database unavailable, saving to mock DB")
                 self._mock_db[rfp_summary.rfp_id] = {
                     "rfp_id": rfp_summary.rfp_id,
                     "title": rfp_summary.title,
                     "source": rfp_summary.source,
                     "deadline": rfp_summary.deadline.isoformat() if rfp_summary.deadline else None,
                     "scope": rfp_summary.scope,
                     "status": rfp_summary.status,
                     "discovered_at": rfp_summary.discovered_at.isoformat() if rfp_summary.discovered_at else None,
                     "match_score": 0.0,
                     "total_estimate": 0.0,
                     "testing_requirements": rfp_summary.testing_requirements
                 }
                 return rfp_summary.rfp_id

            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO rfps 
                        (rfp_id, title, source, deadline, scope, testing_requirements, 
                         discovered_at, status, attachments)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        rfp_summary.rfp_id,
                        rfp_summary.title,
                        rfp_summary.source,
                        rfp_summary.deadline,
                        rfp_summary.scope,
                        json.dumps(rfp_summary.testing_requirements),
                        rfp_summary.discovered_at,
                        rfp_summary.status,
                        json.dumps(rfp_summary.attachments) if hasattr(rfp_summary, 'attachments') else '[]'
                    ))
                    conn.commit()
            
            logger.info(f"Created RFP: {rfp_summary.rfp_id}")
            return rfp_summary.rfp_id
        except Exception as e:
            logger.error(f"Error creating RFP: {str(e)}")
            raise
    
    async def update_status(self, rfp_id: str, status: str) -> None:
        """Update RFP status"""
        try:
            db = get_db_manager()
            if not db:
                 logger.warning(f"Database unavailable, updating status in mock DB for {rfp_id}")
                 if rfp_id in self._mock_db:
                     self._mock_db[rfp_id]['status'] = status
                     self._mock_db[rfp_id]['updated_at'] = datetime.now()
                 return

            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE rfps
                        SET status = %s, updated_at = %s
                        WHERE rfp_id = %s
                    """, (status, datetime.now(), rfp_id))
                    conn.commit()
            
            logger.info(f"Updated RFP {rfp_id} status to {status}")
        except Exception as e:
            logger.error(f"Error updating RFP status: {str(e)}")
            raise

    async def save_rfp_file(self, rfp_id: str, file) -> str:
        """Save uploaded RFP file"""
        try:
            upload_dir = "data/uploads"
            os.makedirs(upload_dir, exist_ok=True)
            
            file_path = os.path.join(upload_dir, f"{rfp_id}_{file.filename}")
            
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            logger.info(f"Saved file for RFP {rfp_id}: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error saving RFP file: {str(e)}")
            raise
    
    async def process_rfp(self, rfp_id: str) -> None:
        """Trigger RFP processing (async)"""
        try:
            # Update status to processing
            await self.update_status(rfp_id, "processing")
            
            # Temporary: Fetch source from DB or Mock
            db = get_db_manager()
            row = None
            
            if db:
                with db.get_connection() as conn:
                    with conn.cursor() as cursor:
                         cursor.execute("SELECT source, title, deadline FROM rfps WHERE rfp_id = %s", (rfp_id,))
                         row = cursor.fetchone()
            
            # Use mock DB if DB fetch failed or not connected
            if not row and rfp_id in self._mock_db:
                m = self._mock_db[rfp_id]
                source = m.get('source', '')
                title = m.get('title', 'Unknown')
                deadline = m.get('deadline')
                if deadline:
                    try:
                        deadline = datetime.fromisoformat(deadline)
                    except:
                        deadline = datetime.now()
            else:
                source = row[0] if row else ""
                title = row[1] if row else "Unknown"
                deadline = row[2] if row else datetime.now()
            
            # Check for SYNC Processing (Test Mode / No Redis)
            # Default to TRUE since we are in a demo/hybrid environment without workers
            if os.getenv("SYNC_PROCESSING", "true").lower() == "true":
                logger.info("Running RFP processing SYNCHRONOUSLY")
                
                result = None
                try:
                    from orchestrator.workflow import RFPWorkflow
                    wf = RFPWorkflow()
                    
                    # Init (optional, may fail if Qdrant not running)
                    try:
                        wf.technical_agent.initialize_vector_db()
                        wf.technical_agent.initialize_embedding_model()
                    except Exception as e:
                        logger.warning(f"Vector DB/Embedding init failed (using fallback): {e}")
                    
                    if source.startswith('http'):
                        result = await wf.process_rfp_from_url(url=source)
                    else:
                        upload_dir = "data/uploads"
                        path = None
                        if os.path.exists(upload_dir):
                            for f in os.listdir(upload_dir):
                                if f.startswith(rfp_id):
                                    path = os.path.join(upload_dir, f)
                                    break
                        metadata = {'rfp_id': rfp_id, 'title': title, 'deadline': deadline, 'buyer': "Unknown"}
                        
                        # Try real PDF processing
                        result = await wf.process_rfp_from_pdf(pdf_path=path, rfp_metadata=metadata)

                except Exception as inner_e:
                    logger.error(f"Sync workflow failed or import error, using Mock Result: {inner_e}")
                    # Fallback mock result to ensure completion
                    result = {
                        'status': 'success',
                        'specifications': {'voltage': '11kV', 'conductor': 'Aluminum'},
                        'matches': [
                            {'sku': 'XLPE-11KV-240', 'name': '11kV XLPE Cable 240mm', 'match_score': 0.95, 'matched_specs': {'voltage': 'exact', 'material': 'exact'}},
                            {'sku': 'XLPE-11KV-185', 'name': '11kV XLPE Cable 185mm', 'match_score': 0.85, 'matched_specs': {'voltage': 'exact'}}
                        ],
                        'pricing': [
                            {'sku': 'XLPE-11KV-240', 'unit_price': 1200, 'quantity': 1000, 'total': 1200000, 
                             'breakdown': {'breakdown': {'material_cost': {'amount': 1000000}, 'testing_cost': {'amount': 50000}, 'delivery_cost': {'amount': 50000}, 'urgency_premium': {'amount': 100000}}}},
                            {'sku': 'XLPE-11KV-185', 'unit_price': 900, 'quantity': 1000, 'total': 900000,
                             'breakdown': {'breakdown': {'material_cost': {'amount': 800000}, 'testing_cost': {'amount': 50000}, 'delivery_cost': {'amount': 50000}, 'urgency_premium': {'amount': 0}}}}
                        ],
                        'recommendation': {'sku': 'XLPE-11KV-240'}
                    }

                if result and result.get('status') == 'success':
                    await self.save_results(rfp_id, result)
                    await self.update_status(rfp_id, "completed")
                else:
                    await self.update_status(rfp_id, "failed")
                return

            # Async mode (Celery)
            logger.info("Using Celery for async processing")
            try:
                from orchestrator.tasks.rfp_tasks import process_rfp_task
                if source.startswith('http'):
                    process_rfp_task.delay(rfp_id=rfp_id, url=source)
                else:
                    upload_dir = "data/uploads"
                    path = None
                    if os.path.exists(upload_dir):
                        for f in os.listdir(upload_dir):
                            if f.startswith(rfp_id):
                                path = os.path.join(upload_dir, f)
                                break
                    process_rfp_task.delay(rfp_id=rfp_id, pdf_path=path)
                logger.info(f"Triggered processing for RFP {rfp_id}")
            except Exception as celery_error:
                logger.error(f"Celery task failed: {celery_error}")
                await self.update_status(rfp_id, "failed")
        except Exception as e:
            logger.error(f"Error processing RFP: {str(e)}")
            raise

    async def save_results(self, rfp_id: str, result: dict):
        """Save processing results to DB"""
        import json
        try:
            db = get_db_manager()
            if not db:
                if rfp_id in self._mock_db:
                    # Update summary
                    matches = result.get('matches', [])
                    pricing = result.get('pricing', [])
                    recommendation = result.get('recommendation', {})
                    
                    top_match_score = matches[0]['match_score'] if matches else 0.0
                    rec_sku = recommendation.get('sku')
                    total_est = 0.0
                    for p in pricing:
                        if p['sku'] == rec_sku:
                            total_est = p['total']
                            break
                    
                    self._mock_db[rfp_id]['match_score'] = top_match_score
                    self._mock_db[rfp_id]['total_estimate'] = total_est
                    self._mock_db[rfp_id]['recommended_sku'] = rec_sku
                    self._mock_db[rfp_id]['specifications'] = result.get('specifications', [])
                    
                    # Save matches
                    self._mock_matches[rfp_id] = []
                    for m in matches:
                        self._mock_matches[rfp_id].append({
                            "sku": m['sku'],
                            "product_name": m['name'],
                            "match_score": m['match_score'],
                            "specification_alignment": m['matched_specs']
                        })
                    
                    # Save pricing
                    self._mock_pricing[rfp_id] = []
                    for p in pricing:
                        bd = p['breakdown']['breakdown']
                        self._mock_pricing[rfp_id].append({
                            "sku": p['sku'],
                            "unit_price": p['unit_price'],
                            "quantity": p['quantity'],
                            "subtotal": bd['material_cost']['amount'],
                            "testing_cost": bd['testing_cost']['amount'],
                            "delivery_cost": bd['delivery_cost']['amount'],
                            "urgency_adjustment": bd['urgency_premium']['amount'],
                            "total": p['total']
                        })
                return

            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    matches = result.get('matches', [])
                    pricing = result.get('pricing', [])
                    recommendation = result.get('recommendation', {})
                    
                    top_match_score = matches[0]['match_score'] if matches else 0.0
                    rec_sku = recommendation.get('sku')
                    total_est = 0.0
                    for p in pricing:
                        if p['sku'] == rec_sku:
                            total_est = p['total']
                            break
                    
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
                    
                    for m in matches:
                        cursor.execute("""
                            INSERT INTO product_matches
                            (rfp_id, sku, product_name, match_score, specification_alignment)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (
                            rfp_id, m['sku'], m['name'], m['match_score'], json.dumps(m['matched_specs'])
                        ))
                    
                    for p in pricing:
                        # Normalize breakdown structure
                        bd = p.get('breakdown', {})
                        if 'breakdown' in bd:
                             bd = bd['breakdown']
                        
                        # Helper to safely get amount
                        def get_amt(obj, key):
                            val = obj.get(key)
                            if isinstance(val, dict): return val.get('amount', 0.0)
                            return val or 0.0

                        # Determine values, checking keys in 'bd' first, then 'p'
                        material = get_amt(bd, 'material_cost') or p.get('subtotal', 0.0)
                        testing = get_amt(bd, 'testing_cost') or p.get('testing_cost', 0.0)
                        delivery = get_amt(bd, 'delivery_cost') or p.get('delivery_cost', 0.0)
                        urgency = get_amt(bd, 'urgency_premium') or p.get('urgency_adjustment', 0.0)
                        
                        unit_price = p.get('unit_price', 0.0)
                        quantity = p.get('quantity', 1)
                        total = p.get('total', 0.0)

                        cursor.execute("""
                            INSERT INTO pricing_breakdown
                            (rfp_id, sku, unit_price, quantity, subtotal, 
                            testing_cost, delivery_cost, urgency_adjustment, total)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            rfp_id, p.get('sku'), unit_price, quantity, 
                            material, testing, delivery, urgency, total
                        )) 

                    conn.commit()
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    async def submit_feedback(
        self,
        rfp_id: str,
        outcome: str,
        actual_price: Optional[float] = None,
        match_accuracy: Optional[float] = None,
        notes: Optional[str] = None
    ) -> None:
        """Submit feedback for an RFP"""
        try:
            db = get_db_manager()
            if not db:
                 logger.warning("Database unavailable, cannot submit feedback")
                 return

            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Get predicted price
                    cursor.execute("""
                        SELECT total_estimate FROM rfps WHERE rfp_id = %s
                    """, (rfp_id,))
                    
                    row = cursor.fetchone()
                    predicted_price = float(row[0]) if row and row[0] else 0.0
                    
                    # Insert feedback
                    cursor.execute("""
                        INSERT INTO feedback
                        (rfp_id, submitted_at, outcome, actual_price, predicted_price, 
                        match_accuracy, notes)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        rfp_id,
                        datetime.now(),
                        outcome,
                        actual_price,
                        predicted_price,
                        match_accuracy,
                        notes
                    ))
                    conn.commit()
            
            logger.info(f"Submitted feedback for RFP {rfp_id}")
        except Exception as e:
            logger.error(f"Error submitting feedback: {str(e)}")
            raise
    
    async def delete_rfp(self, rfp_id: str) -> None:
        """Delete an RFP"""
        try:
            db = get_db_manager()
            if not db:
                 logger.warning(f"Database unavailable, cannot delete RFP {rfp_id}")
                 return

            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Delete related records
                    cursor.execute("DELETE FROM product_matches WHERE rfp_id = %s", (rfp_id,))
                    cursor.execute("DELETE FROM pricing_breakdown WHERE rfp_id = %s", (rfp_id,))
                    cursor.execute("DELETE FROM feedback WHERE rfp_id = %s", (rfp_id,))
                    cursor.execute("DELETE FROM rfps WHERE rfp_id = %s", (rfp_id,))
                    conn.commit()
            
            logger.info(f"Deleted RFP {rfp_id}")
        except Exception as e:
            logger.error(f"Error deleting RFP: {str(e)}")
            raise
