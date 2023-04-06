"""SFTPでリモートサーバからローカルにファイルを取得する"""

import os
import paramiko


def sftp():
    # SFTP接続先を環境変数から取得する
    HOST = os.environ.get('SFTP_HOST') #IPアドレス
    PORT = os.environ.get('SFTP_PORT') #ポート
    USER = os.environ.get('SFTP_USERNAME') #ユーザ名
    PASSWORD = os.environ.get('SFTP_PASSWORD') #パスワード

    # ファイル情報
    FILE_NAME = 'test.txt' #取得するファイル名称
    REMOTE_PATH = '/home/ubuntu/' #ダウンロード対象パス
    LOCAL_PATH = '/tmp/' #ダウンロードするローカルパス

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(HOST, port=PORT, username=USER, password=PASSWORD)
    try:
        sftp_connection = client.open_sftp()
        sftp_connection.get(REMOTE_PATH + FILE_NAME, LOCAL_PATH + FILE_NAME)
    finally:
        client.close()


if __name__ == "__main__":
    sftp()
