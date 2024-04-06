from pathlib import Path
import json
import os


def read_json_file(path: str | Path) -> dict:
    """Read json file"""
    assert os.path.exists(path), f"File {path} does not exists"
    with open(path, "r") as f:
        json_data = json.load(f)

    return json_data


def write_json_file(data: dict, path: str | Path) -> None:
    """Write data to a JSON file."""
    with open(path, "w") as f:
        json.dump(data, f)
