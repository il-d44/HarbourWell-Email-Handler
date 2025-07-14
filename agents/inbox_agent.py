from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build




class InboxAgent:
    """
    InboxAgent class for fetching unread emails from Gmail using the Gmail API.

    This class handles authentication via OAuth and retrieves basic information
    (subject, sender, snippet) for the most recent unread emails.
    """
    def __init__(self, token_path="secrets/token.json", scopes=None):
        """
        Initializes the InboxAgent with OAuth credentials and Gmail API client.

        :param token_path: Path to the token file containing user credentials.
        :param scopes: List of OAuth scopes. Defaults to readonly Gmail access.
        """
        self.token_path = token_path
        self.scopes = scopes or ["https://www.googleapis.com/auth/gmail.readonly"]
        self.creds = self._load_credentials()
        self.service = build("gmail", "v1", credentials=self.creds)

    def _load_credentials(self):
        """
        Loads OAuth credentials from the specified token file.

        :return: A Credentials object for Gmail API access.
        """
        return Credentials.from_authorized_user_file(self.token_path, self.scopes)

    def get_unread_emails(self):
        """
        Retrieves the most recent unread emails.

        :return: A list of dictionaries, each containing:
                 - id: the Gmail message ID
                 - snippet: a short preview of the email body
                 - subject: the subject line
                 - from: the sender's email
        """
        try:
            response = (
                self.service.users()
                .messages()
                .list(userId="me", maxResults=5)
                .execute()
            )

            message_ids = response.get("messages", [])
            emails = []

            for msg in message_ids:
                msg_data = (
                    self.service.users()
                    .messages()
                    .get(
                        userId="me",
                        id=msg["id"],
                        format="full",
                        metadataHeaders=["Subject", "From"],
                    )
                    .execute()
                )

                email_summary = {
                    "id": msg_data["id"],
                    "snippet": msg_data.get("snippet", "(No Snippet)"),
                    "subject": next(
                        (
                            h["value"]
                            for h in msg_data["payload"]["headers"]
                            if h["name"] == "Subject"
                        ),
                        "(No Subject)",
                    ),
                    "from": next(
                        (
                            h["value"]
                            for h in msg_data["payload"]["headers"]
                            if h["name"] == "From"
                        ),
                        "(No Sender)",
                    ),
                }

                emails.append(email_summary)

            return emails

        except Exception as e:
            print(f"[InboxAgent] Error fetching emails: {e}")
            return []
