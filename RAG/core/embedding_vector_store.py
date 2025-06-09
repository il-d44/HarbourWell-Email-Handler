import numpy as np
import faiss
import os
import sys  
# Ensure the parent directory is in the path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.gemini_embedding_client import GeminiEmbeddingClient

def embed_chunks(service_chunks):
    embeddings = []
    for chunk in service_chunks:
        client = GeminiEmbeddingClient()
        embeddings.append({
            "embedding": client.embed(chunk['text']), 
            "metadata": chunk['metadata'],
            "text": chunk['text']})
    return embeddings

def create_faiss_index_from_services(chunks):
    """
    Create a FAISS index from loaded chunks.

    Args:
        chunks (list): A list of dictionaries, each containing a text chunk and its associated metadata.
    Returns:
        tuple: A tuple containing the FAISS index and a list of dictionaries mapping IDs to metadata.
     """
    all_embeddings = []
    id_to_metadata = []

    
    for chunk in chunks:
        all_embeddings.append(chunk['embedding'])
        id_to_metadata.append({
            'metadata': chunk.get('metadata'),
            'text': chunk.get('text'),
            'embedding': chunk.get('embedding') 
        })

    embedding_matrix = np.array(all_embeddings).astype('float32')
    dimension = embedding_matrix.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embedding_matrix) #type: ignore

    return index, id_to_metadata

def query_faiss_index(index, query, id_to_metadata, k=5):
    """
    Query the FAISS index with a given embedding.

    Args:
        index (faiss.Index): The FAISS index to query.
        query_embedding (list): The embedding to query the index with.
        k (int): The number of nearest neighbors to return.
    Returns:
        None: Prints the matched results and their metadata.
    """
    client = GeminiEmbeddingClient()
    query_embedding = client.embed(query)
    query_vector = np.array(query_embedding).astype('float32').reshape(1, -1)
    _, indices = index.search(query_vector, k)
    for idx in indices[0]:
        result = id_to_metadata[idx]
        print("Match:", result["text"])
        print("Metadata:", result["metadata"])
        print("-" * 50)