"""Main agent class with core functionality."""

import json
import re
from typing import List, Dict, Any, Optional, Tuple, Union
from termcolor import colored

from ollama_client import OllamaClient
from memory import Memory
from tools import Tool, STANDARD_TOOLS


class Agent:
    """An agent that can interact with the user and use tools."""
    
    def __init__(self, 
                 model: str = "llama3",
                 system_prompt: Optional[str] = None,
                 tools: Optional[List[Tool]] = None,
                 verbose: bool = False):
        """Initialize the agent.
        
        Args:
            model: The name of the model to use.
            system_prompt: Optional system prompt to guide the model.
            tools: List of tools available to the agent.
            verbose: Whether to print verbose output.
        """
        self.client = OllamaClient()
        self.model = model
        self.memory = Memory()
        self.tools = tools or STANDARD_TOOLS
        self.verbose = verbose
        
        # Set up the default system prompt if none provided
        if system_prompt is None:
            self.system_prompt = self._create_default_system_prompt()
        else:
            self.system_prompt = system_prompt
            
        # Add the system prompt to memory
        self.memory.add_message("system", self.system_prompt)
        
    def _create_default_system_prompt(self) -> str:
        """Create a default system prompt based on available tools.
        
        Returns:
            The default system prompt string.
        """
        tools_description = "\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools])
        
        return f"""You are a helpful AI assistant that can use tools to assist the user. 
        
AVAILABLE TOOLS:
{tools_description}

To use a tool, respond with a JSON object in the following format:{{"tool":"tool_name","parameters":{{"param1":"value1","param2":"value2"}}}}

If you don't need to use a tool, just respond normally.
If a user requests something that would be better handled by a tool, use the appropriate tool.
Always provide thoughtful, helpful responses and prioritize solving the user's problem."""
    
    def _extract_tool_call(self, response: str) -> Tuple[Optional[str], Optional[Dict[str, Any]], str]:
        """Extract tool calls from the model's response.
        
        Args:
            response: The model's response text.
            
        Returns:
            A tuple of (tool_name, parameters, cleaned_response)
        """
        # Check for JSON-formatted tool calls
        json_pattern = r'\{\\s*\"tool\"\\s*:\\s*\"([^\"]+)\"\\s*,\\s*\"parameters\"\\s*:\\s*\\{([^}]+)\\}\\s*\\}'
        match = re.search(json_pattern, response)
        
        if match:
            try:
                # Extract the whole JSON object
                json_str = match.group(0)
                tool_call = json.loads(json_str)
                tool_name = tool_call.get("tool")
                parameters = tool_call.get("parameters", {})
                
                # Remove the tool call from the response
                cleaned_response = response.replace(json_str, "")
                return tool_name, parameters, cleaned_response
            except json.JSONDecodeError:
                pass
        
        return None, None, response
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input and generate a response.
        
        Args:
            user_input: The user's input text.
            
        Returns:
            The agent's response.
        """
        # Add user message to memory
        self.memory.add_message("user", user_input)
        
        # Get the response from the model
        messages = self.memory.get_chat_messages()
        response = self.client.chat(
            model=self.model,
            messages=messages,
            system_prompt=self.system_prompt,
            temperature=0.7
        )
        
        # Extract tool calls if present
        tool_name, parameters, cleaned_response = self._extract_tool_call(response)
        
        # Execute tool if a valid tool call was found
        if tool_name:
            tool_response = self._execute_tool(tool_name, parameters)
            
            # Add the assistant's response and tool response to memory
            self.memory.add_message("assistant", cleaned_response)
            self.memory.add_message("system", f"Tool '{tool_name}' output: {tool_response}")
            
            # Get a follow-up response that incorporates the tool output
            messages = self.memory.get_chat_messages()
            final_response = self.client.chat(
                model=self.model,
                messages=messages,
                system_prompt=self.system_prompt,
                temperature=0.7
            )
            
            # Add the final response to memory
            self.memory.add_message("assistant", final_response)
            
            if self.verbose:
                print(colored(f"\nUsed tool: {tool_name}", "yellow"))
                print(colored(f"Tool response: {tool_response}", "yellow"))
            
            return final_response
        else:
            # Add the assistant's response to memory
            self.memory.add_message("assistant", response)
            return response
    
    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """Execute a tool with the given parameters.
        
        Args:
            tool_name: The name of the tool to execute.
            parameters: The parameters to pass to the tool.
            
        Returns:
            The tool's response as a string.
        """
        for tool in self.tools:
            if tool.name == tool_name:
                try:
                    return tool(**parameters)
                except Exception as e:
                    return f"Error executing tool '{tool_name}': {str(e)}"
        
        return f"Unknown tool: {tool_name}"
    
    def reset(self) -> None:
        """Reset the agent's memory."""
        self.memory.clear()
        # Add the system prompt back to memory
        self.memory.add_message("system", self.system_prompt)


# Example usage
if __name__ == "__main__":
    agent = Agent(model="llama3", verbose=True)
    
    # Test the agent with a simple query
    response = agent.process_user_input("What's the current time in New York?")
    print(f"\nAgent response: {response}")
    
    # Test the agent with a query that should use a tool
    response = agent.process_user_input("Calculate 234 * 456")
    print(f"\nAgent response: {response}")
