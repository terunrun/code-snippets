def split(l, n):
    """
    リストをサブリストに分割する
    :param l: リスト
    :param n: サブリストの要素数
    :return:
    """
    for idx in range(0, len(l), n):
        yield l[idx:idx + n]

def split_list():
    # l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    l = ["12334", "23456", "00000", "11111", "22222", "22222"]
    result = list(split(l, 3))
    print(result) # [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
    for i, r in enumerate(result):
        print(f"splitted target_list {i}: {result[i]}")

    for idx in range(0, len(l), 3):
        l[idx:idx + 3]
    print(l) # [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]

    l_no_duplicate = set(l)
    print(l_no_duplicate)
    print(type(l_no_duplicate))
    print(type(list(l_no_duplicate)))
    for r in l_no_duplicate:
        print(r)


if __name__ == "__main__":
    split_list()
