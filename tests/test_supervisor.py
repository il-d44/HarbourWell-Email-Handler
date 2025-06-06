import unittest
from unittest.mock import patch
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline.global_state import Global_State
from pipeline.supervisor_tdd import supervisor_tdd

class TestSupervisor(unittest.TestCase):

    def test_classify_email_only(self):
        """
        Unit test for the classification step of the supervisor_tdd function.

        This test verifies that when the initial state has status 'start',
        and the classify_fn is a mock that sets the status to 'classified',
        the supervisor_tdd function correctly calls classify_fn and updates
        the state accordingly.

        The draft_fn is mocked as a no-op (does nothing) to isolate the test
        to the classification logic only.
        """
        def mock_classify(state):
            state.status = "classified"
            return state
        
        state = Global_State()
        
        supervisor_tdd(state, classify_fn=mock_classify, draft_fn=lambda s: s)
        
        self.assertEqual(state.status, "classified")

    def test_draft_response_only(self):
        """
        Unit test for the draft response step of the supervisor_tdd function.

        This test verifies that when the initial state has status 'classified',
        and the draft_fn is a mock that sets the status to 'draft_ready' and
        provides a draft reply, the supervisor_tdd function correctly calls
        draft_fn and updates the state accordingly.

        The classify_fn is mocked as a no-op (does nothing) to isolate the test
        to the drafting logic only.
        """
        def mock_draft(state):
            state.status = "draft_ready"
            state.draft_reply = "draft"
            return state
        
        state = Global_State()
        state.status = "classified"
        
        supervisor_tdd(state, classify_fn=lambda s: s, draft_fn=mock_draft)
        
        self.assertEqual(state.status, "draft_ready")
        self.assertEqual(state.draft_reply, "draft")


if __name__ == '__main__':
    unittest.main()