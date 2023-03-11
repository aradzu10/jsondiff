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


def dict_diff(dict_a, dict_b):
    dict_a_missing_keys = []
    dict_b_missing_keys = []
    value_diff = []
    return dict_a_missing_keys, dict_b_missing_keys, value_diff


def print_diff(dict_a_missing_keys, dict_b_missing_keys, value_diff):
    pass


def main(argv):
    assert len(argv) == 2, "Should be only 2 parameters for the script <json_a> <json_b>"
    logging.info(f"Got json_a = {argv[0]}, json_b = {argv[1]}")
    dict_a, dict_b = load_dicts(argv[0], argv[1])
    dict_a_missing_keys, dict_b_missing_keys, value_diff = dict_diff(dict_a, dict_b)
    print_diff(dict_a_missing_keys, dict_b_missing_keys, value_diff)


if __name__ == '__main__':
    app.run(main)
