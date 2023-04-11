""""クライアントライブラリを利用してCloud Workflowsを起動する"""
import json
import os
import time

from flask import Flask, request, jsonify
# from google.cloud import storage
from google.cloud.workflows.executions_v1beta.types import executions
from google.cloud.workflows.executions import ExecutionsClient
from google.cloud.workflows.executions_v1.types import Execution


PROJECT = os.environ.get("PROJECT")
# BACKUP_BUCKET = os.environ.get("BACKUP_BUCKET")
# INTERFACE_PREFIX = os.environ.get("INTERFACE_PREFIX", "AppleMusic")
WORKFLOW = os.environ.get("WORKFLOW", "")

execution_client = ExecutionsClient()
# storage_client = storage.Client()
# Build structured log messages as an object.
global_log_fields = {}

app = Flask(__name__)

def logging(logLevel, msg):
    """Cloud Logging用に構造化ログを作成する"""
    entry = dict(
        severity=logLevel,
        message=msg,
        # Log viewer accesses 'component' as jsonPayload.component'.
        component="arbitrary-property",
        **global_log_fields,
    )
    print(json.dumps(entry))


def execute_workflow(parent, arguments):
    """与えられたワークフロー情報、ワークフロー引数でCloud Workflowsを実行する"""
    # リクエストボディを指定
    execution = Execution(argument=json.dumps(arguments))

    # ワークフロー実行リクエストを作成
    response = execution_client.create_execution(parent=parent, execution=execution)
    logging("INFO", f"Created execution: {response.name}")

    # Wait for execution to finish, then print results.
    execution_finished = False
    backoff_delay = 1  # Start wait with delay of 1 second
    logging("INFO", "Poll every second for result...")
    while not execution_finished:
        execution = execution_client.get_execution(request={"name": response.name})
        execution_finished = execution.state != executions.Execution.State.ACTIVE.value

        # If we haven't seen the result yet, wait a second.
        if not execution_finished:
            logging("INFO", "- Waiting for results...")
            time.sleep(backoff_delay)
            backoff_delay *= 2  # Double the delay to provide exponential backoff.
        else:
            logging("INFO", f"Workflow execution finished, status: {execution.state.name}")
            # logging("INFO", f"Workflow execution finished, result: {execution.result}")
    return execution.state


@app.route("/")
def invoke_workflows():

    # Add log correlation to nest all log messages.
    trace_header = request.headers.get("X-Cloud-Trace-Context")
    if trace_header and PROJECT:
        trace = trace_header.split("/")
        global_log_fields[
            "logging.googleapis.com/trace"
        ] = f"projects/{PROJECT}/traces/{trace[0]}"

    workflow_parent = f"projects/{PROJECT}/locations/us-central1/workflows/{WORKFLOW}"
    workflow_arguments = {}
    execution_status = execute_workflow(workflow_parent, workflow_arguments)
    if not execution_status or execution_status != executions.Execution.State.SUCCEEDED.value:
        logging("ERROR", "Workflow failed")
        raise Exception

    return jsonify({
        'status': "ok",
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
