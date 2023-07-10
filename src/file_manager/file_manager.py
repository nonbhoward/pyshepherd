# imports, python
from json import dumps
from os import environ
from pathlib import Path


class FileManager:
    def __init__(
            self,
            debug=False
    ):
        home = environ.get("HOME")
        self._debug = debug
        self._file_to_write = Path(home, 'pyshepherd', 'all_file_metadata.txt')

    def write(self, data_to_write):
        with open(self._file_to_write, 'w') as ftw:
            ftw.write(dumps(data_to_write))
