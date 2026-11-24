"""Run the experiment end to end for one dataset. Cached, so reruns are cheap.

Usage: uv run python run_all.py [truthfulqa|mmlu_pro] [--n N]
"""
import argparse
from pathlib import Path

from jev_bias.absolute import run_absolute
from jev_bias.analyze import absolute_summary, make_chart, pairwise_summary, write_summary
from jev_bias.data import load_items, load_mmlu_pro
from jev_bias.pairwise import run_pairwise
from jev_bias.styles import build_variants

LOADERS = {"truthfulqa": load_items, "mmlu_pro": load_mmlu_pro}
REWRITE_MODEL = "anthropic/claude-sonnet-5.5"
CHECK_MODEL = "anthropic/claude-haiku-5.5"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset", nargs="?", default="truthfulqa", choices=LOADERS)
    ap.add_argument("--n", type=int, default=80)
    args = ap.parse_args()
    out = Path("results") / args.dataset
    out.mkdir(parents=True, exist_ok=True)

    items = LOADERS[args.dataset](args.n, seed=0)
    variants = build_variants(items, REWRITE_MODEL, CHECK_MODEL, out_path=str(out / "variants.json"))
    excluded = sum(len(v["excluded"]) for v in variants.values())
    print(f"dataset={args.dataset} items={len(items)} excluded variants={excluded}")
    abs_df = run_absolute(variants, items, out_path=str(out / "absolute.csv"))
    pair_df = run_pairwise(variants, items, out_path=str(out / "pairwise.csv"))
    abs_s, pair_s = absolute_summary(abs_df), pairwise_summary(pair_df)
    abs_s.to_csv(out / "absolute_summary.csv", index=False)
    pair_s.to_csv(out / "pairwise_summary.csv", index=False)
    make_chart(abs_s, pair_s, path=str(out / "chart.png"))
    write_summary(abs_s, pair_s, path=str(out / "summary.md"))
    print((out / "summary.md").read_text())


if __name__ == "__main__":
    main()
