MAX_RESULTS = 10

DB_NAME = 'happyfox'

DB_USER = 'root'

DB_PASSWORD = 'password'

FILTER_FIELD_TO_DATA_FIELD_MAPPING = {
    'FROM': 'sender',
    'SUBJECT': 'subject',
    'MESSAGE': 'message',
    'DATE RECEIVED': 'received_date'
}
