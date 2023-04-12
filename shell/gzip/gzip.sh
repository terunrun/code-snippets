#! /bin/sh
# usage: ./gzip.sh ${TARGET_PATH}
# gzip対象ファイル名を記載したlist.txtを配置して実行する

TARGET_PATH=$1

if [ -z "$TARGET_PATH" ];then
    echo "Please Specify target path"
    exit 1;
fi

while read line
do
    /usr/bin/gzip ${TARGET_PATH}/${line}
    wait
done < list.txt
