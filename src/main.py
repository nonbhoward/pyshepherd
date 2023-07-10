# imports, python

# imports, project
from config.config import DEBUG
from src.managers.duplicate_manager import DuplicateManager
from src.managers.system_manager import SystemManager
from src.shepherd.shepherd import Shepherd

shepherd = Shepherd(
    debug=DEBUG,
    duplicate_manager=DuplicateManager,
    system_manager=SystemManager
)
shepherd.run()
