"""Googleドライブのフォルダを作成する"""
# https://developers.google.com/drive/api/v3/reference?hl=ja
# Drive APIの有効化が必要

import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/drive'
]

# 実行時引数として対象ドライブIDを受け取る
args = sys.argv
drive_id = args[1]
drive_name = args[2]


def create_gws_drive():
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
        service = build('drive', 'v3', credentials=creds)
        file_metadata = {
            'name': drive_name,
            'mimeType': 'application/vnd.google-apps.folder',
            # TODO: 共有ドライブ直下の場合はdrive_idに何を指定する？
            'parents': [] if not drive_id else [drive_id]
        }
        drive = service.files().create(
            body = file_metadata,
            # fields = 'id'
            # NOTE: 共有ドライブ配下のフォルダをparentsに指定する場合にTrueを設定する
            supportsAllDrives = True,
        ).execute()
        print(f"drive: {drive}")
    except Exception as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    create_gws_drive()
