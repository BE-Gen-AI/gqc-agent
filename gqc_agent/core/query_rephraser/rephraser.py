from gqc_agent.core.system_prompts.loader import load_system_prompt
from gqc_agent.core._llm_models.gpt_models import list_gpt_models
from gqc_agent.core._llm_models.gemini_models import list_gemini_models
from gqc_agent.core._llm_models.gpt_client import call_gpt
from gqc_agent.core._llm_models.gemini_client import call_gemini
from dotenv import load_dotenv
import os
import json

load_dotenv()

def rephrase_query(user_input: dict, model: str, api_key: str, system_prompt_file="query_rephraser.md"):
    """
    Rephrase a user query in context of history queries.

    Args:
        user_input (dict): Structured input with 'current' and 'history' queries.
        model (str): LLM model to use (GPT or Gemini).
        api_key (str): API key for LLM.
        system_prompt_file (str): Filename of the system prompt.

    Returns:
        dict: JSON with {"rephrased_queries": ["Option 1", "Option 2"]}.
    """
    # Load system prompt
    try:
        system_prompt = load_system_prompt(system_prompt_file)
    except FileNotFoundError:
        print(f"System prompt file '{system_prompt_file}' not found.")
        return {"rephrased_queries": None}
    except Exception as e:
        print(f"Error loading system prompt '{system_prompt_file}': {e}")
        return {"rephrased_queries": None}
        

    # Prepare context
    history_queries = "\n".join([h["query"] for h in user_input.get("history", []) if h.get("role") == "user"])
    current_query = user_input["current"]["query"]

    # Create LLM prompt
    user_prompt = f"""
    History:
    {history_queries}

    Current Query:
    {current_query}
    """
    # -----------------------------
    # Auto route based on API key
    # -----------------------------
    if api_key == os.getenv("OPENAI_API_KEY"):
        # User selected GPT
        # gpt_models = list_gpt_models(api_key)
        # if model not in gpt_models:
        #     raise ValueError(f"Invalid GPT model '{model}'")
        response = call_gpt(api_key, model, system_prompt, user_prompt)

    elif api_key == os.getenv("GEMINI_API_KEY"):
        # User selected Gemini
        # gemini_models = list_gemini_models(api_key)
        # if model not in gemini_models:
        #     raise ValueError(f"Invalid Gemini model '{model}'")
        response = call_gemini(api_key, model, system_prompt, user_prompt)

    else:
        raise ValueError("No valid API key provided or unknown model provider")

    # LLM client should already return dict
    return json.loads(response)


# --------------------------
# Example test
# --------------------------
# if __name__ == "__main__":
#     test_input = {
#         "current": {
#             "role": "user",
#             "query": "description should be xyz for the department",
#             "timestamp": "2025-01-01 12:30:45"
#         },
#         "history": [
#             {"role": "user", "query": "i want to add department with the name ABC", "timestamp": "2025-01-01 12:00:00"},
#             {"role": "user", "query": "Is PHP still useful?", "timestamp": "2025-01-01 12:02:00"}
#         ]
#     }

#     # Replace with your GPT or Gemini model and API key
    # model_name = "gpt-4o-mini"  # or a Gemini model like "gemini-2.5-flash"
    # api_key = os.getenv("OPENAI_API_KEY")
#     # api_key = os.getenv("GEMINI_API_KEY")  # Use Gemini key if testing Gemini
#     if not api_key:
#         raise ValueError("API key missing. Set OPENAI_API_KEY or GEMINI_API_KEY in .env.")

    # result = rephrase_query(test_input, model=model_name, api_key=api_key)
    # print("Output:", result)