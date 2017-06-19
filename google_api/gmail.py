from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import base64
import httplib2

from apiclient import discovery, errors

from .credentials import get_credentials


def send_mail(Subject, Message, From, To, From_name=None, To_name=None):
    message_text = MIMEText(Message)
    if To_name:
        message_text['to'] = formataddr(
            (str(Header(To_name, 'utf-8')),
             To))
    else:
        message_text['to'] = To

    if From_name:
        message_text['from'] = formataddr(
            (str(Header(From_name, 'utf-8')),
             From))
    else:
        message_text['from'] = From
    message_text['subject'] = Subject
    message = {'raw': base64.urlsafe_b64encode(message_text.as_bytes()).decode()}

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    try:
        message = (service.users().messages().send(userId=From, body=message)
            .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
