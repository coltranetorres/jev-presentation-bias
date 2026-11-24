"""TruthfulQA item loader."""
from __future__ import annotations

import random
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

URL = "https://raw.githubusercontent.com/sylinrl/TruthfulQA/main/TruthfulQA.csv"


MMLU_URL = "https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro/resolve/main/data/test-00000-of-00001.parquet"
# Calculation-heavy categories are excluded: a judge cannot verify them without working them out.
MMLU_EXCLUDED = {"math", "physics", "chemistry", "engineering"}


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


def load_mmlu_pro(n: int = 80, seed: int = 0, path: str = "data/mmlu_pro.parquet") -> list[Item]:
    """Correct option vs one randomly chosen distractor, from knowledge-style MMLU-Pro categories."""
    p = Path(path)
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(MMLU_URL, p)
    df = pd.read_parquet(p)
    df = df[~df["category"].isin(MMLU_EXCLUDED)]
    df = df.sample(n=min(n, len(df)), random_state=seed)
    rng = random.Random(seed)
    items = []
    for _, r in df.iterrows():
        opts = list(r["options"])
        correct = opts[int(r["answer_index"])]
        wrong = rng.choice([o for i, o in enumerate(opts) if i != int(r["answer_index"])])
        items.append(Item(f"m{r['question_id']}", r["question"], correct, wrong))
    return items
