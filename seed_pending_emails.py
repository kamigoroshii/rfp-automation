
import asyncio
import json
import uuid
from datetime import datetime
from shared.database.connection import get_db_manager

async def seed_pending_emails():
    """
    Seeds the database with 'Pending' emails for the 'Import from Email' demo flow.
    """
    print("Connecting to database...")
    db = get_db_manager()
    if not db:
        print("Database not available!")
        return

    emails = [
        {
            "subject": "Inquiry: 12000 BTU Split AC Units for Housing Project",
            "sender": "purchase@buildwell-homes.com",
            "body": "Hi Team,\n\nWe require pricing for 50 units of 1.5 Ton (12000 BTU) Split Inverter ACs. \nRating: 5 Star\nCondenser: Copper\n\nDelivery required by 1st Jan 2026 at our Bangalore site.\n\nRegards,\nRajesh Kumar",
            "date": "2025-12-09 09:30:00"
        },
        {
            "subject": "RFP: Fire Alarm System for Datacenter",
            "sender": "infra@netmagic-dc.com",
            "body": "Dear Vendor,\n\nPlease find requirements for Addressable Fire Alarm System.\n- 500+ Detectors\n- 4 Loop Panel\n- Integration with BMS required\n\nSubmit technical bid by next week.",
            "date": "2025-12-09 10:15:00"
        },
        {
            "subject": "Requirement: 500kVA Diesel Generator Set",
            "sender": "procurement@karnataka-textiles.com",
            "body": "We are looking for a 500kVA DG Set (Caterpillar/Cummins engine preferred). \nShould include AMF Panel and Acoustic Enclosure.\nWarranty: 2 Years minimum.\n\nInstallation location: Mysore Factory.",
            "date": "2025-12-09 11:00:00"
        }
    ]

    with db.get_connection() as conn:
        with conn.cursor() as cursor:
            print("Seeding Pending Emails...")
            for e in emails:
                email_id = f"email-pending-{str(uuid.uuid4())[:8]}"
                cursor.execute("""
                    INSERT INTO emails (email_id, subject, sender, received_at, body, status, attachments)
                    VALUES (%s, %s, %s, %s, %s, 'pending', '[]')
                    ON CONFLICT (email_id) DO NOTHING
                """, (
                    email_id,
                    e['subject'],
                    e['sender'],
                    datetime.strptime(e['date'], "%Y-%m-%d %H:%M:%S"),
                    e['body']
                ))
            conn.commit()
    
    print("Successfully seeded Pending Emails!")

if __name__ == "__main__":
    asyncio.run(seed_pending_emails())
