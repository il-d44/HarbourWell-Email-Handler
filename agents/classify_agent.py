import os
import sys

# Add parent directory to fix import issues
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pipeline.global_state import Global_State
from agents.exceptions import EmailClassificationAPIError




class ClassifyAgent:
    """
    Agent for classifying incoming emails into predefined categories using an LLM.

    Categories include:
    - "routine enquiry"
    - "referrals"
    - "other"

    This agent updates the shared Global_State with the classification result.
    """

    def __init__(self, llm_client):
        """
        Initialize the agent with using language model client.

        :param llm_client: A GeminiClient instance with a `.generate(prompt: str)` method.
        """
        self.llm = llm_client

    def classify_email(self, state: "Global_State") -> "Global_State":
        """
        Use an LLM to classify the email stored in the global state.

        :param state: Global_State instance containing the current email
        :return: The updated Global_State with .category and .status set
        :raises ValueError: If no email is present in state
        :raises EmailClassificationAPIError: If the LLM call fails
        """
        if not state.email:
            raise ValueError("No email data found in the state")

        prompt = f"""
        You are an assistant for a mental health wellbeing organisation that classifies emails into categories.
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
            state.status = "classified"
            return state
        except Exception as e:
            raise EmailClassificationAPIError("Failed to classify email via API") from e
