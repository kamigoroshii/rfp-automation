print("Starting...", flush=True)
import sys
import os
sys.path.append(os.getcwd())

print("Importing RedisManager...", flush=True)
try:
    from shared.cache.redis_manager import RedisManager
    print("RedisManager imported.", flush=True)
except Exception as e:
    print(f"Error importing RedisManager: {e}", flush=True)

print("Importing SalesAgent...", flush=True)
try:
    from agents.sales.agent import SalesAgent
    print("SalesAgent imported.", flush=True)
except Exception as e:
    print(f"Error importing SalesAgent: {e}", flush=True)

print("Importing TechnicalAgent...", flush=True)
try:
    from agents.technical.agent import TechnicalAgent
    print("TechnicalAgent imported.", flush=True)
except Exception as e:
    print(f"Error importing TechnicalAgent: {e}", flush=True)

print("Importing PricingAgent...", flush=True)
try:
    from agents.pricing.agent import PricingAgent
    print("PricingAgent imported.", flush=True)
except Exception as e:
    print(f"Error importing PricingAgent: {e}", flush=True)

print("Importing LearningAgent...", flush=True)
try:
    from agents.learning.agent import LearningAgent
    print("LearningAgent imported.", flush=True)
except Exception as e:
    print(f"Error importing LearningAgent: {e}", flush=True)

print("Done.", flush=True)
