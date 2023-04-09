"""zip形式ファイルを解凍する"""

import glob
import sys
import zipfile

args = sys.argv
SOURCE_FILE_NAME = args[1]

def unzip_file():
    with zipfile.ZipFile(f"{SOURCE_FILE_NAME}.zip", "r") as zip_file:
        zip_file.extractall("./")
    txt_files = glob.glob(f"./{SOURCE_FILE_NAME}/*.txt")
    print(f"Successfully unzip: {SOURCE_FILE_NAME}.zip")
    print(f"type: {type(txt_files)}")
    print(txt_files)

    txt_file_list = []
    for txt_file in txt_files:
        target_file_name = txt_file.split("/", 1)[1]
        txt_file_list.append(target_file_name)
    print(f"Files: f{txt_file_list}")

if __name__ == "__main__":
    unzip_file()
