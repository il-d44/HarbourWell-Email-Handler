import os
import sys
from typing import Callable

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline.global_state import Global_State 
from agents.classify_agent import classify_email
from agents.draft_response_agent import draft_response

"""This supervisor function uses logical conditions to execute individual nodes in the desired order"""
def supervisor_tdd(
    state: Global_State,
    classify_fn: Callable[[Global_State], Global_State],
    draft_fn: Callable[[Global_State], Global_State]
):    
    if state.status == 'start':
        print("Email is being classified...")
        state = classify_fn(state)

    if state.status == 'classified':
        print(f"Category: {state.category}")
        print("Generating response...")
        state = draft_fn(state)
    

    
        

