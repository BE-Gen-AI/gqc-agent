import json

def call_gpt(client, model, system_prompt: str, user_prompt: str) -> str:
    """
    Generate a JSON response using a GPT language model.

    Args:
        api_key (str): API key for GPT 
        model (str): GPT model name.
        system_prompt (str): System instructions.
        user_prompt (str): User query.

    Returns:
        dict: JSON response from GPT. If parsing fails, returns {"intent": "ambiguous"}.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": json.dumps(user_prompt)}
        ],
        response_format={"type": "json_object"},
        temperature=0
    )

    return response.choices[0].message.content



# try:
#     return json.loads(response.choices[0].message.content)
# except json.JSONDecodeError:
#     return {"intent": "ambiguous"}

