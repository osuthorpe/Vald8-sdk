#!/usr/bin/env python3
"""
Quick test to verify core Vald8 functionality works correctly.
"""

import sys
sys.path.insert(0, '.')

import json
from pathlib import Path
from vald8 import DatasetExample, vald8, load_dataset, validate_dataset_format

def test_dataset_example():
    """Test DatasetExample model creation."""
    print("Testing DatasetExample creation...")
    
    example = DatasetExample(
        id="test1",
        input="What is 2+2?",
        expected={"reference": "4"}
    )
    
    assert example.id == "test1"
    assert example.input == "What is 2+2?"
    assert example.expected == {"reference": "4"}
    print("✅ DatasetExample creation works")

def test_dataset_loading():
    """Test dataset loading."""
    print("Testing dataset loading...")
    
    # Create test dataset
    test_dataset = Path("test_loading.jsonl")
    with open(test_dataset, 'w') as f:
        f.write('{"id": "test1", "input": "hello", "expected": {"reference": "world"}}\n')
        f.write('{"id": "test2", "input": "foo", "expected": {"reference": "bar"}}\n')
    
    try:
        examples = load_dataset(str(test_dataset))
        assert len(examples) == 2
        assert all(isinstance(ex, DatasetExample) for ex in examples)
        print("✅ Dataset loading works")
        
        # Test validation
        warnings = validate_dataset_format(str(test_dataset))
        assert isinstance(warnings, list)
        print("✅ Dataset validation works")
        
    finally:
        test_dataset.unlink(missing_ok=True)

def test_decorator_basic():
    """Test basic decorator functionality."""
    print("Testing @vald8 decorator...")
    
    # Create temporary dataset
    test_dataset = Path("test_decorator.jsonl")
    with open(test_dataset, 'w') as f:
        f.write('{"id": "test1", "input": "2+2", "expected": {"reference": "4"}}\n')
    
    try:
        @vald8(dataset=str(test_dataset))
        def simple_math(expr: str) -> str:
            if expr == "2+2":
                return "4"
            else:
                return "unknown"
        
        # Test normal function call
        assert simple_math("2+2") == "4"
        
        # Test that it has evaluation methods
        assert hasattr(simple_math, 'run_eval')
        assert hasattr(simple_math, 'get_config')
        
        # Test config access
        config = simple_math.get_config()
        assert config.dataset == str(test_dataset)
        
        print("✅ @vald8 decorator works")
        
        # Test evaluation (basic)
        print("Testing evaluation...")
        results = simple_math.run_eval()
        assert 'passed' in results
        assert 'summary' in results
        assert 'run_id' in results
        print("✅ Evaluation works")
        
    finally:
        test_dataset.unlink(missing_ok=True)

if __name__ == "__main__":
    print("🚀 Running Vald8 Quick Tests\n")
    
    try:
        test_dataset_example()
        print()
        
        test_dataset_loading()
        print()
        
        test_decorator_basic()
        print()
        
        print("🎉 All tests passed! Vald8 is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)