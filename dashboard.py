"""
Gradio Dashboard - Interactive UI for LangChain Debugger
"""
import gradio as gr
import os
from typing import Optional, Tuple
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from debugger import DebugMode
from examples.demo_chains import (
    get_simple_chain,
    get_complex_chain,
    get_parallel_chain,
    get_json_output_chain,
    get_multi_step_analysis_chain
)


class DashboardState:
    """Holds state for the dashboard"""
    def __init__(self):
        self.debugger = None
        self.llm = None
        self.chain = None
        self.last_result = None


state = DashboardState()


def initialize_llm(provider: str, model: str, api_key: str, temperature: float) -> str:
    """Initialize the LLM based on provider"""
    try:
        if not api_key:
            return "❌ Please provide an API key"
        
        os.environ[f"{provider.upper()}_API_KEY"] = api_key
        
        if provider == "openai":
            from langchain_openai import ChatOpenAI
            state.llm = ChatOpenAI(model=model, temperature=temperature)
        elif provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            state.llm = ChatAnthropic(model=model, temperature=temperature)
        elif provider == "groq":
            from langchain_groq import ChatGroq
            state.llm = ChatGroq(model=model, temperature=temperature)
        else:
            return f"❌ Unsupported provider: {provider}"
        
        return f"✅ {provider.upper()} LLM initialized with model: {model}"
    
    except Exception as e:
        return f"❌ Error initializing LLM: {str(e)}"


def create_chain(chain_type: str) -> str:
    """Create a chain based on the selected type"""
    try:
        if state.llm is None:
            return "❌ Please initialize an LLM first"
        
        chain_builders = {
            "Simple Chain": get_simple_chain,
            "Complex Chain": get_complex_chain,
            "Parallel Chain": get_parallel_chain,
            "JSON Output Chain": get_json_output_chain,
            "Multi-Step Analysis": get_multi_step_analysis_chain
        }
        
        if chain_type not in chain_builders:
            return f"❌ Unknown chain type: {chain_type}"
        
        state.chain = chain_builders[chain_type](state.llm)
        return f"✅ {chain_type} created successfully"
    
    except Exception as e:
        return f"❌ Error creating chain: {str(e)}"


def debug_and_run(inputs_json: str) -> Tuple[str, str, str, Optional[object]]:
    """Debug the chain and run it with inputs"""
    try:
        if state.chain is None:
            return "❌ Please create a chain first", "", "", None
        
        # Parse inputs
        import json
        try:
            inputs = json.loads(inputs_json)
        except json.JSONDecodeError:
            return "❌ Invalid JSON input", "", "", None
        
        # Create debugger
        state.debugger = DebugMode(verbose=False)
        
        # Debug and run chain
        result = state.debugger.debug_chain(state.chain, inputs)
        state.last_result = result
        
        # Get outputs
        chain_structure = get_chain_structure()
        performance_report = get_performance_report()
        analysis_report = get_analysis_report()
        
        # Get visualization
        fig = state.debugger.get_plotly_figure()
        
        return chain_structure, performance_report, analysis_report, fig
    
    except Exception as e:
        return f"❌ Error: {str(e)}", "", "", None


def get_chain_structure() -> str:
    """Get chain structure as text"""
    if state.debugger is None or state.debugger.chain_info is None:
        return "No chain structure available"
    
    chain_info = state.debugger.chain_info
    
    output = "=== CHAIN STRUCTURE ===\n\n"
    output += f"Type: {chain_info['type']}\n"
    output += f"Structure: {chain_info['structure']}\n\n"
    output += f"Components ({len(chain_info['components'])}):\n"
    
    for component in chain_info['components']:
        output += f"\n  {component['index'] + 1}. {component['name']} ({component['type']})\n"
        if component['config']:
            for key, value in component['config'].items():
                output += f"     • {key}: {value}\n"
    
    return output


def get_performance_report() -> str:
    """Get performance metrics as text"""
    if state.debugger is None or state.debugger.analysis is None:
        return "No performance data available"
    
    analysis = state.debugger.analysis
    
    output = "=== PERFORMANCE METRICS ===\n\n"
    
    perf = analysis['performance']
    output += f"Total Latency: {perf['total_latency']}s\n"
    output += f"LLM Calls: {perf['llm_calls']}\n"
    output += f"Avg Latency/Call: {perf['avg_latency_per_call']}s\n\n"
    
    cost = analysis['cost']
    output += "=== COST ANALYSIS ===\n\n"
    output += f"Total Cost: ${cost['total_cost']:.6f}\n"
    output += f"Cost per Call: ${cost['cost_per_call']:.6f}\n"
    output += f"Est. 1K calls: ${cost['estimated_1k_calls']:.2f}\n"
    output += f"Est. Monthly (30K): ${cost['estimated_monthly']:.2f}\n\n"
    
    tokens = analysis['token_efficiency']
    output += "=== TOKEN USAGE ===\n\n"
    output += f"Prompt Tokens: {tokens['prompt_tokens']}\n"
    output += f"Completion Tokens: {tokens['completion_tokens']}\n"
    output += f"Total Tokens: {tokens['total_tokens']}\n"
    output += f"Efficiency Score: {tokens['efficiency_score']}\n"
    
    return output


def get_analysis_report() -> str:
    """Get optimization suggestions as text"""
    if state.debugger is None or state.debugger.analysis is None:
        return "No analysis available"
    
    analysis = state.debugger.analysis
    
    output = "=== OPTIMIZATION SUGGESTIONS ===\n\n"
    
    if analysis['suggestions']:
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_suggestions = sorted(
            analysis['suggestions'],
            key=lambda x: priority_order.get(x['priority'], 3)
        )
        
        priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
        
        for idx, suggestion in enumerate(sorted_suggestions, 1):
            emoji = priority_emoji.get(suggestion['priority'], '⚪')
            output += f"{idx}. {emoji} {suggestion['message']}\n"
            if suggestion.get('potential_savings'):
                output += f"   → Potential savings: {suggestion['potential_savings']}\n"
            output += "\n"
    else:
        output += "No suggestions - chain is well optimized!"
    
    return output


def get_mermaid_diagram() -> str:
    """Get Mermaid diagram syntax"""
    if state.debugger is None or state.debugger.chain_info is None:
        return "No diagram available"
    
    return state.debugger.get_mermaid_diagram()


# Create Gradio interface
def create_dashboard():
    """Create the Gradio dashboard"""
    
    with gr.Blocks(title="🔍 LangChain Debugger", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🔍 LangChain Debugger
        
        Visual debugging and optimization tool for LangChain applications.
        Monitor, analyze, and optimize your LLM chains in real-time.
        """)
        
        with gr.Tab("⚙️ Setup"):
            gr.Markdown("### 1. Initialize LLM")
            
            with gr.Row():
                provider = gr.Dropdown(
                    choices=["openai", "anthropic", "groq"],
                    label="LLM Provider",
                    value="openai"
                )
                model = gr.Dropdown(
                    choices=[
                        "gpt-3.5-turbo",
                        "gpt-4",
                        "gpt-4-turbo",
                        "claude-3-haiku-20240307",
                        "claude-3-sonnet-20240229",
                        "llama-3.1-70b-versatile",
                        "mixtral-8x7b-32768"
                    ],
                    label="Model",
                    value="gpt-3.5-turbo"
                )
            
            with gr.Row():
                api_key = gr.Textbox(
                    label="API Key",
                    type="password",
                    placeholder="Enter your API key"
                )
                temperature = gr.Slider(
                    minimum=0.0,
                    maximum=2.0,
                    value=0.7,
                    step=0.1,
                    label="Temperature"
                )
            
            init_btn = gr.Button("Initialize LLM", variant="primary")
            init_output = gr.Textbox(label="Status", interactive=False)
            
            init_btn.click(
                fn=initialize_llm,
                inputs=[provider, model, api_key, temperature],
                outputs=init_output
            )
            
            gr.Markdown("### 2. Select Chain Type")
            
            chain_type = gr.Dropdown(
                choices=[
                    "Simple Chain",
                    "Complex Chain",
                    "Parallel Chain",
                    "JSON Output Chain",
                    "Multi-Step Analysis"
                ],
                label="Chain Type",
                value="Simple Chain"
            )
            
            create_btn = gr.Button("Create Chain", variant="primary")
            create_output = gr.Textbox(label="Status", interactive=False)
            
            create_btn.click(
                fn=create_chain,
                inputs=chain_type,
                outputs=create_output
            )
        
        with gr.Tab("🚀 Debug & Run"):
            gr.Markdown("### Execute Chain with Inputs")
            
            inputs_json = gr.Textbox(
                label="Chain Inputs (JSON)",
                placeholder='{"topic": "AI", "length": "short"}',
                value='{"topic": "artificial intelligence", "length": "short"}',
                lines=3
            )
            
            run_btn = gr.Button("Debug & Run Chain", variant="primary")
            
            with gr.Row():
                with gr.Column():
                    structure_output = gr.Textbox(
                        label="Chain Structure",
                        lines=15,
                        interactive=False
                    )
                
                with gr.Column():
                    performance_output = gr.Textbox(
                        label="Performance Metrics",
                        lines=15,
                        interactive=False
                    )
            
            analysis_output = gr.Textbox(
                label="Optimization Suggestions",
                lines=10,
                interactive=False
            )
            
            run_btn.click(
                fn=debug_and_run,
                inputs=inputs_json,
                outputs=[structure_output, performance_output, analysis_output]
            )
        
        with gr.Tab("📊 Visualization"):
            gr.Markdown("### Chain Flow Diagram")
            
            viz_btn = gr.Button("Generate Visualization", variant="primary")
            
            with gr.Row():
                mermaid_output = gr.Textbox(
                    label="Mermaid Diagram (copy to mermaid.live)",
                    lines=15,
                    interactive=False
                )
            
            viz_btn.click(
                fn=get_mermaid_diagram,
                outputs=mermaid_output
            )
            
            gr.Markdown("""
            **Tip:** Copy the Mermaid diagram above and paste it into [mermaid.live](https://mermaid.live) 
            for interactive visualization!
            """)
        
        with gr.Tab("📖 Examples"):
            gr.Markdown("""
            ## Example Inputs for Different Chain Types
            
            ### Simple Chain
            ```json
            {"topic": "programming", "length": "short"}
            ```
            
            ### Complex Chain
            ```json
            {"topic": "space exploration"}
            ```
            
            ### Parallel Chain
            ```json
            {"topic": "artificial intelligence"}
            ```
            
            ### JSON Output Chain
            ```json
            {"topic": "Python"}
            ```
            
            ### Multi-Step Analysis
            ```json
            {"text": "Artificial intelligence is transforming industries worldwide. From healthcare to finance, AI systems are improving efficiency and accuracy. However, ethical considerations remain important."}
            ```
            
            ## Features
            
            - **Chain Visualization**: See your chain structure as a flow diagram
            - **Performance Monitoring**: Track token usage, latency, and costs
            - **Cost Analysis**: Understand costs per call and monthly estimates
            - **Optimization Suggestions**: Get actionable recommendations
            - **Multiple LLM Providers**: Support for OpenAI, Anthropic, and Groq
            """)
    
    return demo


if __name__ == "__main__":
    demo = create_dashboard()
    demo.launch(share=False)
