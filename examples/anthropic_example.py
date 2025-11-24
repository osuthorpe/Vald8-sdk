"""
Anthropic Vald8 Example.

Requires ANTHROPIC_API_KEY to be set in .env or environment variables.
"""

import os
from dotenv import load_dotenv
from vald8 import vald8

# Load environment variables
load_dotenv()

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

# Initialize client
anthropic_client = Anthropic() if Anthropic and os.getenv("ANTHROPIC_API_KEY") else None


@vald8(dataset="examples/eval_dataset.jsonl")
def call_claude_35(prompt: str) -> str:
    """Calls Anthropic's Claude 3.5 Sonnet."""
    if not anthropic_client:
        return "Error: Anthropic client not initialized or missing API key."

    try:
        response = anthropic_client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Anthropic API Error: {str(e)}"


if __name__ == "__main__":
    print("🚀 Running Anthropic Evaluation")
    if anthropic_client:
        results = call_claude_35.run_eval()
        print(f"   Result: {'✅ PASSED' if results['passed'] else '❌ FAILED'}")
        print(f"   Success Rate: {results['summary']['success_rate']:.1%}")
    else:
        print("   ⚠️ Skipped: Anthropic API key missing or SDK not installed.")
