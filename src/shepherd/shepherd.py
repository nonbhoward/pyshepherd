class Shepherd:
    def __init__(
            self,
            archive_manager,
            system_manager,
            debug=False,
    ):
        self._debug = debug
        self._archive_manager = archive_manager(debug=debug)
        self._system_manager = system_manager(debug=debug)

    def run(self):
        self._system_manager.run()
        self._archive_manager.run()
