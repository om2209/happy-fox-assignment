# happy-fox-assignment

## Description

This project has below two scripts 
  1. To download emails from Google's Gmail API and saving that to MySQL database. (`scripts/save_emails.py`)
  2. Update the emails in the DB using the filters and a list of actions provided by the user in a file called `rules.json` (`scripts/filter_emails.py`)

## Installation

  1. After cloning the project, install and activate a python virtual environment using below commands
       `python3 -m venv venv`
       `source venv/bin/activate`
  2. Install the required dependencies by this command: `pip3 install -r requirements.txt`
  3. Go to Google Cloud Console, create a project. Inside the project, enable the GmailAPI, and then go to consent screen and add the following scope
       `https://www.googleapis.com/auth/gmail.readonly`. Add the redirect URI: `http://localhost:8080/` and add the email which will be used in users.
  4. Once step 3 is done, go to OAuth credentials screen and create a clientId. Download and save the credentials file naming it `client_secrets.json` in `credentials` directory of the project.
  5. Install MySQL and start it. Create a database naming `happyfox` and inside this database, create a TABLE with following command:
       `CREATE TABLE IF NOT EXISTS email(
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            sender TEXT,
            subject TEXT,
            message TEXT,
            received_date TEXT,
            labels TEXT,
            is_read BOOL
        )`
  6. Add the name of the database, user and password details of the database in `helpers/constants.py` file in `DB_NAME`, `DB_USER`, `DB_PASSWORD` respectively.
  7. Test cases for filtering emails might fail if you have different details in your DB, please adjust the message and count of emails accordingly in `tests/TestGmailService.py` file.
  8. Use main methods in the script files to run the scripts.
  9. This app by default will fetch 10 emails, if you want to pull more, change the value of `MAX_RESULTS` in `helpers/constants.py` file to your choice.
