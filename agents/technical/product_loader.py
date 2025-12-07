"""
Product Loader Script
Loads sample products into PostgreSQL and Qdrant
"""
import os
import sys
import json
import logging
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

load_dotenv()

from shared.database.connection import get_db_connection
from shared.models import ProductMatch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample Products Data
SAMPLE_PRODUCTS = [
    {
        "sku": "XLPE-11KV-185",
        "product_name": "11kV XLPE Cable 185 sq mm",
        "category": "Medium Voltage Cables",
        "manufacturer": "CableCo Industries",
        "specifications": {
            "voltage": "11kV",
            "conductor_material": "Copper",
            "insulation_material": "XLPE",
            "conductor_size": "185 sq mm",
            "cable_type": "3 core, armoured",
            "standards": ["IEC 60502", "IS 7098"]
        },
        "unit_price": 450.00,
        "stock_status": "in_stock",
        "description": "Premium 11kV XLPE cable for distribution networks."
    },
    {
        "sku": "XLPE-11KV-240",
        "product_name": "11kV XLPE Cable 240 sq mm",
        "category": "Medium Voltage Cables",
        "manufacturer": "CableCo Industries",
        "specifications": {
            "voltage": "11kV",
            "conductor_material": "Copper",
            "insulation_material": "XLPE",
            "conductor_size": "240 sq mm",
            "cable_type": "3 core, armoured",
            "standards": ["IEC 60502", "IS 7098"]
        },
        "unit_price": 580.00,
        "stock_status": "in_stock",
        "description": "Heavy duty 11kV XLPE cable."
    },
    {
        "sku": "XLPE-33KV-185",
        "product_name": "33kV XLPE Cable 185 sq mm",
        "category": "High Voltage Cables",
        "manufacturer": "CableCo Industries",
        "specifications": {
            "voltage": "33kV",
            "conductor_material": "Copper",
            "insulation_material": "XLPE",
            "conductor_size": "185 sq mm",
            "cable_type": "3 core, armoured",
            "standards": ["IEC 60502", "IS 7098"]
        },
        "unit_price": 850.00,
        "stock_status": "low_stock",
        "description": "33kV transmission cable."
    },
    {
        "sku": "PVC-1.1KV-50",
        "product_name": "1.1kV PVC Cable 50 sq mm",
        "category": "Low Voltage Cables",
        "manufacturer": "WireTech Solutions",
        "specifications": {
            "voltage": "1.1kV",
            "conductor_material": "Copper",
            "insulation_material": "PVC",
            "conductor_size": "50 sq mm",
            "cable_type": "4 core",
            "standards": ["IEC 60227", "IS 694"]
        },
        "unit_price": 120.00,
        "stock_status": "in_stock",
        "description": "Standard LT PVC cable."
    },
    {
        "sku": "XLPE-11KV-300-AL",
        "product_name": "11kV XLPE Cable 300 sq mm Al",
        "category": "Medium Voltage Cables",
        "manufacturer": "CableCo Industries",
        "specifications": {
            "voltage": "11kV",
            "conductor_material": "Aluminium",
            "insulation_material": "XLPE",
            "conductor_size": "300 sq mm",
            "cable_type": "3 core, armoured",
            "standards": ["IEC 60502", "IS 7098"]
        },
        "unit_price": 520.00,
        "stock_status": "in_stock",
        "description": "Aluminium conductor 11kV cable."
    }
]

def load_products_postgres(products: List[Dict[str, Any]]):
    """Load products into PostgreSQL"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        logger.info(f"Loading {len(products)} products into PostgreSQL...")
        
        for p in products:
            cursor.execute("""
                INSERT INTO products 
                (sku, product_name, category, manufacturer, specifications, 
                 unit_price, stock_status, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
                ON CONFLICT (sku) DO UPDATE SET
                product_name = EXCLUDED.product_name,
                specifications = EXCLUDED.specifications,
                unit_price = EXCLUDED.unit_price,
                updated_at = NOW()
            """, (
                p['sku'], p['product_name'], p['category'], p['manufacturer'],
                json.dumps(p['specifications']), p['unit_price'], 
                p['stock_status'], p['description']
            ))
            
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("PostgreSQL load successful.")
        return True
    except Exception as e:
        logger.error(f"Error loading Postgres: {e}")
        return False

def load_products_qdrant(products: List[Dict[str, Any]]):
    """Load products into Qdrant"""
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.http import models
        from sentence_transformers import SentenceTransformer
        
        # Connect to Qdrant
        host = os.getenv("QDRANT_HOST", "localhost")
        port = int(os.getenv("QDRANT_PORT", 6333))
        client = QdrantClient(host=host, port=port)
        
        collection_name = os.getenv("QDRANT_COLLECTION", "products")
        
        # Initialize embedding model
        model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        logger.info(f"Loading embedding model: {model_name}...")
        model = SentenceTransformer(model_name)
        
        # Create collection if likely not exists (or recreate)
        collections = client.get_collections().collections
        exists = any(c.name == collection_name for c in collections)
        
        if not exists:
            logger.info(f"Creating collection {collection_name}...")
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=384,  # all-MiniLM-L6-v2 output size
                    distance=models.Distance.COSINE
                )
            )
        
        logger.info("Generating embeddings and uploading to Qdrant...")
        
        points = []
        for idx, p in enumerate(products):
            # Create text representation for embedding
            specs = p['specifications']
            text_to_embed = f"{p['product_name']} {specs.get('voltage', '')} {specs.get('conductor_material', '')} {specs.get('cable_type', '')} {p['description']}"
            
            vector = model.encode(text_to_embed).tolist()
            
            points.append(models.PointStruct(
                id=idx,  # Integer ID
                vector=vector,
                payload={
                    "sku": p['sku'],
                    "product_name": p['product_name'],
                    "specifications": p['specifications']
                }
            ))
            
        client.upsert(
            collection_name=collection_name,
            points=points
        )
        
        logger.info("Qdrant load successful.")
        return True
        
    except ImportError:
        logger.error("Missing dependencies for Qdrant/Embeddings. Install sentence-transformers and qdrant-client.")
        return False
    except Exception as e:
        logger.error(f"Error loading Qdrant: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting Product Loader...")
    
    # 1. Load to Postgres
    pg_success = load_products_postgres(SAMPLE_PRODUCTS)
    
    # 2. Load to Qdrant
    q_success = load_products_qdrant(SAMPLE_PRODUCTS)
    
    if pg_success and q_success:
        logger.info("Product loading completed successfully.")
        sys.exit(0)
    else:
        logger.error("Product loading failed.")
        sys.exit(1)
