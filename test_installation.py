"""
Test Script - Verify LangChain Debugger Installation
"""
import sys
import importlib 
  

def check_package(package_name):
    """Check if a package is installed"""
    try:
        importlib.import_module(package_name)
        return True, "✅"
    except ImportError:
        return False, "❌"


def test_installation():
    """Test if all required packages are installed"""
    print("="*60)
    print("LangChain Debugger - Installation Test")
    print("="*60)
    
    required_packages = [
        ("langchain", "LangChain"),
        ("langchain_core", "LangChain Core"),
        ("gradio", "Gradio (for UI)"),
        ("plotly", "Plotly (for visualizations)"),
        ("networkx", "NetworkX (for graphs)"),
        ("tiktoken", "TikTok (for token counting)"),
    ]
    
    optional_packages = [
        ("langchain_openai", "OpenAI Integration"),
        ("langchain_anthropic", "Anthropic Integration"),
        ("langchain_groq", "Groq Integration"),
    ]
    
    print("\n📦 Required Packages:")
    all_required_ok = True
    for package, name in required_packages:
        installed, status = check_package(package)
        print(f"  {status} {name}")
        if not installed:
            all_required_ok = False
    
    print("\n📦 Optional Packages (at least one needed):")
    any_optional_ok = False
    for package, name in optional_packages:
        installed, status = check_package(package)
        print(f"  {status} {name}")
        if installed:
            any_optional_ok = True
    
    print("\n🔧 Debugger Modules:")
    debugger_modules = [
        ("debugger.inspector", "Chain Inspector"),
        ("debugger.monitor", "Chain Monitor"),
        ("debugger.analyzer", "Performance Analyzer"),
        ("debugger.visualizer", "Visualizer"),
    ]
    
    all_modules_ok = True
    for module, name in debugger_modules:
        installed, status = check_package(module)
        print(f"  {status} {name}")
        if not installed:
            all_modules_ok = False
    
    print("\n" + "="*60)
    
    if all_required_ok and any_optional_ok and all_modules_ok:
        print("✅ All checks passed! You're ready to use LangChain Debugger!")
        print("\n🚀 Next steps:")
        print("   1. Set your API key: export OPENAI_API_KEY='...'")
        print("   2. Run examples: python examples/cli_examples.py")
        print("   3. Launch dashboard: python ui/dashboard.py")
        return True
    else:
        print("❌ Some dependencies are missing!")
        print("\n🔧 To fix:")
        print("   pip install -r requirements.txt")
        
        if not any_optional_ok:
            print("\n📝 Also install at least one LLM provider:")
            print("   pip install langchain-openai  # For OpenAI")
            print("   pip install langchain-groq    # For Groq (free & fast!)")
            print("   pip install langchain-anthropic  # For Claude")
        
        return False


def test_basic_functionality():
    """Test basic debugger functionality"""
    print("\n" + "="*60)
    print("Testing Basic Functionality")
    print("="*60)
    
    try:
        from debugger import DebugMode
        print("✅ DebugMode imported successfully")
        
        from debugger.inspector import ChainInspector
        print("✅ ChainInspector imported successfully")
        
        from debugger.monitor import ChainMonitor
        print("✅ ChainMonitor imported successfully")
        
        from debugger.analyzer import ChainAnalyzer
        print("✅ ChainAnalyzer imported successfully")
        
        from debugger.visualizer import ChainVisualizer
        print("✅ ChainVisualizer imported successfully")
        
        print("\n✅ All core modules working!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing functionality: {e}")
        return False


def main():
    """Run all tests"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║         🔍 LangChain Debugger - Installation Test       ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Test installation
    install_ok = test_installation()
    
    # Test functionality if installation is OK
    if install_ok:
        func_ok = test_basic_functionality()
        
        if func_ok:
            print("\n" + "="*60)
            print("🎉 Everything is working perfectly!")
            print("="*60)
            print("\n📚 Quick Start:")
            print("   See QUICKSTART.md for a 5-minute tutorial")
            print("\n📖 Full Documentation:")
            print("   See README.md for complete documentation")
    else:
        print("\n⚠️  Please install missing dependencies first.")


if __name__ == "__main__":
    main()
