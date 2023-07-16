# Copy and move files

# imports python
from os import mkdir
from os.path import exists
from pathlib import Path
from shutil import copy
from shutil import move
from subprocess import run


class FileManager:

    def unstage(self, unstaging_metadata):
        # Read metadata
        path_to_duplicate = unstaging_metadata['path_to_duplicate']
        path_to_original = unstaging_metadata['path_to_original']
        soft_link = unstaging_metadata['soft_link_name']
        unstage_path = unstaging_metadata['unstage_path']

        # Create file structure
        self.make_dir(unstage_path)
        if not exists(unstage_path):
            raise OSError(f'Failed to mkdir : {unstage_path}')

        # Create soft-link to original and relocate duplicate
        self.create_soft_link(unstage_path, path_to_original, soft_link)
        self.move_file(path_to_duplicate, unstage_path)

    @staticmethod
    def make_dir(dir_to_make):
        if exists(dir_to_make):
            return
        try:
            mkdir(dir_to_make)
        except OSError as exc:
            print(f'Failed to mkdir : {dir_to_make}')
            raise exc

    def create_soft_link(self, path, path_to_original, link_name):
        path_to_soft_link = str(Path(path, link_name))
        ln_output = run(['ln', '-s', path_to_original, path_to_soft_link], capture_output=True)
        if hasattr(ln_output, 'stderr'):
            print(f'{ln_output.stderr}')

    def copy_file(self, src, dst):
        self.validate_paths(src, dst)
        try:
            copy(src=src, dst=dst)
        except OSError as exc:
            print(f'Failed to move file : {src} > {dst}')
            raise exc

    def move_file(self, src, dst):
        self.validate_paths(src, dst)
        try:
            move(src=src, dst=dst)
        except OSError as exc:
            print(f'Failed to move file : {src} > {dst}')
            raise exc

    @staticmethod
    def validate_paths(src, dst):
        if not exists(src):
            raise OSError(f'Src not exist : {src}')
        if not exists(dst):
            raise OSError(f'Dst not exist : {dst}')
