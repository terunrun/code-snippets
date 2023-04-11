"""Firestoreのドキュメントを削除する"""
import os
import sys
from google.cloud import firestore

args = sys.argv
if len(args) < 3:
    print(f"Arguments are short. Given {len(args)-1}. Required 2.")
    sys.exit()

PROJECT = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get("LOCATION", "asia-northeast1")

# インスタンスを初期化する
client = firestore.Client()

print("Start Delete")

target_collection = args[1]
try:
    target_document = args[2]
    doc_ref = client.collection(target_collection).document(target_document)
except:
    doc_ref = client.collection(target_collection)

# データを削除する
doc_ref.delete()

print("Finish Delete")
