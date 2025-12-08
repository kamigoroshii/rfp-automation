"""
Add Sample Email Data to Database
This script populates the emails table with sample data for testing
"""
import psycopg2
from datetime import datetime, timedelta
import json
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

# Sample email data
SAMPLE_EMAILS = [
    {
        'email_id': 'email-001',
        'subject': 'RFP for 11kV XLPE Cable Supply - Urgent Requirement',
        'sender': 'procurement@powergrid.com',
        'received_at': datetime.now() - timedelta(days=2),
        'body': '''Dear Supplier,

We have an urgent requirement for 11kV XLPE cables for our upcoming substation project.

Requirements:
- 500 meters of 11kV XLPE cable, 185 sq.mm
- Aluminum conductor
- IS 7098 Part 2 compliant
- Delivery within 30 days

Please provide your best quotation along with technical specifications and test certificates.

Deadline for submission: 15 days from today.

Best regards,
Procurement Team
Power Grid Corporation''',
        'attachments': json.dumps(['rfp_cable_specifications.pdf', 'technical_requirements.pdf']),
        'status': 'processed',
        'processed_at': datetime.now() - timedelta(days=1),
        'rfp_id': 'RFP-2025-A1B2C3D4'
    },
    {
        'email_id': 'email-002',
        'subject': '100kVA Distribution Transformer Quotation Request',
        'sender': 'buyer@electricalco.in',
        'received_at': datetime.now() - timedelta(days=1),
        'body': '''Hello,

We need pricing for the following:

Product: 100kVA Distribution Transformer
Voltage: 11kV/433V
Type: Oil-filled, outdoor
Quantity: 5 units

Please include:
- Unit price
- Delivery time
- Warranty terms
- Testing charges

Attached are the detailed specifications.

Thanks,
Electrical Co. Procurement''',
        'attachments': json.dumps(['transformer_specs.pdf']),
        'status': 'processed',
        'processed_at': datetime.now(),
        'rfp_id': 'RFP-2025-E5F6G7H8'
    },
    {
        'email_id': 'email-003',
        'subject': 'Government Tender - Electrical Equipment Supply',
        'sender': 'tender@govt.in',
        'received_at': datetime.now() - timedelta(hours=3),
        'body': '''TENDER NOTICE

Tender No: GOV/ELEC/2025/123
Subject: Supply of Electrical Equipment

The Government of India invites sealed tenders for supply of various electrical equipment including:
- HT Cables
- Transformers
- Switchgear
- Protection equipment

Total estimated value: Rs. 75 Lakhs

Last date for submission: 15 days from publication
Technical bid opening: 20 days from publication

Detailed tender document and specifications are attached.

For queries, contact: tender@govt.in''',
        'attachments': json.dumps(['tender_document.pdf', 'technical_specs.xlsx', 'terms_conditions.pdf']),
        'status': 'pending',
        'processed_at': None,
        'rfp_id': None
    },
    {
        'email_id': 'email-004',
        'subject': 'Re: Cable Testing Requirements - Clarification Needed',
        'sender': 'quality@testlab.com',
        'received_at': datetime.now() - timedelta(hours=1),
        'body': '''Hi,

Regarding the cable samples you sent for testing, we need clarification on:

1. Type test or routine test?
2. IS 7098 Part 1 or Part 2?
3. Voltage withstand test duration?
4. Partial discharge test required?

Please confirm so we can proceed with the testing schedule.

Regards,
Quality Assurance Team
Test Lab India''',
        'attachments': json.dumps([]),
        'status': 'pending',
        'processed_at': None,
        'rfp_id': None
    },
    {
        'email_id': 'email-005',
        'subject': 'Switchgear RFP - Metro Rail Project',
        'sender': 'projects@metrorail.gov.in',
        'received_at': datetime.now() - timedelta(minutes=30),
        'body': '''Dear Vendors,

Metro Rail Corporation invites proposals for supply and installation of:

11kV Switchgear Panels
- Ring Main Units: 10 nos
- Metering Panels: 5 nos
- Protection Relays: Numerical type
- SCADA integration required

Project value: Approx. Rs. 1.2 Crores
Timeline: 90 days from award

Pre-bid meeting: 5 days from today
Bid submission deadline: 20 days from today

Please find detailed specifications in the attached RFP document.

Metro Rail Corporation
Infrastructure Projects Division''',
        'attachments': json.dumps(['metro_rfp_switchgear.pdf', 'site_layout.pdf']),
        'status': 'pending',
        'processed_at': None,
        'rfp_id': None
    }
]

def add_sample_emails():
    """Add sample emails to database"""
    try:
        print("🔌 Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("📧 Adding sample emails...")
        
        for email in SAMPLE_EMAILS:
            try:
                cursor.execute("""
                    INSERT INTO emails (email_id, subject, sender, received_at, body, attachments, status, processed_at, rfp_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (email_id) DO NOTHING
                """, (
                    email['email_id'],
                    email['subject'],
                    email['sender'],
                    email['received_at'],
                    email['body'],
                    email['attachments'],
                    email['status'],
                    email['processed_at'],
                    email['rfp_id']
                ))
                print(f"  ✅ Added: {email['subject'][:50]}...")
            except Exception as e:
                print(f"  ❌ Error adding email {email['email_id']}: {str(e)}")
        
        conn.commit()
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM emails")
        count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        print(f"\n🎉 SUCCESS! {count} emails now in database")
        print("\n📬 Refresh your Email Inbox page to see the emails!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nMake sure:")
        print("  1. PostgreSQL is running")
        print("  2. Database 'rfp_automation' exists")
        print("  3. Table 'emails' exists (run python run_migration.py)")
        print("  4. .env file has correct database credentials")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  📧 ADDING SAMPLE EMAIL DATA")
    print("="*60 + "\n")
    add_sample_emails()
    print("\n" + "="*60 + "\n")
