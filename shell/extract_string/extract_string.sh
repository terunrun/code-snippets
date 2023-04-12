#!/bin/bash
# usage: ./extract_string.sh

# ファイルの特定行から特定行までを出力
# https://hacknote.jp/archives/25401/
cat sample.txt | awk '/START/,/END/' > sample_.txt

# ファイルの行数をカウント（ファイルを直接wcするとファイル名も出力されるためまずはcatする）
line=(`cat sample_.txt | wc -l`)

# ファイルの特定行から特定行までを出力
# https://it-ojisan.tokyo/sh-sed-awk-line/
sed -n 2,$((line-1))p sample_.txt > result.csv

rm sample_.txt
