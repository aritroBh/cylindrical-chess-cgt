# VERIFY (referee for K19), 2026-10-27

Verdict: **ACCEPT_WITH_FIXES.** Every number and both counterexamples reproduce with my own code and my own kpsolve builds.
Five of the 18 EDIT blocks need a fix (one has a false statement, one an unqualified number, one an unsupported
gloss, two an overstated source; one of the two also carries a label that can be raised), and one block is missing. Corrected blocks:
`verify/EDITS_FIXED.md` (5 corrected blocks and 1 new block; with K19's other 13 blocks all 19 apply in sequence to the current LOOPY.md).

## What I used (none of K19's scripts for the numbers)
- `verify/lg.py`: my own local game of Definition 2.6 (own move generator, e.p., cylinder/flat, pass budget k or infinity,
  queen clause, mate rule and confinement as switches), written from the LOOPY text. `verify/l3.py`: (L3) as "exists a guided
  strategy such that the real s (no passes) is never stalemated". Drivers: `ref51*.py`, `ref52.py`, `ref55*.py`, `ref56.py`, `cmpP.py`.
- Private builds `cc -O2 -o kp kings/kpsolve.c -lpthread` and `kp_p` from K7's `kp_p.c` (deleted at the end).
  Note kp_p is kpsolve.c with a PMODEL flag, so kp_p and kpsolve are not independent of each other.
- K19's own code was only used to check that its `xcheck_p.py` claim holds (below).

## Claims

| # | Claim | Result | Evidence (my code) |
|---|---|---|---|
| 1 | 5.1 (L1), K7 rules, T = 6,6,6,7,7 (queen) and 6,6,5,6,6 (L1_P) | **CONFIRMED** (CHECKED-2 is right) | `lg.py`, `ref51.py`: White sorties `[6,6,6,7,7]` / `[6,6,5,6,6]`; Black sorties `[7,7,6,6,6]` / `[6,6,5,6,6]` for a3,b3,c3,c4,c5 (the mirror) |
| 2 | pre-K7 rules, k = 0..8 and inf, T in 5..7, k = 5,6 equal inf | **CONFIRMED** | `ref51b.py 0`, `ref51b.py 1` (no mate rule), `ref51c.py` (unconfined): every row constant 6,6,6,7,7 for k >= 0, except Ka6 with k = 0: 5 (then 7 for k = 1..9 and inf), as K19 reports. k >= 7 equals inf: the argument is valid (at most T <= 7 moves of s in the window). The scratch run covered only k <= 4 and inf, so k = 5, 6, 8 rest on K19 and on me |
| 3 | (L3) holds for ten sorties at T, T+1, T+2, both clause settings (COMPUTED-1) | **CONFIRMED**, and now a second implementation exists | `l3.py`: all 60 values True. The label COMPUTED-1 is not too strong, it is now too weak |
| 4 | Black's legal moves Ka3,Kb3,Kc3,Kc4,Kc5; Kb5 illegal | **CONFIRMED** | `kp --moves` lists exactly `Kb4b3 Kb4c4 Kb4c5 Kb4c3 Kb4a3`, all W; `Kh5 Pa4 kb5 pa5 w` is X (illegal) in kp and kp_p. Also `notes/diagram_audit.md` §C.3 has the correct list (see Problem 1) |
| 5 | P6 = (L, W) in P and C; all ten sorties lose | **CONFIRMED** | kp (chess) and kp_p (P) on cyl:8x8: bare `w` L, `b` W; five White sorties (b) L; five Black sorties (w) W. P model shares code with kp, so "two solvers" = K19's own solver + kp_p. K19's own solver I did not re-run; instead `cmpP.py` (my local game with k = 0, unconfined, no queen clause) agrees with kp_p on 15 positions of 5.1, 5.2, 5.5, 5.6 and the analogue |
| 6 | 5.2: Kd5, Ke5, Kf5 not punished; only Kf7 loses (T = 10) | **CONFIRMED** | `ref52.py`: after Kxd7 no win up to T = 13 for all 8 variants (queen or not, confined or not, k = 0 or inf); Kf7: T = 10 (queen k = 0), 11 (queen k = inf), 10 (no queen, both). kp and kp_p on cyl:8x8 and flat:8x8: Kd5, Ke5, Kf5 = D, Kf7 = L, bare `w` D, `b` W. Analogue cyl:7x6: Kb3, Kc3, Kd3 = D, Kd5 = L (T = 6; `ref52.py`) |
| 7 | P5 bare w = D, P7 w = D, Z_72 + Hp1 = (W,W) | **CONFIRMED** | kp, kp_p on cyl:7x6 (bare: D / W; Hp1: W W in chess; the P value of Hp1 I did not re-run) and cyl:8x8, flat:8x8 |
| 8 | 5.5 Black's moves Kc5,Kd3,Kd4,Kd5; Kc3 illegal; kc5 D, others W | **CONFIRMED** | kp --moves and kp_p --moves on cyl:8x6 |
| 9 | 5.5 local game: Kc5 no win; Kd3 T = 5 for all budgets | **CONFIRMED** | `ref55.py q`, `ref55.py p`, `ref55u.py` (unconfined): c5 None for k = 0,..,6,8,inf (bounded: T <= 20 confined, <= 12 unconfined); d3 = 5 everywhere |
| 10 | Kd4, Kd5: T = 6 + k (queen), none for unlimited passes | **CONFIRMED for the queen clause; the number is different without it** | queen: `[6,7,8,9,10,11,12,14,None]` for k = 0..6,8,inf; no queen clause (L1_P): `[6,6,7,8,9,10,11,13,None]`, that is 5 + k for k >= 1. "None" is bounded evidence (T <= 20 confined, 12 unconfined), K19 reports an unbounded fixed point |
| 11 | 5.6 mu_W = 5, T = 5 for every budget, (L2) fails by one tempo | **CONFIRMED** | `ref56.py`: T = 5 for k = 0,1,2,3,4,inf in all four variants (queen or not, confined or not); BFS mu_W = 5 (also trivial: c3 to c8 is 5 pushes) |
| 12 | kp_p: `Ke6 Pg4 Pc3 kh4 pg5 pd6 b -` is L (COMPUTED-1) | **CONFIRMED, one implementation** | kp_p on flat:8x8: `L`, and `Pc3c4:W` is White's only winning move from `Kf5 ... w`, which agrees with engine/suite/README.md line 190 ("The model says Ke6 loses"). The chess value (kpsolve) I did not obtain: the heavy run never got a slot. The README's tablebase draw supplies it |
| counter 1 | 5.1 Kb5 illegal, Kb3 missing | **REPRODUCES** | as claim 4 |
| counter 2 | 5.5 "only if Black has no spare move" too strong | **REPRODUCES** | as claim 10 |

Also checked: K19's `xcheck_p.py` (350 positions, own P solver vs kp_p): I re-ran a copy, **0 mismatches** (its log was not saved in K19/logs). `xcheck_local.log` and `xcheck_movegen.log` are saved and say 110 / 980 with 0 mismatches; I did not re-run them.

## Proof steps
K19 proves nothing new; the only argument is "k >= 7 equals inf because the window holds at most T <= 7 moves of s". It is valid for k >= T(inf) (each of the T moves of s, passes included, is available), and the computed T(inf) <= 7.

## Problems with the EDITS

1. **5.1-black-moves (false statement).** The NEW text says "The agreement with `notes/diagram_audit.md` §C.3 claimed earlier refers to the earlier list; K19 did not re-read the audit." The audit's §C.3 table lists Black's moves as `a3, b3, c3, c4, c5` (the correct list), and Appendix A (LOOPY line 2001) says the scratch run reproduced the audit's lists. So the Kb5 error is a transcription slip in §5.1, not a list that the audit and scratch shared. Fixed in `EDITS_FIXED.md`. (The §5 intro, "its lists for 5.1, 7.2 and 7.3 agree with the audit", is then true of the audit and false of the §5.1 text as it stood; K19's edit fixes the text.)
2. **status-5.5 (number without qualifier).** "T = 6 + k" holds with the queen clause only; without it T = 6 (k = 0), 5 + k (k >= 1). Fixed.
3. **5.5-escape (unsupported gloss).** "nevertheless punished in P and in C, because the real supply is finite" is not what was computed. What is computed: k = 0 (bare group) T = 6, and T = 6 + k for a budget k. Reworded.
4. **5.1-L1-bullet and status-5.1-L1 (source overstated).** They say "the scratch run and K19's code agree" for every k = 0..8, but the scratch run stopped at k = 4 and inf, and the same edit says k = 5, 6 were never checked. The numbers for k = 5, 6, 8 rest on K19 and on this referee. Reworded; CHECKED-2 is justified by those two implementations.
5. **(L3) label.** COMPUTED-1 is correct for K19 alone; with `l3.py` it is CHECKED-2. Raised in the corrected status and bullet blocks (the project may keep COMPUTED-1 if it does not count a referee run).
6. **Labels paragraph.** LOOPY lines 120-121 say a claim supported only by a kpsolve run keeps CONJECTURE. With the new labels that sentence conflicts with COMPUTED-1 and CHECKED-2. New block `labels-kpsolve` adds the missing clause, including that a build derived from the same source (kp_p from kpsolve.c) does not count as independent.

Everything else: for each of the 18 K19 blocks OLD occurs exactly once in the current LOOPY.md and the blocks do not overlap (`verify/check_edits.py`). NEW texts for labels-checked2, status-5.2, status-5.6, status-P5, status-P6P7, 5.1-K7-sub, 5.1-prediction, 5.2-not-punished, 5.6-T-mu, 6-P5, 6-P6, 6-P7 and appendix-K19 are accurate against the numbers above. The appendix bullet begins at column 0 and so is a sibling of "K7 checks", as it should be. One thing I could not verify: appendix-K19's "written without reading kings/ref/ or the K7 scripts" (the file header of `k19engine.py` says so; nothing in the file contradicts it).

## Labels, summary
No label was stronger than the evidence, except that the wording of problem 4 hid which implementations stood behind k = 5, 6, 8. Claims 1-2, 4-11 are CHECKED-2 (two implementations agree), claim 3 is COMPUTED-1 (CHECKED-2 now), claim 12 is COMPUTED-1.

## Process notes (shared-machine rules)
- Slips: `ref52.py` ran about 6.5 minutes (about 3 CPU-minutes, up to 2.2 GB RSS; under the 3 GB cap) without the heavy lock, because I misjudged its cost; the first `ref51b.py` timed out and was stopped; one `kp --board cyl:7x6` chess run (37 CPU-s) ran without the lock. The three heavy.sh wrappers that never got a slot were killed by PID. No pattern kills, no git, no edit outside K19/VERIFY.md and K19/verify/. Binaries and bulk batches deleted; `verify/` keeps scripts, small inputs and logs.
- Reproduce: `cd kings/delegate/out/K19/verify && PYTHONPATH=<repo> <repo>/.venv/bin/python ref51.py` (17 s), `l3.py` (about 30 s), `ref51b.py 0|1`, `ref51c.py`, `ref55.py q|p`, `ref55u.py`, `ref56.py`; `ref52.py` and `cmpP.py` take minutes (use `heavy.sh`). kp lines: `kp --board cyl:8x8 --ep on --promote QRBN --cap 1 --moves < verify/in52.txt` (and `in51.txt`, `in55.txt` with `--board cyl:8x6`, `inP5.txt`, `inhp1.txt` with `cyl:7x6`, `in56.txt` with `flat:8x8` and `kp_p ... --pmodel`).
