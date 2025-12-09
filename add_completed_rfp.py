
import asyncio
import json
import uuid
from datetime import datetime
from shared.database.connection import get_db_manager
from orchestrator.services.rfp_service import RFPService

async def add_sample_completed_data():
    """
    Adds a sample 'Completed' RFP that simulates one coming from Email.
    This guarantees the 'Generate Proposal PDF' button is visible.
    """
    print("Connecting to database...")
    db = get_db_manager()
    if not db:
        print("Database not available!")
        return

    rfp_id = f"RFP-EMAIL-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4].upper()}"
    
    # 1. Create RFP Record
    rfp_data = {
        "rfp_id": rfp_id,
        "title": "Urgent Requirement: 11kV XLPE Cables for Metro Project",
        "source": "Email: procurement@metro-infra.gov.in", 
        "deadline": datetime.now(), # Today
        "scope": "Supply of 11kV XLPE 3-Core Cables. REQUIRED URGENTLY. \n\nSpecifications:\n- Voltage: 11kV\n- Conductor: Copper\n- Insulation: XLPE\n- Armor: Galvanized Steel Wire\n- Quantity: 5000 meters",
        "testing_requirements": ["Type Test", "Routine Test"],
        "discovered_at": datetime.now(),
        "status": "completed",
        "match_score": 0.95,
        "total_estimate": 4500000.00,
        "recommended_sku": "XLPE-11KV-240",
        "specifications": {
            "voltage": "11kV",
            "conductor_material": "Copper",
            "insulation_material": "XLPE",
            "conductor_size": "240 sq mm",
            "cable_type": "3 core, armoured"
        }
    }
    
    print(f"Inserting RFP {rfp_id}...")
    
    with db.get_connection() as conn:
        with conn.cursor() as cursor:
            # Ensure Products Exist
            products_to_add = [
                ("XLPE-11KV-240", "11kV XLPE Cable 240 sq mm", "Cables", 450.00),
                ("XLPE-11KV-185", "11kV XLPE Cable 185 sq mm", "Cables", 350.00)
            ]
            for sku, name, category, price in products_to_add:
                cursor.execute("""
                    INSERT INTO products (sku, product_name, category, unit_price, specifications, stock_status)
                    VALUES (%s, %s, %s, %s, '{}', 'In Stock')
                    ON CONFLICT (sku) DO NOTHING
                """, (sku, name, category, price))

            # Insert RFP
            cursor.execute("""
                INSERT INTO rfps 
                (rfp_id, title, source, deadline, scope, testing_requirements, 
                 discovered_at, status, match_score, total_estimate, recommended_sku, specifications)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                rfp_data['rfp_id'], rfp_data['title'], rfp_data['source'], rfp_data['deadline'],
                rfp_data['scope'], json.dumps(rfp_data['testing_requirements']), rfp_data['discovered_at'],
                rfp_data['status'], rfp_data['match_score'], rfp_data['total_estimate'],
                rfp_data['recommended_sku'], json.dumps(rfp_data['specifications'])
            ))
            
            # Insert Matches
            matches = [
                {
                    "sku": "XLPE-11KV-240",
                    "product_name": "11kV XLPE Cable 240 sq mm (Copper)",
                    "match_score": 0.95,
                    "specification_alignment": {"voltage": "exact_match", "conductor": "exact_match"}
                },
                {
                    "sku": "XLPE-11KV-185",
                    "product_name": "11kV XLPE Cable 185 sq mm (Copper)",
                    "match_score": 0.88,
                    "specification_alignment": {"voltage": "exact_match", "conductor": "partial_match"}
                }
            ]
            
            for m in matches:
                cursor.execute("""
                    INSERT INTO product_matches
                    (rfp_id, sku, product_name, match_score, specification_alignment)
                    VALUES (%s, %s, %s, %s, %s)
                """, (rfp_id, m['sku'], m['product_name'], m['match_score'], json.dumps(m['specification_alignment'])))
                
            # Insert Pricing
            pricing = [
                {
                    "sku": "XLPE-11KV-240",
                    "unit_price": 850.00,
                    "quantity": 5000,
                    "subtotal": 4250000.00,
                    "testing_cost": 50000.00,
                    "delivery_cost": 25000.00,
                    "urgency_adjustment": 175000.00,
                    "total": 4500000.00
                },
                 {
                    "sku": "XLPE-11KV-185",
                    "unit_price": 700.00,
                    "quantity": 5000,
                    "subtotal": 3500000.00,
                    "testing_cost": 50000.00,
                    "delivery_cost": 25000.00,
                    "urgency_adjustment": 125000.00,
                    "total": 3700000.00
                }
            ]
            
            for p in pricing:
                cursor.execute("""
                    INSERT INTO pricing_breakdown
                    (rfp_id, sku, unit_price, quantity, subtotal, 
                    testing_cost, delivery_cost, urgency_adjustment, total)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    rfp_id, p['sku'], p['unit_price'], p['quantity'], p['subtotal'],
                    p['testing_cost'], p['delivery_cost'], p['urgency_adjustment'], p['total']
                ))

            # Link to Email
            email_id = f"email-{str(uuid.uuid4())}"
            cursor.execute("""
                INSERT INTO emails (email_id, subject, sender, received_at, body, rfp_id, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                email_id, 
                rfp_data['title'], 
                "Procurement Officer <procurement@metro-infra.gov.in>", 
                rfp_data['discovered_at'], 
                rfp_data['scope'], 
                rfp_id, 
                'processed'
            ))
            
            conn.commit()

    print(f"Successfully added RFP {rfp_id} to database.")
    print("You should see it in the list immediately with 'Completed' status.")

if __name__ == "__main__":
    asyncio.run(add_sample_completed_data())
