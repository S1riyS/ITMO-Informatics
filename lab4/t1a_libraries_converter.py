import json
import yaml
import typing as t

from lab4._base_converter import BaseConverter


class LibrariesConverter(BaseConverter):
    def _process_data(self) -> None:
        # Converting raw str with json data to Python object
        json_obj = json.loads(self._file_data)
        # Converting Python object to yaml file
        self._converted_data = yaml.dump(json_obj, default_flow_style=False, allow_unicode=True)

if __name__ == '__main__':
    converter = LibrariesConverter('./resources/input.json')
    converter.convert(f'./results/LibrariesConverter.yaml')