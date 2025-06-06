import os
import json
import tempfile

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
            credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

            if not credentials_json:
                raise EnvironmentError("GOOGLE_CREDENTIALS_JSON is not set")

            # Write JSON to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp:
                temp.write(credentials_json)
                temp_filepath = temp.name

            flow = InstalledAppFlow.from_client_secrets_file(temp_filepath, SCOPES)
            creds = flow.run_local_server(port=0)

            # Optionally delete the temp file
            os.remove(temp_filepath)

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