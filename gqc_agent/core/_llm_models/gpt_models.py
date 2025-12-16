def list_gpt_models(client):
    """
    List all available GPT models for the given API key.

    Args:
        client: Initialized GPT client object.

    Returns:
        list: List of model IDs available in GPT.

    Raises:
        ValueError: If API key is missing.
        Exception: If the API call fails.
    """

    if not client:
        raise ValueError("OpenAI API key is missing. Set OPENAI_API_KEY in .env or pass as argument.")

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
