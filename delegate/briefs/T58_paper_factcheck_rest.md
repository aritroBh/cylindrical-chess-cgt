# T58: fact-check the rest of the paper against the repository (non-Claude reviewer)

Output: `delegate/checks/T58_factcheck_rest.md` (new file). Write nothing else. Do not edit `paper/`.

The paper is `paper/ieee/main.tex` with `paper/ieee/sections/*.tex`. Another reviewer covers Section VIII and the
conclusion. You cover every OTHER section: 00_abstract, 02_rules, 03_basic, 04_kings, 05_sums, 06_atlas, 07_targets,
09_real, 10_tablebases (or whatever file holds the tablebase section), 11_dawson, 12_engines, 13_verification and the
appendix.

The labels mean:
- [P] proved by hand;
- [AI] proof checked by AI models only;
- [C2] two independently written programs agree;
- [C1] one program;
- [Conj] conjecture.

For every sentence that states a number, a position, a value or a label:
1. Find the evidence. Start from `RESULTS.md`, `delegate/REVIEW.md` and the directories they name.
2. Say whether the claim is supported, quoting the file and line.

Flag:
- overclaims;
- wrong or missing labels;
- stale numbers;
- grammar errors;
- sentences a reader cannot follow.

Give a one-line fix for each, no longer than the original. Order the findings by severity.

Rules:
- Read-only except your output file.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`.
- No git.
- No computation over 2 minutes.
