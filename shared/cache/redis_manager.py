"""
Redis Manager - Handles connection and queue operations for Redis
"""
import os
import redis
import json
import logging
from typing import Dict, Any, Optional
from threading import Lock

logger = logging.getLogger(__name__)

class RedisManager:
    """Singleton helper for Redis operations"""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(RedisManager, cls).__new__(cls)
                cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize Redis connection"""
        try:
            host = os.getenv("REDIS_HOST", "localhost")
            port = int(os.getenv("REDIS_PORT", 6379))
            db = int(os.getenv("REDIS_DB", 0))
            password = os.getenv("REDIS_PASSWORD", None)
            
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True
            )
            
            # Test connection
            self.client.ping()
            logger.info(f"Connected to Redis at {host}:{port}")
            self.connected = True
            
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            self.connected = False
            self.client = None
        except Exception as e:
            logger.error(f"Error initializing Redis: {str(e)}")
            self.connected = False
            self.client = None
            
    def push_rfp(self, rfp_data: Dict[str, Any], queue_name: str = "rfp_tickets") -> bool:
        """
        Push RFP data to a Redis queue
        
        Args:
            rfp_data: Dictionary containing RFP data
            queue_name: Name of the Redis list/queue
            
        Returns:
            True if successful, False otherwise
        """
        if not self.connected or not self.client:
            logger.warning("Redis not connected. Cannot push RFP.")
            return False
            
        try:
            # Convert to JSON string
            payload = json.dumps(rfp_data)
            
            # Push to right end of list (queue)
            self.client.rpush(queue_name, payload)
            
            logger.debug(f"Pushed RFP to {queue_name}: {rfp_data.get('rfp_id', 'unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Error pushing to Redis queue {queue_name}: {str(e)}")
            return False

    def pop_rfp(self, queue_name: str = "rfp_tickets") -> Optional[Dict[str, Any]]:
        """
        Pop RFP data from a Redis queue (blocking)
        
        Args:
            queue_name: Name of the Redis list/queue
            
        Returns:
            RFP data dictionary or None
        """
        if not self.connected or not self.client:
            return None
            
        try:
            # BLPOP returns a tuple (key, element) or None
            # Timeout 0 blocks indefinitely, but we use a small timeout to allow graceful shutdowns if needed
            # For this simple implementation, we'll use lpop (non-blocking) or blpop with timeout
            
            # Non-blocking pop
            result = self.client.lpop(queue_name)
            
            if result:
                return json.loads(result)
            return None
            
        except Exception as e:
            logger.error(f"Error popping from Redis queue {queue_name}: {str(e)}")
            return None
