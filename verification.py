
import asyncio
import aiohttp
from datetime import datetime

API_URL = "http://localhost:8003/api"

async def test_backend():
    print("Testing Backend API...")
    
    async with aiohttp.ClientSession() as session:
        # 1. Test Create JSON RFP
        print("\n1. Testing Create JSON RFP...")
        rfp_payload = {
            "title": "Test RFP for Verification",
            "source": "Verification Script",
            "deadline": datetime.now().isoformat(),
            "scope": "Testing verification process",
            "testing_requirements": ["test1"],
            "match_score": 0.95,
            "total_estimate": 100000.0,
            "specifications": [{"type": "test", "value": "check"}],
            "matches": [{"sku": "XLPE-33KV-3C-400", "match_score": 0.95, "name": "33kV 3-Core XLPE Cable 400sqmm"}],
            "pricing": [{"sku": "XLPE-33KV-3C-400", "total": 100000.0, "unit_price": 40.0, "quantity": 2500, "breakdown": {"material_cost": {"amount": 80000.0}, "testing_cost": {"amount": 10000.0}, "delivery_cost": {"amount": 5000.0}, "urgency_premium": {"amount": 5000.0}}}],
            "recommended_sku": "XLPE-33KV-3C-400"
        }
        
        try:
            async with session.post(f"{API_URL}/rfp/create-json", json=rfp_payload) as resp:
                print(f"Status: {resp.status}")
                if resp.status == 200:
                    data = await resp.json()
                    rfp_id = data.get('id') or data.get('rfp_id')
                    print(f"Success! Created RFP ID: {rfp_id}")
                else:
                    text = await resp.text()
                    print(f"Failed: {text}")
                    return

            # 2. Test PDF Generation
            print(f"\n2. Testing PDF Generation for {rfp_id}...")
            async with session.post(f"{API_URL}/rfp/{rfp_id}/generate-pdf") as resp:
                print(f"Status: {resp.status}")
                if resp.status == 200:
                    data = await resp.json()
                    print(f"Success! PDF URL: {data.get('download_url')}")
                else:
                    text = await resp.text()
                    print(f"Failed: {text}")

        except Exception as e:
            print(f"Exception during test: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(test_backend())
    except ImportError:
        # Fallback if aiohttp not installed
        import requests
        print("Using requests library fallback...")
        # ... sync implementation if needed, but assuming aiohttp or just simple requests
        pass
