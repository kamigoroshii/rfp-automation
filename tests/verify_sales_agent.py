"""
Verification script for Sales Agent Module
Tests:
1. Redis Manager Connection
2. Sales Agent Go/No-Go Logic
3. Email Ingestion
4. Redis Queue Push
"""
import sys
import os
import logging
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.sales.agent import SalesAgent
from shared.models import RFPSummary
from shared.cache.redis_manager import RedisManager

# Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# Mock logger to just print and write to file
class MockLogger:
    def __init__(self):
        self.log_file = "verification_log.txt"
        with open(self.log_file, "w") as f:
            f.write("--- Verification Log ---\n")
            
    def _log(self, level, msg):
        log_msg = f"{level}: {msg}"
        print(log_msg, flush=True)
        with open(self.log_file, "a") as f:
            f.write(log_msg + "\n")

    def info(self, msg): self._log("INFO", msg)
    def warning(self, msg): self._log("WARN", msg)
    def error(self, msg): self._log("ERROR", msg)
    
logger = MockLogger()

def test_redis_connection():
    logger.info("--- Testing Redis Connection ---")
    try:
        redis_mgr = RedisManager()
        if redis_mgr.connected:
            logger.info("✅ Redis connected successfully")
            return True
        else:
            logger.warning("⚠️ Redis not connected (Expected if no local Redis running)")
            return False
    except Exception as e:
        logger.error(f"❌ Redis connection failed: {e}")
        return False

def test_scoring_logic():
    logger.info("\n--- Testing Go/No-Go Scoring Logic ---")
    agent = SalesAgent()
    
    # Mock Redis to avoid connection errors during logic test
    agent.redis = MagicMock()
    
    # Case 1: Perfect RFP (High Value, Tier 1, Keyword match)
    rfp_high = RFPSummary(
        rfp_id="TEST-HIGH",
        title="Supply of 11kV XLPE Cables",
        source="Test",
        deadline=datetime.now() + timedelta(days=45),
        scope="Requirement for 50km of XLPE cables",
        testing_requirements=[],
        discovered_at=datetime.now(),
        status="new",
        client_tier="Tier-1",
        project_value=2000000.0
    )
    
    is_go_high = agent._evaluate_rfp(rfp_high)
    logger.info(f"High Value Case Score: {rfp_high.go_no_go_score}")
    if is_go_high and rfp_high.go_no_go_score >= 80: # 30(title) + 20(scope) + 30(tier1) + 20(value) = 100
        logger.info("✅ High Value Case Passed")
    else:
        logger.error(f"❌ High Value Case Failed (Got {rfp_high.go_no_go_score})")

    # Case 2: Low Value, No Keywords (Should Fail)
    rfp_low = RFPSummary(
        rfp_id="TEST-LOW",
        title="General Office Supplies",
        source="Test",
        deadline=datetime.now() + timedelta(days=45),
        scope="Pens and paper",
        testing_requirements=[],
        discovered_at=datetime.now(),
        status="new",
        client_tier="Standard",
        project_value=5000.0
    )
    
    is_go_low = agent._evaluate_rfp(rfp_low)
    logger.info(f"Low Value Case Score: {rfp_low.go_no_go_score}")
    if not is_go_low and rfp_low.go_no_go_score < 40:
        logger.info("✅ Low Value Case Correctly Rejected")
    else:
        logger.error(f"❌ Low Value Case Incorrectly Accepted")
        
    # Case 3: Deadline too far (> 90 days)
    rfp_far = RFPSummary(
        rfp_id="TEST-FAR",
        title="Supply of Cables",
        source="Test",
        deadline=datetime.now() + timedelta(days=100),
        scope="Cables",
        testing_requirements=[],
        discovered_at=datetime.now(),
        status="new"
    )
    
    is_go_far = agent._evaluate_rfp(rfp_far)
    if not is_go_far:
        logger.info("✅ Far Deadline Correctly Rejected")
    else:
        logger.error("❌ Far Deadline Incorrectly Accepted")

def test_email_ingestion():
    logger.info("\n--- Testing Email Ingestion ---")
    agent = SalesAgent()
    agent.redis = MagicMock()
    
    email_data = {
        "subject": "Urgent Tender: 33kV Underground Cables for State Power",
        "body": "We invite bids for 33kV cables. Deadline is 2025-12-30. Value approx 5M.",
        "sender": "tender@statepower.gov" # Should detect Tier-1/Gov
    }
    
    rfp = agent.ingest_email_rfp(email_data)
    
    if rfp:
        logger.info(f"✅ Generated RFP ID: {rfp.rfp_id}")
        logger.info(f"   Score: {rfp.go_no_go_score}")
        logger.info(f"   Tier: {rfp.client_tier}")
        if rfp.client_tier == "Tier-1":
             logger.info("✅ Client Tier Detection Working")
        else:
             logger.error("❌ Client Tier Detection Failed")
    else:
        logger.error("❌ Email Ingestion Failed to produce RFP")

if __name__ == "__main__":
    test_redis_connection()
    test_scoring_logic()
    test_email_ingestion()
