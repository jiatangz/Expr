# ---- declare rules ----
from expr import *

FIELDS = [
    Rule(
        name="throughput",
        regex=r"agg_throughput:\s+([0-9.eE+-]+)\s+ops/sec",
        process=expr_avg
    ),
    Rule(
        name="avg_latency",
        regex=r"avg_latency:\s+([0-9.eE+-]+)\s+ms",
        process=expr_avg
    ),
    Rule(
        name="p99",
        regex=r"p99_latency:\s+([0-9.eE+-]+)\s+ms",
        process=expr_max
    )
]

COMMANDS = [
    Command(
        name="threads",
        value=[1, 2],
        pattern="-threads={}",
        suffix="-suffix_{}",
        symbols=["t1", "t2"],
    ),
    Command(
        name="buffer_size",
        value=[64, 128],
        pattern="-buffer_size={}"
    ),
    Command(
        name="runs",
        value=[1, 2, 3],
        pattern="",
        suffix="_run_{}.txt"
    )
]

if __name__ == '__main__':
    # example: execute command
    execute("./test", COMMANDS, "test", run=False)

    # example: filter data from files
    out = from_files(FIELDS, 
               [
                   "./sample_output/test_1.txt",
                   "./sample_output/test_2.txt",
                   "./sample_output/test_3.txt"
                ], a=1, b=2)
    for k,v in out.items():
        print(f"{k}={v}")
    
    # example: using command to get files, then filter data and store to csv
    filename = "test"
    COMMANDS = [
        Command(
            name="thread",
            value=[1, 2, 3],
            pattern="-thread={}",
            suffix=""
        ),
        Command(
            name="runs",
            value=[1, 2, 3],
            pattern="",
            suffix="_{}.txt"
        )
    ]
    # groups = [
    #     ([os.path.join("./sample_output", f"{filename}{c1.suffix}{c2.suffix}") 
    #     for c2 in expand_commands(COMMANDS[-1:])], c1.params)
    #     for c1 in expand_commands(COMMANDS[:-1])
    # ]
    # results = [from_files(FIELDS, group, **param) for group, param in groups]
    # dict_to_csv(results, "./sample_output/out.csv")
    parse(COMMANDS, FIELDS, filename, "./sample_output/out.csv", "./sample_output")
