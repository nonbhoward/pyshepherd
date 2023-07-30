# Copy and move files

# imports python
from os import environ
from os import mkdir
from os.path import exists
from pathlib import Path
from shutil import move
from subprocess import run

# imports, project
from src.enumerations import ConfigKey


class FileManager:

    def __init__(self, managers):
        print(f'Init {self.__class__.__name__}')
        self.conf = managers['config_manager']

    @staticmethod
    def check_exists(path):
        return True if exists(path) else False

    def create_default_archive_paths(self, archive_name):
        # Build the root path
        home = environ.get("HOME")
        default_parent_folder = self.conf.default_parent_folder
        default_folder_root = str(Path(home, default_parent_folder))

        # Build the children paths
        default_archive_folder = self.conf.default_archive_folder
        default_archive_path = str(Path(default_folder_root,
                                        default_archive_folder))
        default_unstage_folder = self.conf.default_unstage_folder
        default_unstage_path = str(Path(default_folder_root,
                                        default_unstage_folder))

        # Create the children
        self.create_default_path(default_archive_path)
        self.create_default_path(default_unstage_path)

        self.conf.update_archive_paths({
            ConfigKey.ARCHIVE_PATH_LABEL: default_archive_path,
            ConfigKey.UNSTAGE_PATH: default_unstage_path
        })

    def create_default_source_paths(self, archive_name):
        # Build the root path
        home = environ.get("HOME")
        default_parent_folder = self.conf.default_parent_folder
        default_folder_root = str(Path(home, default_parent_folder))

        default_graveyard_folder = self.conf.default_graveyard_folder
        default_graveyard_path = str(Path(default_folder_root,
                                          default_graveyard_folder))
        default_source_folder = self.conf.default_source_folder
        default_source_path = str(Path(default_folder_root,
                                       default_source_folder))
        default_stage_folder = self.conf.default_stage_folder
        default_stage_path = str(Path(default_folder_root,
                                      default_stage_folder))

        # Create the root
        self.create_default_path(default_folder_root)
        self.create_default_path(default_stage_path)

        # Create the children
        self.create_default_path(default_graveyard_path)
        self.create_default_path(default_source_path)

        self.conf.update_source_paths({
            ConfigKey.GRAVEYARD_PATH: default_graveyard_path,
            ConfigKey.STAGE_PATH: default_stage_path,
            ConfigKey.SOURCE_PATH: default_source_path,
        })

    @staticmethod
    def create_default_path(default_path):
        # TODO fix bug that doesn't create parent folders
        #   also, this should call "create required folders" and pass
        #   arguments to that
        if exists(default_path):
            print(f'Default folder {default_path} already exists, '
                  f'continuing..')
        else:
            try:
                mkdir(default_path)
            except Exception as exc:
                print(f'Error creating default folder root : '
                      f'{default_path}, {exc}')

    @staticmethod
    def create_required_folders(duplicate_parent_folder: str) -> None:
        """Recursively create all parent folders up to and including the parent
            directory being requested

        :param duplicate_parent_folder: metadata used to create the folders
        """
        # Convenience
        udes = unstage_destination_elements = duplicate_parent_folder.split('/')

        progressive_path = ''
        for ude in udes:
            progressive_path += ude + '/' if ude else '/'
            if not exists(progressive_path):
                try:
                    mkdir(progressive_path)
                except OSError as exc:
                    print(f'Failed to make path : {progressive_path}, {exc}')
                    raise exc

    @staticmethod
    def create_soft_link(soft_link_command: list) -> None:
        """Create a soft link, aborts if soft link already exists

        :param soft_link_command: the command to create the soft link
        """
        try:
            soft_link_target = soft_link_command[3]
            if exists(soft_link_target):
                return  # Soft link to original already exists
            run(soft_link_command)
        except OSError as exc:
            print(f'Failed to create soft link : {soft_link_command}, {exc}')
            raise exc

    def move_duplicate_file(self, duplicate_details: dict) -> None:
        """Move a file

        :param duplicate_details: file destination details
        """
        duplicate_file = duplicate_details['name']
        duplicate_file_dst = duplicate_details['unstage_file_destination']
        self.move_file(
            src=duplicate_file,
            dst=duplicate_file_dst
        )

    def move_file(self, src: str, dst: str) -> None:
        """Validate the paths and move the file

        :param src: the source file
        :param dst: the destination file
        """
        self.validate_paths(src, dst)
        try:
            move(src=src, dst=dst)
        except OSError as exc:
            print(f'Failed to move file : {src} > {dst}')
            raise exc

    @staticmethod
    def validate_paths(src: str, dst: str) -> None:
        """Validate paths exist

        :param src: a path to validate
        :param dst: a path to validate
        """
        if not exists(src):
            raise OSError(f'Src not exist : {src}')
        dst = '/'.join(dst.split('/')[:-1])
        if not exists(dst):
            raise OSError(f'Dst not exist : {dst}')
