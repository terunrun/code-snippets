"""Google CloudのVPC Service ControlのjSONを読み込み、結果をCSV出力する"""
# インプットは
# gcloud access-context-manager policies list --organization {org_id}
# でpolicy_idを取得し、
# gcloud access-context-manager perimeters list --format=json --policy={policy_id}
# で取得する


import csv
import json
import sys


# 実行時引数として対象を受け取る
args = sys.argv
file_name = args[1]


def main():
    # 対象JSONを読み込む
    with open(f"./{file_name}.json", 'r') as input_json:
        vpcsc_list = json.load(input_json)

        # 結果出力CSVを作成
        with open(f"./output_{file_name}.csv", 'w') as output_csv:
            writer = csv.writer(output_csv)
            writer.writerow(["タイプ", "プリンシパル", "アドレス", "ドメイン", "名前", "タイトル", "内向き/外向き", "ポリシー番号"])

            for vpcsc in vpcsc_list:
                # NOTE: 境界のタイプ「通常」はperimeterType要素が存在しない
                if "perimeterType" in vpcsc:
                    # NOTE: 境界のタイプ「ブリッジ」はポリシーがない
                    if vpcsc["perimeterType"] == "PERIMETER_TYPE_BRIDGE":
                        continue

                # 内向きポリシーを取得
                # NOTE: 内向きポリシーが存在しない場合はingressPolicies要素が存在しない
                if "ingressPolicies" in vpcsc["status"]:
                    ingressPolicies = vpcsc["status"]["ingressPolicies"]

                    for i, ingressPolicy in enumerate(ingressPolicies):
                        policy_number = i + 1
                        type = ""
                        principal = ""
                        address = ""
                        domain = ""

                        if "ingressFrom" in ingressPolicy:
                            # print(ingressPolicy["ingressFrom"])

                            if "identityType" in ingressPolicy["ingressFrom"]:
                                principal = ingressPolicy["ingressFrom"]["identityType"]
                            elif "identities" in ingressPolicy["ingressFrom"]:
                                for identity in ingressPolicy["ingressFrom"]["identities"]:
                                    if ":" not in identity:
                                        principal = identity
                                    else:
                                        splitted_identity = identity.split(":")
                                        if splitted_identity[0] == "deleted":
                                            type = splitted_identity[1]
                                            principal = splitted_identity[2]
                                        else:
                                            type = splitted_identity[0]
                                            principal = splitted_identity[1]
                                        if "@" in principal:
                                            splitted_principal = principal.split("@")
                                            address = splitted_principal[0]
                                            domain = splitted_principal[1]
                            writer.writerow([type, principal, address, domain, vpcsc["name"], vpcsc["title"], "内向き", policy_number])

                # 外向きポリシーを取得
                # NOTE: 外向きポリシーが存在しない場合はegressPolicies要素が存在しない
                if "egressPolicies" in vpcsc["status"]:
                    egressPolicies = vpcsc["status"]["egressPolicies"]

                    for i, egressPolicy in enumerate(egressPolicies):
                        policy_number = i + 1
                        type = ""
                        principal = ""
                        address = ""
                        domain = ""

                        if "egressFrom" in egressPolicy:
                            # print(egressPolicy["egressFrom"])

                            if "identityType" in egressPolicy["egressFrom"]:
                                principal = egressPolicy["egressFrom"]["identityType"]
                                writer.writerow([type, principal, address, domain, vpcsc["name"], vpcsc["title"], "外向き", policy_number])
                            elif "identities" in egressPolicy["egressFrom"]:
                                for identity in egressPolicy["egressFrom"]["identities"]:
                                    # TODO: 関数化する
                                    if ":" not in identity:
                                        principal = identity
                                    else:
                                        splitted_identity = identity.split(":")
                                        if splitted_identity[0] == "deleted":
                                            type = splitted_identity[1]
                                            principal = splitted_identity[2]
                                        else:
                                            type = splitted_identity[0]
                                            principal = splitted_identity[1]
                                        if "@" in principal:
                                            splitted_principal = principal.split("@")
                                            address = splitted_principal[0]
                                            domain = splitted_principal[1]
                                    writer.writerow([type, principal, address, domain, vpcsc["name"], vpcsc["title"], "外向き", policy_number])


if __name__ == "__main__":
    main()
