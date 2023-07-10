class SystemManager:
    def __init__(
            self,
            debug=False
    ):
        self._debug = debug
        self._disks_ready = None
        self._network_connected = None

        # Perform checks
        self.disk_check()
        self.network_check()

    def run(self):
        pass

    def disk_check(self):
        if self._debug:
            return  # Skip check
        # Poll the disk state
        if not self._disks_ready():
            self.disk_mount()

    def disk_mount(self):
        # Mount the disks
        pass
        # If not successful
        self._disks_ready = False

    def network_check(self):
        if self._debug:
            return  # Skip check
        # Poll the network connection
        if not self._network_connected:
            self.network_connect()

    def network_connect(self):
        # Connect to the network
        pass
        # If not successful
        self._network_connected = False
