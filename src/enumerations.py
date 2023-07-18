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
    # Parent Keys
    DEBUG = 'DEBUG'
    BUF_SIZE = 'BUF_SIZE'
    ARCHIVES = 'ARCHIVES'
    FILE_NAME_LEN_MAX_VALUE = 'FILE_NAME_LEN_MAX_VALUE'
    HASH_ALGO = 'HASH_ALGO'
    LARGE_FILE_THRESHOLD = 'LARGE_FILE_THRESHOLD'
    SORT_DUPLICATE_HIERARCHY = 'SORT_DUPLICATE_HIERARCHY'
    NETWORK_CHECK_DELAY = 'NETWORK_CHECK_DELAY'
    NETWORK_CHECK_COUNT = 'NETWORK_CHECK_COUNT'
    REQUIRE_NETWORK = 'REQUIRE_NETWORK'
    # Child Keys, Archives
    SOURCE_PATH = 'SOURCE_PATH'
    STAGE_PATH = 'STAGE_PATH'
    ARCHIVE_PATH = 'ARCHIVE_PATH'
    UNSTAGE_PATH = 'UNSTAGE_PATH'


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
