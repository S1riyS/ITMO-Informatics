from time import time

from lab4.t1_metasymbols_replacement import MetasymbolsReplacementConverter
from lab4.t1a_libraries_converter import LibrariesConverter
from lab4.t2a_regexp_converter import RegExpConverter
from lab4.t3a_formal_grammars_converter import FormalGrammarsConverter

t1_converter = MetasymbolsReplacementConverter('./resources/input_a4.json')
t1a_converter = LibrariesConverter('./resources/input_a4.json')
t2a_converter = RegExpConverter('./resources/input_a4.json')
t3a_converter = FormalGrammarsConverter('./resources/input_a4.json')

converters = [
    {'name': 'MetasymbolsReplacementConverter', 'class_': t1_converter},
    {'name': 'LibrariesConverter', 'class_': t1a_converter},
    {'name': 'RegExpConverter', 'class_': t2a_converter},
    {'name': 'FormalGrammarsConverter', 'class_': t3a_converter}
]

for converter in converters:
    class_obj = converter['class_']
    name = converter['name']

    start_time = time()
    for _ in range(100):
        class_obj.convert('', save_to_file=False)
    end_time = time()

    print(f'{name} finished working in {end_time - start_time} seconds')
