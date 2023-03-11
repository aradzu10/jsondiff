#!/usr/bin/env python3
from absl import app, flags, logging

FLAGS = flags.FLAGS
flags.DEFINE_bool("color", True, "Print lines with colors.")


def load_dicts(dict_a_path, dict_b_path):
    with open(dict_a_path) as f:
        dict_a = json.load(f)
    with open(dict_b_path) as f:
        dict_b = json.load(f)
    return dict_a, dict_b


def dict_diff_impl(dict_a, dict_b):
    dict_a_missing_keys = []
    dict_b_missing_keys = []
    value_diff = []

    if not isinstance(dict_a, dict) or not isinstance(dict_b, dict):
        empty_diff = []
        if dict_a == dict_b:
            return empty_diff, empty_diff, empty_diff
        empty_key = []
        value_diff.append([empty_key, dict_a, dict_b])
        return empty_diff, empty_diff, value_diff

    for key in dict_b:
        if key not in dict_a:
            dict_b_missing_keys.append([[key], dict_a[key]])

    for key in dict_a:
        if key not in dict_b:
            dict_a_missing_keys.append([[key], dict_a[key]])
            continue

        dict_a_mk, dict_b_mk, sub_value_d = dict_diff_impl(dict_a[key], dict_b[key])
        for sub_key, value in dict_a_mk:
            sub_key.append(key)
        for sub_key, value in dict_b_mk:
            sub_key.append(key)
        for sub_key, value_a, value_b in sub_value_d:
            sub_key.append(key)
        dict_a_missing_keys.extend(dict_a_mk)
        dict_b_missing_keys.extend(dict_b_mk)
        value_diff.extend(sub_value_d)

    return dict_a_missing_keys, dict_b_missing_keys, value_diff


def dict_diff(dict_a, dict_b):
    dict_a_missing_keys, dict_b_missing_keys, value_diff = dict_diff_impl(dict_a, dict_b)
    dict_a_missing_keys = [[key[::-1], value] for key, value in dict_a_missing_keys]
    dict_b_missing_keys = [[key[::-1], value] for key, value in dict_b_missing_keys]
    value_diff = [[key[::-1], value_a, value_b] for key, value_a, value_b in value_diff]
    return dict_a_missing_keys, dict_b_missing_keys, value_diff


def print_diff(dict_a_missing_keys, dict_b_missing_keys, value_diff):
    print("Keys inside of json_a, missing in json_b")
    for key, value in dict_a_missing_keys:
        print("::".join(key), "=", value)

    print("Keys inside of json_b, missing in json_a")
    for key, value in dict_b_missing_keys:
        print("::".join(key), "=", value)

    print("Keys with diffrent values")
    for key, value_a, value_b in dict_b_missing_keys:
        print("::".join(key))
        print("a:", value_a)
        print("b:", value_b)


def main(argv):
    assert len(argv) == 2, "Should be only 2 parameters for the script <json_a> <json_b>"
    logging.info(f"Got json_a = {argv[0]}, json_b = {argv[1]}")
    dict_a, dict_b = load_dicts(argv[0], argv[1])
    dict_a_missing_keys, dict_b_missing_keys, value_diff = dict_diff(dict_a, dict_b)
    print_diff(dict_a_missing_keys, dict_b_missing_keys, value_diff)


if __name__ == '__main__':
    app.run(main)
