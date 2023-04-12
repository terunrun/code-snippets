#! /bin/bash
# usage: ./bq_rm.sh {PROJECT_ID} {DATASET}
# 同ディレクトリ階層に削除対象テーブルを記載したbq_rm_list.txtを配置して実行する
# bq ls --dataset_id {PROJECT}:{DATASET} の実行結果を利用すると記載がしやすい

PROJECT=$1
DATASET=$2

if [ -z "$PROJECT" ];then
    echo "PROJECT is empty"
    exit 1;
fi

if [ -z "$DATASET" ];then
    echo "DATASET is empty"
    exit 1;
fi

while read line
do
    echo start removing ${line} ...
    bq rm -f $PROJECT:$DATASET.${line}
    wait
    echo finish removing ${line}
done < bq_del_list.txt