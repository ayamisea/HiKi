"""
Use $ python credentials.py --noauth_local_webserver
"""
from __future__ import print_function
import os
import json

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
GOOGLE_APPLICATION_CREDENTIALS = '.credentials/gapi.json'

def main():
    print(os.environ.get('CLIENT_ID'))
    home_dir = os.getcwd()
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gapi.json')
    # access_type="offline" and approval_prompt='force'.
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.OAuth2WebServerFlow(os.environ.get('CLIENT_ID'),
                                          os.environ.get('CLIENT_SECRET'),
                                          scope=SCOPES,
                                          access_type='offline',
                                          approval_prompt='force',)
        if flags:
                credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_path = GOOGLE_APPLICATION_CREDENTIALS#os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    credentials_json = json.loads(open(credential_path).read())
    credentials = client.OAuth2Credentials(
        credentials_json['access_token'],
        credentials_json['client_id'],
        credentials_json['client_secret'],
        credentials_json['refresh_token'],
        credentials_json['token_expiry'],
        credentials_json['token_uri'],
        'hiki-diary'
    )
    return credentials

if __name__ == '__main__':
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    main()
