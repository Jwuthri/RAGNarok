import pytest

from src.utils.dict_utils import flatten_dict, replace_none_values


@pytest.mark.parametrize(
    "input_dict, expected_output",
    [
        ({"a": 1, "b": {"c": 2, "d": {"e": 3}}}, {"a": 1, "b_c": 2, "b_d_e": 3}),
        ({"a": {"b": {"c": {"d": {"e": {"f": "g"}}}}}}, {"a_b_c_d_e_f": "g"}),
        ({}, {}),
        ({"a": {"b": 2}, "c": [1, 2, 3]}, {"a_b": 2, "c": [1, 2, 3]}),
        ({"a": []}, {"a": []}),
    ],
)
def test_flatten_dict(input_dict, expected_output):
    assert flatten_dict(input_dict) == expected_output


@pytest.mark.parametrize(
    "input_dict, default_value, value_to_replace, expected_output",
    [
        ({"a": None, "b": 2, "c": None}, "default", None, {"a": "default", "b": 2, "c": "default"}),
        ({"a": "", "b": 2, "c": ""}, "none", "", {"a": "none", "b": 2, "c": "none"}),
        ({"a": None, "b": "None", "c": None}, 0, None, {"a": 0, "b": "None", "c": 0}),
        ({}, "default", None, {}),
        ({"a": 1, "b": 2, "c": 3}, "replaced", 2, {"a": 1, "b": "replaced", "c": 3}),
    ],
)
def test_replace_none_values(input_dict, default_value, value_to_replace, expected_output):
    assert replace_none_values(input_dict, default_value, value_to_replace) == expected_output
