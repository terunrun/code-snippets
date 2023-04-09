"""xlsxファイルをcsvファイルに変換する"""
# https://qiita.com/Mistizz/items/9a4b271e1412550db811
# https://gist.github.com/yukinishinet/ad09ba3d158667d5b174bbf61d7c3fb2

import os
import csv
import openpyxl
# from natsort import natsorted

INPUT_FOLDER = "folder1"
OUTPUT_FOLDER = "folder1"
INPUT_FOLDER_PATH = os.path.join(INPUT_FOLDER)
OUTPUT_FOLDER_PATH = os.path.join(OUTPUT_FOLDER)

def convert_xlsx_to_csv():
    # Excelファイル名リストを自然順で取得
    # files = natsorted(os.listdir(INPUT_FOLDER_PATH))
    files = os.listdir(INPUT_FOLDER_PATH)

    #ファイル名リストをfor文でまわして各ファイルの絶対パスを構築
    for file in files:
        filepath = os.path.join(INPUT_FOLDER_PATH, file)

        # xlsxファイルにアクセス→先頭シートのオブジェクトを取得
        workbook = openpyxl.load_workbook(filepath)
        worksheet_name = workbook.sheetnames[0]
        worksheet = workbook[worksheet_name]

        # csvに変換して、OUTPUT_FOLDERに保存
        savecsv_path = os.path.join(OUTPUT_FOLDER_PATH, file.rstrip(".xlsx")+".csv")
        with open(savecsv_path, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for row in worksheet.rows:
                writer.writerow([cell.value for cell in row])


if __name__ == "__main__":
    convert_xlsx_to_csv()
