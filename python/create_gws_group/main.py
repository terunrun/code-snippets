"""GoogleWorkspaceのグループを作成する"""
# Admin SDK APIの有効化が必要

import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/admin.directory.user',
    'https://www.googleapis.com/auth/admin.directory.group',
]

# 実行時引数
args = sys.argv
group_address = args[1]
group_name = args[2]


def create_gws_group():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('admin', 'directory_v1', credentials=creds)
        # グループを作成
        # https://developers.google.com/admin-sdk/directory/reference/rest/v1/groups/insert?hl=ja
        # emailはドメイン名を含めて指定する必要がある
        group = service.groups().insert(
            # https://developers.google.com/admin-sdk/directory/reference/rest/v1/groups?hl=ja#Group
            body = {"email": group_address, "name": group_name,}
        ).execute()
        print(f'Created group: {group["id"]}, {group["name"]}')
    except Exception as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    create_gws_group()
