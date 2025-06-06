import json
import os
import sys  
# Ensure the parent directory is in the path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RAG.core.create_chunks import create_chunks_with_metadata
from RAG.core.embedding_vector_store import embed_chunks


# Load your JSON data (replace this with your actual JSON loading method)
with open("service_data/services.json", "r") as f:
    service_data = json.load(f)

# Generate chunks
service_chunks = [create_chunks_with_metadata(service) for service in service_data]
# Flatten the list of chunks
flattened_service_chunks = [chunk for service in service_chunks for chunk in service]
# Embed the chunks
embedded_chunks = embed_chunks(flattened_service_chunks)
# Save the embedded chunks to a JSONL file
with open("service_data/service_chunks.jsonl", "w") as f:
    for chunk in embedded_chunks:
        json.dump(chunk, f, separators=(',', ':'))
        f.write("\n")