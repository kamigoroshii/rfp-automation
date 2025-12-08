
import psycopg2
import os
import uuid
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'rfp_automation'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

SAMPLE_EMAILS = [
    {
        "subject": "RFP Request - Project Alpha Cabling",
        "sender": "procurement@construction-corp.com",
        "body": "Please find attached the specifications for the Alpha Cabling project. Deadline is next Friday.",
        "attachments": [{"filename": "specs_alpha.pdf", "path": "/uploads/mock_specs_alpha.pdf", "size": 102400}],
        "status": "processed",
        "received_offset_hours": 2
    },
    {
        "subject": "Urgent: Supply of 11kV Cables",
        "sender": "tenders@grid-utility.org",
        "body": "We are looking for immediate supply of 5km of 11kV XLPE cables. See details attached.",
        "attachments": [{"filename": "tender_11kv_req.pdf", "path": "/uploads/mock_tender_11kv.pdf", "size": 204800}],
        "status": "pending",
        "received_offset_hours": 5
    },
    {
        "subject": "Meeting Notes - Q4 Planning",
        "sender": "internal@ourcompany.com",
        "body": "Just sending over the notes from yesterday.",
        "attachments": [],
        "status": "ignored",
        "received_offset_hours": 24
    },
    {
        "subject": "New Vendor Registration",
        "sender": "admin@supplier-portal.net",
        "body": "Your vendor registration has been approved. Please log in to complete your profile.",
        "attachments": [{"filename": "guide.pdf", "path": "/uploads/guide.pdf", "size": 55000}],
        "status": "pending",
        "received_offset_hours": 48
    }
]

def add_sample_emails():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("📧 Adding sample emails to Inbox...")
        
        for email in SAMPLE_EMAILS:
            email_id = f"email-sample-{str(uuid.uuid4())[:8]}"
            received_at = datetime.now() - timedelta(hours=email["received_offset_hours"])
            
            cursor.execute("""
                INSERT INTO emails 
                (email_id, subject, sender, received_at, body, attachments, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (email_id) DO NOTHING
            """, (
                email_id,
                email["subject"],
                email["sender"],
                received_at,
                email["body"],
                json.dumps(email["attachments"]),
                email["status"]
            ))
            print(f"  + Added: {email['subject']}")
            
        cursor.close()
        conn.close()
        print("✅ Sample emails added successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_sample_emails()
