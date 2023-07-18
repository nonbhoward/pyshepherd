# Enumerated labels for constants

# imports, python
import os

# Local variables
user = os.environ.get('USER')


class ArchiveType:
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
    ARCHIVES = 'ARCHIVES'
    FILE_NAME_LEN_MAX_VALUE = 'FILE_NAME_LEN_MAX_VALUE'
    HASH_ALGO = 'HASH_ALGO'
    LARGE_FILE_THRESHOLD = 'LARGE_FILE_THRESHOLD'
    SKIP_SOFT_LINKS = 'SKIP_SOFT_LINKS'
    SORT_DUPLICATE_HIERARCHY = 'SORT_DUPLICATE_HIERARCHY'

    # Child Keys, Archive Manager
    ARCHIVE_PATH = 'ARCHIVE_PATH'
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


class MetadataKey:
    DUPLICATES = 'DUPLICATES'
    TYPE = 'TYPE'
    UNSTAGE = 'UNSTAGE'


class Network:
    # Define network interface requirements
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
