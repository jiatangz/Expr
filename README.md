# Expr

A tool to run shell experiments and parse output

## Command Runner
Example:

```python
from expr import *

COMMANDS = [
    Command(
        name="threads",
        value=[1, 2],
        pattern="-threads={}"
    ),
    Command(
        name="buffer",
        value=[64, 128],
        pattern="-buffer_size={}"
    )
]

if __name__ == '__main__':
    execute("./test", COMMANDS, "test_out", run=False)
```

Output

```shell
./test -threads=1 -buffer_size=64 >> ./test-threads=1-buffer_size=64
./test -threads=1 -buffer_size=128 >> ./test-threads=1-buffer_size=128
./test -threads=2 -buffer_size=64 >> ./test-threads=2-buffer_size=64
./test -threads=2 -buffer_size=128 >> ./test-threads=2-buffer_size=128
```

Will compute the Cartesian product of the commands and join with the base command.

<hr>

By default, the filename suffix is the same as the pattern, but you can also specify a custom suffix (similar to pattern)
```python
Command(
    name="xxx",
    value=[1, 2],
    pattern="-threads={}",
    suffix="-suffix_{}"
)
```
Will give you output to `./test-suffix_1-buffer_size=64` etc.

<br>

If the value is a List or Tuple, it will also expand the list to match with pattern.
```python
Command(
    name="xxx",
    value=[(1, 2), (3, 4)],
    pattern="a={}, b={}"
)
```

<br>

In some cases, we may need a special suffix instead of using the value, for example when the value itself is the command
```python
Command(
    name="xxx",
    value=["-v1 -v5", "-v2 -v3", "-v4"],
    pattern="{}",
    suffix="{}",
    symbols=["name1", "name2", "name3"]
)
```
If we specify the symbols, then when compute the suffix, it will use the symbol instead of value as the suffix, note `len(value) == len(symbols)`


## Result Parser

```python
FIELDS = [
    Rule(
        name="throughput",
        regex=r"agg_throughput:\s+([0-9.eE+-]+)\s+ops/sec",
        process=expr_avg
    ),
    Rule(
        name="p99",
        regex=r"p99_latency:\s+([0-9.eE+-]+)\s+ms",
        process=expr_max
    )
]

if __name__ == '__main__':
    out = from_files(FIELDS, 
               [
                   "./sample_output/test_1.txt",
                   "./sample_output/test_2.txt",
                   "./sample_output/test_3.txt"
                ], a=1, b=2)
    for k,v in out.items():
        print(f"{k}={v}")
```

Give a list of filenames, and list of rules, it will try to match the regex to each file,
then for the list of result, process with the `process` function.
The final result will be stored in a dict, you can add some results to the dict also, like `a=1, b=2` above, 
which will generalize other processing, like output to CSV file.

You can also declare your own function

```python
def avg(l:List[str]):
    return sum(map(float, l)) / len(l)
```

Note that the result of regex matching is a string.
Since most of the time I need to handle double/int, so I provide some build in functions which can be used directly.

```python
def expr_avg(l):
    return sum(map(float, l)) / len(l)

def expr_sum(l):
    return sum(map(float, l))

def expr_max(l):
    return max(map(float, l))
```

## Dict to CSV
Then we can simply convert results to CSV file, assume the last command is the replicates.

```python
filename = "test"
COMMANDS = [
    Command(
        name="thread",
        value=[1, 2, 3],
        pattern="-thread={}",
        suffix=""
    ),
    # ... other Commands
    Command(
        name="runs",
        value=[1, 2, 3],
        pattern="",
        suffix="_{}.txt"
    )
]

# group by the last command, params is the combination of commands
groups = [
    ([os.path.join("./sample_output", f"{filename}{c1.suffix}{c2.suffix}") 
    for c2 in expand_commands(COMMANDS[-1:])], c1.params)
    for c1 in expand_commands(COMMANDS[:-1])
]

# for each group, compute the result
results = [from_files(FIELDS, group, **param) for group, param in groups]

# dump the results to CSV file
dict_to_csv(results, "./sample_output/out.csv")
```
