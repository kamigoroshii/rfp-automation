
import asyncio
import uuid
import json
from datetime import datetime, timedelta
from shared.database.connection import get_db_manager

async def add_failed_rfps():
    print("Connecting to database...")
    db = get_db_manager()
    if not db:
        print("Database not available!")
        return

    base_time = datetime.now()

    failed_rfps = [
        {
            "title": "Aerospace: Titanium Alloy Sheets (Gr 5)",
            "source": "tender@boeing-supply-demo.com",
            "scope": "Supply of 500 Sheets of Titanium Grade 5 (Ti-6Al-4V) for aircraft fuselage.\nThickness: 2mm\nCertification: AMS 4911",
            "reason": "No matching product in catalog (Grade 5 Titanium)",
            "advice": "Initiate vendor onboarding with 'TitanEx Corp' or 'AeroMetals Inc'. Update catalog with ASTM B265 compliant materials.",
            "score": 0.15,
            "est_val": 50000000.00
        },
        {
            "title": "Municipal Tender: Bio-Medical Waste Incinerator",
            "source": "health-dept@city-corp.gov",
            "scope": "Design and Supply of 500kg/hr Waste Incinerator.\nMust include Wet Scrubber and continuous emission monitoring.",
            "reason": "Specification mismatch: Capacity gap (Req: 500kg/hr, Max Available: 200kg/hr)",
            "advice": "R&D required for higher capacity model. Alternatively, propose 3x 200kg/hr cascade setup if tender allows deviation.",
            "score": 0.35,
            "est_val": 25000000.00
        }
    ]

    with db.get_connection() as conn:
        with conn.cursor() as cursor:
            for rfp in failed_rfps:
                rfp_id = f"RFP-FAIL-{str(uuid.uuid4())[:8]}"
                print(f"Adding Failed RFP: {rfp['title']}")
                
                # Prepare specifications JSON with failure reason
                specs_json = json.dumps({
                    "failure_reason": rfp['reason'],
                    "improvement_advice": rfp['advice']
                })
                
                # Insert RFP with 'failed' status
                cursor.execute("""
                    INSERT INTO rfps 
                    (rfp_id, title, source, deadline, scope, testing_requirements, 
                     discovered_at, status, match_score, total_estimate, specifications, attachments)
                    VALUES (%s, %s, %s, %s, %s, '[]', %s, 'failed', %s, %s, %s, '[]')
                    ON CONFLICT (rfp_id) DO NOTHING
                """, (
                    rfp_id,
                    rfp['title'],
                    rfp['source'],
                    (base_time + timedelta(days=10)).isoformat(),
                    rfp['scope'],
                    base_time - timedelta(days=2),
                    rfp['score'],
                    rfp['est_val'],
                    specs_json
                ))
                
                # Ensure dummy product exists
                cursor.execute("""
                    INSERT INTO products (sku, product_name, category, unit_price, specifications, stock_status)
                    VALUES ('GENERIC-FAIL', 'Generic Placeholder', 'Misc', 0, '{}', 'Out of Stock')
                    ON CONFLICT (sku) DO NOTHING
                """)

                # We can verify why it failed by looking at matches (empty or low score)
                # Let's insert a dummy low match
                cursor.execute("""
                    INSERT INTO product_matches
                    (rfp_id, sku, product_name, match_score, specification_alignment)
                    VALUES (%s, 'GENERIC-FAIL', 'Generic Item', %s, '{}')
                """, (rfp_id, rfp['score']))
            
            conn.commit()
    
    print("Successfully added Failed RFPs!")

if __name__ == "__main__":
    asyncio.run(add_failed_rfps())
