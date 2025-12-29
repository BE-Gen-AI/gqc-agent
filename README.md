# GQC Agent

![Version](https://img.shields.io/badge/version-v1.0.2-blue)
![License](https://img.shields.io/pypi/l/gqc-agent)
![Agent](https://img.shields.io/badge/Agent-GQC-red)

GQC (General Query Classifier) Agent helps developers work with AI models using an agent-based pipeline. It includes intent classification, query rephrasing, history summarization, and an orchestrator that manages all agents.

## Quick Install

```bash
pip install gqc-agent
```

# Documentation

## What is this?
GQC Agent is a lightweight, modular Python solution for building agent-based LLM applications. It enables developers to orchestrate multiple AI agents—such as intent classification, query rephrasing, and note creation—within a single, structured pipeline. GQC Agent simplifies validating and structuring user input, selecting and managing LLM models like OpenAI and Gemini, running multiple agents in parallel, and combining their outputs into a meaningful response. It takes standard input along with the current query and the past three inputs with their responses, allowing agents to maintain context for more accurate and relevant outputs.

Designed to be simple, extensible, and production-ready, GQC Agent makes it easy to integrate intelligent conversational workflows into applications without complex setup or heavy frameworks. It is ideal for organizations and developers seeking a clean, opinionated agent pipeline, fast integration with GPT and Gemini models, clear separation of responsibilities between agents, and full control over prompts, models, and orchestration logic.

## Features

* Intent classifier – Understands and categorizes user intent.
* Query rephraser – Rewrites user queries for clarity or better processing.
* Summarizer agent – Generates concise summaries from content.
* Orchestrator for multi-agent flow – Coordinates multiple agents to work together smoothly.

## Use Cases

* AI chatbots with enhanced context handling
* Retrieval-Augmented Generation (RAG) for Q&A and summarization
* Workflow automation using multiple AI agents
* Note-taking and interaction summarization

## Examples

### Example: Using OPENAI and GEMINI Client

This example demonstrates how to use GQC Agent with OpenAI or Gemini clients to process user input, track conversation history, and generate structured responses that include intent, rephrased queries, and notes summarizing previous interactions, highlighting what has been covered, what is missing, and whether the current query relates to prior queries.

```python
from gqc_agent.core.orchestrator import AgentPipeline

OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
# GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

# client = AgentPipeline(api_key=GEMINI_API_KEY, model="models/gemini-2.5-flash", provider="gemini")
client = AgentPipeline(api_key=OPENAI_API_KEY, model="gpt-4o-mini", provider="gpt")
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

### Response

```bash
Model 'gpt-4o-mini' is valid for GPT client
{
    "intent": "search",
    "rephrased_queries": [
        "Provide more details about active and pending brokers.",
        "Explain the differences and functions of active and pending brokers."
    ],
    "notes": "The user is seeking more detailed information about both 'active broker' and 'pending broker'. Previous responses provided basic definitions but did not elaborate on their functions, differences, or specific use cases. The next response should include detailed explanations of both terms, their roles in the treaty and claims modules, and any relevant examples to enhance understanding."
}
```
### List Supported Models

This example demonstrates how to retrieve the list of all supported GPT and Gemini models available through the AgentPipeline client, allowing users to check which models they can use for their workflows.

```python
from gqc_agent.core.orchestrator import AgentPipeline

OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
# GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

# client = AgentPipeline(api_key=GEMINI_API_KEY, model="models/gemini-2.5-flash", provider="gemini")
client = AgentPipeline(api_key=OPENAI_API_KEY, model="gpt-4o-mini", provider="gpt")
gpt_models = client.get_supported_models()
# gemini_models = client.get_supported_models()
print("GPT Models from AgentPipeline:", gpt_models)
# print("GEMINI Models from AgentPipeline:", gemini_models)
```

### Response

```bash
['gpt-4-0613', 'gpt-4', 'gpt-3.5-turbo', 'gpt-5.2-chat-latest', 'gpt-5.2-2025-12-11', 'gpt-5.2', 'gpt-5.2-pro-2025-12-11', 'gpt-5.2-pro',
'davinci-002', 'babbage-002', 'gpt-3.5-turbo-instruct', 'gpt-3.5-turbo-instruct-0914',
'dall-e-3', 'dall-e-2', 'gpt-4-1106-preview', 'gpt-3.5-turbo-1106', 'tts-1-hd', 'tts-1-1106', 'tts-1-hd-1106',
'text-embedding-3-small', 'text-embedding-3-large', 'gpt-4-0125-preview', 'gpt-4-turbo-preview', 'gpt-3.5-turbo-0125', 'gpt-4-turbo', 'gpt-4-turbo-2024-04-09',
'gpt-4o', 'gpt-4o-2024-05-13', 'gpt-4o-mini-2024-07-18', 'gpt-4o-mini', 'gpt-4o-2024-08-06', 'chatgpt-4o-latest', 'gpt-4o-audio-preview', 'gpt-4o-realtime-preview',
'omni-moderation-latest', 'omni-moderation-2024-09-26', 'gpt-4o-realtime-preview-2024-12-17', 'gpt-4o-audio-preview-2024-12-17', 'gpt-4o-mini-realtime-preview-2024-12-17',
'gpt-4o-mini-audio-preview-2024-12-17', 'o1-2024-12-17', 'o1', 'gpt-4o-mini-realtime-preview', 'gpt-4o-mini-audio-preview', 'computer-use-preview', 'o3-mini', 'o3-mini-2025-01-31',
'gpt-4o-2024-11-20', 'computer-use-preview-2025-03-11', 'gpt-4o-search-preview-2025-03-11', 'gpt-4o-search-preview', 'gpt-4o-mini-search-preview-2025-03-11', 'gpt-4o-mini-search-preview',
'gpt-4o-transcribe', 'gpt-4o-mini-transcribe', 'o1-pro-2025-03-19', 'o1-pro', 'gpt-4o-mini-tts', 'o3-2025-04-16', 'o4-mini-2025-04-16', 'o3', 'o4-mini', 'gpt-4.1-2025-04-14',
'gpt-4.1', 'gpt-4.1-mini-2025-04-14', 'gpt-4.1-mini', 'gpt-4.1-nano-2025-04-14', 'gpt-4.1-nano', 'gpt-image-1', 'codex-mini-latest', 'gpt-4o-realtime-preview-2025-06-03',
'gpt-4o-audio-preview-2025-06-03', 'o4-mini-deep-research', 'gpt-4o-transcribe-diarize', 'o4-mini-deep-research-2025-06-26', 'gpt-5-chat-latest', 'gpt-5-2025-08-07', 'gpt-5',
'gpt-5-mini-2025-08-07', 'gpt-5-mini', 'gpt-5-nano-2025-08-07', 'gpt-5-nano', 'gpt-audio-2025-08-28', 'gpt-realtime', 'gpt-realtime-2025-08-28', 'gpt-audio', 'gpt-5-codex', 'gpt-image-1-mini',
'gpt-5-pro-2025-10-06', 'gpt-5-pro', 'gpt-audio-mini', 'gpt-audio-mini-2025-10-06', 'gpt-5-search-api', 'gpt-realtime-mini', 'gpt-realtime-mini-2025-10-06', 'sora-2', 'sora-2-pro',
'gpt-5-search-api-2025-10-14', 'gpt-5.1-chat-latest', 'gpt-5.1-2025-11-13', 'gpt-5.1', 'gpt-5.1-codex', 'gpt-5.1-codex-mini', 'gpt-5.1-codex-max', 'gpt-3.5-turbo-16k', 'tts-1',
'whisper-1', 'text-embedding-ada-002']
```

### Load System Prompt

This example demonstrates how to load and display a predefined system prompt using AgentPipeline. It shows the instructions and expected output format that the agent uses to create structured notes from conversation history.

```python
from gqc_agent.core.orchestrator import AgentPipeline

prompt = AgentPipeline.show_system_prompt(filename="note_creator.md")
print(prompt)
```

### Response

```bash
Available system prompts: You are an advanced note creation assistant.

Task:
- Read the current user input and the full conversation history.
- Create a detailed note that explains:
    - The user’s intent.
    - What previous responses have already covered.
    - What is missing or needs elaboration.
- Provide context so the next response can be complete and helpful.
- Always return output in JSON with a single key "notes".
- Do not include greetings, explanations, or text outside the JSON.

Example format:
{
    "notes": "The user asked for more detailed information. Previous responses covered some points, but did not provide full context or examples. Include missing context and elaborate where needed."
}
```