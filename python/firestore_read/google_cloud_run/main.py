import os
from flask import Flask

from google.cloud import firestore

PROJECT = os.environ.get("PROJECT")
LOCATION = os.environ.get('LOCATION', "asia-northeast1")

app = Flask(__name__)
client = firestore.Client()

@app.route("/")
def firestoreRead():
    name = os.environ.get("NAME", "World")
    print("Start Read")

    # データを読み取る
    users_ref = client.collection(u'users')
    docs = users_ref.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

    print("Finish Write")
    return "ok"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

