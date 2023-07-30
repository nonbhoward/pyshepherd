# General purpose functions

# imports, python
from os import stat
from os import walk
from os.path import exists
from os.path import islink
from src.enumerations import Command
from src.enumerations import FileAttribute
import shutil
import sys


def build_soft_link_command(path_to_target: str, soft_link_name: str) -> list:
    """Build a soft link command using the provided target and name

    :param path_to_target: the target of the soft link
    :param soft_link_name: the soft link label
    :return: the soft link command
    """
    path_to_soft_link = soft_link_name
    return [* Command.SoftLink.root, path_to_target, path_to_soft_link]


def convert_filepath_to_filename(file_path: str) -> str:
    """Replaces /'s with _'s to convert a filepath into a filename

    :param file_path: the path to a file
    :return: the new file name
    """
    file_name = file_path.replace('/', '_')[1:]
    # TODO, bug, detect and strip file names with repeating patterns
    return file_name


def convert_filepath_to_soft_link_name(file_path: str) -> str:
    """Replaces /'s with _'s to convert a filepath into a link name

    :param file_path: the path to a file
    :return: the new link name
    """
    soft_link_name = file_path.replace('/', '_')[1:]
    return soft_link_name


def read_all_files(path: str, skip_soft_links: bool) -> dict:
    """Recursively fetch all files in a path

    :param path: the path to recursively crawl
    :param skip_soft_links: a toggle to ignore soft links
    :return: a dictionary of all files, with their file size
    """
    all_files = {}
    for root, _, files in walk(path):
        sys.stdout.write(f'\rReading files in {root}')
        for file in files:
            file_path = root + '/' + file
            if exists(file_path):
                if skip_soft_links and islink(file_path):
                    # print(f'Skipping soft-link {file_path} ')
                    continue
                file_stat = stat(file_path)
                # TODO compare sizes against size limits
                all_files[file_path] = {
                    FileAttribute.ST_SIZE: file_stat.st_size
                }
            else:
                print(f'Error, file does not exist : {file_path}')
    return all_files


def loading_dialog(percentage: float) -> str:
    """Construct the loading dialog from a percentage, taking into account
        the width of the parent terminal

    :param percentage: a float value representing a percentage
    :return: a string that visually represents the percentage
    """
    if percentage < 0:
        return  # Disregard negative values

    # Get loading bar environment
    # TODO replace int with padding value
    loading_bar_length = shutil.get_terminal_size().columns - 7

    # Scale loading bar percent to total width available
    percentage *= 0.01
    loaded = int(loading_bar_length * percentage)
    unloaded = int(loading_bar_length - loaded)

    # Build and return the loading string
    loading_string = loaded * '*' + unloaded * '-'
    loading_bar = '[' + loading_string + ']'
    return loading_bar
