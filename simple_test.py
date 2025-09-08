#!/usr/bin/env python3
"""
Simple test to verify Vald8 basic functionality.
"""

import json
from pathlib import Path

# Add current directory to path
import sys
sys.path.insert(0, '.')

from vald8 import vald8

# Create a simple test dataset
test_data = [
    {"id": "test1", "input": "2+2", "expected": {"reference": "4"}},
    {"id": "test2", "input": "hello", "expected": {"contains": ["hello"]}}
]

# Write test dataset
with open("simple_test.jsonl", "w") as f:
    for item in test_data:
        f.write(json.dumps(item) + "\n")

# Define a simple function with @vald8
@vald8(dataset="simple_test.jsonl")
def simple_function(input_text: str) -> str:
    """Simple test function."""
    if input_text == "2+2":
        return "4"
    elif "hello" in input_text.lower():
        return "hello world"
    else:
        return "unknown"

if __name__ == "__main__":
    print("🚀 Testing Vald8 basic functionality\n")
    
    # Test normal function usage
    print("1️⃣ Normal function usage:")
    print(f'   simple_function("2+2") = "{simple_function("2+2")}"')
    print(f'   simple_function("hello") = "{simple_function("hello")}"')
    print()
    
    # Test evaluation
    print("2️⃣ Running evaluation:")
    try:
        results = simple_function.run_eval()
        print(f"   Result: {'✅ PASSED' if results['passed'] else '❌ FAILED'}")
        print(f"   Success Rate: {results['summary']['success_rate']:.1%}")
        print(f"   Tests: {results['summary']['passed_tests']}/{results['summary']['total_tests']}")
        print(f"   Run ID: {results['run_id'][:8]}")
        if results['run_dir']:
            print(f"   Results saved to: {results['run_dir']}")
        print()
        
        print("3️⃣ Test details:")
        for metric_name, stats in results['summary']['metrics'].items():
            print(f"   {metric_name}: {stats['mean']:.2f} (min: {stats['min']:.2f}, max: {stats['max']:.2f})")
        
    except Exception as e:
        print(f"   ❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Cleanup
    Path("simple_test.jsonl").unlink(missing_ok=True)
    
    print("\n🎉 Test completed!")