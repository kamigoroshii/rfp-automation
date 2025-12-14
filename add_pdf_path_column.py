"""
Add pdf_path column to rfps table
"""
import logging
from shared.database.connection import get_db_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_pdf_path_column():
    """Add pdf_path column to rfps table if it doesn't exist"""
    try:
        db = get_db_manager()
        if not db:
            logger.error("Database connection unavailable")
            return False
        
        with db.get_connection() as conn:
            with conn.cursor() as cursor:
                # Check if column exists
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='rfps' AND column_name='pdf_path'
                """)
                
                if cursor.fetchone():
                    logger.info("✓ pdf_path column already exists in rfps table")
                else:
                    # Add column
                    cursor.execute("ALTER TABLE rfps ADD COLUMN pdf_path TEXT")
                    conn.commit()
                    logger.info("✓ Added pdf_path column to rfps table")
                
                # Add index
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_rfps_pdf_path ON rfps(pdf_path)
                """)
                conn.commit()
                logger.info("✓ Created index on pdf_path column")
                
                # Show summary
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total,
                        COUNT(pdf_path) as with_pdf,
                        COUNT(*) - COUNT(pdf_path) as without_pdf
                    FROM rfps
                """)
                row = cursor.fetchone()
                logger.info(f"✓ RFPs summary: {row[0]} total, {row[1]} with PDF, {row[2]} without PDF")
                
        return True
        
    except Exception as e:
        logger.error(f"Error adding pdf_path column: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Adding pdf_path column to rfps table...")
    success = add_pdf_path_column()
    if success:
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration failed!")
