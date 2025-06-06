from google import genai
from dotenv import load_dotenv  
import os
load_dotenv()  # Load environment variables from .env file

"""A client for interacting with the Gemini API for text embeddings."""
class GeminiEmbeddingClient:
    def __init__(self, api_key = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in GEMINI_API_KEY environment variable")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-embedding-exp-03-07"
    
    def embed(self, text: str) -> list[float]:
        """
        Embed a single string of text.
        """
        result = self.client.models.embed_content(
            model=self.model_name,
            contents=text,
        )
        return result.embeddings[0].values
        
text = "This is a sample text to be embedded."
if __name__ == "__main__":
    client = GeminiEmbeddingClient()
    embedding = client.embed(text)
    print(f"Embedding for the text: {embedding}")