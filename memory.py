"""Memory management for agent conversations."""

from typing import List, Dict, Any, Optional
from datetime import datetime


class Message:
    """A message in a conversation."""
    
    def __init__(self, role: str, content: str):
        """Initialize a message.
        
        Args:
            role: The role of the message sender (e.g., 'user', 'system', 'assistant').
            content: The content of the message.
        """
        self.role = role
        self.content = content
        self.timestamp = datetime.now().isoformat()
        
    def to_dict(self) -> Dict[str, str]:
        """Convert the message to a dictionary.
        
        Returns:
            A dictionary representation of the message.
        """
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp
        }
    
    def to_chat_message(self) -> Dict[str, str]:
        """Convert the message to a chat message format for API.
        
        Returns:
            A dictionary with role and content keys.
        """
        return {
            "role": self.role,
            "content": self.content
        }


class Memory:
    """Memory management for agent conversations."""
    
    def __init__(self, max_tokens: int = 16000):
        """Initialize the memory.
        
        Args:
            max_tokens: Maximum number of tokens to store in memory.
        """
        self.messages: List[Message] = []
        self.max_tokens = max_tokens
        self.token_count = 0  # Simple approximation: 1 word = 1.3 tokens
        
    def add_message(self, role: str, content: str) -> None:
        """Add a message to memory.
        
        Args:
            role: The role of the message sender.
            content: The content of the message.
        """
        message = Message(role, content)
        self.messages.append(message)
        
        # Very rough token counting - in a real implementation use a tokenizer
        self.token_count += len(content.split()) * 1.3
        
        # Prune old messages if we exceed max_tokens
        self._prune_if_needed()
        
    def get_chat_messages(self) -> List[Dict[str, str]]:
        """Get messages in a format suitable for chat APIs.
        
        Returns:
            A list of message dictionaries with role and content keys.
        """
        return [msg.to_chat_message() for msg in self.messages]
    
    def get_last_n_messages(self, n: int) -> List[Dict[str, str]]:
        """Get the last n messages.
        
        Args:
            n: The number of messages to retrieve.
            
        Returns:
            A list of the last n message dictionaries.
        """
        return [msg.to_chat_message() for msg in self.messages[-n:]]
    
    def get_context_window(self) -> str:
        """Get the entire conversation history as a formatted string.
        
        Returns:
            A string containing the formatted conversation history.
        """
        formatted_messages = []
        for msg in self.messages:
            formatted_messages.append(f"{msg.role.upper()}: {msg.content}")
        return "\n\n".join(formatted_messages)
    
    def clear(self) -> None:
        """Clear all messages from memory."""
        self.messages = []
        self.token_count = 0
        
    def _prune_if_needed(self) -> None:
        """Remove oldest messages if token count exceeds max_tokens."""
        while self.token_count > self.max_tokens and len(self.messages) > 3:
            removed_message = self.messages.pop(0)
            self.token_count -= len(removed_message.content.split()) * 1.3


# Example usage
if __name__ == "__main__":
    memory = Memory(max_tokens=1000)
    
    # Add some messages
    memory.add_message("system", "You are a helpful assistant.")
    memory.add_message("user", "Hi, can you help me with a Python question?")
    memory.add_message("assistant", "Of course! I'm happy to help with Python. What's your question?")
    
    # Get messages for API
    chat_messages = memory.get_chat_messages()
    print(f"Chat messages: {chat_messages}")
    
    # Get formatted context window
    context = memory.get_context_window()
    print(f"\nContext window:\n{context}")
