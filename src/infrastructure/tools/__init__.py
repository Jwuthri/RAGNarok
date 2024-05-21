import json

from src.schemas.prompt import ToolCall


def run_tool(tool_call: ToolCall, allowed_tools: dict):
    if tool_call:
        tool = tool_call.function["name"]
        function_to_call = allowed_tools.get(tool)
        if function_to_call:
            return function_to_call(**json.loads(tool_call.function["arguments"]))

    return None
