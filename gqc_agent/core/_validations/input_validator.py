from gqc_agent.core._constants.constants import INPUT, CURRENT, HISTORY, ROLE, QUERY, TIMESTAMP, USER, ASSISTANT, RESPONSE

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
    for key in [INPUT, CURRENT, HISTORY]:
        if key not in user_input:
            raise ValueError(f"Missing key: {key}")
        
    # -----------------------------
    # Step 2: Validate 'input'
    # -----------------------------
    if not isinstance(user_input[INPUT], str):
        raise ValueError("`input` must be a string")
    if not user_input[INPUT].strip():
        raise ValueError("`input` cannot be empty")

    # -----------------------------
    # Step 3: Validate 'current' section
    # -----------------------------
    current = user_input[CURRENT]
    
    if not isinstance(current, dict):
        raise ValueError("`current` must be a dict")
    
    # Ensure all required fields are present and are strings
    for field in [ROLE, QUERY, TIMESTAMP]:
        if field not in current:
            raise ValueError(f"Missing field in current: {field}")
        if not isinstance(current[field], str):
            raise ValueError(f"`{field}` must be a string")
    
    # 'current.role' must always be 'user'
    if current[ROLE] != USER:
        raise ValueError("`current.role` must be 'user'")

    # -----------------------------
    # Step 4: Validate 'history' section
    # -----------------------------
    history = user_input[HISTORY]
    
    if not isinstance(history, list):
        raise ValueError("`history` must be a list")
    
    for idx, msg in enumerate(history):
        # Each history item must be a dictionary
        if not isinstance(msg, dict):
            raise ValueError(f"History item {idx} must be a dict")
        
        # Each item must have 'role' and 'timestamp'
        if ROLE not in msg or TIMESTAMP not in msg:
            raise ValueError(f"History item {idx} missing 'role' or 'timestamp'")
        
        # Role must be either 'user' or 'assistant'
        if msg[ROLE] not in [USER, ASSISTANT]:
            raise ValueError(f"Invalid role in history item {idx}")
        
        # User messages must have 'query'
        if msg[ROLE] == USER and QUERY not in msg:
            raise ValueError(f"User history item {idx} missing 'query'")
        
        # Assistant messages must have 'response'
        if msg[ROLE] == ASSISTANT and RESPONSE not in msg:
            raise ValueError(f"Assistant history item {idx} missing 'response'")


# -----------------------------
# Quick test of the validator
# -----------------------------
# if __name__ == "__main__":
#     test_input = {
#         "input": "Tell me more about it",
#         "current": {"role": "user", "query": "Tell me more about it", "timestamp": "2025-01-01 12:30:45"},
#         "history": [
#             {"role": "user", "query": "What is PHP?", "timestamp": "2025-01-01 12:00:00"},
#             {"role": "assistant", "response": "PHP is a language", "timestamp": "2025-01-01 12:01:10"}
#         ]
#     }
    
#     # Run the validator
#     validate_input(test_input)
#     print("Input is valid")
    