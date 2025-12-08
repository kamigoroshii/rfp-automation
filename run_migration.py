"""
Safe Database Migration Script
Creates 'emails' and 'audit_reports' tables if they don't exist.
Skips existing tables to avoid errors.
"""
import logging
import sys
import os

# Ensure we can import from shared
sys.path.append(os.getcwd())

try:
    from shared.database.connection import get_db_connection
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you are in the f:\\eytech directory and venv is activated.")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def run_safe_migration():
    print("🔌 Connecting to database...")
    try:
        conn = get_db_connection()
        conn.autocommit = True  # Ensure immediate execution
        cursor = conn.cursor()
        
        # 1. Create emails table
        print("🔨 Checking 'emails' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                email_id VARCHAR(50) PRIMARY KEY,
                subject TEXT NOT NULL,
                sender VARCHAR(255),
                received_at TIMESTAMP,
                body TEXT,
                attachments JSONB,
                status VARCHAR(20) DEFAULT 'pending',
                processed_at TIMESTAMP,
                rfp_id VARCHAR(50),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # 2. Create emails indexes (safe with IF NOT EXISTS)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_emails_status ON emails(status);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_emails_rfp_id ON emails(rfp_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_emails_received_at ON emails(received_at);")
        print("✅ 'emails' table and indexes ready.")

        # 3. Create audit_reports table
        print("🔨 Checking 'audit_reports' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_reports (
                audit_id VARCHAR(50) PRIMARY KEY,
                rfp_id VARCHAR(50),
                audit_timestamp TIMESTAMP DEFAULT NOW(),
                overall_recommendation VARCHAR(20) NOT NULL,
                compliance_score FLOAT,
                critical_issues_count INTEGER DEFAULT 0,
                summary TEXT,
                rfp_validation JSONB,
                match_validation JSONB,
                pricing_validation JSONB,
                details JSONB,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)

        # 4. Create audit_reports indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_rfp_id ON audit_reports(rfp_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_reports(audit_timestamp);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_recommendation ON audit_reports(overall_recommendation);")
        print("✅ 'audit_reports' table and indexes ready.")

        # 5. Verify creation
        print("\n🔍 Verifying tables...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('emails', 'audit_reports');
        """)
        found_tables = [row[0] for row in cursor.fetchall()]
        
        if 'emails' in found_tables and 'audit_reports' in found_tables:
            print("\n🎉 SUCCESS! All tables exist.")
            print(f"Found: {', '.join(found_tables)}")
        else:
            print("\n⚠️ WARNING: Some tables might be missing: " + str(found_tables))

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        return False

if __name__ == "__main__":
    run_safe_migration()
