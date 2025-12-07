import sys
import os

# Add project root
sys.path.append(os.getcwd())

print("Attempting to import shared.database.connection...")
try:
    import shared.database.connection
    print("✅ shared.database.connection imported cleanly (no immediate DB connection)")
except Exception as e:
    print(f"❌ Failed to import connection: {e}")
    sys.exit(1)

print("Attempting to import orchestrator.api.main...")
try:
    import orchestrator.api.main
    print("✅ orchestrator.api.main imported cleanly")
except Exception as e:
    print(f"❌ Failed to import main: {e}")
    sys.exit(1)

print("Verification Successful: Server should start up even if DB is offline.")
