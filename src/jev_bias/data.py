"""TruthfulQA item loader."""
from __future__ import annotations

import urllib.request
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

URL = "https://raw.githubusercontent.com/sylinrl/TruthfulQA/main/TruthfulQA.csv"


@dataclass(frozen=True)
class Item:
    qid: str
    question: str
    correct: str
    wrong: str


def load_items(n: int = 80, seed: int = 0, path: str = "data/truthfulqa.csv") -> list[Item]:
    p = Path(path)
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL, p)
    df = pd.read_csv(p)
    df["qid"] = [f"q{i}" for i in df.index]
    cols = ["Question", "Best Answer", "Best Incorrect Answer"]
    df = df.dropna(subset=cols)
    df = df[(df[cols].apply(lambda c: c.str.strip()) != "").all(axis=1)]
    df = df.sample(n=min(n, len(df)), random_state=seed)
    return [
        Item(r["qid"], r["Question"], r["Best Answer"], r["Best Incorrect Answer"])
        for _, r in df.iterrows()
    ]
