"""
Chain Visualizer - Creates visual representations of chains
"""
import networkx as nx
from typing import Dict, Any, List
import plotly.graph_objects as go


class ChainVisualizer:
    """Creates visual diagrams of LangChain chains"""
    
    def __init__(self):
        self.graph = None
        
    def create_graph(self, chain_info: Dict[str, Any]) -> nx.DiGraph:
        """
        Create NetworkX graph from chain info
        
        Args:
            chain_info: Chain structure information
            
        Returns:
            NetworkX directed graph
        """
        G = nx.DiGraph()
        
        nodes = chain_info['graph']['nodes']
        edges = chain_info['graph']['edges']
        
        # Add nodes
        for node in nodes:
            G.add_node(
                node['id'],
                label=node['label'],
                type=node['type']
            )
        
        # Add edges
        for edge in edges:
            G.add_edge(edge['from'], edge['to'])
        
        self.graph = G
        return G
    
    def generate_mermaid(self, chain_info: Dict[str, Any]) -> str:
        """
        Generate Mermaid diagram syntax
        
        Args:
            chain_info: Chain structure information
            
        Returns:
            Mermaid diagram as string
        """
        lines = ["graph LR"]
        
        nodes = chain_info['graph']['nodes']
        edges = chain_info['graph']['edges']
        
        # Define node styles based on type
        style_map = {
            'prompt': '([{label}])',
            'llm': '[{label}]',
            'parser': '>{label}]',
            'retriever': '({label})',
            'other': '[{label}]'
        }
        
        # Add nodes
        for node in nodes:
            node_id = f"N{node['id']}"
            label = node['label']
            node_type = node.get('type', 'other')
            style = style_map.get(node_type, '[{label}]')
            lines.append(f"    {node_id}{style.format(label=label)}")
        
        # Add edges
        for edge in edges:
            from_id = f"N{edge['from']}"
            to_id = f"N{edge['to']}"
            lines.append(f"    {from_id} --> {to_id}")
        
        # Add styling
        lines.append("    classDef promptClass fill:#e1f5ff,stroke:#01579b,stroke-width:2px")
        lines.append("    classDef llmClass fill:#fff3e0,stroke:#e65100,stroke-width:2px")
        lines.append("    classDef parserClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px")
        
        for node in nodes:
            node_id = f"N{node['id']}"
            node_type = node.get('type', 'other')
            if node_type == 'prompt':
                lines.append(f"    class {node_id} promptClass")
            elif node_type == 'llm':
                lines.append(f"    class {node_id} llmClass")
            elif node_type == 'parser':
                lines.append(f"    class {node_id} parserClass")
        
        return '\n'.join(lines)
    
    def generate_plotly_figure(self, chain_info: Dict[str, Any], monitor_data: Dict[str, Any] = None) -> go.Figure:
        """
        Generate interactive Plotly visualization
        
        Args:
            chain_info: Chain structure information
            monitor_data: Optional runtime monitoring data
            
        Returns:
            Plotly Figure object
        """
        G = self.create_graph(chain_info)
        
        # Create layout
        pos = self._create_layout(G)
        
        # Create edge traces
        edge_trace = self._create_edge_trace(G, pos)
        
        # Create node traces
        node_trace = self._create_node_trace(G, pos, chain_info, monitor_data)
        
        # Create figure
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title='LangChain Execution Flow',
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='white'
            )
        )
        
        return fig
    
    def _create_layout(self, G: nx.DiGraph) -> Dict[int, tuple]:
        """Create layout positions for nodes"""
        # Use hierarchical layout for sequential chains
        if nx.is_directed_acyclic_graph(G):
            # Topological sort for y-axis
            layers = list(nx.topological_generations(G))
            pos = {}
            
            for i, layer in enumerate(layers):
                for j, node in enumerate(layer):
                    pos[node] = (j * 2, -i * 2)
        else:
            # Fallback to spring layout
            pos = nx.spring_layout(G)
            # Scale positions
            pos = {k: (v[0] * 10, v[1] * 10) for k, v in pos.items()}
        
        return pos
    
    def _create_edge_trace(self, G: nx.DiGraph, pos: Dict[int, tuple]) -> go.Scatter:
        """Create Plotly trace for edges"""
        edge_x = []
        edge_y = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        )
        
        return edge_trace
    
    def _create_node_trace(
        self,
        G: nx.DiGraph,
        pos: Dict[int, tuple],
        chain_info: Dict[str, Any],
        monitor_data: Dict[str, Any] = None
    ) -> go.Scatter:
        """Create Plotly trace for nodes"""
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        
        # Color mapping for node types
        color_map = {
            'prompt': '#2196F3',
            'llm': '#FF9800',
            'parser': '#9C27B0',
            'retriever': '#4CAF50',
            'other': '#757575'
        }
        
        for node_id in G.nodes():
            x, y = pos[node_id]
            node_x.append(x)
            node_y.append(y)
            
            # Get node info
            node_data = G.nodes[node_id]
            label = node_data.get('label', f'Node {node_id}')
            node_type = node_data.get('type', 'other')
            
            # Create hover text
            hover_text = f"<b>{label}</b><br>Type: {node_type}"
            
            # Add monitoring data if available
            if monitor_data and 'events' in monitor_data:
                # This is simplified - you'd want to match events to specific nodes
                hover_text += f"<br>Status: Completed"
            
            node_text.append(hover_text)
            node_color.append(color_map.get(node_type, color_map['other']))
        
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[G.nodes[node]['label'] for node in G.nodes()],
            textposition="bottom center",
            hovertext=node_text,
            marker=dict(
                color=node_color,
                size=30,
                line=dict(width=2, color='white')
            ),
            showlegend=False
        )
        
        return node_trace
    
    def generate_ascii_diagram(self, chain_info: Dict[str, Any]) -> str:
        """
        Generate simple ASCII representation of the chain
        
        Args:
            chain_info: Chain structure information
            
        Returns:
            ASCII diagram as string
        """
        components = chain_info.get('components', [])
        
        lines = []
        lines.append("┌" + "─" * 50 + "┐")
        
        for idx, component in enumerate(components):
            name = component['name']
            comp_type = component['type']
            
            # Add component box
            lines.append("│ " + " " * 48 + " │")
            lines.append(f"│  [{idx + 1}] {name} ({comp_type})" + " " * (48 - len(name) - len(comp_type) - 8) + "│")
            
            # Add config if available
            if component.get('config'):
                for key, value in component['config'].items():
                    config_text = f"     • {key}: {value}"
                    lines.append("│ " + config_text + " " * (48 - len(config_text)) + " │")
            
            lines.append("│ " + " " * 48 + " │")
            
            # Add arrow to next component
            if idx < len(components) - 1:
                lines.append("│" + " " * 24 + "↓" + " " * 25 + "│")
        
        lines.append("└" + "─" * 50 + "┘")
        
        return '\n'.join(lines)
    
    def print_visualization(self, chain_info: Dict[str, Any]):
        """Print ASCII visualization"""
        print("\n=== Chain Visualization ===")
        print(self.generate_ascii_diagram(chain_info))
