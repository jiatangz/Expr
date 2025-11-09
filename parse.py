import re
import os
from dataclasses import dataclass
from typing import Callable, List


@dataclass
class Rule:
    name: str
    regex: str
    process: Callable[[List[str]], str]


def __read_file(filename):
    with open(filename, "r") as f:
        text = f.read()
    return text


def __merge_result(result: dict, **kwargs):
    for k, v in kwargs.items():
        if k in result:
            print(f"[Warning] Overwriting key '{k}': {result[k]} -> {v}")
        result[k] = v


def from_files(fields: List[Rule], filenames: List[str], **kwargs):
    # { field_name: [values...] }
    values_map = {field.name: [] for field in fields}

    for fname in filenames:
        if not os.path.exists(fname):
            print("Warning, skip:", fname)
            continue

        text = __read_file(fname)

        for field in fields:
            match = re.search(field.regex, text)
            if match:
                values_map[field.name].append(float(match.group(1)))
            else:
                print(f"[Warning] {fname} not match with {field.regex}")

    result = {}
    for field in fields:
        vals = values_map[field.name]
        if vals:
            result[field.name] = field.process(vals)
        else:
            result[field.name] = None

    __merge_result(result, **kwargs)
    return result

