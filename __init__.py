"""
Debug Mode - Main interface for LangChain debugging
"""
from typing import Any, Optional
from langchain_core.runnables import Runnable
from .inspector import ChainInspector
from .monitor import ChainMonitor
from .analyzer import ChainAnalyzer
from .visualizer import ChainVisualizer


class DebugMode:
    """
    Context manager for debugging LangChain chains
    
    Usage:
        with DebugMode() as debugger:
            chain = prompt | llm | parser
            result = chain.invoke({"input": "..."})
            debugger.print_report()
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize debug mode
        
        Args:
            verbose: Whether to print detailed information
        """
        self.verbose = verbose
        self.inspector = ChainInspector()
        self.monitor = ChainMonitor()
        self.analyzer = ChainAnalyzer()
        self.visualizer = ChainVisualizer()
        
        self.chain_info = None
        self.analysis = None
        self.current_chain = None
        
    def __enter__(self):
        """Enter debug context"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit debug context"""
        if exc_type is not None:
            print(f"Error during chain execution: {exc_val}")
        return False
    
    def debug_chain(self, chain: Runnable, inputs: Any = None) -> Any:
        """
        Debug a chain with optional execution
        
        Args:
            chain: LangChain Runnable to debug
            inputs: Optional inputs to execute the chain with
            
        Returns:
            Chain output if inputs provided, else None
        """
        self.current_chain = chain
        
        # Inspect chain structure
        self.chain_info = self.inspector.inspect_chain(chain)
        
        if self.verbose:
            self.inspector.print_structure(self.chain_info)
        
        # Execute chain if inputs provided
        result = None
        if inputs is not None:
            result = chain.invoke(inputs, config={"callbacks": [self.monitor]})
            
            # Analyze results
            monitor_summary = self.monitor.get_summary()
            self.analysis = self.analyzer.analyze(self.chain_info, monitor_summary)
        
        return result
    
    def print_report(self, include_visualization: bool = True):
        """
        Print complete debug report
        
        Args:
            include_visualization: Whether to include ASCII visualization
        """
        print("\n" + "=" * 60)
        print(" " * 15 + "LANGCHAIN DEBUG REPORT")
        print("=" * 60)
        
        if self.chain_info:
            self.inspector.print_structure(self.chain_info)
            
            if include_visualization:
                self.visualizer.print_visualization(self.chain_info)
        
        if self.analysis:
            self.analyzer.print_analysis(self.analysis)
        else:
            print("\n⚠️  No execution data available. Run chain with inputs to see analysis.")
        
        print("\n" + "=" * 60)
    
    def get_mermaid_diagram(self) -> str:
        """
        Get Mermaid diagram syntax
        
        Returns:
            Mermaid diagram string
        """
        if self.chain_info:
            return self.visualizer.generate_mermaid(self.chain_info)
        return ""
    
    def get_plotly_figure(self):
        """
        Get Plotly figure for visualization
        
        Returns:
            Plotly Figure object
        """
        if self.chain_info:
            monitor_summary = self.monitor.get_summary() if self.analysis else None
            return self.visualizer.generate_plotly_figure(self.chain_info, monitor_summary)
        return None
    
    def get_summary(self) -> dict:
        """
        Get summary of debug session
        
        Returns:
            Dictionary with debug summary
        """
        summary = {
            'chain_structure': self.chain_info,
            'performance': None,
            'analysis': None
        }
        
        if self.analysis:
            summary['performance'] = self.monitor.get_summary()
            summary['analysis'] = self.analysis
        
        return summary
    
    def reset(self):
        """Reset debug state"""
        self.monitor.reset()
        self.chain_info = None
        self.analysis = None
        self.current_chain = None


# Convenience function
def debug_chain(chain: Runnable, inputs: Any = None, verbose: bool = True) -> Any:
    """
    Quick debug function for one-off debugging
    
    Args:
        chain: LangChain Runnable to debug
        inputs: Optional inputs to execute the chain with
        verbose: Whether to print detailed information
        
    Returns:
        Chain output if inputs provided, else None
    """
    debugger = DebugMode(verbose=verbose)
    result = debugger.debug_chain(chain, inputs)
    debugger.print_report()
    return result
