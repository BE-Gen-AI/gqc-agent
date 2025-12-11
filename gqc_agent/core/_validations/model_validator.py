import os
from difflib import get_close_matches
from gqc_agent.core._llm_models.gpt_models import list_gpt_models
from gqc_agent.core._llm_models.gemini_models import list_gemini_models
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

def validate_model(model: str, api_key: str = None):
    """
    Validate that a given model is supported by the provider corresponding to the API key.

    Only checks GPT if GPT key is provided, or Gemini if Gemini key is provided.
    Suggests closest matches if the model is invalid.

    Args:
        model (str): The model name to validate.
        api_key (str): The API key provided by the user.

    Raises:
        ValueError: If the model is invalid or no valid API key is provided.
    """
    try:
        if api_key == os.getenv("OPENAI_API_KEY"):
            # User selected GPT
            gpt_models = list_gpt_models(api_key)
            if model not in gpt_models:
                suggestion = get_close_matches(model, gpt_models, n=3, cutoff=0.4)
                suggestion_msg = f" Did you mean: {suggestion}?" if suggestion else ""
                raise ValueError(f"Invalid GPT model '{model}'. Supported models: {gpt_models}{suggestion_msg}")
            print(f"Model '{model}' is valid for GPT client")

        elif api_key == os.getenv("GEMINI_API_KEY"):
            # User selected Gemini
            gemini_models = list_gemini_models(api_key)
            if model not in gemini_models:
                suggestion = get_close_matches(model, gemini_models, n=3, cutoff=0.4)
                suggestion_msg = f" Did you mean: {suggestion}?" if suggestion else ""
                raise ValueError(f"Invalid Gemini model '{model}'. Supported models: {gemini_models}{suggestion_msg}")
            print(f"Model '{model}' is valid for Gemini client")

        else:
            raise ValueError("No valid API key provided or unknown model provider")
    except ValueError:
        
        raise
    except Exception as e:
        print(f"Error validating model: {e}")
        raise ValueError("Could not validate model due to internal error.")


# Example usage
# if __name__ == "__main__":
#     # Slightly incorrect GPT input
#     try:
#         validate_model("gpt4-mini", api_key=os.getenv("OPENAI_API_KEY"))
#     except ValueError as e:
#         print(e)

#     # Slightly incorrect Gemini input
#     try:
#         validate_model("gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY"))
#     except ValueError as e:
#         print(e)

#     # Correct model
#     validate_model("gpt-4.1-mini",  api_key=os.getenv("OPENAI_API_KEY"))
