# A dictionary that shows how program metadata is organized,
#   Typically accessed through the detail_manager's attribute
#   detail_manager.collection_metadata

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

path_to_fila_b = '/path/to/file/b'
file_b_size = 20
file_b_hash = 'wxyz'

path_to_fila_c = '/path/to/file/c'
file_c_size = 10
file_c_hash = 'abcd'

path_to_fila_d = '/path/to/file/d'
file_d_size = 20
file_d_hash = 'wxyz'

example_collection_metadata = {
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
                    'DUPLICATES': {}
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
