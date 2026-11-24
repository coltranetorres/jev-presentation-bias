"""Absolute grading run: is a single answer factually correct?"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .client import call_jev
from .data import Item
from .util import pmap

QUESTIONS = {
    "is_correct": {
        "type": "noul",
        "instructions": "Is the answer factually correct?",
        "criteria": {"true": "The answer is factually correct", "false": "The answer is factually incorrect"},
    }
}


def run_absolute(variants: dict, items: list[Item], out_path: str = "results/absolute.csv") -> pd.DataFrame:
    qmap = {it.qid: it.question for it in items}
    jobs = [(qid, side, style, text)
            for qid, v in variants.items() for side in ("correct", "wrong") for style, text in v[side].items()]

    def run(job):
        qid, _, _, text = job
        ans = call_jev([f"Question: {qmap[qid]}", f"Answer: {text}"], QUESTIONS)
        return ans["is_correct"]["noul"]

    probs = pmap(run, jobs)
    df = pd.DataFrame([(q, s, st, p) for (q, s, st, _), p in zip(jobs, probs)],
                      columns=["qid", "side", "style", "p_correct"])
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    return df
