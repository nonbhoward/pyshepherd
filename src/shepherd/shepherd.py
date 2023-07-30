# Class meta management

# imports, project
from src.enumerations import Class


class Shepherd:
    def __init__(
            self,
            config,
            managers
    ):
        print(f'Init {self.__class__.__name__}')
        config_manager = self.conf = managers[Class.CONFIG_MANAGER](
            config=config,
        )
        managers[Class.CONFIG_MANAGER] = config_manager
        self._debug = config_manager.debug
        self.system_manager = managers[Class.SYSTEM_MANAGER](managers)
        self.collection_manager = managers[Class.COLLECTION_MANAGER](managers)

    def run(self):
        print(f'Running {self.__class__.__name__}')
        self.system_manager.run()
        self.collection_manager.run()
