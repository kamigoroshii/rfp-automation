"""
Database Initialization Script
Creates database, tables, and loads initial data
"""
import os
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from orchestrator.config import settings

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (default postgres database)
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (settings.DB_NAME,)
        )
        exists = cursor.fetchone()
        
        if not exists:
            logger.info(f"Creating database '{settings.DB_NAME}'...")
            cursor.execute(f"CREATE DATABASE {settings.DB_NAME}")
            logger.info(f"✅ Database '{settings.DB_NAME}' created successfully")
        else:
            logger.info(f"ℹ️  Database '{settings.DB_NAME}' already exists")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        logger.error(f"❌ Error creating database: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False


def create_tables():
    """Create all tables from schema.sql"""
    try:
        # Connect to the application database
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME
        )
        cursor = conn.cursor()
        
        # Read schema file
        schema_path = Path(__file__).parent / 'schema.sql'
        logger.info(f"Reading schema from {schema_path}...")
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema
        logger.info("Creating tables...")
        cursor.execute(schema_sql)
        conn.commit()
        
        logger.info("✅ All tables created successfully")
        
        # Verify tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        logger.info(f"📊 Created {len(tables)} tables:")
        for table in tables:
            logger.info(f"   - {table[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except FileNotFoundError:
        logger.error(f"❌ Schema file not found: {schema_path}")
        return False
    except psycopg2.Error as e:
        logger.error(f"❌ Error creating tables: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False


def verify_connection():
    """Verify database connection"""
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        logger.info(f"✅ Connected to PostgreSQL: {version[0][:50]}...")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        return False


def main():
    """Main initialization process"""
    logger.info("=" * 60)
    logger.info("🚀 Starting Database Initialization")
    logger.info("=" * 60)
    
    # Step 1: Verify connection to PostgreSQL server
    logger.info("\n📡 Step 1: Verifying PostgreSQL connection...")
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database='postgres'
        )
        conn.close()
        logger.info("✅ PostgreSQL server is accessible")
    except Exception as e:
        logger.error(f"❌ Cannot connect to PostgreSQL server: {e}")
        logger.error("\n💡 Please ensure:")
        logger.error("   1. PostgreSQL is installed and running")
        logger.error("   2. Credentials in .env are correct")
        logger.error("   3. PostgreSQL is accepting connections")
        return False
    
    # Step 2: Create database
    logger.info("\n🗄️  Step 2: Creating database...")
    if not create_database():
        return False
    
    # Step 3: Create tables
    logger.info("\n📊 Step 3: Creating tables...")
    if not create_tables():
        return False
    
    # Step 4: Verify connection
    logger.info("\n✅ Step 4: Verifying setup...")
    if not verify_connection():
        return False
    
    logger.info("\n" + "=" * 60)
    logger.info("🎉 Database initialization completed successfully!")
    logger.info("=" * 60)
    logger.info("\n📝 Next steps:")
    logger.info("   1. Run: python shared/database/seed_data.py")
    logger.info("   2. Start backend: uvicorn orchestrator.api.main:app --reload")
    logger.info("   3. Start frontend: cd frontend && npm run dev")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
