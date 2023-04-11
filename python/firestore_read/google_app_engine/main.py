from flask import Flask
from google.cloud import firestore

app = Flask(__name__)
client = firestore.Client()

@app.route('/')
def firestoreRead():
    print("Start Read")

    # データを読み取る
    users_ref = client.collection(u'users')
    docs = users_ref.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

    print("Finish Write")
    return "ok"

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)