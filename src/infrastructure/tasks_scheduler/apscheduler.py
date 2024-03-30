import logging

from src.infrastructure.tasks_scheduler.base import TasksScheduler

logger = logging.getLogger(__name__)


try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger
except ModuleNotFoundError as e:
    logger.error(e)
    logger.warning("Please run `pip install torch`")
    logger.warning("Please run `pip install sentence-transformers`")


class Apscheduler(TasksScheduler):
    def __init__(self, scheduler=BackgroundScheduler(), triggerer=IntervalTrigger) -> None:
        super().__init__(scheduler, triggerer)

    def start(self):
        self.scheduler.start()

        return self
