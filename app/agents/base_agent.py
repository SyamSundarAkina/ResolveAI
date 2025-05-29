# app/agents/base_agent.py

from abc import ABC, abstractmethod
import logging

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)
        logging.basicConfig(level=logging.INFO)

    @abstractmethod
    def run(self, input_data: str) -> dict:
        """
        All agents should implement this method.
        It takes input_data (usually a user request) and returns a structured dict.
        """
        pass

    def log(self, message: str):
        self.logger.info(f"[{self.name}] {message}")
