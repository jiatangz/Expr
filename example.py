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
        suffix="-suffix_{}"
    ),
    Command(
        value=[64, 128],
        pattern="-buffer_size={}"
    )
]

if __name__ == '__main__':
    execute("./test", COMMANDS, "test", run=False)
    out = from_files(FIELDS, 
               [
                   "./sample_output/test_1.txt",
                   "./sample_output/test_2.txt",
                   "./sample_output/test_3.txt"
                ], a=1, b=2)
    for k,v in out.items():
        print(f"{k}={v}")

