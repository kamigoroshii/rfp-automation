"""
Notifications API - Real-time RFP and system alerts
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from shared.database.connection import get_db_connection

logger = logging.getLogger(__name__)

router = APIRouter()

class Notification(BaseModel):
    id: int
    type: str
    icon: str
    title: str
    message: str
    time: str
    unread: bool
    color: str
    rfp_id: Optional[str] = None

class NotificationsResponse(BaseModel):
    notifications: List[Notification]
    unread_count: int

@router.get("/list", response_model=NotificationsResponse)
async def get_notifications():
    """
    Get system notifications based on RFP status and values
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        notifications = []
        notification_id = 1
        
        # 1. High-Value RFP Alerts (>1M)
        cursor.execute("""
            SELECT rfp_id, title, total_estimate, discovered_at
            FROM rfps
            WHERE total_estimate > 1000000
            ORDER BY discovered_at DESC
            LIMIT 3
        """)
        high_value_rfps = cursor.fetchall()
        
        for rfp in high_value_rfps:
            rfp_id, title, total_estimate, discovered_at = rfp
            time_ago = get_time_ago(discovered_at)
            
            notifications.append({
                "id": notification_id,
                "type": "alert",
                "icon": "DollarSign",
                "title": "🚨 High-Value RFP Alert",
                "message": f"{title} - Estimated value: ₹{format_currency(total_estimate)}",
                "time": time_ago,
                "unread": is_recent(discovered_at, hours=24),
                "color": "text-red-600 bg-red-50",
                "rfp_id": rfp_id
            })
            notification_id += 1
        
        # 2. Recently Completed RFPs
        cursor.execute("""
            SELECT rfp_id, title, updated_at, match_score
            FROM rfps
            WHERE status = 'completed'
            ORDER BY updated_at DESC
            LIMIT 3
        """)
        completed_rfps = cursor.fetchall()
        
        for rfp in completed_rfps:
            rfp_id, title, updated_at, match_score = rfp
            time_ago = get_time_ago(updated_at)
            match_pct = int((match_score or 0) * 100)
            
            notifications.append({
                "id": notification_id,
                "type": "success",
                "icon": "CheckCircle",
                "title": "✅ RFP Processing Complete",
                "message": f"{title} - {match_pct}% match found",
                "time": time_ago,
                "unread": is_recent(updated_at, hours=6),
                "color": "text-primary-600 bg-primary-50",
                "rfp_id": rfp_id
            })
            notification_id += 1
        
        # 3. Pending/New RFPs
        cursor.execute("""
            SELECT rfp_id, title, discovered_at
            FROM rfps
            WHERE status = 'new' OR status = 'pending'
            ORDER BY discovered_at DESC
            LIMIT 3
        """)
        pending_rfps = cursor.fetchall()
        
        for rfp in pending_rfps:
            rfp_id, title, discovered_at = rfp
            time_ago = get_time_ago(discovered_at)
            
            notifications.append({
                "id": notification_id,
                "type": "info",
                "icon": "AlertCircle",
                "title": "⏳ RFP Pending Review",
                "message": f"{title} - Awaiting processing",
                "time": time_ago,
                "unread": is_recent(discovered_at, hours=12),
                "color": "text-blue-600 bg-blue-50",
                "rfp_id": rfp_id
            })
            notification_id += 1
        
        # 4. Processing RFPs
        cursor.execute("""
            SELECT rfp_id, title, updated_at
            FROM rfps
            WHERE status = 'processing'
            ORDER BY updated_at DESC
            LIMIT 2
        """)
        processing_rfps = cursor.fetchall()
        
        for rfp in processing_rfps:
            rfp_id, title, updated_at = rfp
            time_ago = get_time_ago(updated_at)
            
            notifications.append({
                "id": notification_id,
                "type": "info",
                "icon": "Loader",
                "title": "⚙️ RFP Processing",
                "message": f"{title} - Analysis in progress",
                "time": time_ago,
                "unread": is_recent(updated_at, hours=2),
                "color": "text-orange-600 bg-orange-50",
                "rfp_id": rfp_id
            })
            notification_id += 1
        
        # 5. Deadline Reminders (within 3 days)
        cursor.execute("""
            SELECT rfp_id, title, deadline
            FROM rfps
            WHERE deadline > NOW() 
            AND deadline <= NOW() + INTERVAL '3 days'
            AND status != 'completed'
            ORDER BY deadline ASC
            LIMIT 3
        """)
        deadline_rfps = cursor.fetchall()
        
        for rfp in deadline_rfps:
            rfp_id, title, deadline = rfp
            days_left = (deadline - datetime.now()).days
            time_text = f"{days_left} day{'s' if days_left != 1 else ''} left"
            
            notifications.append({
                "id": notification_id,
                "type": "warning",
                "icon": "Clock",
                "title": "⏰ Deadline Approaching",
                "message": f"{title} - {time_text}",
                "time": "Reminder",
                "unread": True,
                "color": "text-orange-600 bg-orange-50",
                "rfp_id": rfp_id
            })
            notification_id += 1
        
        cursor.close()
        conn.close()
        
        # Sort by unread first, then by ID (most recent)
        notifications.sort(key=lambda x: (not x['unread'], -x['id']))
        
        unread_count = sum(1 for n in notifications if n['unread'])
        
        return NotificationsResponse(
            notifications=notifications[:10],  # Limit to 10 most relevant
            unread_count=unread_count
        )
        
    except Exception as e:
        logger.error(f"Error fetching notifications: {str(e)}")
        # Return empty notifications on error
        return NotificationsResponse(notifications=[], unread_count=0)


def get_time_ago(dt: datetime) -> str:
    """Convert datetime to human-readable time ago"""
    if not dt:
        return "Unknown"
    
    now = datetime.now()
    if dt.tzinfo:
        from datetime import timezone
        now = datetime.now(timezone.utc)
    
    diff = now - dt
    
    if diff.days > 0:
        if diff.days == 1:
            return "1 day ago"
        return f"{diff.days} days ago"
    
    hours = diff.seconds // 3600
    if hours > 0:
        if hours == 1:
            return "1 hour ago"
        return f"{hours} hours ago"
    
    minutes = diff.seconds // 60
    if minutes > 0:
        if minutes == 1:
            return "1 minute ago"
        return f"{minutes} minutes ago"
    
    return "Just now"


def is_recent(dt: datetime, hours: int = 24) -> bool:
    """Check if datetime is within the last N hours"""
    if not dt:
        return False
    
    now = datetime.now()
    if dt.tzinfo:
        from datetime import timezone
        now = datetime.now(timezone.utc)
    
    return (now - dt) < timedelta(hours=hours)


def format_currency(amount: float) -> str:
    """Format currency in Indian notation"""
    if amount >= 10000000:  # 1 Crore
        return f"{amount/10000000:.2f}Cr"
    elif amount >= 100000:  # 1 Lakh
        return f"{amount/100000:.2f}L"
    else:
        return f"{amount:,.0f}"
