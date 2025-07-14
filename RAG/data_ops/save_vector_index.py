"""
This script loads previously embedded service chunks from a JSONL file,
creates a FAISS index for fast similarity search, and saves both the index
and associated metadata for use in retrieval pipelines.
"""

import json
import os
import sys
import faiss

# Add parent directory to sys.path to allow imports from core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from rag.core.embedding_vector_store import create_faiss_index_from_services

# --------------------------------------------------
# Load embedded service chunks from JSONL file
# --------------------------------------------------
chunks = []
with open("harbourwell_mock_data/service_chunks.jsonl", "r") as f:
    for line in f:
        chunks.append(json.loads(line))

# --------------------------------------------------
# Create FAISS index and metadata mapping
# --------------------------------------------------
index, id_to_metadata = create_faiss_index_from_services(chunks)

# --------------------------------------------------
# Save index and metadata to disk
# --------------------------------------------------

# Save the FAISS index to file for fast vector search
faiss.write_index(index, "harbourwell_mock_data/service_index.index")

# Save the ID-to-metadata mapping for retrieval reference
with open("harbourwell_mock_data/id_to_metadata.json", "w") as f:
    json.dump(id_to_metadata, f, indent=2)

