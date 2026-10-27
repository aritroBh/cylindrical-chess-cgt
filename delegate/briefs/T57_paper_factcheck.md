# T57: fact-check the paper's Section VIII and conclusion against the repository (non-Claude reviewer)

Output: `delegate/checks/T57_factcheck.md` (new file). Write nothing else. Do not edit `paper/`.

## What to do

The paper is `paper/ieee/main.tex` with `paper/ieee/sections/*.tex`. Read `sections/08_star2.tex` and
`sections/14_conclusion.tex` in full, plus the intro's contribution list in `sections/01_intro.tex`.

The labels mean:
- [P] proved by hand;
- [AI] proof checked by AI models only;
- [C2] two independently written programs agree;
- [C1] one program;
- [Conj] conjecture.

For EVERY sentence in Section VIII that states a number, a position, a value or a label:
1. Find the evidence in the repository. Start from:
   - `RESULTS.md` and `delegate/REVIEW.md`;
   - `research/star26_rings/`, `research/c8_independent/`, `research/ring_min_c5c6/`;
   - `research/ring_family_proof/`, `research/ring_n_plus_2_proof/` (PROOF.md), `research/ring_n_plus_2_check/`;
   - `research/star4_hunt/`.
2. Say whether the number, position and label are supported. Quote the file and line.
3. Flag:
   - overclaims;
   - missing model qualifiers ("whole-board game" vs "sum of components");
   - wrong labels;
   - stale numbers;
   - sentences that are unclear to a reader.

For each problem give a one-line fix in plain short sentences, no longer than the original.

Then list results in the repository that are verified (CHECKED-2 or refereed) but missing from the paper, with the
evidence file.

## Rules

- Read-only, except your one output file.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`.
- No git, no long computations (nothing over 2 minutes).
