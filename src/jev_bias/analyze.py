"""Summaries, bootstrap CIs, chart and markdown summary for the experiment."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def bootstrap_ci(values: np.ndarray, stat=np.mean, n: int = 2000, seed: int = 0) -> tuple[float, float]:
    values = np.asarray(values, dtype=float)
    if len(values) == 0:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    stats = [stat(rng.choice(values, size=len(values), replace=True)) for _ in range(n)]
    return float(np.percentile(stats, 2.5)), float(np.percentile(stats, 97.5))


def absolute_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Per (side, style): mean shift in p_correct vs the plain variant of the same answer, flip rate across 0.5."""
    cols = ["side", "style", "shift", "ci_lo", "ci_hi", "flip_rate", "n"]
    plain = df[df["style"] == "plain"].set_index(["qid", "side"])["p_correct"].rename("p_plain")
    m = df.join(plain, on=["qid", "side"]).dropna(subset=["p_plain"])
    m["shift"] = m["p_correct"] - m["p_plain"]
    m["flip"] = (m["p_correct"] > 0.5) != (m["p_plain"] > 0.5)
    rows = []
    for (side, style), g in m.groupby(["side", "style"], sort=False):
        lo, hi = bootstrap_ci(g["shift"].to_numpy())
        rows.append((side, style, g["shift"].mean(), lo, hi, g["flip"].mean(), len(g)))
    return pd.DataFrame(rows, columns=cols)


def pairwise_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Per (correct_style, wrong_style, order|both): accuracy (+CI) and flip rate vs the plain/plain baseline."""
    cols = ["correct_style", "wrong_style", "order", "accuracy", "ci_lo", "ci_hi", "flip_rate", "n"]
    if df.empty:
        return pd.DataFrame(columns=cols)
    base = (df[(df.correct_style == "plain") & (df.wrong_style == "plain")]
            .set_index(["qid", "order"])["picked_correct"].rename("base"))
    m = df.join(base, on=["qid", "order"])
    m["flip"] = m["picked_correct"] != m["base"]
    rows = []
    for (cs, ws), g in m.groupby(["correct_style", "wrong_style"], sort=False):
        for order, gg in [*g.groupby("order"), ("both", g)]:
            lo, hi = bootstrap_ci(gg["picked_correct"].astype(float).to_numpy())
            flip = gg["flip"].mean() if gg["base"].notna().any() else float("nan")
            rows.append((cs, ws, order, gg["picked_correct"].mean(), lo, hi, flip, len(gg)))
    return pd.DataFrame(rows, columns=cols)


def make_chart(abs_df: pd.DataFrame, pair_df: pd.DataFrame, path: str = "results/chart.png") -> None:
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [1, 1]})
    colors = {"correct": "#3b6fd4", "wrong": "#d9663a"}

    styles = [s for s in abs_df["style"].unique() if s != "plain"]
    x = np.arange(len(styles))
    for i, side in enumerate(("correct", "wrong")):
        g = abs_df[abs_df.side == side].set_index("style").reindex(styles)
        err = [g["shift"] - g["ci_lo"], g["ci_hi"] - g["shift"]]
        ax1.bar(x + (i - 0.5) * 0.38, g["shift"], 0.38, yerr=err, color=colors[side], capsize=3,
                label=f"{side} answers")
    ax1.axhline(0, color="#555", lw=0.8)
    ax1.set_xticks(x, styles, rotation=30, ha="right")
    ax1.set_ylabel("Change in P(judged correct) vs plain")
    ax1.set_title("Same facts, different style: how much Jev's score moves", loc="left", fontsize=11)
    ax1.legend(frameon=False)

    both = pair_df[pair_df.order == "both"]
    styled_wrong = both[both.correct_style == "plain"].set_index("wrong_style")
    styled_right = both[both.wrong_style == "plain"].set_index("correct_style")
    labels = ["plain"] + styles
    acc_w = [styled_wrong.loc[s, "accuracy"] if s in styled_wrong.index else np.nan for s in labels]
    acc_r = [styled_right.loc[s, "accuracy"] if s in styled_right.index else np.nan for s in labels]
    x2 = np.arange(len(labels))
    ax2.bar(x2 - 0.19, acc_r, 0.38, color=colors["correct"], label="correct answer styled")
    ax2.bar(x2 + 0.19, acc_w, 0.38, color=colors["wrong"], label="wrong answer styled")
    ax2.axhline(0.5, color="#555", lw=0.8, ls="--")
    ax2.set_ylim(0, 1.05)
    ax2.set_xticks(x2, labels, rotation=30, ha="right")
    ax2.set_ylabel("Share of pairs where Jev picks the correct answer")
    ax2.set_title("Pairwise: can polish beat correctness?", loc="left", fontsize=11)
    ax2.legend(frameon=False, loc="lower left")

    fig.suptitle("Does presentation sway Jev as a judge?", fontsize=15, x=0.02, ha="left", fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160)
    plt.close(fig)


def write_summary(abs_df: pd.DataFrame, pair_df: pd.DataFrame, path: str = "results/summary.md") -> None:
    parts = ["# Results summary\n", "## Absolute grading (shift in P(correct) vs plain)\n",
             abs_df.round(3).to_markdown(index=False),
             "\n\n## Pairwise (accuracy, flips vs plain/plain)\n",
             pair_df.round(3).to_markdown(index=False)]
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(parts) + "\n")
