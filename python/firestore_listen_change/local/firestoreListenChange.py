"""Firestoreのドキュメントの変更をリッスンする"""
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/HEAD/firestore/cloud-client/snippets.py#L756
import os
import sys
import time
import threading

from google.cloud import firestore

args = sys.argv
if len(args) < 2:
    print(f"Arguments are short. Given {len(args)-1}. Required 1.")
    sys.exit()

PROJECT = os.environ.get("GCP_PROJECT")
LOCATION = os.environ.get('LOCATION', "asia-northeast1")

client = firestore.Client()
delete_done = threading.Event()

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

# col_query = client.collection(u'cities').where(u'state', u'==', u'CA')
# col_query = client.collection(u'users').document(u'alovelace')

target_collection = args[1]
try:
    target_document = args[2]
    col_query = client.collection(target_collection).document(target_document)
except:
    col_query = client.collection(target_collection)

# Watch the collection query
query_watch = col_query.on_snapshot(on_snapshot)

# [END firestore_listen_query_changes]
# mtv_document = client.collection(u'cities').document(u'MTV')
# # Creating document
# mtv_document.set({
#     u'name': u'Mountain View',
#     u'state': u'CA',
#     u'country': u'USA',
#     u'capital': False,
#     u'population': 80000
# })
# sleep(1)

# # Modifying document
# mtv_document.update({
#     u'name': u'Mountain View',
#     u'state': u'CA',
#     u'country': u'USA',
#     u'capital': False,
#     u'population': 90000
# })
# sleep(1)

# # Delete document
# mtv_document.delete()

# # Wait for the callback captures the deletion.
# delete_done.wait(timeout=60)
# query_watch.unsubscribe()
while True:
    time.sleep(5)
    print('processing...')

print("Finish listen")
