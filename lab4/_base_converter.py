from abc import ABC, abstractmethod

from lab4._utils import read_file


class BaseConverter(ABC):
    def __init__(self, filename) -> None:
        self.__input_filename = filename
        self._file_data = read_file(self.__input_filename)
        self._converted_data = ''

    @abstractmethod
    def _process_data(self) -> None:
        """Processes data from given file"""

    def convert(self, output_filename: str, save_to_file: bool = True) -> None:
        self._process_data()

        if save_to_file:
            with open(output_filename, 'w') as output_file:
                output_file.write(self._converted_data)
