"""
Email API endpoints for viewing discovered emails
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from shared.database.connection import get_db_connection

logger = logging.getLogger(__name__)

router = APIRouter()


class Email(BaseModel):
    email_id: str
    subject: str
    sender: str
    received_at: datetime
    body: Optional[str] = None
    attachments: List[Any] = []
    rfp_id: Optional[str] = None
    status: str
    processed_at: Optional[datetime] = None


class EmailListResponse(BaseModel):
    emails: List[Email]
    total: int
    processed_count: int
    pending_count: int


@router.get("/list", response_model=EmailListResponse)
async def get_emails(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """
    Get list of discovered emails
    
    Args:
        status: Filter by status (processed/pending)
        limit: Number of emails to return
        offset: Offset for pagination
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build query
        query = """
            SELECT 
                email_id, subject, sender, received_at, body,
                attachments, rfp_id, status, processed_at
            FROM emails
        """
        
        params = []
        if status:
            query += " WHERE status = %s"
            params.append(status)
        
        query += " ORDER BY received_at DESC, email_id LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Get counts
        cursor.execute("SELECT COUNT(*) FROM emails")
        total = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM emails WHERE status = 'processed'")
        processed_count = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM emails WHERE status = 'pending'")
        pending_count = cursor.fetchone()[0] or 0
        
        # Format emails
        emails = []
        for row in rows:
            # Parse attachments JSON
            attachments = row[5] if row[5] else []
            if isinstance(attachments, str):
                import json
                try:
                    attachments = json.loads(attachments)
                except:
                    attachments = []
            elif not isinstance(attachments, list):
                # Should be list if parsed by driver, otherwise fallback
                attachments = []
            
            emails.append(Email(
                email_id=row[0],
                subject=row[1],
                sender=row[2],
                received_at=row[3],
                body=row[4],
                attachments=attachments,
                rfp_id=row[6],
                status=row[7],
                processed_at=row[8]
            ))
        
        cursor.close()
        conn.close()
        
        return EmailListResponse(
            emails=emails,
            total=total,
            processed_count=processed_count,
            pending_count=pending_count
        )
        
    except Exception as e:
        logger.error(f"Error fetching emails: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{email_id}", response_model=Email)
async def get_email(email_id: str):
    """Get details of a specific email"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                email_id, subject, sender, received_at, body,
                attachments, rfp_id, status, processed_at
            FROM emails
            WHERE email_id = %s
        """, (email_id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Email not found")
        
        # Parse attachments JSON
        attachments = row[5] if row[5] else []
        if isinstance(attachments, str):
            import json
            try:
                attachments = json.loads(attachments)
            except:
                attachments = []
        
        return Email(
            email_id=row[0],
            subject=row[1],
            sender=row[2],
            received_at=row[3],
            body=row[4],
            attachments=attachments,
            rfp_id=row[6],
            status=row[7],
            processed_at=row[8]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=Dict[str, Any])
async def get_email_stats():
    """Get email statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total emails
        cursor.execute("SELECT COUNT(*) FROM emails")
        total = cursor.fetchone()[0] or 0
        
        # Processed
        cursor.execute("SELECT COUNT(*) FROM emails WHERE status = 'processed'")
        processed = cursor.fetchone()[0] or 0
        
        # Pending
        cursor.execute("SELECT COUNT(*) FROM emails WHERE status = 'pending'")
        pending = cursor.fetchone()[0] or 0
        
        # Total attachments
        cursor.execute("""
            SELECT COALESCE(SUM(jsonb_array_length(CASE WHEN jsonb_typeof(attachments) = 'array' THEN attachments ELSE '[]'::jsonb END)), 0)
            FROM emails
            WHERE attachments IS NOT NULL
        """)
        total_attachments = cursor.fetchone()[0] or 0
        
        # Recent emails (last 7 days)
        cursor.execute("""
            SELECT COUNT(*) FROM emails
            WHERE received_at >= NOW() - INTERVAL '7 days'
        """)
        recent = cursor.fetchone()[0] or 0
        
        cursor.close()
        conn.close()
        
        return {
            "total_emails": total,
            "processed": processed,
            "pending": pending,
            "total_attachments": total_attachments,
            "recent_7_days": recent
        }
        
    except Exception as e:
        logger.error(f"Error fetching email stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
