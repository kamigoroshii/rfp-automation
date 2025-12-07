import requests
import time
import uuid
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("E2E_TEST")

BASE_URL = "http://localhost:8005/api"

def test_health():
    try:
        resp = requests.get(f"http://localhost:8005/health")
        if resp.status_code == 200:
            logger.info("✅ Health check passed")
            return True
        else:
            logger.error(f"❌ Health check failed: {resp.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        return False

def test_rfp_flow():
    # 1. Submit RFP
    logger.info("Testing RFP Submission...")
    rfp_data = {
        "title": f"E2E Test RFP {uuid.uuid4()}",
        "source": "E2E Script",
        "deadline": "2025-12-31",
        "scope": "Supply of 11kV XPLE Cables. 50km length. Technical reqs: IEC 60502-2, Copper Conductor.",
        "testing_requirements": "Routine Tests, Type Tests",
        # Optional file upload logic could go here but we use form data mostly
    }
    
    try:
        # Note: API expects Form data for submit
        resp = requests.post(f"{BASE_URL}/rfp/submit", data=rfp_data)
        if resp.status_code == 200:
            data = resp.json()
            rfp_id = data.get("rfp_id")
            logger.info(f"✅ RFP Submitted ID: {rfp_id}")
        else:
            logger.error(f"❌ RFP Submission failed: {resp.text}")
            return
            
        # 2. Poll for status (List)
        logger.info("Testing RFP List & Polling...")
        found = False
        for _ in range(5):
            time.sleep(1)
            resp = requests.get(f"{BASE_URL}/rfp/list?limit=10")
            rfps = resp.json().get("rfps", [])
            target = next((r for r in rfps if r["rfp_id"] == rfp_id), None)
            
            if target:
                logger.info(f"✅ RFP found in list. Status: {target['status']}")
                found = True
                break
        
        if not found:
            logger.warning("⚠️ RFP not found in list after polling (Indexing delay?)")

        # 3. Get Details
        logger.info(f"Testing RFP Details for {rfp_id}...")
        resp = requests.get(f"{BASE_URL}/rfp/{rfp_id}")
        if resp.status_code == 200:
            detail = resp.json()
            # Check if processing happened (might be async/queued)
            logger.info(f"✅ RFP Details fetched. Scope length: {len(detail.get('scope', ''))}")
        else:
            logger.error(f"❌ RFP Details failed: {resp.status_code}")

        # 4. Submit Feedback
        logger.info("Testing Feedback Submission...")
        feedback_data = {
            "outcome": "loss",
            "actual_price": 50000.0,
            "match_accuracy": 0.8,
            "notes": "Price was too high"
        }
        # In API it's params or body? Check route.
        # @router.post("/{rfp_id}/feedback") with args: outcome, actual_price... (Query params by default in FastAPI if not typed as Pydantic model body)
        # Wait, looked at rfp.py earlier:
        # async def submit_feedback(rfp_id: str, outcome: str, ...)
        # These are query parameters unless we wrap them in a Pydantic model or Body
        # Let's verify `rfp.py` signature again...
        # It didn't use Pydantic model in the snippet I saw. It used individual args.
        # FastAPI treats individual args as Query Params for GET/DELETE and Query/Form/Body depending on complexity for POST.
        # If they are simple types, they are Query params often? Or Body if Body(...) used.
        # Let's try sending as query params for safety, or JSON body if it accepts it.
        # Actually, let's look at the implementation again in rfp.py.
        # `async def submit_feedback(...)` - no Body() or Form() markers seen in previous `view_file`.
        # So likely Query params.
        
        resp = requests.post(f"{BASE_URL}/rfp/{rfp_id}/feedback", params=feedback_data)
        if resp.status_code == 200:
            logger.info("✅ Feedback submitted successfully")
        else:
            logger.error(f"❌ Feedback submission failed: {resp.text}")

    except Exception as e:
        logger.error(f"Test failed with exception: {e}")

def test_products():
    logger.info("Testing Product Search...")
    try:
        resp = requests.get(f"{BASE_URL}/products/search?query=cable")
        if resp.status_code == 200:
            data = resp.json()
            products = data.get("products", [])
            logger.info(f"✅ Search successful. Found {len(products)} products.")
            if len(products) > 0:
                logger.debug(f"First product: {products[0].get('product_name')}")
        else:
            logger.error(f"❌ Product search failed: {resp.status_code}")
    except Exception as e:
        logger.error(f"Product test failed: {e}")

if __name__ == "__main__":
    if test_health():
        test_rfp_flow()
        test_products()
    else:
        logger.error("Skipping tests due to health check failure. Is the server running?")
