import os
from dotenv import load_dotenv

load_dotenv()

print("=== Testing Gemini ===")
try:
    from google import genai
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input="Reply with exactly: Gemini OK"
    )
    print(f"Gemini response: {interaction.output_text.strip()}")
except Exception as e:
    print(f"Gemini FAILED: {e}")

print("\n=== Testing Groq ===")
try:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    completion = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        messages=[{"role": "user", "content": "Reply with exactly: Groq OK"}],
    )
    print(f"Groq response: {completion.choices[0].message.content.strip()}")
except Exception as e:
    print(f"Groq FAILED: {e}")
