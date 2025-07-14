from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pipeline.global_state import Global_State
    from agents.classify_agent import ClassifyAgent
    from agents.rag_agent import RAGAgent
    from agents.draft_response_agent import DraftResponseAgent

def run_supervisor_step(
    state: "Global_State",
    classify_agent: "ClassifyAgent",
    rag_agent: "RAGAgent",
    draft_response_agent: "DraftResponseAgent",
) -> "Global_State":
    """
    Supervises a single step in the email processing pipeline by coordinating 
    classification, chunk retrieval, and draft response generation.

    This function is intended to be called iteratively in the main application loop.
    It updates the pipeline state based on the current processing status.

    Args:
        state (Global_State): Current global state of the pipeline.
        classify_agent (ClassifyAgent): Agent responsible for classifying the email.
        rag_agent (RAGAgent): Agent responsible for retrieving relevant text chunks.
        draft_response_agent (DraftResponseAgent): Agent responsible for drafting the email reply.

    Returns:
        Global_State: Updated state after processing this step.
    """
    if state.status == "email_unprocessed":
        # Classify the email to determine the category
        state = classify_agent.classify_email(state)

        if state.status == "classified":
            if state.category == "routine enquiry":
                # Retrieve relevant chunks for routine enquiries
                state.status = "retrieving_chunks"
                state = rag_agent.retrieve_relevant_chunks(state)

                # If chunks are retrieved, draft a response
                if state.status == "chunks_retrieved":
                    # Draft the response based on retrieved chunks
                    state = draft_response_agent.draft_response(state)
            else:
                # Placeholder for other category handling logic
                state.status = "skipped"
                print("Category logic not yet implemented")

    else:
        # Unexpected status indicates a processing error
        state.error == "Unexpected status when attepting to categorise email"
        print("Error: Unexpected status when attepting to categorise email")

    return state
