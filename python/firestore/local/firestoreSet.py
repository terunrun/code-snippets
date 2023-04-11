"""Firestoreのドキュメントを更新する"""
import os
import sys
from google.cloud import firestore

args = sys.argv
if len(args) < 3:
    print(f"Arguments are short. Given {len(args)-1}. Required 2.")
    sys.exit()
target_collection = args[1]
target_docunment = args[2]

PROJECT = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get("LOCATION", "asia-northeast1")

# インスタンスを初期化する
client = firestore.Client()

print("Start Set")

target_collection = args[1]
try:
    target_document = args[2]
    doc_ref = client.collection(target_collection).document(target_document)
except:
    doc_ref = client.collection(target_collection)

# データを書き込む

doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1815
})

print("Finish Set")
