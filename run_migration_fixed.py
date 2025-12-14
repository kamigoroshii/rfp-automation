"""
Migration script to add pdf_path column to rfps table.
Uses the existing database connection from shared module.
"""

import sys
import logging
from shared.database.connection import DatabaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration():
    """Add pdf_path column to rfps table"""
    
    db = DatabaseManager()
    
    if not db.is_available():
        logger.error("Database connection unavailable")
        print("❌ Migration failed - database not available!")
        return False
    
    try:
        print("Adding pdf_path column to rfps table...")
        
        # Get a connection
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Add the column
        cursor.execute("""
            ALTER TABLE rfps 
            ADD COLUMN IF NOT EXISTS pdf_path TEXT;
        """)
        
        # Add index for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_rfps_pdf_path ON rfps(pdf_path);
        """)
        
        # Commit the changes
        conn.commit()
        
        # Verify the column was added
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'rfps' AND column_name = 'pdf_path';
        """)
        
        result = cursor.fetchone()
        
        cursor.close()
        db.return_connection(conn)
        
        if result:
            print(f"✅ Column added successfully: {result[0]} ({result[1]})")
            return True
        else:
            print("❌ Column verification failed")
            return False
            
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
