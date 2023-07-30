# Class meta management

class Shepherd:
    def __init__(
            self,
            config,
            managers
    ):
        print(f'Init {self.__class__.__name__}')
        config_manager = self.conf = managers['config_manager'](
            config=config,
        )
        managers['config_manager'] = config_manager
        self._debug = config_manager.debug
        self.system_manager = managers['system_manager'](managers)
        self.collection_manager = managers['collection_manager'](managers)

    def run(self):
        print(f'Running {self.__class__.__name__}')
        self.system_manager.run()
        self.collection_manager.run()
