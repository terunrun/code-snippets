"""Google Cloud Storageのバケットにファイルを格納し、それを取得する"""

import datetime
import json
import os
import sys

from google.cloud import storage

args = sys.argv
PROJECT = args[1]
BUCKET_ID = args[2]

output_contents = [
    {
        "key": "value1",
        "nest_key": [{"in_nest_key1": "in_nest_value1", "in_nest_key2": "in_nest_value2",}]
    },
    {
        "key": "value2",
        "nest_key": [{"in_nest_key1": "in_nest_value3", "in_nest_key4": "in_nest_value4",}]
    },
]


def main():
    storage_client = storage.Client()

    dt_now_jst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    date = dt_now_jst.strftime('%Y%m%d%H%M%S')

    # Google Cloud Storageのバケットにファイルを格納する
    bucket = storage_client.get_bucket(BUCKET_ID)
    filename = f"sample_{date}.json"

    with open(f"./{filename}", 'w', encoding='utf-8', newline='\n') as out:
        for target in output_contents:
            json.dump(target, out)
            out.write("\n")

    blob = storage.Blob(f"target_folder/{filename}", bucket)
    blob.upload_from_filename(f"./{filename}", "application/json")
    os.remove(f"./{filename}")
    print(f"Successfully put {filename} to {BUCKET_ID}")

    # Google Cloud Storageのバケットのファイルを取得する
    blob_file = bucket.blob(f"target_folder/{filename}")
    blob_file.download_to_filename(f"./{filename}")
    print(f"Successfully get {filename} from {BUCKET_ID}")

    # Google Cloud Storageのバケットのファイルを直接取得する
    txt_file = (blob_file.download_as_text()).split('\n')
    nest_value_list = []
    for txt in txt_file:
        if not txt:
            break
        json_file = json.loads(txt)
        for nest_key in json_file["nest_key"]:
            nest_value_list.append(nest_key["in_nest_key1"])
    print(nest_value_list)


if __name__ == "__main__":
    main()
