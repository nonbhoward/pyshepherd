# imports, python
import copy
from hashlib import md5
from hashlib import sha1
from os import walk
from pathlib import Path

# imports, project
from config.config import archives
from config.config import BUF_SIZE
from config.config import hash_algo
from src.lib import get_filename_from
from src.lib import transform_file_path_to_folder
from src.lib import transform_file_path_to_soft_link
from src.managers.archive_metadata_manager import ArchiveMetadataManager
from src.managers.file_manager import FileManager

# Hash generators
if hash_algo == 'sha1':
    hasher_also = sha1
elif hash_algo == 'md5':
    hasher_algo = md5
else:
    raise RuntimeError(f'Unknown hash_algo value set : {hash_algo}')


class DuplicateManager:
    """This class finds duplicate files by hashing their contents and comparing
        the hashes to the hashes of other files.

    The duplicate manager works in a similar fashion to git.
        The key locations (in order of timeline) are :
            "source file location" called "source"
            "staging file location" called "stage"
            "final file destination" called "archive"
            "unstaging file location" called "unstage"

    Every file will first start as a source file, it will be hashed, and that
        hash will be compared against every hash in the archive.

    Situation A for a source file :
        If the hash shows that the file is not a duplicate of an already
        archived file, then the source file will be moved to the staging area.
        It is now a staged file. The user (or an automation script) can then
            choose where to put that file in the archive, as it has been shown
            to be unique.

    Situation B for a source file :
        If the hash shows that the file is a duplicate of an already archived
            file, then the source file will be moved to a "duplicates" area,
            where there will also be a soft-link generated to the duplicate
            file in the archive. The user (or an automation script) can then
            choose whether to delete that file, as it already exists in
            the archive.

    The staged files are files nominated for inclusion in the archive, they
        have been shown to be unique, and do not exist in the archive.

    The archive is a collection of unique files.

    This manager has the ability to manage multiple archives, each archive
        will need to have a defined path to :
            1. The archive itself
            2. The staging area
            3. The source file location
            4. The un-staging area

    Inevitably, errors will be made when including files in the archive, and
        when a file needs to be removed from the archive, it will be removed
        to the unstaging area from the archive. This can be thought of as a
        recycling bin where files can be evaluated before they are deleted.
    """
    def __init__(self, debug=False):
        self._debug = debug
        # Store metadata about each archive
        self.amm = ArchiveMetadataManager(archives)
        self.fm = FileManager()

    def run(self):
        for archive_name, paths in self.amm.archives.items():
            self.amm.md = ArchiveMetadataManager.Metadata(archive_name)
            self.validate_archive(archive_name)
            if self.amm.md.get_duplicates(archive_name):
                self.unstage_duplicates(archive_name)
            else:
                # Validate source and staging paths
                self.validate_source_path(archive_name)
                self.validate_stage_path(archive_name)
                # Read the source
                # Compare the source to the archive
                source_filedata = \
                    self.parse_source(self.read_source(archive_name))
                # Stage unique source files
                self.stage_unique(source_filedata)

    def validate_archive(self, archive_name):
        """Verify that the archive contains no duplicate files"""
        path_archive = self.amm.path_archive(archive_name)
        archive_files = read_all_files(path_archive)
        if not archive_files:
            print(f'Archive is empty or path is incorrect : {path_archive}')
            exit()
        duplicates = archive_self_check(generate_hashes(archive_files))
        self.amm.md.set_duplicates(archive_name, duplicates)

    def unstage_duplicates(self, archive_name):
        archive_duplicates = self.amm.md.get_duplicates(archive_name)
        for original, duplicates in archive_duplicates.items():
            for duplicate in duplicates:
                self.unstage_duplicate(archive_name, original, duplicate)

    def unstage_duplicate(self, archive_name, original, duplicate):
        unstage_path = self.amm.path_unstage(archive_name)
        unstaging_metadata = build_unstaging_metadata_for(unstage_path, original, duplicate)
        self.fm.unstage(unstaging_metadata)

    def validate_source_path(self):
        pass

    def validate_stage_path(self):
        pass

    def parse_source(self, source_files):
        return ''

    def stage_unique(self, source_files):
        pass

    def read_source(self, paths):
        path_source = paths['source']
        return ''


def archive_self_check(archive_hashes):
    archive_duplicates = _get_archive_duplicates(archive_hashes)
    if archive_duplicates:
        print(f'Archive is invalid, {len(archive_duplicates)} duplicate files '
              f'found')
        return archive_duplicates


def _get_archive_duplicates(archive_hashes):
    archive_duplicates = {}
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
            duplicate_list = []  # Duplicates for this file
            for aa_file, aa_hash in archive_hashes.items():

                if a_file == aa_file:
                    continue  # Do not compare a file with itself

                # Compare the hashes of differing file paths
                if a_hash == aa_hash:
                    print(f'Duplicate file found in archive : {a_file}')
                    # Initialize list of duplicates
                    found_duplicates.append(aa_file)
                    if not duplicate_list:
                        duplicate_list = [aa_file]
                    else:
                        # Update list of duplicates
                        duplicate_list.append(aa_file)
                    archive_duplicates.update({
                        a_file: duplicate_list
                    })

            # The internal loop has concluded, discard this value
            del archive_hashes_dc[a_file]
            break  # Force restart of the for loop with new dict

    return archive_duplicates


def generate_hashes(archive_files):
    archive_hashes = {}
    for archive_file in archive_files:
        archive_hashes.update({
            archive_file: generate_hash(archive_file)
        })
    return archive_hashes


def generate_hash(archive_file):
    hasher = hasher_algo()
    with open(archive_file, 'rb') as af:
        while True:
            data = af.read(BUF_SIZE)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def read_all_files(path):
    all_files = []
    for root, _, files in walk(path):
        for file in files:
            all_files.append(root + '/' + file)
    return all_files


def read_source(archive):
    pass


def build_unstaging_metadata_for(unstage_path, original, duplicate):
    # Generate the metadata to return
    soft_link_to_original = transform_file_path_to_soft_link(original)
    duplicate_filename = get_filename_from(duplicate)
    unstaged_destination_for_duplicate = \
        build_unstaged_destination_for(unstage_path, original)

    # Package and return the metadata
    unstaging_metadata = {
        'path_to_duplicate': duplicate,
        'path_to_original': original,
        'soft_link_name': soft_link_to_original,
        'unstage_path': unstaged_destination_for_duplicate,
    }
    return unstaging_metadata


def build_unstaged_destination_for(unstage_path, original_filename):
    # Use the original filename as the container for duplicates,
    #   to avoid spawning a folder per duplicate
    duplicate_folder = transform_file_path_to_folder(original_filename)
    unstaged_destination = Path(unstage_path, duplicate_folder)
    return unstaged_destination
