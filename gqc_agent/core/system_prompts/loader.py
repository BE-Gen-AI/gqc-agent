import os

def load_system_prompt(name: str = "version1.md") -> str:
    """
    Load the content of a system prompt markdown file.

    This function reads a `.md` file from the `system_prompts` directory
    and returns its content as a string. It is used to provide system-level
    instructions or context for language models.

    Args:
        name (str, optional): The filename of the system prompt to load.
                              Defaults to "version1.md".

    Returns:
        str: The content of the system prompt file.

    Raises:
        FileNotFoundError: If the specified file does not exist in the
                           `system_prompts` directory.
    """
    base_path = os.path.dirname(__file__)       # folder: /system_prompts
    file_path = os.path.join(base_path, name)   # version1.md

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"System prompt '{name}' not found.")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
