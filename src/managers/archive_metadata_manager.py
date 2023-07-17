# imports, python
from types import MappingProxyType


class ArchiveMetadataManager:
    def __init__(self, archives):
        # Make archives dict immutable
        self._mpt_archives = MappingProxyType(archives)
        self.metadata = {}

    # Archives functions
    @property
    def archives(self):
        return dict(self._mpt_archives)

    def path_archive(self, archive_name):
        return self.archives[archive_name]['archive_path']

    def path_source(self, archive_name):
        return self.archives[archive_name]['source_path']

    def path_stage(self, archive_name):
        return self.archives[archive_name]['stage_path']

    def path_unstage(self, archive_name):
        return self.archives[archive_name]['unstage_path']

    # Metadata functions
    def read_metadata(self, archive_name):
        return self.metadata[archive_name]

    def write_metadata(self, archive_name, file_metadata):
        self.metadata[archive_name] = file_metadata

    def update_metadata(self, archive_name, file_metadata):
        self.metadata[archive_name].update({file_metadata})
