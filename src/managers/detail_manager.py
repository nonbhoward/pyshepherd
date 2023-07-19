# Manage details with attributes instead of manually manipulating collections

# imports, python
from types import MappingProxyType

# imports, project
from src.enumerations import ArchiveType
from src.enumerations import ConfigKey
from src.enumerations import MetadataKey


class DetailManager:

    def __init__(self, config):
        print(f'Init {self.__class__.__name__}')
        self._config = config
        self._hasher_algo = None
        self._mpt_archives = MappingProxyType(self.archives)
        self.metadata = {}

    # Archive
    def archive_paths(self, archive_name):
        return self._config[ConfigKey.ARCHIVES][archive_name]

    @property
    def create_default_archive_paths(self):
        return self._config[ConfigKey.CREATE_DEFAULT_ARCHIVE_PATHS]

    @property
    def create_default_source_paths(self):
        return self._config[ConfigKey.CREATE_DEFAULT_SOURCE_PATHS]

    def path_archive(self, archive_name):
        return self.archives[archive_name][ConfigKey.ARCHIVE_PATH]

    def path_graveyard(self, archive_name):
        return self.archives[archive_name][ConfigKey.GRAVEYARD_PATH]

    def path_source(self, archive_name):
        return self.archives[archive_name][ConfigKey.SOURCE_PATH]

    def path_stage(self, archive_name):
        return self.archives[archive_name][ConfigKey.STAGE_PATH]

    def path_unstage(self, archive_name):
        return self.archives[archive_name][ConfigKey.UNSTAGE_PATH]

    # Config
    @property
    def archives(self):
        return dict(self.config[ConfigKey.ARCHIVES])

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
        return self._config[ConfigKey.FILE_NAME_LEN_MAX_VALUE]

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
        return self._config[ConfigKey.LARGE_FILE_THRESHOLD]

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
        return self._config[ConfigKey.SKIP_SOFT_LINKS]

    @property
    def sort_duplicate_hierarchy(self):
        return self._config[ConfigKey.SORT_DUPLICATE_HIERARCHY]

    def update_archive_paths(self, archive_paths):
        try:
            self._config[ConfigKey.ARCHIVES][ConfigKey.DEFAULT_ARCHIVE].update({
                ConfigKey.ARCHIVE_PATH: archive_paths[ConfigKey.ARCHIVE_PATH],
                ConfigKey.UNSTAGE_PATH: archive_paths[ConfigKey.UNSTAGE_PATH]
            })
        except Exception as exc:
            print(exc)
            raise exc

    def update_source_paths(self, archive_paths):
        try:
            self._config[ConfigKey.ARCHIVES][ConfigKey.DEFAULT_ARCHIVE].update({
                ConfigKey.GRAVEYARD_PATH: archive_paths[ConfigKey.GRAVEYARD_PATH],
                ConfigKey.SOURCE_PATH: archive_paths[ConfigKey.SOURCE_PATH],
                ConfigKey.STAGE_PATH: archive_paths[ConfigKey.STAGE_PATH],
            })
        except Exception as exc:
            print(exc)
            raise exc

    # File Manager
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

    # Metadata
    @property
    def archive_metadata_empty(self):
        archive_metadata_empty = {
            MetadataKey.TYPE: ArchiveType.ARCHIVE,
            MetadataKey.UNSTAGE: {}
        }
        return archive_metadata_empty

    @staticmethod
    def archive_metadata_update(archive_metadata, file, metadata):
        archive_metadata[MetadataKey.UNSTAGE].update({
            file: metadata
        })

    @staticmethod
    def duplicate_metadata_init(file):
        duplicate_metadata_empty = {
            file: {}
        }
        return duplicate_metadata_empty

    @staticmethod
    def duplicate_metadata_add_new_entry(duplicate_metadata, file):
        duplicate_metadata.update({
            file: {}
        })

    def read_metadata(self, archive_name):
        return self.metadata[archive_name]

    @staticmethod
    def read_metadata_type(unstage_metadata):
        return unstage_metadata[MetadataKey.TYPE]

    @staticmethod
    def read_unstage(archive_metadata):
        return archive_metadata[MetadataKey.UNSTAGE]

    def write_metadata(self, archive_name, file_metadata):
        self.metadata[archive_name] = file_metadata

    def update_metadata(self, archive_name, file_metadata):
        self.metadata[archive_name].update({file_metadata})

    # Progress
    @property
    def progress_bar_increment(self):
        return self._config[ConfigKey.PROGRESS_BAR_INCREMENT]

    def terminal_dialog_padding(self):
        return self._config[ConfigKey.TERMINAL_DIALOG_PADDING]
