# Does answer presentation affect Jev's judgment? (Experiment 3)

## Intent
Use Jev (`typesafe/jev-1.14` via OpenRouter decisions API) as a straight LLM judge and test whether it evaluates answer quality or reacts to presentation. Output is a LinkedIn-style writeup: one headline chart, 2-3 numbered findings, honest caveats (same format as the Gemma fine-tuning post).

Research question: is Jev evaluating actual answer quality or reacting to presentation?

## Goals / non-goals / anti-goals
- Goals: measure (a) verdict flips and (b) probability shift when only style changes; produce reproducible scripts, raw results, and a chart.
- Non-goals: comparing against other judges, fine-tuning, multimodal inputs.
- Anti-goals: style rewrites that quietly change facts (would invalidate the result); claiming more than ~1 run per setting supports.

## Approach (chosen: C)
Considered A (absolute grading only), B (pairwise only), C (both on the same question set). Chose C: absolute grading shows whether style moves scores in isolation, pairwise shows whether style can beat correctness head to head. Cost is ~2x API calls.

## Design
1. **Data**: ~60-100 factual questions with one correct and one plausible-but-wrong answer, drawn from a public set (TruthfulQA-style). *My call.*
2. **Style variants** (LLM-generated via OpenRouter, facts held constant), applied to both the correct and wrong answer:
   - baseline (plain)
   - reworded
   - formatted (markdown bullets/headers/bold)
   - long (padded, same facts)
   - short
   - confident tone
   - technical vs. conversational
   A fact-preservation check (LLM check plus manual spot-check of a sample) gates inclusion. *Variant list is my call.*
3. **Absolute run**: per (answer, style), ask Jev a `noul` question "Is this answer factually correct?" Record probability. Metric: mean shift vs. baseline per style, and flip rate (crosses 0.5).
4. **Pairwise run**: `choice` question "Which answer is better?" Pairs: correct-plain vs. wrong-styled (does polish beat correctness?) and correct-styled vs. wrong-plain (sanity). Each pair run in both A/B orders to cancel position bias. Metric: verdict flip rate vs. the plain/plain pair, plus accuracy per style.
5. **Stats**: bootstrap 95% CIs over questions; report n. One run per setting (caveat), unless the API is cheap enough to repeat. *My call.*
6. **Outputs**: `results/*.json|csv` raw responses, one chart (flip rate / accuracy by style), writeup draft.

## Constraints
- API key in `.env` as `OPENROUTER_API_KEY`, loaded with `load_dotenv()`; `.env` stays uncommitted.
- Endpoint: `https://openrouter.ai/api/alpha/decisions` (alpha, so cache all responses on disk).
- Python, `requests`, `python-dotenv`.

## Left to the builder
Exact question wording and criteria text for Jev, rewrite prompts, which model generates rewrites, caching and retry details, chart styling.
