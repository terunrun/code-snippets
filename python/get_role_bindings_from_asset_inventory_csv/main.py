"""Google CloudのAsset InventoryのCSVを読み込み、ポリシー列を展開して列を並べ替えた結果をCSV出力する"""

import csv
import json
import re
import sys


# 実行時引数としてAsset Inventoryの画面から取得した対象CSVを受け取る
args = sys.argv
file_name = args[1]


def main():
    # 対象CSVをヘッダー抜きで読み込む
    with open(f"./{file_name}.csv", 'rt') as input_csv:
        # header = next(csv.reader(input_csv))
        # input_csv_rows = csv.reader(input_csv)
        dict_reader = csv.DictReader(input_csv)
        input_csv_rows = [row for row in dict_reader]

        # 結果出力CSVを作成
        with open(f"./output_{file_name}.csv", 'w') as output_csv:
            writer = csv.writer(output_csv)
            writer.writerow([
                "タイプ", "プリンシパル", "アドレス", "ドメイン", "リソースの種類", "組織",
                "フォルダ", "プロジェクト ID", "リソース", "ロール", "ポリシー", "説明"
            ])

            for input_csv_row in input_csv_rows:
                # ポリシー列文字列を辞書形式に変換できるように編集
                # NOTE: 最後のreplaceはroleごとに分割したいために実行
                regex_policy = re.sub(
                    ',condition:[a-zA-Z0-9_]*}', '","condition":""}', re.sub(
                    '\],auditConfigs:\[\],etag:}', '', re.sub(
                    '{version:[0-9]+,bindings:\[', '', input_csv_row["ポリシー"]
                )))
                quoted_regex_policy = regex_policy \
                    .replace(",members:[", '","members":"[') \
                    .replace("role:", '"role":"') \
                    .replace(',{"role":', '|{"role":')

                # roleとmemberのbindingリストを作成
                role_bindings_list = quoted_regex_policy.split("|")

                for role_bindings in role_bindings_list:
                    role_bindings_json = json.loads(role_bindings)

                    # roleにbindingされたmemberのリストを作成
                    members = role_bindings_json["members"].split(",")

                    for member in members:
                        # NOTE: リストごと辞書値化されたことで前後に不要な[]があるため削除
                        replaced_member = member.replace("[", "").replace("]", "")

                        type = ""
                        principal = ""
                        address = ""
                        domain =""
                        # NOTE: allUsersなどの場合は:の後がなくsplitできないため処理を分ける
                        if ":" not in replaced_member:
                            principal = replaced_member
                        else:
                            splitted_replaced_members = replaced_member.split(":")
                            if splitted_replaced_members[0] == "deleted":
                                type = splitted_replaced_members[1]
                                principal = splitted_replaced_members[2]
                            else:
                                type = splitted_replaced_members[0]
                                principal = splitted_replaced_members[1]
                            if "@" in principal:
                                splitted_principal = principal.split("@")
                                address = splitted_principal[0]
                                domain = splitted_principal[1]

                        writer.writerow([
                                            type,
                                            principal,
                                            address,
                                            domain,
                                            input_csv_row["リソースの種類"],
                                            input_csv_row["組織"],
                                            input_csv_row["フォルダ"],
                                            input_csv_row["プロジェクト ID"],
                                            input_csv_row["リソース"],
                                            role_bindings_json["role"],
                                            input_csv_row["ポリシー"],
                                            input_csv_row["説明"],
                                        ])


if __name__ == "__main__":
    main()
