# General purpose functions

# imports, python
from os import walk
from os.path import exists


def build_soft_link_command(path_to_target, soft_link_name):
    path_to_soft_link = soft_link_name
    return ['ln', '-s', path_to_target, path_to_soft_link]


def convert_filepath_to_filename(file_path):
    file_name = file_path.replace('/', '_')[1:]
    return file_name


def convert_filepath_to_soft_link_name(file_path):
    soft_link_name = file_path.replace('/', '_')[1:]
    return soft_link_name


def read_all_files(path):
    all_files = []
    for root, _, files in walk(path):
        print(f'Reading files in {root}')
        for file in files:
            file_path = root + '/' + file
            if exists(file_path):
                all_files.append(file_path)
            else:
                print(f'Error, file does not exist : {file_path}')
    return all_files
