"""Firestoreにデータの読み書きを行う"""
import json
import os

from google.cloud import firestore

PROJECT = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get('LOCATION', "asia-northeast1")

client = firestore.Client()

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

def firestoreRead(request):
    """メイン関数"""
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json:
        pass
    elif request_args:
        pass

    logging("INFO", "Start Read")

    # データを読み取る
    users_ref = client.collection(u'users')
    docs = users_ref.stream()

    for doc in docs:
        logging("INFO", f'{doc.id} => {doc.to_dict()}')

    logging("INFO", "Finish Write")
    return "ok"
