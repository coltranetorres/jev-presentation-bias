"""Run the whole experiment end to end. Cached, so reruns are cheap."""
import json
from pathlib import Path

import pandas as pd

from jev_bias.absolute import run_absolute
from jev_bias.analyze import absolute_summary, make_chart, pairwise_summary, write_summary
from jev_bias.data import load_items
from jev_bias.pairwise import run_pairwise
from jev_bias.styles import build_variants

N_ITEMS = 80
REWRITE_MODEL = "anthropic/claude-sonnet-5.5"
CHECK_MODEL = "anthropic/claude-haiku-5.5"


def main() -> None:
    items = load_items(N_ITEMS, seed=0)
    variants = build_variants(items, REWRITE_MODEL, CHECK_MODEL)
    excluded = sum(len(v["excluded"]) for v in variants.values())
    print(f"items={len(items)} excluded variants={excluded}")
    abs_df = run_absolute(variants, items)
    pair_df = run_pairwise(variants, items)
    abs_s, pair_s = absolute_summary(abs_df), pairwise_summary(pair_df)
    abs_s.to_csv("results/absolute_summary.csv", index=False)
    pair_s.to_csv("results/pairwise_summary.csv", index=False)
    make_chart(abs_s, pair_s)
    write_summary(abs_s, pair_s)
    print(Path("results/summary.md").read_text())


if __name__ == "__main__":
    main()
