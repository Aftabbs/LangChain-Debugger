# 🚀 Quick Start Guide

Get started with LangChain Debugger in 5 minutes!

## Step 1: Installation (1 minute)

```bash
# Clone the repository 
git clone https://github.com/yourusername/langchain-debugger.git
cd langchain-debugger

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Set API Key (30 seconds)

Choose ONE of these methods:

### Method A: Environment Variable
```bash
export OPENAI_API_KEY="sk-..."
```

### Method B: .env File
```bash
cp .env.example .env
# Edit .env and add your API key
```

### Method C: In Python
```python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."
```

## Step 3: Run Your First Debug (1 minute)

### Option A: Command Line Examples

```bash
python examples/cli_examples.py
```

Select example 1 for a simple demonstration.

### Option B: Quick Python Script

Create `test.py`:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from debugger import debug_chain

# Create chain
llm = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
chain = prompt | llm | StrOutputParser()

# Debug it!
result = debug_chain(chain, inputs={"topic": "Python"})
```

Run it:
```bash
python test.py
```

### Option C: Interactive Dashboard

```bash
python ui/dashboard.py
```

Then:
1. Open http://localhost:7860
2. Enter your API key
3. Click "Initialize LLM"
4. Click "Create Chain"
5. Click "Debug & Run Chain"

## What You'll See

```
============================================================
               LANGCHAIN DEBUG REPORT
============================================================

=== Chain Structure ===
Type: RunnableSequence
Components (3):
  1. ChatPromptTemplate (prompt)
  2. ChatOpenAI (llm)
  3. StrOutputParser (parser)

=== Performance Analysis ===
Total Latency: 1.23s
Total Tokens: 150
Total Cost: $0.000300

=== Optimization Suggestions ===
1. ✅ Prompt is well optimized!
2. 💡 Consider Groq for 10x faster inference
3. 🗄️ Implement caching for 50-90% savings
============================================================
```

## Next Steps

1. **Try Different Chains**: Check `examples/demo_chains.py`
2. **Explore Dashboard**: Test various chain types
3. **Debug Your Own Chains**: Replace the example with your code
4. **Read Full Docs**: See README.md for advanced features

## Common Issues

### "No module named 'langchain'"
```bash
pip install langchain langchain-core langchain-openai
```

### "API key not found"
Make sure you've set the environment variable:
```bash
echo $OPENAI_API_KEY  # Should show your key
```

### "Import error"
Make sure you're in the project directory:
```bash
cd langchain-debugger
python examples/cli_examples.py
```

## Alternative: Use Groq (Free & Fast)

Groq offers free API access with ultra-fast inference:

1. Get free API key: https://console.groq.com/
2. Set it: `export GROQ_API_KEY="gsk-..."`
3. Use in code:
```python
from langchain_groq import ChatGroq
llm = ChatGroq(model="llama-3.1-70b-versatile")
```

Groq is often 5-10x faster than OpenAI!

## Support

- 📖 **Full Documentation**: See README.md
- 🐛 **Issues**: GitHub Issues
- 💬 **Questions**: GitHub Discussions

---

**You're ready to start debugging! 🎉**
