# Copy and move files

# imports python
from os import mkdir
from os.path import exists
from shutil import copy
from shutil import move
from subprocess import run


class FileManager:

    def __init__(self, detail_manager):
        print(f'Init {self.__class__.__name__}')
        self.detail_manager = detail_manager

    @staticmethod
    def create_required_folders(unstage_file_details):
        print(f'create_required_folders')
        unstage_parent_folder = \
            str(unstage_file_details[
                    'unstage_storage_details'][
                    'unstage_parent_folder'])
        udes = unstage_destination_elements = unstage_parent_folder.split('/')
        progressive_path = ''
        for ude in udes:
            progressive_path += ude + '/' if ude else '/'
            if not exists(progressive_path):
                try:
                    mkdir(progressive_path)
                except OSError as exc:
                    print(f'Failed to make path : {progressive_path}, {exc}')
                    raise exc

    @staticmethod
    def create_soft_link(soft_link_command):
        try:
            run(soft_link_command)
        except OSError as exc:
            print(f'Failed to create soft link : {soft_link_command}, {exc}')
            raise exc

    def move_duplicate_file(self, unstage_file, unstage_file_details):
        unstage_file_dst = unstage_file_details['unstage_storage_details']['unstage_file_destination']
        self.move_file(
            src=unstage_file,
            dst=unstage_file_dst
        )

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
        dst = '/'.join(dst.split('/')[:-1])
        if not exists(dst):
            raise OSError(f'Dst not exist : {dst}')
