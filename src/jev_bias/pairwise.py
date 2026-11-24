"""Pairwise run: which of two answers is better? Correct vs wrong, in styled combinations, both orders."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .client import call_jev
from .data import Item
from .styles import STYLES
from .util import pmap

QUESTIONS = {
    "better": {
        "type": "choice",
        "instructions": "Which answer is better (more factually correct)?",
        "criteria": {"A": "Answer A is better", "B": "Answer B is better"},
    }
}


def _conditions(styles: list[str]) -> list[tuple[str, str]]:
    """(correct_style, wrong_style): plain/plain, then each style on the correct side, then on the wrong side."""
    conds = [("plain", "plain")]
    for s in styles:
        if s != "plain":
            conds += [(s, "plain"), ("plain", s)]
    return conds


def run_pairwise(variants: dict, items: list[Item], styles: list[str] = STYLES,
                 out_path: str = "results/pairwise.csv") -> pd.DataFrame:
    qmap = {it.qid: it.question for it in items}
    jobs = []
    for qid, v in variants.items():
        for cs, ws in _conditions(styles):
            if cs not in v["correct"] or ws not in v["wrong"]:
                continue
            for order in ("correct_first", "wrong_first"):
                jobs.append((qid, cs, ws, order, v["correct"][cs], v["wrong"][ws]))

    def run(job):
        qid, _, _, order, c, w = job
        a, b = (c, w) if order == "correct_first" else (w, c)
        ans = call_jev([f"Question: {qmap[qid]}", f"Answer A: {a}", f"Answer B: {b}"], QUESTIONS)["better"]
        if ans["choice"] not in ("A", "B"):
            raise ValueError(f"unexpected choice key {ans['choice']!r}")
        correct_slot = "A" if order == "correct_first" else "B"
        return ans["choice"] == correct_slot, float(ans["probabilities"][correct_slot])

    res = pmap(run, jobs)
    df = pd.DataFrame([(j[0], j[1], j[2], j[3], r[0], r[1]) for j, r in zip(jobs, res)],
                      columns=["qid", "correct_style", "wrong_style", "order", "picked_correct", "p_correct_side"])
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    return df
