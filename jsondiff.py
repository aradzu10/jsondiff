#!/usr/bin/env python3
import argparse
import json
import sys

args = None


BLUE = "\033[96m"
GREEN = "\033[92m"
RESET = "\033[00m"


def blue_str(string):
    if args.nocolor:
        return string
    return f"{BLUE}{string}{RESET}"


def green_str(string):
    if args.nocolor:
        return string
    return f"{GREEN}{string}{RESET}"


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
            dict_b_missing_keys.append([[key], dict_b[key]])

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
    # Keys are reverse, because it better to add the key as append instead of
    # allocating a new list each time we go back in the recursion.
    dict_a_missing_keys = [[key[::-1], value] for key, value in dict_a_missing_keys]
    dict_b_missing_keys = [[key[::-1], value] for key, value in dict_b_missing_keys]
    value_diff = [[key[::-1], value_a, value_b] for key, value_a, value_b in value_diff]
    return dict_a_missing_keys, dict_b_missing_keys, value_diff


def print_diff(dict_a_missing_keys, dict_b_missing_keys, value_diff):
    print(blue_str("Keys inside of json_a"), "(missing in json_b)")
    for key, value in dict_a_missing_keys:
        print("::".join(key), "=", value)
    print("")

    print(green_str("Keys inside of json_b"), "(missing in json_a)")
    for key, value in dict_b_missing_keys:
        print("::".join(key), "=", value)
    print("")

    print("Keys with diffrent values")
    for key, value_a, value_b in value_diff:
        print("@", "::".join(key))
        print(blue_str(f"json a: {value_a}"))
        print(green_str(f"json b: {value_b}"))
        print("")


def main():
    if not sys.stdout.isatty():
        args.nocolor = True

    print("Got", blue_str(f"json_a = {args.json_a}") + ",", green_str(f"json_b = {args.json_b}"))
    print("")
    dict_a, dict_b = load_dicts(args.json_a, args.json_b)
    dict_a_missing_keys, dict_b_missing_keys, value_diff = dict_diff(dict_a, dict_b)
    print_diff(dict_a_missing_keys, dict_b_missing_keys, value_diff)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='jsondiff',
        description='Json diff using a python script in your bash.',
    )
    parser.add_argument('json_a', help="First json to be compare.")
    parser.add_argument('json_b', help="Second json to be compare.")
    parser.add_argument(
        '--nocolor', action='store_true', default=False, help="Turn colors off.")
    args = parser.parse_args()
    main()
