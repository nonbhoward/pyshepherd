# General purpose functions

# imports, python
from os import stat
from os import walk
from os.path import exists
from os.path import islink
from src.enumerations import Command
import shutil


def build_soft_link_command(path_to_target, soft_link_name):
    path_to_soft_link = soft_link_name
    return [* Command.SoftLink.root, path_to_target, path_to_soft_link]


def convert_filepath_to_filename(file_path):
    file_name = file_path.replace('/', '_')[1:]
    return file_name


def convert_filepath_to_soft_link_name(file_path):
    soft_link_name = file_path.replace('/', '_')[1:]
    return soft_link_name


def read_all_files(path, skip_soft_links):
    all_files = {}
    for root, _, files in walk(path):
        print(f'Reading files in {root}')
        for file in files:
            file_path = root + '/' + file
            if exists(file_path):
                if skip_soft_links and islink(file_path):
                    print(f'Skipping soft-link {file_path} ')
                    print('Optionally disable this behavior in the '
                          'configuration file')
                    continue
                file_stat = stat(file_path)
                all_files[file_path] = {
                    'st_size': file_stat.st_size
                }
            else:
                print(f'Error, file does not exist : {file_path}')
    return all_files


def loading_dialog(percentage):
    if percentage < 0:
        return  # Disregard negative values

    # Get loading bar environment
    loading_bar_length = shutil.get_terminal_size().columns - 7

    # Scale loading bar percent to total width available
    percentage *= 0.01
    loaded = int(loading_bar_length * percentage)
    unloaded = int(loading_bar_length - loaded)

    # Build and return the loading string
    loading_string = loaded * '*' + unloaded * '-'
    loading_bar = '[' + loading_string + ']'
    return loading_bar
