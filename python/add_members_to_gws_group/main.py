"""GoogleWorkspaceのグループを作成しメンバーを追加する"""
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
group_id = args[1]
members = [
    {"email": "terunrun@gmail.com", "role": "OWNER"},
]


def add_members_to_gws_group():
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

    # グループにメンバーを追加
    # https://developers.google.com/admin-sdk/directory/reference/rest/v1/members/insert?hl=ja
    try:
        service = build('admin', 'directory_v1', credentials=creds)
        for member in members:
            result = service.members().insert(
                # https://developers.google.com/admin-sdk/directory/reference/rest/v1/members?hl=ja#Member
                body = {"email": member["email"], "role": member["role"]},
                groupKey = group_id,
            ).execute()
            print(f'Add member result: {result}')
    except Exception as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    add_members_to_gws_group()
