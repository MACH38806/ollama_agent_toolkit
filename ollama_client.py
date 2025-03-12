"""Client for interacting with the Ollama API."""

import json
import requests
from typing import Dict, List, Optional, Union, Any


class OllamaClient:
    """Client for the Ollama API to run inference with local models."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize the Ollama client.

        Args:
            base_url: The base URL for the Ollama API.
        """
        self.base_url = base_url

    def generate(self, 
                 model: str, 
                 prompt: str, 
                 system_prompt: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: int = 1000,
                 stream: bool = False) -> Union[str, Dict[str, Any]]:
        """Generate a completion for the given prompt.

        Args:
            model: The name of the model to use.
            prompt: The prompt to generate from.
            system_prompt: Optional system prompt to guide the model.
            temperature: The temperature to use for generation.
            max_tokens: The maximum number of tokens to generate.
            stream: Whether to stream the response.

        Returns:
            The generated text or full API response if streaming.
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
            
        if stream:
            response = requests.post(url, json=payload, stream=True)
            return response
        else:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json()["response"]
            else:
                raise Exception(f"Error: {response.status_code} - {response.text}")
    
    def chat(self,
             model: str,
             messages: List[Dict[str, str]],
             system_prompt: Optional[str] = None,
             temperature: float = 0.7,
             max_tokens: int = 1000,
             stream: bool = False) -> Union[str, Dict[str, Any]]:
        """Generate a response in a chat conversation.

        Args:
            model: The name of the model to use.
            messages: A list of message dictionaries with 'role' and 'content' keys.
            system_prompt: Optional system prompt to guide the model.
            temperature: The temperature to use for generation.
            max_tokens: The maximum number of tokens to generate.
            stream: Whether to stream the response.

        Returns:
            The generated text or full API response if streaming.
        """
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
            
        if stream:
            response = requests.post(url, json=payload, stream=True)
            return response
        else:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json()["message"]["content"]
            else:
                raise Exception(f"Error: {response.status_code} - {response.text}")
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List all available models.

        Returns:
            A list of model information dictionaries.
        """
        url = f"{self.base_url}/api/tags"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()["models"]
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
    
    def pull_model(self, model: str) -> None:
        """Pull a model from the Ollama library.

        Args:
            model: The name of the model to pull.
        """
        url = f"{self.base_url}/api/pull"
        payload = {"name": model}
        response = requests.post(url, json=payload, stream=True)
        
        for line in response.iter_lines():
            if line:
                print(json.loads(line.decode('utf-8')))

    def get_model_info(self, model: str) -> Dict[str, Any]:
        """Get information about a specific model.

        Args:
            model: The name of the model.

        Returns:
            A dictionary containing model information.
        """
        url = f"{self.base_url}/api/show"
        payload = {"name": model}
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")


# Example usage
if __name__ == "__main__":
    client = OllamaClient()
    
    # List available models
    try:
        models = client.list_models()
        print(f"Available models: {[model['name'] for model in models]}")
    except Exception as e:
        print(f"Error listing models: {e}")
    
    # Simple generation example
    try:
        response = client.generate(
            model="llama3", 
            prompt="Explain what Ollama is in one paragraph",
            temperature=0.7
        )
        print(f"Generated response:\n{response}")
    except Exception as e:
        print(f"Error generating response: {e}")
