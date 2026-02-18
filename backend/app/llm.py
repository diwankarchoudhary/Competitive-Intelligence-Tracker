import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")

client = OpenAI(api_key=API_KEY)

def summarize_diff(diff_text: str) -> str:
    if not diff_text.strip():
        return "No meaningful changes detected."

    prompt = f"""
You are a competitive intelligence analyst.

Summarize ONLY meaningful changes.
Ignore formatting-only changes.
Focus on pricing, features, or policy changes.
Include short quoted snippets as evidence.

DIFF:
{diff_text[:6000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI summary failed: {str(e)}"
