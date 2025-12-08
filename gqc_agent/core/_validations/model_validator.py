import os
from difflib import get_close_matches
from gqc_agent.core._llm_models.gpt_models import list_gpt_models
from gqc_agent.core._llm_models.gemini_models import list_gemini_models
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

def validate_model(model: str):
    """
    Validate that a given model is supported by either GPT or Gemini.

    If the model is invalid, it provides a suggestion of the closest valid model(s)
    in the relevant category (GPT or Gemini) or all models if unknown type.

    Args:
        model (str): The model name to validate.

    Raises:
        ValueError: If the model is not in GPT or Gemini supported models.
    """
    gpt_api_key = os.getenv("OPENAI_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    # Fetch models dynamically
    gpt_models = list_gpt_models(api_key=gpt_api_key)
    gemini_models = list_gemini_models(api_key=gemini_api_key)

    all_supported = gpt_models + gemini_models

    if model not in all_supported:
        # Determine which category to check
        if "gpt" in model.lower():
            category_models = gpt_models
        elif "gemini" in model.lower():
            category_models = gemini_models
        else:
            category_models = all_supported

        # Find closest matches
        suggestion = get_close_matches(model, category_models, n=3, cutoff=0.4)
        suggestion_msg = f" Did you mean: {suggestion}?" if suggestion else ""
        raise ValueError(
            f"Invalid model '{model}'. Supported models in this category: {category_models}{suggestion_msg}"
        )

    print(f"Model '{model}' is valid ✅")


# Example usage
if __name__ == "__main__":
    # Slightly incorrect GPT input
    try:
        validate_model("gpt4-mini")
    except ValueError as e:
        print(e)

    # Slightly incorrect Gemini input
    try:
        validate_model("gemini-2.5-flash")
    except ValueError as e:
        print(e)

    # Correct model
    validate_model("gpt-4.1-mini")
