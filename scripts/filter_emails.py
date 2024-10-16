import json
import os

from data.RuleSet import RuleSet
from services.GmailService import GmailService


def perform_ops_on_emails():
    with open('rules.json', 'r') as f:
        rule_set = json.load(f)

    if not rule_set:
        return False, 0

    email_filters = RuleSet(**rule_set)

    return True, GmailService().perform_actions_on_rules(email_filters)


if __name__ == '__main__':
    status, rows_affected = perform_ops_on_emails()
    if not status:
        print("No rule set found")
    else:
        print(f'{rows_affected} rows affected')
