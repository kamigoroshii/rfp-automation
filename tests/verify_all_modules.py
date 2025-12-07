"""
Consolidated Verification Script for Modules 1, 2, and 3
Verifies the logic implementation of:
1. Sales Agent (Go/No-Go Scoring)
2. Technical Agent (Equal-Weight Scoring & Normalization)
3. Pricing Agent (Bid Banding)
4. Learning Agent (Adaptive Weights)
"""
import sys
import os
import logging
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("VERIFY_ALL")

from shared.models import RFPSummary, Specification, ProductMatch
from agents.sales.agent import SalesAgent
from agents.technical.agent import TechnicalAgent
from agents.pricing.agent import PricingAgent
from agents.learning.agent import LearningAgent
from shared.cache.redis_manager import RedisManager

# Mock Redis Manager to prevent connection errors during logic verification
class MockRedisManager:
    def __init__(self):
        self.connected = True
        self.queues = {}
    
    def push_rfp(self, rfp_data, queue_name="rfp_tickets"):
        if queue_name not in self.queues:
            self.queues[queue_name] = []
        self.queues[queue_name].append(rfp_data)
        return True
        
    def pop_rfp(self, queue_name="rfp_tickets"):
        if queue_name in self.queues and self.queues[queue_name]:
            return self.queues[queue_name].pop(0)
        return None

# Monkey patch the singleton instance
RedisManager._instance = MockRedisManager()

class VerificationSuite:
    def __init__(self):
        self.sales_agent = SalesAgent()
        self.tech_agent = TechnicalAgent()
        self.pricing_agent = PricingAgent()
        self.learning_agent = LearningAgent()
        self.errors = []

    def assert_true(self, condition, message):
        if condition:
            logger.info(f"✅ PASS: {message}")
        else:
            logger.error(f"❌ FAIL: {message}")
            self.errors.append(message)

    def verify_module_1_sales(self):
        logger.info("\n--- Module 1: Sales Agent Logic ---")
        
        # Test Go/No-Go Logic
        # Case 1: High Value, Tier 1, Near Deadline (Should be GO)
        rfp_text_go = "Supply of 11kV XLPE Cables for State Electricity Board. Budget: 50 Lakhs."
        
        # We need to simulate the _evaluate_rfp method behavior or use public methods
        # Since _evaluate_rfp is internal, we'll mimic the scoring check logic or access it if possible
        # Accessing protected member for verification
        
        # Helper Test: Client Tier Logic
        sender_tier1 = "State Electricity Board (Gov)"
        tier = self.sales_agent._determine_client_tier(sender_tier1)
        self.assert_true(tier == "Tier-1", f"Sender '{sender_tier1}' should be Tier-1")
        
        rfp_summary = RFPSummary(
            rfp_id="TEST-GO",
            title="Supply of 11kV Cables",
            source="Test Source",
            deadline=datetime.now() + timedelta(days=30),
            scope=rfp_text_go,
            testing_requirements=[],
            discovered_at=datetime.now(),
            status="new",
            client_tier=tier, # Set derived tier
            project_value=5000000.0 # 50 Lakhs
        )
        
        self.sales_agent._evaluate_rfp(rfp_summary)
        
        logger.info(f"RFP Score: {rfp_summary.go_no_go_score}")
        self.assert_true(rfp_summary.go_no_go_score >= 40, "Go/No-Go Score should be >= 40 for good RFP")

    def verify_module_2_technical(self):
        logger.info("\n--- Module 2: Technical Agent Logic ---")
        
        # Test 1: Normalization
        val1 = self.tech_agent._normalize_unit("11 kV")
        val2 = self.tech_agent._normalize_unit("11000 V")
        self.assert_true(val1 == "11000.0", f"Normalization '11 kV' -> {val1}")
        
        # Test 2: Equal Weight Scoring
        # Create Dummy Specs
        rfp_specs = {
            'voltage': '11 kV', 
            'conductor_size': '185 sqmm',
            'conductor_material': 'Copper'
        }
        
        prod_specs_perfect = {
            'voltage': '11000',
            'conductor_size': '185',
            'conductor_material': 'Copper'
        }
        
        prod_specs_partial = {
            'voltage': '11000',
            'conductor_size': '300', # Mismatch
            'conductor_material': 'Copper'
        }
        
        score_perfect = self.tech_agent._calculate_match_score(rfp_specs, prod_specs_perfect)
        score_partial = self.tech_agent._calculate_match_score(rfp_specs, prod_specs_partial)
        
        # Perfect should be 1.0 (or close)
        # Partial (2/3 matches) should be 0.66
        
        self.assert_true(score_perfect > 0.99, f"Perfect Match Score: {score_perfect}")
        self.assert_true(0.6 < score_partial < 0.7, f"Partial Match Score (2/3): {score_partial}")

    def verify_module_3_pricing_learning(self):
        logger.info("\n--- Module 3: Pricing & Learning Logic ---")
        
        # Pricing: Bid Banding
        sku = "XLPE-11KV-185"
        band = self.pricing_agent.calculate_bid_band(sku)
        
        logger.info(f"Bid Band for {sku}: {band}")
        self.assert_true(band['p25'] < band['median'] < band['p75'], "Bid Band should be P25 < Median < P75")
        
        # Pricing: Recommendation Strategy
        # High score -> Aggressive price
        match_high = ProductMatch(
            sku=sku, 
            product_name="Cable", 
            match_score=0.95, 
            specification_alignment={},
            datasheet_url="http://mock.url/spec.pdf" # Fixed: Added missing arg
        )
        pricing_list = self.pricing_agent.calculate_pricing("TEST", [match_high])
        
        rec_sku = self.pricing_agent.get_recommended_product(pricing_list, [match_high])
        self.assert_true(rec_sku == sku, "Should recommend the valid product")
        
        # Learning: Adaptive Weights
        logger.info(f"Original Weights: {self.learning_agent.adaptive_weights}")
        
        # Simulate a LOSS
        self.learning_agent._adjust_weights('loss')
        
        new_weights = self.learning_agent.adaptive_weights
        logger.info(f"New Weights: {new_weights}")
        
        self.assert_true(new_weights['price_competitiveness'] > 0.3, "Price weight should increase after loss")

    def run(self):
        logger.info("STARTING FULL SYSTEM VERIFICATION")
        try:
            self.verify_module_1_sales()
            self.verify_module_2_technical()
            self.verify_module_3_pricing_learning()
            
            if not self.errors:
                logger.info("\n🌟 ALL MODULES VERIFIED SUCCESSFULLY 🌟")
                logger.info("The system is ready for Module 4 integration (Frontend/E2E).")
                return True
            else:
                logger.error(f"\n⚠️ FOUND {len(self.errors)} ISSUES")
                return False
                
        except Exception as e:
            logger.error(f"FATAL ERROR IN VERIFICATION: {e}", exc_info=True)
            return False

if __name__ == "__main__":
    suite = VerificationSuite()
    success = suite.run()
    if not success:
        sys.exit(1)
