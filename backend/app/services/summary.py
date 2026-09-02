import os
from app.models.threat import Threat


def build_briefing_prompt(threats: list[Threat]) -> str:
    lines = [
        "You are a SOC analyst writing a short daily threat briefing for a logistics "
        "and supply chain company. Summarize the following top-priority threats in "
        "plain English, 3-5 sentences, for a non-technical manager audience. "
        "Mention the highest-priority items by name and why they matter to the business.",
        "",
        "Top priority threats:",
    ]
    for t in threats:
        tag_str = t.tags if t.tags else "untagged"
        lines.append(
            f"- [{t.priority_score}] ({t.source}, tags: {tag_str}) {t.title}: "
            f"{(t.description or '')[:200]}"
        )
    return "\n".join(lines)


def get_ai_summary(prompt: str, break_gemini: bool = False) -> tuple[str, str]:
    # Tier 1: Gemini
    try:
        from google import genai
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        model_name = "gemini-nonexistent-model" if break_gemini else "gemini-3.6-flash"
        interaction = client.interactions.create(model=model_name, input=prompt)
        return interaction.output_text.strip(), "gemini"
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
        return completion.choices[0].message.content.strip(), "groq"
    except Exception as e:
        print(f"[fallback chain] Groq failed ({e}), using static template...")

    # Tier 3: static template
    return (
        "Summary unavailable — AI providers unreachable. Showing raw threat data instead.",
        "static",
    )
