"""Google CloudのIAMポリシーを出力する"""
# https://cloud.google.com/python/docs/reference/cloudresourcemanager/latest/

import sys
from google.cloud import resourcemanager_v3
from google.iam.v1 import iam_policy_pb2  # type: ignore

args = sys.argv
TARGET_ORGANIZATION = args[1]


def main():
    organization_client = resourcemanager_v3.OrganizationsClient()
    folder_client = resourcemanager_v3.FoldersClient()
    project_client = resourcemanager_v3.ProjectsClient()

    # 組織リソースのIAMポリシーを表示する
    request = iam_policy_pb2.GetIamPolicyRequest(resource=f"organizations/{TARGET_ORGANIZATION}")
    organization_iam_policy = organization_client.get_iam_policy(request=request)
    print(organization_iam_policy)

    #TODO: 組織直下のプロジェクトに対応する

    # フォルダリソースのIAMポリシーを表示する
    request = resourcemanager_v3.ListFoldersRequest(parent=f"organizations/{TARGET_ORGANIZATION}")
    folders = folder_client.list_folders(request=request)
    # TODO: フォルダのネストに対応する
    for folder in folders:
        print(f"Target folder: {folder.name}")
        request = iam_policy_pb2.GetIamPolicyRequest(resource=folder.name)
        folder_iam_policy = folder_client.get_iam_policy(request=request)
        print(folder_iam_policy)

        # プロジェクトリソースのIAMポリシーを表示
        request = resourcemanager_v3.ListProjectsRequest(parent=folder.name)
        projects = project_client.list_projects(request=request)
        for project in projects:
            print(f"Target project: {project.name}")
            request = iam_policy_pb2.GetIamPolicyRequest(resource=project.name)
            project_iam_policy = project_client.get_iam_policy(request=request)
            print(project_iam_policy)


if __name__ == "__main__":
    main()
