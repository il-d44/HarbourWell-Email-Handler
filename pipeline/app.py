import streamlit as st
import sys
import os

# Add parent directory to fix import issues
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import core pipeline and agent classes
from pipeline.global_state import Global_State
from pipeline.supervisor import run_supervisor_step
from agents.inbox_agent import InboxAgent
from agents.classify_agent import ClassifyAgent
from agents.rag_agent import RAGAgent
from agents.draft_response_agent import DraftResponseAgent
from utils.gemini_client import GeminiClient
from utils.gemini_embedding_client import GeminiEmbeddingClient

# Initialize LLM and embedding clients
llm_client = GeminiClient()
embedder = GeminiEmbeddingClient()

# Initialize LLM and embedding clients
inbox_agent = InboxAgent()
classifier_agent = ClassifyAgent(llm_client)
rag_agent = RAGAgent(embedder)
draft_agent = DraftResponseAgent(llm_client)

# Initialize or retrieve shared Streamlit session state variables
# emails: list of unread emails fetched from inbox_agent
# index: current email index being viewed
# state: global pipeline state for the current email processing
if 'emails' not in st.session_state:
    st.session_state.emails  = inbox_agent.get_unread_emails()
if 'index' not in st.session_state:
    st.session_state.index = 0 
if 'state' not in st.session_state:
    st.session_state.state = Global_State()

# Convenience references to session state variables
emails = st.session_state.emails
index = st.session_state.index
state = st.session_state.state

# If no emails are found, inform the user
if not emails:
    st.write("No unread emails found.")
else:
    # Select the current email by index and update global state
    current_email =  emails[index]
    state.email = current_email
    state.status = "email_unprocessed"

    # Run the pipeline supervisor step to process the current email
    state = run_supervisor_step(state, classifier_agent, rag_agent, draft_agent)

    # If the email is classified as a routine enquiry, show relevant UI elements
    if state.category == 'routine enquiry':

        # Display basic email details in the app
        st.header("Email Preview")
        st.markdown(f"From: {state.email['from']}")
        st.markdown(f"Subject: {state.email['subject']}")
        st.markdown(f"Body: {state.email['snippet']}")

        # If a draft reply has been generated, display it
        if state.status == 'response_drafted':
            st.header("Drafted Response")        
            st.markdown(f"{state.draft_reply}")

        # Display Approve and Reject buttons for user feedback
        approve = st.button("Approve Response", key="approve_button")
        reject = st.button("Reject Response", key="next_email_button")

        # If user approves or rejects, move to next email and show confirmation
        if approve:
            st.session_state.update({'index': (st.session_state.index + 1) % len(emails)})
            st.success("Response approved. Moving to next email.")
        elif reject:
            st.session_state.update({'index': (st.session_state.index + 1) % len(emails)})
            st.success("Response rejected. Moving to next email.")

            # Draft response not ready yet — could happen if processing is slow or incomplete
        else:
            print("Draft response not available yet.")
            
    else:
        # For categories other than routine enquiry, display placeholder text
        st.write(f"Logic for category:{state.category} not yet implemented")
        # Provide a button to move to the next email in the list
        st.button("Next Email", on_click=lambda: st.session_state.update({'index': (st.session_state.index + 1) % len(emails)}))

                    



    