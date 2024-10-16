from googleapiclient.discovery import build

from credentials.oauth import GmailAuthentication
from helpers.constants import MAX_RESULTS
from services.GmailService import GmailService


def fetch_and_save_emails():
    creds = GmailAuthentication.authenticate()
    service = build('gmail', 'v1', credentials=creds)

    try:
        results = service.users().messages().list(userId='me', maxResults=MAX_RESULTS).execute()
        messages = results.get('messages', [])
        if not messages:
            return True, 0
        else:
            saved_emails = GmailService().save_emails(service, messages)
            return (True, saved_emails) if saved_emails > 0 else (False, saved_emails)

    except Exception as e:
        print(f'Exception occurred {e}')
        return False, 0


if __name__ == '__main__':
    emails_saved, count = fetch_and_save_emails()
    if emails_saved:
        if count > 0:
            print(f'{count} emails saved')
        else:
            print("No emails found")
    else:
        print('Some issue occurred in saving the emails')
