# Ollama Agent Toolkit

This repository provides a toolkit for building intelligent agents using Ollama, an open-source framework for running language models locally.

## Quick Setup Guide

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed on your system

### Installation

1. Clone this repository:
```bash
git clone https://github.com/MACH38806/ollama_agent_toolkit.git
cd ollama_agent_toolkit
```

2. Create a virtual environment:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make sure Ollama is running on your system:
```bash
ollama serve
```

5. Pull at least one model to use with your agent:
```bash
ollama pull llama3
```

### Running the Sample Agent

To run the sample agent:

```bash
python run_agent.py
```

This will start an interactive session with the basic agent.

## Project Structure

- `agent.py` - Main agent class with core functionality
- `ollama_client.py` - Client for Ollama API integration
- `tools.py` - Example tools that can be integrated with the agent
- `memory.py` - Simple conversation memory management
- `run_agent.py` - Entry point script to run the agent
- `examples/` - Example agent implementations for various use cases

## Example Agents

The toolkit includes several example agent implementations:

1. **Research Agent** - Specialized for information gathering and research tasks
2. **Coding Agent** - Focused on programming assistance and code generation
3. **Chat Agent** - Optimized for natural conversation with configurable personalities

To run an example agent:

```bash
python -m examples.run_example [research|coding|chat] --model llama3
```

## Customizing Your Agent

For details on how to customize the agent with different models, tools, and capabilities, see the comments in each file. The basic architecture supports:

- Adding custom tools
- Configuring different Ollama models
- Extending the agent's memory and reasoning capabilities

## Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [Agent Design Patterns](https://www.datacamp.com/blog/ai-agents-practical-guide)
