from src.schemas.chat_message import ChatMessage

SYSTEM_MSG = """
You are an AI multi-class classifier.
Your job is to classify the given Input, using the following set of Classes.

## Instructions:
    * You must reply with a simple token representing the classe.
## Classes: {CLASSES}
## Output format: str
## Examples: {EXAMPLES}
"""
USER_MSG = "## Input: {INPUT}\n## Output:"
