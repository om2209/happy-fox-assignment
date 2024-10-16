import json
from unittest import TestCase, mock
from unittest.mock import MagicMock

from data.Email import Email
from data.RuleSet import RuleSet
from services.GmailService import GmailService


class TestGmailService(TestCase):

    @mock.patch('services.GmailService.EmailRepository')
    def test_save_emails_success(self, mock_email_repository):
        service = MagicMock()

        messages = [{'id': '1'}, {'id': '2'}]
        service.users().messages().get.return_value.execute.return_value = self.get_message_details()

        mock_email_repository.return_value.save_email.return_value = True
        mock_email_repository.return_value.destroy_connection.return_value = None

        response = GmailService().save_emails(service, messages)

        self.assertEqual(response, 2)
        mock_email_repository.return_value.save_email.assert_called()
        self.assertEqual(mock_email_repository.return_value.save_email.call_count, 2)

    @mock.patch('services.GmailService.EmailRepository')
    def test_save_emails_failure(self, mock_email_repository):
        service = MagicMock()

        messages = [{'id': '1'}]
        service.users().messages().get.return_value.execute.return_value = self.get_message_details()

        mock_email_repository.return_value.save_email.return_value = False
        mock_email_repository.return_value.destroy_connection.return_value = None

        response = GmailService().save_emails(service, messages)

        self.assertEqual(response, 0)
        mock_email_repository.return_value.save_email.assert_called()
        self.assertNotEqual(mock_email_repository.return_value.save_email.call_count, 2)
        self.assertEqual(mock_email_repository.return_value.save_email.call_count, 1)

    @mock.patch('services.GmailService.EmailRepository')
    def test_perform_actions_on_rules_success(self, mock_email_repository):
        email_filters = self.get_rule_set_positive()
        mock_email_repository.return_value.get_emails.return_value = self.get_emails()
        mock_email_repository.return_value.update_email.return_value = True

        response = GmailService().perform_actions_on_rules(RuleSet(**email_filters))

        self.assertEqual(response, 3)
        mock_email_repository.return_value.update_email.assert_called()
        self.assertEqual(mock_email_repository.return_value.update_email.call_count, 3)

    @mock.patch('services.GmailService.EmailRepository')
    def test_perform_actions_on_rules_failure(self, mock_email_repository):
        email_filters = self.get_rule_set_negative()
        mock_email_repository.return_value.get_emails.return_value = self.get_emails()
        mock_email_repository.return_value.update_email.return_value = False

        response = GmailService().perform_actions_on_rules(RuleSet(**email_filters))

        self.assertEqual(response, 0)
        mock_email_repository.return_value.update_email.assert_called()
        self.assertEqual(mock_email_repository.return_value.update_email.call_count, 2)

    @staticmethod
    def get_message_details():
        with open('email_details.json', 'r') as f:
            return json.load(f)

    @staticmethod
    def get_rule_set_positive():
        with open('email_filters_positive.json', 'r') as f:
            return json.load(f)

    @staticmethod
    def get_rule_set_negative():
        with open('email_filters_negative.json', 'r') as f:
            return json.load(f)

    @staticmethod
    def get_emails():
        with open('emails.json', 'r') as f:
            emails_from_file = json.load(f)['emails']
        emails = []
        for email_from_file in emails_from_file:
            emails.append(Email(email_from_file['id'], email_from_file['from'], email_from_file['subject'],
                                email_from_file['receivedDate'], email_from_file['message'],
                                email_from_file['labels'], email_from_file['isRead']))

        return emails
