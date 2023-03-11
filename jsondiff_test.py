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


def test_diff_keys():
    dict_a = {
        "a": 1,
        "b": 1,
    }
    dict_b = {
        "a": 1,
        "c": 2,
    }
    dict_a_mk, dict_b_mk, value_diff = jsondiff.dict_diff(dict_a, dict_b)
    assert dict_a_mk == [[["b"], 1]], "Key only in dict a. {dict_a_mk}"
    assert dict_b_mk == [[["c"], 2]], "Key only in dict b. {dict_b_mk}"
    assert len(value_diff) == 0, "Same values for all same keys. {value_diff}"

    dict_b_mk, dict_a_mk, value_diff = jsondiff.dict_diff(dict_b, dict_a)
    assert dict_a_mk == [[["b"], 1]], "Key only in dict a. {dict_a_mk}"
    assert dict_b_mk == [[["c"], 2]], "Key only in dict b. {dict_b_mk}"
    assert len(value_diff) == 0, "Same values for all same keys. {value_diff}"


def test_diff_keys_in_one_dict():
    dict_a = {
        "a": 1,
        "b": 1,
    }
    dict_b = {
        "a": 1,
    }
    dict_a_mk, dict_b_mk, value_diff = jsondiff.dict_diff(dict_a, dict_b)
    assert dict_a_mk == [[["b"], 1]], "Key only in dict a. {dict_a_mk}"
    assert len(dict_b_mk) == 0, "Same keys from b in a. {dict_b_mk}"
    assert len(value_diff) == 0, "Same values for all same keys. {value_diff}"

    dict_b_mk, dict_a_mk, value_diff = jsondiff.dict_diff(dict_b, dict_a)
    assert dict_a_mk == [[["b"], 1]], "Key only in dict a. {dict_a_mk}"
    assert len(dict_b_mk) == 0, "Same keys from b in a. {dict_b_mk}"
    assert len(value_diff) == 0, "Same values for all same keys. {value_diff}"


def test_same_keys_diff_value_list():
    dict_a = {
        "a": 1,
        "b": [1, 2, 3],
    }
    dict_b = {
        "a": 1,
        "b": [1, 1, 3],
    }
    dict_a_mk, dict_b_mk, value_diff = jsondiff.dict_diff(dict_a, dict_b)
    assert len(dict_a_mk) == 0, "Same keys, shouldn't be any diff. {dict_a_mk}"
    assert len(dict_b_mk) == 0, "Same keys, shouldn't be any diff. {dict_b_mk}"
    assert value_diff == [[["b"], [1, 2, 3], [1, 1, 3]]], "The diffrent key. {value_diff}"


def test_same_dict_recursive():
    dict_a = {
        "a": {
            "a": {
                "a": 1,
                "b": [1, 2],
            },
        },
        "b": [1, 2, 3],
    }
    dict_a_mk, dict_b_mk, value_diff = jsondiff.dict_diff(dict_a, dict_a)
    assert len(dict_a_mk) == 0, "Same dict, shouldn't be any diff. {dict_a_mk}"
    assert len(dict_b_mk) == 0, "Same dict, shouldn't be any diff. {dict_b_mk}"
    assert len(value_diff) == 0, "Same dict, shouldn't be any diff. {value_diff}"


def test_same_keys_diff_value_recursive():
    dict_a = {
        "a": {
            "a": {
                "a": 1,
                "b": [1, 2],
            },
        },
        "b": [1, 2, 3],
    }
    dict_b = {
        "a": {
            "a": {
                "a": 2, # Diffrent value
                "b": [1, 2],
            },
        },
        "b": [1, 2, 3],
    }
    dict_a_mk, dict_b_mk, value_diff = jsondiff.dict_diff(dict_a, dict_b)
    assert len(dict_a_mk) == 0, "Same keys, shouldn't be any diff. {dict_a_mk}"
    assert len(dict_b_mk) == 0, "Same keys, shouldn't be any diff. {dict_b_mk}"
    assert value_diff == [[["a", "a", "a"], 1, 2]], "The diffrent key. {value_diff}"


def test_diff_key_value_recursive():
    dict_a = {
        "a": {
            "a": {
                "a": 1,
                "b": 1,
            },
        },
        "b": [1, 2, 3],
    }
    dict_b = {
        "a": {
            "a": {
                "a": 1,
                "c": 2,
            },
        },
        "b": [1, 2, 3],
    }
    dict_a_mk, dict_b_mk, value_diff = jsondiff.dict_diff(dict_a, dict_b)
    assert dict_a_mk == [[["a", "a", "b"], 1]], "Key only in dict a. {dict_a_mk}"
    assert dict_b_mk == [[["a", "a", "c"], 2]], "Key only in dict b. {dict_b_mk}"
    assert len(value_diff) == 0, "Same values for all same keys. {value_diff}"

    dict_b_mk, dict_a_mk, value_diff = jsondiff.dict_diff(dict_b, dict_a)
    assert dict_a_mk == [[["a", "a", "b"], 1]], "Key only in dict a. {dict_a_mk}"
    assert dict_b_mk == [[["a", "a", "c"], 2]], "Key only in dict b. {dict_b_mk}"
    assert len(value_diff) == 0, "Same values for all same keys. {value_diff}"


def test_diff_keys_in_one_dict():
    dict_a = {
        "a": {
            "a": {
                "a": 1,
                "b": 1,
            },
        },
        "b": [1, 2, 3],
    }
    dict_b = {
        "a": {
            "a": {
                "a": 1,
            },
        },
        "b": [1, 2, 3],
    }
    dict_a_mk, dict_b_mk, value_diff = jsondiff.dict_diff(dict_a, dict_b)
    assert dict_a_mk == [[["a", "a", "b"], 1]], "Key only in dict a. {dict_a_mk}"
    assert len(dict_b_mk) == 0, "Same keys from b in a. {dict_b_mk}"
    assert len(value_diff) == 0, "Same values for all same keys. {value_diff}"

    dict_b_mk, dict_a_mk, value_diff = jsondiff.dict_diff(dict_b, dict_a)
    assert dict_a_mk == [[["a", "a", "b"], 1]], "Key only in dict a. {dict_a_mk}"
    assert len(dict_b_mk) == 0, "Same keys from b in a. {dict_b_mk}"
    assert len(value_diff) == 0, "Same values for all same keys. {value_diff}"


def test_single_missing_key_and_value_diff():
    dict_a = {
        "a": {
            "a": {
                "a": 1,
                "b": 1,
                "diff": 1,
            },
        },
        "b": [1, 2, 3],
    }
    dict_b = {
        "a": {
            "a": {
                "a": 1,
                "c": 2,
                "diff": 2,
            },
        },
        "b": [1, 2, 3],
    }
    dict_a_mk, dict_b_mk, value_diff = jsondiff.dict_diff(dict_a, dict_b)
    assert dict_a_mk == [[["a", "a", "b"], 1]], "Key only in dict a. {dict_a_mk}"
    assert dict_b_mk == [[["a", "a", "c"], 2]], "Key only in dict b. {dict_b_mk}"
    assert value_diff == [[["a", "a", "diff"], 1, 2]], "Diffrent value. {value_diff}"

    dict_b_mk, dict_a_mk, value_diff = jsondiff.dict_diff(dict_b, dict_a)
    assert dict_a_mk == [[["a", "a", "b"], 1]], "Key only in dict a. {dict_a_mk}"
    assert dict_b_mk == [[["a", "a", "c"], 2]], "Key only in dict b. {dict_b_mk}"
    assert value_diff == [[["a", "a", "diff"], 2, 1]], "Diffrent value. {value_diff}"


def test_complex_missing_key_and_value_diff():
    dict_a = {
        "a": {
            "a": {
                "a": 1,
                "b": 1,
                "diff": 1,
            },
            "b": {
                "a": 1,
            },
            "c": {
                "a": 1,
            },
        },
        "b": [1, 2, 3],
    }
    dict_b = {
        "a": {
            "a": {
                "a": 1,
                "c": 2,
                "diff": [1, 2],
            },
            "b": 3,
            "c": {
                "a": 2,
                "c": 1,
            },
        },
        "b": [1, 2, 3],
    }
    dict_a_mk, dict_b_mk, value_diff = jsondiff.dict_diff(dict_a, dict_b)
    assert dict_a_mk == [[["a", "a", "b"], 1]], "Key only in dict a. {dict_a_mk}"
    assert dict_b_mk == [[["a", "a", "c"], 2], [["a", "c", "c"], 1]], "Key only in dict b. {dict_b_mk}"
    assert value_diff == [[["a", "a", "diff"], 1, [1, 2]], [['a', 'b'], {'a': 1}, 3], [['a', 'c', 'a'], 1, 2]], "Diffrent value. {value_diff}"
