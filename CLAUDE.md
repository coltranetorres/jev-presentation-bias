# jev-presentation-bias

Mini research experiment: does answer presentation (wording, formatting, length, tone) change the verdicts of Jev (`typesafe/jev-1.14`, OpenRouter decisions API) when used as an LLM judge? Output is a LinkedIn-style writeup.

Spec: `docs/superpowers/specs/2026-11-24-jev-presentation-bias-design.md`
Plan: `docs/superpowers/plans/2026-11-24-jev-presentation-bias.md`

## Commands

- Install: `uv sync`
- Tests: `uv run pytest`
- Single test: `uv run pytest tests/test_client.py::test_name -v`
- Full pipeline: `uv run python run_all.py [truthfulqa|mmlu_pro] [--n N]`

Use `uv` for everything (`uv add <pkg>`, `uv run ...`). Do not use pip or `requirements.txt`.

## Layout

- `src/jev_bias/`: `client.py` (cached Jev + chat clients), `data.py`, `styles.py`, `absolute.py`, `pairwise.py`, `analyze.py`
- `results/<dataset>/` (truthfulqa, mmlu_pro): raw CSV/JSON, `chart.png`, `summary.md` (committed)
- `cache/`, `data/`: API response cache and downloaded dataset (git-ignored)

## Rules

- API key is `OPENROUTER_API_KEY` in `.env`, loaded with `load_dotenv()`. Never print, log, or commit it.
- Every network response is cached on disk. Reruns must not hit the network for cached inputs. Never cache failed responses.
- The decisions endpoint is alpha: `https://openrouter.ai/api/alpha/decisions`. Parse responses strictly and fail loudly on unexpected shapes.
- Style rewrites must keep facts unchanged. Variants that fail the fact check are excluded and the exclusion count is reported, never silently dropped.
- Pairwise runs always cover both A/B orders.
- Never invent numbers in the writeup; every figure comes from `results/<dataset>/summary.md`.
- Write the failing test first. Mock network calls in tests (`requests.post` / `chat`); tests must not need the API key.
- Python: type hints on public functions, small focused modules, no dead code.
