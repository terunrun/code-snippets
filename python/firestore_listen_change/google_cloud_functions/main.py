"""Firestoreのドキュメントの変更をリッスンする"""
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/HEAD/firestore/cloud-client/snippets.py#L685
import json
import os
import threading

from google.cloud import firestore

PROJECT = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get('LOCATION', "asia-northeast1")

client = firestore.Client()

# Create an Event for notifying main thread.
delete_done = threading.Event()

# https://cloud.google.com/functions/docs/monitoring/logging?hl=ja#writing_structured_logs
def logging(level, msg):
    """Cloud Logging 用に構造化ログを作成する"""
    trace_header = ""

    # Build structured log messages as an object.
    global_log_fields = {}

    if trace_header and PROJECT:
        trace = trace_header.split("/")
        global_log_fields[
            "logging.googleapis.com/trace"
        ] = f"projects/{PROJECT}/traces/{trace[0]}"

    # Complete a structured log entry.
    entry = dict(
        severity=level,
        message=msg,
        # Log viewer accesses 'component' as jsonPayload.component'.
        component="arbitrary-property",
        **global_log_fields,
    )
    print(json.dumps(entry))


# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot, changes, read_time):
    print(u'Callback received query snapshot.')
    for col in col_snapshot:
        print(f'Received document snapshot: {col.id}')
    # print(u'Current cities in California: ')
    for change in changes:
        if change.type.name == 'ADDED':
            print(f'New: {change.document.id}')
        elif change.type.name == 'MODIFIED':
            print(f'Modified: {change.document.id}')
        elif change.type.name == 'REMOVED':
            print(f'Removed: {change.document.id}')
            delete_done.set()
        else:
            print(f'No Change: {change.document.id}')


# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f'Received document snapshot: {doc.id}')
    callback_done.set()


def firestoreListenChange(request):
    """メイン関数"""
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json:
        pass
    elif request_args:
        pass

    logging("INFO", f"Start listen Change...")

    col_query = client.collection(u'users')

    # Watch the collection query
    query_watch = col_query.on_snapshot(on_snapshot)

    logging("INFO", "Finish listen Change.")
    return "ok"
