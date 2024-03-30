from abc import ABC, abstractmethod
from typing import Any, Callable


class TasksScheduler(ABC):
    def __init__(self, scheduler: Any, triggerer: Callable) -> None:
        self.scheduler = scheduler
        self.triggerer = triggerer

    @abstractmethod
    def start(self):
        ...
