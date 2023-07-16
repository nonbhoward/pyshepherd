# imports, python
from types import MappingProxyType


class ArchiveMetadataManager:
    def __init__(self, archives):
        # Make archives dict immutable
        self.mpt_archives = MappingProxyType(archives)

    class Metadata:
        def __init__(self, archive_name):
            self.duplicates = {
                archive_name: {
                    'duplicates': []
                }
            }

        def get_duplicates(self, archive_name):
            return self.duplicates[archive_name]['duplicates']

        def set_duplicates(self, archive_name, duplicates):
            self.duplicates = {
                archive_name: {
                    'duplicates': duplicates
                }
            }

    @property
    def archives(self):
        return self.mpt_archives

    def path_archive(self, archive_name):
        return self.archives[archive_name]['archive_path']

    def path_source(self, archive_name):
        return self.archives[archive_name]['source_path']

    def path_stage(self, archive_name):
        return self.archives[archive_name]['stage_path']

    def path_unstage(self, archive_name):
        return self.archives[archive_name]['unstage_path']
