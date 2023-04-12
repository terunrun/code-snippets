#! /bin/bash
# usage: ./bq_cp.sh {FROM_PROJECT_ID} {FROM_DATASET} {TO_PROJECT_ID} {TO_DATASET}
# 同ディレクトリ階層に削除対象テーブルを記載したbq_cp_list.txtを配置して実行する
# bq ls --dataset_id {PROJECT}:{DATASET} の実行結果を利用すると記載がしやすい

FROM_PROJECT_ID=$1
FROM_DATASET=$2
TO_PROJECT_ID=$3
TO_DATASET=$4

if [ -z "$FROM_PROJECT_ID" ];then
    echo "FROM_PROJECT_ID is empty"
    exit 1;
fi

if [ -z "$FROM_DATASET" ];then
    echo "FROM_DATASET is empty"
    exit 1;
fi

if [ -z "$TO_PROJECT_ID" ];then
    echo "TO_PROJECT_ID is empty"
    exit 1;
fi

if [ -z "$TO_DATASET" ];then
    echo "TO_DATASET is empty"
    exit 1;
fi

while read line
do
    echo start copying ${line} ...
    bq cp ${FROM_PROJECT_ID}:${FROM_DATASET}.${line} ${TO_PROJECT}:${TO_DATASET}.${line}
    wait
    echo finish copying ${line}
done < bq_cp_list.txt
