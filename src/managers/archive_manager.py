# The manager of archives, the uniqueness of their files, the file metadata,
#   and the files themselves

# imports, python
from collections import namedtuple
from hashlib import md5
from hashlib import sha1
from os import listdir
import copy
import sys

# imports, project
from src.enumerations import Progress
from src.lib.lib import loading_dialog
from src.lib.lib import read_all_files


class ArchiveManager:
    """This class finds duplicate files by hashing their contents and comparing
        the hashes to the hashes of other files.

    The archive manager works in a similar fashion to git.
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

    # TODO This feature is not operational
    Source Files
        "New" files that are introduced to the system must first be compared
            against every file in the archive. If the source file is found to
            be unique when compared to the archive, then it will be moved to
            the staging area. If that file is not found to be unique, then it
            will be moved to the graveyard.

    Situation A for a source file (source ~> stage) :
        If the hash shows that the file is not a duplicate of an already
        archived file, then the source file will be moved to the staging area.
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
            1. The archive itself
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
        self.detail_manager = detail_manager
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
        The primary actions of the archive manager. If the archive is
            found to be invalid for any reason then the source will not
            be parsed and instead the archive itself will be parsed and
            staged.
        If the archive is found to be valid, then the source will be
            parsed and staged.
        The archive is valid when it contains no duplicate files.
        """
        print(f'Running {self.__class__.__name__}')

        # Iterate through each archive
        for archive_name, paths in self.detail_manager.archives.items():

            # Validate staging, unstaging, and graveyard areas
            #   If those locations are not empty this will fail
            self.validate_path_empty(archive_name, 'UNSTAGE')
            self.validate_path_empty(archive_name, 'STAGE')
            self.validate_path_empty(archive_name, 'GRAVEYARD')

            # Validate there are no duplicate files in the archive
            self.validate_archive(archive_name)

            # If there are duplicate files found in the archive, begin the
            #   unstaging process, the source will not be evaluated this run
            if self.detail_manager.read_metadata(archive_name):
                unstage_path = self.detail_manager.path_unstage(archive_name)
                self.unstage_archive(archive_name, unstage_path)
            else:
                # TODO features below are placeholder functions, at the moment
                #   this program only evaluates the archive
                # The archive is valid, parse the source for staging
                # Validate source and staging paths
                self.validate_source_path(archive_name)

                # Read files from the source path
                source_filedata = self.parse_source(self.read_source(archive_name))
                # Compare the source to the archive
                # Stage unique source files
                self.stage_unique(source_filedata)

    def validate_archive(self, archive_name: str) -> None:
        """Validate the archive by reading file metadata. Populate the file
            metadata and resume
        :arg, archive_name: a string that allows the archive manager to know
            which archive is being validated.
        """
        print(f'validate_archive')

        # Get the path to the archive
        path_archive = self.detail_manager.path_archive(archive_name)
        skip_soft_links = self.detail_manager.skip_soft_links
        archive_files = read_all_files(path_archive, skip_soft_links)

        # If no files are found
        if not archive_files:
            print(f'Archive is empty or path is incorrect : {path_archive}')
            exit()

        # Read the files and populate the metadata instructions for unstaging
        archive_metadata = \
            self.archive_self_check(
                self.generate_hashes(archive_files, self.detail_manager))

        # Save the metadata instructions to the detail manager
        self.detail_manager.write_metadata(archive_name, archive_metadata)

    def validate_path_empty(self, archive_name: str, path_label: str):

        # Exit program if path is not empty
        if path_label == 'GRAVEYARD':
            path_to_validate = self.detail_manager.path_graveyard(archive_name)
        elif path_label == 'STAGE':
            path_to_validate = self.detail_manager.path_stage(archive_name)
        elif path_label == 'UNSTAGE':
            path_to_validate = self.detail_manager.path_unstage(archive_name)
        else:
            print(f'Invalid path label {path_label}')
            exit()
        path_contents = listdir(path_to_validate)
        if path_contents:
            print(f'The {path_label} area : {path_to_validate} is not empty')
            print('This directory is required to be empty to prevent data loss')
            print('Program will now exit')
            exit()

    def unstage_archive(self, archive_name: str, unstage_path: str) -> None:
        """Read the populated file metadata, load it into the stage
            manager, and the stage manager will unstage the files.
        :arg, archive_name: a string that allows the archive manager to know
            which archive is being validated.
        :arg, unstage_path: a string that points to the unstaging parent
            folder, which is where unstaged files will be moved
        """
        print(f'unstage_archive')

        archive_metadata = \
            self.detail_manager.read_metadata(archive_name)
        self.stage_manager.load_metadata(archive_metadata, unstage_path)
        self.stage_manager.unstage_files(archive_metadata, self.file_manager)

    def validate_source_path(self, archive_name):
        print(f'validate_source_path')  # TODO

    def parse_source(self, source_files):
        print(f'parse_source')  # TODO

    def stage_unique(self, source_files):
        print(f'stage_unique')  # TODO

    def read_source(self, paths):
        print(f'read_source')  # TODO

    def archive_self_check(self, archive_hashes: dict):
        """Process the list of files and included hashes in order to find duplicate
            files.
        :arg, archive_hashes: a dict of hash values keyed by file path
        :return, archive_metadata: an initialized metadata container for
            duplicate files with empty dictionaries initialized for each
            file
        """
        print(f'archive_self_check')

        archive_metadata = self._get_archive_duplicates(archive_hashes)
        if self.detail_manager.sort_duplicate_hierarchy:
            archive_metadata = self._sort_unstage_hierarchy(archive_metadata)
        if archive_metadata:
            parent_count, children_count = _count_duplicates(archive_metadata)
            print(f'Archive invalid, {parent_count} parent file(s) found with '
                  f'{children_count} duplicate children')
            return archive_metadata

    def _get_archive_duplicates(self, archive_hashes: dict) -> dict:
        """Find non-unique files in the archive_hashes dictionary
        :arg, archive_hashes: a dictionary of hash values keyed by the file path
            used to generate them
        :returns, archive_metadata: data about the duplicate files that will help
            to relocate them out of the archive
        """
        print(f'_get_archive_duplicates')

        archive_metadata = self.detail_manager.archive_metadata_empty
        archive_hashes_dc = copy.deepcopy(archive_hashes)
        found_duplicates = []
        # While dictionary has files
        while list(archive_hashes_dc.keys()):
            # This flag is used to escape the external for loop after a
            #   duplicate file is found

            # Iterate over a copy of the archive against another copy
            for a_file, a_hash in archive_hashes_dc.items():

                if a_file in found_duplicates:
                    del archive_hashes_dc[a_file]  # Prevent infinite loop
                    break  # This file is already identified as a duplicate

                # Init duplicate tracking for this a_file
                duplicate_metadata = {}  # Duplicates for this file
                for aa_file, aa_hash in archive_hashes.items():

                    if a_file == aa_file:
                        continue  # Do not compare a file with itself

                    # Compare the hashes of differing file paths
                    if a_hash == aa_hash:
                        print(f'Duplicate file found in archive : {aa_file}')
                        # Initialize list of duplicates
                        found_duplicates.append(aa_file)
                        if not duplicate_metadata:
                            duplicate_metadata = \
                                self.detail_manager.duplicate_metadata_init(aa_file)
                        else:
                            # Update collection of duplicates with new init
                            self.detail_manager.duplicate_metadata_add_new_entry(
                                duplicate_metadata,
                                aa_file
                            )

                        self.detail_manager.archive_metadata_update(
                            archive_metadata,
                            a_file,
                            duplicate_metadata
                        )

                # The internal loop has concluded, discard this value
                del archive_hashes_dc[a_file]
                break  # Force restart of the for loop with new dict

        return archive_metadata

    def _sort_unstage_hierarchy(self, archive_details):
        """Extracts the original file and duplicate files, reads their
            length, and declares the shortest file name to be
            the original. If more than one file matches the length of the
            shortest file, then sort them alphabetically and declare the
            'first' file to be the new parent. This is obviously not
            necessary, so it can be skipped in the configuration.
        :arg, archive_details: metadata about the archive duplicates,
            containing empty containers for each duplicate file
        """
        print(f'_sort_unstage_hierarchy')

        unstage = self.detail_manager.read_unstage(archive_details)
        unstage_dc = copy.deepcopy(unstage)
        for parent_file, child_files in unstage_dc.items():

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
            shortest_len = self.detail_manager.file_name_len_max_value
            shortest_idx = None
            file_lengths = []
            for file_name_datum in file_name_data:
                file_lengths.append(file_name_datum.length)
                if file_name_datum.length < shortest_len:
                    shortest_idx = file_name_datum.index
                    shortest_len = file_name_datum.length

            if shortest_len == self.detail_manager.file_name_len_max_value:
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
            del unstage[parent_file]

            # Update the dictionary with the sorted files
            unstage[files_sorted[0]] = {
                file: {} for file in files_sorted[1:]
            }

        return archive_details

    def generate_hashes(self, archive_files: dict, detail_manager) -> dict:
        """Given a list of files, generate hashes for each
        :arg, archive_files, a dict of file sizes keyed by file path
        :arg, detail_manager, the container for the hashing function
        """
        print(f'generate_hashes')

        archive_hashes = {}
        hash_count = 0
        hash_mod = 100
        hashes_needed = len(archive_files)
        for file, file_details in archive_files.items():
            file_size = file_details['st_size']
            if not hash_count % hash_mod:
                print(f'Generated {hash_count} of {hashes_needed}..')
            archive_hashes.update({
                file: self.generate_hash(
                    file,
                    file_size,
                    detail_manager,
                    hash_count,
                    hashes_needed
                )
            })
            hash_count += 1
        return archive_hashes

    def generate_hash(self,
                      archive_file: str,
                      file_size: int,
                      detail_manager,
                      hash_count: int,
                      hashed_needed: int) -> None:
        """Given a file, generate a hash and return it

        :param archive_file, the path to a file
        :param file_size, the size of the file
        :param detail_manager, access to configuration and helper functions
        :param hash_count, the number of the hash being processed
        :param hashed_needed, the total number of hashes to be processed
        :return a hash string
        """

        # Initialize loading bar values
        data_read_sum = 0
        large_file = True \
            if file_size > self.detail_manager.large_file_threshold \
            else False

        # Metadata for the loading bar
        progress_bar_increment = self.detail_manager.progress_bar_increment()
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
        hasher = detail_manager.hasher_algo()

        # Read the file and update progress
        with open(archive_file, 'rb') as af:
            while True:
                data = af.read(detail_manager.buf_size)
                data_read_sum += detail_manager.buf_size

                # Update progress metadata with file read
                progress_metadata[
                    Progress.DATA_READ_SUM] += detail_manager.buf_size

                # Only show loading bars for large files
                if large_file:
                    display_loading_dialog(progress_metadata)
                if not data:
                    display_loading_dialog(complete=True)
                    break
                hasher.update(data)
        return hasher.hexdigest()


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


def _count_duplicates(archive_metadata):
    """Count duplicate parents and children

    :param archive_metadata: the archive metadata containing details about
        duplicate files
    :return: parent_count, children_count, the number of parent duplicate files
        and the number of children duplicates
    """
    unstage_archive = archive_metadata['UNSTAGE']
    parent_count = len(archive_metadata['UNSTAGE'])
    children_count = 0

    # Count the children duplicates
    for _, children in unstage_archive.items():
        children_count += len(children)

    return parent_count, children_count
