import tempfile
import json

from ragnarok.utils.file_utils import read_json_file, write_json_file


def test_read_and_write_json_file():
    """
    Test case for read_json_file and write_json_file functions.
    """
    test_data = {"key": "value"}
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(json.dumps(test_data))
        temp_file_path = temp_file.name

    loaded_data = read_json_file(temp_file_path)
    assert loaded_data == test_data
    modified_data = {"key": "new_value"}
    write_json_file(modified_data, temp_file_path)
    with open(temp_file_path, "r") as file:
        updated_data = json.load(file)
        assert updated_data == modified_data
