import quickstart
import httplib2
import pprint
import base64
from bs4 import BeautifulSoup
from apiclient import discovery, errors
import email
class Mail:

    def __init__(self):
        credentials = quickstart.get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.client = discovery.build('gmail', 'v1', http=http)
   
    def formatQuery(self, query=''):
        if query == '':
            return query


    def getMessages(self, query='', labels=[]):
        ''' List all of user's messages in mailbox by query'''
        def first_page():
            return self.client.users().messages().list(
                                                userId='me',
                                                q=query,
                                                labelIds=labels).execute()
        def next_page(page_token):
            return self.client.users().messages().list(
                                                userId='me',
                                                q=query,
                                                labelIds=labels,
                                                pageToken=page_token).execute() 
        try:
            messages = []
            result = first_page()
            if 'messages' in result:
                messages.extend(result['messages'])
            while 'nextPageToken' in result:
                    page_token = result['nextPageToken']
                    result = next_page(page_token)
                    messages.extend(result['messages'])
            
            return messages
        except errors.HttpError as error:
            print("Error: {}".format(error))
            print("Aborting Fetching Messages Command")

    def getMessage(self, msgId):
        ''' 
            Assuming each email recieved is well-formed
            parses the message for from and subject fields
    
         '''
        def _parse_header(header):
            header_from, header_subj = None, None
            for i in message['payload']['headers']:
                if i['name'].lower() == 'from':
                    header_from = i['value'].split(" <")[0].replace('"','')
                if i['name'].lower() == 'subject':
                    header_subj = i['value']
            return header_from, header_subj
        try:
            message = self.client.users().messages().get(
                                                userId='me', 
                                                id=msgId,
                                                format='full').execute()
            header_from, header_subj = _parse_header(message['payload']['headers'])
            print("{:<25}:- {:<70}".format(header_from[:25:], header_subj[:70:]))
            return message
        except errors.HttpError as error:
            print('Error: {}'.format(error))
            print("Aborting Fetching Message Command")

    def delMessages(self, messages):
        ''' 
            Deleting Groups of Messages 
            '''
        for i in messages:
            self.delMessage(message[i]['id'])

    def delMessage(self, msgId):
        ''' 
            Deleting Single Message 
        '''
        try:
            message = self.client.users().messages().trash(
                                                userId='me', 
                                                id=msgId).execute()
            print("Message {} deleted".format(msgId))
        except errors.HttpError as error:
            print("Error: {}".format(error))
            print("Aborting Delete Message Command")

def main():
    mail = Mail()
    msgs = mail.getMessages()
    msg = mail.getMessage(msgs[0]['id'])
if __name__ == '__main__':
    main()
