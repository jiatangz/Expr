import re
import os
from dataclasses import dataclass
import subprocess
from typing import Callable, List
from itertools import product


def expr_avg(l):
    return sum(map(float, l)) / len(l)

def expr_sum(l):
    return sum(map(float, l))

def expr_max(l):
    return max(map(float, l))

def expr_min(l):
    return min(map(float, l))

def expr_first(l):
    return l[0]

def expr_last(l):
    return l[-1]

@dataclass
class Rule:
    name: str
    regex: str
    process: Callable[[List[str]], str]

@dataclass
class Command:
    value: List
    pattern: str
    suffix: str = None

    def __post_init__(self):
        if self.suffix is None:
            self.suffix = self.pattern


def __expand_commands__(commands: List[Command]):
    value_lists = [cmd.value for cmd in commands]
    for combo in product(*value_lists):
        parts = []
        suffixes = []
        for (cmd, val) in zip(commands, combo):
            if isinstance(val, (list, tuple)):
                parts.append(cmd.pattern.format(*val))
                suffixes.append(cmd.suffix.format(*val))
            else:
                parts.append(cmd.pattern.format(val))
                suffixes.append(cmd.suffix.format(val))
        yield " ".join(parts), "".join(suffixes)


def __read_file__(filename: str):
    with open(filename, "r") as f:
        text = f.read()
    return text


def __merge_result__(result: dict, **kwargs):
    for k, v in kwargs.items():
        if k in result:
            print(f"[Warning] Overwriting key '{k}': {result[k]} -> {v}")
        result[k] = v


def __run_cmd__(log_dir: str, filename: str, cmd: str):
    os.makedirs(log_dir, exist_ok=True)
    if os.path.exists(filename):
        print(f"[SKIP] {filename} already exists.")
        return
    filename = os.path.join(log_dir, filename)
    print(f"[RUN] {filename}")
    with open(filename, "w") as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
            

def from_files(fields: List[Rule], filenames: List[str], **kwargs):
    # { field_name: [values...] }
    values_map = {field.name: [] for field in fields}

    for fname in filenames:
        if not os.path.exists(fname):
            print("[Warning] skip:", fname)
            continue

        text = __read_file__(fname)

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

    __merge_result__(result, **kwargs)
    return result


def execute(basic_cmd:str, commands:List[Command], filename: str, log_dir='./', run=True):
    for custom_cmd, suffix in __expand_commands__(commands):
        cmd = " ".join([basic_cmd, custom_cmd])
        if run:
            __run_cmd__(log_dir=log_dir, filename=filename+suffix, cmd=cmd)
        else:
            print(cmd + " >> " + os.path.join(log_dir, filename + suffix))

    