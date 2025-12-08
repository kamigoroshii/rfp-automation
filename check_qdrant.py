"""
Check if Qdrant is running and accessible
"""
import requests

print("🔍 Checking Qdrant status...")
print("=" * 60)

try:
    response = requests.get("http://localhost:6333/", timeout=5)
    if response.status_code == 200:
        print("✅ Qdrant is running!")
        print(f"   Response: {response.json()}")
        
        # Check collections
        try:
            collections_response = requests.get("http://localhost:6333/collections", timeout=5)
            if collections_response.status_code == 200:
                collections = collections_response.json()
                print(f"\n📚 Collections: {collections}")
        except:
            pass
            
    else:
        print(f"⚠️  Qdrant responded with status: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("❌ Qdrant is NOT running!")
    print("\n📝 To start Qdrant:")
    print("   Option 1 (Docker): docker run -p 6333:6333 qdrant/qdrant")
    print("   Option 2 (Standalone): Download from https://qdrant.tech/")
    print("   Option 3 (Cloud): Use Qdrant Cloud at https://cloud.qdrant.io/")
except Exception as e:
    print(f"❌ Error: {e}")

print("=" * 60)
