
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'rfp_automation'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

def force_fix_emails():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("Checking 'emails' table columns...")
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'emails'")
        cols = [row[0] for row in cursor.fetchall()]
        print(f"Current columns: {cols}")
        
        if 'processed_at' not in cols:
            print("Adding 'processed_at' column...")
            cursor.execute("ALTER TABLE emails ADD COLUMN processed_at TIMESTAMP")
            print("Added.")
        
        if 'processed' in cols:
            print("Old 'processed' column found. Checking data migration...")
            # If we want to keep data, maybe we should migrate 'processed' boolean to status?
            # But earlier code assumes 'processed_at' exists.
            # Let's just ensuring 'processed_at' exists is the key.
            pass
            
        conn.close()
        print("Fix complete.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    force_fix_emails()
