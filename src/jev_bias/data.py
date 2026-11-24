"""TruthfulQA item loader."""
from __future__ import annotations

import random
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .client import EmptyChatError, chat

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


def _tempting_distractor(question: str, opts: list[str], correct_idx: int, model: str) -> int | None:
    """Ask an LLM (never Jev) for the wrong option most likely to fool an expert; None if the reply is unusable."""
    letters = "ABCDEFGHIJ"
    listing = "\n".join(f"{letters[i]}. {o}" for i, o in enumerate(opts))
    prompt = (f"Question: {question}\n\n{listing}\n\nThe correct answer is {letters[correct_idx]}. "
              "Which ONE incorrect option is most tempting, the one most likely to fool a knowledgeable person? "
              "Reply with a single letter only.")
    try:
        reply = chat(prompt, model).strip().upper()[:1]
    except EmptyChatError:
        return None
    idx = letters.find(reply) if reply else -1
    return idx if 0 <= idx < len(opts) and idx != correct_idx else None


def load_mmlu_pro(n: int = 80, seed: int = 0, path: str = "data/mmlu_pro.parquet",
                  distractor_model: str | None = None) -> list[Item]:
    """Correct option vs a distractor, from knowledge-style MMLU-Pro categories.

    The distractor is the LLM-chosen most tempting wrong option when `distractor_model` is given
    (falling back to a random one if the reply is unusable), else random.
    """
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
        ci = int(r["answer_index"])
        pick = _tempting_distractor(r["question"], opts, ci, distractor_model) if distractor_model else None
        wrong = opts[pick] if pick is not None else rng.choice([o for i, o in enumerate(opts) if i != ci])
        items.append(Item(f"m{r['question_id']}", r["question"], correct, wrong))
    return items
