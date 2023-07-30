# Manage details with attributes instead of manually manipulating collections

# imports, python
from types import MappingProxyType

# imports, project
from src.enumerations import ArchiveType
from src.enumerations import ConfigKey
from src.enumerations import FileAttribute
from src.enumerations import MetadataKey


class DetailManager:

    def __init__(self, config):
        print(f'Init {self.__class__.__name__}')
        self._config = config
        self._hasher_algo = None
        self._collection_metadata = None
        self.metadata = {}

    # Collection
    @property
    def collection_metadata(self):
        return self._collection_metadata

    @collection_metadata.setter
    def collection_metadata(self, value):
        self._collection_metadata = value

    @property
    def create_default_archive_paths(self):
        return self.config[ConfigKey.CREATE_DEFAULT_ARCHIVE_PATHS]

    @property
    def create_default_source_paths(self):
        return self.config[ConfigKey.CREATE_DEFAULT_SOURCE_PATHS]

    # Config
    @property
    def collection_config(self):
        return self.config[ConfigKey.COLLECTION]

    @property
    def buf_size(self):
        return self.config[ConfigKey.BUF_SIZE]

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def debug(self):
        return self.config[ConfigKey.DEBUG]

    @property
    def file_name_len_max_value(self):
        return self.config[ConfigKey.FILE_NAME_LEN_MAX_VALUE]

    @property
    def file_size_limit_max(self):
        return self.config[ConfigKey.FILE_SIZE_TO_HASH_MAX]

    @property
    def file_size_limit_min(self):
        return self.config[ConfigKey.FILE_SIZE_TO_HASH_MIN]

    @property
    def hash_algo(self):
        return self.config[ConfigKey.HASH_ALGO]

    @property
    def hasher_algo(self):
        return self._hasher_algo

    @hasher_algo.setter
    def hasher_algo(self, value):
        self._hasher_algo = value

    @property
    def large_file_threshold(self):
        return self.config[ConfigKey.LARGE_FILE_THRESHOLD]

    @property
    def network_check_count(self):
        return self.config[ConfigKey.NETWORK_CHECK_COUNT]

    @property
    def network_check_delay(self):
        return self.config[ConfigKey.NETWORK_CHECK_DELAY]

    @property
    def require_network(self):
        return self.config[ConfigKey.REQUIRE_NETWORK]

    @property
    def skip_soft_links(self):
        return self.config[ConfigKey.SKIP_SOFT_LINKS]

    # FILES
    @property
    def default_parent_folder(self):
        return self.config[ConfigKey.DEFAULT_PARENT_FOLDER]

    @property
    def default_archive_folder(self):
        return self.config[ConfigKey.DEFAULT_ARCHIVE_FOLDER]

    @property
    def default_graveyard_folder(self):
        return self.config[ConfigKey.DEFAULT_GRAVEYARD_FOLDER]

    @property
    def default_source_folder(self):
        return self.config[ConfigKey.DEFAULT_SOURCE_FOLDER]

    @property
    def default_stage_folder(self):
        return self.config[ConfigKey.DEFAULT_STAGE_FOLDER]

    @property
    def default_unstage_folder(self):
        return self.config[ConfigKey.DEFAULT_UNSTAGE_FOLDER]

    # METADATA
    # All objects in this section should always include collection dict as an
    #   argument or return the collection_metadata, plus any additional keys
    #   required to reach the data

    def get_archive_file_metadata(self, collection_name, file_type):
        return self.collection_metadata[collection_name]['FILES'][file_type]

    def get_collection_metadata(self, collection_name: str, file_type: str) -> dict:
        if file_type == 'ARCHIVE':
            return self.collection_metadata[collection_name]['FILES']['ARCHIVE']

    def get_files(self, collection_name, file_type):
        return self.collection_metadata[collection_name]['FILES'][file_type]

    @staticmethod
    def get_file_size_from(collection_metadata, file):
        return collection_metadata[file][FileAttribute.ST_SIZE]

    @staticmethod
    def get_parent_count_from(duplicate_metadata):
        return len(duplicate_metadata)

    @staticmethod
    def get_unstage_file_dst_from(unstage_file_details):
        return unstage_file_details['unstage_file_destination']

    def get_unstage_metadata(self, collection_metadata: dict) -> dict:
        pass

    def init_collection_metadata(self, collection_name, collection_paths):
        self.collection_metadata = {
            collection_name: {
                MetadataKey.COLLECTION_PATHS: collection_paths
            }
        }

    @staticmethod
    def read_metadata_type(unstage_metadata):
        return unstage_metadata[MetadataKey.TYPE]

    @staticmethod
    def read_unstage(duplicate_metadata):
        # TODO delete me
        return duplicate_metadata

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

    def update_archive_paths(self, archive_paths):
        try:
            self.config[ConfigKey.COLLECTION][ConfigKey.DEFAULT_COLLECTION].update({
                ConfigKey.ARCHIVE_PATH_LABEL: archive_paths[ConfigKey.ARCHIVE_PATH_LABEL],
                ConfigKey.UNSTAGE_PATH: archive_paths[ConfigKey.UNSTAGE_PATH]
            })
        except Exception as exc:
            print(exc)
            raise exc

    def update_file_hashes(self, collection_name, file_type: str, file_hashes: dict) -> None:
        files = self.collection_metadata[collection_name]['FILES'][file_type]
        for file, file_details in files.items():
            file_details.update({
                'HASH': file_hashes[file]['HASH']
            })

    def update_metadata(self, archive_name, file_metadata):
        self.metadata[archive_name].update({file_metadata})

    def update_source_paths(self, archive_paths):
        try:
            self.config[ConfigKey.COLLECTION][ConfigKey.DEFAULT_COLLECTION].update({
                ConfigKey.GRAVEYARD_PATH: archive_paths[ConfigKey.GRAVEYARD_PATH],
                ConfigKey.SOURCE_PATH: archive_paths[ConfigKey.SOURCE_PATH],
                ConfigKey.STAGE_PATH: archive_paths[ConfigKey.STAGE_PATH],
            })
        except Exception as exc:
            print(exc)
            raise exc

    # Metadata, Duplicates
    @staticmethod
    def duplicate_metadata_for_file_init(file):
        duplicate_metadata_empty = {
            file: {
                'name': file
            }
        }
        return duplicate_metadata_empty

    @staticmethod
    def duplicate_metadata_add_new_entry(duplicate_metadata, file):
        # TODO delete
        duplicate_metadata.update({
            file: {}
        })

    # Paths
    def get_collection(self, collection_name: str) -> dict:
        return self.collection_config[collection_name]

    def get_path_archive(self, collection_name) -> dict:
        path = self.config[
            ConfigKey.COLLECTION][
            collection_name][
            ConfigKey.ARCHIVE_PATH
        ]
        return path

    def get_path_graveyard(self, collection_name) -> dict:
        path = self.config[
            ConfigKey.COLLECTION][
            collection_name][
            ConfigKey.GRAVEYARD_PATH
        ]
        return path

    def get_path_source(self, collection_name) -> dict:
        path = self.config[
            ConfigKey.COLLECTION][
            collection_name][
            ConfigKey.SOURCE_PATH
        ]
        return path

    def get_path_stage(self, collection_name) -> dict:
        path = self.config[
            ConfigKey.COLLECTION][
            collection_name][
            ConfigKey.STAGE_PATH
        ]
        return path

    def get_path_unstage(self, collection_name) -> dict:
        path = self.config[
            ConfigKey.COLLECTION][
            collection_name][
            ConfigKey.UNSTAGE_PATH
        ]
        return path

    # Progress
    @property
    def progress_bar_increment(self):
        return self.config[ConfigKey.PROGRESS_BAR_INCREMENT]

    def terminal_dialog_padding(self):
        return self.config[ConfigKey.TERMINAL_DIALOG_PADDING]
