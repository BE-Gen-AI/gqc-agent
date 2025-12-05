from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def list_gemini_models(api_key: str = None):
    """
    List all available Gemini models for the given API key.

    Args:
        api_key (str, optional): Gemini API key. If not provided, it will
                                 be read from the .env file (GEMINI_API_KEY).

    Returns:
        list: List of model names available in Gemini.

    Raises:
        ValueError: If API key is missing.
        Exception: If the API call fails.
    """
    api_key = api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Gemini API key is missing. Set GEMINI_API_KEY in .env or pass as argument.")

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)
    
    # Fetch available models
    try:
        models = client.models.list()  # replace with actual method if different
        return [model.name for model in models]
    except Exception as e:
        raise Exception(f"Failed to fetch Gemini models: {e}")

# Example usage
if __name__ == "__main__":
    gemini_models = list_gemini_models()
    print("Available Gemini models:", gemini_models)
