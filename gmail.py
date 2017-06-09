import quickstart
import httplib2
from apiclient import discovery, errors

class Mail:

    def __init__(self):
        credentials = quickstart.get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.client = discovery.build('gmail', 'v1', http=http)
    
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

    def getMessage(self, msgId):
        try:
            message = self.client.users().messages().get(userId='me', id=msgId).execute()

            print('Message {}',format(message['snippet']))
            return message
        except errors.HttpError as error:
            print('Error: {}'.format(error))


if __name__ == '__main__':
    mail = Mail()
    msgs = mail.getMessages()
    print(msgs)
    for i in msgs:
        mail.getMessage(i['id'])
