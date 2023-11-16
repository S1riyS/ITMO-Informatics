def read_file(filename: str) -> str:
    with open(filename, 'r', encoding="utf8") as file:
        return file.read()


def is_digit_1_to_9(digit: str) -> bool:
    return digit in ['1', '2', '3', '4', '5', '6', '7', '8', '9']
