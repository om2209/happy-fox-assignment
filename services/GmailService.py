import base64
import re
from datetime import datetime
from typing import List

from data.Action import Action
from data.Email import Email
from data.Rule import Rule
from data.RuleSet import RuleSet
from enums.DatePredicate import DatePredicate
from enums.FieldType import FieldType
from enums.RuleSetPredicate import RuleSetPredicate
from enums.StringPredicate import StringPredicate
from helpers.constants import FILTER_FIELD_TO_DATA_FIELD_MAPPING
from repositories.EmailRepository import EmailRepository


class GmailService:

    def save_emails(self, service, messages):
        saved_emails = 0
        for message in messages:
            message_details = service.users().messages().get(userId='me', id=message['id']).execute()
            headers = message_details['payload']['headers']
            email: Email = self.get_email_details(headers, message_details)
            is_saved = EmailRepository().save_email(email)
            if is_saved:
                saved_emails += 1
        EmailRepository().destroy_connection()

        return saved_emails

    def get_email_details(self, headers, message_details):
        sender = next(header['value'] for header in headers if header['name'] == 'From')
        subject = next(header['value'] for header in headers if header['name'] == 'Subject')
        received_date = next(header['value'].split('(')[0].strip() for header in headers if header['name'] == 'Date')
        message = self.get_full_message(message_details)
        labels = ','.join(list(filter(lambda label: label != 'UNREAD', message_details.get('labelIds', []))))
        is_read = True if 'UNREAD' not in message_details.get('labelIds', []) else False

        return Email(None, sender, subject, received_date, message, labels, is_read)

    @staticmethod
    def get_full_message(message):
        if 'payload' in message:
            if 'parts' in message['payload']:
                for part in message['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    elif part['mimeType'] == 'text/html':
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            elif 'body' in message['payload']:
                return base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
        return None

    def perform_actions_on_rules(self, email_filters: RuleSet):

        emails = EmailRepository().get_emails()
        filtered_emails = [email for email in emails if self.apply_rules(email_filters, email)]

        return self.perform_actions(filtered_emails, email_filters.actions)

    def apply_rules(self, rule_set: RuleSet, email: Email) -> bool:

        results = [self.apply_rule(Rule(**rule), email) for rule in rule_set.rules]

        if rule_set.predicate.upper() == RuleSetPredicate.ALL.value.upper():
            return all(results)
        elif rule_set.predicate.upper() == RuleSetPredicate.ANY.value.upper():
            return any(results)

    def apply_rule(self, rule: Rule, email: Email):

        field_value = getattr(email, FILTER_FIELD_TO_DATA_FIELD_MAPPING[FieldType(rule.field).value.upper()])
        if FieldType(rule.field).value.upper() == 'DATE RECEIVED':
            field_value = (field_value.split(',')[-1]).split('+')[0]
            field_value = field_value.split('-')[0]
            field_value = datetime.strptime(field_value.strip(), "%d %b %Y %H:%M:%S").replace(tzinfo=None)

        if rule.predicate in [string_predicate.value for string_predicate in StringPredicate]:
            return self.apply_string_predicates(rule, field_value)

        elif (rule.predicate in [date_predicate.value for date_predicate in DatePredicate] and
              isinstance(field_value, datetime)):
            return self.apply_date_predicates(rule, field_value)

        return False

    @staticmethod
    def has_timezone(time_string):
        timezone_pattern = r'[+-]\d{4}$'
        return bool(re.search(timezone_pattern, time_string))

    @staticmethod
    def apply_string_predicates(rule, field_value):
        if rule.predicate == StringPredicate.CONTAINS.value:
            return rule.value.lower() in field_value.lower()
        elif rule.predicate == StringPredicate.DOES_NOT_CONTAIN.value:
            return rule.value.lower() not in field_value.lower()
        elif rule.predicate == StringPredicate.EQUALS.value:
            return rule.value.lower() == field_value.lower()
        elif rule.predicate == StringPredicate.DOES_NOT_EQUAL.value:
            return rule.value.lower() != field_value.lower()

    @staticmethod
    def apply_date_predicates(rule, field_value):
        difference = (datetime.now() - field_value).days
        if rule.predicate == DatePredicate.LESS_THAN.value:
            return difference < rule.value
        elif rule.predicate == DatePredicate.GREATER_THAN.value:
            return difference > rule.value

    @staticmethod
    def perform_actions(emails: List[Email], actions: List[Action]):
        rows_affected = 0
        for email in emails:
            if EmailRepository().update_email(email, actions):
                rows_affected += 1

        return rows_affected
