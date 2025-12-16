from gqc_agent.core._system_prompts.loader import load_system_prompt
from gqc_agent.core._llm_models.gpt_client import call_gpt
from gqc_agent.core._llm_models.gemini_client import call_gemini
import json
from gqc_agent.core._constants.constants import CURRENT, HISTORY, QUERY, ROLE, USER, CLASSIFIER_PROMPT


def classify_intent(user_input: dict, model: str, provider: str, client, system_prompt_file=CLASSIFIER_PROMPT):
    """
    Classify user intent using GPT or Gemini.

    Args:
        user_input (dict): Structured input with 'current' and 'history' queries.
        model (str): Model name supported (GPT or Gemini).
        provider (str): LLM provider, either "gpt" or "gemini".
        client: Initialized LLM client (OpenAI or Gemini client object).
        system_prompt_file (str): Filename of the system prompt.

    Returns:
        dict: JSON with {"intent": "..."}.
    """
    try:
        system_prompt = load_system_prompt(system_prompt_file)
    except FileNotFoundError:
        print(f"System prompt file '{system_prompt_file}' not found.")
        return {"intent": None}
    except Exception as e:
        print(f"Error loading system prompt '{system_prompt_file}': {e}")
        return {"intent": None}

    current_query = user_input[CURRENT][QUERY]
    history_queries = "\n".join([h[QUERY] for h in user_input.get(HISTORY, []) if h.get(ROLE) == USER])

    user_prompt = f"""
    History User Queries:
    {history_queries}

    Current User Query:
    {current_query}
    """
    
    # -----------------------------
    # Auto route based on API key
    # -----------------------------
    if provider.lower() == "gpt":

        response = call_gpt(client, model, system_prompt, user_prompt)

    elif provider.lower() == "gemini":

        response = call_gemini(client, model, system_prompt, user_prompt)

    else:
        raise ValueError("No valid API key provided or unknown model provider")


    return json.loads(response)

# --------------------------
# Example test
# --------------------------
# if __name__ == "__main__":
#     test_input = {
#         "current": {
#             "role": "user",
#             "query": "i want to send an email to john",
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

    # if not api_key:
    #     raise ValueError("API key missing. Set OPENAI_API_KEY or GEMINI_API_KEY in .env.")

    # result = classify_intent(test_input, model=model_name, api_key=api_key)
    # print("Output:", result)