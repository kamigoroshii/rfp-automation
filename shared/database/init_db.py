"""
Database initialization script
"""
import os
import sys
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

load_dotenv()
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    """Initialize database with schema"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 5432)),
            database=os.getenv("DB_NAME", "rfp_automation"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres")
        )
        cursor = conn.cursor()
        
        # Read schema file
        schema_path = Path(__file__).parent / 'schema.sql'
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema
        logger.info("Creating database schema...")
        cursor.execute(schema_sql)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        logger.info("Database initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False


if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
