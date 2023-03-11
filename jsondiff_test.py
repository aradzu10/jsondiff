import jsondiff
import pytest


def test_same_dict():
    dict_a = {
        "a": 1,
        "b": 1,
    }
    dict_a_mk, dict_b_mk, value_diff = jsondiff.dict_diff(dict_a, dict_a)
    assert len(dict_a_mk) == 0, "Same dict, shouldn't be any diff. {dict_a_mk}"
    assert len(dict_b_mk) == 0, "Same dict, shouldn't be any diff. {dict_b_mk}"
    assert len(value_diff) == 0, "Same dict, shouldn't be any diff. {value_diff}"


def test_same_keys_diff_value():
    dict_a = {
        "a": 1,
        "b": 1,
    }
    dict_b = {
        "a": 1,
        "b": 2,
    }
    dict_a_mk, dict_b_mk, value_diff = jsondiff.dict_diff(dict_a, dict_b)
    assert len(dict_a_mk) == 0, "Same keys, shouldn't be any diff. {dict_a_mk}"
    assert len(dict_b_mk) == 0, "Same keys, shouldn't be any diff. {dict_b_mk}"
    assert value_diff == [[["b"], 1, 2]], "The diffrent key. {value_diff}"

