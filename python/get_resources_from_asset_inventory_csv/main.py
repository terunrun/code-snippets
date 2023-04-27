"""Google CloudのAsset InventoryのCSVを読み込み、列を並べ替えた結果をCSV出力する"""

import csv
import os
import sys

# 実行時引数としてAsset Inventoryの画面から取得した対象CSVを受け取る
args = sys.argv
FILE_NAME = args[1]

output_csv_header = [
    "組織", "フォルダ", "プロジェクト ID", "リソースの種類", "名前",
     "表示名", "ステータス", "親のアセットタイプ", "親の完全なリソース名",
    "KMS 鍵", "説明", "ロケーション", "ラベル", "ネットワーク タグ", "その他の属性"
]

def get_output_csv_row(input_csv_row):
    return [
        input_csv_row["組織"],
        input_csv_row["フォルダ"],
        input_csv_row["プロジェクト ID"],
        input_csv_row["リソースの種類"],
        input_csv_row["名前"],
        input_csv_row["表示名"],
        input_csv_row["ステータス"],
        input_csv_row["親のアセットタイプ"],
        input_csv_row["親の完全なリソース名"],
        input_csv_row["KMS 鍵"],
        input_csv_row["説明"],
        input_csv_row["ロケーション"],
        input_csv_row["ラベル"],
        input_csv_row["ネットワーク タグ"],
        input_csv_row["その他の属性"]
    ]

def sort_output_rows(output_rows):
    output_rows_sorted = sorted(output_rows, key=lambda x: (x[0], x[1], x[2], x[3], x[4]))
    output_rows_sorted.insert(0, output_csv_header)
    return output_rows_sorted

def main():
    # 対象CSVをヘッダー抜きで読み込む
    os.makedirs('./output', exist_ok=True)
    with open(f"./{FILE_NAME}.csv", "rt", encoding="utf-8") as input_csv:
        dict_reader = csv.DictReader(input_csv)
        input_csv_rows = list(dict_reader)

        organization_list_raw = []
        folder_list_raw = []
        project_list_raw = []
        for input_csv_row in input_csv_rows:
            if input_csv_row["組織"]:
                organization_list_raw.append(input_csv_row["組織"])
            if input_csv_row["フォルダ"] and input_csv_row["フォルダ"] != "[]":
                folder_list_raw.append(input_csv_row["フォルダ"])
            # 「sys-」始まりのプロジェクトは自動的に作成される（であろう）ため除外する
            if input_csv_row["プロジェクト ID"] and not input_csv_row["プロジェクト ID"].startswith("sys-"):
                project_list_raw.append(input_csv_row["プロジェクト ID"])

        organization_list = list(set(organization_list_raw))
        folder_list = list(set(folder_list_raw))
        project_list = list(set(project_list_raw))

        # print(f"organization_list: {organization_list}")
        # print(f"folder_list: {folder_list}")
        # print(f"project_list: {project_list}")

        # for organization in organization_list:
        #     # 結果出力CSVを作成
        #     with open(f'./{FILE_NAME}_{organization.replace("/", "_")}.csv', 'w') as output_csv:
        #         writer = csv.writer(output_csv)
        #         writer.writerow(output_csv_header)
        #         for input_csv_row in input_csv_rows:
        #             if input_csv_row["組織"] == organization:
        #                 if input_csv_row["フォルダ"] == "[]":
        #                     if not input_csv_row["プロジェクト ID"]:
        #                         writer.writerow(get_output_csv_row(input_csv_row))

        for organization in organization_list:
            # 結果出力CSVを作成
            with open(
                f'./output/{FILE_NAME}_{organization.replace("/", "_")}.csv',
                'w', encoding='utf-8', newline='\n'
            ) as output_csv:
                writer = csv.writer(output_csv)
                output_rows = []
                for input_csv_row in input_csv_rows:
                    if input_csv_row["組織"] == organization:
                        if input_csv_row["フォルダ"] == "[]":
                            if not input_csv_row["プロジェクト ID"]:
                                output_rows.append(get_output_csv_row(input_csv_row))
                writer.writerows(sort_output_rows(output_rows))

        for folder in folder_list:
            # 結果出力CSVを作成
            with open(
                f'./output/{FILE_NAME}_{folder.replace("/", "_").replace("[", "").replace("]", "")}.csv',
                'w', encoding='utf-8', newline='\n'
            )as output_csv:
                writer = csv.writer(output_csv)
                output_rows = []
                for input_csv_row in input_csv_rows:
                    if input_csv_row["フォルダ"] == folder:
                        if not input_csv_row["プロジェクト ID"]:
                            output_rows.append(get_output_csv_row(input_csv_row))
                writer.writerows(sort_output_rows(output_rows))

        for project in project_list:
            # 結果出力CSVを作成
            with open(
                f'./output/{FILE_NAME}_{project}.csv',
                'w', encoding='utf-8', newline='\n'
            ) as output_csv:
                writer = csv.writer(output_csv)
                output_rows = []
                for input_csv_row in input_csv_rows:
                    if input_csv_row["プロジェクト ID"] == project:
                        output_rows.append(get_output_csv_row(input_csv_row))
                writer.writerows(sort_output_rows(output_rows))


if __name__ == "__main__":
    main()
