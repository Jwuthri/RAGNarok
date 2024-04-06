from typing import Any


def flatten_dict(d: dict, parent_key: str = "", sep: str = "_") -> dict:
    """
    Flatten a nested dictionary.

    Args:
        d (dict): The input dictionary.
        parent_key (str): The key representing the parent dictionary.
        sep (str): The separator to use when combining keys.

    Returns:
        dict: The flattened dictionary.
    """
    items: list = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def replace_none_values(d: dict, default_value: str = "", value_to_replace: Any = None) -> dict:
    """
    Replaces values in a dictionary that match a specified value with a default value.

    Parameters:
    - d (dict): The dictionary whose values are to be checked and possibly replaced.
    - default_value (str, optional): The value to replace the matched values with. Defaults to an empty string.
    - value_to_replace (Any, optional): The value that needs to be replaced. Defaults to None.

    Returns:
    - dict: A new dictionary with the specified values replaced by the default value.
    """
    return {k: default_value if v == value_to_replace else v for k, v in d.items()}
