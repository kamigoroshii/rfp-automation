
import asyncio
import json
import uuid
from datetime import datetime, timedelta
from shared.database.connection import get_db_manager

# Demo Configuration
DEMO_EMAIL_RECIPIENT = "pamedipagaraphel@gmail.com" # Just for reference, frontend handles this.

async def seed_demo_data():
    """
    Seeds the database with 5 distinct, fully completed RFPs for the Jury Demo.
    Each RFP will have:
    - Detailed Scope & Specifications
    - Matched Products
    - Complete Pricing Breakdown
    - Linked Email Record (for authentic source display)
    - 'Completed' status to enable PDF generation
    """
    print("Connecting to database...")
    db = get_db_manager()
    if not db:
        print("Database not available!")
        return

    # Base timestamp (start from 1 hour ago to appear recent)
    base_time = datetime.now()

    demos = [
        {
            "id_suffix": "CABLE",
            "title": "Urgent: 33kV High Voltage Cabling for Metro Phase II",
            "sender": "Rahul Sharma <procurement@delhimetro.gov.in>",
            "scope": "Supply and installation of 33kV XLPE Insulated Underground Cables for the Phase II Metro expansion. Total length required: 15km. Must adhere to IEC 60502 standards. \n\nSpecs:\n- Voltage: 33kV\n- Core: 3-Core\n- Conductor: Copper\n- Armouring: Steel Wire",
            "est_val": 15000000.00,
            "sku_rec": "XLPE-33KV-3C-400",
            "products": [
                ("XLPE-33KV-3C-400", "33kV 3-Core XLPE Cable 400sqmm", "Cables", 2500.00),
                ("XLPE-33KV-3C-300", "33kV 3-Core XLPE Cable 300sqmm", "Cables", 2200.00)
            ],
            "matches": [
                {"sku": "XLPE-33KV-3C-400", "score": 0.98, "specs": {"voltage": "exact", "type": "exact"}},
                {"sku": "XLPE-33KV-3C-300", "score": 0.85, "specs": {"voltage": "exact", "size": "close"}}
            ],
            "pricing": [
                {"sku": "XLPE-33KV-3C-400", "qty": 15000, "unit": 2500, "delivered": 34500000, "install": 2000000},
                {"sku": "XLPE-33KV-3C-300", "qty": 15000, "unit": 2200, "delivered": 30000000, "install": 2000000}
            ]
        },
        {
            "id_suffix": "SOLAR",
            "title": "RFP: 5MW Solar Power Plant Components - Rajasthan",
            "sender": "Aditi Verma <projects@renewpower.in>",
            "scope": "Requesting proposals for supply of Mono-PERC Solar Modules and Central Inverters for a 5MW ground-mounted solar project in Jodhpur. \n\nRequirements:\n- Module Efficiency: >21%\n- Wattage: 540Wp+\n- Inverter: 2.5MW Central Inverter x 2\n- Warranty: 25 Years performance",
            "est_val": 125000000.00,
            "sku_rec": "SOLAR-MOD-550",
            "products": [
                ("SOLAR-MOD-550", "Mono-PERC Solar Module 550Wp", "Solar", 12000.00),
                ("SOLAR-INV-2.5MW", "Central Inverter 2.5MW Outdoor", "Solar", 1500000.00)
            ],
            "matches": [
                {"sku": "SOLAR-MOD-550", "score": 0.96, "specs": {"technology": "exact", "power": "exceeds"}},
                {"sku": "SOLAR-INV-2.5MW", "score": 0.94, "specs": {"capacity": "exact"}}
            ],
            "pricing": [
                {"sku": "SOLAR-MOD-550", "qty": 9090, "unit": 12000, "delivered": 109080000, "install": 5000000},
                {"sku": "SOLAR-INV-2.5MW", "qty": 2, "unit": 1500000, "delivered": 3000000, "install": 100000}
            ]
        },
        {
            "id_suffix": "HVAC",
            "title": "Tender: Centralized HVAC for Tech Park (Block A)",
            "sender": "Facilities Manager <fm@prestigetech.com>",
            "scope": "Supply, T&C of Water Cooled Screw Chillers (300TR x 3 Nos). \n\nApplication: Commercial Office Space Cooling.\nSpecs:\n- Capacity: 300 TR\n- Efficiency: IKWe/TR < 0.65\n- Refrigerant: R134a",
            "est_val": 18000000.00,
            "sku_rec": "CHILLER-300TR-SCREW",
            "products": [
                ("CHILLER-300TR-SCREW", "Water Cooled Screw Chiller 300TR", "HVAC", 4500000.00),
                ("CHILLER-350TR-SCREW", "Water Cooled Screw Chiller 350TR", "HVAC", 5200000.00)
            ],
            "matches": [
                {"sku": "CHILLER-300TR-SCREW", "score": 0.99, "specs": {"capacity": "exact", "type": "exact"}},
                {"sku": "CHILLER-350TR-SCREW", "score": 0.82, "specs": {"capacity": "higher"}}
            ],
            "pricing": [
                {"sku": "CHILLER-300TR-SCREW", "qty": 3, "unit": 4500000, "delivered": 13500000, "install": 1500000},
                {"sku": "CHILLER-350TR-SCREW", "qty": 3, "unit": 5200000, "delivered": 15600000, "install": 1800000}
            ]
        },
        {
            "id_suffix": "CCTV",
            "title": "Security Upgrade: IP CCTV Installation for Warehouse",
            "sender": "Security Ops <ops@logistics-solutions.com>",
            "scope": "Looking for 50 units of 4MP IP Dome Cameras with Night Vision and NVR system. Must support IR distance up to 30m and POE.\n\nItems:\n- 4MP IP Dome Camera\n- 64 Channel NVR\n- 4TB Surveillance HDD x 4",
            "est_val": 850000.00,
            "sku_rec": "CAM-IP-4MP-DOME",
            "products": [
                ("CAM-IP-4MP-DOME", "4MP IR Dome Network Camera", "Security", 6500.00),
                ("NVR-64CH-4K", "64 Channel 4K NVR", "Security", 45000.00)
            ],
            "matches": [
                {"sku": "CAM-IP-4MP-DOME", "score": 0.95, "specs": {"resolution": "exact", "features": "match"}},
                {"sku": "NVR-64CH-4K", "score": 0.97, "specs": {"channels": "exact"}}
            ],
            "pricing": [
                {"sku": "CAM-IP-4MP-DOME", "qty": 50, "unit": 6500, "delivered": 325000, "install": 50000},
                {"sku": "NVR-64CH-4K", "qty": 1, "unit": 45000, "delivered": 45000, "install": 5000}
            ]
        },
        {
            "id_suffix": "LAPTOP",
            "title": "Corporate IT: 200 Enterprise Laptops Refresh",
            "sender": "IT Procurement <procurement@infosys-demo.com>",
            "scope": "Procurement of 200 Business Series Laptops for developers.\nMinimum Specs:\n- Processor: Intel Core i7 12th Gen / AMD Ryzen 7\n- RAM: 32GB DDR4\n- Storage: 1TB NVMe SSD\n- OS: Windows 11 Pro\n- Warranty: 3 Years Onsite",
            "est_val": 22000000.00,
            "sku_rec": "NB-BIZ-i7-32G",
            "products": [
                ("NB-BIZ-i7-32G", "Enterprise Laptop 14-inch i7/32GB/1TB", "IT", 105000.00),
                ("NB-BIZ-i5-16G", "Enterprise Laptop 14-inch i5/16GB/512GB", "IT", 85000.00)
            ],
            "matches": [
                {"sku": "NB-BIZ-i7-32G", "score": 0.98, "specs": {"cpu": "exact", "ram": "exact"}},
                {"sku": "NB-BIZ-i5-16G", "score": 0.60, "specs": {"ram": "low"}}
            ],
            "pricing": [
                {"sku": "NB-BIZ-i7-32G", "qty": 200, "unit": 105000, "delivered": 21000000, "install": 0},
                {"sku": "NB-BIZ-i5-16G", "qty": 200, "unit": 85000, "delivered": 17000000, "install": 0}
            ]
        }
    ]

    with db.get_connection() as conn:
        with conn.cursor() as cursor:
            for i, d in enumerate(demos):
                rfp_id = f"RFP-DEMO-{d['id_suffix']}-{str(uuid.uuid4())[:4]}"
                disc_time = base_time - timedelta(minutes=i*15) # Staggered times
                
                print(f"Creating Demo RFP: {d['title']} ({rfp_id})")

                # 1. Insert Products
                for p_sku, p_name, p_cat, p_price in d['products']:
                    cursor.execute("""
                        INSERT INTO products (sku, product_name, category, unit_price, specifications, stock_status)
                        VALUES (%s, %s, %s, %s, '{}', 'In Stock')
                        ON CONFLICT (sku) DO NOTHING
                    """, (p_sku, p_name, p_cat, p_price))

                # 2. Insert RFP
                cursor.execute("""
                    INSERT INTO rfps 
                    (rfp_id, title, source, deadline, scope, testing_requirements, 
                     discovered_at, status, match_score, total_estimate, recommended_sku, specifications, attachments)
                    VALUES (%s, %s, %s, %s, %s, '[]', %s, 'completed', %s, %s, %s, '{}', '[]')
                    ON CONFLICT (rfp_id) DO NOTHING
                """, (
                    rfp_id,
                    d['title'],
                    f"Email: {d['sender'].split('<')[1][:-1]}", # Extract email for display
                    (base_time + timedelta(days=14)).isoformat(),
                    d['scope'],
                    disc_time,
                    d['matches'][0]['score'],
                    d['est_val'],
                    d['sku_rec']
                ))

                # 3. Insert Email Record (for Authentic Source Display)
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

                # 4. Insert Matches
                for m in d['matches']:
                    p_name = next(p[1] for p in d['products'] if p[0] == m['sku'])
                    cursor.execute("""
                        INSERT INTO product_matches
                        (rfp_id, sku, product_name, match_score, specification_alignment)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (rfp_id, m['sku'], p_name, m['score'], json.dumps(m['specs'])))

                # 5. Insert Pricing
                for p in d['pricing']:
                    total = p['delivered'] + p['install'] # Simplified logic
                    cursor.execute("""
                        INSERT INTO pricing_breakdown
                        (rfp_id, sku, unit_price, quantity, subtotal, 
                        testing_cost, delivery_cost, urgency_adjustment, total)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        rfp_id, p['sku'], p['unit'], p['qty'], 
                        p['delivered'], # using 'delivered' as subtotal proxy for simplicity
                        p['install'], # install/testing cost
                        0, # delivery
                        0, # urgency
                        total
                    ))
            
            conn.commit()
    
    print("Successfully seeded 5 Demo RFPs!")

if __name__ == "__main__":
    asyncio.run(seed_demo_data())
