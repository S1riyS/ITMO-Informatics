"""
Номер ИСУ: 413732
Глаза (%6 = 2): "X"
Нос   (%4 = 0): "-"
Рот   (%7 = 4): "\"
Смайлик: "X-\"
"""

import re
import typing as t

from lab3.tests import TestGroup, TestCase


def solution(pattern: t.Pattern, string: str) -> str:
    found_substrings = pattern.findall(string)
    result = str(len(found_substrings))
    return result


solution_pattern = re.compile(r'X-\\')

test_1 = TestCase(string=r'Hello X-\, how are you doing X-\?', answer='2')
test_2 = TestCase(string=r'Hello X-\, how are you doing X-\X-\X-\X-\.', answer='5')
test_3 = TestCase(string=r'Hello X-\, how are you doing X-\? ALL RIGHT X-\?', answer='3')
test_4 = TestCase(string=r'XX--\\_X-\_X-\__X--\_X-\___X-\.', answer='4')
test_5 = TestCase(string=r'There are no emojis, only sadness', answer='0')

test_group = TestGroup(name='Подсчет количества смайликов', pattern=solution_pattern, function=solution)
test_group.add_tests(test_1, test_2, test_3, test_4, test_5)
test_group.run()

test_group.run_on_users_input()
