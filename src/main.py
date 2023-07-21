# The python entry-point

# imports, project
from config.config import config
from src.managers.collection_manager import CollectionManager
from src.managers.detail_manager import DetailManager
from src.managers.file_manager import FileManager
from src.managers.stage_manager import StageManager
from src.managers.system_manager import SystemManager
from src.shepherd.shepherd import Shepherd

shepherd = Shepherd(
    config=config,
    collection_manager=CollectionManager,
    detail_manager=DetailManager,
    file_manager=FileManager,
    stage_manager=StageManager,
    system_manager=SystemManager,
)
shepherd.run()
