# Perform checks and fixes related to the operating system

# imports, python
from subprocess import run
from time import sleep

# imports, project
from src.enumerations import Class
from src.enumerations import Command
from src.enumerations import Disk
from src.enumerations import Network


class SystemManager:

    def __init__(self, managers):
        """Initialize the system manager

        :param managers: collection of manager classes
        """
        print(f'Init {self.__class__.__name__}')
        self.conf = managers[Class.CONFIG_MANAGER]
        self._debug = self.conf.debug
        self._network_connected = None

    def run(self):
        """Primary actions of the system manager"""
        print(f'Running {self.__class__.__name__}')

        self.disk_check()

        if self.conf.require_network:
            self.network_check()

    @staticmethod
    def disk_check():
        """Check the disks from the command line"""
        print(f'disk_check')
        if not disks_ready():
            raise OSError(f'Disks in unexpected state')

    def network_check(self):
        """Check the network from the command line"""
        print(f'network_check')
        if not network_ready(self.conf):
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


def network_ready(detail_manager):
    """Ensure that network is available and active"""
    network_snapshots = []
    for _ in range(detail_manager.network_check_count):
        network_snapshots.append(read_network_state(cmd=Command.Network.ifconfig))
        sleep(detail_manager.network_check_delay)
        if not network_snapshots[0]:
            return False  # No interfaces found, is Wi-Fi disabled?
    try:
        _validate_network_snapshots(network_snapshots)
    except OSError as exc:
        print(exc)
        return False
    return True


def read_disk_state(cmd=Command.Disk.df) -> dict:
    """Get information about the current state of disks"""
    return _parse_raw_disk_state(_read_raw_disk_state(cmd))


def read_network_state(cmd=Command.Network.ifconfig) -> dict:
    """Get information about the current state the network"""
    return _parse_raw_network_state(_read_raw_network_state(cmd))


def _read_raw_disk_state(cmd: list) -> str:
    """Read and return the raw disk information

    :param cmd: the disk information command
    :return: the raw disk information from the command line
    """
    if cmd == Command.Disk.df:
        return str(run(['df'], capture_output=True).stdout.decode())


def _read_raw_network_state(cmd: str) -> str:
    """Read and return the raw network information

    :param cmd: the network information command
    :return: the raw network information from the command line
    """
    if cmd == Command.Network.ifconfig:
        return str(run(['ifconfig'], capture_output=True).stdout.decode())


def _parse_raw_disk_state(raw_disk_state: str,
                          cmd: str = Command.Disk.df) -> dict:
    """Parse the raw disk state into a python dictionary

    :param raw_disk_state: the raw disk state from the command line
    :param cmd: the command used to generate the raw disk state information
    :return: a dictionary containing the parsed disk state
    """
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


def _parse_raw_network_state(raw_network_state: str,
                             cmd: str = Command.Network.ifconfig) -> dict:
    """Parse the raw network state into a python dictionary

    :param raw_network_state: the raw network state from the command line
    :param cmd: the command used to generate the raw network state information
    :return: a dictionary containing the parsed network state
    """
    raw_network_state_lines = raw_network_state.split('\n')
    _verify_header(raw_network_state_lines, cmd)
    network_state = {}
    # This flag is necessary because when an interface is skipped, the lines
    #   following will attempt to be parsed. This prevents that and instead
    #   directs the loop to search for the next line containing 'flags'. That
    #   line will be the interface, and then the flag is deactivated.
    interface_search_active = True
    for raw_network_state_line in raw_network_state_lines:
        if cmd == Command.Network.ifconfig:
            # Split and remove blank entries
            nsl = network_state_line = [val for val in raw_network_state_line.split(' ') if val]

            if not network_state_line:
                continue

            if 'flags' in raw_network_state_line:
                interface_search_active = False
                interface = network_state_line[0]

            if interface_search_active:
                continue  # These lines are part of a skipped interface

            if network_state_line[0] in Network.Interface.skip:
                interface_search_active = True
                continue  # Skip some interfaces

            # An interface has been found, read and populate until the next
            if network_state_line[0] == interface:
                # Initialize the new entry
                network_state.update({
                    interface: {
                        'flags': network_state_line[1],
                        'maximum_transmission_unit': nsl[2] + ' ' + nsl[3]
                    }
                })
            elif nsl[0] == 'inet':
                network_state[interface].update({
                    nsl[0] + ' ' + nsl[1]: nsl[2] + ' ' + nsl[3]
                })
            elif nsl[1] == 'packets':
                network_state[interface].update({
                    nsl[0] + ' ' + nsl[1]: {
                        nsl[1]: nsl[2],
                        nsl[3]: nsl[4],
                        'xfer': nsl[5] + nsl[6]
                    }
                })
            elif nsl[1] == 'errors':
                network_state[interface].update({
                    nsl[0] + ' ' + nsl[1]: {
                        nsl[1]: nsl[2],
                        nsl[3]: nsl[4],
                        nsl[5]: nsl[6],
                        nsl[7]: nsl[8]
                    }
                })

    return network_state


def _validate_network_snapshots(network_snapshots: dict) -> None:
    """Read the network snapshots to verify network activity is ongoing

    :param network_snapshots: time-spaced snapshots of the network interfaces
    """
    byte_rx_snapshots = []
    byte_tx_snapshots = []
    for idx, network_snapshot in enumerate(network_snapshots):
        for interface, details in network_snapshot.items():
            byte_rx_snapshots.append(int(details['RX packets']['bytes']))
            byte_tx_snapshots.append(int(details['TX packets']['bytes']))
    byte_rx_delta = byte_rx_snapshots[-1] - byte_rx_snapshots[0]
    byte_tx_delta = byte_tx_snapshots[-1] - byte_tx_snapshots[0]
    if not byte_rx_delta or byte_tx_delta:
        raise OSError('No network activity detected')


def _verify_header(raw_disk_state_lines: list, cmd: str) -> None:
    """Validate the raw disk state header is in expected format

    :param raw_disk_state_lines: a list of raw disk state lines
    :param cmd: the command used to generate the raw disk state lines
    """
    if cmd == Command.Disk.df:
        header_cols = Command.Output.df['Header Columns']
        header = raw_disk_state_lines[0]
        valid_df_header = _validate_df_header(header, header_cols)
        if not valid_df_header:
            raise OSError(f'Invalid {cmd} header found : {header}')


def _validate_df_header(header: str, header_cols: list) -> bool:
    """Validate the raw disk state header is in expected format

    :param header: the unparsed disk header
    :param header_cols: the disk header columns
    :return: bool indicating all expected headers found in header string
    """
    header_cols_state = [0 for _ in header_cols]
    for idx, header_col in enumerate(header_cols):
        if header_col in header:
            header_cols_state[idx] = header_col
    return all(header_cols_state)
