"""xlsxファイルをcsvファイルに変換する"""
# https://qiita.com/Mistizz/items/9a4b271e1412550db811
# https://gist.github.com/yukinishinet/ad09ba3d158667d5b174bbf61d7c3fb2

import os
import os
import csv
import openpyxl
# from natsort import natsorted

input_folder = "folder1"
output_folder = "folder1"
input_folder_path = os.path.join(input_folder)
output_folder_path = os.path.join(output_folder)

def convert_xlsx_to_csv():
    # Excelファイル名リストを自然順で取得
    # files = natsorted(os.listdir(input_folder_path))
    files = os.listdir(input_folder_path)

    #ファイル名リストをfor文でまわして各ファイルの絶対パスを構築
    for file in files:
        filepath = os.path.join(input_folder_path, file)

        # xlsxファイルにアクセス→先頭シートのオブジェクトを取得
        wb = openpyxl.load_workbook(filepath)
        ws_name = wb.sheetnames[0]
        ws = wb[ws_name]

        # csvに変換して、output_folderに保存
        savecsv_path = os.path.join(output_folder_path, file.rstrip(".xlsx")+".csv")
        with open(savecsv_path, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            for row in ws.rows:
                writer.writerow([cell.value for cell in row])


if __name__ == "__main__":
    convert_xlsx_to_csv()
