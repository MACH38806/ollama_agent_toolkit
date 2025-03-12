"""Example implementation of a coding assistant agent."""

import json
import re
from typing import List, Dict, Any, Optional
from agent import Agent
from tools import Tool, STANDARD_TOOLS


def search_documentation(topic: str, language: str = "python") -> str:
    """Search documentation for a programming topic.
    
    Args:
        topic: The topic to search for.
        language: The programming language.
        
    Returns:
        Documentation results as a string.
    """
    # In a real implementation, integrate with documentation APIs or web scraping
    return f"Mock documentation for {topic} in {language}:\n\nFunction signature: example_function(param1, param2)\nDescription: This function does something related to {topic}\nExample usage: example_code_here"


def run_code(code: str, language: str = "python") -> str:
    """Run code and return the output.
    
    Args:
        code: The code to run.
        language: The programming language.
        
    Returns:
        The output of running the code.
    """
    # In a real implementation, this would use a sandboxed environment to execute code
    # Here we just return a mock response
    return f"Mock output from running {language} code:\n\nExecution successful\nOutput: [Expected output would appear here]"


def fix_bugs(code: str, error_message: str, language: str = "python") -> str:
    """Attempt to fix bugs in code based on error messages.
    
    Args:
        code: The code with bugs.
        error_message: The error message.
        language: The programming language.
        
    Returns:
        Fixed code or suggestions.
    """
    # In a real implementation, this would analyze the code and error
    # Here we just return a mock response
    return f"Mock bug fix suggestion for {language} code:\n\nThe error '{error_message}' might be caused by [reason].\nHere's a potential fix:\n\n```{language}\n# Fixed version of code\n```"


class CodingAgent(Agent):
    """An agent specialized for programming and coding assistance."""
    
    def __init__(self, model: str = "codellama", verbose: bool = False):
        """Initialize the coding agent.
        
        Args:
            model: The name of the model to use (preferably code-specialized).
            verbose: Whether to print verbose output.
        """
        # Define coding-specific tools
        coding_tools = STANDARD_TOOLS + [
            Tool("docs", "Search programming documentation", search_documentation),
            Tool("run", "Run code and get output", run_code),
            Tool("fix", "Fix bugs in code", fix_bugs),
        ]
        
        # Define coding-specific system prompt
        coding_prompt = """You are a coding assistant that helps users write, debug, and understand code.
        Your goal is to provide clear, efficient, and well-documented code solutions.
        
        When helping with coding tasks, follow these best practices:
        1. Understand the user's requirements before writing code
        2. Write clean, readable, and efficient code
        3. Include appropriate comments and documentation
        4. Explain your code's logic and design decisions
        5. Follow language-specific conventions and best practices
        
        Use the tool that best fits the coding need:
        - For language/library documentation, use docs
        - For testing code execution, use run
        - For debugging and fixing errors, use fix
        
        When showing code, use appropriate syntax highlighting and formatting.
        """
        
        # Initialize the base agent with coding configuration
        super().__init__(
            model=model,
            system_prompt=coding_prompt,
            tools=coding_tools,
            verbose=verbose
        )
    
    def process_code_review(self, code: str, language: str = "python") -> str:
        """Perform a code review and provide suggestions.
        
        Args:
            code: The code to review.
            language: The programming language.
            
        Returns:
            Code review feedback.
        """
        prompt = f"Please review this {language} code and provide suggestions for improvement:\n\n```{language}\n{code}\n```"
        return self.process_user_input(prompt)
    
    def generate_unit_tests(self, code: str, language: str = "python") -> str:
        """Generate unit tests for the given code.
        
        Args:
            code: The code to generate tests for.
            language: The programming language.
            
        Returns:
            Generated unit tests.
        """
        prompt = f"Please generate comprehensive unit tests for this {language} code:\n\n```{language}\n{code}\n```"
        return self.process_user_input(prompt)


# Example usage
if __name__ == "__main__":
    # Create a coding agent
    agent = CodingAgent(model="codellama", verbose=True)
    
    # Test with a coding question
    response = agent.process_user_input("How do I read a CSV file in Python?")
    print(f"\nCoding Agent response: {response}")
    
    # Test with a bug fixing request
    buggy_code = """def calculate_average(numbers):
    total = 0
    for num in numbers
        total += num
    return total / len(numbers)

nums = [1, 2, 3, 4, 5]
print(calculate_average(nums))"""
    
    error_message = "SyntaxError: invalid syntax at line 3"
    
    response = agent.process_user_input(f"Can you fix this Python code?\n\n```python\n{buggy_code}\n```\n\nI'm getting this error: {error_message}")
    print(f"\nCoding Agent response: {response}")
