"""
Seed Data Script
Loads initial sample data into the database
"""
import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from decimal import Decimal

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

import psycopg2
from psycopg2.extras import Json
from orchestrator.config import settings

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


# Sample Products Data
SAMPLE_PRODUCTS = [
    {
        "sku": "XLPE-11KV-185-CU",
        "product_name": "11kV XLPE Insulated Copper Cable 185 sq.mm",
        "category": "Power Cables",
        "manufacturer": "Your Company",
        "specifications": {
            "voltage": "11000",
            "conductor_size": "185",
            "conductor_material": "Copper",
            "insulation": "XLPE",
            "cores": "3",
            "standard": "IEC 60502"
        },
        "unit_price": Decimal("850.00"),
        "stock_status": "In Stock",
        "datasheet_url": "https://example.com/datasheets/xlpe-11kv-185-cu.pdf",
        "description": "High quality 11kV XLPE insulated copper cable suitable for underground power distribution"
    },
    {
        "sku": "XLPE-11KV-240-CU",
        "product_name": "11kV XLPE Insulated Copper Cable 240 sq.mm",
        "category": "Power Cables",
        "manufacturer": "Your Company",
        "specifications": {
            "voltage": "11000",
            "conductor_size": "240",
            "conductor_material": "Copper",
            "insulation": "XLPE",
            "cores": "3",
            "standard": "IEC 60502"
        },
        "unit_price": Decimal("1050.00"),
        "stock_status": "In Stock",
        "datasheet_url": "https://example.com/datasheets/xlpe-11kv-240-cu.pdf",
        "description": "Premium 11kV XLPE insulated copper cable for heavy-duty applications"
    },
    {
        "sku": "XLPE-33KV-185-CU",
        "product_name": "33kV XLPE Insulated Copper Cable 185 sq.mm",
        "category": "Power Cables",
        "manufacturer": "Your Company",
        "specifications": {
            "voltage": "33000",
            "conductor_size": "185",
            "conductor_material": "Copper",
            "insulation": "XLPE",
            "cores": "3",
            "standard": "IEC 60502"
        },
        "unit_price": Decimal("1250.00"),
        "stock_status": "In Stock",
        "datasheet_url": "https://example.com/datasheets/xlpe-33kv-185-cu.pdf",
        "description": "High voltage 33kV XLPE cable for transmission applications"
    },
    {
        "sku": "XLPE-11KV-185-AL",
        "product_name": "11kV XLPE Insulated Aluminum Cable 185 sq.mm",
        "category": "Power Cables",
        "manufacturer": "Your Company",
        "specifications": {
            "voltage": "11000",
            "conductor_size": "185",
            "conductor_material": "Aluminum",
            "insulation": "XLPE",
            "cores": "3",
            "standard": "IEC 60502"
        },
        "unit_price": Decimal("620.00"),
        "stock_status": "In Stock",
        "datasheet_url": "https://example.com/datasheets/xlpe-11kv-185-al.pdf",
        "description": "Cost-effective 11kV XLPE aluminum cable for distribution networks"
    },
    {
        "sku": "PVC-1KV-95-CU",
        "product_name": "1kV PVC Insulated Copper Cable 95 sq.mm",
        "category": "LV Cables",
        "manufacturer": "Your Company",
        "specifications": {
            "voltage": "1000",
            "conductor_size": "95",
            "conductor_material": "Copper",
            "insulation": "PVC",
            "cores": "4",
            "standard": "IS 1554"
        },
        "unit_price": Decimal("280.00"),
        "stock_status": "In Stock",
        "datasheet_url": "https://example.com/datasheets/pvc-1kv-95-cu.pdf",
        "description": "Standard LV PVC cable for building wiring and installations"
    },
    {
        "sku": "XLPE-11KV-300-CU",
        "product_name": "11kV XLPE Insulated Copper Cable 300 sq.mm",
        "category": "Power Cables",
        "manufacturer": "Your Company",
        "specifications": {
            "voltage": "11000",
            "conductor_size": "300",
            "conductor_material": "Copper",
            "insulation": "XLPE",
            "cores": "3",
            "standard": "IEC 60502"
        },
        "unit_price": Decimal("1350.00"),
        "stock_status": "In Stock",
        "datasheet_url": "https://example.com/datasheets/xlpe-11kv-300-cu.pdf",
        "description": "Heavy-duty 11kV XLPE cable for high current applications"
    }
]


def seed_products(cursor):
    """Insert sample products"""
    logger.info("📦 Seeding products...")
    
    for product in SAMPLE_PRODUCTS:
        cursor.execute("""
            INSERT INTO products (
                sku, product_name, category, manufacturer, 
                specifications, unit_price, stock_status, 
                datasheet_url, description
            ) VALUES (
                %(sku)s, %(product_name)s, %(category)s, %(manufacturer)s,
                %(specifications)s, %(unit_price)s, %(stock_status)s,
                %(datasheet_url)s, %(description)s
            )
            ON CONFLICT (sku) DO UPDATE SET
                product_name = EXCLUDED.product_name,
                unit_price = EXCLUDED.unit_price,
                updated_at = NOW()
        """, {
            **product,
            'specifications': Json(product['specifications'])
        })
    
    logger.info(f"✅ Inserted {len(SAMPLE_PRODUCTS)} products")


def seed_sample_rfps(cursor):
    """Insert sample RFPs for testing"""
    logger.info("📄 Seeding sample RFPs...")
    
    sample_rfps = [
        {
            "rfp_id": "RFP-2025-001",
            "title": "Supply of 11kV XLPE Cables for State Electricity Board",
            "source": "https://tenders.gov.in/sample-1",
            "deadline": datetime.now() + timedelta(days=30),
            "scope": "Supply and installation of 11kV XLPE insulated copper cables, 185 sq.mm, 3 core. Total length: 5000 meters.",
            "testing_requirements": Json(["Type Test", "Routine Test"]),
            "specifications": Json({
                "voltage": "11kV",
                "conductor_size": "185 sq.mm",
                "conductor_material": "Copper",
                "insulation": "XLPE",
                "cores": "3",
                "length": "5000 meters"
            }),
            "status": "new"
        },
        {
            "rfp_id": "RFP-2025-002",
            "title": "33kV Underground Cable Supply - Metro Project",
            "source": "Email",
            "deadline": datetime.now() + timedelta(days=45),
            "scope": "Supply of 33kV XLPE cables for metro rail underground power distribution. Quantity: 3000 meters.",
            "testing_requirements": Json(["Type Test", "Sample Test"]),
            "specifications": Json({
                "voltage": "33kV",
                "conductor_size": "185 sq.mm",
                "conductor_material": "Copper",
                "insulation": "XLPE",
                "cores": "3",
                "length": "3000 meters"
            }),
            "status": "new"
        },
        {
            "rfp_id": "RFP-2025-003",
            "title": "LV Cables for Industrial Complex",
            "source": "https://tenders.gov.in/sample-3",
            "deadline": datetime.now() + timedelta(days=15),
            "scope": "Supply of 1kV PVC cables for new industrial complex wiring. Various sizes required.",
            "testing_requirements": Json(["Routine Test"]),
            "specifications": Json({
                "voltage": "1kV",
                "conductor_size": "95 sq.mm",
                "conductor_material": "Copper",
                "insulation": "PVC",
                "cores": "4",
                "length": "2000 meters"
            }),
            "status": "processing"
        }
    ]
    
    for rfp in sample_rfps:
        cursor.execute("""
            INSERT INTO rfps (
                rfp_id, title, source, deadline, scope,
                testing_requirements, specifications, status
            ) VALUES (
                %(rfp_id)s, %(title)s, %(source)s, %(deadline)s, %(scope)s,
                %(testing_requirements)s, %(specifications)s, %(status)s
            )
            ON CONFLICT (rfp_id) DO NOTHING
        """, rfp)
    
    logger.info(f"✅ Inserted {len(sample_rfps)} sample RFPs")


def seed_performance_metrics(cursor):
    """Insert initial performance metrics"""
    logger.info("📊 Seeding performance metrics...")
    
    metrics = [
        {
            "metric_name": "total_rfps_processed",
            "metric_value": 0,
            "period_start": datetime.now() - timedelta(days=30),
            "period_end": datetime.now()
        },
        {
            "metric_name": "average_processing_time",
            "metric_value": 0,
            "period_start": datetime.now() - timedelta(days=30),
            "period_end": datetime.now()
        },
        {
            "metric_name": "win_rate",
            "metric_value": 0,
            "period_start": datetime.now() - timedelta(days=30),
            "period_end": datetime.now()
        }
    ]
    
    for metric in metrics:
        cursor.execute("""
            INSERT INTO performance_metrics (
                metric_name, metric_value, period_start, period_end
            ) VALUES (
                %(metric_name)s, %(metric_value)s, %(period_start)s, %(period_end)s
            )
        """, metric)
    
    logger.info(f"✅ Inserted {len(metrics)} performance metrics")


def main():
    """Main seeding process"""
    logger.info("=" * 60)
    logger.info("🌱 Starting Data Seeding")
    logger.info("=" * 60)
    
    try:
        # Connect to database
        logger.info("\n📡 Connecting to database...")
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME
        )
        cursor = conn.cursor()
        logger.info("✅ Connected successfully")
        
        # Seed data
        seed_products(cursor)
        seed_sample_rfps(cursor)
        seed_performance_metrics(cursor)
        
        # Commit changes
        conn.commit()
        
        # Verify data
        logger.info("\n📊 Verifying seeded data...")
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        logger.info(f"   Products: {product_count}")
        
        cursor.execute("SELECT COUNT(*) FROM rfps")
        rfp_count = cursor.fetchone()[0]
        logger.info(f"   RFPs: {rfp_count}")
        
        cursor.execute("SELECT COUNT(*) FROM performance_metrics")
        metric_count = cursor.fetchone()[0]
        logger.info(f"   Metrics: {metric_count}")
        
        cursor.close()
        conn.close()
        
        logger.info("\n" + "=" * 60)
        logger.info("🎉 Data seeding completed successfully!")
        logger.info("=" * 60)
        logger.info("\n📝 Next steps:")
        logger.info("   1. Start backend: uvicorn orchestrator.api.main:app --reload")
        logger.info("   2. Test API: http://localhost:8000/docs")
        logger.info("   3. Start frontend: cd frontend && npm run dev")
        
        return True
        
    except psycopg2.Error as e:
        logger.error(f"❌ Database error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
