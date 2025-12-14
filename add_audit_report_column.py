"""
Add audit_report column to rfps table
"""
from shared.database.connection import get_db_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_audit_report_column():
    """Add audit_report JSONB column to rfps table"""
    try:
        db = get_db_manager()
        
        with db.get_connection() as conn:
            with conn.cursor() as cursor:
                # Add audit_report column if it doesn't exist
                cursor.execute("""
                    ALTER TABLE rfps 
                    ADD COLUMN IF NOT EXISTS audit_report JSONB DEFAULT '{}'::jsonb
                """)
                
                conn.commit()
                logger.info("Successfully added audit_report column to rfps table")
                
    except Exception as e:
        logger.error(f"Error adding audit_report column: {str(e)}")
        raise

if __name__ == "__main__":
    add_audit_report_column()
    print("Migration complete!")
