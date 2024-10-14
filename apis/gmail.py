from chalice import Blueprint, Response

from googleapiclient.discovery import build

from credentials.oauth import GmailAuthentication
from data.RuleSet import RuleSet
from helpers.constants import MAX_RESULTS
from services.GmailService import GmailService

gmail_apis = Blueprint(__name__)


@gmail_apis.route('/emails', methods=['GET'], api_key_required=False)
def fetch_and_save_emails():
    creds = GmailAuthentication.authenticate()
    service = build('gmail', 'v1', credentials=creds)

    try:
        results = service.users().messages().list(userId='me', maxResults=MAX_RESULTS).execute()
        messages = results.get('messages', [])
        if not messages:
            return Response(body={
                'message': 'No messages available'
            }, status_code=204, headers={'Content-Type': 'application/json'})
        else:
            return GmailService().save_emails(service, messages)

    except Exception as e:
        return Response(body={
            'message': f'Exception occurred {e}'
        }, status_code=500, headers={'Content-Type': 'application/json'})


@gmail_apis.route('/emails', methods=['POST'], api_key_required=False)
def perform_ops_on_emails():
    request = gmail_apis.current_request
    request_body = request.json_body

    if not request_body:
        return Response(body={
            'message': 'Missing filters'
        }, status_code=400, headers={'Content-Type': 'application/json'})

    email_filters = RuleSet(**request_body)

    return GmailService().perform_actions_on_rules(email_filters)




