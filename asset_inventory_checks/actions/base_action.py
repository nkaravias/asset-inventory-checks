from abc import ABC, abstractmethod
from asset_inventory_checks.logger_config import setup_logger

class Action(ABC):
    def __init__(self):
        self.logger = setup_logger()

    @abstractmethod
    def execute(self):
        pass