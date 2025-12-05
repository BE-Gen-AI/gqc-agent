from gqc_agent.core.system_prompts.loader import load_system_prompt
from gqc_agent.core._llm_models.gpt_client import call_gpt
from gqc_agent.core._llm_models.gemini_client import call_gemini
from dotenv import load_dotenv
import os
import json

load_dotenv()

def classify_intent(user_input: dict, model: str, api_key: str, system_prompt_file="intent_classifier.md"):
    """
    Classify user intent using GPT or Gemini.

    Args:
        user_input (dict): Structured input with 'current' and 'previous' queries.
        model (str): Model name (GPT or Gemini).
        api_key (str): API key for the LLM.
        system_prompt_file (str): Filename of the system prompt.

    Returns:
        dict: JSON with {"intent": "..."}.
    """
    system_prompt = load_system_prompt(system_prompt_file)

    previous = "\n".join([p["query"] for p in user_input.get("previous", [])])
    current = user_input["current"]["query"]

    user_prompt = f"""
Previous User Queries:
{previous}

Current User Query:
{current}

Return only JSON:
{{ "intent": "search" }} OR {{ "intent": "tool_call" }} OR {{ "intent": "ambiguous" }}
"""

    # Auto route to GPT or Gemini
    if model.lower().startswith("gpt"):
        response = call_gpt(api_key, model, system_prompt, user_prompt)
    else:
        response = call_gemini(api_key, model, system_prompt, user_prompt)

    return response

# --------------------------
# Example test
# --------------------------
if __name__ == "__main__":
    test_input = {
        "current": {
            "role": "user",
            "query": "i want to add department with the name HR",
            "timestamp": "2025-01-01 12:30:45"
        },
        "previous": [
            {"role": "user", "query": "i want to add department with the name ABC", "timestamp": "2025-01-01 12:00:00"},
            {"role": "user", "query": "Is PHP still useful?", "timestamp": "2025-01-01 12:02:00"}
        ]
    }

    # Replace with your GPT or Gemini model and API key
    model_name = "gpt-4o-mini"  # or a Gemini model like "gemini-2.5-flash"
    api_key = os.getenv("OPENAI_API_KEY")
    # api_key = os.getenv("GEMINI_API_KEY")  # Use Gemini key if testing Gemini
    if not api_key:
        raise ValueError("API key missing. Set OPENAI_API_KEY or GEMINI_API_KEY in .env.")

    result = classify_intent(test_input, model=model_name, api_key=api_key)
    print("Output:", result)