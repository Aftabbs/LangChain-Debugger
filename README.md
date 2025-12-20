# 🔍 LangChain-Debugger

<img width="428" height="260" alt="image" src="https://github.com/user-attachments/assets/5c275341-6d49-4ab8-9220-92a16a8ee826" />


**Visual debugging and optimization tool for LangChain applications**

Monitor, analyze, and optimize your LLM chains in real-time with detailed performance metrics, cost breakdowns, and actionable optimization suggestions.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/langchain-0.1+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
 
---
 
## 🌟 Features

### 📊 Chain Visualization
- Auto-generate flow diagrams from LangChain code
- Mermaid diagram export for documentation
- Interactive Plotly visualizations
- ASCII diagrams for command-line use

### 📈 Real-time Monitoring
- Track token usage per component
- Measure latency at each step
- Monitor LLM API calls
- Capture complete execution flow

### 💰 Cost Analysis
- Cost breakdown per LLM call
- Estimated costs for 1K, 10K calls
- Monthly cost projections
- Model comparison recommendations

### 🎯 Performance Optimization
- Identify bottlenecks in your chain
- Get actionable suggestions to reduce costs
- Token efficiency scoring
- Model alternatives with savings estimates

### 🛠️ Easy Integration
```python
from debugger import DebugMode

with DebugMode() as debugger:
    result = chain.invoke({"input": "..."})
    debugger.print_report()
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/aftabbs/langchain-debugger.git
cd langchain-debugger

# Install dependencies
pip install -r requirements.txt

# Set your API key
export OPENAI_API_KEY="your-key-here"
# or GROQ_API_KEY, ANTHROPIC_API_KEY
```

### Basic Usage

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from debugger import DebugMode

# Create your chain
llm = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | llm | StrOutputParser()

# Debug it!
with DebugMode() as debugger:
    result = debugger.debug_chain(
        chain,
        inputs={"topic": "programming"}
    )
    debugger.print_report()
```

### Output Example

```
============================================================
               LANGCHAIN DEBUG REPORT
============================================================

=== Chain Structure ===
Type: RunnableSequence
Structure: sequence

Components (3):
  1. ChatPromptTemplate (prompt)
  2. ChatOpenAI (llm)
     • model: gpt-3.5-turbo
     • temperature: 0.7
  3. StrOutputParser (parser)

=== Performance Analysis ===
Total Latency: 1.23s
LLM Calls: 1
Avg Latency/Call: 1.23s

=== Cost Analysis ===
Total Cost: $0.000300
Cost per Call: $0.000300
Est. 1K calls: $0.30
Est. Monthly (30K): $9.00

=== Token Efficiency ===
Prompt Tokens: 45
Completion Tokens: 105
Total Tokens: 150
Efficiency Score: Good

=== Optimization Suggestions ===
1. 🟢 ✅ Prompt length (45 tokens) is well optimized!
2. 🟡 🗄️ Implement prompt caching for repeated queries
   → Potential savings: 50-90%
3. 🟢 ⚡ For ultra-fast inference, consider Groq API
   → Potential savings: 90% latency reduction
============================================================
```

---

## 📖 Usage Examples

### Example 1: Quick Debug (One-liner)

```python
from debugger import debug_chain

result = debug_chain(chain, inputs={"topic": "AI"})
```

### Example 2: Inspect Chain Without Execution

```python
debugger = DebugMode(verbose=True)
debugger.debug_chain(chain)  # No inputs = structure only
print(debugger.get_mermaid_diagram())
```

### Example 3: Compare Model Costs

```python
models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]

for model_name in models:
    llm = ChatOpenAI(model=model_name)
    chain = prompt | llm | StrOutputParser()
    
    debugger = DebugMode(verbose=False)
    debugger.debug_chain(chain, inputs={"topic": "AI"})
    
    cost = debugger.analysis['cost']['total_cost']
    print(f"{model_name}: ${cost:.6f}")
```

### Example 4: Export Mermaid Diagram

```python
with DebugMode() as debugger:
    debugger.debug_chain(chain)
    
    # Get Mermaid syntax
    mermaid = debugger.get_mermaid_diagram()
    
    # Save to file
    with open("chain_diagram.mmd", "w") as f:
        f.write(mermaid)
    
    # Open in mermaid.live for visualization
```

---

## 🖥️ Interactive Dashboard

Launch the Gradio web interface for visual debugging:

```bash
python ui/dashboard.py
```

Then open http://localhost:7860 in your browser.

**Dashboard Features:**
- 🎛️ Configure multiple LLM providers (OpenAI, Anthropic, Groq)
- 🧪 Test different chain types
- 📊 Real-time performance visualization
- 💡 Interactive optimization suggestions
- 📈 Cost comparison tools

---

## 📁 Project Structure

```
langchain-debugger/
├── debugger/
│   ├── __init__.py          # Main DebugMode interface
│   ├── inspector.py         # Chain structure introspection
│   ├── monitor.py           # Runtime execution monitoring
│   ├── analyzer.py          # Performance analysis
│   └── visualizer.py        # Diagram generation
├── ui/
│   └── dashboard.py         # Gradio web interface
├── examples/
│   ├── demo_chains.py       # Example chain builders
│   └── cli_examples.py      # Command-line examples
├── requirements.txt
└── README.md
```

---

## 🔧 Supported Features

### Chain Types
- ✅ Sequential chains (RunnableSequence)
- ✅ Parallel chains (RunnableParallel)
- ✅ Single component chains
- ✅ Multi-step chains
- ✅ Nested chains

### LLM Providers
- ✅ OpenAI (GPT-3.5, GPT-4)
- ✅ Anthropic (Claude)
- ✅ Groq (Llama, Mixtral)
- ✅ Any LangChain-compatible LLM

### Output Formats
- ✅ Console text report
- ✅ ASCII diagrams
- ✅ Mermaid diagrams
- ✅ Plotly interactive graphs
- ✅ JSON export

---

## 💡 Use Cases

### 1. Development & Debugging
- Understand complex chain structures
- Identify which components are slow
- Debug unexpected behavior

### 2. Cost Optimization
- Find expensive LLM calls
- Compare model pricing
- Optimize token usage

### 3. Performance Tuning
- Identify latency bottlenecks
- Test parallel vs sequential execution
- Benchmark different models

### 4. Documentation
- Generate visual chain diagrams
- Export architecture documentation
- Share chain designs with team

---

## 🎯 Optimization Suggestions Examples

The debugger provides intelligent suggestions:

**High Priority:**
- 💰 "High cost per call ($0.05) - consider cheaper models or caching"
- ⏱️ "Total latency is 5.2s - consider streaming or parallel execution"
- 📝 "Prompt is 1500 tokens - consider summarizing or using RAG"

**Medium Priority:**
- 💡 "Consider using GPT-4 Turbo instead of GPT-4 for 67% cost savings"
- 🔄 "Chain makes 5 LLM calls - consider combining prompts"

**Low Priority:**
- ⚡ "For ultra-fast inference, consider Groq API - 10x faster"
- ✅ "Prompt length (45 tokens) is well optimized!"

---

## 🤝 Contributing

Contributions are welcome! This tool is built for the LangChain community.

**Ways to contribute:**
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests

---

## 📝 Requirements

- Python 3.8+
- LangChain 0.1.0+
- Gradio 4.0+ (for UI)
- Plotly 5.18+ (for visualizations)

See `requirements.txt` for full list.

---

## 🎓 Examples & Tutorials

### Run CLI Examples

```bash
python examples/cli_examples.py
```

This provides 5 interactive examples:
1. Simple chain debugging
2. Chain structure inspection
3. Quick debug (one-liner)
4. Groq fast inference comparison
5. Cost comparison across models

### Import Demo Chains

```python
from examples.demo_chains import (
    get_simple_chain,
    get_complex_chain,
    get_parallel_chain,
    get_json_output_chain,
    get_multi_step_analysis_chain
)

# Use any demo chain
chain = get_simple_chain(llm)
```

---

## 🚦 Getting Started Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Set API key: `export OPENAI_API_KEY="..."`
- [ ] Run basic example: `python examples/cli_examples.py`
- [ ] Try web dashboard: `python ui/dashboard.py`
- [ ] Debug your own chain
- [ ] Optimize based on suggestions

---

## 🔒 Privacy & Security

- **No data storage**: All debugging happens locally
- **API keys**: Never logged or stored
- **Chain data**: Only in memory during execution
- **Open source**: Review the code yourself

---

## 📄 License

MIT License - see LICENSE file for details.

---

## ⭐ Star History

If you find this tool useful, please consider giving it a star! ⭐

---

**Made with 🔍 by the LangChain community**
