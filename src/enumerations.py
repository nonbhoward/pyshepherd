# Enumerated labels for constants

# imports, python
import os

# Local variables
user = os.environ.get('USER')


class Class:
    COLLECTION_MANAGER = 'COLLECTION_MANAGER'
    CONFIG_MANAGER = 'CONFIG_MANAGER'
    FILE_MANAGER = 'FILE_MANAGER'
    METADATA_MANAGER = 'METADATA_MANAGER'
    STAGE_MANAGER = 'STAGE_MANAGER'
    SYSTEM_MANAGER = 'SYSTEM_MANAGER'


class CollectionType:
    ARCHIVE = 'ARCHIVE'
    SOURCE = 'SOURCE'


class Command:
    class Disk:
        df = 'df'

    class SoftLink:
        root = ['ln', '-s']

    class Network:
        ifconfig = 'ifconfig'

    class Output:
        df = {
            'Header Columns': [
                'Filesystem',
                '1K-blocks',
                'Used',
                'Available',
                'Use%',
                'Mounted on'
            ]
        }


class ConfigKey:
    # Parent Keys, Main
    DEBUG = 'DEBUG'

    # Parent Keys, Archive Manager
    BUF_SIZE = 'BUF_SIZE'
    COLLECTION = 'COLLECTION'
    CREATE_DEFAULT_ARCHIVE_PATHS = 'CREATE_DEFAULT_ARCHIVE_PATHS'
    CREATE_DEFAULT_SOURCE_PATHS = 'CREATE_DEFAULT_SOURCE_PATHS'
    DEFAULT_COLLECTION = 'DEFAULT_COLLECTION'
    FILE_NAME_LEN_MAX_VALUE = 'FILE_NAME_LEN_MAX_VALUE'
    FILE_SIZE_TO_HASH_MAX = 'FILE_SIZE_TO_HASH_MAX'
    FILE_SIZE_TO_HASH_MIN = 'FILE_SIZE_TO_HASH_MIN'
    HASH_ALGO = 'HASH_ALGO'
    LARGE_FILE_THRESHOLD = 'LARGE_FILE_THRESHOLD'
    SKIP_SOFT_LINKS = 'SKIP_SOFT_LINKS'
    UNMERGE_ARCHIVE = 'UNMERGE_ARCHIVE'

    # Child Keys, Archive Manager
    ARCHIVE_PATH = 'ARCHIVE_PATH'
    DEFAULT_PARENT_FOLDER = 'DEFAULT_PARENT_FOLDER'
    DEFAULT_ARCHIVE_FOLDER = 'DEFAULT_ARCHIVE_FOLDER'
    DEFAULT_GRAVEYARD_FOLDER = 'DEFAULT_GRAVEYARD_FOLDER'
    DEFAULT_SOURCE_FOLDER = 'DEFAULT_SOURCE_FOLDER'
    DEFAULT_STAGE_FOLDER = 'DEFAULT_STAGE_FOLDER'
    DEFAULT_UNSTAGE_FOLDER = 'DEFAULT_UNSTAGE_FOLDER'
    GRAVEYARD_PATH = 'GRAVEYARD_PATH'
    SOURCE_PATH = 'SOURCE_PATH'
    STAGE_PATH = 'STAGE_PATH'
    UNSTAGE_PATH = 'UNSTAGE_PATH'

    # Parent Keys, Logging
    DEFAULT_LEVEL = 'DEBUG'

    # Parent Keys, Progress
    PROGRESS_BAR_INCREMENT = 'PROGRESS_BAR_INCREMENT'
    TERMINAL_DIALOG_PADDING = 'TERMINAL_DIALOG_PADDING'

    # Parent Keys, System Manager
    NETWORK_CHECK_DELAY = 'NETWORK_CHECK_DELAY'
    NETWORK_CHECK_COUNT = 'NETWORK_CHECK_COUNT'
    REQUIRE_NETWORK = 'REQUIRE_NETWORK'


class Disk:
    class Dev:
        # Define mount point requirements
        mount = {
        }
        # Define Filesystems to ignore and skip
        skip = [
            'tmpfs'
        ]


class FileAttribute:
    HASH = 'HASH'
    ST_SIZE = 'ST_SIZE'


class Hash:
    MD5 = 'MD5'
    SHA1 = 'SHA1'


class MetadataKey:
    COLLECTION = 'COLLECTION'
    COLLECTION_NAME = 'COLLECTION_NAME'
    COLLECTION_PATHS = 'COLLECTION_PATHS'
    DUPLICATES = 'DUPLICATES'
    FILES = 'FILES'
    HASH = 'HASH'
    NAME = 'NAME'
    ORIGINAL = 'ORIGINAL'
    PARENT = 'PARENT'
    SOFT_LINK_COMMAND = 'SOFT_LINK_COMMAND'
    SIZE = 'SIZE'
    TYPE = 'TYPE'
    UNSTAGE = 'UNSTAGE'
    UNSTAGE_DST = 'UNSTAGE_DST'
    UNSTAGE_ROOT = 'UNSTAGE_ROOT'


class Network:
    # Define network interface requirements
    # TODO this shouldn't be hardcoded
    interface = {
        'wlp0s20f3': {}
    }

    class Interface:
        # Define interfaces to ignore and skip
        skip = [
            'lo:'
        ]


class Progress:
    DATA_READ_SUM = 'DATA_READ_SUM'
    DATA_SIZE = 'DATA_SIZE'
    PERCENTAGE_LAST_UPDATE = 'PERCENTAGE_LAST_UPDATE'
    PERCENTAGE_NOW = 'PERCENTAGE_NOW'
    UPDATE_INCREMENT = 'UPDATE_INCREMENT'
