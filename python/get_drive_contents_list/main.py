"""指定したGoogleドライブフォルダ配下に存在するコンテンツの一覧をCSVファイルに出力する"""
# https://developers.google.com/drive/api/v3/reference?hl=ja
# https://zenn.dev/wtkn25/articles/python-googledriveapi-operation

from __future__ import print_function

import csv
import os.path
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

file_fields = [
    'parents', 'name', 'id', 'trashed', 'createdTime',
    'modifiedTime', 'webContentLink', 'webViewLink'
]

# 実行時引数として対象のドライブID受け取る
args = sys.argv
DRIVE_ID = args[1]

# idからリソース名を取得し、親リソースがある場合はそのidに対して再帰呼び出し
def get_full_parent(full_parent, item_parent, id_list, item_list):
    if item_parent not in id_list:
        return full_parent

    for item in item_list:
        if item_parent == item[1]:
            full_parent = f'{item[0]}/{full_parent}'
            return get_full_parent(full_parent, item[4][0], id_list, item_list)

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
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
                "credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", 'w', encoding='utf-8', newline='\n') as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        with open(f"file_list_{DRIVE_ID}.csv", 'w', encoding='utf-8', newline='\n') as result_file:
            writer = csv.writer(result_file)
            page_token = None
            item_list = []
            id_list = []
            while True:
                results = service.files().list(
                    # https://developers.google.com/drive/api/v3/reference/files?hl=ja
                    # spaces='drive',
                    corpora="drive",
                    driveId=DRIVE_ID,
                    includeItemsFromAllDrives=True,
                    supportsAllDrives=True,
                    # pageSize=10,
                    fields=f'nextPageToken, files({", ".join(file_fields)})',
                    pageToken=page_token
                ).execute()
                items = results.get("files", [])
                if not items:
                    print("No files found.")
                    return
                for item in items:
                    if not item["trashed"]:
                        id_list.append(item["id"])
                        item_list.append([
                            item["name"], item["id"], item["createdTime"],
                            item["modifiedTime"], item["parents"],
                            item["webContentLink"] if "webContentLink" in item else "",
                            item["webViewLink"] if 'webViewLink' in item else "",
                        ])
                page_token = results.get("nextPageToken", None)
                if page_token is None:
                    break

            # While文が終わってからでないとAPIでの取得結果をすべてリストに格納できていない
            item_list_with_full_parent = []
            for item in item_list:
                full_parent = ''
                item_list_with_full_parent.append([
                    # APIでの取得結果をすべてリストに格納したあとなので要素名で指定できない
                    # item['name'], item['id'], item['createdTime'], item['modifiedTime'],
                    # get_full_parent(full_parent, item['parents'][0], id_list, item_list)
                    get_full_parent(full_parent, item[4][0], id_list, item_list),
                    item[0], item[1], item[2], item[3], item[5], item[6]
                ])

            # 並べ替えてヘッダーをつける
            item_list_with_full_parent_sorted = sorted(item_list_with_full_parent, key=lambda x: (x[0], x[1]))
            file_fields.remove("trashed")
            item_list_with_full_parent_sorted.insert(0, file_fields)
            writer.writerows(item_list_with_full_parent_sorted)

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
