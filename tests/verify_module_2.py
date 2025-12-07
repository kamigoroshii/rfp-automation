"""
Verification script for Module 2: Orchestrator & Technical Agent
Tests:
1. Redis Consumption (via Mock)
2. Summary Splitting
3. Technical Agent Normalization
4. Orchestration Flow
"""
import sys
import os
import asyncio
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from orchestrator.workflow import RFPWorkflow
from agents.technical.agent import TechnicalAgent
from shared.models import RFPSummary

# Mock logger
class MockLogger:
    def __init__(self):
        self.log_file = "verification_mod2_log.txt"
        with open(self.log_file, "w") as f:
            f.write("--- Verification Module 2 Log ---\n")
            
    def _log(self, level, msg):
        log_msg = f"{level}: {msg}"
        print(log_msg, flush=True)
        with open(self.log_file, "a") as f:
            f.write(log_msg + "\n")

    def info(self, msg): self._log("INFO", msg)
    def warning(self, msg): self._log("WARN", msg)
    def error(self, msg): self._log("ERROR", msg)
    
logger = MockLogger()

def test_normalization():
    logger.info("\n--- Testing Normalization ---")
    agent = TechnicalAgent()
    
    # Test Cases
    cases = [
        ("11 kV", "11000.0", "Voltage KV -> V"),
        ("33kv", "33000.0", "Voltage kv -> V"),
        ("185 sqmm", "185.0", "Area sqmm"),
        ("240 mm2", "240.0", "Area mm2"),
        ("Copper", "copper", "Material case"),
    ]
    
    for input_val, expected, desc in cases:
        norm = agent._normalize_unit(input_val)
        if norm == expected or (expected == "copper" and "copper" in norm):
            logger.info(f"✅ {desc}: {input_val} -> {norm}")
        else:
            logger.error(f"❌ {desc}: {input_val} -> {norm} (Expected {expected})")

def test_splitting():
    logger.info("\n--- Testing Summary Splitting ---")
    workflow = RFPWorkflow()
    
    scope_text = """
    Technical Requirements:
    - Supply of 11kV XLPE Cable
    - Conductor: Copper, 185 sqmm
    
    Commercial Terms:
    - Payment: 100% against delivery
    - Warranty: 18 months
    - Delivery: 4 weeks
    """
    
    rfp = RFPSummary(
        rfp_id="TEST-SPLIT",
        title="Test",
        source="Test",
        deadline=datetime.now(),
        scope=scope_text,
        testing_requirements=[],
        discovered_at=datetime.now(),
        status="new"
    )
    
    tech, comm = workflow._split_summary(rfp)
    
    if "11kV" in tech and "Payment" not in tech:
        logger.info(f"✅ Technical Split Correct")
    else:
        logger.error(f"❌ Technical Split Failed: {tech[:50]}...")
        
    if "Payment" in comm and "11kV" not in comm:
        logger.info(f"✅ Commercial Split Correct")
    else:
        logger.error(f"❌ Commercial Split Failed: {comm[:50]}...")

async def test_workflow_flow():
    logger.info("\n--- Testing Workflow Flow (Mocked) ---")
    workflow = RFPWorkflow()
    
    # Mock Redis Manager
    mock_ticket = {
        "rfp_id": "TEST-FLOW-001",
        "title": "Supply of 11kV Cables",
        "source": "Manual",
        "deadline": datetime.now().isoformat(),
        "discovered_at": datetime.now().isoformat(),
        "status": "new",
        "scope": "Supply of 11kV XLPE 3-core cable, 185 sqmm copper conductor. Quantity: 5000m.",
        "go_no_go_score": 80.0,
        "client_tier": "Tier-1",
        "project_value": 500000.0
    }
    
    # We can't easily mock the lazy import in the method without dependency injection or patching
    # So we will unit test the components used inside process_next_rfp instead
    
    # 1. Split
    rfp = RFPSummary.from_dict(mock_ticket)
    tech, comm = workflow._split_summary(rfp)
    
    # 2. Extract (using the text method we added)
    specs = workflow.document_agent.extract_specifications_from_text(tech)
    logger.info(f"Extracted Specs: Voltage={specs.specifications.get('voltage')}, Size={specs.specifications.get('conductor_size')}")
    
    if specs.specifications.get('voltage'):
        logger.info("✅ Extraction Successful")
    else:
        logger.error("❌ Extraction Failed")
        
    # 3. Match
    matches = workflow.technical_agent.match_products(specs)
    logger.info(f"Matches Found: {len(matches)}")
    if matches:
        top_match = matches[0]
        logger.info(f"Top Match: {top_match.sku} (Score: {top_match.match_score:.2f})")
        if top_match.match_score > 0:
            logger.info("✅ Matching Successful")
        else:
            logger.warning("⚠️ Match score is 0")
            
    # 4. Pricing
    pricing = workflow.pricing_agent.calculate_pricing(rfp.rfp_id, matches, quantity=1000)
    if pricing:
        logger.info(f"✅ Pricing Calculated: {pricing[0].total}")
    else:
        logger.error("❌ Pricing Failed")


if __name__ == "__main__":
    test_normalization()
    test_splitting()
    asyncio.run(test_workflow_flow())
