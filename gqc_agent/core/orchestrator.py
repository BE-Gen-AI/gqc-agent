import json
import threading
from gqc_agent.core._llm_models.gpt_models import list_gpt_models
from gqc_agent.core._llm_models.gemini_models import list_gemini_models
from gqc_agent.core._validations.input_validator import validate_input
from gqc_agent.core._validations.model_validator import validate_model
from gqc_agent.core._intent_classifier.classifier import classify_intent
from gqc_agent.core._query_rephraser.rephraser import rephrase_query
from gqc_agent.core._note_creator.note_creator import create_note
from gqc_agent.core._system_prompts.loader import load_system_prompt
from gqc_agent.core._constants.constants import CURRENT, HISTORY, ROLE, USER, QUERY


class AgentPipeline:
    """
    Orchestrator class for running multiple agents (Intent Classifier, Query Rephraser, Note Creator)
    using a specified LLM model (GPT or Gemini) and API key.

    Attributes:
        api_key (str): API key for the selected LLM provider.
        model (str): Name of the model to use.
    """
    def __init__(self, api_key: str, model: str, provider: str):
        """
        Initialize the AgentPipeline with API key and model name.

        Args:
            api_key (str): OpenAI or Gemini API key.
            model (str): Model name to be used with the API key.
            provider (str): LLM provider, must be either "gpt" or "gemini".
        """
        self.api_key = api_key
        self.model = model
        self.provider = provider

    def get_supported_models(self):
        """
        Fetch the list of supported models for the given API key.

        Args:
            provider (str): LLM provider, either "gpt" or "gemini".
            api_key (str): The API key for GPT or Gemini.

        Returns:
            list: Supported model names. Returns empty list if error occurs.
        """
        try:
            if self.provider.lower() == "gpt":
                return list_gpt_models(self.api_key)
            elif self.provider.lower() == "gemini":
                return list_gemini_models(self.api_key)
            else:
                raise ValueError("Provider must be either 'gpt' or 'gemini'")
        except Exception as e:
            print(f"Error fetching supported models: {e}")
            return []
        
    @classmethod
    def show_system_prompt(cls, filename="default_prompt.md"):
        """
        Load and return the content of a system prompt file.

        Args:
            filename (str): Name of the system prompt file in /system_prompts.
                            Examples: "intent_classifier.md", "note_creator.md", "query_rephraser.md".

        Returns:
            str: File content. Returns empty string if file not found or error occurs.
        """
        try:
            content = load_system_prompt(filename)
            return content
        except FileNotFoundError:
            print(f"System prompt file '{filename}' not found.")
            return ""
        except Exception as e:
            print(f"Error loading system prompt: {e}")
            return ""

    def run_gqc(self, user_input: dict):
        """
        Run all agents in parallel threads and return combined results.

        Steps:
            1. Validate main user input.
            2. Validate model selection.
            3. Prepare inputs for agents:
                - Intent Classifier & Query Rephraser get only current + history of user messages.
                - Note Creator gets full user input.
            4. Execute agents in parallel threads:
                - classify_intent
                - rephrase_query
                - create_note
            5. Merge agent results into a single dictionary.

        Args:
            user_input (dict): Structured user input including:
                {
                    "input": str,
                    "current": {"role": "user", "query": str, "timestamp": str},
                    "history": [{"role": "user"/"assistant", "query"/"response": str, "timestamp": str}, ...]
                }

        Returns:
            dict: Combined output from all agents:
                {
                    "intent": str | None,
                    "rephrased_queries": list | None,
                    "notes": str | None
                }
                Each field is None if the corresponding agent failed.
        """
        # -----------------------------
        # Step 1: Validate main input
        # -----------------------------
        try:
            validate_input(user_input)
        except ValueError as ve:
            print(f"Input validation failed: {ve}")
            return {"error": "Invalid input format"}

        # -----------------------------
        # Step 2: Validate model
        # -----------------------------
        try:
            validate_model(self.model, self.api_key, self.provider)
            
        except ValueError as ve:
            print(f"Model validation failed: {ve}")
            return {"error": "Invalid model selection"}
        except Exception as e:
            print(f"Unexpected error during model validation: {e}")
            return {"error": "Internal error validating model"}

        # -----------------------------
        # Step 3: Prepare agent inputs
        # -----------------------------
        # Intent Classifier & Query Rephraser get only current + history
        agent_input = {
            CURRENT: user_input[CURRENT],
            HISTORY: [h for h in user_input.get(HISTORY, []) if h[ROLE] == USER]
        }

        # Note Creator gets full input
        note_creator_input = user_input

        # -----------------------------
        # Step 4: Thread results storage
        # -----------------------------
        results = {
            "intent_classifier": None,
            "query_rephraser": None,
            "note_creator": None
        }

        # -----------------------------
        # Step 5: Define threads
        # -----------------------------
        def run_intent():
            try:
                results["intent_classifier"] = classify_intent(agent_input, self.model, self.api_key, self.provider)
            except Exception as e:
                print(f"Intent classification error: {e}")
                results["intent_classifier"] = {"intent": None}
            
        def run_rephrase():
            try:
                results["query_rephraser"] = rephrase_query(agent_input, self.model, self.api_key, self.provider)
            except Exception as e:
                print(f"Query rephrasing error: {e}")
                results["query_rephraser"] = {"rephrased_queries": None}
                
        def run_note():
            try:
                results["note_creator"] = create_note(note_creator_input, self.model, self.api_key, self.provider)
            except Exception as e:
                print(f"Note creation error: {e}")
                results["note_creator"] = {"notes": None}

        # -----------------------------
        # Step 6: Create threads objects
        # -----------------------------
        t1 = threading.Thread(target=run_intent)
        t2 = threading.Thread(target=run_rephrase)
        t3 = threading.Thread(target=run_note)


        # -----------------------------
        # Step 6: Start threads
        # -----------------------------
        t1.start()
        t2.start()
        t3.start()

        # -----------------------------
        # Step 7: Join threads
        # -----------------------------
        t1.join()
        t2.join()
        t3.join()

        # -----------------------------
        # Step 8: Merge results
        # -----------------------------
        try:
            final_output = {
                "intent": results["intent_classifier"].get("intent") if results["intent_classifier"] else None,
                "rephrased_queries": results["query_rephraser"].get("rephrased_queries") if results["query_rephraser"] else None,
                "notes": results["note_creator"].get("notes") if results["note_creator"] else None
            }
        except Exception as e:
            print(f"Error merging results: {e}")
            final_output = {
                "intent": None,
                "rephrased_queries": None,
                "notes": None
            }


        return final_output


# -----------------------
# Quick CLI test
# -----------------------
# if __name__ == "__main__":
#     sample_input = {
#         "input": "i want to add department with the name HR",
#         "current": {"role": "user", "query": "i want to add department with the name HR", "timestamp": "2025-01-01 12:30:45"},
#         "history": [
#             {"role": "user", "query": "i want to add department with the name medical", "timestamp": "2025-01-01 12:00:00"},
#             {"role": "assistant", "response": "department name is medical, but provide me the description, and active status to add department.", "timestamp": "2025-01-01 12:01:10"},
#             {"role": "user", "query": "Is PHP still useful?", "timestamp": "2025-01-01 12:02:00"},
#             {"role": "assistant", "response": "Yes, PHP is still widely used, especially for WordPress and backend APIs.", "timestamp": "2025-01-01 12:03:22"}
#         ]
#     }

#     openai_api_key = os.getenv("OPENAI_API_KEY")
#     if not openai_api_key:
#         raise ValueError("API key missing. Set OPENAI_API_KEY in .env.")
#     model = "gpt-4o-mini"  
#     orch = AgentPipeline(api_key=openai_api_key, model=model)
    
    # gemini_api_key = os.getenv("GEMINI_API_KEY")
    # if not gemini_api_key:
    #     raise ValueError("API key missing. Set GEMINI_API_KEY in .env.")
    # model = "models/gemini-2.5-flash"
    # orch = AgentPipeline(api_key=gemini_api_key, model=model)
    
    # output = orch.run_gqc(sample_input)
    # print(json.dumps(output, indent=2))
