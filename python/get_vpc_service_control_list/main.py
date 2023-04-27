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
FILE_NAME = args[1]


def main():
    # 対象JSONを読み込む
    with open(f"./{FILE_NAME}.json", "r", encoding="utf-8") as input_json:
        vpcsc_list = json.load(input_json)

        # 結果出力CSVを作成
        with open(f"./output_{FILE_NAME}.csv", 'w', encoding='utf-8', newline='\n') as output_csv:
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
                    ingress_policies = vpcsc["status"]["ingressPolicies"]

                    for i, ingress_policy in enumerate(ingress_policies):
                        policy_number = i + 1
                        member_type = ""
                        principal = ""
                        address = ""
                        domain = ""

                        if "ingressFrom" in ingress_policy:
                            # print(ingress_policy["ingressFrom"])

                            if "identityType" in ingress_policy["ingressFrom"]:
                                principal = ingress_policy["ingressFrom"]["identityType"]
                            elif "identities" in ingress_policy["ingressFrom"]:
                                for identity in ingress_policy["ingressFrom"]["identities"]:
                                    if ":" not in identity:
                                        principal = identity
                                    else:
                                        splitted_identity = identity.split(":")
                                        if splitted_identity[0] == "deleted":
                                            member_type = splitted_identity[1]
                                            principal = splitted_identity[2]
                                        else:
                                            member_type = splitted_identity[0]
                                            principal = splitted_identity[1]
                                        if "@" in principal:
                                            splitted_principal = principal.split("@")
                                            address = splitted_principal[0]
                                            domain = splitted_principal[1]
                            writer.writerow(
                                [member_type, principal, address, domain, vpcsc["name"], vpcsc["title"], "内向き", policy_number]
                            )

                # 外向きポリシーを取得
                # NOTE: 外向きポリシーが存在しない場合はegressPolicies要素が存在しない
                if "egressPolicies" in vpcsc["status"]:
                    egress_policies = vpcsc["status"]["egressPolicies"]

                    for i, egress_policy in enumerate(egress_policies):
                        policy_number = i + 1
                        member_type = ""
                        principal = ""
                        address = ""
                        domain = ""

                        if "egressFrom" in egress_policy:
                            # print(egress_policy["egressFrom"])

                            if "identityType" in egress_policy["egressFrom"]:
                                principal = egress_policy["egressFrom"]["identityType"]
                                writer.writerow(
                                    [member_type, principal, address, domain, vpcsc["name"], vpcsc["title"], "外向き", policy_number]
                                )
                            elif "identities" in egress_policy["egressFrom"]:
                                for identity in egress_policy["egressFrom"]["identities"]:
                                    # TODO: 関数化する
                                    if ":" not in identity:
                                        principal = identity
                                    else:
                                        splitted_identity = identity.split(":")
                                        if splitted_identity[0] == "deleted":
                                            member_type = splitted_identity[1]
                                            principal = splitted_identity[2]
                                        else:
                                            member_type = splitted_identity[0]
                                            principal = splitted_identity[1]
                                        if "@" in principal:
                                            splitted_principal = principal.split("@")
                                            address = splitted_principal[0]
                                            domain = splitted_principal[1]
                                    writer.writerow(
                                        [member_type, principal, address, domain, vpcsc["name"], vpcsc["title"], "外向き", policy_number]
                                    )


if __name__ == "__main__":
    main()
