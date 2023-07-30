# The python entry-point

# imports, project
from config.config import config
from src.enumerations import Class
from src.managers.collection_manager import CollectionManager
from src.managers.config_manager import ConfigManager
from src.managers.file_manager import FileManager
from src.managers.metadata_manager import MetadataManager
from src.managers.stage_manager import StageManager
from src.managers.system_manager import SystemManager
from src.shepherd.shepherd import Shepherd

managers = {
    Class.COLLECTION_MANAGER: CollectionManager,
    Class.CONFIG_MANAGER: ConfigManager,
    Class.FILE_MANAGER: FileManager,
    Class.METADATA_MANAGER: MetadataManager,
    Class.STAGE_MANAGER: StageManager,
    Class.SYSTEM_MANAGER: SystemManager
}

shepherd = Shepherd(
    config=config,
    managers=managers
)
shepherd.run()
