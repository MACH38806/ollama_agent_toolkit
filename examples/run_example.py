"""Script to run example agents."""

import sys
import argparse
from termcolor import colored

from examples.research_agent import ResearchAgent
from examples.coding_agent import CodingAgent
from examples.chat_agent import ChatAgent


def main():
    """Run an example agent."""
    parser = argparse.ArgumentParser(description="Run an example agent")
    parser.add_argument("agent_type", type=str, choices=["research", "coding", "chat"],
                        help="Type of agent to run")
    parser.add_argument("--model", type=str, default="llama3", 
                        help="Model to use (default: llama3)")
    parser.add_argument("--verbose", action="store_true", 
                        help="Enable verbose output")
    parser.add_argument("--personality", type=str, default="friendly",
                        help="Personality for chat agent (friendly, professional, creative, supportive)")
    args = parser.parse_args()
    
    print(colored(f"\n===== {args.agent_type.capitalize()} Agent =====\n", "cyan"))
    print(colored(f"Using model: {args.model}", "cyan"))
    print(colored("Type 'exit' or 'quit' to end the session.", "cyan"))
    print(colored("Type 'reset' to reset the conversation.", "cyan"))
    print(colored("\n", "cyan"))
    
    try:
        # Initialize the appropriate agent
        if args.agent_type == "research":
            agent = ResearchAgent(model=args.model, verbose=args.verbose)
        elif args.agent_type == "coding":
            agent = CodingAgent(model=args.model, verbose=args.verbose)
        elif args.agent_type == "chat":
            agent = ChatAgent(model=args.model, verbose=args.verbose, personality=args.personality)
            print(colored(f"Chat agent personality: {args.personality}", "cyan"))
            print(colored("Type 'personality:NAME' to change personality.", "cyan"))
        
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
                
            # Check for personality change (chat agent only)
            if args.agent_type == "chat" and user_input.startswith("personality:"):
                personality = user_input.split(":")[1].strip().lower()
                response = agent.change_personality(personality)
                print(colored(f"\nSystem: {response}", "yellow"))
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
