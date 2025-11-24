"""
OpenAI Vald8 Example.

Requires OPENAI_API_KEY to be set in .env or environment variables.
"""

import os
from dotenv import load_dotenv
from vald8 import vald8

# Load environment variables
load_dotenv()

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Initialize client
openai_client = OpenAI() if OpenAI and os.getenv("OPENAI_API_KEY") else None


@vald8(dataset="examples/eval_dataset.jsonl")
def call_openai_gpt5(prompt: str) -> str:
    """
    Calls OpenAI's GPT-5.1 model.
    """
    if not openai_client:
        return "Error: OpenAI client not initialized or missing API key."

    try:
        response = openai_client.chat.completions.create(
            model="gpt-5.1",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI API Error: {str(e)}"


if __name__ == "__main__":
    print("🚀 Running OpenAI Evaluation")
    if openai_client:
        results = call_openai_gpt5.run_eval()
        print(f"   Result: {'✅ PASSED' if results['passed'] else '❌ FAILED'}")
        print(f"   Success Rate: {results['summary']['success_rate']:.1%}")
    else:
        print("   ⚠️ Skipped: OpenAI API key missing or SDK not installed.")
