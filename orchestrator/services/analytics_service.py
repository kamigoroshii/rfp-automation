"""
Analytics Service - Business logic for analytics operations
"""
import logging
from typing import Optional
from datetime import datetime, timedelta
from collections import defaultdict

from shared.database.connection import get_db_manager

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for analytics operations"""
    
    async def get_dashboard_data(self) -> dict:
        """Get dashboard overview data"""
        try:
            db = get_db_manager()
            if not db:
                 # Mock data
                 return {
                    "overview": {
                        "total_rfps": 15,
                        "completed": 12,
                        "in_progress": 2,
                        "new": 1,
                        "avg_match_accuracy": 0.85,
                        "avg_processing_time": 2.5,
                        "win_rate": 0.4
                    }
                 }

            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Get overview stats
                    cursor.execute("""
                        SELECT 
                            COUNT(*) as total_rfps,
                            COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
                            COUNT(CASE WHEN status = 'processing' THEN 1 END) as in_progress,
                            COUNT(CASE WHEN status = 'new' THEN 1 END) as new,
                            AVG(match_score) as avg_match_accuracy,
                            AVG(EXTRACT(EPOCH FROM (updated_at - discovered_at))/60) as avg_processing_time
                        FROM rfps
                    """)
                    
                    row = cursor.fetchone()
                    
                    # Get win rate
                    cursor.execute("""
                        SELECT 
                            COUNT(CASE WHEN outcome = 'won' THEN 1 END)::float / 
                            NULLIF(COUNT(*), 0) as win_rate
                        FROM feedback
                    """)
                    
                    win_rate_row = cursor.fetchone()
                    
                    return {
                        "overview": {
                            "total_rfps": int(row[0]) if row[0] else 0,
                            "completed": int(row[1]) if row[1] else 0,
                            "in_progress": int(row[2]) if row[2] else 0,
                            "new": int(row[3]) if row[3] else 0,
                            "avg_match_accuracy": float(row[4]) if row[4] else 0.0,
                            "avg_processing_time": float(row[5]) if row[5] else 0.0,
                            "win_rate": float(win_rate_row[0]) if win_rate_row and win_rate_row[0] else 0.0
                        }
                    }
        except Exception as e:
            logger.error(f"Error fetching dashboard data: {str(e)}")
            # Fallback mock
            return {
                "overview": {
                    "total_rfps": 0, "completed": 0, "in_progress": 0, "new": 0,
                    "avg_match_accuracy": 0.0, "avg_processing_time": 0.0, "win_rate": 0.0
                }
            }
    
    async def get_trends(self, period: str = "month", metric: str = "rfps") -> list:
        """Get trend data"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Determine date grouping based on period
            if period == "week":
                date_trunc = "day"
                days_back = 7
            elif period == "month":
                date_trunc = "day"
                days_back = 30
            elif period == "quarter":
                date_trunc = "week"
                days_back = 90
            else:
                date_trunc = "month"
                days_back = 365
            
            start_date = datetime.now() - timedelta(days=days_back)
            
            if metric == "rfps":
                cursor.execute(f"""
                    SELECT 
                        DATE_TRUNC('{date_trunc}', discovered_at) as period,
                        COUNT(*) as count
                    FROM rfps
                    WHERE discovered_at >= %s
                    GROUP BY period
                    ORDER BY period
                """, (start_date,))
            elif metric == "revenue":
                cursor.execute(f"""
                    SELECT 
                        DATE_TRUNC('{date_trunc}', r.discovered_at) as period,
                        SUM(r.total_estimate) as total
                    FROM rfps r
                    WHERE r.discovered_at >= %s
                    GROUP BY period
                    ORDER BY period
                """, (start_date,))
            elif metric == "win_rate":
                cursor.execute(f"""
                    SELECT 
                        DATE_TRUNC('{date_trunc}', submitted_at) as period,
                        COUNT(CASE WHEN outcome = 'won' THEN 1 END)::float / 
                        NULLIF(COUNT(*), 0) as win_rate
                    FROM feedback
                    WHERE submitted_at >= %s
                    GROUP BY period
                    ORDER BY period
                """, (start_date,))
            
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            
            trends = []
            for row in rows:
                trends.append({
                    "date": row[0].isoformat() if row[0] else None,
                    "value": float(row[1]) if row[1] else 0.0
                })
            
            return trends
        except Exception as e:
            logger.error(f"Error fetching trends: {str(e)}")
            raise
    
    async def get_performance_metrics(self) -> dict:
        """Get system performance metrics"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Processing time stats
            cursor.execute("""
                SELECT 
                    AVG(EXTRACT(EPOCH FROM (updated_at - discovered_at))/60) as avg_time,
                    MIN(EXTRACT(EPOCH FROM (updated_at - discovered_at))/60) as min_time,
                    MAX(EXTRACT(EPOCH FROM (updated_at - discovered_at))/60) as max_time
                FROM rfps
                WHERE status = 'completed'
            """)
            
            time_row = cursor.fetchone()
            
            # Match accuracy stats
            cursor.execute("""
                SELECT 
                    AVG(match_score) as avg_accuracy,
                    MIN(match_score) as min_accuracy,
                    MAX(match_score) as max_accuracy
                FROM rfps
                WHERE match_score IS NOT NULL
            """)
            
            accuracy_row = cursor.fetchone()
            
            # Success rate
            cursor.execute("""
                SELECT 
                    COUNT(CASE WHEN status = 'completed' THEN 1 END)::float / 
                    NULLIF(COUNT(*), 0) as success_rate
                FROM rfps
            """)
            
            success_row = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return {
                "processing_time": {
                    "average": float(time_row[0]) if time_row and time_row[0] else 0.0,
                    "min": float(time_row[1]) if time_row and time_row[1] else 0.0,
                    "max": float(time_row[2]) if time_row and time_row[2] else 0.0
                },
                "match_accuracy": {
                    "average": float(accuracy_row[0]) if accuracy_row and accuracy_row[0] else 0.0,
                    "min": float(accuracy_row[1]) if accuracy_row and accuracy_row[1] else 0.0,
                    "max": float(accuracy_row[2]) if accuracy_row and accuracy_row[2] else 0.0
                },
                "success_rate": float(success_row[0]) if success_row and success_row[0] else 0.0
            }
        except Exception as e:
            logger.error(f"Error fetching performance metrics: {str(e)}")
            raise
    
    async def get_monthly_report(self, year: int, month: int) -> dict:
        """Get monthly report"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            
            # RFP stats
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
                    SUM(total_estimate) as total_value
                FROM rfps
                WHERE discovered_at >= %s AND discovered_at < %s
            """, (start_date, end_date))
            
            rfp_row = cursor.fetchone()
            
            # Feedback stats
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN outcome = 'won' THEN 1 END) as won,
                    AVG(match_accuracy) as avg_accuracy
                FROM feedback
                WHERE submitted_at >= %s AND submitted_at < %s
            """, (start_date, end_date))
            
            feedback_row = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return {
                "period": {
                    "year": year,
                    "month": month,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat()
                },
                "rfps": {
                    "total": int(rfp_row[0]) if rfp_row[0] else 0,
                    "completed": int(rfp_row[1]) if rfp_row[1] else 0,
                    "total_value": float(rfp_row[2]) if rfp_row[2] else 0.0
                },
                "outcomes": {
                    "total_feedback": int(feedback_row[0]) if feedback_row and feedback_row[0] else 0,
                    "won": int(feedback_row[1]) if feedback_row and feedback_row[1] else 0,
                    "avg_accuracy": float(feedback_row[2]) if feedback_row and feedback_row[2] else 0.0
                }
            }
        except Exception as e:
            logger.error(f"Error generating monthly report: {str(e)}")
            raise
    
    async def get_win_rate(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> dict:
        """Get win rate statistics"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if not start_date:
                start_date = datetime.now() - timedelta(days=90)
            if not end_date:
                end_date = datetime.now()
            
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN outcome = 'won' THEN 1 END) as won,
                    COUNT(CASE WHEN outcome = 'lost' THEN 1 END) as lost,
                    COUNT(CASE WHEN outcome = 'pending' THEN 1 END) as pending,
                    COUNT(CASE WHEN outcome = 'won' THEN 1 END)::float / 
                    NULLIF(COUNT(*), 0) as win_rate
                FROM feedback
                WHERE submitted_at >= %s AND submitted_at <= %s
            """, (start_date, end_date))
            
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return {
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat()
                },
                "total_submissions": int(row[0]) if row[0] else 0,
                "won": int(row[1]) if row[1] else 0,
                "lost": int(row[2]) if row[2] else 0,
                "pending": int(row[3]) if row[3] else 0,
                "win_rate": float(row[4]) if row[4] else 0.0
            }
        except Exception as e:
            logger.error(f"Error fetching win rate: {str(e)}")
            raise
