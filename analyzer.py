"""
Chain Analyzer - Analyzes performance and provides optimization suggestions
"""
from typing import Dict, List, Any
import statistics


class ChainAnalyzer:
    """Analyzes chain performance and provides optimization recommendations"""
    
    def __init__(self):
        self.suggestions = []
        
    def analyze(self, chain_info: Dict[str, Any], monitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze chain performance and generate suggestions
        
        Args:
            chain_info: Chain structure information
            monitor_data: Runtime monitoring data
            
        Returns:
            Analysis results with suggestions
        """
        self.suggestions = []
        
        analysis = {
            'performance': self._analyze_performance(monitor_data),
            'cost': self._analyze_cost(chain_info, monitor_data),
            'token_efficiency': self._analyze_tokens(monitor_data),
            'suggestions': []
        }
        
        # Generate suggestions
        self._suggest_model_optimization(chain_info, monitor_data)
        self._suggest_prompt_optimization(monitor_data)
        self._suggest_cost_optimization(monitor_data)
        self._suggest_latency_optimization(monitor_data)
        
        analysis['suggestions'] = self.suggestions
        
        return analysis
    
    def _analyze_performance(self, monitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance metrics"""
        total_latency = monitor_data.get('total_latency', 0)
        llm_calls = monitor_data.get('llm_calls', 0)
        
        return {
            'total_latency': round(total_latency, 2),
            'llm_calls': llm_calls,
            'avg_latency_per_call': round(total_latency / llm_calls, 2) if llm_calls > 0 else 0
        }
    
    def _analyze_cost(self, chain_info: Dict[str, Any], monitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze cost metrics"""
        total_cost = monitor_data.get('total_cost', 0)
        
        return {
            'total_cost': round(total_cost, 6),
            'cost_per_call': round(total_cost / max(monitor_data.get('llm_calls', 1), 1), 6),
            'estimated_1k_calls': round(total_cost * 1000, 2),
            'estimated_monthly': round(total_cost * 30000, 2)  # ~1k calls/day
        }
    
    def _analyze_tokens(self, monitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze token usage efficiency"""
        token_usage = monitor_data.get('token_usage', {})
        
        prompt_tokens = token_usage.get('prompt_tokens', 0)
        completion_tokens = token_usage.get('completion_tokens', 0)
        total_tokens = token_usage.get('total_tokens', 0)
        
        return {
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
            'total_tokens': total_tokens,
            'prompt_to_completion_ratio': round(prompt_tokens / max(completion_tokens, 1), 2),
            'efficiency_score': self._calculate_efficiency_score(prompt_tokens, completion_tokens)
        }
    
    def _calculate_efficiency_score(self, prompt_tokens: int, completion_tokens: int) -> str:
        """Calculate efficiency score based on token usage"""
        if prompt_tokens == 0:
            return 'N/A'
        
        ratio = prompt_tokens / max(completion_tokens, 1)
        
        if ratio < 2:
            return 'Excellent'
        elif ratio < 5:
            return 'Good'
        elif ratio < 10:
            return 'Fair'
        else:
            return 'Poor - Consider prompt optimization'
    
    def _suggest_model_optimization(self, chain_info: Dict[str, Any], monitor_data: Dict[str, Any]):
        """Suggest model optimizations"""
        components = chain_info.get('components', [])
        
        for component in components:
            if component['type'] == 'llm':
                model = component.get('config', {}).get('model', '')
                
                if 'gpt-4' in model.lower() and 'turbo' not in model.lower():
                    self.suggestions.append({
                        'type': 'model',
                        'priority': 'high',
                        'message': f'💡 Consider using GPT-4 Turbo instead of {model} for 67% cost savings',
                        'potential_savings': '67%'
                    })
                
                if 'gpt-3.5-turbo' in model.lower():
                    tokens = monitor_data.get('token_usage', {}).get('total_tokens', 0)
                    if tokens < 500:
                        self.suggestions.append({
                            'type': 'model',
                            'priority': 'medium',
                            'message': f'💡 For simple tasks, consider using gpt-3.5-turbo-instruct for faster responses',
                            'potential_savings': '10-20% latency reduction'
                        })
                
                # Suggest Groq for speed
                if 'claude' not in model.lower():
                    self.suggestions.append({
                        'type': 'model',
                        'priority': 'low',
                        'message': '⚡ For ultra-fast inference, consider Groq API (llama-3 models) - 10x faster',
                        'potential_savings': '90% latency reduction'
                    })
    
    def _suggest_prompt_optimization(self, monitor_data: Dict[str, Any]):
        """Suggest prompt optimizations"""
        prompt_tokens = monitor_data.get('token_usage', {}).get('prompt_tokens', 0)
        
        if prompt_tokens > 1000:
            self.suggestions.append({
                'type': 'prompt',
                'priority': 'high',
                'message': f'📝 Prompt is {prompt_tokens} tokens - consider summarizing or using RAG for context',
                'potential_savings': f'{int((prompt_tokens - 500) / prompt_tokens * 100)}% token reduction'
            })
        elif prompt_tokens > 500:
            self.suggestions.append({
                'type': 'prompt',
                'priority': 'medium',
                'message': f'📝 Prompt is {prompt_tokens} tokens - review for unnecessary content',
                'potential_savings': f'{int((prompt_tokens - 300) / prompt_tokens * 100)}% token reduction'
            })
        elif prompt_tokens < 100:
            self.suggestions.append({
                'type': 'prompt',
                'priority': 'low',
                'message': f'✅ Prompt length ({prompt_tokens} tokens) is well optimized!',
                'potential_savings': 'None needed'
            })
    
    def _suggest_cost_optimization(self, monitor_data: Dict[str, Any]):
        """Suggest cost optimizations"""
        total_cost = monitor_data.get('total_cost', 0)
        
        if total_cost > 0.01:  # More than 1 cent per call
            self.suggestions.append({
                'type': 'cost',
                'priority': 'high',
                'message': f'💰 High cost per call (${total_cost:.4f}) - consider cheaper models or caching',
                'potential_savings': '50-90%'
            })
        
        # Suggest caching
        self.suggestions.append({
            'type': 'cost',
            'priority': 'medium',
            'message': '🗄️ Implement prompt caching for repeated queries to reduce costs by 50-90%',
            'potential_savings': '50-90%'
        })
    
    def _suggest_latency_optimization(self, monitor_data: Dict[str, Any]):
        """Suggest latency optimizations"""
        total_latency = monitor_data.get('total_latency', 0)
        llm_calls = monitor_data.get('llm_calls', 1)
        
        if total_latency > 3.0:
            self.suggestions.append({
                'type': 'latency',
                'priority': 'high',
                'message': f'⏱️ Total latency is {total_latency:.2f}s - consider streaming responses or parallel execution',
                'potential_savings': '30-50% latency reduction'
            })
        
        if llm_calls > 3:
            self.suggestions.append({
                'type': 'latency',
                'priority': 'medium',
                'message': f'🔄 Chain makes {llm_calls} LLM calls - consider combining prompts or using agents',
                'potential_savings': f'{int((llm_calls - 1) / llm_calls * 100)}% call reduction'
            })
    
    def print_analysis(self, analysis: Dict[str, Any]):
        """Print analysis in a readable format"""
        print("\n=== Performance Analysis ===")
        perf = analysis['performance']
        print(f"Total Latency: {perf['total_latency']}s")
        print(f"LLM Calls: {perf['llm_calls']}")
        print(f"Avg Latency/Call: {perf['avg_latency_per_call']}s")
        
        print("\n=== Cost Analysis ===")
        cost = analysis['cost']
        print(f"Total Cost: ${cost['total_cost']:.6f}")
        print(f"Cost per Call: ${cost['cost_per_call']:.6f}")
        print(f"Est. 1K calls: ${cost['estimated_1k_calls']:.2f}")
        print(f"Est. Monthly (30K): ${cost['estimated_monthly']:.2f}")
        
        print("\n=== Token Efficiency ===")
        tokens = analysis['token_efficiency']
        print(f"Prompt Tokens: {tokens['prompt_tokens']}")
        print(f"Completion Tokens: {tokens['completion_tokens']}")
        print(f"Total Tokens: {tokens['total_tokens']}")
        print(f"Efficiency Score: {tokens['efficiency_score']}")
        
        print("\n=== Optimization Suggestions ===")
        if analysis['suggestions']:
            # Sort by priority
            priority_order = {'high': 0, 'medium': 1, 'low': 2}
            sorted_suggestions = sorted(
                analysis['suggestions'],
                key=lambda x: priority_order.get(x['priority'], 3)
            )
            
            for idx, suggestion in enumerate(sorted_suggestions, 1):
                priority_emoji = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }
                emoji = priority_emoji.get(suggestion['priority'], '⚪')
                print(f"{idx}. {emoji} {suggestion['message']}")
                if suggestion.get('potential_savings'):
                    print(f"   → Potential savings: {suggestion['potential_savings']}")
        else:
            print("No suggestions - chain is well optimized!")
