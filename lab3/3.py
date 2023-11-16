"""
Номер ИСУ: 413732
Вариант (%5): 2

Студент Вася очень любит курс «Компьютерная безопасность». Однажды Васе
задали домашнее задание зашифровать данные, переданные в сообщении. Недолго
думая, Вася решил заменить все целые числа на функцию от этого числа. Функцию
он придумал не сложную 4𝑥^2 − 7, где 𝑥 − исходное число.
Помогите Васе с егодомашним заданием.

Предусмотреть ситуацию, когда в тексте будут не только целые числа, но и любые символы
"""

import re
import typing as t

from lab3.tests import TestCase, TestGroup


def _replace_callback(match_obj: t.Match[str]) -> str:
    """Processes each found integer"""
    x = int(match_obj.group(0))
    return str(4 * x ** 2 - 7)


def solution(pattern: t.Pattern, string: str) -> str:
    result = pattern.sub(_replace_callback, string)
    return result


solution_pattern = re.compile(r'-?\b(?<!\.)\d+(?!\.)\b')

test_1 = TestCase(string='20 + 22 = 42', answer='1593 + 1929 = 7049')
test_2 = TestCase(string='20.0 + 22.0 = 42.0', answer='20.0 + 22.0 = 42.0')
test_3 = TestCase(string='-20 + (-22) = -42', answer='1593 + (1929) = 7049')
test_4 = TestCase(
    string='Start velocity: 5, acceleration: 1 -> Speed after 2 seconds: 7',
    answer='Start velocity: 93, acceleration: -3 -> Speed after 9 seconds: 189'
)
test_5 = TestCase(
    string='Corner cases: .123; -123.45; -.987 1.0; 0.0.0.0.1; 123AAAA123. Normal cases: 5 -4 123',
    answer='Corner cases: .123; -123.45; -.987 1.0; 0.0.0.0.1; 123AAAA123. Normal cases: 93 57 60509'
)

test_group = TestGroup(name='Шифрование целых чисел', pattern=solution_pattern, function=solution)
test_group.add_tests(test_1, test_2, test_3, test_4, test_5)
test_group.run()

test_group.run_on_users_input()