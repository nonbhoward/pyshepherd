# Example dictionary showing how program metadata is organized.
# Accessed through the file_metadata_manager's attributes.

# Example values

a_collection_name = 'an archive name'

path_to_archive = '/path/to/archive/'
path_to_graveyard = '/path/to/graveyard/'
path_to_stage = '/path/to/stage/'
path_to_source = '/path/to/source/'
path_to_unstage = '/path/to/unstage/'

path_to_fila_a = '/path/to/file/a'
file_a_size = 10
file_a_hash = 'abcd'

duplicate_file_a = '/path/to/duplicate/file/a'
path_to_file_a = '/path/to/file/a'
size_file_a = 10
path_to_unstage_file_a_root = '/path/to/unstage/file/a/root'
path_to_unstage_duplicate_file_a = '/path/to/unstage/duplicate/file/a'
soft_link_target = '/path/to/soft/link/target'
soft_link_label = '/path/to/soft/link/label'

path_to_fila_b = '/path/to/file/b'
file_b_size = 20
file_b_hash = 'wxyz'

path_to_fila_c = '/path/to/file/c'
file_c_size = 10
file_c_hash = 'abcd'

path_to_fila_d = '/path/to/file/d'
file_d_size = 20
file_d_hash = 'wxyz'

example_collections_metadata = {
    a_collection_name: {
        'COLLECTION_PATHS': {
            'ARCHIVE_PATH': path_to_archive,
            'GRAVEYARD_PATH': path_to_graveyard,
            'SOURCE_PATH': path_to_source,
            'STAGE_PATH': path_to_stage,
            'UNSTAGE_PATH': path_to_stage
        },
        'FILES': {
            'ARCHIVE': {
                path_to_fila_a: {
                    'ST_SIZE': file_a_size,
                    'HASH': file_a_hash,
                    'DUPLICATES': {
                        duplicate_file_a : {
                            'collection': a_collection_name,
                            'hash': file_a_hash,
                            'name': duplicate_file_a,
                            'original': path_to_file_a,
                            'parent': {
                                'hash': file_a_hash,
                                'name': path_to_file_a,
                                'size': size_file_a
                            },
                            'size': size_file_a,
                            'unstage_parent_folder': path_to_unstage_file_a_root,
                            'unstage_file_destination': path_to_unstage_duplicate_file_a,
                            'soft_link_command': [
                                'ln', '-s-', soft_link_target, soft_link_label
                            ]
                        }
                    }
                },
                path_to_fila_b: {
                    'ST_SIZE': file_b_size,
                    'HASH': file_b_hash,
                    'DUPLICATES': {}
                }
            },
            'SOURCE': {
                path_to_fila_c: {
                    'ST_SIZE': file_c_size,
                    'HASH': file_c_hash,
                    'DUPLICATES': {}
                },
                path_to_fila_d: {
                    'ST_SIZE': file_d_size,
                    'HASH': file_d_hash,
                    'DUPLICATES': {}
                }
            }
        }
    }
}
