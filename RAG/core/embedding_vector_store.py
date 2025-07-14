"""
This module handles embedding text chunks, creating a FAISS index from them,
and querying the index for the most relevant matches using vector similarity.
"""

import numpy as np
import faiss
import os
import sys
from typing import List, Tuple, Dict, Any


# Add parent directory to fix import issues
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.gemini_embedding_client import GeminiEmbeddingClient


def embed_chunks(service_chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate embeddings for each text chunk using the GeminiEmbeddingClient.

    Args:
        service_chunks (list): List of dictionaries, each with 'text' and 'metadata'.

    Returns:
        list: List of dictionaries, each with 'embedding', 'text', and 'metadata'.
    """
    client = GeminiEmbeddingClient()
    embedded = []

    for chunk in service_chunks:
        embedded.append({
            "embedding": client.embed(chunk["text"]),
            "text": chunk["text"],
            "metadata": chunk["metadata"],
        })

    return embedded



def create_faiss_index_from_services(
    chunks: List[Dict[str, Any]]
) -> Tuple[faiss.IndexFlatL2, List[Dict[str, Any]]]:
    """
    Create a FAISS index from embedded service chunks.

    Args:
        chunks (list): List of dictionaries with 'embedding', 'text', and 'metadata'.

    Returns:
        tuple: (FAISS index, List of ID-to-metadata mappings)
    """
    all_embeddings = [chunk["embedding"] for chunk in chunks]
    id_to_metadata = [{
        "embedding": chunk["embedding"],
        "text": chunk["text"],
        "metadata": chunk["metadata"]
    } for chunk in chunks]

    embedding_matrix = np.array(all_embeddings).astype("float32")
    dimension = embedding_matrix.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embedding_matrix)  # type: ignore

    return index, id_to_metadata



