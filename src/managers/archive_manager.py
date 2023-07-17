# imports, python
import copy
from hashlib import md5
from hashlib import sha1

# imports, project
from config.config import Archives
from config.config import BUF_SIZE
from config.config import hash_algo
from src.lib.lib import read_all_files
from src.managers.archive_metadata_manager import ArchiveMetadataManager
from src.managers.file_manager import FileManager
from src.managers.stage_manager import StageManager

# Hash generators
if hash_algo == 'sha1':
    hasher_also = sha1
elif hash_algo == 'md5':
    hasher_algo = md5
else:
    raise RuntimeError(f'Unknown hash_algo value set : {hash_algo}')


class ArchiveManager:
    """This class finds duplicate files by hashing their contents and comparing
        the hashes to the hashes of other files.

    The archive manager works in a similar fashion to git.
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
        self.archive_metadata_manager = ArchiveMetadataManager(Archives)
        self.file_manager = FileManager()
        self.stage_manager = StageManager()

    def run(self):
        for archive_name, paths in self.archive_metadata_manager.archives.items():
            self.validate_archive(archive_name)
            if self.archive_metadata_manager.read_metadata(archive_name):
                unstage_path = \
                    self.archive_metadata_manager.path_unstage(archive_name)
                self.unstage_duplicates(archive_name, unstage_path)
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
        path_archive = self.archive_metadata_manager.path_archive(archive_name)
        archive_files = read_all_files(path_archive)
        if not archive_files:
            print(f'Archive is empty or path is incorrect : {path_archive}')
            exit()
        unstage_metadata = archive_self_check(generate_hashes(archive_files))
        self.archive_metadata_manager.write_metadata(archive_name, unstage_metadata)

    def unstage_duplicates(self, archive_name, unstage_path):
        archive_duplicates = \
            self.archive_metadata_manager.read_metadata(archive_name)
        self.stage_manager.load_metadata(archive_duplicates, unstage_path)

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
    unstage_metadata = _get_archive_duplicates(archive_hashes)
    if unstage_metadata:
        print(f'Archive invalid, {len(unstage_metadata)} duplicate files '
              f'found')
        return unstage_metadata


def _get_archive_duplicates(archive_hashes):
    unstage_metadata = {
        'type': 'archive',
        'unstage': {}
    }
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
                    print(f'Duplicate file found in archive : {a_file}')
                    # Initialize list of duplicates
                    found_duplicates.append(aa_file)
                    if not duplicate_metadata:
                        duplicate_metadata = {aa_file: {}}
                    else:
                        # Update list of duplicates
                        duplicate_metadata.update({aa_file: {}})
                    unstage_metadata['unstage'].update({
                        a_file: duplicate_metadata
                    })

            # The internal loop has concluded, discard this value
            del archive_hashes_dc[a_file]
            break  # Force restart of the for loop with new dict

    return unstage_metadata


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
