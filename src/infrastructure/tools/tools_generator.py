import inspect
import logging
from typing import Callable, get_type_hints

logger = logging.getLogger(__name__)


class FunctionToOpenAITool:
    def __init__(self, func: Callable):
        self.func = func
        self.func_signature = inspect.signature(func)
        try:
            import docstring_parser

            self.docstring = docstring_parser.parse(func.__doc__)
        except ModuleNotFoundError as e:
            logger.error("Please run `pip install docstring_parser`")

    def get_param_type(self, param):
        if param.annotation != inspect._empty:
            param_type = str(param.annotation)
            if "int" in param_type:
                return "number"
            elif "float" in param_type:
                return "number"
            elif "str" in param_type:
                return "string"
            elif "bool" in param_type:
                return "boolean"
            elif "list" in param_type:
                return "array"
            elif "dict" in param_type:
                return "object"
            elif "datetime.date" in param_type or "datetime.datetime" in param_type:
                return "date-time"

            return param_type
        else:
            return "string"

    def generate_tool_json(self) -> str:
        parameters = {"type": "object", "properties": {}, "required": []}
        type_hints = get_type_hints(self.func)
        for param in self.func_signature.parameters.values():
            param_description = next((p.description for p in self.docstring.params if p.arg_name == param.name), "")
            param_type = self.get_param_type(param)
            param_enum = type_hints[param.name].__args__ if hasattr(type_hints[param.name], "__args__") else []
            parameters["properties"][param.name] = {"type": param_type, "description": param_description}
            if param_enum:
                parameters["properties"][param.name]["enum"] = [e.__name__ for e in param_enum]
            if param.default is inspect.Parameter.empty:
                parameters["required"].append(param.name)
        tool_descriptor = {
            "type": "function",
            "function": {
                "name": self.func.__name__,
                "description": self.docstring.short_description,
                "parameters": parameters,
            },
        }

        return tool_descriptor
