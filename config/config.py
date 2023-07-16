from os import environ

# GLOBAL VALUES BELOW
DEBUG = False
# GLOBAL VALUES ABOVE

# DUPLICATE MANAGER VALUES BELOW

# Dict : duplicate_search_targets : The locations
#   that will be searched in an attempt to identify
#   duplicated files.
# Key : 'enabled'. Allows discrete toggling of
#   disable/enable per path.
# Key : 'path_to_check'. The path from which to
#   read all files.
# Key : 'path_to_result'. The location to record
#   the result.
username = environ.get("USERNAME")
duplicate_search_targets = {
}

# Float : duplicate_size_lookaround : When
#   searching for duplicates, it seems that the
#   most obvious place to start searching is
#   similarly sized files. This value sets a threshold
#   for how far the algorithm will "look around".
#   For example, a value of 0.05 indicates that the
#   algorithm will search files that are of size
#   larger than (file_size - file_size * 0.05) and
#   smaller than (file_size + file_size * 0.05).
duplicate_size_lookaround = 0.05

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
require_network = True
# SYSTEM MANAGER VALUES ABOVE
