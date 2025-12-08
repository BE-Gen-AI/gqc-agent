import json
import threading
import os
from dotenv import load_dotenv

from gqc_agent.core._validations.input_validator import validate_input
from gqc_agent.core._validations.model_validator import validate_model
from gqc_agent.core.intent_classifier.classifier import classify_intent
from gqc_agent.core.query_rephraser.rephraser import rephrase_query
from gqc_agent.core.note_creator.note_creator import create_note

load_dotenv()


class AgentPipeline:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def run_gqc(self, user_input: dict):
        # -----------------------------
        # Step 1: Validate main input
        # -----------------------------
        validate_input(user_input)

        # -----------------------------
        # Step 2: Validate model
        # -----------------------------
        validate_model(self.model)

        # -----------------------------
        # Step 3: Prepare agent inputs
        # -----------------------------
        # Intent Classifier & Query Rephraser get only current + history
        agent_input = {
            "current": user_input["current"],
            "history": user_input.get("history", [])
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
        t1 = threading.Thread(
            target=lambda: results.update(
                intent_classifier=classify_intent(agent_input, self.model, self.api_key)
            )
        )

        t2 = threading.Thread(
            target=lambda: results.update(
                query_rephraser=rephrase_query(agent_input, self.model, self.api_key)
            )
        )

        t3 = threading.Thread(
            target=lambda: results.update(
                note_creator=create_note(note_creator_input, self.model, self.api_key)
            )
        )

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
if __name__ == "__main__":
    sample_input = {
        "input": "Tell me more about it",
        "current": {"role": "user", "query": "Tell me more about it", "timestamp": "2025-01-01 12:30:45"},
        "history": [
            {"role": "user", "query": "What is PHP?", "timestamp": "2025-01-01 12:00:00"},
            {"role": "assistant", "response": "PHP is a server-side scripting language used for web development.", "timestamp": "2025-01-01 12:01:10"},
            {"role": "user", "query": "Is PHP still useful?", "timestamp": "2025-01-01 12:02:00"},
            {"role": "assistant", "response": "Yes, PHP is still widely used, especially for WordPress and backend APIs.", "timestamp": "2025-01-01 12:03:22"}
        ]
    }

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("API key missing. Set OPENAI_API_KEY in .env.")
    model = "gpt-4o-mini"  
    orch = AgentPipeline(api_key=openai_api_key, model=model)
    
    # gemini_api_key = os.getenv("GEMINI_API_KEY")
    # if not gemini_api_key:
    #     raise ValueError("API key missing. Set GEMINI_API_KEY in .env.")
    # model = "models/gemini-2.5-flash"
    # orch = AgentPipeline(api_key=gemini_api_key, model=model)
    
    output = orch.run_gqc(sample_input)
    print(json.dumps(output, indent=2))
