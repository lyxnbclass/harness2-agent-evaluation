# Harness²: Evaluation-Driven Self-Improving Coding Agent

An engineering project to reproduce Google Research Harness² and build an auditable evaluation workflow for coding agents. The central question is whether a harness change improves task outcomes **without hiding regressions, infrastructure failures, or extra cost**.

> **Status (2026-10-30): Stage 00 in progress.** This repository currently contains the project plan, evidence records, a sample run manifest, and local progress-check scripts. The upstream Harness² checkout, official demo, public benchmark integration, custom evaluator modules, and agent-performance experiments have **not** been completed.

## Engineering scope

| Track | Responsibility | Current state |
| --- | --- | --- |
| Official reproduction | Check out a pinned revision of [google-research/harness2](https://github.com/google-research/harness2), trace its runner/evaluator/report flow, and reproduce its demo and authorized single-task run | **In progress:** environment inventory started; upstream code and demo not yet verified |
| Public coding benchmark | Select a benchmark (SWE-bench is the leading candidate), run its **native evaluator** independently, then build a Harness² adapter | **Planned:** benchmark selection and evaluator run have not occurred |
| Project evaluation extensions | Implement metrics, trajectory validation, bad-case records, paired comparisons, a regression gate, and reproducible reports | **Planned:** specifications exist; implementation and tests do not |

The benchmark's native evaluator will determine the task verdict. The project evaluation layer will normalize and compare results, diagnose failures, and decide whether a proposed harness change needs review. It will not override the native verdict.

## Planned architecture

The following is a **target data flow**, not a claim about verified upstream APIs or implemented modules:

```text
Coding task + pinned repository revision
                 |
                 v
       Harness² run + agent executor
                 |
          trace + proposed patch
                 |
       benchmark-native evaluator
                 |
             task verdict
                 |
      result normalization + metrics
                 |
       trace / bad-case analysis
                 |
       paired baseline comparison
                 |
          regression gate
                 |
        report + run manifest
```

The adapter, evaluator boundaries, and actual function-level call graph will be documented only after the relevant source and artifacts are verified. The [official evaluation audit](learning/OFFICIAL_EVAL_AUDIT.md) tracks that work.

## Evaluation design

The planned implementation separates **what happened** from **why it happened**:

| Evidence | Planned handling |
| --- | --- |
| Native task verdict | Preserve the evaluator, version, task ID, and original verdict artifact |
| Outcome accounting | Report `resolved`, `failed`, `infra_error`, and `unscored` separately, with an explicit denominator |
| Agent trajectory | Validate tool calls, arguments, ordering, retries, timeouts, and policy violations without treating a clean trace as proof of task success |
| Bad cases | Link each diagnosis to a reproducible task, run, trace step, and falsifiable root-cause hypothesis |
| Paired comparison | Align baseline and candidate by task ID under comparable model, environment, and evaluator settings |
| Regression decision | Use `PASS`, `REVIEW`, or `FAIL`; safety failures block automatic adoption, while ordinary regressions or uncertain evidence require review |
| Efficiency | Record tokens, latency, and cost when observable; leave unavailable fields unknown rather than inventing values |

Development, validation, and locally un-tuned task sets will be separated. Small samples will be labeled smoke tests; a local held-out set cannot prove that a model never saw a task during training. The module contracts and planned counterexamples are in [EVALUATION_SYSTEM_SPEC.md](EVALUATION_SYSTEM_SPEC.md).

## Implementation roadmap

A stage is checked only after its required implementation and tests have evidence, its interview gate passes, and its PR is merged. The detailed [14-stage plan](MASTER_PLAN.md) and [current progress record](learning/PROGRESS.md) are the source of truth.

| Stage | Engineering milestone | Status |
| --- | --- | --- |
| 00 | Environment, upstream revision, and official demo | **In progress** |
| 01 | Minimal agent runtime and tool calling | Planned |
| 02 | Dataset design and outcome metrics | Planned |
| 03 | Trajectory validation and bad-case analysis | Planned |
| 04 | Judge rubric, validation, and calibration | Planned |
| 05 | Prompt, tool-schema, retry, and runtime experiments | Planned |
| 06 | Source-level Propose–Probe–Compose and reflection trace | Planned |
| 07 | Authorized official single-task model run | Planned |
| 08 | Public benchmark selection and native evaluator | Planned |
| 09 | Coding-benchmark adapter | Planned |
| 10 | Paired comparison, ablations, and regression gate | Planned |
| 11 | Reflection and long-term-memory experiments | Planned |
| 12 | Original engineering extension and validation | Planned |
| 13 | Final reproducibility review and technical presentation | Planned |

## What is in the repository today

- [`scripts/resume.py`](scripts/resume.py) restores the recorded current stage; [`scripts/check_workspace.py`](scripts/check_workspace.py) checks record completeness. Both ran successfully in the Stage 00 workspace check. They do **not** validate agent quality or stage mastery.
- [`learning/`](learning/) contains stage status, source/audit templates, interview gates, and command evidence.
- [`experiments/manifests/EXAMPLE_MANIFEST.json`](experiments/manifests/EXAMPLE_MANIFEST.json) is a **sample schema**, not a completed experiment.
- [`upstream/README.md`](upstream/README.md) documents the intended location for official source. `upstream/harness2/` is not present yet.

No project-specific Harness² install or demo command is published here yet: the upstream revision and its CLI have not been verified. The currently verified local record checks, run from the repository root, are:

```powershell
python scripts/resume.py
python scripts/check_workspace.py
```

Both commands exited with code 0 in the latest recorded Stage 00 check. The second command checks documentation consistency only. Once the official checkout is available, this section will add pinned dependency versions, verified setup steps, executable demo commands, and artifact paths.

## Experimental results

**No coding-agent performance results are available.** There is no measured baseline, candidate harness, SWE-bench verdict, success-rate delta, token cost, or latency comparison to report. Future results will link a run manifest, fixed task IDs, model and executor configuration, upstream/benchmark commits, native verdicts, paired changes, regression cases, cost, and limitations. The [deliverables checklist](PROJECT_DELIVERABLES.md) distinguishes completed evidence from planned work.

## Development, review, and attribution

Stage 00 work is on [`stage-00-setup`](https://github.com/lyxnbclass/harness2-agent-evaluation/tree/stage-00-setup); the stage PR has not been created because its implementation and interview gate are incomplete. Each stage uses a dedicated branch and reviewable PR. After a stage PR is merged, this README must be updated with the verified milestone, implemented functions, tests, run commands, and results. Unfinished work remains labeled **Planned** or **In progress**.

Google Research Harness² is upstream work. The public benchmark and its native evaluator are separate upstream work. Project extensions under `experiments/` will be identified by their own code and test evidence. Development here is performed with Codex; the project owner reviews architecture, code behavior, failure analysis, and stage evidence. Contribution claims will follow those records rather than attributing generated code to the owner.

This is an independent project, not an official Google Research or SWE-bench release. Any upstream code added here must retain its applicable license and copyright notices.
