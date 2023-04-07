
"""指定したプロジェクトのBigQueryのテーブル一覧を取得する"""
"""https://cloud.google.com/bigquery/docs/listing-datasets?hl=ja#python"""

import csv
import sys
from google.cloud import bigquery

args = sys.argv
PROJECT = args[1]


def main():
    bigquery_client = bigquery.Client()
    datasets = list(bigquery_client.list_datasets())
    if not datasets:
        print(f"project:{PROJECT} does not contain any datasets.")

    with open(f'bq_tables_{PROJECT}.csv', 'w') as output_file:
        writer = csv.writer(output_file)
        result_array = []
        for dataset in datasets:
            # クライアントライブラリlist_tablesで得られるTableListItemでは得られない情報がある
            QUERY = f"SELECT * FROM `{PROJECT}.{dataset.dataset_id}.__TABLES__`;"
            # dataset_info = bigquery_client.get_dataset(dataset_ref=dataset.reference)
            # query_job = bigquery_client.query(QUERY, location=dataset_info.location)
            query_job = bigquery_client.query(QUERY)
            rows = query_job.result()  # Waits for query to finish
            for row in rows:
                array = []
                for item in row:
                    array.append(str(item))
                result_array.append(array)
        writer.writerows(result_array)


if __name__ == "__main__":
    main()
