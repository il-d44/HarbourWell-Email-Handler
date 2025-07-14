from dataclasses import dataclass
from typing import Optional

@dataclass
class Global_State:
    """
    Represents the shared state throughout the email processing pipeline.

    Attributes:
        email (Optional[dict]): The current email data being processed.
        category (Optional[str]): The classification category assigned to the email.
        retrieved_chunks (Optional[List[str]]): List of relevant text chunks retrieved from the RAG index.
        draft_reply (Optional[str]): Generated draft response for the email.
        status (Optional[str]): Current processing status (e.g., 'start', 'classified', 'response_drafted').
        error (Optional[str]): Error message if any failure occurs during processing.
    """

    email: Optional[dict] = None
    category: Optional[str] = None
    retrieved_chunks: Optional[list] = None
    draft_reply: Optional[str] = None
    status: Optional[str] = "start"
    error: Optional[str] = None
