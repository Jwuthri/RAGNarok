from src.core.tools.tools_generator import FunctionToOpenAITool


def test_generate_tool_json():
    def example_function(a: int, b: str = "default_value", c: bool = True) -> str:
        """
        This is a sample function.

        :param a: This is parameter 'a'.
        :param b: This is parameter 'b' with default value 'default_value'.
        :param c: This is parameter 'c' with default value True.
        :return: It returns a string.
        """
        return "result"

    tool = FunctionToOpenAITool(example_function)
    expected_json = {
        "type": "function",
        "function": {
            "name": "example_function",
            "description": "This is a sample function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "This is parameter 'a'."},
                    "b": {"type": "string", "description": "This is parameter 'b' with default value 'default_value'."},
                    "c": {"type": "boolean", "description": "This is parameter 'c' with default value True."},
                },
                "required": ["a"],
            },
        },
    }
    assert tool.generate_tool_json() == expected_json
