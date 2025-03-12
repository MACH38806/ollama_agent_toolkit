"""Example implementation of a research agent."""

import json
import requests
from typing import List, Dict, Any, Optional
from agent import Agent
from tools import Tool, STANDARD_TOOLS


def search_google(query: str) -> str:
    """Mock Google search function.
    
    Args:
        query: The search query.
        
    Returns:
        Search results as a string.
    """
    # In a real implementation, integrate with the Google Search API
    return f"Mock Google search results for: {query}\n\n1. Result 1 description\n2. Result 2 description\n3. Result 3 description"


def search_academic_papers(query: str) -> str:
    """Search for academic papers on a topic.
    
    Args:
        query: The search query.
        
    Returns:
        List of academic papers as a string.
    """
    # In a real implementation, integrate with arXiv, Google Scholar, or similar API
    return f"Mock academic paper results for: {query}\n\n1. Paper Title 1 (2023) - Authors et al.\n2. Paper Title 2 (2022) - Authors et al.\n3. Paper Title 3 (2024) - Authors et al."


def summarize_text(text: str, max_length: int = 200) -> str:
    """Summarize the given text.
    
    Args:
        text: The text to summarize.
        max_length: Maximum length of the summary.
        
    Returns:
        A summary of the text.
    """
    # In a real implementation, this would use Ollama for the summarization
    # Here we just return a mock summary
    return f"Mock summary of the text (max {max_length} chars): {text[:100]}..."


class ResearchAgent(Agent):
    """An agent specialized for research tasks."""
    
    def __init__(self, model: str = "llama3", verbose: bool = False):
        """Initialize the research agent.
        
        Args:
            model: The name of the model to use.
            verbose: Whether to print verbose output.
        """
        # Define research-specific tools
        research_tools = STANDARD_TOOLS + [
            Tool("google_search", "Search Google for information", search_google),
            Tool("academic_search", "Search for academic papers", search_academic_papers),
            Tool("summarize", "Summarize a piece of text", summarize_text),
        ]
        
        # Define research-specific system prompt
        research_prompt = """You are a research assistant that helps users find and process information.
        Your goal is to provide accurate, well-sourced information on any topic.
        
        When answering research questions, follow these steps:
        1. Search for relevant information using the provided tools
        2. Analyze and synthesize the information
        3. Present findings in a clear, organized manner
        4. Cite sources appropriately
        5. Acknowledge limitations or gaps in the available information
        
        Use the tool that best fits the research need:
        - For general information, use google_search
        - For academic sources, use academic_search
        - For condensing information, use summarize
        
        Present information objectively and distinguish between facts and opinions.
        """
        
        # Initialize the base agent with research configuration
        super().__init__(
            model=model,
            system_prompt=research_prompt,
            tools=research_tools,
            verbose=verbose
        )


# Example usage
if __name__ == "__main__":
    # Create a research agent
    agent = ResearchAgent(model="llama3", verbose=True)
    
    # Test with a research query
    response = agent.process_user_input("What are the latest developments in quantum computing?")
    print(f"\nResearch Agent response: {response}")
    
    # Test with a request to summarize
    text_to_summarize = """Quantum computing is a rapidly evolving field that leverages the principles of quantum mechanics to process information. Unlike classical computers that use bits (0s and 1s), quantum computers use quantum bits or qubits that can exist in multiple states simultaneously through superposition. This allows quantum computers to explore many possible solutions to a problem at once, potentially offering exponential speedups for certain types of calculations."""
    response = agent.process_user_input(f"Can you summarize this text about quantum computing: {text_to_summarize}")
    print(f"\nResearch Agent response: {response}")
