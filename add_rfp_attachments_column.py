"""
Add attachments column to rfps table
This allows RFPs to store PDF attachments from emails
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'rfp_automation'),
    'user': os.getenv('DB_USER', 'rfp_user'),
    'password': os.getenv('DB_PASSWORD', 'rfp_password')
}

def add_attachments_column():
    """Add attachments column to rfps table"""
    try:
        print("\n" + "="*60)
        print("  📎 ADDING ATTACHMENTS COLUMN TO RFPS TABLE")
        print("="*60 + "\n")
        
        print("🔌 Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'rfps' AND column_name = 'attachments'
        """)
        
        if cursor.fetchone():
            print("✅ Attachments column already exists")
        else:
            print("🔨 Adding attachments column...")
            cursor.execute("""
                ALTER TABLE rfps 
                ADD COLUMN attachments JSONB DEFAULT '[]'::jsonb
            """)
            print("✅ Attachments column added successfully!")
        
        # Verify
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'rfps'
            ORDER BY ordinal_position
        """)
        
        print("\n📋 RFPs table structure:")
        for row in cursor.fetchall():
            print(f"  - {row[0]}: {row[1]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 SUCCESS! RFPs table is ready for attachments")
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure:")
        print("  1. PostgreSQL is running")
        print("  2. Database 'rfp_automation' exists")
        print("  3. .env file has correct credentials")

if __name__ == "__main__":
    add_attachments_column()
