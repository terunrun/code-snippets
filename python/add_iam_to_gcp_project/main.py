"""GoogleCloudのプロジェクトにIAMロールを設定する"""
# https://cloud.google.com/iam/docs/granting-changing-revoking-access?hl=ja#iam-view-access-rest
# Resource Manager API、Cloud Billing APIの有効化が必要

import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
]

# 実行時引数
args = sys.argv
project_id = args[1]
# NOTE: 指定するプリンシパルに応じてtypeを変更する（例：グループの場合はgroup）
principals = [
    {"email": "terunrun@gmail.com", "type": "user", "role": "roles/browser"},
]


def add_iam_to_gcp_project():
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

    # プリンシパルにIAMロールを付与
    # https://cloud.google.com/resource-manager/reference/rest/v3/projects/setIamPolicy
    try:
        service = build('cloudresourcemanager', 'v3', credentials=creds)
        policies_json = {"bindings": []}
        for principal in principals:
            # https://cloud.google.com/resource-manager/reference/rest/Shared.Types/Policy
            policies_json["bindings"].append({
                    "role": principal['role'],
                    "members": f"{principal['type']}:{principal['email']}"
            }),
        policy = service.projects().setIamPolicy(
            resource = f"projects/{project_id}",
            body = {"policy": policies_json},
        ).execute()
        print(f'policy: {policy}')
    except Exception as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    add_iam_to_gcp_project()
