import os
from dotenv import load_dotenv

load_dotenv()

def get_ai_summary(prompt: str, break_gemini: bool = False) -> str:
    # Tier 1: Gemini
    try:
        from google import genai
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        model_name = "gemini-nonexistent-model" if break_gemini else "gemini-3.6-flash"
        interaction = client.interactions.create(model=model_name, input=prompt)
        print("[fallback chain] Gemini succeeded")
        return interaction.output_text.strip()
    except Exception as e:
        print(f"[fallback chain] Gemini failed ({e}), trying Groq...")

    # Tier 2: Groq
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        completion = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
            messages=[{"role": "user", "content": prompt}],
        )
        print("[fallback chain] Groq succeeded")
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"[fallback chain] Groq failed ({e}), using static template...")

    # Tier 3: static template
    print("[fallback chain] Using static fallback")
    return "Summary unavailable — AI providers unreachable. Showing raw threat data instead."

print("=== Test 1: normal path (Gemini should succeed) ===")
result = get_ai_summary("Reply with exactly: chain test", break_gemini=False)
print(f"Result: {result}\n")

print("=== Test 2: forced fallback (Gemini broken, Groq should catch it) ===")
result = get_ai_summary("Reply with exactly: chain test", break_gemini=True)
print(f"Result: {result}")
