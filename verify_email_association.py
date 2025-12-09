
import asyncio
from orchestrator.services.rfp_service import RFPService

async def verify():
    rfp_id = "RFP-EMAIL-20251209-E60B" 
    # Use the one from the last run. If it failed, use the one from logs.
    # The last log said: RFP-EMAIL-20251209-E60B
    
    service = RFPService()
    print(f"Fetching RFP {rfp_id}...")
    rfp = await service.get_rfp_by_id(rfp_id)
    
    if rfp:
        print(f"RFP Found: {rfp.get('title')}")
        print(f"Source: {rfp.get('source')}")
        print(f"Source Email (Extracted): {rfp.get('source_email')}")
        
        if rfp.get('source_email') == "procurement@metro-infra.gov.in":
            print("SUCCESS: Source email correctly associated!")
        else:
            print(f"FAILURE: Expected procurement@metro-infra.gov.in, got {rfp.get('source_email')}")
    else:
        print("RFP Not Found in DB (check ID)")

if __name__ == "__main__":
    asyncio.run(verify())
