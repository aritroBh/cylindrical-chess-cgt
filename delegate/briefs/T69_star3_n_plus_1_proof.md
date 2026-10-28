# T69: proof note — a ring *3 with n+1 pawns on every C_n, n >= 12 (whole-board game)

Output directory: `research/star3_proof/`. It exists and holds `logs/` with the two pump runs below. Write nothing
anywhere else.

## Background

Game, notation and method are exactly those of `research/ring_n_proof/PROOF_N.md` (read it first; it is the template,
and its referee report `research/ring_n_check_logic/REPORT.md` lists the mistakes to avoid). The difference: these
rings are *3, not *2, so the signature of G + *h for h = 0..5 must be NNNPNN (P exactly at h = 3).

Two families, both in `research/ring_n_plus_2_proof/fam.py` (`fam.T3`, `fam.S3`), with n+1 pawns (one file holds two):
- **T_n, even n >= 12:** `(B4 W2)^((n-10)/2) B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2`. Wall: files 0..n-11.
- **S_n, odd n >= 13:** `B4 B6 W3 (W2 B4)^((n-11)/2) W6B7 W3 B7 B6 W3 W2 B6 W2`. Wall: files 3..n-9.

What is known:
- rg gives NNNP for every even n = 12..58 (T) and every odd n = 13..59 (S): `research/c9_rings/star3/res_fam3_even.tsv`,
  `res_fam3_odd.tsv`. The n = 10 (T) and n = 11 (S) members are not *3.
- Two non-Claude solvers give NNNPNN for T at n = 12, 14 and S at n = 13, 15:
  `research/c9_rings/npawn/cross_check_T3.out`, `cross_check_S3.out`.
- `pump_verify.py T3 12 40` (`logs/pump_T3_12_40.txt`): 1305 nodes for every n, no e.p. flag, zone
  {n-10, n-9, n-7..n-2}; insertion isomorphism from 20 -> 22 on, first at c = 4.
- `pump_verify.py S3 13 41` (`logs/pump_S3_13_41.txt`): 40445 nodes from n = 19 on (33715, 45997, 42527 at
  n = 13, 15, 17), no flag, zone {0, 1, 2, n-10, n-9, n-7..n-1}; insertion isomorphism from 25 -> 27 on, first at c = 7.
  Note that S's zone reaches into the wall (files n-10, n-9), so the unchanged wall is files 3..n-11.

## What to do

1. **check_S3T3.py.** Adapt `research/ring_n_proof/check_N1.py` to T3 and S3 with the independent engine
   `research/ring_n_plus_2_proof/verify_compute/myeng.py` (program E). Choose one fixed cut c and base n0 per family
   and justify them (for which n does the arc c-4..c+5 lie inside the unchanged wall?). Check the reduced graph
   (nodes, K/T edges, no flag, zone, signature h = 0..5), every node (no passer, no flag, the arc made of exact pattern
   files), Lemma 2 on every central wall pawn with its windows, Lemma 3 on every node over two insertion steps, and a
   sensitivity control.
2. **base_S3T3.py.** Direct search (unreduced) of G + *h, h = 0..5, with E under both e.p.-across-heap readings, for
   every n of each family from its least member up to n0 - 2, and as far beyond as fits in 45 minutes.
3. **A third program.** Repeat the smallest base cases (T: n = 12, 14; S: n = 13, 15) with
   `research/c9_rings/codex/engine.py`.
4. **PROOF_S3T3.md**, in PROOF_N.md's format: 5-line summary; claims/labels table (PROVED by hand given the lemmas,
   CHECKED-2, COMPUTED-1); hypotheses H1-H7 for T and S, including the wall phase and ends, the two arc ends and their
   windows written out in full (no unfinished sentences), and the meaning of *3 (signature NNNPNN; for h >= 6 the heap
   move to G + *3 gives N); finite checks with exact commands and log paths; the proof; "Gaps and caveats". Do not
   overclaim. If a hypothesis fails, say so and stop there.

## Rules

- Follow `delegate/COMMON.md`.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID. Other projects share this machine.
- At most 2 processes, each under 4 GB RSS, under `nice -n 15`.
- No git. Do not edit `paper/` or any file outside `research/star3_proof/`. Do not change `fam.py` or `pump_verify.py`.
