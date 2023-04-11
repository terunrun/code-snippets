"""BigQueryへクエリを発行する"""

from google.cloud import bigquery

PROJECT = 'sandbox-terunrun-dev'
LOCATION = 'asia-northeast1'
DESTINATION_DATASET = 'sample_dataset'
DESTINATION_TABLE = 'sample_table'
QUERY_PARAMS_VALUES = {'date': '20210222'}
TIME_PARTITIONING_TYPE = bigquery.TimePartitioningType.DAY
TIME_PARTITIONING_COLUMN = 'time_partitioning_column'
CLUSTER_FIELDS = []


def run_bq_query():
    bigquery_client = bigquery.Client(PROJECT)

    # クエリファイルを文字列として展開
    with open(f"./sql/{DESTINATION_TABLE}.sql", "r", encoding="utf-8") as file:
        query = file.read()
        print(f'query:"{query}"')

    # クエリ発行時の設定
    job_config = bigquery.QueryJobConfig()
    job_config.destination = bigquery_client.dataset(DESTINATION_DATASET).table(DESTINATION_TABLE)
    job_config.write_disposition = "WRITE_TRUNCATE"
    job_config.create_disposition = "CREATE_IF_NEEDED"
    job_config.use_legacy_sql = False

    # クエリパラメータの設定
    if QUERY_PARAMS_VALUES:
        query_params = []
        for key, value in QUERY_PARAMS_VALUES.items():
            print(f"query parameter name: @{key}, value: {value}")
            query_params.append(bigquery.ScalarQueryParameter(key, "STRING", value))
        job_config.query_parameters = query_params

    # パーティションの設定
    if TIME_PARTITIONING_COLUMN:
        print(f"time_partitioning_column: {TIME_PARTITIONING_COLUMN}")
        job_config.time_partitioning = bigquery.TimePartitioning(
            type_=TIME_PARTITIONING_TYPE,
            field=TIME_PARTITIONING_COLUMN,
        )
        # クラスタの設定
        if CLUSTER_FIELDS:
            print(f"cluster_fields: {CLUSTER_FIELDS}")
            job_config.clustering_fields = CLUSTER_FIELDS

    # クエリ発行
    query_job = bigquery_client.query(query, job_config=job_config, location=LOCATION)
    query_job.result()


if __name__ == "__main__":
    run_bq_query()
