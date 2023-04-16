"""GoogleCloudのプロジェクトを作成し請求先アカウントを設定する"""
# https://cloud.google.com/resource-manager/docs/creating-managing-projects?hl=ja#api
# Resource Manager API、Cloud Billing APIの有効化が必要

import os
import sys
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
]

# 実行時引数
args = sys.argv
organization_id = args[1]
folder_id = args[2]
project_id = args[3]
billing_account  = args[4]


def create_gcp_project():
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

    # プロジェクトを作成
    # https://cloud.google.com/resource-manager/reference/rest/v3/projects/create
    try:
        service = build('cloudresourcemanager', 'v3', credentials=creds)
        parent = ""
        if organization_id:
            parent = f"organizations/{organization_id}"
        if folder_id:
            parent = f"folders/{folder_id}"
        print(f"parent: {parent}")
        operation = service.projects().create(
            # https://cloud.google.com/resource-manager/reference/rest/v3/projects#Project
            body = {"projectId": project_id, "displayName": project_id, "parent": parent,}
        ).execute()
        print(f'operation: {operation}')
    except Exception as error:
        print(f'An error occurred: {error}')

    # NOTE: 後続処理がエラーとならないようプロジェクト作成が完了するまで待つ
    operation_done = False
    try:
        while True:
            print(f'Waiting {operation["name"]} finish...')
            operation = service.operations().get(
                # https://cloud.google.com/resource-manager/reference/rest/v3/operations/get
                name = operation['name']
            ).execute()
            if 'done' in operation:
                operation_done = operation['done']
            if operation_done:
                break
            time.sleep(10)
        print(f'operation: {operation}')
        print(f'response: {operation["response"]}')
    except Exception as error:
        print(f'An error occurred: {error}')

    # 請求先アカウントを設定
    if billing_account:
        try:
            # https://cloud.google.com/billing/docs/reference/rest/v1/projects/updateBillingInfo
            service = build('cloudbilling', 'v1', credentials=creds)
            updateBillingInfo = service.projects().updateBillingInfo(
                # https://cloud.google.com/billing/docs/reference/rest/v1/ProjectBillingInfo
                name = f"projects/{project_id}",
                body = {"billingAccountName": f"billingAccounts/{billing_account}",}
            ).execute()
            print(f'updateBillingInfo: {updateBillingInfo}')
        except Exception as error:
            print(f'An error occurred: {error}')


if __name__ == '__main__':
    create_gcp_project()
