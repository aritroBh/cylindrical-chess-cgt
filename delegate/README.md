# Delegated execution

Claude plans and integrates. External AI CLIs do the execution, which saves Claude tokens and gives the
project non-Claude implementations for verification.

| Task | Tool | Brief | Output |
|---|---|---|---|
| T1 | codex | independent solver; re-check the §1 headline results | `verify_ext/codex/` |
| T2 | kilo (Nemotron Ultra) | second-model re-derivation of the proofs | `verify_ext/qwen/` |
| T3 | opencode (OmniRoute coding:free) | Elkies targets: robustness, reachability, FENs | `atlas/targets/` |
| T4 | opencode | cylinder atlas under the e.p.-aware test | `atlas/cylinder/ep_aware/` |
| T5 | opencode (OmniRoute best-free) | ML baselines on ChessSums | `ml/chesssums_baseline/` |
| T6 | opencode (beam-free) | ML on Dawson's chess | `ml/dawson/` |
| T7 | kilo (kilo-auto free) | referee / completeness review | `notes/ext_review_kilo/` |

- **Briefs:** each prompt is `COMMON.md` followed by the file in `briefs/`.
- **Launch:** start everything with `delegate/run.sh`, or a subset with, for example, `delegate/run.sh T1 T5`.
- **Watch:** each task writes `logs/<task>.log`. A finished task leaves a REPORT.md in its output directory.
