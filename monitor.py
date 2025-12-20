"""
Chain Monitor - Monitors runtime execution of chains
"""
import time
from typing import Any, Dict, List, Optional
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
import tiktoken


class ChainMonitor(BaseCallbackHandler):
    """Callback handler to monitor chain execution"""
    
    def __init__(self):
        self.events = []
        self.llm_calls = []
        self.current_chain_start = None
        self.token_usage = {
            'prompt_tokens': 0,
            'completion_tokens': 0,
            'total_tokens': 0
        }
        self.total_cost = 0.0
        self.start_time = None
        self.end_time = None
        
    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs) -> None:
        """Track chain start"""
        if self.start_time is None:
            self.start_time = time.time()
        
        self.events.append({
            'type': 'chain_start',
            'timestamp': time.time(),
            'data': {
                'name': serialized.get('name', 'unknown'),
                'inputs': inputs
            }
        })
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        """Track chain end"""
        self.end_time = time.time()
        
        self.events.append({
            'type': 'chain_end',
            'timestamp': time.time(),
            'data': {
                'outputs': outputs
            }
        })
    
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs) -> None:
        """Track LLM call start"""
        self.events.append({
            'type': 'llm_start',
            'timestamp': time.time(),
            'data': {
                'model': serialized.get('name', 'unknown'),
                'prompts': prompts,
                'num_prompts': len(prompts)
            }
        })
        
        # Store for matching with end
        self.llm_calls.append({
            'start_time': time.time(),
            'prompts': prompts,
            'model': serialized.get('name', 'unknown')
        })
    
    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """Track LLM call end and calculate tokens/cost"""
        end_time = time.time()
        
        # Get matching start
        if self.llm_calls:
            llm_call = self.llm_calls[-1]
            latency = end_time - llm_call['start_time']
            
            # Extract token usage if available
            if response.llm_output and 'token_usage' in response.llm_output:
                usage = response.llm_output['token_usage']
                self.token_usage['prompt_tokens'] += usage.get('prompt_tokens', 0)
                self.token_usage['completion_tokens'] += usage.get('completion_tokens', 0)
                self.token_usage['total_tokens'] += usage.get('total_tokens', 0)
                
                # Calculate cost (approximate)
                model_name = llm_call.get('model', 'gpt-3.5-turbo')
                cost = self._calculate_cost(
                    model_name,
                    usage.get('prompt_tokens', 0),
                    usage.get('completion_tokens', 0)
                )
                self.total_cost += cost
            else:
                # Estimate tokens if not provided
                prompt_text = ' '.join(llm_call.get('prompts', []))
                response_text = str(response.generations[0][0].text if response.generations else '')
                
                prompt_tokens = self._estimate_tokens(prompt_text)
                completion_tokens = self._estimate_tokens(response_text)
                
                self.token_usage['prompt_tokens'] += prompt_tokens
                self.token_usage['completion_tokens'] += completion_tokens
                self.token_usage['total_tokens'] += prompt_tokens + completion_tokens
                
                model_name = llm_call.get('model', 'gpt-3.5-turbo')
                cost = self._calculate_cost(model_name, prompt_tokens, completion_tokens)
                self.total_cost += cost
            
            self.events.append({
                'type': 'llm_end',
                'timestamp': end_time,
                'data': {
                    'latency': latency,
                    'tokens': self.token_usage.copy(),
                    'cost': self.total_cost
                }
            })
    
    def on_llm_error(self, error: Exception, **kwargs) -> None:
        """Track LLM errors"""
        self.events.append({
            'type': 'llm_error',
            'timestamp': time.time(),
            'data': {
                'error': str(error)
            }
        })
    
    def _estimate_tokens(self, text: str, model: str = "gpt-3.5-turbo") -> int:
        """Estimate token count for text"""
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except:
            # Fallback: rough estimate (1 token ≈ 4 characters)
            return len(text) // 4
    
    def _calculate_cost(self, model_name: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost based on model and token usage"""
        # Pricing per 1K tokens (as of 2024)
        pricing = {
            'gpt-4': {'prompt': 0.03, 'completion': 0.06},
            'gpt-4-turbo': {'prompt': 0.01, 'completion': 0.03},
            'gpt-3.5-turbo': {'prompt': 0.0005, 'completion': 0.0015},
            'gpt-3.5-turbo-instruct': {'prompt': 0.0015, 'completion': 0.002},
            'claude-3-opus': {'prompt': 0.015, 'completion': 0.075},
            'claude-3-sonnet': {'prompt': 0.003, 'completion': 0.015},
            'claude-3-haiku': {'prompt': 0.00025, 'completion': 0.00125},
            'claude-sonnet-4': {'prompt': 0.003, 'completion': 0.015},
        }
        
        # Find matching pricing
        model_pricing = None
        for key in pricing.keys():
            if key in model_name.lower():
                model_pricing = pricing[key]
                break
        
        if not model_pricing:
            # Default to GPT-3.5 pricing
            model_pricing = pricing['gpt-3.5-turbo']
        
        prompt_cost = (prompt_tokens / 1000) * model_pricing['prompt']
        completion_cost = (completion_tokens / 1000) * model_pricing['completion']
        
        return prompt_cost + completion_cost
    
    def get_total_latency(self) -> float:
        """Get total execution time"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    def get_summary(self) -> Dict[str, Any]:
        """Get execution summary"""
        return {
            'total_latency': self.get_total_latency(),
            'token_usage': self.token_usage.copy(),
            'total_cost': self.total_cost,
            'events': len(self.events),
            'llm_calls': len([e for e in self.events if e['type'] == 'llm_end'])
        }
    
    def reset(self):
        """Reset monitor state"""
        self.events = []
        self.llm_calls = []
        self.current_chain_start = None
        self.token_usage = {
            'prompt_tokens': 0,
            'completion_tokens': 0,
            'total_tokens': 0
        }
        self.total_cost = 0.0
        self.start_time = None
        self.end_time = None
