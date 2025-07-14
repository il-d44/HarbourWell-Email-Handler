import os
import sys
from typing import TYPE_CHECKING

# Add parent directory to fix import issues
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pipeline.global_state import Global_State

if TYPE_CHECKING:
    from utils.gemini_client import GeminiClient


class DraftResponseAgent:
    """
    Agent responsible for drafting an email reply using retrieved RAG chunks and email content.
    
    Prompt is engineered to esure response is warm, professional, and context-aware.
    """
    def __init__(self, llm_client: "GeminiClient"):
        """
        Initialize the agent with a language model client.

        :param llm_client: A GeminiClient instance with a `.generate(prompt: str)` method.
        """
        self.llm = llm_client

    def draft_response(self, state: "Global_State") -> "Global_State":
        """
        Drafts a response to the email based on the retrieved chunks and email data in the global state.

            :param state: The global state containing the email data and retrieved chunks
            :return: The updated global state with the drafted response (string) and status (string)
        """
        if not state.email:
            raise ValueError("No email data found in the state")
        if not state.retrieved_chunks:
            raise ValueError("No retrieved chunks found in the state")

        context_text = (
            "\n\n".join(state.retrieved_chunks) if state.retrieved_chunks else ""
        )

        prompt = f"""
        You are an assistant at a mental health organisation named HarbourWell.
        Based on the email below, and context, write a polite and helpful response.
        
        Email Subject: {state.email['subject']}
        Email Snippet: {state.email['snippet']}
        
        {"Relevant context:" if context_text else ""} {context_text}
        
        Please respond in a warm, professional tone. You can sign off with "Best regards, HarbourWell Team".
        """
        try:
            response = self.llm.generate(
                prompt
            )  # use llm_client to generate the response
            state.draft_reply = response
            state.status = "response_drafted"
            return state
        except Exception as e:
            raise Exception("Failed to draft response via API") from e
