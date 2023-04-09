"""Google CloudのAccess Control ManagerのjSONを読み込み、結果をCSV出力する"""
# インプットは
# gcloud access-context-manager policies list --organization {org_id}
# でpolicy_idを取得し、
# gcloud access-context-manager levels list --format=json --policy={policy_id}
# で取得する


import csv
import json
import sys


# 実行時引数として対象を受け取る
args = sys.argv
FILE_NAME = args[1]


def main():
    # 対象JSONを読み込む
    with open(f"./{FILE_NAME}.json", "r", encoding="utf-8") as input_json:
        acm_list = json.load(input_json)

        # 結果出力CSVを作成
        with open(f"./output_{FILE_NAME}.csv", "w", encoding="utf-8") as output_csv:
            writer = csv.writer(output_csv)
            writer.writerow([ "タイプ", "プリンシパル", "アドレス", "ドメイン", "名前", "タイトル",])

            for acm in acm_list:
                # TODO: conditionsのリストが複数要素になる場合に対応する
                if "members" in acm["basic"]["conditions"][0]:
                    members = acm["basic"]["conditions"][0]["members"]
                    for member in members:
                        member_type = ""
                        principal = ""
                        address = ""
                        domain =""

                        if ":" not in member:
                            principal = member
                        else:
                            splitted_member = member.split(":")
                            if splitted_member[0] == "deleted":
                                member_type = splitted_member[1]
                                principal = splitted_member[2]
                            else:
                                member_type = splitted_member[0]
                                principal = splitted_member[1]
                            if "@" in principal:
                                splitted_principal = principal.split("@")
                                address = splitted_principal[0]
                                domain = splitted_principal[1]

                        writer.writerow(
                            [member_type, principal, address, domain, acm["name"], acm["title"]]
                        )


if __name__ == "__main__":
    main()
