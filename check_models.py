import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    # Hardcoding briefly for the test script using the key user provided earlier
    # To avoid .env parsing issues
    api_key = "AIzaSyCy9nHyUY55euTPN7E6Ufq02HOnKoSLFos"

genai.configure(api_key=api_key)

print("Listing available models:")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")
