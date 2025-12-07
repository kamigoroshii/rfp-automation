import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test():
    print("Testing Health...")
    try:
        r = requests.get(f"http://localhost:8000/health", timeout=2)
        print(f"Health: {r.status_code} {r.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return

    print("Submitting RFP...")
    data = {
        "title": "Simple Test RFP",
        "source": "E2E Script",
        "deadline": "2025-12-31",
        "scope": "Test Scope"
    }
    try:
        r = requests.post(f"{BASE_URL}/rfp/submit", data=data, timeout=5)
        print(f"Submit: {r.status_code}")
        print(r.text)
    except Exception as e:
        print(f"Submit failed/timed out: {e}")

if __name__ == "__main__":
    test()
