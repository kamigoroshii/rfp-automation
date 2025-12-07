"""
RFP Service - Business logic for RFP operations
"""
import os
import logging
from typing import List, Optional
from datetime import datetime
import uuid

from shared.models import RFPSummary, Feedback
from shared.database.connection import get_db_connection
from orchestrator.tasks.rfp_tasks import process_rfp_task

logger = logging.getLogger(__name__)


class RFPService:
    """Service for RFP operations"""
    
    async def get_rfps(self, status: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[dict]:
        """Get list of RFPs"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
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
            cursor.close()
            conn.close()
            
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
            raise
    
    async def get_rfp_by_id(self, rfp_id: str) -> Optional[dict]:
        """Get RFP by ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT r.rfp_id, r.title, r.source, r.deadline, r.scope, 
                       r.status, r.discovered_at, r.match_score, r.total_estimate,
                       r.testing_requirements, r.specifications, r.recommended_sku
                FROM rfps r
                WHERE r.rfp_id = %s
            """, (rfp_id,))
            
            row = cursor.fetchone()
            
            if not row:
                cursor.close()
                conn.close()
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
            
            cursor.close()
            conn.close()
            
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
                "matches": matches,
                "pricing": pricing
            }
            
            return rfp
        except Exception as e:
            logger.error(f"Error fetching RFP {rfp_id}: {str(e)}")
            raise
    
    async def create_rfp(self, rfp_summary: RFPSummary) -> str:
        """Create a new RFP"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO rfps 
                (rfp_id, title, source, deadline, scope, testing_requirements, 
                 discovered_at, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                rfp_summary.rfp_id,
                rfp_summary.title,
                rfp_summary.source,
                rfp_summary.deadline,
                rfp_summary.scope,
                rfp_summary.testing_requirements,
                rfp_summary.discovered_at,
                rfp_summary.status
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"Created RFP: {rfp_summary.rfp_id}")
            return rfp_summary.rfp_id
        except Exception as e:
            logger.error(f"Error creating RFP: {str(e)}")
            raise
    
    async def update_status(self, rfp_id: str, status: str) -> None:
        """Update RFP status"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE rfps
                SET status = %s, updated_at = %s
                WHERE rfp_id = %s
            """, (status, datetime.now(), rfp_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
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
            
            # Trigger Celery task
            # TODO: Get URL or file path from DB/Logic
            # For now, we assume URL if source is a URL, else file
            
            # Temporary: Fetch source from DB to decide
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT source FROM rfps WHERE rfp_id = %s", (rfp_id,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            
            source = row[0] if row else ""
            
            if source.startswith('http'):
                process_rfp_task.delay(rfp_id=rfp_id, url=source)
            else:
                # Assume it's a file we uploaded (naming convention used in save_rfp_file)
                # Ideally config/db should store the file path. 
                # For this MVP, we reconstructed it or need to save it in DB.
                # Let's check the upload dir
                upload_dir = "data/uploads"
                path = None
                if os.path.exists(upload_dir):
                    for f in os.listdir(upload_dir):
                        if f.startswith(rfp_id):
                            path = os.path.join(upload_dir, f)
                            break
                            
                process_rfp_task.delay(rfp_id=rfp_id, pdf_path=path)
                
            logger.info(f"Triggered processing for RFP {rfp_id}")
        except Exception as e:
            logger.error(f"Error processing RFP: {str(e)}")
            raise
    
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
            conn = get_db_connection()
            cursor = conn.cursor()
            
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
            cursor.close()
            conn.close()
            
            logger.info(f"Submitted feedback for RFP {rfp_id}")
        except Exception as e:
            logger.error(f"Error submitting feedback: {str(e)}")
            raise
    
    async def delete_rfp(self, rfp_id: str) -> None:
        """Delete an RFP"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Delete related records
            cursor.execute("DELETE FROM product_matches WHERE rfp_id = %s", (rfp_id,))
            cursor.execute("DELETE FROM pricing_breakdown WHERE rfp_id = %s", (rfp_id,))
            cursor.execute("DELETE FROM feedback WHERE rfp_id = %s", (rfp_id,))
            cursor.execute("DELETE FROM rfps WHERE rfp_id = %s", (rfp_id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"Deleted RFP {rfp_id}")
        except Exception as e:
            logger.error(f"Error deleting RFP: {str(e)}")
            raise
