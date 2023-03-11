# jsondiff
Json diff using a python script in your bash.

## Installation
The project written in `python 3.8.10`.

After cloning, run `jsondiff.py`.

## Usage
```bash
» python jsondiff.py
<Complete>
```

JSON one and two are the jsons to be compare.

`--nocolor` is determind to cancel colors. When redirect output, the color will also be canceled.

## Examples
```
» cat dict_a.json
{
    "a": {
        "a": {
            "a": 1,
            "b": 1,
            "diff": 1
        },
        "b": {
            "a": 1
        },
        "c": {
            "a": 1
        }
    },
    "b": [
        1,
        2,
        3
    ]
}
» cat dict_b.json
{
    "a": {
        "a": {
            "a": 1,
            "c": 2,
            "diff": [
                1,
                2
            ]
        },
        "b": 3,
        "c": {
            "a": 2,
            "c": 1
        }
    },
    "b": [
        1,
        2,
        3
    ]
}
» python jsondiff.py dict_a.json dict_b.json
Got json_a = dict_a.json, json_b = dict_b.json

Keys inside of json_a (missing in json_b)
a::a::b = 1

Keys inside of json_b (missing in json_a)
a::a::c = 2
a::c::c = 1

Keys with diffrent values
@ a::a::diff
json a: 1
json a: 1

@ a::b
json a: {'a': 1}
json a: {'a': 1}

@ a::c::a
json a: 1
json a: 1
```
