# The parent class of all classes

class Shepherd:
    def __init__(
            self,
            config,
            collection_manager,
            detail_manager,
            file_manager,
            stage_manager,
            system_manager,
    ):
        print(f'Init {self.__class__.__name__}')
        detail_manager = self.dm = detail_manager(
            config=config,
        )
        self._debug = detail_manager.debug
        self._system_manager = system_manager(detail_manager)
        self._archive_manager = collection_manager(
            detail_manager,
            file_manager,
            stage_manager
        )

    def run(self):
        print(f'Running {self.__class__.__name__}')
        self._system_manager.run()
        self._archive_manager.run()
