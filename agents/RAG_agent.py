import os
import sys
import faiss
import json
from typing import List
import numpy as np

# Add parent directory to fix import issues
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pipeline.global_state import Global_State
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.gemini_embedding_client import GeminiEmbeddingClient


"""
RAGAgent class for retrieving relevant chunks from a vector index based on email data.
This class uses:
- Gemini's embedding model to embed the email subject and snippet
- Loads a pre-saved FAISS index
- Retrieves the top-k relevant chunks based on the embedded query
- Updates the global state with the retrieved chunks
"""


class RAGAgent:
    """
    RAGAgent retrieves contextually relevant text chunks from a FAISS vector index
    using the subject and snippet of an email as the query.

    It uses:
    - A Gemini embedding model to embed the input query
    - A pre-saved FAISS index for nearest-neighbour search
    - A JSON metadata map to resolve chunk IDs to actual text
    - Updates the Global_State with retrieved chunks
    """

    def __init__(
        self,
        embedding_client: "GeminiEmbeddingClient",
        index_path: str = "harbourwell_mock_data/service_index.index",
        id_to_metadata_path: str = "harbourwell_mock_data/id_to_metadata.json",
    ):
        """
        Initializes the RAGAgent with an embedding client and paths to index and metadata files.

        :param embedding_client: GeminiEmbeddingClient used to generate query embeddings
        :param index_path: Path to the saved FAISS index file
        :param id_to_metadata_path: Path to the saved JSON file mapping vector IDs to text chunks
        """
        # Load faiss index and metadata mapping
        self.index = faiss.read_index(index_path)
        with open(id_to_metadata_path, "r", encoding="utf-8") as f:
            self.id_to_metadata: List[str] = json.load(f)
        # Store the embedding client
        self.embedding_client = embedding_client

    def embed_query(self, query: str) -> List[float]:
        """
        Embeds a query string using the embedding client.

        :param query: The input query string (e.g., email subject + snippet)
        :return: A list of floats representing the query embedding vector
        """
        return self.embedding_client.embed(query)

    def retrieve_relevant_chunks(
        self, state: Global_State, top_k: int = 3
    ) -> Global_State:
        """
        Retrieves the top-k relevant text chunks from the FAISS index
        using an embedded email query, and updates the global state.

        :param state: Global_State containing the current email
        :param top_k: Number of top chunks to retrieve (default: 3)
        :return: The updated Global_State with retrieved_chunks and status set
        :raises ValueError: If the email is missing from state
        """
        if not state.email:
            raise ValueError("No email data found in state")

        # Construct the query from the email subject and snippet
        query = state.email["subject"] + " " + state.email["snippet"]
        # Query the vector index with the query text
        query_vector = self.embed_query(query)
        query_vector_np = np.array([query_vector], dtype="float32")
        _, indices = self.index.search(query_vector_np, top_k)

        top_chunks = [self.id_to_metadata[i]["text"] for i in indices[0]]
        state.retrieved_chunks = top_chunks
        state.status = "chunks_retrieved"

        return state
