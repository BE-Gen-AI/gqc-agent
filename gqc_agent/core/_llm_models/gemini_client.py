from google.genai import types
import json
def call_gemini(client, model, system_prompt: str, user_prompt: str) -> str:
    """
    Generate a JSON response using a Gemini language model.

    Args:
        client: Initialized GEMINI client object.
        model (str): Gemini model name.
        system_prompt (str): System instructions.
        user_prompt (str): User query.

    Returns:
        dict: JSON response from Gemini. If parsing fails, returns {"intent": "ambiguous"}.
    """

    chat = client.chats.create(
        model=model,
        config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
    )
    response = chat.send_message(
        f"System: {system_prompt}\nUser: {user_prompt}"
    )

    return response.text


    # try:
    #     return json.loads(response.text)
    # except json.JSONDecodeError:
    #     return {"intent": "ambiguous"}
