from enum import Enum
import typing as t

from lab4._base_converter import BaseConverter
from lab4._utils import is_digit_1_to_9


class JSONTokens:
    WHITESPACE = [' ', '\n', '\t']
    QUOTE = '"'
    MINUS = '-'
    LEFT_BRACKET = '['
    RIGHT_BRACKET = ']'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    COLON = ':'
    COMMA = ','
    TRUE = 'true'
    FALSE = 'false'
    NULL = 'null'


class JSONParser:
    def __init__(self, raw_json: str) -> None:
        self.raw_json = raw_json
        self.i = 0
        self.parsed_data = None

    def cur(self) -> str:
        """Returns current symbol"""
        return self.raw_json[self.i]

    def next_(self) -> str:
        """Returns next symbol"""
        return self.raw_json[self.i + 1]

    def advance(self, steps: int = 1) -> None:
        """Advance to next symbol"""
        self.i += steps

    def eat_whitespace(self) -> None:
        """Skips space characters"""
        while self.cur() in JSONTokens.WHITESPACE:
            self.advance()

    def lookup(self, value: str) -> bool:
        """Checks if given value in located after current symbol"""
        file_size_exceeded = self.i + len(value) > len(self.raw_json)
        value_matched = self.raw_json[self.i: self.i + len(value)] == value
        return value_matched and not file_size_exceeded

    def eat(self, char: str) -> None:
        if self.cur() == char:
            self.advance()
            return
        raise Exception(f'Parsing error at position {self.i}, "{char}" is expected')

    def eat_number(self) -> t.Union[int, float]:
        """Reads number"""
        is_fractional = False
        numeric_value_start = self.i

        if self.cur() == JSONTokens.MINUS:
            self.advance()
        if (self.cur() == '0' and is_digit_1_to_9(self.next_())) or is_digit_1_to_9(self.cur()):
            self.advance()
        else:
            raise Exception(f'Parsing error in number at position {self.i}')

        while self.cur().isdecimal():
            self.advance()

        if self.cur() == '.':
            is_fractional = True
            self.advance()
            if not self.cur().isdecimal():
                raise Exception(f'Parsing error in number at position {self.i}')
            while self.cur().isdecimal():
                self.advance()

        if self.cur() == 'e' or self.cur() == 'E':
            is_fractional = True
            self.advance()
            if self.cur() == '+' or self.cur() == '-':
                self.advance()
            if not self.cur().isdecimal():
                raise Exception(f'Parsing error in number at position {self.i}')
            while self.cur().isdecimal():
                self.advance()

        value = self.raw_json[numeric_value_start: self.i]
        return float(value) if is_fractional else int(value)

    def eat_boolean(self) -> bool:
        """Read boolean value."""
        if self.lookup("true"):
            self.advance(4)
            return True
        elif self.lookup("false"):
            self.advance(5)
            return False
        raise Exception(f"Parsing error in boolean at position: {self.i}")

    def eat_string(self) -> str:
        """Read string symbols and return the whole string read."""
        string_value_start = self.i
        self.advance()
        while self.cur() != JSONTokens.QUOTE:
            self.advance()
        self.advance()
        return self.raw_json[string_value_start: self.i][1: -1]

    def eat_property_name(self) -> str:
        """Read property name."""
        property_name_start = self.i
        while self.cur() != JSONTokens.COLON:
            self.advance()
        return self.raw_json[property_name_start:self.i][1:-1]

    def eat_array(self) -> list:
        """Read array value recursively."""
        result = []
        self.eat_whitespace()
        while self.cur() != JSONTokens.RIGHT_BRACKET:
            result.append(self.eat_value())
            if self.cur() != JSONTokens.RIGHT_BRACKET:
                self.eat(JSONTokens.COMMA)
        return result

    def eat_null(self) -> None:
        """Read null value."""
        if self.lookup(JSONTokens.NULL):
            self.advance(4)
            return None

    def eat_value(self) -> t.Union[list, dict, int, str, None, bool]:
        """Read value of an array or object."""
        self.eat_whitespace()
        value = None

        if self.cur().isdigit() or self.cur() == JSONTokens.MINUS:
            value = self.eat_number()
        elif self.cur() == JSONTokens.QUOTE:
            value = self.eat_string()
        elif self.lookup(JSONTokens.TRUE) or self.lookup(JSONTokens.FALSE):
            value = self.eat_boolean()
        elif self.lookup(JSONTokens.NULL):
            value = self.eat_null()
        elif self.cur() == JSONTokens.LEFT_BRACKET:
            self.eat(JSONTokens.LEFT_BRACKET)
            value = self.eat_array()
            self.eat(JSONTokens.RIGHT_BRACKET)
        elif self.cur() == JSONTokens.LEFT_BRACE:
            self.eat(JSONTokens.LEFT_BRACE)
            value = self.eat_object()
            self.eat(JSONTokens.RIGHT_BRACE)
        else:
            raise Exception(f'Parsing error at position: {self.i}')

        self.eat_whitespace()
        return value

    def eat_object(self) -> dict:
        """Read objects value recursively."""
        result = {}
        self.eat_whitespace()
        while self.cur() != JSONTokens.RIGHT_BRACE:
            self.eat_whitespace()
            property_name = self.eat_property_name()
            self.eat_whitespace()

            self.eat(JSONTokens.COLON)
            property_value = self.eat_value()

            if self.cur() != JSONTokens.RIGHT_BRACE:
                self.eat(JSONTokens.COMMA)
            result[property_name] = property_value
        return result

    def parse(self) -> t.Union[dict, list]:
        if self.cur() == JSONTokens.LEFT_BRACKET:
            self.advance()
            self.parsed_data = self.eat_array()
            self.eat(JSONTokens.RIGHT_BRACKET)
        elif self.cur() == JSONTokens.LEFT_BRACE:
            self.advance()
            self.parsed_data = self.eat_object()
            self.eat(JSONTokens.RIGHT_BRACE)

        self.i = 0
        return self.parsed_data


class Obj2YAML:
    def __init__(self, obj: t.Union[dict, list]):
        self.__obj = obj
        self.__result = ''
        self.__ignore_indent_flag = False

    def __convert_dict(self, obj: dict, indent: int = 0) -> None:
        for key, value in obj.items():
            if isinstance(value, dict):
                self.__add_line(f'{key}:', indent)
                self.__convert_dict(value, indent + 1)
            elif isinstance(value, list):
                self.__add_line(f'{key}:', indent)
                self.__convert_list(value, indent + 1)
            else:
                self.__add_line(f'{key}: {value}', indent)

    def __convert_list(self, obj: list, indent: int = 0) -> None:
        for index, value in enumerate(obj):
            self.__add_line('- ', indent, line_break=False)
            self.__ignore_indent_flag = True

            if isinstance(value, dict):
                self.__convert_dict(value, indent + 1)
            elif isinstance(value, list):
                self.__convert_list(value, indent + 1)
            else:
                self.__add_line(f'{value}', indent + 1)

    def __add_line(self, line: str, indent: int, line_break: bool = True) -> None:
        current_line = line
        if not self.__ignore_indent_flag:
            current_line = ('  ' * indent) + current_line
        else:
            self.__ignore_indent_flag = False
        if line_break:
            current_line += '\n'

        self.__result += current_line

    def convert(self):
        if isinstance(self.__obj, dict):
            self.__convert_dict(self.__obj)
        elif isinstance(self.__obj, list):
            self.__convert_list(self.__obj)

        return self.__result


class FormalGrammarsConverter(BaseConverter):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.__parser = JSONParser(self._file_data)

    def _process_data(self) -> None:
        python_obj = self.__parser.parse()
        obj2yaml = Obj2YAML(python_obj)
        self._converted_data = obj2yaml.convert()


if __name__ == '__main__':
    converter = FormalGrammarsConverter('resources/input_a3.json')
    converter.convert('./results/FormalGrammarsConverter.yaml')
