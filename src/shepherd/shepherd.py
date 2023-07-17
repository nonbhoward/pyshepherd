class Shepherd:
    def __init__(
            self,
            config,
            archive_manager,
            detail_manager,
            system_manager,
    ):
        detail_manager = self.dm = detail_manager(config=config)
        self._debug = detail_manager.debug
        self._archive_manager = archive_manager(detail_manager)
        self._system_manager = system_manager(detail_manager)

    def run(self):
        self._system_manager.run()
        self._archive_manager.run()
