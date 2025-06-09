import os
import sys
from typing import TYPE_CHECKING


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pipeline.global_state import Global_State
if TYPE_CHECKING:
    from utils.gemini_client import GeminiClient

class DraftResponseAgent:
    def __init__(self, llm_client: "GeminiClient"):
        self.llm = llm_client

    def draft_response(self, state: "Global_State") -> "Global_State":
        if not state.email:
            raise ValueError("No email data found in the state")
        if not state.retrieved_chunks:
            raise ValueError("No retrieved chunks found in the state")
        
        context_text = "\n\n".join(state.retrieved_chunks) if state.retrieved_chunks else ""

        prompt = f"""
        You are an assistant at a mental health organisation.
        Based on the email below, and context, write a polite and helpful response.
        
        Email Subject: {state.email['subject']}
        Email Snippet: {state.email['snippet']}
        
        {"Relevant context:" if context_text else ""} {context_text}
        
        Please respond in a warm, professional tone.
        """
        try:
            response = self.llm.generate(prompt) # use llm_client to generate the response
            state.draft_reply = response
            state.status = 'response_drafted'
            return state   
        except Exception as e: 
            raise Exception("Failed to draft response via API") from e




from utils.gemini_client import GeminiClient
llm_client = GeminiClient()  
draft_agent = DraftResponseAgent(llm_client)
state = Global_State(email={'subject': 'Mental Health Services Inquiry', 'snippet': 'What services are available for depression in Broxbourne?'}, 
             category=None, 
             retrieved_chunks=['The Depression Support group meets at the Broxbourne every Monday from 6:30pmâ€“8:00pm.Depression Support is a support group for individuals experiencing depression, offering peer-led discussion and coping strategies..', 'The Broxbourne centre is located at Broxbourne Community Centre, 1 High Street, Broxbourne, EN10 7HX. Services offered include: Depression Support, Anxiety Support, Bipolar Support, LGBTQ+ Support, Carers Support, Cognitive Behavioral Therapy (CBT), Psychodynamic Counselling, Intergrative Counselling, Mindfulness-Based Therapy.You can contact the Broxbourne centre by calling 01279 123456 or emailing broxboure_centre@harbourwell.org.uk.', 'Cognitive Behavioral Therapy (CBT) counselling service is available at the Broxbourne centre. It is available Monday to Friday, 9:00amâ€“5:00pm. CBT is a structured, time-limited therapy that helps individuals identify and change negative thought patterns and behaviors..'], draft_reply=None, status='chunks_retrieved', error=None)
drafted_state = draft_agent.draft_response(state)
print(drafted_state.draft_reply)  # Output the drafted response