# K5b: cylcgt's values checked by playing G − V with `sumtest/sumsolver.py`

## Summary

1. **CHECKED-2.** All 39 claimed identities of the brief's target table give G + (−V_claim) = 𝓟 in both sumsolver modes ("whole" and "comp"). The 9 literal {0, \* | ↓} rows for ↑²\* are also 𝓟 (same outcomes as the ↑² + \* form).
2. **CHECKED-2.** cylcgt's own value at the 81 target × setting pairs: 72 tested, all 𝓟 in both modes; 9 skipped as BIG translations (an integer of absolute value 256 in V_cyl). The 39 claims are all among the 72 tested pairs, so there are 72 distinct confirmations (not 111), 33 of which were not claimed in the brief.
3. No non-𝓟 result and no "whole" versus "comp" difference anywhere (162 solves, all status `ok`). The sanity checks (26 required, 11 controls) and the decoy controls pass, so the test is not vacuous.
4. "Confirmed" means G + (−V) is 𝓟 in sumsolver's own rule model. sumsolver was written by a Claude model, so the check is independent of cylcgt's code but not of the model family, and it cannot see a misreading of the rules shared by both programs.
5. Reproduce everything from scratch with `bash kings/delegate/out/K5b/run.sh` (262 s wall clock, peak RSS 151 MiB, one Python process at a time under `nice -n 10`).

## Method

> G = V if and only if G + (−V) is a second-player win (outcome 𝓟).

- `sumtest/sumsolver.py` plays a pawn position G plus an explicit game tree by exhaustive minimax. It computes no canonical forms and does not import cylcgt. `cylcgt/cgt.py` was not read.
- Every named V is built from its definition with `Trees.node`, `Trees.add` and `Trees.neg` (`Vals` in `identities.py`): numbers n = {n−1 | }, 1/2 = {0 | 1}, …, 1/16 = {0 | 1/8}; \* = {0 | 0}; \*2 = {0, \* | 0, \*}; ↑ = {0 | \*}; ↓ = {\* | 0}; ↓\* = ↓ + \* and ↑²\* = ↑² + \* as explicit sums; ↑² = {0 | ↓\*}; tiny(1) = {0 | {0 | −1}}; {2±1 | −2±1} = {{3 | 1} | {−1 | −3}}.
- Nine settings: e.p. off, textbook (`ep=True, ep_aware=False`), e.p.-aware (`ep=True, ep_aware=True`), each with race rule count, mover, opponent. `race_double=True`, `ep_scope="component"`.
- Both modes ("whole", "comp") were run for every cell. All trees are added before the solver is built.
- **Pass 1 (claims).** 39 claim cells. **Pass 2 (cylcgt).** V_cyl from `cylcgt.pawns.value`, converted to a `Trees` node by walking the `.L` and `.R` option lists only (no number or nimber tags). `cylcgt.cgt.show` is used for display only. A pair is skipped if V_cyl contains an integer chain of absolute value 64 or more.
- Every cell finished in at most 0.36 s of solver time, far below the 5-minute cutoff.

## Coverage accounting (the numbers are not additive)

| Quantity | Count |
|---|---|
| Target × setting pairs (9 × 9) | 81 |
| Pairs tested against V_cyl | 72 (all 𝓟 in both modes) |
| Pairs skipped as BIG | 9 (so 81 = 72 confirmed + 9 skipped; it is **not** "81 of 81 confirmed") |
| Claimed cells (the brief's table) | 39, all 𝓟 in both modes |
| Claimed cells that are among the 72 tested pairs | 39 (none untested, none skipped) |
| Tested pairs with no claim in the brief | 33 = T3 × 5, T4 × 8, T5 × 2, T7 × 8, T8 × 2, T9 × 8 |

So 39 + 33 = 72 distinct pairs are confirmed. Adding 39 and 72 would double-count.

Claims per target: T1 9, T2 9, T3 1, T4 1, T5 1, T6 9, T7 1, T8 7, T9 1. Tested pairs per target: T1 9, T2 9, T3 6, T4 9, T5 3, T6 9, T7 9, T8 9, T9 9.

**Notation.** The claim column and cylcgt's printed value differ only in notation, never in meaning: ↑² is printed by cylcgt as {0 | ↓\*} and ↑²\* as {0, \* | ↓}; claims.tsv writes `up2`, `up2*` and ASCII `{2+-1|-2+-1}`, cylcgt prints `{2±1 | -2±1}`. This affects exactly 11 of the 39 rows (T5 aware/count, the 9 T6 rows, T8 aware/count). In the sanity run, ↑²\* written as the literal {0, \* | ↓} minus ↑² + \* is 𝓟 in both modes (they are the same game).

## Results

All "outcome" columns below are for G + (−V); 𝓟 means the identity holds.

### Pass 1: claims (`claims.tsv`, `claims_literal_up2star.tsv`)

| Target | Board and position | Claim | Cells | whole / comp |
|---|---|---|---|---|
| 1 | flat `W: a2 a3 b2 / B: a6 b5 b6` | 1/8, all 9 settings | 9 | 𝓟 / 𝓟 |
| 2 | flat `W: a2 b2 b3 / B: a5 a6 b6` | 1/8, all 9 settings | 9 | 𝓟 / 𝓟 |
| 3 | flat `W: a2 b4 c4 / B: a7 b7 d6` | 1/8, aware/count | 1 | 𝓟 / 𝓟 |
| 4 | flat `W: a2 b2 c3 / B: b5 b6 c7` | 1/16, aware/count | 1 | 𝓟 / 𝓟 |
| 5 | flat `W: a2 b2 d4 / B: a7 c6 d7` | ↑², aware/count | 1 | 𝓟 / 𝓟 |
| 6 | flat `W: a2 b2 b6 / B: a6 b7 c5` | ↑²\*, all 9 settings (also literal {0, \* \| ↓}) | 9 (+9) | 𝓟 / 𝓟 |
| 7 | flat `W: a2 b2 b6 / B: a6 b7 c6` | tiny(1), aware/count | 1 | 𝓟 / 𝓟 |
| 8 | flat `W: a2 c2 / B: b7 d7` | \*2 (count, mover) and 0 (opponent) under off and textbook; {2±1 \| −2±1}, aware/count | 7 | 𝓟 / 𝓟 |
| 9 | cyl 3×8 `W: a2 a3 b2 / B: b7 c6 c7` | \*2, aware/count | 1 | 𝓟 / 𝓟 |
| | | **Total** | **39** (+9 literal) | **39 / 39** (+9 / 9) |

### Pass 2: cylcgt's value, per target (`cylcgt.tsv`)

All tested values were 𝓟 in both modes. The value shown is cylcgt's printed form.

| Target | cylcgt's values by setting (count / mover / opponent) |
|---|---|
| 1, 2 | 1/8 in all 9 settings |
| 3 | off, textbook, aware: 1/8 / skipped (BIG) / \* |
| 4 | off: 1/2 / 3/4 / 1/2; textbook and aware: 1/16 / 1/16 / 1/8 |
| 5 | off: all three skipped (BIG); textbook: {0 \| ↓\*} / skipped / skipped; aware: {0 \| ↓\*} / \* / skipped |
| 6 | {0, \* \| ↓} in all 9 settings |
| 7 | off: ↑ in all three races; textbook and aware: tiny(1) in all three races |
| 8 | off and textbook: \*2 / \*2 / 0; aware: {2±1 \| −2±1} / {2±1 \| −2±1} / 0 |
| 9 | off: 0 / 0 / \*2; textbook and aware: \*2 / 0 / \*2 |

Distinct printed values over the 72 tested pairs: 1/8 (23), {0, \* | ↓} (9), \*2 (9), 0 (7), tiny(1) (6), 1/16 (4), \* (4), ↑ (3), {2±1 | −2±1} (2), {0 | ↓\*} (2), 1/2 (2), 3/4 (1).

### Skipped pairs (9, BIG translations)

V_cyl contains the integer 256 (±BIG), so sumsolver's passer handling (a win in "whole" mode, 64 in "comp" mode) would make the test meaningless. These cylcgt values are **not** checked by K5b:

- T3: off/mover, textbook/mover, aware/mover.
- T5: off/count, off/mover, off/opponent, textbook/mover, textbook/opponent, aware/opponent.

For the 72 tested pairs the largest integer chain in V_cyl is 3, so the "comp" shortcut for large integers never came into play.

### Non-𝓟 results

**None.** No claim, and no tested cylcgt value, gave 𝓛, 𝓡 or 𝓝. No cell gave different outcomes in "whole" and "comp" mode (`summary.json`: `claim_non_P`, `cyl_non_P`, `mode_disagreements` are all empty).

### Sanity and controls

- `sanity.txt` (G0 = `W: a4 / B: a5`, no moves for either side, all 9 settings × both modes): 37 PASS, 0 FAIL (26 required, 11 controls). This covers V + (−V) = 𝓟 for every named V (including both ↑²\* forms), 1/8 + 1/8 − 1/4 = 𝓟, ↑² is 𝓛, ↑ − ↑² is 𝓛, tiny(1) is 𝓛, \*2 + \*2 = 𝓟, G + G = 𝓟 for G = {2±1 | −2±1}, and the controls (for example 1/8 − 1/16 is 𝓛, 1/16 − 1/8 is 𝓡, \*2 − \* is 𝓝).
- Recorded, not pass or fail: ↑² − tiny(1) is 𝓛 (so ↑² > tiny(1) here).
- `controls.tsv`: for every target (aware/count) G − V′ was played for 19 decoy values V′. In every row the claimed value is the **only** decoy giving 𝓟 (the other decoys give 𝓛, 𝓡 or 𝓝), so the identities are not vacuous.
- `spotcheck.py` rebuilds five cells and one negative control (T1 against 1/16 gives 𝓛) by hand, stand-alone, without importing `identities.py`: all PASS. The audit adds 20 wrong-setting and wrong-value checks (below).
- The race rule was exercised: the settings in which count, mover and opponent differ (T3, T4, T5, T8, T9) give different cylcgt values, and every tested one is confirmed by the matching setting of sumsolver.

## What "confirmed" does and does not mean

- **CHECKED-2 means:** cylcgt's canonical form (a separate computation, in `cylcgt/cgt.py`) and an exhaustive minimax search over explicit game trees (`sumtest/sumsolver.py`, no canonical forms) agree that G − V is a second-player win.
- sumsolver was written by a Claude model. The check is independent of cylcgt's code but **not** of the model family.
- A shared misreading of the rules (Elkies conventions, passed-pawn and race rules, the e.p. test) in both programs would not be caught. "G = V" is established in sumsolver's rule model.
- The 9 BIG pairs are untested here. Equality is shown only for the finite V built here.
- The time-limit and memory watchdog never fired in the real run (every solve took at most 0.36 s, below its 3 s tick). It is exercised separately by `guardtest.txt`.

## Reproduce

From the project root, one command (about 4.5 minutes; it recomputes everything because it deletes `results.jsonl` first):

    bash kings/delegate/out/K5b/run.sh

It runs these stages one after another, each as one Python process under `nice -n 10` (all with `PYTHONPATH=.` and `.venv/bin/python`), logged to `run.log` with per-stage seconds:

| Stage | Command | Writes |
|---|---|---|
| sanity | `identities.py sanity` | `sanity.txt` (exit 1 stops the script on failure) |
| guardtest | `identities.py guardtest` | `guardtest.txt` |
| run | `identities.py run 40` | `results.jsonl` (162 records: 81 pairs × 2 modes) |
| tables | `identities.py tables` | `claims.tsv`, `claims_literal_up2star.tsv`, `cylcgt.tsv`, `summary.json` |
| controls | `identities.py controls` | `controls.tsv` |
| spotcheck | `spotcheck.py` | `spotcheck.txt` (also appended to `run.log`) |

`time.log` is `/usr/bin/time -l` over the whole of `run.sh` (all stages): 262.12 s real, 136.65 s user, 0.87 s sys; "maximum resident set size" 158,466,048 bytes = 151.1 MiB, the largest single child process. This agrees with the `proc_peak_rss_mb` field of the last record (151.1). Limits met: one Python process at a time, under 3 GB, far under 45 minutes, largest file `results.jsonl` (54 KB).

Where the time goes: sanity (0 s), guardtest (3 s), tables and controls (0 s each) and spotcheck (1 s) are small, and the solver play (sum of `secs` over the 162 records) is about 5 s. Almost everything in the `run` stage (258 s in `run.sh`) is cylcgt evaluating its own values. Measured separately with timers around the calls (a rerun of the same loop into a scratch file, 222.8 s in total): `cylcgt.pawns.value` 216.5 s, solver play 4.2 s, tree conversion, integer scan and `SumSolver` construction about 0 s each. Wall-clock time varies with load on the shared machine.

## Files

`identities.py`, `run.sh`, `spotcheck.py`, `sanity.txt`, `guardtest.txt`, `results.jsonl`, `claims.tsv`, `claims_literal_up2star.tsv`, `cylcgt.tsv`, `controls.tsv`, `summary.json`, `run.log`, `spotcheck.txt`, `time.log`, `audit/` (the auditor's script and output), `REPORT.md`.

`results.jsonl` fields: `target`, `epmode`, `race`, `mode`, `position`, `claim`, `cyl_shown`, `cyl_skip`, `cyl_max_int`, `tree_nodes`, `status`, `secs` (solver play only), `states`, `race_hits`, `proc_peak_rss_mb` (high-water RSS of the process after the solve, in MiB, from `getrusage`, so it never decreases along the file), `outcomes`.

## Audit

An independent auditor re-derived the results with its own script (`audit/audit_k5b.py`, written from the brief and `sumsolver.py` only; it does not import `identities.py`). It builds each V with a string parser on `Trees.node/add/neg`, evaluates the sanity facts with its own lazy-sum evaluator, and re-solves pass 1 and pass 2. Its output is `audit/audit_out.txt`; `audit/audit_out_run1_with_script_bug.txt` is an earlier run that I did not rely on.

**Auditor's independent recomputation (all agree with the tables here):**

- Sanity: 0 discrepancies against `sanity.txt` (its own evaluator agrees with sumsolver on every fact).
- Pass 1: 39 claims, all 𝓟 in both modes; 0 rows differ from `claims.tsv`.
- Wiring and negative checks: 20 checks that a claim fails under the wrong setting or value, 0 failing.
- Pass 2: 81 pairs, 72 tested, 72 𝓟 in both modes, 9 skipped; 0 rows differ from `cylcgt.tsv`; largest integer among tested pairs 3; 0 cylcgt integer tags disagreeing with the structure; the e.p.-off value never changes with the e.p. test.
- After my from-scratch rerun, `claims.tsv`, `claims_literal_up2star.tsv`, `cylcgt.tsv`, `controls.tsv`, `summary.json`, `sanity.txt` and `spotcheck.txt` are **byte-identical** to the versions the auditor checked, and the 162 records of `results.jsonl` agree in every field except the timings.

**Per issue:**

1. **Blocking: `REPORT.md` missing. Verdict: real, fixed (this file).** I confirmed `ls kings/delegate/out/K5b/REPORT.md` failed, and that only the brief and `K5/REVIEW.md` mentioned K5b. This file supplies the 5-line summary, the CHECKED-2 labels, the list of non-𝓟 results (none), the Claude-model caveat and the meaning of "confirmed". Every figure was recomputed: 39/39 claims, 9/9 literal rows, 72/72 tested pairs, 9 skipped, no non-𝓟 result, no "whole" versus "comp" difference. The auditor's recomputation agrees (above). Not done: `kings/delegate/logs/K5b.log` does not exist and I did not create it, because the task allows writing only inside the output directory; `run.log` here is the full stage log.
2. **Minor: REPORT could overstate coverage. Verdict: real, fixed (by wording).** Rechecked with `comm` and `awk` over `claims.tsv` and `cylcgt.tsv`: 39 claim pairs, 72 tested pairs, 39 in both, 0 claim pairs untested or skipped, 33 tested pairs without a claim (T3 5, T4 8, T5 2, T7 8, T8 2, T9 8), 9 skipped. (a) The report now says the 39 claims are among the 72, so there are 72 distinct confirmations, not 111. (b) It says 81 = 72 confirmed + 9 skipped, never "81 of 81". (c) The notation paragraph states that ↑² prints as {0 | ↓\*} and ↑²\* as {0, \* | ↓}, and ASCII `+-` versus ±; exactly 11 of the 39 rows differ in notation only (T5 aware/count, 9 T6 rows, T8 aware/count), as the auditor said.
3. **Minor: `run.sh` does not reproduce from scratch. Verdict: real, fixed; one sub-claim corrected.** Confirmed in the old code: `done_keys()` and `run()` skip finished items and `run.sh` never deleted `results.jsonl`; the old `time.log` named no command; the solver seconds summed to 5.16 s against 243.61 s real. Fixed: `run.sh` now deletes `results.jsonl`, pipes every stage through `tee` into `run.log` (with per-stage seconds), pipes `spotcheck.py` through `tee` into `spotcheck.txt`, and re-executes itself under `/usr/bin/time -l -a -o time.log`, so `time.log` names the covered command (the whole script). I then ran the new `run.sh` completely: it exited 0 in 262.12 s and rebuilt all 162 records. Sub-claim corrected: the auditor guessed that the time was "cylcgt value computation and sanity". Sanity takes under 1 s; the time is cylcgt value computation (216.5 s of 222.8 s measured, see Reproduce).
4. **Minor: `peak_rss_mb` is 0.0 in all 162 records. Verdict: real, fixed.** Confirmed: 162 records, all `peak_rss_mb == 0.0`, maximum solver time 0.27 s against a 3 s watchdog tick. The field is replaced by `proc_peak_rss_mb`, read after each solve with `resource.getrusage(RUSAGE_SELF).ru_maxrss` (bytes on macOS); in the new `results.jsonl` it runs from 23.4 to 151.1 MiB and the last value matches `time.log` (158,466,048 bytes). The watchdog itself now reads the same `getrusage` value instead of spawning `ps`. It still never fires in the real run, so `identities.py guardtest` (new, in `run.sh`) exercises it on a busy loop: an RSS limit forced below the current RSS aborts with `memory`, a 0 s wall-clock limit aborts with `timeout`, and a control with no limit does not abort (all PASS in `guardtest.txt`). The cited peak is `time.log`: 151.1 MiB (the auditor's earlier run gave 161,333,248 bytes, 153.9 MiB; both are about 150 MiB, well under 3 GB).

No issue was rejected outright. The only correction to the auditor is the sub-claim in issue 3 about where the time goes (sanity is negligible).

---

*Saved by the orchestrating session from the fix agent's reply (workflow `wf_b4065698-d8f`), which could not write files itself. Reviewed: table counts recounted (claims 39 yes; cylcgt 72 yes, 9 skipped) and `spotcheck.py` rerun (6 of 6 PASS) on 2026-10-22.*
