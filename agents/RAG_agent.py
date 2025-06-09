import os
import sys
import faiss
import json
from typing import List 
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pipeline.global_state import Global_State
from agents.exceptions import EmailClassificationAPIError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.gemini_embedding_client import GeminiEmbeddingClient



class RAGAgent:
    def __init__(self, 
                 embedding_client: 'GeminiEmbeddingClient',
                 index_path: str = "service_data/service_index.index", 
                 id_to_metadata_path: str ="service_data/id_to_metadata.json"
                 ):
        # Load faiss index and metadata mapping
        self.index = faiss.read_index(index_path)
        with open(id_to_metadata_path, "r", encoding="utf-8") as f:
            self.id_to_metadata: List[str] = json.load(f)
        # Store the embedding client
        self.embedding_client = embedding_client

    def embed_query(self, query: str) -> List[float]:
        return self.embedding_client.embed(query)
        

    def retrieve_relevant_chunks(self, state: Global_State, top_k: int =3)-> Global_State:
        if not state.email:
            raise ValueError("No email data found in state")
        
        # Construct the query from the email subject and snippet
        query = state.email["subject"] + " " + state.email["snippet"]
        # Query the vector index with the query text
        query_vector = self.embed_query(query)
        query_vector_np = np.array([query_vector], dtype="float32")
        _, I = self.index.search(query_vector_np, top_k)

        top_chunks = [self.id_to_metadata[i]['text'] for i in I[0]]
        state.retrieved_chunks = top_chunks
        state.status = "chunks_retrieved"

        return state
            
