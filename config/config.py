import os
from os import environ
home = os.environ.get("HOME")

# MAIN VALUES BELOW
DEBUG = False
# MAIN VALUES ABOVE

# DUPLICATE MANAGER VALUES BELOW
# BUF_SIZE is to prevent hashing of large files from consuming
#   system resources by hashing the file in BUF_SIZE chunks
BUF_SIZE = 65536
archives = {
    'archive_a': {
        'source_path': '',
        'stage_path': '',
        'archive_path': '',
        'unstage_path': ''
    },
    'archive_b': {
        'source_path': '',
        'stage_path': '',
        'archive_path': '',
        'unstage_path': ''
    }
}
# Available values : md5, sha1
#   Determines which hashing algorithm to use
hash_algo = 'md5'
# DUPLICATE MANAGER VALUES ABOVE

# SYSTEM MANAGER VALUES BELOW
# Time to wait between checks of the network interfaces
#   This is used to ensure that they are active, so some
#   delay must be used to allow the ifconfig command to
#   update.
network_check_delay = 1
# Note that each time a network check count is added, each
#   check requires a wait time of network_check_delay. This
#   will create a total wait time of :
#       network_check_delay * network_check_count
# At the moment, there is no practical reason to change this value
#   since only the first and last snapshots are compared.
network_check_count = 2
# If enabled, requires internet connectivity
require_network = False
# SYSTEM MANAGER VALUES ABOVE
