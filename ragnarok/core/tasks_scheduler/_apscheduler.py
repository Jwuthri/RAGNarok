import logging

from ragnarok.core.tasks_scheduler.base import TasksScheduler

logger = logging.getLogger(__name__)


class Apscheduler(TasksScheduler):
    def __init__(self, scheduler=None, triggerer=None) -> None:
        if scheduler is None or triggerer is None:
            try:
                from apscheduler.schedulers.background import BackgroundScheduler
                from apscheduler.triggers.interval import IntervalTrigger

                if scheduler is None:
                    scheduler = BackgroundScheduler()
                if triggerer is None:
                    triggerer = IntervalTrigger
            except ModuleNotFoundError as e:
                logger.warning("Please run `pip install apscheduler`")

    def start(self):
        self.scheduler.start()

        return self


if __name__ == "__main__":
    pass
