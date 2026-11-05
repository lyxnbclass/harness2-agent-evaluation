# Stage 02 deterministic metrics smoke test

Date: 2026-11-05. All figures below are **OBSERVED local scripted-contract results**, not Google Harness², SWE-bench, a real model, or coding-agent performance results.

## Inputs and commands

- 24 hand-authored cases in `experiments/datasets/stage02_multitool_cases.jsonl`: 8 `dev`, 8 `validation`, 8 `local-held-out`; tags cover normal, boundary, error, permission, and attack. Each row has `case_id`, `input`, `split`, `expected_outcome`, `tool_constraints`, and `tags`.
- Scripted decisions are separate in `experiments/datasets/stage02_fake_decisions.jsonl`. `run_agent()` receives only each case's `input` and step budget. This is a deterministic teaching fixture, not an independent model solving unseen tasks.
- Run manifest: `experiments/manifests/stage02_fake_v1.json`. The Markdown explanation in this file was written from observed output; an automated `report_generator.py` is a later-stage deliverable.
- `python -m unittest discover -s experiments/evaluators -p test_*.py -v` under local Python 3.12.13 exited 0: **13 tests passed** (recorded run 0.636s; post-PR metadata check also passed 13/13). The existing Toy Runtime suite also passed 8/8 tests (0.110s), and `python scripts/check_workspace.py` exited 0.
- `python -m experiments.evaluators.stage02_demo --output reports/stage02_fake_results.jsonl` under the same Python 3.12 exited 0. The committed JSONL contains all 24 normalized results and local Trace messages.

## Result and denominator contract

| Metric | Observed value | Definition |
| --- | ---: | --- |
| `resolved` | 19 | Scripted runtime status and answer matched the case's contract |
| `failed` | 3 | Contract mismatch after a local run |
| `infra_error` | 1 | Explicitly simulated runner failure; no verdict inferred |
| `unscored` | 1 | Explicitly simulated missing judge result |
| Scored success rate | 19 / 22 = 86.36% | `resolved / (resolved + failed)`; excludes infra and unscored |
| Scored coverage | 22 / 24 = 91.67% | `(resolved + failed) / all cases` |
| Tool schema valid rate | 18 / 23 = 78.26% | Calls with a known tool and exact input names/types / observed calls |
| Unsafe tool rate | 4 / 23 = 17.39% | Calls outside that case's allowlist / observed calls, including blocked attempts |

`median_latency_sec` is recorded for 22 local executions, but the median is only a few microseconds because `FakeModel` uses scripted decisions. It is **not** a model or benchmark latency estimate. No token or API cost was measured.

## Counterexamples and limits

- `dev-08`: expected final answer `5`, observed final answer `5`, and local contract verdict `resolved`. Its Trace shows `uppercase("5")` although the case allowlist contains only `add`; `unsafe_tool_calls=1`. `val-07` has the same pattern with the opposite tool restriction. A correct final answer does not establish a compliant trajectory.
- `val-04`: `add(2,2)` returned `4`, but the scripted final answer was `5`; the local contract verdict is `failed`. A correct tool result does not guarantee a correct final answer.
- `val-08` and `held-06` explicitly simulate `infra_error` and `unscored`. They are not counted as Agent failures or successes.
- A case expecting `invalid_args`, `unknown_tool`, or `max_steps` can count as `resolved` **only because this dataset tests the teaching Runtime contract**. This is not equivalent to solving a software issue or passing SWE-bench.
- This run inspected the `local-held-out` rows. They were not used to tune this version, but future tuning against these observed outcomes would contaminate that local split. The public nature of any benchmark also cannot establish whether a model saw it during training.
- No native Benchmark judge, real model, statistical significance claim, or performance improvement is included. Stage 03 will implement fuller Trace validation; Stage 09 will implement a public Coding Benchmark adapter.
