import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

CREDENTIALS_DIRECTORY = 'credentials'


class GmailAuthentication:

    @staticmethod
    def authenticate():

        creds = None
        token_file_path = os.path.join(CREDENTIALS_DIRECTORY, 'token.json')
        client_secret_path = os.path.join(CREDENTIALS_DIRECTORY, 'client_secrets.json')

        if os.path.exists(token_file_path):
            creds = Credentials.from_authorized_user_file(token_file_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
                creds = flow.run_local_server(port=8080, prompt='consent')

            with open(token_file_path, 'w') as token:
                token.write(creds.to_json())

        return creds
