"""
Script to convert structured service data into embedded text chunks
and save them in JSONL format for use in a vector search pipeline.
""" 
import json
import os
import sys

# Add parent directory to sys.path to allow importing project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import functions for creating and embedding text chunks
from rag.core.create_chunks import create_chunks_with_metadata
from rag.core.embedding_vector_store import embed_chunks

# -----------------------------
# Load service data from JSON
# -----------------------------

# Load structured service data (e.g., mental health centres, support groups, etc.)
with open("harbourwell_mock_data/services.json", "r") as f:
    service_data = json.load(f)

# --------------------------------------------
# Generate, flatten, and embed text chunks
# --------------------------------------------

# Convert each service entry into text chunks with metadata
service_chunks = [create_chunks_with_metadata(service) for service in service_data]

# Flatten the list of chunk lists into a single list of chunk dictionaries
flattened_service_chunks = [chunk for service in service_chunks for chunk in service]

# Use Gemini embeddings to convert text chunks into vector embeddings
embedded_chunks = embed_chunks(flattened_service_chunks)

# --------------------------------------------
# Save embedded chunks to a JSONL file
# --------------------------------------------

# Write each embedded chunk (with metadata and vector) to a new line in JSONL format
with open("harbourwell_mock_data/service_chunks.jsonl", "w") as f:
    for chunk in embedded_chunks:
        json.dump(chunk, f, separators=(",", ":"))  # Compact JSON formatting
        f.write("\n")
