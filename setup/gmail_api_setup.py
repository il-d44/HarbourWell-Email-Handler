import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_credentials():
    creds = None

    # Check if token already exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If token is missing or invalid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Load credentials from environment
            credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
            if not credentials_path or not os.path.exists(credentials_path):
                raise EnvironmentError(
                    "GOOGLE_CREDENTIALS_PATH is not set or the file doesn't exist"
                )

            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token to file for future use
        with open("secrets/token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def main():
    try:
        creds = get_credentials()
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        if not labels:
            print("No labels found.")
            return
        print("Labels:")
        for label in labels:
            print(label["name"])

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
