# Does the way an answer is written change how Jev judges it?

**Draft. All numbers come from `results/summary.md`.**

---

Can a judge model tell a correct answer from a polished one?

I used Jev (typesafe/jev-1.14) as an LLM judge on 80 TruthfulQA questions. Each question has one correct and one plausible-but-wrong answer. I rewrote every answer in 7 styles with the facts held fixed (reworded, formatted, long, short, confident, technical, conversational), then checked whether Jev's verdict moved.

**1. Jev mostly judged the facts, not the packaging.**
Shown a correct and a wrong answer side by side, Jev picked the correct one 94% of the time with both in plain style. Across all 14 styled conditions (correct styled or wrong styled, 7 styles) the figure stayed between 92% and 96%. No style pushed accuracy below 92%, and every styled condition's interval overlaps the plain baseline.

**2. The one consistent effect was the opposite of what I expected.**
Confident language ("without question", "definitely") lowered Jev's P(correct): -7.2 points on correct answers and -4.0 on wrong ones. Long rewrites lowered it by 3.8 points on correct answers. Jev didn't reward bluster; if anything it was mildly skeptical of it. Other styles moved scores by about a point or less.

**3. Style effects show up in the scores before they show up in the verdicts.**
In the pairwise setup, no style moved accuracy outside normal noise. In the absolute setup, confident rewrites crossed the 0.5 line for 14.7% of correct answers, while most other styles stayed under 8%.

**Takeaway:** On this task, Jev behaves like it is evaluating what is said rather than how it is said. Style is a small nudge on confidence, not a lever on the verdict.

**Caveats:**
- One run per setting, 80 questions. Intervals are bootstrap 95% CIs.
- TruthfulQA wrong answers may be easy to spot (94% plain/plain), so there is little headroom; subtler errors could show more bias.
- Rewrites were LLM-generated and fact-checked by another LLM, with a manual spot-check of 12 variants. The fact check excluded 71 of 2,240 variants (most often `long`: 32 and `confident`: 18), so surviving variants stayed closer to the original claims.
- "Confident" rewrites add certainty phrases, so a small penalty may be a reasonable reaction to unsupported certainty rather than bias.
- The decisions endpoint is alpha.

Code and results: [link]
