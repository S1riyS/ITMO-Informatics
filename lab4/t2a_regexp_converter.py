import re
import typing as t

from lab4._base_converter import BaseConverter


class RegExpConverter(BaseConverter):
    def __init__(self, filename):
        super().__init__(filename)
        self.__INDENT_SIZE = 2

    def get_indent(self, match_obj: t.Match[str], json: str):
        """Returns indent at given position"""
        OPEN_BRACKETS = '{['
        CLOSE_BRACKETS = '}]'

        n = 0
        stop_index = match_obj.span()[1]

        for i in range(1, stop_index):
            current_symbol = json[i]
            if current_symbol in OPEN_BRACKETS:
                n += 1
            elif current_symbol in CLOSE_BRACKETS:
                n -= 1

        return ' ' * (n * self.__INDENT_SIZE)

    def _process_data(self) -> None:
        # Compressing json
        reg_exp = re.compile(r'(".*?")|[\n\t\s]')
        result: str = reg_exp.sub(lambda m: m.group(1) or "", self._file_data)

        # Adding indents to "key-value" objects
        reg_exp = re.compile(r'(".*?")|,')
        result = reg_exp.sub(lambda m: m.group(1) or "\n" + self.get_indent(m, result), result)

        # Adding indents to complex objects
        reg_exp = re.compile(r'(".*?")|:{')
        result = reg_exp.sub(lambda m: m.group(1) or ":\n" + self.get_indent(m, result), result)

        # Adding spaces after ":"
        reg_exp = re.compile(r'(".*?")|:(?!\n)')
        result = reg_exp.sub(lambda m: m.group(1) or ": ", result)

        # Deleting quotes
        reg_exp = re.compile(r'"(\S+)"')
        result = reg_exp.sub(lambda m: m.group(1), result, 0)

        # Deleting brackets
        reg_exp = re.compile("[{}]")
        result = reg_exp.sub("", result)

        self._converted_data = result

if __name__ == '__main__':
    converter = RegExpConverter('./resources/input_a2.json')
    converter.convert('./results/RegExpConverter.yaml')
