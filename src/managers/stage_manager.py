# A class to handle the staging and unstaging of files
import copy
# imports, python
from pathlib import Path

# imports, project
from src.lib.lib import build_soft_link_command
from src.lib.lib import convert_filepath_to_filename
from src.lib.lib import convert_filepath_to_soft_link_name


class StageManager:

    def __init__(self, detail_manager):
        self.detail_manager = detail_manager

    def load_metadata(self, unstage_metadata, unstage_path):
        archive_type = unstage_metadata['type']
        if archive_type == 'archive':
            self.populate_unstage_metadata(unstage_metadata, unstage_path)

    def populate_unstage_metadata(self, unstage_metadata, unstage_path):
        self._update_with_unstaging_destinations(unstage_metadata, unstage_path)
        self._update_with_soft_links(unstage_metadata, unstage_path)

    @staticmethod
    def _update_with_unstaging_destinations(unstage_metadata, unstage_path):
        file_metadata_dc = copy.deepcopy(unstage_metadata)
        for original_file_dc, unstage_details_dc in file_metadata_dc['unstage'].items():
            for unstage_file_dc, unstage_file_details_dc in unstage_details_dc.items():
                unstage_storage_details = \
                    _build_unstage_storage_details(
                        original_file_dc,
                        unstage_file_dc,
                        unstage_path)
                unstage_metadata['unstage'][
                    original_file_dc][
                    unstage_file_dc].update({
                        'unstage_storage_details': unstage_storage_details})

    @staticmethod
    def _update_with_soft_links(unstage_metadata, unstage_path):
        unstage_metadata_dc = copy.deepcopy(unstage_metadata)
        for original_file_dc, unstage_details_dc in unstage_metadata_dc['unstage'].items():
            for unstage_file_dc, unstage_file_details_dc in unstage_details_dc.items():
                soft_link_command = _build_soft_link_command(
                    original_file_dc,
                    unstage_path
                )
                unstage_metadata['unstage'][
                    original_file_dc][
                    unstage_file_dc].update({
                        'soft_link_command': soft_link_command})

    def stage_files(self):
        pass

    @staticmethod
    def unstage_files(unstage_metadata, file_manager):
        unstage_metadata = unstage_metadata['unstage']
        for original_file, unstage_details in unstage_metadata.items():
            for unstage_file, unstage_file_details in unstage_details.items():
                file_manager.create_required_folders(unstage_file_details)
                soft_link_command = unstage_file_details['soft_link_command']
                file_manager.create_soft_link(soft_link_command)
                file_manager.move_duplicate_files(unstage_file, unstage_file_details)
        pass


def _build_unstage_storage_details(original, unstage_file, unstage_path):
    original_filepath_as_name = convert_filepath_to_filename(original)
    unstage_filepath_as_name = convert_filepath_to_filename(unstage_file)
    unstage_parent_folder = Path(unstage_path, original_filepath_as_name)
    unstage_file_destination = \
        Path(unstage_path, original_filepath_as_name, unstage_filepath_as_name)
    unstage_storage_details = {
        'unstage_parent_folder': unstage_parent_folder,
        'unstage_file_destination': unstage_file_destination
    }
    return unstage_storage_details


def _build_soft_link_command(original, unstage_path):
    soft_link_name = convert_filepath_to_soft_link_name(original)
    soft_link_label = str(Path(unstage_path, soft_link_name, soft_link_name))
    soft_link_command = build_soft_link_command(original, soft_link_label)
    return soft_link_command
