"""
Database connection manager with connection pooling
"""
import os
import time
from typing import Optional, Any, List, Tuple
from contextlib import contextmanager
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

try:
    import psycopg2
    from psycopg2 import pool
    from psycopg2.extras import RealDictCursor
    DB_DRIVER_AVAILABLE = True
except ImportError:
    logger.warning("psycopg2 driver not found. Database features will be disabled.")
    psycopg2 = None
    DB_DRIVER_AVAILABLE = False


def get_db_connection():
    """Get simple database connection (for backward compatibility)"""
    if not DB_DRIVER_AVAILABLE:
        raise ImportError("psycopg2 driver not available")
        
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 5432)),
            database=os.getenv("DB_NAME", "rfp_automation"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres")
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise


class DatabaseManager:
    """PostgreSQL database connection manager"""
    
    def __init__(self):
        self.connection_pool = None
        if DB_DRIVER_AVAILABLE:
            self._initialize_pool()
        else:
            logger.warning("DatabaseManager initialized in simplified mode (no driver)")
    
    def _initialize_pool(self):
        """Initialize connection pool"""
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME', 'rfp_automation'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'postgres')
            )
            logger.info("Database connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize connection pool: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Get connection from pool with context manager"""
        if not self.connection_pool:
            raise RuntimeError("Database connection pool not initialized")
            
        conn = None
        try:
            conn = self.connection_pool.getconn()
            yield conn
        finally:
            if conn:
                self.connection_pool.putconn(conn)
    
    def execute_query(self, query: str, params: Optional[Tuple] = None, 
                     fetch: bool = True) -> Optional[List[Tuple]]:
        """
        Execute a query with retry logic
        
        Args:
            query: SQL query string
            params: Query parameters
            fetch: Whether to fetch results
            
        Returns:
            Query results if fetch=True, None otherwise
        """
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                with self.get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query, params)
                        
                        if fetch:
                            results = cursor.fetchall()
                            conn.commit()
                            return results
                        else:
                            conn.commit()
                            return None
            except Exception as e:
                logger.error(f"Query execution failed (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                else:
                    raise
    
    def execute_transaction(self, queries: List[Tuple[str, Optional[Tuple]]]) -> bool:
        """
        Execute multiple queries in a transaction
        
        Args:
            queries: List of (query, params) tuples
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    for query, params in queries:
                        cursor.execute(query, params)
                    conn.commit()
                    logger.info(f"Transaction with {len(queries)} queries completed")
                    return True
        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            if conn:
                conn.rollback()
            return False
    
    def close_pool(self):
        """Close all connections in pool"""
        if self.connection_pool:
            self.connection_pool.closeall()
            logger.info("Database connection pool closed")


# Global database manager instance
# db_manager = DatabaseManager()

_db_manager = None

def get_db_manager():
    """Lazy initialization of database manager"""
    global _db_manager
    if _db_manager is None:
        try:
            _db_manager = DatabaseManager()
        except Exception as e:
            logger.error(f"Could not initialize DatabaseManager: {e}")
            return None
            
    # If pool is not initialized (e.g. no driver), return None to force Mock usage
    if _db_manager and not _db_manager.connection_pool:
        return None
        
    return _db_manager
