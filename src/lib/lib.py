# General purpose functions

# imports, python
from os import walk


def read_all_files(path):
    all_files = []
    for root, _, files in walk(path):
        for file in files:
            all_files.append(root + '/' + file)
    return all_files


def transform_filename_to_pathed_filename(file):
    file_elements = file.split('/')
    pathed_filename = '_'.join(file_elements)
    return pathed_filename


def transform_file_path_to_soft_link(file):
    file_elements = file.split('/')
    return '_'.join(file_elements)


def transform_file_path_to_folder(file_name):
    character_to_replace = ['/', '>', '<', '|', ':', '&', '(', ')']

    # Build raw name before replacements
    raw_folder_name = '_'.join(file_name.split('/'))

    # Build new name with replacements
    folder_name = ''
    for char in raw_folder_name:
        if char in character_to_replace:
            char = '_'
        folder_name += char
    folder_name = folder_name.replace(' ', '')
    return folder_name
