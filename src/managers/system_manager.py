# imports, python
from subprocess import run

# imports, project
from src.enumerations import Command
from src.enumerations import Disk


class SystemManager:
    def __init__(
            self,
            debug=False
    ):
        self._debug = debug
        self._network_connected = None

        # Perform checks
        self.disk_check()
        self.network_check()

    def run(self):
        self.disk_check()
        self.network_check()

    @staticmethod
    def disk_check():
        if not disks_ready():
            raise OSError(f'Disks in unexpected state')

    @staticmethod
    def network_check():
        if not network_ready():
            raise OSError(f'Network in unexpected state')


def disks_ready():
    """Ensure that disks are mounted at expected mount points"""
    disk_state = read_disk_state(cmd=Command.Disk.df)
    for dev, mount in Disk.Dev.mount.items():
        if dev not in disk_state:
            print(f'Expected disk missing : {dev}')
            return False

        mounted_on = disk_state[dev]['Mounted on']
        if mount != mounted_on:
            print(f'Unexpected mount point for {mount} : {mounted_on}')
            return False
    return True


def network_ready():
    pass


def read_disk_state(cmd=Command.Disk.df) -> dict:
    """Get information about the current state of disks"""
    return _parse_raw_disk_state(_read_raw_disk_state(cmd))


def _read_raw_disk_state(cmd) -> str:
    if cmd == Command.Disk.df:
        return str(run(['df'], capture_output=True).stdout.decode())


def _parse_raw_disk_state(raw_disk_state, cmd=Command.Disk.df):
    raw_disk_state_lines = raw_disk_state.split('\n')
    _verify_header(raw_disk_state_lines, cmd)
    disk_state = {}
    for raw_disk_state_line in raw_disk_state_lines[1:]:
        if cmd == Command.Disk.df:
            # Split and remove blank entries
            disk_state_line = [val for val in raw_disk_state_line.split(' ') if val]

            if not disk_state_line:
                continue

            if disk_state_line[0] in Disk.Dev.skip:
                continue  # Skip some Filesystems

            disk_state.update({
                disk_state_line[0]: {
                    '1K-blocks': disk_state_line[1],
                    'Used': disk_state_line[2],
                    'Available': disk_state_line[3],
                    'Use%': disk_state_line[4],
                    'Mounted on': disk_state_line[5],
                }
            })
    return disk_state


def _verify_header(raw_disk_state_lines: list, cmd: str):
    if cmd == Command.Disk.df:
        header_cols = Command.Output.df['Header Columns']
        header = raw_disk_state_lines[0]
        valid_df_header = _validate_df_header(header, header_cols)
        if not valid_df_header:
            raise OSError(f'Invalid {cmd} header found : {header}')


def _validate_df_header(header: str, header_cols: list) -> bool:
    header_cols_state = [0 for _ in header_cols]
    for idx, header_col in enumerate(header_cols):
        if header_col in header:
            header_cols_state[idx] = header_col
    return all(header_cols_state)
