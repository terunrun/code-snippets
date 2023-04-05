"""指定したGoogle Workspace組織のグループと所属するユーザーの一覧をCSVファイルに出力する"""
# https://developers.google.com/admin-sdk/directory/v1/guides/guides?hl=ja
# https://developers.google.com/admin-sdk/directory/v1/guides?hl=ja
# https://developers.google.com/admin-sdk/reference-overview?hl=ja

from __future__ import print_function

import csv
import os.path
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

# 実行時引数としてGWS顧客IDを受け取る
args = sys.argv
customer_id = args[1]


def main():
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
    """
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
    service = build('admin', 'directory_v1', credentials=creds)

    # # 対象GWSドメインのユーザー一覧を取得してCSVに出力する
    # users_list = []
    # with open(f'users_list_{customer_id}.csv', 'w') as users_file:
    #     writer = csv.writer(users_file)
    #     page_token = None
    #     while True:
    #         results = service.users().list(customer=customer_id,
    #                                     # maxResults=10,
    #                                     orderBy='email',
    #                                     pageToken=page_token,
    #                                     ).execute()
    #         users = results.get('users', [])
    #         if not users:
    #             print('\nNo users in the domain.')
    #         else:
    #             for user in users:
    #                 # 取得したい項目は以下を参照に変更する
    #                 # https://developers.google.com/admin-sdk/directory/reference/rest/v1/users?hl=ja#User
    #                 users_list.append([user["primaryEmail"], user["name"]["fullName"]])
    #         page_token = results.get('nextPageToken', None)
    #         if page_token is None:
    #             break
    #     # 並べ替えてヘッダーをつける
    #     users_list_sorted = sorted(users_list, key=lambda x: (x[0], x[1]))
    #     users_list_sorted.insert(0, ["primaryEmail", "fullName"])
    #     writer.writerows(users_list_sorted)

    groups_list = []
    with open(f'groups_list_{customer_id}.csv', 'w') as groups_file:
        writer = csv.writer(groups_file)
        page_token = None
        while True:
            results = service.groups().list(customer=customer_id,
                                            # maxResults=10,
                                            orderBy='email',
                                            pageToken=page_token,
                                        ).execute()
            groups = results.get('groups', [])
            if not groups:
                print('\nNo groups in the domain.')
            else:
                for group in groups:
                    page_token_members = None
                    while True:
                        results = service.members().list(groupKey=group['id'],
                                                        # maxResults=10,
                                                        pageToken=page_token_members,
                                                        ).execute()
                        members = results.get('members', [])

                        if not members:
                            print(f'\nNo members in {group["name"]}.')
                            groups_list.append([group["id"], group["email"], group["name"], "", "", "",])
                        else:
                            for member in members:
                                user = service.users().get(userKey=member["id"],).execute()
                                print(user)
                                if not user:
                                    print(f'\nNo user id: {member["id"]}.')
                                else:
                                    # 取得したい項目は以下を参照に変更する
                                    # https://developers.google.com/admin-sdk/directory/reference/rest/v1/users?hl=ja#User
                                    # https://developers.google.com/admin-sdk/directory/reference/rest/v1/groups?hl=ja#Group
                                    # https://developers.google.com/admin-sdk/directory/reference/rest/v1/members?hl=ja#Member
                                    groups_list.append([group["id"], group["email"], group["name"], member["role"], member["email"], user["name"]["fullName"]])
                        page_token_members = results.get('nextPageToken', None)
                        if page_token_members is None:
                            break
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break
        # 並べ替えてヘッダーをつける
        groups_list_sorted = sorted(groups_list, key=lambda x: (x[1], x[3], x[4]))
        groups_list_sorted.insert(0, ["group_id", "email", "name", "role", "user_id", "email"])
        writer.writerows(groups_list_sorted)


if __name__ == '__main__':
    main()
