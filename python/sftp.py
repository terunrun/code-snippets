"""SFTPでリモートサーバからローカルにファイルを取得する"""

import os
import sys
import paramiko

# 接続情報
HOST = os.environ.get('SFTP_HOST') #IPアドレス
PORT = os.environ.get('SFTP_PORT') #ポート
USER = os.environ.get('SFTP_USERNAME') #ユーザ名
PASSWORD = os.environ.get('SFTP_PASSWORD') #パスワード
MAX_TRY_NUM = 3
# ファイル情報
FILE_NAME = 'test.txt' #取得するファイル名称
REMOTE_PATH = '/home/ubuntu/' #ダウンロード対象パス
LOCAL_PATH = '/tmp/' #ダウンロードするローカルパス


def sftp():

    sftp_client = paramiko.SSHClient()
    sftp_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    sftp_client.connect(HOST, port=PORT, username=USER, password=PASSWORD)
    for i in range(1, MAX_TRY_NUM + 1):
        try:
            print(f"connect {i}th started...")
            sftp_connection = sftp_client.open_sftp()
            sftp_connection.get(REMOTE_PATH + FILE_NAME, LOCAL_PATH + FILE_NAME)
        # TODO:例外内容によって処理を変える
        except Exception as exception:
            print(f"connect {i}th failed!({i}/{MAX_TRY_NUM}) {exception}")
        # 失敗しなかった時はループを抜ける
        else:
            print(f"Successfully get {REMOTE_PATH + FILE_NAME} from {HOST}!")
            break
    else:
        sftp_client.close()
        print("Connect all failed!")
        sys.exit()


if __name__ == "__main__":
    sftp()
