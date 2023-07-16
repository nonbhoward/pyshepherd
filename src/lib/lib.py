# General purpose functions

def get_filename_from(file):
    return file.split('/')[-1]


def transform_file_path_to_soft_link(file):
    return '_'.join(file.split('/'))


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
