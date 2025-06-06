import json
import os
import sys
import faiss
# Ensure the parent directory is in the path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from RAG.core.embedding_vector_store import create_faiss_index_from_services

# load the saved embedded chunks from the JSONL file
chunks = []
with open("service_data/service_chunks.jsonl", "r") as f:
    for line in f:
        chunks.append(json.loads(line))


# create the FAISS index from the embedded chunks
index, id_to_metadata = create_faiss_index_from_services(chunks)
# save the FAISS index to a file
faiss.write_index(index, "service_data/service_index.index")
# save the metadata to a JSON file
with open("service_data/id_to_metadata.json", "w") as f:
    json.dump(id_to_metadata, f, indent=2)

    
