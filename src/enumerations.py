# Enumerated labels for constants

# imports, python
import os

# Local variables
user = os.environ.get('USER')


class ArchiveType:
    archive = 'archive'
    source = 'source'


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


class Disk:
    class Dev:
        # Define mount point requirements
        mount = {
        }
        # Define Filesystems to ignore and skip
        skip = [
            'tmpfs'
        ]


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
