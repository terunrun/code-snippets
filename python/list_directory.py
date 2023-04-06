"""ディレクトリに含まれるファイルの一覧を取得する"""

import os
import sys

args = sys.argv
target_full_path = args[1]

def list_directory():
    files = os.listdir(target_full_path)
    for file in files:
        print(f"{file}")

if __name__ == "__main__":
    list_directory()
