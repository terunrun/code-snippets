"""BigQueryスケジュールクエリの情報をCSV出力する"""
#https://cloud.google.com/bigquery/docs/scheduling-queries?hl=ja#python_2
#https://cloud.google.com/python/docs/reference/bigquerydatatransfer/latest/google.cloud.bigquery_datatransfer_v1.services.data_transfer_service.DataTransferServiceClient

import csv
import sys
from google.cloud import bigquery_datatransfer
from google.cloud import resourcemanager_v3
from google.cloud import service_usage_v1

# 実行時引数として対象のGoogleCloud組織のIDを受け取る
args = sys.argv
TARGET_ORGANIZATION = args[1]


# TODO:全量をシステマチックに取得したい
# https://cloud.google.com/bigquery/docs/scheduling-queries?hl=ja#supported_regions
LOCATIONS = [
    "us-east5", "us-central1", "us-west4", "us-west2", "northamerica-northeast1",
    "us-east4", "us-west1", "us-west3","southamerica-east1", "southamerica-west1",
    "us-east1", "northamerica-northeast2", "asia-south2", "asia-east2",
    "asia-southeast2", "australia-southeast2", "asia-south1","asia-northeast2",
    "asia-northeast3", "asia-southeast1","australia-southeast1", "asia-east1",
    "asia-northeast1", "europe-west1", "europe-north1", "europe-west3", "europe-west2",
    "europe-southwest1", "europe-west8", "europe-west4", "europe-west9",
    "europe-central2", "europe-west6", "EU", "US"
]


def main():
    folder_client = resourcemanager_v3.FoldersClient()
    project_client = resourcemanager_v3.ProjectsClient()
    service_usage_client = service_usage_v1.ServiceUsageClient()
    transfer_client = bigquery_datatransfer.DataTransferServiceClient()

    with open(f"./output_bq_scheduled_query_{TARGET_ORGANIZATION}.csv", "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "プロジェクト", "スケジュールクエリ名", "ロケーション", "有効/無効", "ステータス", "ユーザー"
        ])

        # 組織配下のフォルダ一覧を取得する
        request = resourcemanager_v3.ListFoldersRequest(parent=f"organizations/{TARGET_ORGANIZATION}",)
        folders = folder_client.list_folders(request=request)

        for folder in folders:
            print(f"Target folder: {folder.name}")

            # フォルダ配下のプロジェクト一覧を取得する
            request = resourcemanager_v3.ListProjectsRequest(parent=folder.name,)
            projects = project_client.list_projects(request=request)

            for project in projects:
                print(f"\tTarget project: {project.project_id}")

                # BigQuery Data Transfer APIが有効化されているかどうかをチェック（無効の場合後続でエラーとなるため）
                request = service_usage_v1.GetServiceRequest(
                    name=f"{project.name}/services/bigquerydatatransfer.googleapis.com"
                )
                service = service_usage_client.get_service(request=request)
                if service.state != service_usage_v1.State.ENABLED:
                    print(
                        f"\t\tBigQuery Data Transfer API is not enabled in Project: {project.project_id}"
                    )
                    # writer.writerow(["なし", "なし", "なし", project, "なし", "なし", "なし", "なし"])
                    continue

                # プロジェクトごとにスケジュールクエリの一覧を取得
                for location in LOCATIONS:
                    print(f"\t\tTarget location: {location}")
                    transfer_configs = transfer_client.list_transfer_configs(
                        parent=f"projects/{project.project_id}/locations/{location}"
                    )

                    # スケジュールクエリごとに詳細を取得
                    for transfer_config in transfer_configs:
                        transfer_config_detail = transfer_client.get_transfer_config(name=transfer_config.name)
                        # print(f"\t\t\tDisplay Name: {transfer_config_detail.display_name}, Disabled: {transfer_config_detail.disabled}, State: {transfer_config_detail.state}, User: {transfer_config_detail.owner_info.email}")
                        # 取得した詳細から必要な情報を抽出してCSV出力
                        principal = transfer_config_detail.owner_info.email
                        address = ""
                        domain = ""
                        if "@" in transfer_config_detail.owner_info.email:
                            splitted_principal = principal.split("@")
                            address = splitted_principal[0]
                            domain = splitted_principal[1]
                        writer.writerow([
                            principal,
                            address,
                            domain,
                            project,
                            transfer_config_detail.display_name,
                            location, transfer_config_detail.disabled,
                            transfer_config_detail.state
                        ])


if __name__ == "__main__":
    main()
