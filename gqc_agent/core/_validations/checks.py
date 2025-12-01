from .._llm_models.gpt_models import GPT_SUPPORTED_MODELS
from .._llm_models.gemini_models import GEMINI_SUPPORTED_MODELS

def validate_model(model: str):
    """
    Validate that a given model is supported.

    Checks if the provided `model` exists in the list of supported GPT or Gemini models.
    Raises an error if the model is not supported.

    Args:
        model (str): The name of the model to validate.

    Raises:
        ValueError: If the model is not in GPT_SUPPORTED_MODELS or GEMINI_SUPPORTED_MODELS.
    """
    all_supported = GPT_SUPPORTED_MODELS + GEMINI_SUPPORTED_MODELS

    if model not in all_supported:
        raise ValueError(
            f"Invalid model '{model}'. Supported models: {all_supported}"
        )