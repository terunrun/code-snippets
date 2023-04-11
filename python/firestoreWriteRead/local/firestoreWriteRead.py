"""Firestoreにデータの読み書きを行う"""
import os
from google.cloud import firestore

PROJECT = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get("LOCATION", "asia-northeast1")

client = firestore.Client()

print("Start Write")

# データを書き込む
doc_ref = client.collection(u'users').document(u'alovelace')
doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1815
})

# 別のデータを書き込む
doc_ref = client.collection(u'users').document(u'aturing')
doc_ref.set({
    u'first': u'Alan',
    u'middle': u'Mathison',
    u'last': u'Turing',
    u'born': 1912
})

print("Finish Write")
print("Start Read")

# データを読み取る
users_ref = client.collection(u'users')
docs = users_ref.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')

print("Finish Read")
