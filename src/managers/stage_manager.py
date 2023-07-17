# A class to handle the staging and unstaging of files

class StageManager:

    def run(self, action):
        if action == 'unstage':
            self.pre_unstage_files()
            self.unstage_files()
        elif action == 'stage':
            self.pre_stage_files()
            self.stage_files()

    def load_metadata(self, file_metadata):
        archive_type = file_metadata['type']
        if archive_type == 'archive':
            self.load_archive_metadata(file_metadata)
        pass

    def load_archive_metadata(self, file_metadata):
        self._update_with_unstaging_folders(file_metadata)
        self._update_with_soft_links(file_metadata)

    def _update_with_unstaging_folders(self, file_metadata):
        for original_file, unstage_details in file_metadata['unstage'].items():
            pass

    def _update_with_soft_links(self, file_metadata):
        for original_file, unstage_details in file_metadata['unstage'].items():
            pass

    def pre_stage_files(self):
        pass

    def pre_unstage_files(self):
        pass

    def stage_files(self):
        pass

    def unstage_files(self):
        pass
