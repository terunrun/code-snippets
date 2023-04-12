#! /bin/sh
# usage: ./gunzip.sh ${TARGET_PATH}

TARGET_PATH=$1

if [ -z "$TARGET_PATH" ];then
    echo "Please Specify target path"
    exit 1;
fi

for file in `ls $TARGET_PATH`; do
  echo "gunzip ${TARGET_PATH}/${file}"
  /usr/bin/gunzip ${TARGET_PATH}/${file}
done

for file in `ls $TARGET_PATH`; do
  echo "concat ${TARGET_PATH}/${file}"
  cat ${TARGET_PATH}/${file} >> ${TARGET_PATH}/merged_file.csv
done
