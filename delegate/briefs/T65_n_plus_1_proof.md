# T65: proof note — a ring *2 with exactly n pawns on every C_n, n >= 10 (whole-board game)

Output directory: `research/ring_n_proof/`. It exists, and holds:
- `logs/`, with the pump runs below;
- `check_N1.py`, a checker written by an earlier attempt at this task, whose M run passed in
  `logs/check_N1_odd.log` (reuse it).

Write nothing anywhere else.

## Background

Game: the whole-board pawn game on the n-file cylinder C_n:
- 8 ranks; files wrap;
- race rule "count"; e.p. on;
- a pawn that can still be taken e.p. is not passed;
- the game ends at the first passed pawn.

Rings are written as per-file tokens, file 0 first: `W5` = a white pawn on rank 5. A ring has a pawn on every file, so
n pawns is the least possible.

Two families (from `research/c9_rings/`, 2026-10-27), both in `research/ring_n_plus_2_proof/fam.py`, one pawn per file:
- **M_n, even n >= 10:** `(B4 W2)^((n-8)/2) B6 W2 W3 B6 B7 W3 B7 W5` (`fam.M`).
- **O_n, odd n >= 11:** `B4 (B7 W5)^((n-9)/2) B7 W3 B7 B6 W3 W2 B6 W2` (`fam.O`). Its wall (B7 W5) is the colour mirror
  of the wall (W2 B4).

What is known:
- rg gives signature NNPN for M_n + *h at every even n = 10..60 and for O_n + *h at every odd n = 11..59.
- O_9 = `B4 B7 W3 B7 B6 W3 W2 B6 W2` is RRRR. On C9 no 9-pawn ring is *2 (exhaustive, two programs).
- `pump_verify.py M 10 40` and `pump_verify.py O 11 41` (logs in `logs/`) give:
  - **M_n, even n >= 12:** 441 nodes, no e.p. flag, zone {n-8..n-3, n-1}. The insertion ins_c (Lemma 3, a 10-file
    arc of unchanged wall files) is an isomorphism from 18->20 on, first at c = 4.
  - **O_n, odd n >= 11:** 2132 nodes, no flag, zone {0} ∪ {n-7..n-1}. The insertion is an isomorphism from 19->21 on,
    first at c = 5.

This is the same structure as the proved families P_n, Q_n, R_n and Qo_n.

## Read first

- `research/ring_n_plus_2_proof/PROOF_odd.md`, the closest template: same lemmas, labels and layout.
- `research/ring_n_plus_2_proof/PROOF.md`, section 2b: the written-out Lemma 3.
- T50's Lemmas 1-3 in `research/ring_family_proof/proof.tex`.
  - T50's Lemma 2 table is written for a W2/B4 wall. For O_n either redo that table for B7/W5 or argue by colour
    reversal (swap colours and rank r -> 9-r; that maps O_n to a ring with a W2/B4 wall and value -*2 = *2). Say which.
- `research/ring_n_plus_2_proof/odd/check_odd.py` and `odd/base_cases.py`.

## What to do

1. **check_N1.py.** Extend `research/ring_n_proof/check_N1.py` to M and O, using the independent engine
   `research/ring_n_plus_2_proof/verify_compute/myeng.py` (program E). For each family choose the base n0 and the cut
   c, and justify them as PROOF_odd.md section 2 does. It must check:
   - the reduced graph (nodes, K/T edges, no flag, zone, signature h = 0..4);
   - every node: no passed pawn, no flag, and the Lemma-3 arc made of exact pattern files;
   - Lemma 2 on every central wall pawn, with its windows, both ends reported;
   - Lemma 3 on every node over two insertion steps;
   - a sensitivity control.
2. **base_N.py.** Direct search (unreduced, no poison pruning) of M_n + *h and O_n + *h, h = 0..4, with E, under both
   e.p.-across-heap readings ("keep", "expire"):
   - every even n = 10..n0-2 for M and every odd n = 11..n0-2 for O (C2 base cases);
   - also up to 25 if it fits in 45 minutes.
3. **A third program.** Repeat the base cases n = 10..14 with `research/c9_rings/codex/engine.py` (written from the rules
   by another model).
4. **PROOF_N.md.** Write it in PROOF_odd.md's format:
   - a 5-line summary;
   - a claims/labels table: PROVED = by hand given the lemmas, CHECKED-2 = two or more programs, COMPUTED-1 = one;
   - hypotheses H1-H7 adapted to M and to O: wall phase and ends, the two arc ends and their windows, start
     position, race rule, invariant, meaning of *2;
   - finite checks with the exact commands and log paths;
   - the proof;
   - a "Gaps and caveats" section that says plainly what is not shown.
   Do not overclaim. If a hypothesis fails, say so and stop there.

## Rules

- Follow `delegate/COMMON.md`.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID. Other projects share this machine.
- At most 2 processes, each under 4 GB RSS, under `nice -n 15`.
- No git. Do not edit `paper/` or any file outside `research/ring_n_proof/`. The families M, O, N1 are already in
  `fam.py` and `pump_verify.py`; do not change those files.
