def validate_input(user_input: dict):
    """
    Validate that the user input JSON matches the required format.
    
    Expected format:
    {
      "input": str,
      "current": {"role": "user", "query": str, "timestamp": str},
      "history": [
          {"role": "user"/"assistant", "query"/"response": str, "timestamp": str}, ...
      ]
    }
    
    Raises:
        ValueError: if any required field is missing or incorrectly formatted.
    """
    
    # -----------------------------
    # Step 1: Check top-level keys
    # -----------------------------
    for key in ["input", "current", "history"]:
        if key not in user_input:
            raise ValueError(f"Missing key: {key}")
        
    # -----------------------------
    # Step 2: Validate 'input'
    # -----------------------------
    if not isinstance(user_input["input"], str):
        raise ValueError("`input` must be a string")
    if not user_input["input"].strip():
        raise ValueError("`input` cannot be empty")

    # -----------------------------
    # Step 3: Validate 'current' section
    # -----------------------------
    current = user_input["current"]
    
    if not isinstance(current, dict):
        raise ValueError("`current` must be a dict")
    
    # Ensure all required fields are present and are strings
    for field in ["role", "query", "timestamp"]:
        if field not in current:
            raise ValueError(f"Missing field in current: {field}")
        if not isinstance(current[field], str):
            raise ValueError(f"`{field}` must be a string")
    
    # 'current.role' must always be 'user'
    if current["role"] != "user":
        raise ValueError("`current.role` must be 'user'")

    # -----------------------------
    # Step 4: Validate 'history' section
    # -----------------------------
    history = user_input["history"]
    
    if not isinstance(history, list):
        raise ValueError("`history` must be a list")
    
    for idx, msg in enumerate(history):
        # Each history item must be a dictionary
        if not isinstance(msg, dict):
            raise ValueError(f"History item {idx} must be a dict")
        
        # Each item must have 'role' and 'timestamp'
        if "role" not in msg or "timestamp" not in msg:
            raise ValueError(f"History item {idx} missing 'role' or 'timestamp'")
        
        # Role must be either 'user' or 'assistant'
        if msg["role"] not in ["user", "assistant"]:
            raise ValueError(f"Invalid role in history item {idx}")
        
        # User messages must have 'query'
        if msg["role"] == "user" and "query" not in msg:
            raise ValueError(f"User history item {idx} missing 'query'")
        
        # Assistant messages must have 'response'
        if msg["role"] == "assistant" and "response" not in msg:
            raise ValueError(f"Assistant history item {idx} missing 'response'")


# -----------------------------
# Quick test of the validator
# -----------------------------
if __name__ == "__main__":
    test_input = {
        "input": "Tell me more about it",
        "current": {"role": "user", "query": "Tell me more about it", "timestamp": "2025-01-01 12:30:45"},
        "history": [
            {"role": "user", "query": "What is PHP?", "timestamp": "2025-01-01 12:00:00"},
            {"role": "assistant", "response": "PHP is a language", "timestamp": "2025-01-01 12:01:10"}
        ]
    }
    
    # Run the validator
    validate_input(test_input)
    print("Input is valid ✅")
    