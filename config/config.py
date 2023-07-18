# Configuration, read by the detail manager

# imports, project
from src.enumerations import ConfigKey

from os import environ
home = environ.get("HOME")

config = {

    # MAIN VALUES BELOW
    ConfigKey.DEBUG: False,
    # MAIN VALUES ABOVE

    # ARCHIVE MANAGER VALUES BELOW
    # BUF_SIZE is to prevent hashing of large files from consuming
    #   system resources by hashing the file in BUF_SIZE chunks
    ConfigKey.BUF_SIZE: 65536,
    # Archives is the collected archives that will be managed by the
    #   archive manager class. Each archive has a label, and four
    #   paths. The use of those paths is described in the archive
    #   manager class documentation
    ConfigKey.ARCHIVES: {
        'archive_a': {
            ConfigKey.SOURCE_PATH:  f'',
            ConfigKey.STAGE_PATH:   f'',
            ConfigKey.ARCHIVE_PATH: f'',
            ConfigKey.UNSTAGE_PATH: f''
        },
        'archive_b': {
            ConfigKey.SOURCE_PATH:  f'',
            ConfigKey.STAGE_PATH:   f'',
            ConfigKey.ARCHIVE_PATH: f'',
            ConfigKey.UNSTAGE_PATH: f''
        }
    },
    # Value chosen to be beyond reasonable file path lengths
    ConfigKey.FILE_NAME_LEN_MAX_VALUE: 9999,
    # Available values : md5, sha1
    #   Determines which hashing algorithm to use
    ConfigKey.HASH_ALGO: 'md5',
    # Flag to toggle sorting files to determine original
    # This feature will compare the original and duplicate files, sorting them
    #   alphabetically, and declares the "alphabetically first" file as the
    #   original. This is obviously not necessary, so it can be skipped.
    ConfigKey.SORT_DUPLICATE_HIERARCHY: True,
    # ARCHIVE MANAGER VALUES ABOVE

    # SYSTEM MANAGER VALUES BELOW
    # Time to wait between checks of the network interfaces
    #   This is used to ensure that they are active, so some
    #   delay must be used to allow the ifconfig command to
    #   update.
    ConfigKey.NETWORK_CHECK_DELAY: 1,
    # Note that each time a network check count is added, each
    #   check requires a wait time of network_check_delay. This
    #   will create a total wait time of :
    #       network_check_delay * network_check_count
    # At the moment, there is no practical reason to change this value
    #   since only the first and last snapshots are compared.
    ConfigKey.NETWORK_CHECK_COUNT: 2,
    # If enabled, requires internet connectivity
    ConfigKey.REQUIRE_NETWORK: False,
    # SYSTEM MANAGER VALUES ABOVE

}
