"""Test which Gemini models are available"""
import os
import google.generativeai as genai
from orchestrator.config import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)

print("Available Gemini models:")
print("=" * 60)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✓ {model.name}")
        print(f"  Display: {model.display_name}")
        print(f"  Methods: {', '.join(model.supported_generation_methods)}")
        print()
