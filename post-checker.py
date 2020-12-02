import os
import re
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
from apiclient import errors
import tempfile




"""
scope for sending emails
"""
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


class PostChecker:

    def __init__(self, website, recipient_name):
        """
        str website: The website on which to search for the recipient name
        str recipient_name: The name to search for on the website
        """
        self.website = website
        self.recipient_name = recipient_name
        self.tmp_file = tempfile.NamedTemporaryFile() 

    def _get_html(self):
        os.system('wget -O ' + self.tmp_file.name + " " + self.website)

    def check_post(self):
        """
        Search for the recipient name on the website.
        If found, return True, else False.
        """
        self._get_html()
        with open(self.tmp_file.name, 'r') as f:
            text = f.read()
        post_match = re.search(self.recipient_name, text)
        return True if post_match else False

    
class Mail:

    def __init__(self, sender, to, subject, message_text):
        self.sender = sender
        self.to = to
        self.subject = subject
        self.message_text = message_text
        creds = None
        """
        You should have a file credentials.json.
        If not, you can get it by enabling the Gmail API on
        https://developers.google.com/gmail/api/quickstart/python
        """
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)

    def create_message(self):
        message = MIMEText(self.message_text)
        message['to'] = self.to
        print(message['Content-Type'])
        message['from'] = self.sender
        message['subject'] = self.subject

        b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
        b64_string = b64_bytes.decode()
        return {'raw': b64_string}

    def send_message(self):
        try:
            message = self.create_message()
            message = self.service.users().messages().send(userId=self.sender, body=message).execute()
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as err:
            print(f'An error occurred: {err}s')


def main():
    website = r"url-for-list-of-post"
    name = "name-of-recipient-here"

    sender = 'your-gmail-address'
    to = 'the-addres-to-be-notified'
    subject = 'PostChecker'
    message_text = 'Your package has arrived.'

    checker = PostChecker(website, name)
    if checker.check_post():
        Mail(sender, to, subject, message_text).send_message()
    else:
        print("No Email sent.")
    

if __name__ == '__main__':
  main()
