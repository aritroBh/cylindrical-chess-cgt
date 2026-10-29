# K28 referee report

## Verdict: ACCEPT_WITH_FIXES

All five values reproduce. The conclusion stands: **Z_B is not exactly two-shuttle in chess**, because Kc3-d2 from (c3, b5)
draws (child exactly D at cap 2). The fixes are to the proposed LOOPY edits only: two places that still say "chess open"
were not covered (the §3 table row P3.2' on line 89 and the §8 item 2 sentence), and two sentences overclaim a little
(see "Problems"). Replacement edits: `verify/EDITS.md` (7 edits; every OLD text occurs exactly once in the current LOOPY.md,
re-checked after LOOPY changed under us at 23:40).

## Claim table (values from White's view; mover in brackets)

| row | claim | my re-run | independent check | label |
|---|---|---|---|---|
| 1 c4-c3 (B) child `Kb2 Pa3 Pb4 ka4 pb3 pc3 w -` | W (Black's push loses) | kp cap 1 (W,L); kq3 cap 1 +refine (W,W); ownref cap 1 +refine (W,W); kq3 cap 2 of grandchild `Kc3 Pa3 Pb4 ka4 pb3 b -` after Kxc3 = (W,W) | kp cap 2 on the grandchild: investigator's log `logs/E` (W,W), not re-run | CHECKED-2 (agree) |
| 2 a3-a4 (W) child `Kc3 Pa4 Pb4 kb5 pb3 pc4 b -` | L (White's push loses) | kp cap 1 (W,L); kq3 +refine (L,L); ownref +refine (L,L); kq3 cap 2 of grandchild `Kc3 Pb4 ka4 pb3 pc4 w -` after Kxa4 = (L,L) | as row 1 | CHECKED-2 |
| 3 Kxc4 (W) `Kc4 Pa3 Pb4 ka4 pb3 b -` | L | kp cap 1 (W,L); kq3 cap 2 (L,L), moves Ka4a3 W, Pb3b2 L; kq3 cap 1 +refine (L,L); ownref +refine (L,L) | kp cap 2 (L,L) in investigator's `logs/E`, not re-run | CHECKED-2 |
| 4 Kxa3 (B) `Kc3 Pb4 ka3 pb3 pc4 w -` | W | kp cap 1 (W,L); kq3 cap 2 (W,W), only winning move Pb4b5; kq3 +refine (W,W); ownref +refine (W,W) | kp cap 2 (W,W) in `logs/E`, not re-run | CHECKED-2 |
| 5 Kd2 (W) `Kd2 Pa3 Pb4 kb5 pb3 pc4 b -` | D exactly; Kd2 does not lose | kp cap 1 (D,L); kq3 cap 2 full (D,D), 1,914 layers, 5.59e9 slots, 431 s, 1.83 GB; kp28 (kpsolve + per-colour cap, White limited to one queen, cap 2) (D,D) i.e. lower bound D; kq3 +refine cap 1 (D,D); ownref +refine (D,D) | upper bound D also from kq3/ownref (different code from kp28); Black's moves Kb5-a4/a6/b6/c6 and b3-b2 are D, c4-c3 loses (W) | CHECKED-2 (no hand proof) |
| Count | 25 of 26 deviations lose, 1 draws (6 + 15 from K27/integrator, + 4 here) | not re-run (K27 items) | | CHECKED-2 |
| Brief correction | the brief's "rows 1, 3, 5 Black wins; 2, 4 White wins" is wrong for rows 1 and 2 | `scripts/rows_check.py` of K28: the five moves from the Z_B roots give the five children, mover as stated (row 1 and 4 Black moves, rows 2, 3, 5 White moves) | I agree: "loses for the mover" is the consistent test | PROVED (by reading the table) |
| Edits | OLD texts occur once | 5 of 5 original, 7 of 7 replacement | | checked |

Unrefined cap-1 bounds (ownchess, the K27 referee's solver, unchanged): bound A: rows 1-4 W, row 5 D;
bound B: all L. So ownchess and kpsolve give the same (W,L) x4 and (D,L), and the refinement is what closes the gap.

## What I ran (all through heavy.sh, nice 15, watch2.sh, under 3 GB)

Build (in `verify/`): kp from `kings/kpsolve.c`, kp28 from K28's `work/kp28.c`, kq3 from `kq3.cpp`, ownref from `ownref.cpp`,
ownchess from K27's `verify/ownchess.cpp`; sources copied to `verify/`.

    scripts/chainA.sh : kp cap 1 --moves on children5 ; kq3 --cap 1 --bound AB --refine --moves ; ownref 7 6 {0,1} {0,1} ;
                        kq3 --cap 2 --bound AB --moves --threads 3 < r5.in ; kp28 ... --promw Q --capw 1 --cap 2 --threads 3 --moves < r5.in
    scripts/chainB.sh : kq3 --cap 2 --bound AB --moves --threads 3 < rowsF.in   (the kp cap-2 run on rows 3, 4 was not started, see below)
    python3 -I scripts/rows_check.py  (in the investigator's directory)

Outputs in `verify/logs/r/*.out`. Peak RSS: kq3 row 5 1.83 GB, kp28 row 5 below 3 GB (no watchdog stop), others below 0.6 GB.
Results are identical to the investigator's logs line for line (`logs/D`, `logs/r`).

## Audit of the method

- `kq3` has no en passant and no double step. That is sound here: White pawns on a3, b4 and Black pawns on b3, c4 are never on their
  second rank, pawns never move backwards, so neither can arise.
- Cap semantics: capped promotion = win for White in A, for Black in B (SPEC). A = B at cap 2 for the children, so exact.
- Capture refinement (`--refine`, in kq3 and ownref): a capped promotion by the colour that the bound favours is scored as the value
  after the opponent's best capture of the new piece (no capture available means the generous value). I checked the argument:
  the true value after the promotion is at most (for the promoter) the value after any capture the opponent has, so A only
  goes down and B only up. Sound. ownref with refine = 0 is ownchess unchanged (diff read: only the `REFINE` branches).
- Reduction for rows 1 and 2: the child is a one-move win for the side that replies (Kxc3 resp. Kxa4) to a grandchild of exact
  value; a win for the side to move cannot be improved, so the child has that value. Correct.
- Restricted runs: limiting White's promotions gives a lower bound for White's value and limiting Black's an upper bound; the
  investigator used them in the right direction.

## Problems (fixes are in `verify/EDITS.md`)

1. LOOPY has two more statements that the edits leave saying "open": the P3.2' row of the §3 table (line 89: "In chess Z_B is OPEN ...
   cap 2 was not run") and §8 item 2 (line 3123: "five are not settled ... cap 2 not run"). Both added as edits.
2. Edit "cap 2 now run" called K27's "over 20 GB for the 4-pawn children" estimate "refuted by measurement". Only kq3 on one 4-pawn
   child was measured (1.94 GB); K27's estimate was for kpsolve, which was not run unrestricted on a 4-pawn child. Reworded.
3. Edit "five open deviations" said kpsolve and kq3 agree "on bounds and on every move" at cap 2; that holds for the 3-pawn positions.
   For row 5 kpsolve ran only in the restricted mode (lower bound). Reworded.
4. Not an error but worth knowing: the draw rests on solvers (kq3, kq3 +refine, ownref +refine, kp28 restricted); there is no hand proof,
   so CHECKED-2 is the right label, not PROVED. The "mirror group" draw is by tau symmetry, not recomputed; correctly stated.
5. FINDINGS.md says "kp (L, L)" etc. for the cap-2 3-pawn rows; I did not re-run those kpsolve cap-2 runs (see below), I read the logs.

## Limits of this check

- The shared heavy.sh queue (about 15 waiting jobs from other items) kept my jobs waiting for slots for about four hours. I re-ran
  everything except kpsolve cap 2 on the four 3-pawn positions (3,710 s in the investigator's log): the kq3 cap-2 re-run and the
  ownref cap-1 refined solver cover those rows with two independent implementations, but the third (kpsolve cap 2) is the
  investigator's log only. Rows 3 and 4 therefore have two re-run implementations, not three.
- Nothing independent of all three solvers (a hand line) was produced for rows 1-5. I did not attempt a hand proof of the draw.
- I stopped my own chainB script (PID 99160, recorded in `pids.log`) before it queued the kp cap-2 run. No pkill or pattern kill;
  no git; no network.
- Cleanup: the five binaries in `verify/bin/` (about 0.4 MB) could not be deleted: the safety check refused `rm` of the glob, so
  they remain. The directory is 760 KB; no bulk output or cache was written.
