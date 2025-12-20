"""
Demo Chains - Example LangChain chains for testing the debugger
"""
import os
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel


def get_simple_chain(llm):
    """
    Create a simple sequential chain: Prompt -> LLM -> Parser
    
    Args:
        llm: Language model to use
        
    Returns:
        Runnable chain
    """
    prompt = ChatPromptTemplate.from_template(
        "Tell me a {length} joke about {topic}"
    )
    
    chain = prompt | llm | StrOutputParser()
    
    return chain


def get_complex_chain(llm):
    """
    Create a more complex chain with multiple steps
    
    Args:
        llm: Language model to use
        
    Returns:
        Runnable chain
    """
    # First prompt - generate a story outline
    outline_prompt = ChatPromptTemplate.from_template(
        "Create a 3-sentence story outline about {topic}"
    )
    
    # Second prompt - expand the outline
    expand_prompt = ChatPromptTemplate.from_template(
        "Expand this story outline into a full story:\n\n{outline}"
    )
    
    # Chain them together
    chain = (
        {"outline": outline_prompt | llm | StrOutputParser()}
        | expand_prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


def get_parallel_chain(llm):
    """
    Create a chain with parallel execution
    
    Args:
        llm: Language model to use
        
    Returns:
        Runnable chain
    """
    # Multiple prompts running in parallel
    joke_prompt = ChatPromptTemplate.from_template("Tell a joke about {topic}")
    fact_prompt = ChatPromptTemplate.from_template("Tell an interesting fact about {topic}")
    question_prompt = ChatPromptTemplate.from_template("Ask a thought-provoking question about {topic}")
    
    chain = RunnableParallel(
        joke=joke_prompt | llm | StrOutputParser(),
        fact=fact_prompt | llm | StrOutputParser(),
        question=question_prompt | llm | StrOutputParser()
    )
    
    return chain


def get_json_output_chain(llm):
    """
    Create a chain that outputs JSON
    
    Args:
        llm: Language model to use
        
    Returns:
        Runnable chain
    """
    prompt = ChatPromptTemplate.from_template(
        """Generate a JSON object with the following information about {topic}:
        - name: the name
        - description: a brief description
        - fun_fact: an interesting fact
        
        Return only valid JSON, no other text.
        """
    )
    
    chain = prompt | llm | JsonOutputParser()
    
    return chain


def get_multi_step_analysis_chain(llm):
    """
    Create a multi-step analysis chain
    
    Args:
        llm: Language model to use
        
    Returns:
        Runnable chain
    """
    # Step 1: Extract key points
    extract_prompt = ChatPromptTemplate.from_template(
        "Extract 3 key points from this text:\n\n{text}"
    )
    
    # Step 2: Analyze sentiment
    sentiment_prompt = ChatPromptTemplate.from_template(
        "Analyze the sentiment of these key points:\n\n{points}"
    )
    
    # Step 3: Generate summary
    summary_prompt = ChatPromptTemplate.from_template(
        "Create a brief summary based on this sentiment analysis:\n\n{sentiment}"
    )
    
    chain = (
        {"points": extract_prompt | llm | StrOutputParser()}
        | {"sentiment": sentiment_prompt | llm | StrOutputParser()}
        | summary_prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


# Example usage instructions
def print_examples():
    """Print example usage"""
    print("""
=== Example Usage ===

1. Simple Chain:
    from langchain_openai import ChatOpenAI
    from examples.demo_chains import get_simple_chain
    from debugger import DebugMode
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    chain = get_simple_chain(llm)
    
    with DebugMode() as debugger:
        result = debugger.debug_chain(
            chain,
            inputs={"length": "short", "topic": "programming"}
        )
        debugger.print_report()

2. Complex Chain:
    chain = get_complex_chain(llm)
    with DebugMode() as debugger:
        result = debugger.debug_chain(
            chain,
            inputs={"topic": "space exploration"}
        )
        debugger.print_report()

3. Parallel Chain:
    chain = get_parallel_chain(llm)
    with DebugMode() as debugger:
        result = debugger.debug_chain(
            chain,
            inputs={"topic": "artificial intelligence"}
        )
        debugger.print_report()

4. Quick Debug (one-liner):
    from debugger import debug_chain
    result = debug_chain(chain, inputs={"topic": "AI"})
    """)


if __name__ == "__main__":
    print_examples()
