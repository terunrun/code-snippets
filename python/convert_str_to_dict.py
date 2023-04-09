"""文字列を辞書に変換する"""

import ast

def convert_str_to_dict():
    target_string = '{ \
        "test_key": "test_value", \
        "test_key2": "test_value2", \
        "test_key3": "test_value3", \
        "test_key4": "test_value4", \
        "test_key5": "test_value5", \
    }'

    dictionary = ast.literal_eval(target_string)
    print(dictionary)
    for key, value in dictionary.items():
        print(f'key is {key}, value is {value}')


if __name__ == "__main__":
    convert_str_to_dict()
