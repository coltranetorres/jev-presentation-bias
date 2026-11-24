"""Disk-cached clients for the Jev decisions API and OpenRouter chat completions."""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

JEV_URL = "https://openrouter.ai/api/alpha/decisions"
CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"
JEV_MODEL = "typesafe/jev-1.14"
RETRIES = 4

# Observed Jev answer shapes (smoke test):
#   noul:   {"type": "noul", "noul": 0.85}
#   choice: {"type": "choice", "choice": "A", "probabilities": {"A": 1, "B": 0}, "confidence": 1}


def _headers() -> dict:
    key = os.environ["OPENROUTER_API_KEY"]
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def _post_with_retry(url: str, payload: dict) -> dict:
    last = "no attempt"
    for attempt in range(RETRIES):
        resp = requests.post(url, headers=_headers(), data=json.dumps(payload), timeout=120)
        if resp.status_code == 429 or resp.status_code >= 500:
            last = f"http {resp.status_code}"
            time.sleep(2**attempt)
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError(f"request to {url} failed after {RETRIES} attempts: {last}")


def _cached(cache_dir: str, payload: dict, fetch):
    """Return fetch() result, cached on sha256 of payload. Failures are never cached."""
    key = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    path = Path(cache_dir) / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text())
    value = fetch()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))
    return value


def _validate_answer(name: str, spec: dict, ans: object) -> None:
    """Raise RuntimeError unless `ans` has the shape Jev promises for this question type."""
    ok = isinstance(ans, dict)
    if ok and spec["type"] == "noul":
        ok = isinstance(ans.get("noul"), (int, float)) and 0 <= ans["noul"] <= 1
    elif ok and spec["type"] == "choice":
        ok = ans.get("choice") in spec["criteria"] and isinstance(ans.get("probabilities"), dict)
    if not ok:
        raise RuntimeError(f"invalid Jev answer for {name!r}: {str(ans)[:200]}")


def call_jev(state: list, questions: dict, cache_dir: str = "cache/jev") -> dict:
    """Ask Jev typed questions about `state`; returns the response's `answers` dict."""
    payload = {"model": JEV_MODEL, "state": state, "questions": questions}

    def fetch() -> dict:
        body = _post_with_retry(JEV_URL, payload)
        answers = body.get("answers") if isinstance(body, dict) else None
        if not isinstance(answers, dict) or set(answers) != set(questions):
            raise RuntimeError(f"unexpected Jev response shape: {str(body)[:200]}")
        for name, spec in questions.items():
            _validate_answer(name, spec, answers[name])
        return answers

    return _cached(cache_dir, payload, fetch)


def chat(prompt: str, model: str, system: str | None = None, cache_dir: str = "cache/chat") -> str:
    """Single-turn OpenRouter chat completion; returns the message text."""
    messages = ([{"role": "system", "content": system}] if system else []) + [
        {"role": "user", "content": prompt}
    ]
    payload = {"model": model, "messages": messages, "temperature": 0}

    def fetch() -> str:
        body = _post_with_retry(CHAT_URL, payload)
        try:
            return body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as e:
            raise RuntimeError(f"unexpected chat response shape: {str(body)[:200]}") from e

    return _cached(cache_dir, payload, fetch)
