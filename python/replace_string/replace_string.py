"""与えられたファイルを読み取り、文字列を置換して別のファイルに書き込む"""

import re
import sys
import google.auth

# 実行時引数として置換対象文字列を記載したファイル名を受け取る
args = sys.argv
source_object = args[1]
target_file = source_object + "_replaced"


def replace_string():
    with open(f"./{source_object}", mode="r", encoding="utf-8") as source_file:
        strings_from_file = source_file.read()
        # print(f"in: {strings_from_file}")

        # ファイルに含まれる文字列から正規表現にマッチする文字列を取得してリスト化
        # https://qiita.com/luohao0404/items/7135b2b96f9b0b196bf3
        # https://note.nkmk.me/python-str-extract/
        target_strings_org = re.findall(r'\"\d+\-\d*\"', strings_from_file)
        # リストの重複を削除
        # https://note.nkmk.me/python-list-unique-duplicate/
        target_strings = list(set(target_strings_org))
        # print(f"target_strings: {target_strings}")

        # 置換対象文字列に対応する置換後文字列を辞書に追加
        replacers = {'{}': 'null'}
        for target_string in target_strings:
            # https://office54.net/python/basic/str-insert-character
            replacers[target_string] = (target_string[:1] + "_" + target_string[1:]).replace("-", "_")
        print(f"replacers: {replacers}")

        # リストの要素分繰り返す
        # https://note.nkmk.me/python-dict-keys-values-items/
        # ファイル内の規定文字列を置換する
        # https://note.nkmk.me/python-str-replace-translate-re-sub/
        for k, v in replacers.items():
            strings_from_file = strings_from_file.replace(k, v)
            # print(f"work: {string_from_file}")

        # # 置換後のファイルを保存する
        # # https://note.nkmk.me/python-file-io-open-with/
        with open(target_file, mode="w", encoding="utf-8") as output_file:
            output_file.write(strings_from_file)


if __name__ == "__main__":
    replace_string()
