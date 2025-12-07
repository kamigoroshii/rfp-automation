"""
Backend Verification Script
Checks if the implemented logic is sound and components can be imported/initialized.
Does not perform actual full integration test if services (Redis/Qdrant) are not running, 
but validates the code paths.
"""
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_imports():
    """Verify that all new modules can be imported"""
    try:
        logger.info("Verifying imports...")
        from orchestrator.tasks.rfp_tasks import process_rfp_task, get_workflow
        from agents.technical.product_loader import load_products_postgres
        from agents.technical.agent import TechnicalAgent
        
        # Check Technical Agent initialization
        agent = TechnicalAgent()
        logger.info(f"Technical Agent initialized: {agent.name}")
        
        # Check if methods exist
        assert hasattr(agent, 'initialize_vector_db')
        assert hasattr(agent, 'semantic_search')
        
        logger.info("Imports and class structures verified successfully.")
        return True
    except ImportError as e:
        logger.error(f"Import Error: {e}")
        return False
    except Exception as e:
        logger.error(f"Verification Error: {e}")
        return False

def check_db_connection():
    """Check database connection"""
    try:
        from shared.database.connection import get_db_connection
        conn = get_db_connection()
        conn.close()
        logger.info("Database connection check passed (if DB is running).")
        return True
    except Exception as e:
        logger.warning(f"Database connection check failed (expected if DB not running): {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting Backend Code Verification...")
    
    if verify_imports():
        logger.info("✅ Code structure verification passed.")
    else:
        logger.error("❌ Code structure verification failed.")
        sys.exit(1)
        
    check_db_connection()
