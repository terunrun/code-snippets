# 入力の桁数を見る
# 桁数で処理を分岐
#     1桁処理
#     2桁処理
#     3桁処理
#     4〜6桁処理
#         頭3桁とそれ以降に分ける
#         頭3桁処理 + " thousand " + それ以降桁処理（000となるケースがあるので注意）
#     7〜9桁
#         頭3桁とそれ以降に分ける
#         頭3桁処理 + " million " + それ以降桁処理（4〜6桁処理）
#     10桁
#         頭3桁とそれ以降に分ける
#         頭1桁 + " billion " + それ以降桁処理（7〜9桁処理）

import sys

NUMBER_ENGILISH = {
    "0" : "zero",
    "1" : "one",
    "2" : "two",
    "3" : "three",
    "4" : "four",
    "5" : "five",
    "6" : "six",
    "7" : "seven",
    "8" : "eight",
    "9" : "nine",
    "10" : "ten",
    "11" : "eleven",
    "12" : "twelve",
    "13" : "thirteen",
    "14" : "fourteen",
    "15" : "fifteen",
    "16" : "sixteen",
    "17" : "seventeen",
    "18" : "eighteen",
    "19" : "nineteen",
    "20" : "twenty",
    "30" : "thirty",
    "40" : "forty",
    "50" : "fifty",
    "60" : "sixty",
    "70" : "seventy",
    "80" : "eighty",
    "90" : "ninety",
}

args = sys.argv
target_number = args[1]
target_number_string = str(target_number)

def get_one(target_number_string):
    if target_number_string == "0":
        return ""
    return NUMBER_ENGILISH[target_number_string]

def get_ten(target_number_string):
    if target_number_string[0] == "0":
        return get_one(target_number_string[1])
    if int(target_number_string) < 20:
        return NUMBER_ENGILISH[target_number_string]
    elif int(target_number_string) % 10 == 0:
        return NUMBER_ENGILISH[target_number_string]
    else:
        return NUMBER_ENGILISH[target_number_string[0] + "0"] + " " + NUMBER_ENGILISH[target_number_string[1]]

def get_hundred(target_number_string):
    if target_number_string[0] == "0":
        return get_ten(target_number_string[1:3])
    if int(target_number_string) % 100 == 0:
        return get_one(target_number_string[0]) + " hundred"
    else:
        return get_one(target_number_string[0]) + " hundred " + get_ten(target_number_string[1:3])

def get_thousand(target_number_string):
    first_three_digits = target_number_string[:-3]
    last_three_digits = target_number_string[-3:]
    if len(first_three_digits) == 1:
        return get_one(first_three_digits) + " thousand " + get_hundred(last_three_digits)
    elif len(first_three_digits) == 2:
        return get_ten(first_three_digits) + " thousand " + get_hundred(last_three_digits)
    elif len(first_three_digits) == 3:
        return get_hundred(first_three_digits) + " thousand " + get_hundred(last_three_digits)

def get_million(target_number_string):
    first_three_digits = target_number_string[:-6]
    last_six_digits = target_number_string[-6:]
    if len(first_three_digits) == 1:
        return get_one(first_three_digits) + " million " + get_thousand(last_six_digits)
    elif len(first_three_digits) == 2:
        return get_ten(first_three_digits) + " million "  + get_thousand(last_six_digits)
    elif len(first_three_digits) == 3:
        return get_hundred(first_three_digits) + " million " + get_thousand(last_six_digits)

def get_billion(target_number_string):
    first_three_digits = target_number_string[:-9]
    last_nine_digits = target_number_string[-9:]
    if len(first_three_digits) == 1:
        return get_one(first_three_digits) + " billion " + get_million(last_nine_digits)
    elif len(first_three_digits) == 2:
        return get_ten(first_three_digits) + " billion "  + get_million(last_nine_digits)
    elif len(first_three_digits) == 3:
        return get_hundred(first_three_digits) + " billion " + get_million(last_nine_digits)

def convert_number_to_english():
    if not str.isdigit(target_number_string):
        print(f"Please input number")
        sys.exit()

    print(f"input number is {target_number_string}")

    if len(target_number_string) == 1:
        print(NUMBER_ENGILISH[target_number_string])
    elif len(target_number_string) == 2:
        print(get_ten(target_number_string))
    elif len(target_number_string) == 3:
        print(get_hundred(target_number_string))
    elif (len(target_number_string) == 4) or (len(target_number_string) == 5) or (len(target_number_string) == 6):
        print((get_thousand(target_number_string)).rstrip())
    elif (len(target_number_string) == 7) or (len(target_number_string) == 8) or (len(target_number_string) == 9):
        print((get_million(target_number_string)).rstrip())
    elif len(target_number_string) == 10 or (len(target_number_string) == 11) or (len(target_number_string) == 12):
        print((get_billion(target_number_string)).rstrip())

if __name__ == "__main__":
    convert_number_to_english()
