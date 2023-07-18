# The manager of archives, the uniqueness of their files, the file metadata,
#   and the files themselves

# imports, python
import copy
from hashlib import md5
from hashlib import sha1

# imports, project
from src.lib.lib import read_all_files


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
    def __init__(self, detail_manager, file_manager, stage_manager):
        self.detail_manager = detail_manager
        self._debug = detail_manager.debug

        # Store metadata about each archive
        self.file_manager = file_manager(detail_manager)
        self.stage_manager = stage_manager(detail_manager)

        # Setup hash generator
        if detail_manager.hash_algo == 'sha1':
            detail_manager.hasher_algo = sha1
        elif detail_manager.hash_algo == 'md5':
            detail_manager.hasher_algo = md5
        else:
            raise RuntimeError(f'Unknown hash_algo value set : '
                               f'{detail_manager.hash_algo}')

    def run(self) -> None:
        """The primary actions of the archive manager. If the archive is
            found to be invalid then the source will not be parsed.
            If the archive is found to be valid, then the source will be
            parsed. The archive is valid when it contains no duplicate
            files.
        """
        # Iterate through each archive and perform management actions
        for archive_name, paths in self.detail_manager.archives.items():

            # Validate that there are no duplicate files in the archive
            self.validate_archive(archive_name)

            # If there are duplicate files found in the archive, then there
            #   will be metadata. These duplicate files will trigger unstaging
            #   of those files to begin
            if self.detail_manager.read_metadata(archive_name):
                unstage_path = self.detail_manager.path_unstage(archive_name)
                self.unstage_archive(archive_name, unstage_path)
            else:  # The archive is valid, process the source for staging
                # Validate source and staging paths
                self.validate_source_path(archive_name)
                self.validate_stage_path(archive_name)

                # Read files from the source path
                source_filedata = self.parse_source(self.read_source(archive_name))
                # Compare the source to the archive
                # Stage unique source files
                self.stage_unique(source_filedata)

    def validate_archive(self, archive_name: str) -> None:
        """Validate the archive by reading file metadata. Unstage the
            duplicate files.
        :arg, archive_name: a string that allows the archive manager to know
            which archive is being validated.
        """

        # Get the path to the archive
        path_archive = self.detail_manager.path_archive(archive_name)
        archive_files = read_all_files(path_archive)

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

    def unstage_archive(self, archive_name: str, unstage_path: str) -> None:
        """Read the populated file metadata, load it into the stage
            manager, and the stage manager will unstage the files.
        :arg, archive_name: a string that allows the archive manager to know
            which archive is being validated.
        :arg, unstage_path: a string that points to the unstaging parent
            folder, which is where unstaged files will be moved
        """
        archive_metadata = \
            self.detail_manager.read_metadata(archive_name)
        self.stage_manager.load_metadata(archive_metadata, unstage_path)
        self.stage_manager.unstage_files(archive_metadata, self.file_manager)

    def validate_source_path(self, archive_name):
        pass

    def validate_stage_path(self, archive_name):
        pass

    def parse_source(self, source_files):
        return ''

    def stage_unique(self, source_files):
        pass

    def read_source(self, paths):
        path_source = self.detail_manager.path_source
        return ''

    def archive_self_check(self, archive_hashes: dict):
        """Process the list of files and included hashes in order to find duplicate
            files.
        :arg, archive_hashes: a dict of hash values keyed by file path
        :return, archive_metadata: an initialized metadata container for
            duplicate files with empty dictionaries initialized for each
            file
        """
        archive_metadata = self._get_archive_duplicates(archive_hashes)
        if archive_metadata:
            print(f'Archive invalid, {len(archive_metadata)} duplicate files '
                  f'found')
            return archive_metadata

    def _get_archive_duplicates(self, archive_hashes: dict) -> dict:
        """Find non-unique files in the archive_hashes dictionary
        :arg, archive_hashes: a dictionary of hash values keyed by the file path
            used to generate them
        :returns, archive_metadata: data about the duplicate files that will help
            to relocate them out of the archive
        """
        archive_metadata = self.detail_manager.unstage_metadata_empty
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

                        self.detail_manager.archive_metadata_update(
                            archive_metadata,
                            a_file,
                            duplicate_metadata
                        )

                # The internal loop has concluded, discard this value
                del archive_hashes_dc[a_file]
                break  # Force restart of the for loop with new dict

        return archive_metadata

    def generate_hashes(self, archive_files: list, detail_manager) -> dict:
        """Given a list of files, generate hashes for each
        :arg, archive_files, a list of files
        :arg, detail_manager, the container for the hashing function
        :return, archive_hashes, a dictionary of hashes keyed by the file path used to
            generate them
        """
        archive_hashes = {}
        for archive_file in archive_files:
            archive_hashes.update({
                archive_file: self.generate_hash(archive_file, detail_manager)
            })
        return archive_hashes

    @staticmethod
    def generate_hash(archive_file: str, detail_manager) -> str:
        """Given a file, generate a hash and return it
        :arg, archive_file, the path to a file
        :return, a hash string
        """
        hasher = detail_manager.hasher_algo()
        with open(archive_file, 'rb') as af:
            while True:
                data = af.read(detail_manager.BUF_SIZE)
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()
