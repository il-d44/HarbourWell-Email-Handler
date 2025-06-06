import google.generativeai as genai
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pipeline.global_state import Global_State



# Load variables from .env file
load_dotenv()

# Get the API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-pro-latest') 


def draft_response(state: Global_State):
    email_text = state.email_body
    classified_category = state.category

    prompt = f"""
    You are an assistant that drafts email replies to customer enquiries.

    A customer has sent the following email:
    \"\"\" 
    {email_text}
    \"\"\"

    This email has been classified as: {classified_category}

    Based on this, write a professional, helpful, and concise email reply.
    The reply should:
    - Match the tone of a professional organisation.
    - Directly address the concern raised.
    - Offer relevant help, information, or next steps.
    - Avoid unnecessary repetition or filler.

    Do not include anything except the drafted email text.
    """

    response = model.generate_content(prompt)
    drafted_email = response.text
    state.draft_reply = drafted_email
    state.status = 'draft_ready'
    return state



email_text = {
    "Subject: Career Switch Advice\nCan your courses help someone transition from marketing to tech? – Jasmine L.",
  }
