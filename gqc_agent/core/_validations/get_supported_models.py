from difflib import get_close_matches
from gqc_agent.core._llm_models.gpt_models import GPT_SUPPORTED_MODELS
from gqc_agent.core._llm_models.gemini_models import GEMINI_SUPPORTED_MODELS

def get_supported_models(models='__all__'):
    """
    Return a list of supported models based on the input category.

    This function can return:
        - Only GPT models
        - Only Gemini models
        - All models (both GPT + Gemini)

    If the user provides an invalid option, it suggests the closest valid choice.

    Args:
        models (str, optional): Category of models to return. Options are:
            - 'gpt'     : return only GPT models
            - 'gemini'  : return only Gemini models
            - '__all__' : return all supported models (default)

    Returns:
        list[str]: A list of supported model names according to the selected category.

    Raises:
        ValueError: If the input `models` is invalid. Provides a suggested correct option
                    if a close match is found.
    """
    valid_options = ['gpt', 'gemini', '__all__']
    if models not in valid_options:
        # Suggest closest match
        suggestion = get_close_matches(models, valid_options, n=1)
        if suggestion:
            raise ValueError(f"Invalid option '{models}'. Did you mean '{suggestion[0]}'?")
        else:
            raise ValueError(f"Invalid option '{models}'. Valid options are: {valid_options}")
        
        # return corresponding models
    if models == 'gpt':
        return GPT_SUPPORTED_MODELS
    elif models == 'gemini':
        return GEMINI_SUPPORTED_MODELS
    elif models == '__all__':
        return GPT_SUPPORTED_MODELS + GEMINI_SUPPORTED_MODELS
    else:
        raise ValueError(f"Invalid option '{models}'")