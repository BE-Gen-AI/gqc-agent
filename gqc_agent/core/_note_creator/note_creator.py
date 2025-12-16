from gqc_agent.core._system_prompts.loader import load_system_prompt
from gqc_agent.core._llm_models.gpt_client import call_gpt
from gqc_agent.core._llm_models.gemini_client import call_gemini
import json
from gqc_agent.core._constants.constants import CURRENT, HISTORY, ROLE, ASSISTANT, USER, QUERY, RESPONSE, NOTES_CREATOR_PROMPT

def create_note(input_data: dict, model: str, provider: str, client, system_prompt_file=NOTES_CREATOR_PROMPT):
    """
    Generate a contextual note based on current input and conversation history.

    Args:
        input_data (dict): Structured input with 'input', 'current', and 'history'.
        model (str): LLM model name (GPT or Gemini).
        api_key (str): API key for the model.
        provider (str): provider name (gpt or gemini).
        system_prompt_file (str): System prompt filename guiding note creation.

    Returns:
        dict: JSON with {"notes": "<generated note>"}.
    """
    try:
        system_prompt = load_system_prompt(system_prompt_file)
    except FileNotFoundError:
        print(f"System prompt file '{system_prompt_file}' not found.")
        return {"notes:": None}
    except Exception as e:
        print(f"Error loading system prompt '{system_prompt_file}': {e}")
        return {"notes:": None}

    # Combine conversation history into context
    history_text = ""
    for item in input_data.get(HISTORY, []):
        if item[ROLE] == USER:
            history_text += f"User: {item[QUERY]}\n"
        elif item[ROLE] == ASSISTANT:
            history_text += f"Assistant: {item[RESPONSE]}\n"

    current_query = input_data[CURRENT][QUERY]
    # user_input_text = input_data.get("input", current_query)

    user_prompt = f"""
    Conversation History:
    {history_text}

    Current User Input:
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
#         "input": "Tell me more about it",
#         "current": {
#             "role": "user",
#             "query": "Tell me more about it",
#             "timestamp": "2025-01-01 12:30:45"
#         },
#         "history": [
#             {"role": "user", "query": "What is PHP?", "timestamp": "2025-01-01 12:00:00"},
#             {"role": "assistant", "response": "PHP is a server-side scripting language used for web development.", "timestamp": "2025-01-01 12:01:10"},
#             {"role": "user", "query": "Is PHP still useful?", "timestamp": "2025-01-01 12:02:00"},
#             {"role": "assistant", "response": "Yes, PHP is still widely used, especially for WordPress and backend APIs.", "timestamp": "2025-01-01 12:03:22"}
#         ]
#     }

#     # Replace with your GPT or Gemini model and API key
    # model_name = "gpt-4o-mini"  # or a Gemini model like "gemini-2.5-flash"
    # api_key = os.getenv("OPENAI_API_KEY")
#     # api_key = os.getenv("GEMINI_API_KEY")  # Use Gemini key if testing Gemini
#     if not api_key:
#         raise ValueError("API key missing. Set OPENAI_API_KEY or GEMINI_API_KEY in .env.")

    # result = create_note(test_input, model=model_name, api_key=api_key)
    # print("Output:", result)