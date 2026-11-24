"""Build results/combined_chart.png from the per-dataset summary CSVs.

Usage: uv run python combine_charts.py
"""
import pandas as pd

from jev_bias.analyze import make_combined_chart

DATASETS = {"TruthfulQA (80 Qs)": "truthfulqa", "MMLU-Pro (40 Qs)": "mmlu_pro"}


def main() -> None:
    data = {
        label: (pd.read_csv(f"results/{d}/absolute_summary.csv"), pd.read_csv(f"results/{d}/pairwise_summary.csv"))
        for label, d in DATASETS.items()
    }
    make_combined_chart(data)


if __name__ == "__main__":
    main()
