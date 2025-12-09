
import asyncio
import json
import uuid
from datetime import datetime, timedelta
from shared.database.connection import get_db_manager

async def reset_and_seed_fresh():
    print("Connecting to database...")
    db = get_db_manager()
    if not db:
        print("Database not available!")
        return

    # 1. CLEANUP ALL EXISTING DATA
    print("Cleaning up old data...")
    with db.get_connection() as conn:
        with conn.cursor() as cursor:
            # Delete in order of dependencies
            cursor.execute("DELETE FROM pricing_breakdown")
            cursor.execute("DELETE FROM product_matches")
            # Unlink emails from RFPs first if necessary, or just delete emails that reference RFPs?
            # Emails reference RFPs via rfp_id? No, RFPs reference Emails via source_email_id sometimes.
            # Actually, emails table has rfp_id foreign key? Let's check schema/models.
            # Assuming 'emails' has 'rfp_id'.
            cursor.execute("DELETE FROM emails") 
            cursor.execute("DELETE FROM rfps")
            conn.commit()
    print("Database wiped clean.")

    # 2. DEFINING NEW FRESh SAMPLE DATA
    base_time = datetime.now()

    demos = [
        {
            "id_suffix": "MRI",
            "title": "Hospital Tender: 3T MRI Scanner Procurement",
            "sender": "Dr. Sarah Khan <director@apollo-hospitals-demo.com>",
            "scope": "Supply, Installation, and Maintenance of a 3 Tesla MRI Scanner for the new Radiology wing.\nRequirements:\n- Field Strength: 3T\n- Bore Size: 70cm\n- Gradient Strength: >45 mT/m\n- Warranty: 5 Years Comprehensive",
            "est_val": 120000000.00,
            "sku_rec": "MED-MRI-3T-PRO",
            "products": [
                ("MED-MRI-3T-PRO", "3T MRI Scanner Pro 70cm", "Medical", 95000000.00),
                ("MED-MRI-1.5T", "1.5T MRI Scanner Standard", "Medical", 60000000.00)
            ],
            "matches": [
                {"sku": "MED-MRI-3T-PRO", "score": 0.99, "specs": {"field_strength": "exact", "bore": "exact"}},
                {"sku": "MED-MRI-1.5T", "score": 0.45, "specs": {"field_strength": "low"}}
            ],
            "pricing": [
                {"sku": "MED-MRI-3T-PRO", "qty": 1, "unit": 95000000, "delivered": 95000000, "install": 2500000},
                {"sku": "MED-MRI-1.5T", "qty": 1, "unit": 60000000, "delivered": 60000000, "install": 2000000}
            ]
        },
        {
            "id_suffix": "BRIDGE",
            "title": "Infra Project: TMT Steel Rebar Supply (Grade Fe 550D)",
            "sender": "Project Mgr <procurement@lnt-infra-demo.com>",
            "scope": "Supply of 5000 MT of TMT Rebar for the Coastal Road Project.\nSpecs:\n- Grade: Fe 550D\n- Diameter: Mix of 8mm, 12mm, 16mm, 25mm\n- Certification: IS 1786:2008\n- Delivery: Phased over 6 months",
            "est_val": 350000000.00,
            "sku_rec": "STEEL-TMT-550D",
            "products": [
                ("STEEL-TMT-550D", "TMT Rebar Fe 550D per MT", "Construction", 68000.00),
                ("STEEL-TMT-500", "TMT Rebar Fe 500 per MT", "Construction", 65000.00)
            ],
            "matches": [
                {"sku": "STEEL-TMT-550D", "score": 0.98, "specs": {"grade": "exact", "standard": "compliant"}},
                {"sku": "STEEL-TMT-500", "score": 0.88, "specs": {"grade": "acceptable_alt"}}
            ],
            "pricing": [
                {"sku": "STEEL-TMT-550D", "qty": 5000, "unit": 68000, "delivered": 340000000, "install": 0},
                {"sku": "STEEL-TMT-500", "qty": 5000, "unit": 65000, "delivered": 325000000, "install": 0}
            ]
        },
        {
            "id_suffix": "FLEET",
            "title": "Logistics: 50 Electric Last-Mile Delivery Vans",
            "sender": "Ops Head <logistics@ecom-express-demo.com>",
            "scope": "RFP for 50 Electric Cargo Vans for urban delivery.\nSpecs:\n- Range: >120km/charge\n- Payload: >600kg\n- Battery Warranty: 8 Years\n- Charging: Fast Charge Support (CCS2)",
            "est_val": 45000000.00,
            "sku_rec": "EV-VAN-LONG",
            "products": [
                ("EV-VAN-LONG", "e-Cargo Van Long Range 150km", "Automotive", 900000.00),
                ("EV-VAN-STD", "e-Cargo Van Std Range 90km", "Automotive", 750000.00)
            ],
            "matches": [
                {"sku": "EV-VAN-LONG", "score": 0.96, "specs": {"range": "exceeds", "payload": "match"}},
                {"sku": "EV-VAN-STD", "score": 0.70, "specs": {"range": "too_low"}}
            ],
            "pricing": [
                {"sku": "EV-VAN-LONG", "qty": 50, "unit": 900000, "delivered": 45000000, "install": 0},
                {"sku": "EV-VAN-STD", "qty": 50, "unit": 750000, "delivered": 37500000, "install": 0}
            ]
        },
        {
            "id_suffix": "CHAIRS",
            "title": "Office Fitout: 500 Ergonomic Task Chairs",
            "sender": "Admin <facilities@tech-startup-demo.com>",
            "scope": "Supply of 500 High-Performance Ergonomic Chairs for new HQ.\nFeatures:\n- Lumbar Support: Adjustable\n- Armrest: 3D Adjustable\n- Mesh Back: Brewthable\n- Certification: BIFMA",
            "est_val": 7500000.00,
            "sku_rec": "FURN-ERGO-PRO",
            "products": [
                ("FURN-ERGO-PRO", "Ergo Pro Mesh Chair Black", "Furniture", 15000.00),
                ("FURN-BASIC", "Basic Task Chair", "Furniture", 8000.00)
            ],
            "matches": [
                {"sku": "FURN-ERGO-PRO", "score": 0.95, "specs": {"features": "exact", "certification": "yes"}},
                {"sku": "FURN-BASIC", "score": 0.60, "specs": {"lumbar": "fixed", "armrest": "fixed"}}
            ],
            "pricing": [
                {"sku": "FURN-ERGO-PRO", "qty": 500, "unit": 15000, "delivered": 7500000, "install": 50000},
                {"sku": "FURN-BASIC", "qty": 500, "unit": 8000, "delivered": 4000000, "install": 50000}
            ]
        },
        {
            "id_suffix": "ROBOT",
            "title": "Factory Automation: 6-Axis Welding Robot Cell",
            "sender": "Plant Head <mfg@auto-parts-demo.com>",
            "scope": "Turnkey supply of Robotic Arc Welding Cell.\nSpecs:\n- Payload: 12kg\n- Reach: 1.4m\n- Axes: 6\n- Controller: Included\n- Safety: Light Curtains included",
            "est_val": 32000000.00,
            "sku_rec": "ROBOT-WELD-6AX",
            "products": [
                ("ROBOT-WELD-6AX", "6-Axis Arc Welding Robot Series-X", "Industrial", 2800000.00),
                ("ROBOT-PICK-4AX", "4-Axis Pick and Place Robot", "Industrial", 1500000.00)
            ],
            "matches": [
                {"sku": "ROBOT-WELD-6AX", "score": 0.99, "specs": {"app": "welding", "axes": "exact"}},
                {"sku": "ROBOT-PICK-4AX", "score": 0.20, "specs": {"app": "wrong_type"}}
            ],
            "pricing": [
                {"sku": "ROBOT-WELD-6AX", "qty": 10, "unit": 2800000, "delivered": 28000000, "install": 4000000},
                {"sku": "ROBOT-PICK-4AX", "qty": 10, "unit": 1500000, "delivered": 15000000, "install": 2000000}
            ]
        }
    ]

    with db.get_connection() as conn:
        with conn.cursor() as cursor:
            # Insert Products & RFPs
            for i, d in enumerate(demos):
                rfp_id = f"RFP-DEMO-{d['id_suffix']}-{str(uuid.uuid4())[:4]}"
                disc_time = base_time - timedelta(minutes=i*20)
                
                print(f"Creating Demo RFP: {d['title']}")

                # Products
                for p_sku, p_name, p_cat, p_price in d['products']:
                    cursor.execute("""
                        INSERT INTO products (sku, product_name, category, unit_price, specifications, stock_status)
                        VALUES (%s, %s, %s, %s, '{}', 'In Stock')
                        ON CONFLICT (sku) DO NOTHING
                    """, (p_sku, p_name, p_cat, p_price))
                
                # RFP
                cursor.execute("""
                    INSERT INTO rfps 
                    (rfp_id, title, source, deadline, scope, testing_requirements, 
                     discovered_at, status, match_score, total_estimate, recommended_sku, specifications, attachments)
                    VALUES (%s, %s, %s, %s, %s, '[]', %s, 'completed', %s, %s, %s, '{}', '[]')
                    ON CONFLICT (rfp_id) DO NOTHING
                """, (
                    rfp_id,
                    d['title'],
                    f"Email: {d['sender']}",
                    (base_time + timedelta(days=20)).isoformat(),
                    d['scope'],
                    disc_time,
                    d['matches'][0]['score'],
                    d['est_val'],
                    d['sku_rec']
                ))

                # Email
                email_id = f"email-demo-{str(uuid.uuid4())}"
                cursor.execute("""
                    INSERT INTO emails (email_id, subject, sender, received_at, body, rfp_id, status)
                    VALUES (%s, %s, %s, %s, %s, %s, 'processed')
                """, (
                    email_id,
                    d['title'],
                    d['sender'],
                    disc_time,
                    d['scope'],
                    rfp_id
                ))

                # Matches
                for m in d['matches']:
                    p_name = next(p[1] for p in d['products'] if p[0] == m['sku'])
                    cursor.execute("""
                        INSERT INTO product_matches
                        (rfp_id, sku, product_name, match_score, specification_alignment)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (rfp_id, m['sku'], p_name, m['score'], json.dumps(m['specs'])))
                
                # Pricing
                for p in d['pricing']:
                    cursor.execute("""
                        INSERT INTO pricing_breakdown
                        (rfp_id, sku, unit_price, quantity, subtotal, 
                        testing_cost, delivery_cost, urgency_adjustment, total)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        rfp_id, p['sku'], p['unit'], p['qty'], 
                        p['delivered'], p['install'], 0, 0, p['delivered'] + p['install']
                    ))

            conn.commit()
    
    # 3. SEED FRESH PENDING EMAILS (Different from previous ones)
    pending_emails = [
        {
            "subject": "RFP Opportunity: 1000 Tablets for Education",
            "sender": "gov-education@state-board.gov.in",
            "body": "Tender for supply of 1000 Educational Tablets.\nSpecs:\n- Screen: 10 inch\n- RAM: 4GB\n- Battery: 6000mAh\n- Rugged Case required",
            "time": 5
        },
        {
            "subject": "Inquiry: 200kVA UPS for Server Room",
            "sender": "cio@banking-corp-demo.com",
            "body": "Need urgent quote for Modular UPS System.\nCapacity: 200kVA\nRedundancy: N+1\nBattery Backup: 30 Mins",
            "time": 25
        },
        {
            "subject": "Tender: Conveyor Belt System for Mining",
            "sender": "ops@mining-co-demo.com",
            "body": "Request for Proposal: 2km Conveyor Belt System.\nWidth: 1200mm\nMaterial: Rubber/Fabric\nLoad: 500 TPH",
            "time": 45
        }
    ]

    with db.get_connection() as conn:
        with conn.cursor() as cursor:
            for e in pending_emails:
                email_id = f"email-pending-{str(uuid.uuid4())[:8]}"
                cursor.execute("""
                    INSERT INTO emails (email_id, subject, sender, received_at, body, status, attachments)
                    VALUES (%s, %s, %s, %s, %s, 'pending', '[]')
                    ON CONFLICT (email_id) DO NOTHING
                """, (
                    email_id,
                    e['subject'],
                    e['sender'],
                    base_time - timedelta(minutes=e['time']),
                    e['body']
                ))
            conn.commit()

    print("Successfully reset and seeded FRESH data!")

if __name__ == "__main__":
    asyncio.run(reset_and_seed_fresh())
