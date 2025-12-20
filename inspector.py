"""
Chain Inspector - Introspects LangChain chain structure
"""
import inspect
from typing import Any, Dict, List, Tuple
from langchain_core.runnables import Runnable, RunnableSequence, RunnableParallel


class ChainInspector:
    """Inspects and analyzes LangChain chain structure"""
    
    def __init__(self):
        self.nodes = []
        self.edges = []
        
    def inspect_chain(self, chain: Runnable) -> Dict[str, Any]:
        """
        Inspect a LangChain chain and extract its structure
        
        Args:
            chain: LangChain Runnable chain
            
        Returns:
            Dictionary containing chain structure information
        """
        self.nodes = []
        self.edges = []
        
        chain_info = {
            'type': self._get_chain_type(chain),
            'components': [],
            'graph': {'nodes': [], 'edges': []},
            'structure': 'unknown'
        }
        
        # Handle different chain types
        if isinstance(chain, RunnableSequence):
            chain_info['structure'] = 'sequence'
            chain_info['components'] = self._inspect_sequence(chain)
        elif isinstance(chain, RunnableParallel):
            chain_info['structure'] = 'parallel'
            chain_info['components'] = self._inspect_parallel(chain)
        else:
            # Single component
            chain_info['structure'] = 'single'
            chain_info['components'] = [self._get_component_info(chain, 0)]
        
        # Build graph representation
        chain_info['graph']['nodes'] = self.nodes
        chain_info['graph']['edges'] = self.edges
        
        return chain_info
    
    def _inspect_sequence(self, chain: RunnableSequence) -> List[Dict[str, Any]]:
        """Inspect a sequential chain"""
        components = []
        steps = chain.steps if hasattr(chain, 'steps') else []
        
        for idx, step in enumerate(steps):
            component_info = self._get_component_info(step, idx)
            components.append(component_info)
            
            # Add node
            self.nodes.append({
                'id': idx,
                'label': component_info['name'],
                'type': component_info['type']
            })
            
            # Add edge to next component
            if idx < len(steps) - 1:
                self.edges.append({
                    'from': idx,
                    'to': idx + 1
                })
        
        return components
    
    def _inspect_parallel(self, chain: RunnableParallel) -> List[Dict[str, Any]]:
        """Inspect a parallel chain"""
        components = []
        
        if hasattr(chain, 'steps'):
            for idx, (key, step) in enumerate(chain.steps.items()):
                component_info = self._get_component_info(step, idx)
                component_info['parallel_key'] = key
                components.append(component_info)
                
                # Add node
                self.nodes.append({
                    'id': idx,
                    'label': f"{key}: {component_info['name']}",
                    'type': component_info['type']
                })
        
        return components
    
    def _get_component_info(self, component: Any, index: int) -> Dict[str, Any]:
        """Extract information about a single component"""
        component_type = type(component).__name__
        module_name = type(component).__module__
        
        info = {
            'index': index,
            'name': component_type,
            'type': self._categorize_component(component_type, module_name),
            'module': module_name,
            'config': {}
        }
        
        # Extract configuration if available
        if hasattr(component, 'model_name'):
            info['config']['model'] = component.model_name
        elif hasattr(component, 'model'):
            info['config']['model'] = component.model
            
        if hasattr(component, 'temperature'):
            info['config']['temperature'] = component.temperature
            
        if hasattr(component, 'max_tokens'):
            info['config']['max_tokens'] = component.max_tokens
        
        return info
    
    def _categorize_component(self, component_type: str, module_name: str) -> str:
        """Categorize component into high-level types"""
        if 'prompt' in component_type.lower() or 'template' in component_type.lower():
            return 'prompt'
        elif 'llm' in component_type.lower() or 'chat' in component_type.lower() or 'openai' in module_name.lower() or 'anthropic' in module_name.lower():
            return 'llm'
        elif 'parser' in component_type.lower() or 'output' in component_type.lower():
            return 'parser'
        elif 'retriever' in component_type.lower():
            return 'retriever'
        elif 'memory' in component_type.lower():
            return 'memory'
        elif 'tool' in component_type.lower():
            return 'tool'
        else:
            return 'other'
    
    def _get_chain_type(self, chain: Runnable) -> str:
        """Get the type of the chain"""
        return type(chain).__name__
    
    def print_structure(self, chain_info: Dict[str, Any]) -> None:
        """Print chain structure in a readable format"""
        print("=== Chain Structure ===")
        print(f"Type: {chain_info['type']}")
        print(f"Structure: {chain_info['structure']}")
        print(f"\nComponents ({len(chain_info['components'])}):")
        
        for component in chain_info['components']:
            print(f"  {component['index'] + 1}. {component['name']} ({component['type']})")
            if component['config']:
                for key, value in component['config'].items():
                    print(f"     - {key}: {value}")
