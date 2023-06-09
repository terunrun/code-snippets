"""Google Cloud Storageのファイルを比較し差分があるかどうかを判定する"""

import logging
import os
import subprocess
import sys

DESTINATION_BUCKET_1 = 'sandbox-terunrun-dev-csv-bucket'
DESTINATION_BUCKET_2 = 'sandbox-terunrun-dev-csv-bucket/backup'


def compare_files_from_gcs():
    # ログを指定ファイルに出力する
    logging.basicConfig(filename='src/logger.log', level=logging.DEBUG)

    # files = ['test_1.txt', 'test_2.txt']
    files = ['test_1.txt']

    for file in files:
        # ファイルをローカルにコピーする
        # TODO: クライアントライブラリを使うようにする
        command = f'gsutil cp gs://{DESTINATION_BUCKET_1}/{file} /tmp/diff/{file}'
        ret = subprocess.run(command.split(), check=False)

        # 比較対象ファイルをローカルにコピーする
        # TODO: クライアントライブラリを使うようにする
        command = f'gsutil cp gs://{DESTINATION_BUCKET_2}/{file} /tmp/diff/backup_{file}'
        ret = subprocess.run(command.split(), check=False)

        # 比較対象ファイルを取得できたかどうかチェックする
        if not os.path.isfile(f'/tmp/diff/backup_{file}'):
            logging.info('比較対象ファイルを取得できない')

        # ファイルを比較する
        command = f'diff /tmp/diff/{file} /tmp/diff/backup_{file}'
        ret = subprocess.run(command.split(), stdout=subprocess.PIPE, check=False)
        output = ret.stdout
        # 結果を行ごとにリストにする。
        lines = output.splitlines()

        # TODO:ここまでの処理でエラーが起きたら場合でも削除できるようにする
        # ローカルファイルを削除する。
        command = f'rm -f /tmp/diff/{file}'
        ret = subprocess.run(command.split(), check=False)
        command = f'rm -f /tmp/diff/backup_{file}'
        ret = subprocess.run(command.split(), check=False)

        if lines:
            logging.info('diff length: %s', len(lines))
            logging.info('%s に差分が存在するため終了', file)
            sys.exit()
        logging.info('%s に差分が存在しないため続行', file)
        continue

    logging.info('差分ありのファイルが存在しない')


if __name__ == "__main__":
    compare_files_from_gcs()
