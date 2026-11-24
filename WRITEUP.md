# Does the way an answer is written change how Jev judges it?

**Draft. All numbers come from `results/truthfulqa/summary.md`, `results/mmlu_pro/summary.md` and the CSVs beside them.**

---

How well can a judge model tell a correct answer from a polished one?

I used Jev (typesafe/jev-1.14) as an LLM judge on two sets of questions, each with one correct and one wrong answer:
- TruthfulQA: 80 questions, wrong answers are common misconceptions.
- MMLU-Pro (knowledge categories): 40 questions, where the wrong answer is the distractor an LLM picked as the most tempting one.

I rewrote every answer in 7 styles with the facts held fixed (reworded, formatted, long, short, confident, technical, conversational), then checked whether Jev's verdict moved.

**1. Jev mostly judged the facts, not the packaging.**
With both answers in plain style, Jev picked the correct one 96.5% of the time on TruthfulQA and 90.5% on MMLU-Pro. Restyling either answer kept TruthfulQA accuracy between 95.5% and 98.3%. On MMLU-Pro, 12 of 14 conditions stayed within about 3 points of the matched baseline (the exceptions were a confident or a conversational correct answer, down 10.6 and 5.4 points), and no style let polish win outright. Putting the correct answer first or second made little difference (TruthfulQA plain/plain: 95.8% vs 97.2%).

**2. The one style that mattered was confidence, and it hurt.**
Confident language ("without question", "definitely") lowered Jev's P(correct) on both datasets, more for correct answers than for wrong ones:
- TruthfulQA: -7.3 points on correct answers, -4.1 on wrong.
- MMLU-Pro: -8.9 points on correct answers, -5.4 on wrong.

On MMLU-Pro that showed up in the verdicts too. When the correct answer was the confident one, accuracy fell to 78.8% against a matched baseline of 89.4%. Jev didn't reward bluster; it was mildly skeptical of it. Other styles moved scores by about 3 points or less: long and conversational rewrites lowered correct-answer scores by about 3 points on MMLU-Pro, and short rewrites raised them by 1-3 points.

**3. Style shows up in the scores before it shows up in the verdicts.**
On TruthfulQA, confident rewrites pushed 14.9% of correct answers across the 0.5 line while no other style went above 7.6%, yet pairwise accuracy never moved outside noise. The harder MMLU-Pro set, with more room for error, was the one where the shift reached the verdicts.

**Takeaway:** On these tasks, Jev behaves like it is evaluating what is said rather than how it is said. Style never made a wrong answer win, but a confident tone made it a little less willing to endorse right ones.

**Caveats:**
- One run per setting. TruthfulQA has 80 questions; MMLU-Pro has 40, of which 37 had usable pairs after filtering, so its intervals are wide (the confident-correct 78.8% has a 95% CI of 68-88%). Treat the size of that effect as suggestive and its direction as consistent across both sets.
- Baselines are high (96.5% and 90.5%), so there is limited headroom for style to flip verdicts.
- MMLU-Pro skips math, physics, chemistry and engineering, because a judge can't check calculations without working them out. Distractors were picked by Claude, not by Jev.
- Rewrites were LLM-generated and checked by another LLM, plus a manual read of 12 TruthfulQA variants. The fact check dropped 76 of 1,120 TruthfulQA variants and 27 of 560 MMLU-Pro ones, most often `long` and `confident`, so surviving variants stayed closer to the original claims. Pairwise accuracies are compared against a baseline on the same questions.
- "Confident" rewrites add certainty phrases, so a penalty may be a reasonable reaction to unsupported certainty rather than bias.
- Exact-0.5 probabilities count as "incorrect" in flip rates.
- The decisions endpoint is alpha.

Code and results: [link]
