# GQC Agent

GQC Agent is a Python library that helps developers work with AI models using an agent-based pipeline. It includes model validation, intent classification, query rephrasing, summarization, and an orchestrator that manages all agents.

## Table of Contents
* [Overview](#overview)
* [Features](#features)
* [Technologies](#technologies)
* [Installation](#installation)
* [Usage Examples](#usage-examples)
* [Project Status](#project-status)
* [License](#license)
* [Author](#author)
* [Sources](#sources)

## Overview
GQC Agent is a lightweight agent orchestration library for LLM applications. It validates AI models, predicts user intent, rephrases queries, summarizes interactions, and organizes the agent workflow.

## Features
* GPT & Gemini model validator
* Intent classifier
* Query rephraser
* Summarizer agent
* Orchestrator for multi-agent flow
* Exception handling
* Standardized input structure
* Easy .env configuration

## Technologies
Project is created with:
* Python 3.13
* OpenAI API
* Google Gemini API

## Installation

### Install using pip (after publishing)
pip install gqc-agent

### Environment Setup
Create a `.env` file:
OPENAI_API_KEY=your_key  
GEMINI_API_KEY=your_key

## Usage Examples

### Example: Using OPENAI Client

```python
from gqc_agent.core.orchestrator import AgentPipeline

OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

client = AgentPipeline(api_key=OPENAI_API_KEY, model="gpt-4o-mini")
response = client.run_gqc(
    user_input={
        "input": "Tell me more about both of them",
        "current": {"role": "user", "query": "Tell me more about both of them", "timestamp": "2025-01-01 12:30:45"},
        "history": [
            {"role": "user", "query": "What is meant by active broker", "timestamp": "2025-01-01 12:00:00"},
            {"role": "assistant", "response": "Active broker is active in treaty and claims modules.", "timestamp": "2025-01-01 12:01:10"},
            {"role": "user", "query": "Where is pending broker used?", "timestamp": "2025-01-01 12:02:00"},
            {"role": "assistant", "response": "Pending broker is used in TR Treaty module.", "timestamp": "2025-01-01 12:03:22"}
        ]
    }
)
print(response)
```

### Example: Using GEMINI Client

```python
from gqc_agent.core.orchestrator import AgentPipeline

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

client = AgentPipeline(api_key=GEMINI_API_KEY, model="gemini-pro")
response = client.run_gqc({...})
print(response)
```

### List Supported Models

```python
from gqc_agent.core.orchestrator import AgentPipeline

print("GPT Models:", AgentPipeline.get_supported_models(api_key="YOUR_OPENAI_API_KEY"))
print("Gemini Models:", AgentPipeline.get_supported_models(api_key="YOUR_GEMINI_API_KEY"))
```

### Load System Prompt

```python
from gqc_agent.core.orchestrator import AgentPipeline

prompt = AgentPipeline.show_system_prompt(filename="sample.md")
print(prompt)
```

## Project Status
* Active Development

Planned updates:
* More LLM vendor support
* Better agent routing
* Improved accuracy
* Performance optimizations

## License
MIT License

## Author
**BIG ENTITIES**  
BE Developers

## Sources
Inspired by modern AI agent frameworks and workflow orchestration systems.