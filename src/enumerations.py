# Enumerated labels for constants

# imports, python
import os

# Local variables
user = os.environ.get('USER')


class Command:
    class Disk:
        df = 'df'

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
