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

    def __init__(self, managers):
        """Manage metadata related to staging and unstaging files

        :param managers: collection of management classes
        """

        print(f'Init {self.__class__.__name__}')
        self.conf = managers['config_manager']
        self.meta = managers['metadata_manager']

    def load_metadata(self,
                      collection_metadata: dict,
                      unstage_path: str,
                      file_type: str) -> None:
        """Populate the staging and unstaging metadata

        :param collection_metadata: the collection name
        :param unstage_path: path to the unstaging area
        :file_type: the type of archive to load SOURCE or ARCHIVE
        """
        print(f'load_metadata')
        if file_type == ArchiveType.ARCHIVE:
            self.populate_unstage_metadata(collection_metadata, unstage_path)

    def populate_unstage_metadata(self,
                                  collection_metadata: dict,
                                  unstage_path: str) -> None:
        """Update the unstaging metadata

        :param collection_metadata: dictionary containing details about the archive
        :param unstage_path: path to the unstaging area
        """
        print(f'populate_unstage_metadata')
        self._update_with_unstaging_destinations(collection_metadata, unstage_path)
        self._update_with_soft_links(collection_metadata, unstage_path)

    def _update_with_unstaging_destinations(self,
                                            collection_metadata: dict,
                                            unstage_path: str) -> None:
        """Build the unstaging destinations for each file to be unstaged

        :param collection_metadata: dictionary containing details about the collection
        :param unstage_path: path to the unstaging area
        """
        print(f'_update_with_unstaging_destinations')
        unstage_metadata_dc = copy.deepcopy(collection_metadata)
        for original_file_dc, original_file_metadata_dc in unstage_metadata_dc.items():
            if 'duplicates' not in original_file_metadata_dc:
                continue  # items without duplicates are unprocessed
            duplicate_metadata_dc = original_file_metadata_dc['duplicates']
            for _, duplicate_file_metadata in duplicate_metadata_dc.items():
                unstage_storage_details = \
                    _build_unstage_storage_details(
                        duplicate_file_metadata,
                        unstage_path
                    )

                self.meta.set_unstage_storage_details(
                    collection_metadata,
                    duplicate_file_metadata,
                    unstage_storage_details
                )

    def _update_with_soft_links(self,
                                collection_metadata: dict,
                                unstage_path: str) -> None:
        """Build the soft link destinations for each file to be unstaged

        :param collection_metadata: dictionary containing details about the archive
        :param unstage_path: path to the unstaging area
        """
        print(f'_update_with_soft_links')
        collection_metadata_dc = copy.deepcopy(collection_metadata)
        for original_file_dc, original_file_metadata_dc in collection_metadata_dc.items():
            if 'duplicates' not in original_file_metadata_dc:
                continue  # items without duplicates are unprocessed
            duplicate_metadata_dc = original_file_metadata_dc['duplicates']
            for duplicate_file_dc, duplicate_file_metadata in duplicate_metadata_dc.items():
                soft_link_command = _build_soft_link_command(
                    original_file_dc,
                    unstage_path
                )

                self.meta.set_soft_link_command(
                    collection_metadata,
                    duplicate_file_metadata,
                    soft_link_command
                )

    @staticmethod
    def unstage_files(collection_metadata, file_manager):
        """Execute the unstaging action, moving files from the archive to their
            respective unstaging destination

        :param collection_metadata: dictionary containing details about the archive
        :param file_manager: the file manager class
        """
        print(f'unstage_files')
        for original_file, duplicate_metadata in collection_metadata.items():
            if 'duplicates' not in duplicate_metadata:
                continue  # no duplicates for this file
            duplicate_details = duplicate_metadata['duplicates']
            for duplicate_file, duplicate_details in duplicate_details.items():
                duplicate_unstage_parent_folder = duplicate_details['unstage_parent_folder']
                file_manager.create_required_folders(duplicate_unstage_parent_folder)
                soft_link_command = duplicate_details['soft_link_command']
                file_manager.create_soft_link(soft_link_command)
                file_manager.move_duplicate_file(duplicate_details)


def _build_unstage_storage_details(
        duplicate_file_metadata: dict,
        unstage_path: str) -> dict:
    """Build the unstaging paths

    : param duplicate_file_metadata: duplicate file metadata
    :param unstage_path: the unstaging path
    :return:
    """
    original = duplicate_file_metadata['original']
    unstage_file = duplicate_file_metadata['name']
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
