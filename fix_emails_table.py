"""
Fix Emails Table - Add Missing Columns
This script adds the processed_at column to the existing emails table
"""
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'rfp_automation'),
    'user': os.getenv('DB_USER', 'rfp_user'),
    'password': os.getenv('DB_PASSWORD', 'rfp_password')
}

def fix_emails_table():
    """Add missing columns to emails table"""
    try:
        print("🔌 Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("🔨 Checking emails table structure...")
        
        # Check if processed_at column exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'emails' AND column_name = 'processed_at'
        """)
        
        if cursor.fetchone() is None:
            print("  → Adding 'processed_at' column...")
            cursor.execute("""
                ALTER TABLE emails 
                ADD COLUMN IF NOT EXISTS processed_at TIMESTAMP
            """)
            print("  ✅ Added 'processed_at' column")
        else:
            print("  ✅ 'processed_at' column already exists")
        
        # Check if processed column exists (old schema)
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'emails' AND column_name = 'processed'
        """)
        
        if cursor.fetchone() is not None:
            print("  → Removing old 'processed' column...")
            cursor.execute("""
                ALTER TABLE emails 
                DROP COLUMN IF EXISTS processed
            """)
            print("  ✅ Removed old 'processed' column")
        
        # Verify final structure
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'emails'
            ORDER BY ordinal_position
        """)
        
        print("\n📋 Final emails table structure:")
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 SUCCESS! Emails table is now fixed")
        print("\nYou can now run: python add_sample_emails.py")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nMake sure:")
        print("  1. PostgreSQL is running")
        print("  2. Database 'rfp_automation' exists")
        print("  3. .env file has correct database credentials")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  🔧 FIXING EMAILS TABLE")
    print("="*60 + "\n")
    fix_emails_table()
    print("\n" + "="*60 + "\n")
