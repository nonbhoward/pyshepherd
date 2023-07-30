# The python entry-point

# imports, project
from config.config import config
from src.managers.collection_manager import CollectionManager
from src.managers.config_manager import ConfigManager
from src.managers.file_manager import FileManager
from src.managers.metadata_manager import MetadataManager
from src.managers.stage_manager import StageManager
from src.managers.system_manager import SystemManager
from src.shepherd.shepherd import Shepherd

shepherd = Shepherd(
    config=config,
    collection_manager=CollectionManager,
    config_manager=ConfigManager,
    file_manager=FileManager,
    metadata_manager=MetadataManager,
    stage_manager=StageManager,
    system_manager=SystemManager,
)
shepherd.run()
