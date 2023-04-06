"""zip形式ファイルを解凍する"""

import glob
import os
import sys
import zipfile

args = sys.argv
source_file_name = args[1]
# source_file = "sample.zip"

def unzip_file():
    with zipfile.ZipFile(f"{source_file_name}.zip", "r") as zip_file:
        zip_file.extractall("./")
        # os.remove(source_file)
    txt_files = glob.glob(f"./{source_file_name}/*.txt")
    print(f"Successfully unzip: {source_file_name}.zip")
    print(f"type: {type(txt_files)}")
    print(txt_files)

    txt_file_list = []
    for txt_file in txt_files:
        target_file_name = txt_file.split("/", 1)[1]
        txt_file_list.append(target_file_name)
    print(f"Files: f{txt_file_list}")

if __name__ == "__main__":
    unzip_file()
