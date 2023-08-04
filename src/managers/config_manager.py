# Access to configuration

# imports, project
from src.enumerations import ConfigKey


class ConfigManager:

    def __init__(self, config):
        print(f'Init {self.__class__.__name__}')
        self._config = config
        self._hasher_algo = None

    @property
    def buf_size(self) -> int:
        return self.config[ConfigKey.BUF_SIZE]

    @property
    def collection_config(self) -> dict:
        return self.config[ConfigKey.COLLECTION]

    @property
    def config(self) -> dict:
        return self._config

    @property
    def create_default_archive_paths(self) -> bool:
        return self.config[ConfigKey.CREATE_DEFAULT_ARCHIVE_PATHS]

    @property
    def create_default_source_paths(self) -> bool:
        return self.config[ConfigKey.CREATE_DEFAULT_SOURCE_PATHS]

    @property
    def debug(self) -> bool:
        return self.config[ConfigKey.DEBUG]

    @property
    def file_name_len_max_value(self) -> int:
        return self.config[ConfigKey.FILE_NAME_LEN_MAX_VALUE]

    @property
    def file_size_limit_max(self) -> int:
        return self.config[ConfigKey.FILE_SIZE_TO_HASH_MAX]

    @property
    def file_size_limit_min(self) -> int:
        return self.config[ConfigKey.FILE_SIZE_TO_HASH_MIN]

    @property
    def hash_algo(self) -> str:
        return self.config[ConfigKey.HASH_ALGO]

    @property
    def hasher_algo(self):
        return self._hasher_algo

    @hasher_algo.setter
    def hasher_algo(self, value):
        self._hasher_algo = value

    @property
    def large_file_threshold(self) -> int:
        return self.config[ConfigKey.LARGE_FILE_THRESHOLD]

    @property
    def network_check_count(self) -> int:
        return self.config[ConfigKey.NETWORK_CHECK_COUNT]

    @property
    def network_check_delay(self) -> int:
        return self.config[ConfigKey.NETWORK_CHECK_DELAY]

    @property
    def require_network(self) -> bool:
        return self.config[ConfigKey.REQUIRE_NETWORK]

    @property
    def skip_soft_links(self) -> bool:
        return self.config[ConfigKey.SKIP_SOFT_LINKS]

    @property
    def stage_source(self) -> bool:
        return self.config[ConfigKey.STAGE_SOURCE]

    @property
    def unstage_archive(self) -> bool:
        return self.config[ConfigKey.UNSTAGE_ARCHIVE]

    # FILES
    @property
    def default_parent_folder(self) -> str:
        return self.config[ConfigKey.DEFAULT_PARENT_FOLDER]

    @property
    def default_archive_folder(self) -> str:
        return self.config[ConfigKey.DEFAULT_ARCHIVE_FOLDER]

    @property
    def default_graveyard_folder(self) -> str:
        return self.config[ConfigKey.DEFAULT_GRAVEYARD_FOLDER]

    @property
    def default_source_folder(self) -> str:
        return self.config[ConfigKey.DEFAULT_SOURCE_FOLDER]

    @property
    def default_stage_folder(self) -> str:
        return self.config[ConfigKey.DEFAULT_STAGE_FOLDER]

    @property
    def default_unstage_folder(self) -> str:
        return self.config[ConfigKey.DEFAULT_UNSTAGE_FOLDER]

    def update_archive_paths(self, archive_paths: dict):
        try:
            self.config[ConfigKey.COLLECTION][ConfigKey.DEFAULT_COLLECTION].update({
                ConfigKey.ARCHIVE_PATH_LABEL: archive_paths[ConfigKey.ARCHIVE_PATH_LABEL],
                ConfigKey.UNSTAGE_PATH: archive_paths[ConfigKey.UNSTAGE_PATH]
            })
        except Exception as exc:
            print(exc)
            raise exc

    def update_source_paths(self, archive_paths: dict):
        try:
            self.config[ConfigKey.COLLECTION][ConfigKey.DEFAULT_COLLECTION].update({
                ConfigKey.GRAVEYARD_PATH: archive_paths[ConfigKey.GRAVEYARD_PATH],
                ConfigKey.SOURCE_PATH: archive_paths[ConfigKey.SOURCE_PATH],
                ConfigKey.STAGE_PATH: archive_paths[ConfigKey.STAGE_PATH],
            })
        except Exception as exc:
            print(exc)
            raise exc

    def get_path_archive(self, collection_name: str) -> dict:
        path = self.config[
            ConfigKey.COLLECTION][
            collection_name][
            ConfigKey.ARCHIVE_PATH
        ]
        return path

    def get_path_graveyard(self, collection_name: str) -> dict:
        path = self.config[
            ConfigKey.COLLECTION][
            collection_name][
            ConfigKey.GRAVEYARD_PATH
        ]
        return path

    def get_path_source(self, collection_name: str) -> dict:
        path = self.config[
            ConfigKey.COLLECTION][
            collection_name][
            ConfigKey.SOURCE_PATH
        ]
        return path

    def get_path_stage(self, collection_name: str) -> dict:
        path = self.config[
            ConfigKey.COLLECTION][
            collection_name][
            ConfigKey.STAGE_PATH
        ]
        return path

    @property
    def get_path_to_write_report(self) -> str:
        return self.config[ConfigKey.PATH_TO_WRITE_REPORT]

    def get_path_unstage(self, collection_name: str) -> dict:
        path = self.config[
            ConfigKey.COLLECTION][
            collection_name][
            ConfigKey.UNSTAGE_PATH
        ]
        return path

    # Progress
    @property
    def progress_bar_increment(self) -> int:
        return self.config[ConfigKey.PROGRESS_BAR_INCREMENT]

    @property
    def terminal_dialog_padding(self) -> int:
        return self.config[ConfigKey.TERMINAL_DIALOG_PADDING]
