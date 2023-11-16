"""
32 % 36 = 32

JSON -> YAML
День недели: Суббота

Задание:
Написать программу на языке Python 3.x, которая бы осуществляла
парсинг и конвертацию исходного файла в новый путём простой
замены метасимволов исходного формата на метасимволы
результирующего формата
"""

import typing as t

from lab4._base_converter import BaseConverter


class MetasymbolsReplacementConverter(BaseConverter):
    def __init__(self, filename):
        super().__init__(filename)
        self.__OUTPUT_TAB_SIZE = 2

        self.__tabs_counter = 0
        self.__list_mode = False
        self.__add_dash = False

    def _process_data(self) -> None:
        raw_lines = self._file_data.split('\n')[1:-1]
        lines: t.List[str] = list(map(lambda x: x.strip(), raw_lines))

        for index, line in enumerate(lines):
            if '{' in line:
                self.__tabs_counter += 1
                # If we are in list mode and there is a "{" it means new object in list has started -> adding dash
                if self.__list_mode:
                    self.__add_dash = True
            elif '}' in line:
                self.__tabs_counter -= 1
            elif ']' in line:
                self.__tabs_counter -= 1
                self.__list_mode = False

            elif line.startswith('"'):
                # Extracting key and value from current line
                key, value = line.removesuffix(',').replace('\"', '').split(': ')
                if value == '[':
                    self.__add_item(key, '')
                    self.__list_mode = True
                    self.__tabs_counter += 1
                else:
                    self.__add_item(key, value)

    def __add_item(self, key: str, value: str) -> None:
        _tabs_to_subtract = 0

        # Formatting key - value pair
        current_line = f'{key}: {value}\n'

        # Adding dash if needed
        if self.__add_dash:
            self.__add_dash = False
            _tabs_to_subtract = 1
            current_line = '- ' + current_line

        # Adding tabs
        tabs = (' ' * (self.__OUTPUT_TAB_SIZE - _tabs_to_subtract)) * self.__tabs_counter
        current_line = tabs + current_line

        # Adding line to result
        self._converted_data += current_line

if __name__ == '__main__':
    converter = MetasymbolsReplacementConverter('./resources/input.json')
    converter.convert('./results/MetasymbolsReplacementConverter.yaml')
