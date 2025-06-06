# pyright: ignore
import google.generativeai as genai
from dotenv import load_dotenv  
import os
load_dotenv()  # Load environment variables from .env file

"""A client for interacting with the Gemini API for text generation."""
class GeminiClient:
    def __init__(self, api_key = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in GEMINI_API_KEY environment variable")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()