"""Firestoreにデータの読み書きを行う"""
import os
import sys
from google.cloud import firestore

args = sys.argv
if len(args) < 3:
    print(f"Arguments are short. Given {len(args)-1}. Required 2.")
    sys.exit()

PROJECT = os.environ.get("PROJECT", "sample-project-yotani")
LOCATION = os.environ.get("LOCATION", "asia-northeast1")

# インスタンスを初期化する
client = firestore.Client()

print("Start Read")

target_collection = args[1]
try:
    target_document = args[2]
    doc_ref = client.collection(target_collection).document(target_document)
except:
    doc_ref = client.collection(target_collection)

# データを読み取る
docs = doc_ref.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')

print("Finish Read")
