# The parent class of all classes

class Shepherd:
    def __init__(
            self,
            config,
            collection_manager,
            config_manager,
            file_manager,
            metadata_manager,
            stage_manager,
            system_manager,
    ):
        print(f'Init {self.__class__.__name__}')
        config_manager = self.cm = config_manager(
            config=config,
        )
        self._debug = config_manager.debug
        self.system_manager = system_manager(config_manager)
        self.collection_manager = collection_manager(
            config_manager,
            file_manager,
            metadata_manager,
            stage_manager
        )

    def run(self):
        print(f'Running {self.__class__.__name__}')
        self.system_manager.run()
        self.collection_manager.run()
