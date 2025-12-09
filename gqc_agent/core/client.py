import json
import threading
import os
from dotenv import load_dotenv
from gqc_agent.core._llm_models.gpt_models import list_gpt_models
from gqc_agent.core._llm_models.gemini_models import list_gemini_models
from gqc_agent.core._validations.input_validator import validate_input
from gqc_agent.core._validations.model_validator import validate_model
from gqc_agent.core.intent_classifier.classifier import classify_intent
from gqc_agent.core.query_rephraser.rephraser import rephrase_query
from gqc_agent.core.note_creator.note_creator import create_note
from gqc_agent.core.system_prompts.loader import load_system_prompt

load_dotenv()


class AgentPipeline:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    @classmethod
    def get_supported_models(cls, api_key: str):
        """
        Get supported models based on the provided API key.

        Args:
            api_key (str): The API key for the model provider.

        Returns:
            list: List of supported model names.
        """

        if api_key == os.getenv("OPENAI_API_KEY"):
            return list_gpt_models(api_key)
        elif api_key == os.getenv("GEMINI_API_KEY"):
            return list_gemini_models(api_key)
        else:
            raise ValueError("No valid API key provided or unknown model provider")
        
    @classmethod
    def show_system_prompt(cls, filename="default_prompt.md"):
        """
        Display the content of a system prompt file to the user.

        Args:
            filename (str): Name of the system prompt file in /system_prompts
            Sample filename : "intent_classifier.md", "note_creator.md", query_rephraser.md", etc.
        Returns:
            str: The content of the system prompt
        """
        content = load_system_prompt(filename)
        return content

    def run_gqc(self, user_input: dict):
        # -----------------------------
        # Step 1: Validate main input
        # -----------------------------
        validate_input(user_input)

        # -----------------------------
        # Step 2: Validate model
        # -----------------------------
        validate_model(self.model, self.api_key)

        # -----------------------------
        # Step 3: Prepare agent inputs
        # -----------------------------
        # Intent Classifier & Query Rephraser get only current + history
        agent_input = {
            "current": user_input["current"],
            "history": [h for h in user_input.get("history", []) if h["role"] == "user"]
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
            results["intent_classifier"] = classify_intent(agent_input, self.model, self.api_key)

        def run_rephrase():
            results["query_rephraser"] = rephrase_query(agent_input, self.model, self.api_key)

        def run_note():
            results["note_creator"] = create_note(note_creator_input, self.model, self.api_key)


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
        final_output = {
            "intent": results["intent_classifier"].get("intent") if results["intent_classifier"] else None,
            "rephrased_queries": results["query_rephraser"].get("rephrased_queries") if results["query_rephraser"] else None,
            "notes": results["note_creator"].get("notes") if results["note_creator"] else None
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
