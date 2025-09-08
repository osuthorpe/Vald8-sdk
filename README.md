# 📦 Vald8 SDK

Vald8 is a lightweight Python SDK for **automated LLM evaluation**.  
Run structured tests against your LLM functions with JSONL datasets, validate behavior, and prevent silent regressions — locally or in CI/CD.

✅ **Works fully local & offline** — no external dependencies required  
✅ **Configurable LLM-as-Judge** — OpenAI, Anthropic, AWS Bedrock, Local  
✅ **Developer-first, CI-friendly** — simple decorators, clear outputs  

---

## 🚀 What is Vald8?

**Vald8 is pytest for LLMs - a lightweight testing framework for AI functions.**

If you're building with LLMs (ChatGPT, Claude, etc.), you need to test that your AI functions work correctly. Just like you test regular Python functions with pytest, Vald8 lets you test LLM functions with real datasets.

**Perfect for:**
- 🔍 **Schema validation** - Ensure JSON responses have the right structure
- 📋 **Instruction adherence** - Verify AI follows your prompts correctly  
- 🛡️ **Regression testing** - Catch when changes break AI behavior
- ⚡ **CI/CD integration** - Run AI tests in your deployment pipeline

**How it works:**
1. Add `@vald8` decorator to any LLM function
2. Create a JSONL test dataset with examples
3. Run `my_function.run_eval()` or in CI with `pytest`

**Zero configuration. Pure open source. Developer-first.**

---

## ✨ Core Testing Capabilities

**🔍 Schema Validation** - "Is my JSON response correct?"
```python
# Test that your AI returns proper JSON structure
expected = {"schema": {"type": "object", "properties": {"answer": {"type": "string"}}}}
```

**📋 Instruction Adherence** - "Did my AI follow the prompt?"
```python  
# Verify AI follows your specific instructions
expected = {"contains": ["step-by-step", "conclusion"]}
```

**🎯 Response Accuracy** - "Is the content correct?"
```python
# Check factual accuracy and expected content
expected = {"reference": "Paris", "contains": ["capital", "France"]}
```

**🛡️ Safety Validation** - "Is the output appropriate?"
```python
# Ensure responses meet safety guidelines  
expected = {"safe": true, "no_harmful_content": true}
```

**⚡ CI-First Design**
- 🚀 **Fast**: Optimized for CI/CD pipelines
- 💰 **Cost-effective**: Configurable to minimize API costs
- 🔧 **Zero setup**: Works with existing Python test infrastructure
- 📊 **Clear reporting**: Pass/fail with detailed context  

---

## 📝 How to Create Test Data

**Test data is just a simple text file with examples.**

Each line has one test case in this format:
```json
{"id": "test1", "input": "your prompt here", "expected": {"reference": "expected answer"}}
```

**Example test file (save as `my_tests.jsonl`):**
```json
{"id": "math1", "input": "What is 2 + 2?", "expected": {"reference": "4"}}
{"id": "math2", "input": "What is 5 + 3?", "expected": {"reference": "8"}}
{"id": "greeting", "input": "Say hello", "expected": {"contains": ["hello", "hi"]}}
```

**What each part means:**
- **`id`** - A unique name for this test (like "math1", "greeting")
- **`input`** - What you want to send to your AI function  
- **`expected`** - What kind of response you want back

**Types of expected responses:**
- **`"reference": "exact answer"`** - AI must give exactly this answer
- **`"contains": ["word1", "word2"]`** - AI response must include these words
- **`"regex": "pattern"`** - For advanced users who know regular expressions

---

## 🚀 Quick Start - pytest for LLMs

### Step 1: Install
```bash
pip install vald8
```

### Step 2: Add @vald8 decorator to your LLM function
```python
# my_llm.py
import openai
from vald8 import vald8

@vald8(dataset="tests.jsonl")
def generate_response(prompt: str) -> dict:
    """Generate structured JSON response."""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return {"response": response.choices[0].message.content}
```

### Step 3: Create test dataset (`tests.jsonl`)
```json
{"id": "test1", "input": "Generate a greeting", "expected": {"schema": {"type": "object", "properties": {"response": {"type": "string"}}}}}
{"id": "test2", "input": "Say hello politely", "expected": {"contains": ["hello", "please"]}}
```

### Step 4: Run tests
```python
# Normal function usage
result = generate_response("Hello world")  # Works normally

# Run evaluation
results = generate_response.run_eval()
print(f"✅ Tests passed: {results['passed']}")
print(f"📊 Success rate: {results['summary']['success_rate']:.1%}")
```

### Step 5: Use in CI/CD
```yaml
# .github/workflows/test.yml
- name: Test LLM Functions
  run: |
    python -c "
    from my_llm import generate_response
    results = generate_response.run_eval()
    assert results['passed'], f'LLM tests failed: {results[\"run_dir\"]}'
    "
```

**That's it!** Your LLM functions are now tested like any other Python code.

---

## 📚 Testing Patterns

### Schema Validation (Most Common)
```python
@vald8(dataset="schema_tests.jsonl")
def extract_data(text: str) -> dict:
    """Extract structured data from text."""
    return llm_extract(text)

# schema_tests.jsonl
# {"id": "person", "input": "John Smith, age 30", "expected": {"schema": {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "number"}}, "required": ["name", "age"]}}}
```

### Multi-Input Functions
```python
@vald8(dataset="multi_input_tests.jsonl")
def chat_with_context(message: str, context: dict) -> str:
    """Chat function with context."""
    return llm_chat(message, context)

# multi_input_tests.jsonl  
# {"id": "context1", "input": {"message": "What's my name?", "context": {"user_name": "Alice"}}, "expected": {"contains": ["Alice"]}}
```

### CI Integration Examples
```python
# test_llm_functions.py (run with pytest)
def test_llm_schema_validation():
    """Test LLM function schema compliance."""
    results = extract_data.run_eval()
    assert results["passed"], f"Schema tests failed: {results['run_dir']}"
    
def test_llm_instruction_following():
    """Test LLM follows instructions correctly.""" 
    results = chat_with_context.run_eval()
    assert results["summary"]["metrics"]["instruction_adherence"]["mean"] >= 0.8
```

### GitHub Actions
```yaml
# .github/workflows/llm-tests.yml
name: LLM Function Tests
on: [push, pull_request]

jobs:
  test-llm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install vald8
          
      - name: Run LLM tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python -c "
          from my_llm import generate_response
          results = generate_response.run_eval()
          if not results['passed']:
              print('❌ LLM tests failed')
              exit(1)
          print('✅ LLM tests passed')
          "
```

---

## 🔧 Advanced Testing Workflows

### Test Organization & Best Practices

#### Grouping Tests by Functionality
```python
# Schema validation tests
@vald8(dataset="schema_tests.jsonl", tests=["schema_fidelity"])
def data_extractor(text: str) -> dict:
    return extract_structured_data(text)

# Instruction following tests  
@vald8(dataset="instruction_tests.jsonl", tests=["instruction_adherence"])
def task_executor(instruction: str) -> str:
    return execute_llm_task(instruction)

# Combined validation
@vald8(dataset="combined_tests.jsonl", tests=["schema_fidelity", "instruction_adherence"])
def complete_workflow(input_data: dict) -> dict:
    return process_complete_workflow(input_data)
```

#### A/B Testing Different Approaches
```python
# Compare different prompting strategies
@vald8(dataset="comparison_tests.jsonl")
def direct_prompting(query: str) -> str:
    return llm_call(f"Answer: {query}")

@vald8(dataset="comparison_tests.jsonl")  
def chain_of_thought(query: str) -> str:
    prompt = f"Think step by step:\n1. Understand: {query}\n2. Analyze:\n3. Answer:"
    return llm_call(prompt)

# Run comparison
results_direct = direct_prompting.run_eval()
results_cot = chain_of_thought.run_eval()

print(f"Direct: {results_direct['summary']['success_rate']:.1%}")
print(f"CoT: {results_cot['summary']['success_rate']:.1%}")
```

### Cost & Performance Optimization

#### Minimizing API Costs in CI
```python
# Use cheaper models for basic validation
@vald8(
    dataset="basic_tests.jsonl", 
    judge_provider="gpt-3.5-turbo",  # Cheaper for simple checks
    tests=["schema_fidelity"]  # No LLM judge needed
)
def cost_optimized_function(prompt: str) -> dict:
    return llm_call(prompt, model="gpt-3.5-turbo")

# Use sampling for large test suites
@vald8(dataset="large_tests.jsonl", sample_size=50)  # Test subset in CI
def performance_function(data: dict) -> dict:
    return expensive_llm_operation(data)
```

#### Caching for Faster CI Runs
```python
@vald8(
    dataset="regression_tests.jsonl",
    cache=True  # Cache results to speed up CI
)
def cached_function(input_data: str) -> str:
    return stable_llm_function(input_data)
```

### Regression Detection Patterns

#### Pre-commit Hooks
```python
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: vald8-tests
        name: LLM Function Tests
        entry: python -c "from my_llm import critical_function; assert critical_function.run_eval()['passed']"
        language: system
        pass_filenames: false
```

#### Critical Path Testing
```python
# test_critical_llm_functions.py
import pytest

def test_schema_validation_critical():
    """Critical path: ensure JSON schema compliance."""
    results = data_extractor.run_eval()
    assert results["passed"], "Schema validation failed - blocking deployment"
    
def test_safety_compliance():
    """Critical path: safety must be 100%."""
    results = content_generator.run_eval() 
    safety_score = results["summary"]["metrics"]["safety"]["mean"]
    assert safety_score == 1.0, f"Safety compliance failed: {safety_score}"

def test_instruction_following():
    """Critical path: instruction adherence above threshold."""
    results = task_executor.run_eval()
    instruction_score = results["summary"]["metrics"]["instruction_adherence"]["mean"]
    assert instruction_score >= 0.8, f"Instruction adherence too low: {instruction_score}"
```

---

## ⚙️ Configuration 

**Zero configuration required** - Vald8 works out of the box:

### Basic Usage
```python
@vald8(dataset="tests.jsonl")  # That's it!
def my_function(prompt: str) -> dict:
    return llm_call(prompt)
```

### Available Options
```python
@vald8(
    dataset="tests.jsonl",
    tests=["schema_fidelity"],             # What to validate  
    thresholds={"schema_fidelity": 1.0},   # Pass/fail criteria
    cache=True,                            # Speed up CI runs
    judge_provider="openai"                # For instruction adherence tests
)
def my_function(prompt: str) -> dict:
    return llm_call(prompt)
```

### Environment Variables
```bash
# API keys (only needed for LLM-as-judge features)
export OPENAI_API_KEY="sk-..."          # For OpenAI judge
export ANTHROPIC_API_KEY="sk-ant-..."   # For Claude judge

# Optional customization
export VALD8_CACHE_DIR=".vald8_cache"   # Cache location  
export VALD8_RESULTS_DIR="./test_runs"  # Results location
```

**Most teams only need schema validation - no API keys required!**

---

## 📊 Understanding Your Results

When Vald8 finishes testing, you get a simple summary:

```python
results = my_function.run_eval()

# Check if everything passed
if results["passed"]:
    print("✅ All good!")
else:
    print("❌ Some tests failed")

# See the overall score
accuracy = results["summary"]["metrics"]["accuracy"]["mean"]
print(f"Accuracy: {accuracy:.1%}")  # Shows like "85.0%"

# See detailed results
print(f"Results saved to: {results['run_dir']}")
```

### What the Numbers Mean

- **Accuracy Score**: 0.0 to 1.0 (where 1.0 = 100% correct)
- **Passed**: Did it meet your threshold? (True/False)
- **Total Examples**: How many tests were run
- **Success Rate**: Overall percentage that passed

### Where Results Are Saved

Vald8 creates a folder with all the details:
```
runs/
└── 2025-09-07_14-05-23_abc123/
    ├── results.jsonl      # Details for each test
    ├── summary.json       # Overall statistics  
    └── metadata.json      # Settings used
```

You can open these files to see exactly what happened with each test.

---

## 🧪 What Vald8 Can Test

**🎯 Accuracy** - "Did my AI give the right answer?"
- Exact matches: AI must say exactly "Paris" when asked for France's capital
- Contains words: AI must mention "hello" when greeting someone  
- Good for: Q&A, facts, specific information

**🛡️ Safety** - "Is my AI being appropriate?"
- Checks for harmful, offensive, or problematic content
- Good for: Public-facing chatbots, content generation

**📋 Instruction Following** - "Did my AI do what I asked?"
- Checks if AI followed your specific instructions
- Good for: Complex prompts, formatting requirements

**📊 Format Checking** - "Is the output structured correctly?"
- Validates JSON responses have the right fields
- Good for: APIs, structured data generation

### How to Use Them
```python
@vald8(
    dataset="my_tests.jsonl",
    tests=["accuracy", "safety"],           # Pick what you want to test
    thresholds={"accuracy": 0.8}            # Set minimum scores
)
```

---

## ❓ Common Questions

**Q: What if my test file has errors?**  
A: Vald8 will tell you exactly what's wrong and which line has the problem.

**Q: Can I test functions that need multiple inputs?**  
A: Yes! Just put them in your test file like this:
```json
{"id": "test1", "input": {"question": "Hi", "language": "en"}, "expected": {"contains": ["hello"]}}
```

**Q: Do I need OpenAI API keys?**  
A: Nope! Vald8 works fine for basic testing without any API keys. You only need them for advanced AI-powered judging.

**Q: Can I test functions that return JSON/objects?**  
A: Yes! Vald8 handles both text and structured data automatically.

**Q: What if my AI function sometimes fails?**  
A: Vald8 will catch errors and continue testing the other examples. You'll see which ones failed in the results.

---

## 🎯 When to Use Vald8

**✅ Schema Validation** - Ensure your LLM returns proper JSON structure  
**✅ Regression Testing** - Catch when changes break AI behavior  
**✅ CI/CD Integration** - Validate AI functions in deployment pipeline  
**✅ Prompt Comparison** - A/B test different prompting strategies  
**✅ Instruction Compliance** - Verify AI follows specific requirements  

## 🚀 Getting Started

```bash
pip install vald8
```

Add `@vald8(dataset="tests.jsonl")` to any LLM function and you're testing like pytest!

---

## 🤝 Open Source Community

**Contributing:**
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/vald8/issues)
- 💡 **Feature Ideas**: [GitHub Discussions](https://github.com/yourusername/vald8/discussions)  
- 🔧 **Pull Requests**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- 📖 **Documentation**: Help improve examples and guides

**Community:**
- ⭐ **Star on GitHub** if Vald8 helps your project
- 🐦 **Share your experience** on Twitter/LinkedIn  
- 💬 **Join discussions** in Python Discord servers
- 📝 **Write blog posts** about LLM testing patterns

---

## 📜 License

MIT License - Free and open source forever.

---

**Built by developers, for developers. pytest for the LLM age. 🚀**