"""指定したGoogle Cloud組織配下のプロジェクトで有効になっているサービスを出力する"""
"""https://cloud.google.com/python/docs/reference/serviceusage/latest/google.cloud.service_usage_v1.services.service_usage.ServiceUsageClient"""

import sys
from google.cloud import resourcemanager_v3
from google.cloud import service_usage_v1

args = sys.argv
target_organization = args[1]


def main():
    # Create a client
    folder_client = resourcemanager_v3.FoldersClient()
    project_client = resourcemanager_v3.ProjectsClient()
    service_usage_client = service_usage_v1.ServiceUsageClient()

    # 指定した組織配下のフォルダを取得する
    request = resourcemanager_v3.ListFoldersRequest(parent=f"organizations/{target_organization}",)
    folders = folder_client.list_folders(request=request)

    # TODO: フォルダのネストに対応する
    for folder in folders:
        print(f"Target folder: {folder.name}")

        # フォルダ配下のプロジェクトを取得する
        request = resourcemanager_v3.ListProjectsRequest(parent=folder.name,)
        projects = project_client.list_projects(request=request)

        for project in projects:
            print(f"Target project: {project.project_id}")

            # request = service_usage_v1.ListServicesRequest(
            #     parent=f"projects/{project.project_id}"
            # )
            # request = service_usage_v1.EnableServiceRequest(
            #     parent=f"projects/{project.project_id}"
            # )
            request = service_usage_v1.GetServiceRequest(
                name=f"{project.name}/services/bigquerydatatransfer.googleapis.com"
            )
            service = service_usage_client.get_service(request=request)

            # for service in services:
            #     print(service)
            print(f"Project: {project.project_id}, State: {service.state}")


if __name__ == "__main__":
    main()
