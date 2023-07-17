# A class to handle the staging and unstaging of files
import copy
# imports, python
from pathlib import Path

# imports, project
from src.lib.lib import build_soft_link_command
from src.lib.lib import convert_filepath_to_filename
from src.lib.lib import convert_filepath_to_soft_link_name


class StageManager:

    def run(self, action):
        if action == 'unstage':
            self.pre_unstage_files()
            self.unstage_files()
        elif action == 'stage':
            self.pre_stage_files()
            self.stage_files()

    def load_metadata(self, file_metadata, unstage_path):
        archive_type = file_metadata['type']
        if archive_type == 'archive':
            self.populate_unstage_metadata(file_metadata, unstage_path)

    def populate_unstage_metadata(self, file_metadata, unstage_path):
        self._update_with_unstaging_destinations(file_metadata, unstage_path)
        self._update_with_soft_links(file_metadata, unstage_path)

    @staticmethod
    def _update_with_unstaging_destinations(file_metadata, unstage_path):
        file_metadata_dc = copy.deepcopy(file_metadata)
        for original_file_dc, unstage_details_dc in file_metadata_dc['unstage'].items():
            for unstage_file_dc, unstage_file_details_dc in unstage_details_dc.items():
                unstage_destination = \
                    _build_unstage_storage_path(
                        original_file_dc,
                        unstage_file_dc,
                        unstage_path)
                file_metadata['unstage'][
                    original_file_dc][
                    unstage_file_dc].update({
                        'unstage_destination': unstage_destination})

    @staticmethod
    def _update_with_soft_links(file_metadata, unstage_path):
        file_metadata_dc = copy.deepcopy(file_metadata)
        for original_file_dc, unstage_details_dc in file_metadata_dc['unstage'].items():
            for unstage_file_dc, unstage_file_details_dc in unstage_details_dc.items():
                soft_link_command = _build_soft_link_command(
                    original_file_dc,
                    unstage_path
                )
                file_metadata['unstage'][
                    original_file_dc][
                    unstage_file_dc].update({
                        'soft_link_command': soft_link_command})

    def pre_stage_files(self):
        pass

    def pre_unstage_files(self):
        pass

    def stage_files(self):
        pass

    def unstage_files(self):
        pass


def _build_unstage_storage_path(original, unstage_file, unstage_path):
    original_filepath_as_name = convert_filepath_to_filename(original)
    unstage_filepath_as_name = convert_filepath_to_filename(unstage_file)
    unstage_destination = Path(unstage_path, original_filepath_as_name, unstage_filepath_as_name)
    return unstage_destination


def _build_soft_link_command(original, unstage_path):
    soft_link_name = convert_filepath_to_soft_link_name(original)
    soft_link_label = str(Path(unstage_path, soft_link_name, soft_link_name))
    soft_link_command = build_soft_link_command(original, soft_link_label)
    return soft_link_command
