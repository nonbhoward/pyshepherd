# A class to handle the staging and unstaging of files

# imports, python
import copy
from pathlib import Path

# imports, project
from src.lib.lib import build_soft_link_command
from src.lib.lib import convert_filepath_to_filename
from src.lib.lib import convert_filepath_to_soft_link_name
from src.enumerations import ArchiveType


class StageManager:

    def __init__(self, detail_manager):
        """Manage metadata related to staging and unstaging files

        :param detail_manager: access to configuration and helper objects
        """

        print(f'Init {self.__class__.__name__}')
        self.detail_manager = detail_manager

    def load_metadata(self, archive_metadata: dict, unstage_path: str) -> None:
        """Populate the staging and unstaging metadata

        :param archive_metadata: dictionary containing details about the archive
        :param unstage_path: path to the unstaging area
        """
        print(f'load_metadata')
        archive_type = self.detail_manager.read_metadata_type(archive_metadata)
        if archive_type == ArchiveType.ARCHIVE:
            self.populate_unstage_metadata(archive_metadata, unstage_path)

    def populate_unstage_metadata(self,
                                  archive_metadata: dict,
                                  unstage_path: str) -> None:
        """Update the unstaging metadata

        :param archive_metadata: dictionary containing details about the archive
        :param unstage_path: path to the unstaging area
        """
        print(f'populate_unstage_metadata')
        self._update_with_unstaging_destinations(archive_metadata, unstage_path)
        self._update_with_soft_links(archive_metadata, unstage_path)

    def _update_with_unstaging_destinations(self,
                                            archive_metadata: dict,
                                            unstage_path: str) -> None:
        """Build the unstaging destinations for each file to be unstaged

        :param archive_metadata: dictionary containing details about the archive
        :param unstage_path: path to the unstaging area
        """
        print(f'_update_with_unstaging_destinations')
        unstage_metadata_dc = copy.deepcopy(
            self.detail_manager.read_unstage(archive_metadata)
        )
        for original_file_dc, unstage_details_dc in unstage_metadata_dc.items():
            for unstage_file_dc, unstage_file_details_dc in unstage_details_dc.items():
                unstage_storage_details = \
                    _build_unstage_storage_details(
                        original_file_dc,
                        unstage_file_dc,
                        unstage_path)
                self.detail_manager.set_unstage_storage_details(
                    archive_metadata,
                    original_file_dc,
                    unstage_file_dc,
                    unstage_storage_details
                )

    def _update_with_soft_links(self,
                                archive_metadata: dict,
                                unstage_path: str) -> None:
        """Build the soft link destinations for each file to be unstaged

        :param archive_metadata: dictionary containing details about the archive
        :param unstage_path: path to the unstaging area
        """
        print(f'_update_with_soft_links')
        archive_metadata_dc = copy.deepcopy(archive_metadata)
        unstage_metadata_dc = \
            self.detail_manager.read_unstage_from(archive_metadata_dc)
        for original_file_dc, unstage_details_dc in unstage_metadata_dc.items():
            for unstage_file_dc, unstage_file_details_dc in unstage_details_dc.items():
                soft_link_command = _build_soft_link_command(
                    original_file_dc,
                    unstage_path
                )
                archive_metadata['UNSTAGE'][
                    original_file_dc][
                    unstage_file_dc].update({
                        'soft_link_command': soft_link_command})

    def stage_files(self):
        print()  # TODO

    @staticmethod
    def unstage_files(archive_metadata, file_manager):
        """Execute the unstaging action, moving files from the archive to their
            respective unstaging destination

        :param archive_metadata: dictionary containing details about the archive
        :param unstage_path: path to the unstaging area
        """
        print(f'unstage_files')
        unstage_metadata = archive_metadata['UNSTAGE']
        for original_file, unstage_details in unstage_metadata.items():
            for unstage_file, unstage_file_details in unstage_details.items():
                file_manager.create_required_folders(unstage_file_details)
                soft_link_command = unstage_file_details['soft_link_command']
                file_manager.create_soft_link(soft_link_command)
                file_manager.move_duplicate_file(unstage_file, unstage_file_details)


def _build_unstage_storage_details(original: str,
                                   unstage_file: str,
                                   unstage_path: str) -> dict:
    """Build the unstaging paths

    :param original: the parent file for the duplicate to be unstaged
    :param unstage_file: the duplicate file to be moved to unstaging
    :param unstage_path: the unstaging path
    :return:
    """
    original_filepath_as_name = convert_filepath_to_filename(original)
    unstage_filepath_as_name = convert_filepath_to_filename(unstage_file)
    unstage_parent_folder = str(Path(unstage_path, original_filepath_as_name))
    unstage_file_destination = \
        str(Path(unstage_path, original_filepath_as_name, unstage_filepath_as_name))
    unstage_storage_details = {
        'unstage_parent_folder': unstage_parent_folder,
        'unstage_file_destination': unstage_file_destination
    }
    return unstage_storage_details


def _build_soft_link_command(original: str, unstage_path: str) -> list:
    """

    :param original: the parent file at which the soft link will point
    :param unstage_path: the unstaging path
    """
    soft_link_name = convert_filepath_to_soft_link_name(original)
    soft_link_label = str(Path(unstage_path, soft_link_name, soft_link_name))
    soft_link_command = build_soft_link_command(original, soft_link_label)
    return soft_link_command
