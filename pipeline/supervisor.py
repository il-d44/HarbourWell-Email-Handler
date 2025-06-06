import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline.global_state import Global_State 
from agents.classify_agent import classify_email
from agents.draft_response_agent import draft_response

"""This supervisor function uses logical conditions to execute individual nodes in the desired order"""
def supervisor(state: Global_State):
    try:
        # Classify email node
        if state.status == "start":
            print("Classifying email...")
            state = classify_email(state)
        # Draft response node 
        if state.status == "classified":
            print(f"Category: {state.category}")
            print("Generating draft response...")
            state = draft_response(state)

        # Trigger human review
        if state.status == "draft_ready":
            print("Draft ready for review:")
            print("→", state.draft_reply)
            state.status = "awaiting_approval"

            # Ask user for approval
            while True:
                decision = input("Do you want to send this draft? Type 'yes' to approve or 'no' to reject: ").strip().lower()
                if decision in ['yes', 'no']:
                    break
                print("Please enter 'yes' or 'no'.")

            if decision == "yes":
                state.status = "approved"
                print("✅ Email sent!")
            else:
                state.status = "rejected"
                print("💾 Email saved to drafts.")


        

    except Exception as e:
        state.error = str(e)
        state.status = "error"
        print("Error occurred:", e)


state = Global_State(
    email_body="Hi, I'd like to know more about your courses, please send me some info.",
    status="start"
)

supervisor(state)