"""
Product Service - Business logic for product operations
"""
import logging
from typing import List, Optional

from shared.database.connection import get_db_manager

logger = logging.getLogger(__name__)


class ProductService:
    """Service for product operations"""
    
    async def get_products(
        self,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[dict]:
        """Get list of products"""
        try:
            db = get_db_manager()
            if not db:
                 # Mock data
                 products = [
                     {"sku": "XLPE-11KV-185", "product_name": "11kV XLPE Cable 185sqmm", "category": "Cables", "manufacturer": "Polycab", "specifications": {}, "unit_price": 500.0, "stock_status": "In Stock"},
                     {"sku": "XLPE-11KV-300", "product_name": "11kV XLPE Cable 300sqmm", "category": "Cables", "manufacturer": "KEI", "specifications": {}, "unit_price": 750.0, "stock_status": "In Stock"},
                     {"sku": "TRANS-100KVA", "product_name": "100kVA Transformer", "category": "Transformers", "manufacturer": "Voltamp", "specifications": {}, "unit_price": 150000.0, "stock_status": "LTS"}
                 ]
                 if category:
                     products = [p for p in products if p['category'] == category]
                 return products

            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    if category:
                        cursor.execute("""
                            SELECT sku, product_name, category, manufacturer, 
                                   specifications, unit_price, stock_status
                            FROM products
                            WHERE category = %s
                            ORDER BY product_name
                            LIMIT %s OFFSET %s
                        """, (category, limit, offset))
                    else:
                        cursor.execute("""
                            SELECT sku, product_name, category, manufacturer, 
                                   specifications, unit_price, stock_status
                            FROM products
                            ORDER BY product_name
                            LIMIT %s OFFSET %s
                        """, (limit, offset))
                    
                    rows = cursor.fetchall()
            
            products = []
            for row in rows:
                products.append({
                    "sku": row[0],
                    "product_name": row[1],
                    "category": row[2],
                    "manufacturer": row[3],
                    "specifications": row[4] if row[4] else {},
                    "unit_price": float(row[5]) if row[5] else 0.0,
                    "stock_status": row[6]
                })
            
            return products
        except Exception as e:
            logger.error(f"Error fetching products: {str(e)}")
            # Fallback
            return []
    
    async def get_product_by_sku(self, sku: str) -> Optional[dict]:
        """Get product by SKU"""
        try:
            db = get_db_manager()
            if not db:
                return None
            
            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT sku, product_name, category, manufacturer, 
                               specifications, unit_price, stock_status, 
                               datasheet_url, description
                        FROM products
                        WHERE sku = %s
                    """, (sku,))
                    
                    row = cursor.fetchone()
            
            if not row:
                return None
            
            return {
                "sku": row[0],
                "product_name": row[1],
                "category": row[2],
                "manufacturer": row[3],
                "specifications": row[4] if row[4] else {},
                "unit_price": float(row[5]) if row[5] else 0.0,
                "stock_status": row[6],
                "datasheet_url": row[7],
                "description": row[8]
            }
        except Exception as e:
            logger.error(f"Error fetching product {sku}: {str(e)}")
            raise
    
    async def search_products(self, query: str, limit: int = 20) -> List[dict]:
        """Search products by query"""
        try:
            db = get_db_manager()
            results = []
            
            if db:
                with db.get_connection() as conn:
                    with conn.cursor() as cursor:
                        search_term = f"%{query}%"
                        cursor.execute("""
                            SELECT sku, product_name, category, manufacturer, unit_price
                            FROM products
                            WHERE product_name ILIKE %s 
                                OR category ILIKE %s
                                OR manufacturer ILIKE %s
                                OR sku ILIKE %s
                            ORDER BY 
                                CASE 
                                    WHEN product_name ILIKE %s THEN 1
                                    WHEN sku ILIKE %s THEN 2
                                    ELSE 3
                                END,
                                product_name
                            LIMIT %s
                        """, (search_term, search_term, search_term, search_term, 
                              search_term, search_term, limit))
                        
                        rows = cursor.fetchall()
                        for row in rows:
                            results.append({
                                "sku": row[0],
                                "product_name": row[1],
                                "category": row[2],
                                "manufacturer": row[3],
                                "unit_price": float(row[4]) if row[4] else 0.0
                            })
                            
            if not results:
                 # Fallback Mock Data for testing
                 mock_data = [
                     {"sku": "XLPE-11KV-185", "product_name": "11kV XLPE Cable 185sqmm", "category": "Cables", "manufacturer": "Polycab", "unit_price": 500.0},
                     {"sku": "XLPE-11KV-300", "product_name": "11kV XLPE Cable 300sqmm", "category": "Cables", "manufacturer": "KEI", "unit_price": 750.0},
                     {"sku": "TRANS-100KVA", "product_name": "100kVA Transformer", "category": "Transformers", "manufacturer": "Voltamp", "unit_price": 150000.0}
                 ]
                 # Simple filter
                 results = [p for p in mock_data if query.lower() in p['product_name'].lower() or query.lower() in p['sku'].lower()]
            
            return results
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            # Fallback on error too
            return []
    
    async def get_categories(self) -> List[dict]:
        """Get all product categories"""
        try:
            db = get_db_manager()
            if not db:
                return []
            
            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT category, COUNT(*) as product_count
                        FROM products
                        GROUP BY category
                        ORDER BY category
                    """)
                    
                    rows = cursor.fetchall()
            
            categories = []
            for row in rows:
                categories.append({
                    "name": row[0],
                    "product_count": int(row[1])
                })
            
            return categories
        except Exception as e:
            logger.error(f"Error fetching categories: {str(e)}")
            raise
    
    async def get_statistics(self) -> dict:
        """Get product statistics"""
        try:
            db = get_db_manager()
            if not db:
                return {"total_products": 0, "total_categories": 0, "total_manufacturers": 0, "average_price": 0.0, "in_stock": 0}
            
            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT 
                            COUNT(*) as total_products,
                            COUNT(DISTINCT category) as total_categories,
                            COUNT(DISTINCT manufacturer) as total_manufacturers,
                            AVG(unit_price) as avg_price,
                            COUNT(CASE WHEN stock_status = 'In Stock' THEN 1 END) as in_stock
                        FROM products
                    """)
                    
                    row = cursor.fetchone()
            
            return {
                "total_products": int(row[0]) if row[0] else 0,
                "total_categories": int(row[1]) if row[1] else 0,
                "total_manufacturers": int(row[2]) if row[2] else 0,
                "average_price": float(row[3]) if row[3] else 0.0,
                "in_stock": int(row[4]) if row[4] else 0
            }
        except Exception as e:
            logger.error(f"Error fetching product stats: {str(e)}")
            raise
