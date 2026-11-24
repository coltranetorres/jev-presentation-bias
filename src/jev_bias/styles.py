"""Generate style variants of answers, gated by a fact-preservation check."""
from __future__ import annotations

import json
from pathlib import Path

from .client import chat
from .data import Item
from .util import pmap

STYLES = ["plain", "reworded", "formatted", "long", "short", "confident", "technical", "conversational"]

_RULES = (
    "Output ONLY the rewritten answer text, no preamble or commentary. "
    "Do not add, remove, soften, or change any factual claim, and do not correct the claim even if "
    "you believe it is false: your job is presentation only.\n\n"
)

STYLE_PROMPTS: dict[str, str] = {
    "plain": (
        "Write a plain, neutral three-sentence answer (claim, brief explanation, brief wrap-up, with no new facts) to the question below that asserts exactly "
        "the given fact and nothing else. Do not correct the fact even if you think it is false. "
        "Output ONLY the answer.\n\n{text}"
    ),
    "reworded": _RULES + "Rewrite this answer using different wording and sentence structure, same tone and length:\n\n{text}",
    "formatted": _RULES + "Rewrite this answer with rich markdown formatting (a bold lead sentence, bullet points, a short header), conveying the same content:\n\n{text}",
    "long": _RULES + "Rewrite this answer at roughly 4x the length using elaboration, framing and restatement, but introduce NO new facts:\n\n{text}",
    "short": _RULES + "Rewrite this answer as tersely as possible while keeping every claim:\n\n{text}",
    "confident": _RULES + "Rewrite this answer in an extremely confident, authoritative, emphatic tone (e.g. 'definitely', 'without question'), same claims:\n\n{text}",
    "technical": _RULES + "Rewrite this answer in a formal, technical, expert register with precise terminology, same claims:\n\n{text}",
    "conversational": _RULES + "Rewrite this answer as if chatting with a friend: contractions, casual phrasing, a bit of filler like 'honestly' or 'so', same claims:\n\n{text}",
}

CHECK_PROMPT = (
    "Do these two answers assert the same factual claims, with nothing added, removed, or reversed? "
    "Ignore tone, formatting, and length. Reply with exactly one word: SAME or DIFFERENT.\n\n"
    "Answer 1:\n{a}\n\nAnswer 2:\n{b}"
)


def _build_side(item: Item, side: str, fact: str, rewrite_model: str, check_model: str) -> tuple[dict, list]:
    plain = chat(STYLE_PROMPTS["plain"].format(text=f"Question: {item.question}\nFact to assert: {fact}"), rewrite_model).strip()
    variants, excluded = {"plain": plain}, []
    for style in STYLES:
        if style == "plain":
            continue
        text = chat(STYLE_PROMPTS[style].format(text=plain), rewrite_model).strip()
        verdict = chat(CHECK_PROMPT.format(a=plain, b=text), check_model).strip().upper()
        if verdict.startswith("SAME"):
            variants[style] = text
        else:
            excluded.append([side, style])
    return variants, excluded


def build_variants(items: list[Item], rewrite_model: str, check_model: str,
                   out_path: str = "results/variants.json") -> dict:
    jobs = [(it, side) for it in items for side in ("correct", "wrong")]
    results = pmap(lambda j: _build_side(j[0], j[1], getattr(j[0], j[1]), rewrite_model, check_model), jobs)
    out: dict = {it.qid: {"correct": {}, "wrong": {}, "excluded": []} for it in items}
    for (it, side), (variants, excluded) in zip(jobs, results):
        out[it.qid][side] = variants
        out[it.qid]["excluded"].extend(excluded)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(out, indent=1))
    return out
