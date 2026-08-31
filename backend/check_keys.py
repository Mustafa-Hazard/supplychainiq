import os
from dotenv import load_dotenv

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

print(f"GEMINI_API_KEY loaded: {bool(gemini_key)} (length: {len(gemini_key) if gemini_key else 0})")
print(f"GROQ_API_KEY loaded: {bool(groq_key)} (length: {len(groq_key) if groq_key else 0})")
