import logging

logger = logging.getLogger(__name__)


class LiveQuestionExtraction:
    def __init__(self) -> None:
        ...

    def predict(self, bot_id: str):
        ...

    def fetch_history_messages(self, bot_id: str):
        ...
