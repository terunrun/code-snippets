"""Google Secret Managerからシークレットを取得する"""
import json
import os
from flask import Flask, request, jsonify
from google.cloud import secretmanager

PROJECT_ID = os.environ.get("PROJECT_ID")
SECRET_ID = os.environ.get("SECRET_ID", KEY_NAME)
VERSION_ID = os.environ.get("VERSION_ID", "latest")
KEY_NAME = os.environ.get("KEY_NAME", "credential")

trace_header = ""
# Create the Secret Manager client.
secret_client = secretmanager.SecretManagerServiceClient()

def logging(level, msg):
    """create structured log for Cloud Logging"""
    # Build structured log messages as an object.
    global_log_fields = {}

    if trace_header and PROJECT_ID:
        trace = trace_header.split("/")
        global_log_fields[
            "logging.googleapis.com/trace"
        ] = f"projects/{PROJECT_ID}/traces/{trace[0]}"

    # Complete a structured log entry.
    entry = dict(
        severity=level,
        message=msg,
        # Log viewer accesses 'component' as jsonPayload.component'.
        component="arbitrary-property",
        **global_log_fields,
    )
    print(json.dumps(entry))


def main(request):
    logging("INFO", f"Start accessing secret {SECRET_ID}.")

    # Build the resource name of the secret version.
    secret_name = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/{VERSION_ID}"

    # Access the secret version.
    access_secret_response = secret_client.access_secret_version(request={"name": secret_name})

    # write secret payload to local file.
    secret_payload = access_secret_response.payload.data.decode("UTF-8")
    # logging("INFO", "Plaintext: {}".format(payload))
    key_file_name = f"/tmp/{KEY_NAME}.json"
    with open(key_file_name, mode='w', encoding="UTF-8") as key_file:
        key_file.write(secret_payload)

    logging("INFO", f"Finish accessing secret. {key_file_name} is successfully created.")
    os.remove(key_file_name)

    return jsonify({
        'status': "ok",
    })
