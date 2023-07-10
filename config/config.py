from os import environ

# GLOBAL VALUES BELOW
DEBUG = True
# GLOBAL VALUES ABOVE

# DUPLICATE MANAGER VALUES BELOW

# Dict : duplicate_search_targets : The locations
#   that will be searched in an attempt to identify
#   duplicated files.
# Key : 'enabled'. Allows discrete toggling of
#   disable/enable per path.
# Key : 'path_to_check'. The path from which to
#   read all files.
# Key : 'path_to_result'. The location to record
#   the result.
username = environ.get("USERNAME")
duplicate_search_targets = {
    'blk_green': {
        'enabled': True,
        'path_to_check':
            f'/media/{username}/hdd_8TB_blk/green/',
        'path_to_result':
            f'/media/{username}/hdd_8TB_blk/green/'
            f'_duplicate_candidates_/'
    },
    'slv_green': {
        'enabled': False,
        'path_to_check':
            f'/media/{username}/hdd_8TB_slv/green/',
        'path_to_result':
            f'/media/{username}/hdd_8TB_slv/green/'
            f'_duplicate_candidates_/'
    }
}

# Float : duplicate_size_lookaround : When
#   searching for duplicates, it seems that the
#   most obvious place to start searching is
#   similarly sized files. This value sets a threshold
#   for how far the algorithm will "look around".
#   For example, a value of 0.05 indicates that the
#   algorithm will search files that are of size
#   larger than (file_size - file_size * 0.05) and
#   smaller than (file_size + file_size * 0.05).
duplicate_size_lookaround = 0.05

# DUPLICATE MANAGER VALUES ABOVE
