# The manager of collections, the uniqueness of their files, the file metadata,
#   and the files themselves

# imports, python
from collections import namedtuple
from hashlib import md5
from hashlib import sha1
import copy
import sys

# imports, project
from src.enumerations import FileAttribute
from src.enumerations import Progress
from src.lib.lib import loading_dialog
from src.lib.lib import read_all_files


class CollectionManager:
    """This class finds duplicate files by hashing their contents and comparing
        the hashes to the hashes of other files.

    The collection manager works in a similar fashion to git.
        The key locations (in order of timeline) are :
            "source file location" called "source"
            "staging file location" called "stage"
            "graveyard location" called "graveyard"
            "final file destination" called "archive"
            "unstaging file location" called "unstage"
        Files can only move in the following manner :
            source ~> stage
            source ~> graveyard
            archive ~> unstage

    # TODO This feature has not been started yet
    Source Files
        "New" files that are introduced to the system must first be compared
            against every file in the archive. If the source file is found to
            be unique when compared to the archive, then it will be moved to
            the staging area. If that file is not found to be unique, then it
            will be moved to the graveyard.

    Situation A for a source file (source ~> stage) :
        If the hash shows that the file is not a duplicate of an already
            archived file, then the source file will be moved to the staging
            area.
        It is now a staged file. The user (or an automation script) can then
            choose where to put that file in the archive, as it has been shown
            to be unique.

    Situation B for a source file (source ~> graveyard) :
        If the hash shows that the file is a duplicate of an already archived
            file, then the source file will be moved to a "duplicates" area
            called the graveyard where there will also be a soft-link
            generated to the duplicate file in the archive. The user
            (or an automation script) can then choose whether to delete that
            file, as it already exists in the archive.

    Staged Files
        The staged files are files nominated for inclusion in the archive, they
            have been shown to be unique, and do not exist in the archive.

    Graveyard Files
        Files that were in the source, but were already found to have duplicates
            in the archive, they are not unique files.

    Archive Files
        The archive is a collection of unique files.

    This manager has the ability to manage multiple archives, each archive
        will need to have a defined path to :
            1. The archive
            2. The staging area (MUST BE EMPTY AT RUNTIME)
            3. A graveyard area (MUST BE EMPTY AT RUNTIME)
            3. The source file location
            4. The un-staging area (MUST BE EMPTY AT RUNTIME)

    Inevitably, errors will be made when including files in the archive, and
        when a file needs to be removed from the archive, it will be removed
        to the unstaging area from the archive. This can be thought of as a
        recycling bin where files can be evaluated before they are deleted.
    """
    def __init__(self, detail_manager, file_manager, stage_manager):
        """Initialize helper classes and pre-runtime configuration

        :param detail_manager: fetcher and setter of objects in data structure
        :param file_manager: writer, mover, and creator of files/folders
        :param stage_manager: reads and evaluates the archive metadata, uses
            the file_handler to handle files
        """
        print(f'Init {self.__class__.__name__}')

        # Initialize and store helper classes
        self.dm = detail_manager
        self._debug = detail_manager.debug
        self.file_manager = file_manager(detail_manager)
        self.stage_manager = stage_manager(detail_manager)

        # Setup hash generator, selection defined in config
        if detail_manager.hash_algo == 'sha1':
            detail_manager.hasher_algo = sha1
        elif detail_manager.hash_algo == 'md5':
            detail_manager.hasher_algo = md5
        else:
            raise RuntimeError(f'Unknown hash_algo value set : '
                               f'{detail_manager.hash_algo}')

    def run(self) -> None:
        """
        The primary actions of the collection manager. If the archive is
        If the archive is found, it will be parsed.
            If the archive is valid, the source will be parsed.
            If the archive is invalid, the archive will be parsed.
        """
        print(f'Running {self.__class__.__name__}')

        # Iterate through each collection
        for collection_name, collection_paths in self.dm.collection_config.items():
            self.dm.init_collection_metadata(collection_name, collection_paths)

            self.validate_paths(collection_name)
            self.validate_archive(collection_name)

            # If there is metadata then some duplicates were found
            archive_metadata = self.dm.read_metadata(collection_name, 'ARCHIVE')
            # TODO bug, archive metadata is never empty since files are always present
            if archive_metadata:
                self.unstage_archive(archive_metadata, archive_metadata)
            else:
                pass  # TODO, handle a source

    def validate_paths(self, collection_name) -> None:
        # Validate collection paths, create defaults if option enabled
        archive_paths_set_in_config_exist = \
            self.validate_collection_paths(collection_name, 'ARCHIVE')
        create_default_archive_paths = self.dm.create_default_archive_paths
        if not archive_paths_set_in_config_exist and create_default_archive_paths:
            self.file_manager.create_default_archive_paths(self.dm.collection_metadata)

        # Validate source paths, create defaults if option enabled
        source_paths_set_in_config_exist = \
            self.validate_collection_paths(collection_name, 'SOURCE')
        create_default_source_paths = self.dm.create_default_source_paths
        if not source_paths_set_in_config_exist and create_default_source_paths:
            self.file_manager.create_default_source_paths(self.dm.collection_metadata)

    def validate_collection_paths(self, collection_name, paths_type) -> bool:
        # Read the paths associated with the path type
        if paths_type == 'ARCHIVE':
            evaluation_paths = [
                self.dm.get_path_archive(collection_name),
                self.dm.get_path_unstage(collection_name)
            ]
        elif paths_type == 'SOURCE':
            evaluation_paths = [
                self.dm.get_path_source(collection_name),
                self.dm.get_path_graveyard(collection_name),
                self.dm.get_path_stage(collection_name)
            ]
        else:
            raise RuntimeError(f'Unknown value for paths_type : {paths_type}')

        # Check that the defined paths exist
        evaluation_paths_exist = []
        # Iterate over the evaluation paths
        for evaluation_path in evaluation_paths:
            evaluation_paths_exist.append(
                self.file_manager.check_exists(evaluation_path)
            )

        # Evaluate path checks
        if all(evaluation_paths_exist):
            return True
        return False

    def validate_archive(self, collection_name) -> None:
        print(f'validate_archive')

        # Get the path to the archive
        path_archive = self.dm.get_path_archive(collection_name)

        # Read all files at path
        duplicate_metadata = read_all_files(path_archive, self.dm.skip_soft_links)

        self.dm.init_file_metadata(collection_name, duplicate_metadata, 'ARCHIVE')

        # If no files are found
        archive_files = self.dm.get_files(collection_name, 'ARCHIVE')
        if not archive_files:
            print(f'Archive is empty or path is incorrect : {path_archive}')
            exit()

        # Read the files and populate the metadata instructions for unstaging
        file_hashes = self.generate_hashes(collection_name, 'ARCHIVE')

        # Update collection metadata with file hashes
        self.dm.update_file_hashes(collection_name, 'ARCHIVE', file_hashes)
        duplicate_metadata = self.archive_search_for_duplicates(collection_name)

        # Save the metadata instructions to the detail manager
        self.dm.set_duplicate_metadata(collection_name, duplicate_metadata)

    def unstage_archive(self, collection_metadata: dict) -> None:
        print(f'unstage_archive')
        unstage_path = self.dm.get_path_unstage(collection_metadata)
        self.stage_manager.load_metadata(collection_metadata, unstage_path)
        self.stage_manager.unstage_files(collection_metadata, self.file_manager)

    def parse_source(self, source_files):
        print(f'parse_source')  # TODO

    def stage_unique(self, source_files):
        print(f'stage_unique')  # TODO

    def read_source(self, paths):
        print(f'read_source')  # TODO

    def archive_search_for_duplicates(self, collection_name):
        print(f'archive_self_check')

        # Find duplicates
        duplicate_metadata = self._get_archive_duplicates(collection_name)

        # Sort duplicates
        if self.dm.sort_duplicate_hierarchy:
            duplicate_metadata = self._sort_unstage_hierarchy(duplicate_metadata)

        # Announce and return duplicates
        if duplicate_metadata:
            parent_count, children_count = self._count_duplicates(duplicate_metadata)
            if parent_count > 0:
                print(f'Archive invalid, {parent_count} parent file(s) found '
                      f'with {children_count} duplicate children')
            return duplicate_metadata

    def _get_archive_duplicates(self, collection_name) -> dict:
        print(f'_get_archive_duplicates')

        archive_file_metadata = self.dm.get_archive_file_metadata(collection_name, 'ARCHIVE')
        archive_file_metadata_dc = copy.deepcopy(archive_file_metadata)
        found_duplicates = []
        # While dictionary has files
        duplicate_metadata = {}  # Duplicate metadata for all files
        while list(archive_file_metadata_dc.keys()):
            # This flag is used to escape the external for loop after a
            #   duplicate file is found

            # Iterate over a copy of the archive against another copy
            for a_file in archive_file_metadata_dc:
                a_hash = archive_file_metadata_dc[a_file]['HASH']

                if a_file in found_duplicates:
                    del archive_file_metadata_dc[a_file]  # Prevent infinite loop
                    break  # This file is already identified as a duplicate

                # Init duplicate tracking for this a_file
                duplicate_metadata_for_file = {}  # Duplicates for this file
                for aa_file in archive_file_metadata:
                    aa_hash = archive_file_metadata[aa_file]['HASH']

                    if a_file == aa_file:
                        continue  # Do not compare a file with itself

                    # Compare the hashes of differing file paths
                    if a_hash == aa_hash:
                        print(f'Duplicate file found in archive : {aa_file}')
                        # Initialize list of duplicates
                        found_duplicates.append(aa_file)
                        if not duplicate_metadata_for_file:
                            duplicate_metadata_for_file = \
                                self.dm.duplicate_metadata_for_file_init(aa_file)
                        else:
                            # Update collection of duplicates with new init
                            duplicate_metadata_for_file.update({
                                aa_file: {}
                            })

                        duplicate_metadata.update({
                            a_file: duplicate_metadata_for_file
                        })

                # The internal loop has concluded, discard this value
                del archive_file_metadata_dc[a_file]
                break  # Force restart of the for loop with new dict

        return duplicate_metadata

    def _sort_unstage_hierarchy(self, duplicate_metadata):
        print(f'_sort_unstage_hierarchy')

        duplicate_metadata_dc = copy.deepcopy(duplicate_metadata)
        for parent_file, child_files in duplicate_metadata_dc.items():

            # Collect the lengths of each file name
            file_name_data = []
            file_name_datum = \
                namedtuple('file_name_datum', ['index', 'length', 'name'])
            # Collect data for each file
            for idx, file in enumerate([parent_file, * list(child_files)]):
                file_name_data.append(file_name_datum(
                    index=idx,
                    length=len(file),
                    name=file)
                )

            # Get the shortest file length and its index
            # Initial value beyond reasonable file lengths
            shortest_len = self.dm.file_name_len_max_value
            shortest_idx = None
            file_lengths = []
            for file_name_datum in file_name_data:
                file_lengths.append(file_name_datum.length)
                if file_name_datum.length < shortest_len:
                    shortest_idx = file_name_datum.index
                    shortest_len = file_name_datum.length

            if shortest_len == self.dm.file_name_len_max_value:
                raise Exception(f'No file lengths processed')

            # Check if multiple files match the shortest length
            shortest_length = file_name_data[shortest_idx].length
            shortest_count = file_lengths.count(shortest_length)

            # Check if multiple files were the same length
            if shortest_count > 1:  # Two file lengths match, sort alphabetically instead
                # Sort alphabetically
                files_sorted = sorted([parent_file, * list(child_files)])
            else:
                # Sort by shortest file name
                files_sorted = []
                for sorted_file_length in sorted(file_lengths):
                    for file_name_datum in file_name_data:
                        if file_name_datum.length == sorted_file_length:
                            files_sorted.append(file_name_datum.name)
            del duplicate_metadata[parent_file]

            # Update the dictionary with the sorted files
            duplicate_metadata[files_sorted[0]] = {
                file: {} for file in files_sorted[1:]
            }

        return duplicate_metadata

    def generate_hashes(self, collection_name, file_type) -> dict:
        print(f'generate_hashes')

        file_metadata = None
        if file_type == 'ARCHIVE':
            file_metadata = self.dm.get_files(collection_name, 'ARCHIVE')
        elif file_type == 'SOURCE':
            file_metadata = self.dm.get_files(collection_name, 'SOURCE')

        if not file_metadata:
            raise RuntimeError(f'No file metadata')

        file_hashes = {}
        hash_count = 0
        hash_mod = 100
        hashes_needed = len(file_metadata)
        file_metadata_dc = copy.deepcopy(file_metadata)
        for file_dc, file_details_dc in file_metadata_dc.items():
            file_size = \
                self.dm.get_file_size_from(file_metadata, file_dc)
            if not hash_count % hash_mod:
                print(f'Generated {hash_count} of {hashes_needed}..')
            file_hashes[file_dc] = {
                FileAttribute.HASH: self.generate_hash(
                    file_dc,
                    file_size,
                    hash_count,
                    hashes_needed)}
            hash_count += 1
        return file_hashes

    def generate_hash(self,
                      archive_file: str,
                      file_size: int,
                      hash_count: int,
                      hashed_needed: int) -> None:
        """Given a file, generate a hash and return it

        :param archive_file, the path to a file
        :param file_size, the size of the file
        :param hash_count, the number of the hash being processed
        :param hashed_needed, the total number of hashes to be processed
        :return a hash string
        """

        # Initialize loading bar values
        data_read_sum = 0
        large_file = True \
            if file_size > self.dm.large_file_threshold \
            else False

        # Metadata for the loading bar
        progress_bar_increment = self.dm.progress_bar_increment
        progress_metadata = {
            Progress.DATA_READ_SUM: 0,
            Progress.DATA_SIZE: file_size,
            Progress.PERCENTAGE_LAST_UPDATE: -100,
            Progress.PERCENTAGE_NOW: 0,
            Progress.UPDATE_INCREMENT: progress_bar_increment,
        }

        # Only display messages for large files
        if large_file:
            print(f'\nGenerating hash {hash_count + 1} of {hashed_needed}, '
                  f'file : {archive_file}')

        # Get the hash generator
        hasher = self.dm.hasher_algo()

        # Read the file and update progress
        with open(archive_file, 'rb') as af:
            while True:
                data = af.read(self.dm.buf_size)
                data_read_sum += self.dm.buf_size

                # Update progress metadata with file read
                progress_metadata[
                    Progress.DATA_READ_SUM] += self.dm.buf_size

                # Only show loading bars for large files
                if large_file:
                    display_loading_dialog(progress_metadata)
                if not data:
                    if large_file:
                        display_loading_dialog(complete=True)
                    break
                hasher.update(data)
        return hasher.hexdigest()

    def _count_duplicates(self, duplicate_metadata):
        parent_count = self.dm.get_parent_count_from(duplicate_metadata)
        children_count = 0

        # Count the children duplicates
        for _, children in duplicate_metadata.items():
            children_count += len(children)

        return parent_count, children_count


def display_loading_dialog(progress_metadata=None, complete=False):
    """Print a loading bar to the console for large files

    :param progress_metadata: tells the progress bar what to display
    :param complete: a flag that indicates there is no more data to be read
    :return: percentage_now, percentage_last_update, the most recent
        completion percentage and the current completion percentage, their
        relative values are used to determine when to udpate the loading bar
    """

    # No data remaining, display final dialog
    if complete:
        sys.stdout.write(f'\r100% {loading_dialog(100)}')
        return

    # Convenience variable, read the most recent percentage
    percentage_last_update = progress_metadata[Progress.PERCENTAGE_LAST_UPDATE]

    # Calculate the current percentage that has been read
    data_read_sum = progress_metadata[Progress.DATA_READ_SUM]
    data_size = progress_metadata[Progress.DATA_SIZE]
    percentage_now = 100 * data_read_sum / data_size

    # Determine if an update needs to be displayed
    increment = progress_metadata[Progress.UPDATE_INCREMENT]
    if percentage_last_update + increment < percentage_now < 99:
        percentage_last_update = percentage_now
        sys.stdout.write(
            f'\r{int(percentage_now)} %'
            f'{loading_dialog(percentage_now)}')

    # Update progress metadata with current state
    progress_metadata[Progress.PERCENTAGE_LAST_UPDATE] = percentage_last_update
    progress_metadata[Progress.PERCENTAGE_NOW] = percentage_now
    return percentage_now, percentage_last_update


