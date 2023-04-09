def split(target_list, number):
    """
    リストをサブリストに分割する
    :param target_list: リスト
    :param number     : サブリストの要素数
    :return:
    """
    for idx in range(0, len(target_list), number):
        yield target_list[idx:idx + number]

def split_list():
    target_list = ["12334", "23456", "00000", "11111", "22222", "22222"]
    print(f"target_list: {target_list}")
    results = list(split(target_list, 3))
    print(results)
    for i, result in enumerate(results):
        print(f"splitted target_list {i}: {result}")
    for idx in range(0, len(target_list), 3):
        print(target_list[idx:idx + 3])

    print("\n")

    target_list_no_duplicate = list(set(target_list))
    print(f"target_list_no_duplicate: {target_list_no_duplicate}")
    results = list(split(target_list_no_duplicate, 3))
    for i, result in enumerate(results):
        print(f"splitted target_list {i}: {result}")
    for idx in range(0, len(target_list_no_duplicate), 3):
        print(target_list_no_duplicate[idx:idx + 3])


if __name__ == "__main__":
    split_list()
