"""ディレクトリに含まれるファイルの一覧を取得する"""

import os
import sys

args = sys.argv
TARGET_FULL_PATH = args[1]

def list_directory():
    files = os.listdir(TARGET_FULL_PATH)
    for file in files:
        print(f"{file}")

if __name__ == "__main__":
    list_directory()
