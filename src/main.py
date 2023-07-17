# The python entry-point

# imports, project
from config.config import DEBUG
from src.managers.archive_manager import ArchiveManager
from src.managers.system_manager import SystemManager
from src.shepherd.shepherd import Shepherd

shepherd = Shepherd(
    debug=DEBUG,
    duplicate_manager=ArchiveManager,
    system_manager=SystemManager
)
shepherd.run()
