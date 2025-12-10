from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def list_gpt_models(api_key: str = None):
    """
    List all available GPT models for the given API key.

    Args:
        api_key (str, optional): OpenAI API key. If not provided, it will
                                 be read from the .env file (OPENAI_API_KEY).

    Returns:
        list: List of model IDs available in GPT.

    Raises:
        ValueError: If API key is missing.
        Exception: If the API call fails.
    """
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is missing. Set OPENAI_API_KEY in .env or pass as argument.")

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Fetch available models
    try:
        models = client.models.list()
        return [model.id for model in models]
    except Exception as e:
        print(f"Failed to fetch GPT models: {e}")
        return []

# Example usage
# if __name__ == "__main__":
#     gpt_models = list_gpt_models()
#     print("Available GPT models:", gpt_models)
