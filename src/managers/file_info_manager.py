# imports, python
import os.path
from os import stat
from os.path import exists
from pathlib import Path


class FileInfoManager:
    def __init__(
            self,
            debug=False
    ):
        self._debug = debug

    def read_file_info(self, path_to_file: Path):
        file_info = {}
        if not exists(path_to_file):
            return
        file_stat = stat(path=path_to_file)
        return file_info
