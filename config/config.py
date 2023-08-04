# Configuration, read by the detail manager

# imports, project
from src.enumerations import ConfigKey

from os import environ
home = environ.get("HOME")

config = {

    # MAIN VALUES BELOW
    # This is not used, but could be if a debug mode was needed
    ConfigKey.DEBUG: False,
    # MAIN VALUES ABOVE

    # COLLECTION MANAGER VALUES BELOW
    # Collections are the collected directories that will be managed by the
    #   collection manager class. Each collection has a label, and four
    #   paths. The use of those paths is described in the collection
    #   manager class documentation
    ConfigKey.COLLECTION: {
        ConfigKey.DEFAULT_COLLECTION: {
            ConfigKey.ARCHIVE_PATH:     f'',
            ConfigKey.GRAVEYARD_PATH:   f'',
            ConfigKey.SOURCE_PATH:      f'',
            ConfigKey.STAGE_PATH:       f'',
            ConfigKey.UNSTAGE_PATH:     f''
        },
    },
    # BUF_SIZE is to prevent hashing of large files from consuming
    #   system resources by hashing the file in BUF_SIZE chunks
    ConfigKey.BUF_SIZE: 65536,
    # Toggle if you want a default path structure to be made for archive
    #   paths which includes the archive and unstage path
    ConfigKey.CREATE_DEFAULT_ARCHIVE_PATHS: True,
    # Toggle if you want a default path structure to be made for source
    #   paths which includes the graveyard, source, and stage path
    ConfigKey.CREATE_DEFAULT_SOURCE_PATHS: True,
    # Value chosen to be beyond reasonable file path lengths
    #   It is used for the file length sorting algorithm
    ConfigKey.FILE_NAME_LEN_MAX_VALUE: 9999,
    # Maximum and minimum file sizes to hash, without a hash, a file will not
    #   be acted on.
    # For minimum size, 0 sets no size limit
    # For maximum size, 0 sets no size limit
    ConfigKey.FILE_SIZE_TO_HASH_MIN: 0,
    ConfigKey.FILE_SIZE_TO_HASH_MAX: 0,
    # Available values : MD5, SHA1
    #   Determines which hashing algorithm to use
    ConfigKey.HASH_ALGO: 'MD5',
    # Flag to toggle sorting files to determine original
    # This feature will compare the original and duplicate files, sorting them
    #   alphabetically, and declares the "alphabetically first" file as the
    #   original. This is obviously not necessary, so it can be skipped.
    # The threshold over which a file will be considered large,
    #   affects the verboseness of some console output, for example, a
    #   loading bar will be displayed when hashing files larger than this
    ConfigKey.LARGE_FILE_THRESHOLD: 100000000,
    # The absolute path to write report data
    ConfigKey.PATH_TO_WRITE_REPORT: f'{home}/pyshepherd.report',
    # Determines whether soft links will be considered when searching for
    #   duplicate files. Disabled by default to prevent moving soft links
    ConfigKey.SKIP_SOFT_LINKS: True,
    # Determines whether the source should be parsed for staging (and then
    #   staged)
    ConfigKey.STAGE_SOURCE: False,
    # Determines whether the archive should be parsed for unstaging (and then
    #   unstaged)
    ConfigKey.UNSTAGE_ARCHIVE: True,

    # FILE MANAGER VALUES BELOW
    ConfigKey.DEFAULT_PARENT_FOLDER: '_PYSHEPHERD',
    ConfigKey.DEFAULT_ARCHIVE_FOLDER: '_ARCHIVE',
    ConfigKey.DEFAULT_GRAVEYARD_FOLDER: '_GRAVEYARD',
    ConfigKey.DEFAULT_SOURCE_FOLDER: '_SOURCE',
    ConfigKey.DEFAULT_STAGE_FOLDER: '_STAGE',
    ConfigKey.DEFAULT_UNSTAGE_FOLDER: '_UNSTAGE',
    # FILE MANAGER VALUES ABOVE

    # LOGGER VALUES BELOW
    # LOGGER VALUES ABOVE

    # PROGRESS VALUES BELOW
    # How often to update the progress bar, a value of 1 would mean to
    #   update the loading bar every time it has moved 1%
    ConfigKey.PROGRESS_BAR_INCREMENT: 1,
    # Padding value to make the loading bar fit the terminal window
    ConfigKey.TERMINAL_DIALOG_PADDING: 7,
    # PROGRESS VALUES ABOVE

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
