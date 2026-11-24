# Jev Presentation-Bias Experiment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Measure whether Jev (as an LLM judge) changes its verdicts or probabilities when answer style changes but facts do not, and produce raw results, one chart, and writeup numbers.

**Architecture:** A small Python package `jev_bias` with a disk-cached Jev client and a disk-cached chat client (for rewrites). Pipeline stages write JSON/CSV into `results/`: build questions -> generate style variants (with fact check) -> absolute run -> pairwise run -> analysis/chart.

**Tech Stack:** Python 3.11+ managed with `uv` (pyproject.toml), `requests`, `python-dotenv`, `pandas`, `numpy`, `matplotlib`, `pytest`.

**Spec:** `docs/superpowers/specs/2026-11-24-jev-presentation-bias-design.md`

## Global Constraints

- Jev model id `typesafe/jev-1.14`, endpoint `https://openrouter.ai/api/alpha/decisions`.
- Key from `.env` as `OPENROUTER_API_KEY` via `load_dotenv()`; never commit `.env`; never print the key.
- Every network response cached on disk (alpha endpoint); reruns must make zero network calls for cached inputs.
- Style variants: `plain`, `reworded`, `formatted`, `long`, `short`, `confident`, `technical`, `conversational`. Facts must be unchanged (fact-check gate).
- ~60-100 questions, one run per setting, bootstrap 95% CIs over questions.
- Pairwise runs both A/B orders.

## Review Focus

- Jev returns an HTTP error/rate limit or malformed `answers`: client retries with backoff, then raises a clear error; never caches failures.
- A style rewrite drops or alters the fact: fact check rejects it and the (question, style) is excluded from both runs, with the exclusion count reported.
- Position bias: pairwise result for the same pair differs by A/B order; analysis must report order-swapped results separately and combined.
- Jev's `choice` returns keys other than the expected `A`/`B`: parsing fails loudly.
- Empty/NaN groups after exclusions: analysis reports n per cell and does not crash on empty cells.

---

### Task 1: Scaffold and cached Jev client

**Files:**
- Create: `.gitignore` (include `.env`, `cache/`, `__pycache__/`), `src/jev_bias/__init__.py`, `src/jev_bias/client.py`
- Test: `tests/test_client.py`

**Interfaces:**
- Produces: `call_jev(state: list, questions: dict, cache_dir: str = "cache/jev") -> dict` returns the response's `answers` dict. `chat(prompt: str, model: str, system: str | None = None, cache_dir: str = "cache/chat") -> str` returns message text via OpenRouter chat completions. Both key the cache on a sha256 of the request payload.

- [ ] **Step 1: Write failing tests** with `requests.post` monkeypatched: `test_call_jev_caches_second_call` (second identical call makes zero HTTP calls and returns equal answers), `test_call_jev_retries_on_429_then_succeeds`, `test_call_jev_raises_and_does_not_cache_on_persistent_error`, `test_chat_caches_second_call`.
- [ ] **Step 2: Run** `uv run pytest tests/test_client.py -v`. Expected: FAIL (module missing).
- [ ] **Step 3: Implement** `call_jev` and `chat` in `src/jev_bias/client.py`; headers per the sample (`Authorization: Bearer`), `load_dotenv()` at import, 4 retries with exponential backoff on 429/5xx, raise `RuntimeError` after.
- [ ] **Step 4: Run** the tests. Expected: PASS.
- [ ] **Step 5: Smoke test** one real `call_jev` with a trivial `noul` question; confirm the response shape (`answers[key]["noul"]`, and for `choice` the `choice` and `probabilities` keys). Record the observed shape in a comment in `client.py`.
- [ ] **Step 6: Commit** `feat: cached jev and chat clients`.

### Task 2: Question set loader

**Files:**
- Create: `src/jev_bias/data.py`
- Test: `tests/test_data.py`

**Interfaces:**
- Produces: `@dataclass Item(qid: str, question: str, correct: str, wrong: str)`; `load_items(n: int = 80, seed: int = 0, path: str = "data/truthfulqa.csv") -> list[Item]`. Downloads TruthfulQA CSV on first use (columns `Question`, `Best Answer`, `Best Incorrect Answer`) to `data/`; deterministic sample by `seed`; skips rows where either answer is empty.

- [ ] **Step 1: Write failing tests** against a tiny fixture CSV: `test_load_items_is_deterministic`, `test_load_items_skips_empty_answers`, `test_load_items_respects_n`.
- [ ] **Step 2: Run** and confirm FAIL.
- [ ] **Step 3: Implement** `load_items` and `Item`.
- [ ] **Step 4: Run** and confirm PASS.
- [ ] **Step 5: Commit** `feat: truthfulqa item loader`.

### Task 3: Style variants with fact-check gate

**Files:**
- Create: `src/jev_bias/styles.py`
- Test: `tests/test_styles.py`

**Interfaces:**
- Consumes: `chat`, `Item`.
- Produces: `STYLES: list[str]` (the 8 styles in Global Constraints); `build_variants(items: list[Item], rewrite_model: str, check_model: str, out_path: str = "results/variants.json") -> dict` writing and returning `{qid: {"correct": {style: text}, "wrong": {style: text}, "excluded": [[side, style], ...]}}`. `plain` is an LLM-written plain full-sentence answer from the short fact; other styles rewrite `plain`. `RewriteModel`/`CheckModel` are parameters (verify the OpenRouter model ids at run time). Fact check: a second `chat` call asks "Do these two answers assert the same facts? Reply SAME or DIFFERENT", and non-`SAME` excludes that variant.

- [ ] **Step 1: Write failing tests** with `chat` monkeypatched: `test_build_variants_covers_all_styles`, `test_different_fact_check_excludes_variant`, `test_exclusions_recorded_not_silently_dropped`.
- [ ] **Step 2: Run** and confirm FAIL.
- [ ] **Step 3: Implement** `build_variants`, with one prompt template per style kept in a `STYLE_PROMPTS: dict[str, str]`.
- [ ] **Step 4: Run** and confirm PASS.
- [ ] **Step 5: Generate for real**, then print the exclusion count and read 15 random variants manually (spec's spot-check). Fix prompts if facts drift; note findings for the writeup caveats.
- [ ] **Step 6: Commit** `feat: style variant generation with fact check`.

### Task 4: Absolute run

**Files:**
- Create: `src/jev_bias/absolute.py`
- Test: `tests/test_absolute.py`

**Interfaces:**
- Consumes: `call_jev`, variants JSON.
- Produces: `run_absolute(variants: dict, items: list[Item], out_path: str = "results/absolute.csv") -> pandas.DataFrame` with columns `qid, side ("correct"|"wrong"), style, p_correct`. State is `[f"Question: {q}", f"Answer: {text}"]`; one `noul` question `is_correct` ("Is the answer factually correct?", criteria true/false). Skips excluded variants.

- [ ] **Step 1: Write failing tests** with `call_jev` monkeypatched: `test_run_absolute_one_row_per_variant`, `test_run_absolute_skips_excluded`.
- [ ] **Step 2: Run** and confirm FAIL.
- [ ] **Step 3: Implement** `run_absolute`.
- [ ] **Step 4: Run** and confirm PASS.
- [ ] **Step 5: Run for real**, confirm the CSV row count equals the non-excluded variant count.
- [ ] **Step 6: Commit** `feat: absolute grading run`.

### Task 5: Pairwise run

**Files:**
- Create: `src/jev_bias/pairwise.py`
- Test: `tests/test_pairwise.py`

**Interfaces:**
- Consumes: `call_jev`, variants JSON.
- Produces: `run_pairwise(variants, items, out_path="results/pairwise.csv") -> DataFrame` with columns `qid, correct_style, wrong_style, order ("correct_first"|"wrong_first"), picked_correct (bool), p_correct_side (float)`. Conditions: for each style s, (`correct=s`, `wrong=plain`) and (`correct=plain`, `wrong=s`), plus `plain/plain`. State holds the question and "Answer A"/"Answer B"; one `choice` question `better` with criteria keys `A` and `B`; parse failure on unknown keys raises `ValueError`.

- [ ] **Step 1: Write failing tests**: `test_both_orders_run_for_every_pair`, `test_picked_correct_maps_through_order` (order-swapped pair where Jev picks "A" yields the right bool), `test_unknown_choice_key_raises`.
- [ ] **Step 2: Run** and confirm FAIL.
- [ ] **Step 3: Implement** `run_pairwise`.
- [ ] **Step 4: Run** and confirm PASS.
- [ ] **Step 5: Run for real**; sanity-check that `plain/plain` accuracy is well above 50% (if not, the judging setup, not style, is the issue; stop and revisit).
- [ ] **Step 6: Commit** `feat: pairwise judging run`.

### Task 6: Analysis and chart

**Files:**
- Create: `src/jev_bias/analyze.py`, `run_all.py` (CLI: `uv run python run_all.py` runs tasks 2-6 in order)
- Test: `tests/test_analyze.py`

**Interfaces:**
- Consumes: the two CSVs.
- Produces: `bootstrap_ci(values: np.ndarray, stat=np.mean, n: int = 2000, seed: int = 0) -> tuple[float, float]`; `absolute_summary(df) -> DataFrame` (per style: mean `p_correct` shift vs `plain` for each side, flip rate across 0.5, CI, n); `pairwise_summary(df) -> DataFrame` (per condition and order: accuracy, flip rate vs `plain/plain`, CI, n); `make_chart(abs_df, pair_df, path="results/chart.png") -> None` (grouped bars by style, CI whiskers, readable at LinkedIn size; follow the `dataviz` skill); `write_summary(abs_df, pair_df, path="results/summary.md")`.

- [ ] **Step 1: Write failing tests**: `test_bootstrap_ci_contains_mean_on_known_data`, `test_absolute_summary_zero_shift_for_plain`, `test_pairwise_summary_handles_empty_cell_without_crash`, `test_pairwise_summary_reports_orders_separately`.
- [ ] **Step 2: Run** and confirm FAIL.
- [ ] **Step 3: Implement** the functions above.
- [ ] **Step 4: Run** and confirm PASS.
- [ ] **Step 5: Run `uv run python run_all.py`** end to end (cached, so no new calls), then view `results/chart.png`.
- [ ] **Step 6: Commit** `feat: analysis, chart, summary`.

### Task 7: Writeup draft

**Files:**
- Create: `WRITEUP.md`

- [ ] **Step 1: Draft** in the style of the Gemma post: a question hook, 2-3 numbered findings using the actual numbers from `results/summary.md`, a one-line takeaway, caveats (one run per setting, n, LLM-generated rewrites with spot-check, exclusion count, alpha endpoint), and a link placeholder for code. Show the draft to the user; do not invent numbers.
- [ ] **Step 2: Commit** `docs: writeup draft`.
