"""
Simple Example - Command-line usage of LangChain Debugger
"""
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from debugger import DebugMode, debug_chain


def example_1_simple_usage():
    """Example 1: Simple chain debugging"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple Chain Debugging")
    print("="*60)
    
    # Note: You need to set your API key
    # os.environ["OPENAI_API_KEY"] = "your-key-here"
    
    try:
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        
        # Create a simple chain
        prompt = ChatPromptTemplate.from_template("Tell me a {length} joke about {topic}")
        chain = prompt | llm | StrOutputParser()
        
        # Debug the chain
        with DebugMode() as debugger:
            result = debugger.debug_chain(
                chain,
                inputs={"length": "short", "topic": "programming"}
            )
            
            print("\n📝 Chain Result:")
            print(result)
            
            debugger.print_report()
    
    except ImportError:
        print("❌ OpenAI package not installed. Run: pip install langchain-openai")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure to set your OPENAI_API_KEY environment variable")


def example_2_without_execution():
    """Example 2: Inspect chain structure without execution"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Chain Structure Inspection (No Execution)")
    print("="*60)
    
    try:
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-3.5-turbo")
        
        # Create a more complex chain
        prompt1 = ChatPromptTemplate.from_template("Summarize this in 3 words: {text}")
        prompt2 = ChatPromptTemplate.from_template("Explain this: {summary}")
        
        chain = (
            {"summary": prompt1 | llm | StrOutputParser()}
            | prompt2
            | llm
            | StrOutputParser()
        )
        
        # Inspect without execution
        debugger = DebugMode(verbose=True)
        debugger.debug_chain(chain)  # No inputs = no execution
        
        print("\n📊 Mermaid Diagram:")
        print(debugger.get_mermaid_diagram())
    
    except ImportError:
        print("❌ OpenAI package not installed. Run: pip install langchain-openai")


def example_3_quick_debug():
    """Example 3: Quick one-liner debugging"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Quick Debug (One-liner)")
    print("="*60)
    
    try:
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
        prompt = ChatPromptTemplate.from_template("What is {topic}?")
        chain = prompt | llm | StrOutputParser()
        
        # One-liner debug
        result = debug_chain(
            chain,
            inputs={"topic": "quantum computing"},
            verbose=True
        )
        
        print(f"\n📝 Result: {result}")
    
    except ImportError:
        print("❌ OpenAI package not installed. Run: pip install langchain-openai")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_4_groq_fast_inference():
    """Example 4: Using Groq for ultra-fast inference"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Groq Fast Inference")
    print("="*60)
    
    try:
        from langchain_groq import ChatGroq
        
        # Groq is much faster than OpenAI
        llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.7)
        
        prompt = ChatPromptTemplate.from_template("Explain {concept} in simple terms")
        chain = prompt | llm | StrOutputParser()
        
        with DebugMode() as debugger:
            result = debugger.debug_chain(
                chain,
                inputs={"concept": "neural networks"}
            )
            
            print(f"\n📝 Result: {result}")
            debugger.print_report()
            
            # Note the latency difference!
            print("\n⚡ Notice the latency - Groq is typically 5-10x faster than OpenAI!")
    
    except ImportError:
        print("❌ Groq package not installed. Run: pip install langchain-groq")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure to set your GROQ_API_KEY environment variable")


def example_5_cost_comparison():
    """Example 5: Compare costs across different models"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Cost Comparison Across Models")
    print("="*60)
    
    models_to_test = [
        ("gpt-3.5-turbo", "OpenAI GPT-3.5 Turbo"),
        ("gpt-4", "OpenAI GPT-4"),
    ]
    
    prompt = ChatPromptTemplate.from_template("Summarize: {text}")
    test_input = {
        "text": "Machine learning is a subset of artificial intelligence that focuses on "
                "training algorithms to learn from data and make predictions."
    }
    
    try:
        from langchain_openai import ChatOpenAI
        
        print("\nComparing costs for the same task across different models:\n")
        
        for model_name, description in models_to_test:
            print(f"\n--- Testing {description} ---")
            
            llm = ChatOpenAI(model=model_name, temperature=0)
            chain = prompt | llm | StrOutputParser()
            
            debugger = DebugMode(verbose=False)
            result = debugger.debug_chain(chain, test_input)
            
            if debugger.analysis:
                cost = debugger.analysis['cost']['total_cost']
                tokens = debugger.analysis['token_efficiency']['total_tokens']
                print(f"   Tokens: {tokens}")
                print(f"   Cost: ${cost:.6f}")
    
    except ImportError:
        print("❌ OpenAI package not installed. Run: pip install langchain-openai")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all examples"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🔍 LANGCHAIN DEBUGGER EXAMPLES 🔍               ║
║                                                              ║
║  Visual debugging and optimization tool for LangChain       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("\n📋 Available Examples:")
    print("1. Simple chain debugging")
    print("2. Chain structure inspection (no execution)")
    print("3. Quick debug (one-liner)")
    print("4. Groq fast inference")
    print("5. Cost comparison across models")
    print("\n0. Run all examples")
    
    choice = input("\nSelect an example (0-5): ").strip()
    
    examples = {
        "1": example_1_simple_usage,
        "2": example_2_without_execution,
        "3": example_3_quick_debug,
        "4": example_4_groq_fast_inference,
        "5": example_5_cost_comparison,
    }
    
    if choice == "0":
        for example_func in examples.values():
            try:
                example_func()
            except Exception as e:
                print(f"\n❌ Example failed: {e}")
    elif choice in examples:
        examples[choice]()
    else:
        print("Invalid choice!")
    
    print("\n" + "="*60)
    print("Done! 🎉")
    print("="*60)


if __name__ == "__main__":
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GROQ_API_KEY"):
        print("""
⚠️  WARNING: No API keys found!

Please set at least one of these environment variables:
- OPENAI_API_KEY (for OpenAI models)
- GROQ_API_KEY (for Groq models)
- ANTHROPIC_API_KEY (for Claude models)

Example:
    export OPENAI_API_KEY="your-key-here"
    
Or set them in Python:
    os.environ["OPENAI_API_KEY"] = "your-key-here"
        """)
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            exit(0)
    
    main()
