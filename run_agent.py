"""Entry point script to run the agent."""

import sys
import argparse
from termcolor import colored

from agent import Agent


def main():
    """Run the agent in interactive mode."""
    parser = argparse.ArgumentParser(description="Run an Ollama-powered agent")
    parser.add_argument("--model", type=str, default="llama3", 
                        help="Model to use (default: llama3)")
    parser.add_argument("--verbose", action="store_true", 
                        help="Enable verbose output")
    args = parser.parse_args()
    
    print(colored("\n===== Ollama Agent =====\n", "cyan"))
    print(colored(f"Using model: {args.model}", "cyan"))
    print(colored("Type 'exit' or 'quit' to end the session.", "cyan"))
    print(colored("Type 'reset' to reset the conversation.", "cyan"))
    print(colored("\n", "cyan"))
    
    try:
        # Initialize the agent
        agent = Agent(model=args.model, verbose=args.verbose)
        
        while True:
            # Get user input
            user_input = input(colored("You: ", "green"))
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print(colored("\nGoodbye!", "cyan"))
                break
                
            # Check for reset command
            if user_input.lower() == "reset":
                agent.reset()
                print(colored("Conversation reset.", "yellow"))
                continue
            
            # Process the user input
            try:
                response = agent.process_user_input(user_input)
                print(colored(f"\nAgent: {response}", "blue"))
            except Exception as e:
                print(colored(f"\nError: {str(e)}", "red"))
                
    except KeyboardInterrupt:
        print(colored("\n\nSession terminated by user.", "cyan"))
        sys.exit(0)


if __name__ == "__main__":
    main()
