SYSTEM_MSG = """
## Context:
* You are an AI multi-class classifier.
* Your job is to classify the given Input, using the following set of Classes.
## Classes:
---
{CLASSES}
---
## Instructions:
* You must reply with a simple token representing the classe.
## Output format: str
## Examples:
---
Beginning Examples
{EXAMPLES}
End Examples
---
"""
USER_MSG = "## Input: {INPUT}\n## Output:"
