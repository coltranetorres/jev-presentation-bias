# Does the way an answer is written change how Jev judges it?

**Draft. All numbers come from `results/summary.md` and the CSVs in `results/`.**

---

Can a judge model tell a correct answer from a polished one?

I used Jev (typesafe/jev-1.14) as an LLM judge on 80 TruthfulQA questions. Each has one correct and one plausible-but-wrong answer. I rewrote every answer in 7 styles with the facts held fixed (reworded, formatted, long, short, confident, technical, conversational), then checked whether Jev's verdict moved.

**1. Jev mostly judged the facts, not the packaging.**
Shown a correct and a wrong answer side by side, Jev picked the correct one 96.5% of the time with both in plain style. With either answer restyled, accuracy stayed between 95.5% and 98.3%, and the largest change against a matched plain baseline was 2.5 points. Putting the correct answer first or second made little difference (95.8% vs 97.2% in the plain/plain pairs).

**2. The clearest effect was the opposite of what I expected.**
Confident language ("without question", "definitely") lowered Jev's P(correct) by 7.3 points on correct answers and 4.1 on wrong ones. Long rewrites lowered it by 3.9 points on correct answers. Jev didn't reward bluster; if anything it was mildly skeptical of it. Most other styles moved scores by about a point or less (short rewrites of correct answers were up 1.3).

**3. Style shows up in the scores before it shows up in the verdicts.**
Confident rewrites pushed 14.9% of correct answers across the 0.5 line in the absolute setup, while no other style went above 7.6%. In the pairwise setup, no style moved accuracy outside noise.

**Takeaway:** On this task, Jev behaves like it is evaluating what is said rather than how it is said. Style is a small nudge on confidence, not a lever on the verdict.

**Caveats:**
- One run per setting, up to 80 questions. Intervals are bootstrap 95% CIs.
- TruthfulQA's wrong answers may be easy to spot (96.5% plain/plain), so there is little headroom; subtler errors could show more bias.
- Rewrites were LLM-generated and checked by another LLM, plus a manual read of 12 variants. The fact check dropped 76 of 1,120 answer variants (31 `long`, 17 `confident`, 8 plain baselines that drifted from the source fact), so surviving variants stayed closer to the original claims. Pairwise accuracies are compared against a baseline on the same questions.
- "Confident" rewrites add certainty phrases, so a small penalty may be a reasonable reaction to unsupported certainty rather than bias.
- Exact-0.5 probabilities count as "incorrect" in flip rates.
- The decisions endpoint is alpha.

Code and results: [link]
