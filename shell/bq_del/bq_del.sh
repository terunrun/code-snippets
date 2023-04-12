#! /bin/bash
# usage: ./bq_del.sh {PROJECT_ID} {DATASET}
# 同ディレクトリ階層に削除対象テーブルを記載したbq_del_list.txtを配置して実行する
# bq ls --dataset_id {PROJECT}:{DATASET} の実行結果を利用すると記載がしやすい

PROJECT_ID=$1
DATASET=$2

if [ -z "$PROJECT_ID" ];then
    echo "PROJECT_ID is empty"
    exit 1;
fi

if [ -z "$DATASET" ];then
    echo "DATASET is empty"
    exit 1;
fi

while read line
do
    echo start deleting ${line} ...
    bq query --nouse_legacy_sql "DELETE FROM `'${PROJECT_ID}'.'${DATASET}'.'${line}'` WHERE TRUE"
    wait
    echo finish deleting ${line}
done < bq_rm_list.txt
