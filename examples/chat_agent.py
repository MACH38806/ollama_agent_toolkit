"""Example implementation of a conversational chat agent."""

import json
from typing import List, Dict, Any, Optional
from agent import Agent
from tools import Tool, STANDARD_TOOLS


class ChatAgent(Agent):
    """A simple conversational agent focused on natural dialogue."""
    
    def __init__(self, model: str = "llama3", verbose: bool = False, personality: str = "friendly"):
        """Initialize the chat agent.
        
        Args:
            model: The name of the model to use.
            verbose: Whether to print verbose output.
            personality: The personality style for the agent.
        """
        # Define available personalities
        personalities = {
            "friendly": "You are friendly, warm, and engaging. You use a conversational tone with occasional humor and emoticons.",
            "professional": "You are professional, clear, and concise. You maintain a formal tone and prioritize accuracy and efficiency.",
            "creative": "You are creative, imaginative, and inspirational. You use vivid language, metaphors, and diverse perspectives.",
            "supportive": "You are supportive, empathetic, and understanding. You acknowledge emotions and provide encouragement."
        }
        
        # Select the personality or default to friendly
        selected_personality = personalities.get(personality, personalities["friendly"])
        
        # Define chat-specific system prompt
        chat_prompt = f"""{selected_personality}
        
        As a conversational assistant, your primary goal is to engage in natural, helpful dialogue.
        
        Guidelines for conversation:
        1. Listen carefully and respond directly to the user's messages
        2. Maintain context throughout the conversation
        3. Ask clarifying questions when needed
        4. Provide concise responses unless detail is requested
        5. Be respectful, inclusive, and considerate
        
        You should aim to be helpful while maintaining a natural conversational flow.
        Avoid unnecessarily formal or robotic responses.
        """
        
        # Initialize the base agent with chat configuration
        super().__init__(
            model=model,
            system_prompt=chat_prompt,
            tools=STANDARD_TOOLS,  # Use standard tools for occasional help requests
            verbose=verbose
        )
        
        self.personality = personality
    
    def change_personality(self, new_personality: str) -> str:
        """Change the agent's personality style.
        
        Args:
            new_personality: The new personality style ('friendly', 'professional', 'creative', 'supportive').
            
        Returns:
            A message indicating the personality change.
        """
        personalities = {
            "friendly": "You are friendly, warm, and engaging. You use a conversational tone with occasional humor and emoticons.",
            "professional": "You are professional, clear, and concise. You maintain a formal tone and prioritize accuracy and efficiency.",
            "creative": "You are creative, imaginative, and inspirational. You use vivid language, metaphors, and diverse perspectives.",
            "supportive": "You are supportive, empathetic, and understanding. You acknowledge emotions and provide encouragement."
        }
        
        if new_personality not in personalities:
            return f"Personality '{new_personality}' not recognized. Available personalities: {', '.join(personalities.keys())}"
        
        self.personality = new_personality
        selected_personality = personalities[new_personality]
        
        # Update the system prompt with the new personality
        new_system_prompt = f"""{selected_personality}
        
        As a conversational assistant, your primary goal is to engage in natural, helpful dialogue.
        
        Guidelines for conversation:
        1. Listen carefully and respond directly to the user's messages
        2. Maintain context throughout the conversation
        3. Ask clarifying questions when needed
        4. Provide concise responses unless detail is requested
        5. Be respectful, inclusive, and considerate
        
        You should aim to be helpful while maintaining a natural conversational flow.
        Avoid unnecessarily formal or robotic responses.
        """
        
        # Reset the agent and add the new system prompt
        self.reset()
        self.system_prompt = new_system_prompt
        self.memory.add_message("system", new_system_prompt)
        
        return f"Personality changed to '{new_personality}'."


# Example usage
if __name__ == "__main__":
    # Create a chat agent
    agent = ChatAgent(model="llama3", verbose=True, personality="friendly")
    
    # Test with a conversational prompt
    response = agent.process_user_input("Hi there! How are you today?")
    print(f"\nChat Agent response: {response}")
    
    # Change personality and test again
    agent.change_personality("professional")
    response = agent.process_user_input("Can you tell me about yourself?")
    print(f"\nChat Agent (professional) response: {response}")
    
    # Test with a request that might use a tool
    response = agent.process_user_input("What's the weather like in New York?")
    print(f"\nChat Agent response: {response}")
