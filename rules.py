# ---- declare rules ----
from parse import *

FIELDS = [
    Rule(
        name="throughput",
        regex=r"agg_throughput:\s+([0-9.eE+-]+)\s+ops/sec",
        process=lambda l: sum(l) / len(l)
    ),
    Rule(
        name="avg_latency",
        regex=r"avg_latency:\s+([0-9.eE+-]+)\s+ops/sec",
        process=lambda l: sum(l) / len(l)
    ),
    Rule(
        name="p99",
        regex=r"p99_latency:\s+([0-9.eE+-]+)\s+ms",
        process=lambda l: max(l)
    )
]