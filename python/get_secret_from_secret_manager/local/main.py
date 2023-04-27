"""Google Secret Managerからシークレットを取得する"""
import sys
from google.cloud import secretmanager

args = sys.argv
PROJECT_ID = args[1]
SECRET_ID = args[2]
VERSION_ID = args[3]
KEY_NAME = args[4]


def main():
    print(f"Start accessing secret {SECRET_ID}.")

    # Create the Secret Manager client.
    secret_client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    secret_name = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/{VERSION_ID}"

    # Access the secret version.
    access_secret_response = secret_client.access_secret_version(request={"name": secret_name})

    # write secret payload to local file.
    secret_payload = access_secret_response.payload.data.decode("UTF-8")
    # print("Plaintext: {}".format(payload))
    with open(f"{KEY_NAME}.json", mode='w', encoding='utf-8', newline='\n') as key_file:
        key_file.write(secret_payload)

    print("Finish.")


if __name__ == "__main__":
    main()
