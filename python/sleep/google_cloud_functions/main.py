import json
import logging
import time
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

global_log_fields = {}

def logging(logLevel, msg):
    entry = dict(
        severity=logLevel,
        message=msg,
        # Log viewer accesses 'component' as jsonPayload.component'.
        component="arbitrary-property",
        **global_log_fields,
    )
    print(json.dumps(entry))

def sleep(request):
    logging("INFO", "start")
    start_time=datetime.now().strftime("%H:%M:%S")
    logging("INFO", f"{start_time}")
    try:
       time.sleep(240)
    except Exception:
        logging("ERROR", "The time is over")
    end_time=datetime.now().strftime("%H:%M:%S")
    logging("INFO", f"{end_time}")
    logging("INFO", "end")

    return jsonify({
        'status': "ok",
    })
