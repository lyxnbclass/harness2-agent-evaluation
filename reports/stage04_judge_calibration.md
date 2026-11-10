# Stage 04 deterministic judge calibration

**Observed local run, 2026-11-10.** `python -m experiments.evaluators.calibrate_judge --output reports/stage04_judge_calibration.json` compared 15 Codex-authored manual reference labels with the rule judge. These labels are review material, not independent user or external human annotations. The dataset is synthetic and deliberately contains counterexamples; the observed 12/15 agreement is not a general reliability estimate or model benchmark result.

| Manual label / Judge result | pass | fail |
| --- | ---: | ---: |
| pass | 7 | 2 |
| fail | 1 | 5 |

Three observed disagreements:

1. `j04`: manual `pass`, rule judge `fail`. The response says `five` while the reference string is `5`. The strict answer comparison misses a semantic equivalent. A future semantic normalizer or human review could resolve this, but the allowable forms must be specified before evaluation.
2. `j08`: manual `pass`, rule judge `fail`. The explanation says “Adding 2 and 3 gives five” but lacks the exact required keyword `sum`. The keyword check mistakes a valid explanation for missing evidence. A broader evidence rubric or review path is needed; simply adding more synonyms after seeing validation cases risks overfitting.
3. `j12`: manual `fail`, rule judge `pass`. The answer and explanation match the answer-only rubric, but separate trace evidence records `unauthorized_tool`. This is missing context in the judge input, not proof that answer text is wrong. A later system should combine the native verdict, trace policy findings, and a safety gate without letting this answer judge overwrite them.

One order probe compared concise-correct `j01` with verbose-wrong `j02`. Results were `A` in original order and `B` after swapping; the same candidate won. One constructed pair cannot rule out position bias in LLM judges. `j02` did not win for verbosity. The fake instruction in `j11` did not change its `fail` result. The schema test rejected extra fields, boolean score, false verdict claims, invalid dimensions and reason codes; bounded retry tests covered an invalid response and a simulated timeout.

**Limitations:** no paid model API, no official Harness² Judge, no SWE-bench native evaluator, no statistical claim from 15 constructed cases. The local reference labels require user review; the three disagreements are intentionally informative, not a representative error rate. The local-held-out Stage 02 cases were previously inspected and cannot be reused as untouched validation evidence.
