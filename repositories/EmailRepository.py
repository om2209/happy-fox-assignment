from typing import List

import mysql.connector

from data.Action import Action
from data.Email import Email
from enums.ActionType import ActionType
from helpers.constants import DB_NAME, DB_USER, DB_PASSWORD


class EmailRepository:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            database=DB_NAME,
            user=DB_USER,
            passwd=DB_PASSWORD
        )

    def save_email(self, email: Email):
        cursor = self.connection.cursor()
        insert_query = '''insert into email(sender, subject,  message, received_date, labels, is_read) values(%s, %s,
                        %s, %s, %s, %s)'''
        try:
            cursor.execute(insert_query, (
                email.sender, email.subject, email.message, email.received_date, email.labels, email.is_read))
            self.connection.commit()
            return True
        except Exception as e:
            print(f'Exception occurred during saving the email {e}')
            return False

    def get_emails(self):
        cursor = self.connection.cursor()
        select_query = 'select * from email'
        try:
            cursor.execute(select_query)
            emails_from_db = cursor.fetchall()
            emails = []
            for email_from_db in emails_from_db:
                email = Email(int(email_from_db[0]), email_from_db[1], email_from_db[2], email_from_db[4],
                              email_from_db[3], email_from_db[5], bool(email_from_db[6]))
                emails.append(email)

            return emails

        except Exception as e:
            print(f'Exception occurred during fetching the emails {e}')
            return {}

    def update_email(self, email: Email, actions: List[Action]):
        cursor = self.connection.cursor()
        errors = 0
        for action in actions:
            action = Action(**action)
            try:
                if action.action_type.upper() == ActionType.MARK_AS_UNREAD.value.upper():
                    cursor.execute('update email set is_read = %s where id = %s', (False, email.id))
                elif action.action_type.upper() == ActionType.MARK_AS_READ.value.upper():
                    cursor.execute('update email set is_read = %s where id = %s', (True, email.id))
                elif action.action_type.upper() == ActionType.MOVE_MESSAGE.value.upper() and action.folder_name:
                    labels = list(filter(lambda label: label not in ['INBOX', action.folder_name],
                                         email.labels.split(',')))
                    labels.append(action.folder_name)
                    labels = ','.join(labels)
                    cursor.execute("UPDATE email SET labels = %s WHERE id = %s",
                                   (labels, email.id))
                self.connection.commit()
            except Exception as e:
                print(f'Exception occurred during updating the emails {e}')
                errors += 1
        return False if errors else True

    def destroy_connection(self):
        self.connection.close()
