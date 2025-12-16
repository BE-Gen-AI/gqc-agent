def list_gemini_models(client):
    """
    List all available Gemini models for the given API key.

    Args:
        client: Initialized GEMINI client object.

    Returns:
        list: List of model names available in Gemini.

    Raises:
        ValueError: If API key is missing.
        Exception: If the API call fails.
    """
    
    if not client:
        raise ValueError("Gemini API key is missing. Set GEMINI_API_KEY in .env or pass as argument.")
    
    # Fetch available models
    try:
        models = client.models.list()  # replace with actual method if different
        return [model.name for model in models]
    except Exception as e:
        print(f"Failed to fetch Gemini models: {e}")
        return []

# # Example usage
# if __name__ == "__main__":
#     gemini_models = list_gemini_models()
#     print("Available Gemini models:", gemini_models)
