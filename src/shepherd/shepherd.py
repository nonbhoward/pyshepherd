class Shepherd:
    def __init__(
            self,
            duplicate_manager,
            system_manager,
            debug=False,
    ):
        self._debug = debug
        self._duplicate_manager = duplicate_manager(debug=debug)
        self._system_manager = system_manager(debug=debug)

    def run(self):
        self._system_manager.run()
        self._duplicate_manager.run()
