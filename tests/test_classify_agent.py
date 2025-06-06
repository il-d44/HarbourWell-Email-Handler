import unittest
from unittest.mock import patch
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.classify_agent import classify_email, Global_State
from agents.exceptions import EmailClassificationAPIError


class TestClassifyAgent(unittest.TestCase):
    
    @patch("agents_plain_python.classify_agent.model.generate_content")
    def test_classify_email_returns_correct_category(self,mock_generate):
            mock_generate.return_value.text = "Course Enquiries"
    
            state = Global_State(email_body="I’d like to learn more about your courses.", status="start")

            new_state = classify_email(state)
    
            self.assertEqual(new_state.category, "Course Enquiries")
            self.assertEqual(new_state.status, "classified")

    
    @patch("agents_plain_python.classify_agent.model.generate_content")
    def test_classify_email_API_call_failure_fall_back(self, mock_generate):
        mock_generate.side_effect = EmailClassificationAPIError("Failed to classify email via API")

        state = Global_State(email_body="Some email text")     

        with self.assertRaises(EmailClassificationAPIError):
            classify_email(state)
                                                   
                                                
         

if __name__ == '__main__':
    unittest.main()
