from datetime import datetime


def int_prompt(msg: str):
    while True:
        try:
            res = int(input(msg))
            break
        except ValueError:
            print('Input must be a whole number')
    return res


def float_prompt(msg: str):
    while True:
        try:
            res = float(input(msg))
            break
        except ValueError:
            print('Input must be decimal number')
    return res


def datetime_prompt(msg: str, format_str: str) -> datetime:
    while True:
        try:
            res = datetime.strptime(input(msg), format_str)
            break
        except ValueError:
            print('Input must be in the given format')
    return res
