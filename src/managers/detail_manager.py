# Avoid hassles managing dictionary details in one location

# imports, python
from types import MappingProxyType

# imports, project
from src.enumerations import ArchiveType


class DetailManager:

    def __init__(self, config):
        self._config = config
        self._hasher_algo = None
        self._mpt_archives = MappingProxyType(self.archives)
        self.metadata = {}

    @property
    def archives(self):
        return dict(self.config['Archives'])

    @property
    def BUF_SIZE(self):
        return self.config['BUF_SIZE']

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def debug(self):
        return self.config['DEBUG']

    @property
    def hash_algo(self):
        return self.config['hash_algo']

    @property
    def hasher_algo(self):
        return self._hasher_algo

    @hasher_algo.setter
    def hasher_algo(self, value):
        self._hasher_algo = value

    @property
    def network_check_count(self):
        return self.config['network_check_count']

    @property
    def network_check_delay(self):
        return self.config['network_check_delay']

    @property
    def require_network(self):
        return self.config['require_network']

    # Archives functions
    def path_archive(self, archive_name):
        return self.archives[archive_name]['archive_path']

    def path_source(self, archive_name):
        return self.archives[archive_name]['source_path']

    def path_stage(self, archive_name):
        return self.archives[archive_name]['stage_path']

    def path_unstage(self, archive_name):
        return self.archives[archive_name]['unstage_path']

    # Metadata functions
    @property
    def unstage_metadata_empty(self):
        unstage_metadata_empty = {
            'type': ArchiveType.archive,
            'unstage': {}
        }
        return unstage_metadata_empty

    @staticmethod
    def archive_metadata_update(archive_metadata, file, metadata):
        archive_metadata['unstage'].update({
            file: metadata
        })

    def read_metadata(self, archive_name):
        return self.metadata[archive_name]

    @staticmethod
    def read_metadata_type(unstage_metadata):
        return unstage_metadata['type']

    def write_metadata(self, archive_name, file_metadata):
        self.metadata[archive_name] = file_metadata

    def update_metadata(self, archive_name, file_metadata):
        self.metadata[archive_name].update({file_metadata})
