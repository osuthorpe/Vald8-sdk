"""
Google GenAI Vald8 Example.

Requires GEMINI_API_KEY to be set in .env or environment variables.
"""

import os
from dotenv import load_dotenv
from vald8 import vald8

# Load environment variables
load_dotenv()

try:
    from google import genai
except ImportError:
    genai = None

# Initialize client
gemini_client = None
if genai and os.getenv("GEMINI_API_KEY"):
    gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@vald8(dataset="examples/eval_dataset.jsonl")
def call_gemini_15(prompt: str) -> str:
    """Calls Google's Gemini 1.5 Pro."""
    if not gemini_client:
        return "Error: Google GenAI client not initialized or missing API key."

    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Gemini API Error: {str(e)}"


if __name__ == "__main__":
    print("🚀 Running Google Gemini Evaluation")
    if gemini_client:
        results = call_gemini_15.run_eval()
        print(f"   Result: {'✅ PASSED' if results['passed'] else '❌ FAILED'}")
        print(f"   Success Rate: {results['summary']['success_rate']:.1%}")
    else:
        print("   ⚠️ Skipped: Gemini API key missing or SDK not installed.")
