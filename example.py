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
        value=[1, 2],
        pattern="-threads={}",
        suffix="-suffix_{}",
        symbols=["t1", "t2"],
    ),
    Command(
        value=[64, 128],
        pattern="-buffer_size={}"
    ),
    Command(
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
            value=[1, 2, 3],
            pattern="",
            suffix="_{}.txt"
        )
    ]
    groups = [
        [os.path.join("./sample_output", f"{filename}{s1}{s2}") 
        for _, s2 in expand_commands(COMMANDS[-1:])]
        for _, s1 in expand_commands(COMMANDS[:-1])
    ]
    results = [from_files(FIELDS, group, exp="exp1") for group in groups]
    dict_to_csv(results, "./sample_output/out.csv")
