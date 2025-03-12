"""A collection of tools that can be used by the agent."""

import json
import requests
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
import pytz
import os


class Tool:
    """Base class for agent tools."""
    
    def __init__(self, name: str, description: str, func: Callable):
        """Initialize a tool.
        
        Args:
            name: The name of the tool.
            description: A description of what the tool does.
            func: The function to call when the tool is used.
        """
        self.name = name
        self.description = description
        self.func = func
        
    def __call__(self, *args, **kwargs) -> str:
        """Call the tool with the given arguments."""
        return self.func(*args, **kwargs)


def search_web(query: str) -> str:
    """Search the web for information.
    
    Args:
        query: The search query.
        
    Returns:
        A string containing search results.
    """
    # This is a mock implementation. In a real application, you would
    # integrate with a search API like Google, Bing, or DuckDuckGo.
    return f"Mock search results for: {query}\n1. First result\n2. Second result\n3. Third result"


def get_weather(location: str) -> str:
    """Get the current weather for a location.
    
    Args:
        location: The location to get weather for.
        
    Returns:
        A string describing the weather.
    """
    # This is a mock implementation. In a real application, you would
    # integrate with a weather API like OpenWeatherMap or WeatherAPI.
    return f"Mock weather for {location}: 72°F, Partly Cloudy"


def get_current_time(timezone: str = "UTC") -> str:
    """Get the current time in the specified timezone.
    
    Args:
        timezone: The timezone to get the time for (default: UTC).
        
    Returns:
        A string with the current time.
    """
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        return f"Current time in {timezone}: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except pytz.exceptions.UnknownTimeZoneError:
        return f"Unknown timezone: {timezone}. Please use a valid timezone name."


def write_to_file(content: str, filename: str) -> str:
    """Write content to a file.
    
    Args:
        content: The content to write.
        filename: The name of the file to write to.
        
    Returns:
        A message indicating success or failure.
    """
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"Successfully wrote content to {filename}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"


def read_from_file(filename: str) -> str:
    """Read content from a file.
    
    Args:
        filename: The name of the file to read from.
        
    Returns:
        The content of the file or an error message.
    """
    try:
        if not os.path.exists(filename):
            return f"File not found: {filename}"
        
        with open(filename, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def calculate(expression: str) -> str:
    """Evaluate a mathematical expression.
    
    Args:
        expression: The expression to evaluate.
        
    Returns:
        The result of the evaluation or an error message.
    """
    try:
        # Warning: eval can be dangerous if used with untrusted input
        # In a production environment, use a safer evaluation method
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating expression: {str(e)}"


# Define standard tools
STANDARD_TOOLS = [
    Tool("search", "Search the web for information", search_web),
    Tool("weather", "Get the current weather for a location", get_weather),
    Tool("time", "Get the current time in a specific timezone", get_current_time),
    Tool("write_file", "Write content to a file", write_to_file),
    Tool("read_file", "Read content from a file", read_from_file),
    Tool("calculate", "Evaluate a mathematical expression", calculate),
]


# Example of how to use tools
if __name__ == "__main__":
    for tool in STANDARD_TOOLS:
        print(f"Tool: {tool.name} - {tool.description}")
        
    # Example usage
    print(get_current_time())
    print(calculate("2 + 2 * 3"))
