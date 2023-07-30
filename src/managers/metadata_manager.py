# Manage the file metadata

from src.enumerations import FileAttribute
from src.enumerations import MetadataKey


class MetadataManager:
    def __init__(self):
        print(f'Init {self.__class__.__name__}')
        self._collection_metadata = {}

    # Parent Properties

    @property
    def collection_metadata(self):
        return self._collection_metadata

    @collection_metadata.setter
    def collection_metadata(self, value):
        self._collection_metadata = value

    # Children Properties

    @staticmethod
    def delete_entry(collection_metadata: dict, file: str):
        del collection_metadata[file]

    def get_collection_file_metadata(self, collection_name, file_type):
        return self.collection_metadata[collection_name]['FILES'][file_type]

    def get_collection_metadata(self, collection_name: str, file_type: str) -> dict:
        if file_type == 'ARCHIVE':
            return self.collection_metadata[collection_name]['FILES']['ARCHIVE']

    @staticmethod
    def get_file_size_from(collection_metadata, file):
        return collection_metadata[file][FileAttribute.ST_SIZE]

    def get_files(self, collection_name, file_type):
        return self.collection_metadata[collection_name]['FILES'][file_type]

    @staticmethod
    def get_hash(collection_metadata: dict, file: str) -> str:
        return collection_metadata[file][MetadataKey.HASH]

    @staticmethod
    def get_parent_count_from(duplicate_metadata):
        return len(duplicate_metadata)

    def init_collection_metadata(self, collection_name, collection_paths):
        self.collection_metadata = {
            collection_name: {
                MetadataKey.COLLECTION_PATHS: collection_paths
            }
        }

    def init_file_metadata(self, collection_name, files_at_path, path_type):
        if 'FILES' not in self.collection_metadata[collection_name]:
            self.collection_metadata[collection_name]['FILES'] = {}
        if path_type == 'ARCHIVE':
            self.collection_metadata[collection_name]['FILES'].update({
                path_type: files_at_path
            })
        elif path_type == 'SOURCE':
            self.collection_metadata[collection_name]['FILES'].update({
                path_type: files_at_path
            })
        else:
            raise RuntimeError(f'Unknown path_type : {path_type}')

    def set_duplicate_metadata(self, collection_name, duplicate_metadata):
        collection_file_metadata = \
            self.collection_metadata[collection_name]['FILES']['ARCHIVE']
        if duplicate_metadata is None:
            return
        for parent_file, children_files in duplicate_metadata.items():
            collection_file_metadata[parent_file].update({
                'duplicates': children_files
            })

    @staticmethod
    def set_soft_link_command(collection_metadata,
                              duplicate_metadata,
                              command):
        original = duplicate_metadata['original']
        duplicate = duplicate_metadata['name']
        collection_metadata[original]['duplicates'][duplicate]['soft_link_command'] = command

    @staticmethod
    def set_unstage_storage_details(
            collection_metadata,
            duplicate_file_metadata,
            unstage_storage_details):
        unstage_file_dc = duplicate_file_metadata['name']
        original_file_dc = duplicate_file_metadata['original']
        collection_metadata[original_file_dc]['duplicates'][unstage_file_dc].update(
            unstage_storage_details)

    @staticmethod
    def update_metadata_for_child(
            collection_name: str,
            collection_metadata: dict,
            duplicate_metadata_for_file: dict,
            parent_name: str,
            parent_hash: str,
            child_name: str,
            child_hash: str):
        duplicate_metadata_for_file.update({child_name: {
            'collection': collection_name,
            'hash': child_hash,
            'name': child_name,
            'parent': {
                'hash': parent_hash,
                'name': parent_name,
                'size': collection_metadata[parent_name]['ST_SIZE']
            },
            'size': collection_metadata[child_name]['ST_SIZE']
        }})

    @staticmethod
    def update_metadata_for_parent(
            parent_file: str,
            parent_metadata: dict,
            child_metadata: dict):
        child_metadata.update({parent_file: parent_metadata })

    def update_file_hashes(self, collection_name, file_type: str, file_hashes: dict) -> None:
        files = self.collection_metadata[collection_name]['FILES'][file_type]
        for file, file_details in files.items():
            file_details.update({
                'HASH': file_hashes[file]['HASH']
            })
