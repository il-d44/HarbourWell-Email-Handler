import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pipeline.global_state import Global_State
from agents.exceptions import EmailClassificationAPIError




class ClassifyAgent:
    def __init__(self, llmclient):
        self.llm = llmclient

    def classify_email(self, state: "Global_State") -> "Global_State":
        if not state.email:
            raise ValueError("No email data found in the state")
        
        prompt = f"""
        You are an assistant for a Mental Health Wellbeing organisation that classifies emails into categories.
        Classify the following email into one of the categories below.

        Email:
        \"\"\"
        Subject: {state.email['subject']}
        Body: {state.email['snippet']}
        \"\"\"

        VALID_CATEGORIES = [
            "routine enquiry",
            "referrals",
            "other",
        ]

        Please respond with exactly one of the categories listed and nothing else.
        """
        try:
            response = self.llm.generate(prompt)
            classified_category = response
            state.category = classified_category
            state.status = 'classified'
            return state
        except Exception as e:
            raise EmailClassificationAPIError("Failed to classify email via API") from e
        

