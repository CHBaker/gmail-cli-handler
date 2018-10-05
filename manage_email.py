from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import imaplib
import sys

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'

// get args from script
ARGS = dict([arg.split('=') for arg in sys.argv[1:]])

def main():
    manager = Manage_emails(ARGS['label'], ARGS['sender'])

class Manage_emails():

    def __init__(self, label, sender):
        print('Getting Auth and logging you in...')
        self.sender = sender
        self.label = label
        self.service = None
        self.labelId = None
        self.emailsByLabel = []
        self.emailsBySender = []
        self.login()

    def get_input(self, question, yes, no):
        while True:
            ask = raw_input(question)
            if ask != 'y' and ask != 'n':
                print('sorry, that is not a valid input')
                continue
            else:
                break
        
        if ask == 'y':
            yes()
        
        if ask == 'n':
            no()

    def what_now(self):
        while True:
            ask = raw_input('Want to delete more emails? y or n: ')
            if ask != 'y' and ask != 'n':
                print('sorry, that is not a valid input')
                continue
            else:
                break
        
        if ask == 'y':
            self.by_label_or_sender()
        
        if ask == 'n':
            print('glad I could help, bye :D')
            sys.exit()


    def login(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('gmail', 'v1', http=creds.authorize(Http()))
        self.by_label_or_sender()


    def by_label_or_sender(self):
        q = 'To get emails by lable, enter y. To get emails by sender, enter n. y or n: '

        def no():
            print('Alright, then lets get your emails by sender')
            self.get_emails_by_sender()
        
        def yes():
            print('Alright, getting your emails by label...')
            self.get_labels()

        self.get_input(q, yes, no)


    def get_labels(self):
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if len(labels) > 0:
            print('%s labels' % len(labels))
            for label in labels:
                if label['name'] == self.label:
                    self.labelId = label['id']

        else:
            print('no labels found')

        if self.labelId != None:
                self.get_emails_by_label()

        else:
            print('sorry, that label was not found')
            self.what_now()


    def get_emails_by_label(self):
        print('fetching emails by that label...')
        results = self.service.users().messages()\
            .list(userId = 'me', labelIds = [self.labelId]).execute()

        messages = results.get('messages', [])

        if len(messages) > 0:
            print('%s Emails by label' % len(messages))
            self.emailsByLabel = messages
            self.delete_emails()

        else: 
            print('you have no messages under that label')
            self.what_now()

    def get_emails_by_sender(self):
        results = self.service.users().messages()\
            .list(userId = 'me', q = self.sender).execute()

        messages = results.get('messages', [])
        if len(messages) > 0:
            print('%s Emails by sender' % len(messages))
            self.emailsBySender = messages
            self.delete_emails()

        else:
            print('You have no emails from this sender')
            self.what_now()


    def delete_emails(self):
        q = 'Are you sure you want to delete those emails? y or n: '

        def yes():
            print('Alright, deleting...')
            success = True

            if len(self.emailsByLabel) > 0:
                for email in self.emailsByLabel:
                    res = self.service.users().messages()\
                        .trash(userId = 'me', id = email['id']).execute()

                    body = res.get('messages', [])
                    if body == []:
                        print('deleted ', email)
                    else:
                        success = False

            if len(self.emailsBySender) > 0:
                for email in self.emailsBySender:
                    res = self.service.users().messages()\
                        .trash(userId = 'me', id = email['id']).execute()

                    body = res.get('messages', [])
                    if body == []:
                        print('deleted ', email)
                    else:
                        success = False
            
            if success:
                print('All emails under that query were deleted')
                self.what_now()
            
            else:
                failed_q = 'One or more emails failed to delete\
                    try again? y or n: '

                def failed_yes():
                    self.delete_emails()
                
                def failed_no():
                    self.what_now()

                self.get_input(failed_q, failed_yes, failed_no)
        
        def no():
            self.what_now()

        self.get_input(q, yes, no)

if __name__ == '__main__':
    main()
