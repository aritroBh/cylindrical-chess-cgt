# K28: the five open chess deviations of Z_B (flat 7x6)

## Summary

1. Rows 1-4 are decided exactly: row 1 = W, row 2 = L, row 3 = L, row 4 = W (White's view, cap-2 bounds A = B, so
   the value is exact). Each loses for the side that played it.
2. **Row 5 is a DRAW, exactly (D).** After Kc3-d2 from (c3, b5) Black cannot win: every Black move leads to D except
   c4-c3, which loses. So Kd2 does not lose for White.
3. Hence **Z_B is NOT exactly two-shuttle in chess.** 25 of the 26 non-shuttle moves lose; Kc3-d2 (White, root (c3, b5))
   draws. (The mirror group follows by the tau symmetry, colours exchanged, with the bounds swapped.)
4. Two independent solvers agree on every row (kpsolve, kq3 written from SPEC.md, and for cap 1 plus capture refinement
   the K27 referee's ownchess extended as `ownref`). All five values are CHECKED-2; none is PROVED by hand.
5. Brief correction: the sentence "rows 1, 3, 5 are Black wins, rows 2, 4 White wins" is wrong for rows 1 and 2. Row 1 is
   Black's move c4-c3, so it must be a White win; row 2 is White's a3-a4, so it must be a Black win. The test used is the
   one stated first, "each loses for the side that played it" (checked by `scripts/rows_check.py`, which finds the mover).

## Table (values from White's view: W / D / L)

| row | deviation (mover) | child | value | method | label |
|---|---|---|---|---|---|
| 1 | c4-c3 from Kb2/ka4 (Black) | `Kb2 Pa3 Pb4 ka4 pb3 pc3 w -` | **W** (Black's push loses) | child --Kxc3--> `Kc3 Pa3 Pb4 ka4 pb3 b -`, exact W at cap 2 (kp and kq3); W is the best White can get, so the child is W. ownref cap 1 + refine: (W, W) | CHECKED-2 |
| 2 | a3-a4 from Kc3/kb5 (White) | `Kc3 Pa4 Pb4 kb5 pb3 pc4 b -` | **L** (White's push loses) | child --Kxa4--> `Kc3 Pb4 ka4 pb3 pc4 w -`, exact L at cap 2 (kp and kq3); a Black win is the best for Black. ownref cap 1 + refine: (L, L) | CHECKED-2 |
| 3 | Kc3xc4 from Kc3/ka4 (White) | `Kc4 Pa3 Pb4 ka4 pb3 b -` | **L** | direct, cap 2: kp (L, L), kq3 (L, L), kq3 with Black restricted to one queen, bound A: L; ownref cap 1 + refine: (L, L) | CHECKED-2 |
| 4 | Ka4xa3 from Kc3/ka4 (Black) | `Kc3 Pb4 ka3 pb3 pc4 w -` | **W** | direct, cap 2: kp (W, W), kq3 (W, W), kq3 with White restricted to one queen, bound B: W; ownref cap 1 + refine: (W, W) | CHECKED-2 |
| 5 | Kc3-d2 from Kc3/kb5 (White) | `Kd2 Pa3 Pb4 kb5 pb3 pc4 b -` | **D** (so Kd2 does not lose) | cap 2, 4 pawns: kq3 (D, D) full; kp28 (kpsolve + per-colour caps) with White restricted to one queen, bound B: D (a lower bound); kq3 same restricted run, B: D, and with Black restricted, A: D (an upper bound); ownref cap 1 + refine: A = D and B = D | CHECKED-2 |

"Exact" means: the cap-2 solve gives bound A (a capped third promotion is a White win) and bound B (a Black win) with
A = B; the true value lies between, so it equals both. For rows 1-2 the exactness is that of the grandchild and of the
move choice (one winning reply settles the child: a win for the side to move cannot be improved).

Moves after Kd2 (row 5, Black to move; value after the move, White's view): Kb5-a4 D, Kb5-a6 D, Kb5-b6 D, Kb5-c6 D,
b3-b2 D, c4-c3 W. Every Black move that does not lose draws, so Black has no win. Children of the draws (`R5_kids_kq3`):
Kd2 vs kc6/kb6/ka6 (pb3 pc4, White to move) D; vs ka4 D; b2 D; the pc3 child W.

## Verdict

**Z_B is not exactly two-shuttle in chess.** The deviation Kc3-d2 from (c3, b5) draws (exact D at cap 2), so it does not
lose for White; the other four open deviations lose for their mover. (Z_B remains exactly two-shuttle in P, PROVED, and
21 + 4 = 25 of its 26 deviations lose in chess.) The mirror group: LOOPY states that tau (rank flip, colour swap) is a symmetry of chess on the flat 7x6 board and exchanges
the two bounds, so the mirror's Kd2 image draws too (by symmetry, not recomputed). What the draw does to chess contexts
is not examined here.

## Solvers, validation, what was reused

- `kp` = `kings/kpsolve.c` (cc -O2 ... -lpthread). `kp28` = kpsolve plus an 84-line patch (per-colour cap and promotion
  set; diff in `verify/kp28.diff`, source `work/kp28.c`). With the new options at their defaults it equals kpsolve.
- `kq3` = `kq3.cpp`, my own layered retrograde solver written from SPEC.md (no code from kpsolve), no en passant and no
  double step (aborts if a pawn stands on its second rank; it never did), options --cap, --capw, --capb, --promw, --promb,
  --bound A|B|AB, --refine, --moves.
- `ownref` = `ownref.cpp` = K27 referee's `ownchess.cpp` + `--refine` (argv[4]=1); with 0 it is ownchess unchanged.
- `--refine` (capture refinement): a capped promotion by the side that the bound favours is not scored at once; it is
  scored as the value for the opponent after his best capture of the new piece. Sound only for that side (White in A,
  Black in B); it only tightens A down and B up, so A >= true >= B still holds.
- Reused from the killed attempt, after audit: `kq.cpp` (became `kq3.cpp`), `scripts/` (hrun.sh, watch2.sh,
  layers_pc.py, gen_rand.py), `logs/val1, val2` inputs, `work/kp28.c` + `verify/kp28.diff`. All binaries rebuilt from
  source; a rebuild now is byte-identical to the ones used (`cmp`), for kp, kp28, kq3, ownref, ownchess.
- Validation (`python3 -I scripts/cmp_solvers.py A.out B.out --moves`):
  - kp vs kq3, cap 1, 120 positions (<= 1 officer incl. promotions): 0 (A, B) and 0 per-move differences.
  - kp vs kq3, cap 2, 28 positions exact at cap 2: 0 differences; kq3 with --refine equals kp there too.
  - kp28 vs kq3 in the restricted mode (one White queen, cap 2), the same 28 positions: 0 differences (incl. moves).
  - ownchess/ownref vs kp (bounds A and B separately), cap 1: 113 positions, 0 differences; ownref refine vs kq3 refine: 0.
  - the five children, cap 1, kp vs kq3: identical (W, L) x4 and (D, L); with --refine all five become exact:
    W, L, L, W, D, and ownref + refine gives the same five.
  - F4 (four 3-pawn positions behind rows 1-4) at cap 2: kp (`logs/E`) and kq3 (`logs/D`) agree on bounds and every move.
  - row 5 at cap 2: kq3 full (D, D); kp28 restricted to one White queen (B' = D) agrees with kq3 in the same mode.
- Resources (all under 3 GB RSS, nice 15, through heavy.sh, under watch2.sh): F4 kp cap 2: 3,710 s, 1.58 GB;
  F4 kq3 cap 2: 402 s, 0.54 GB; row 5 kq3 cap 2: 1,308 s, 1.94 GB (5.59e9 slots); row 5 kp28 restricted: 1,426 s, 1.88 GB.
  No run was stopped by the watchdog. No pkill, no git, no network, no file over 50 MB. PIDs in `pids.log` (all exited).

## Reproduce

Build (from `kings/delegate/out/K28`, `mkdir -p bin`):

    cc  -O2 -o bin/kp   ../../../kpsolve.c -lpthread
    cc  -O2 -o bin/kp28 work/kp28.c -lpthread
    c++ -O2 -std=c++17 -pthread -o bin/kq3 kq3.cpp
    c++ -O2 -std=c++17 -o bin/ownref ownref.cpp
    c++ -O2 -std=c++17 -o bin/ownchess ../K27/verify/ownchess.cpp

Inputs: `logs/children5.in` (the five children), `logs/rowsF.in` (four 3-pawn positions), `logs/r5.in` (row 5 child),
`logs/test_cap1.in`, `logs/test_exact2.in`. Every command below is wrapped as in the scripts, i.e.
`../../heavy.sh /bin/zsh scripts/watch2.sh PIDFILE 3000000 WALL_S CMD < IN > OUT 2> ERR`.

    scripts/rows_check.py                       # the five moves from the Z_B roots give the five children; reductions; who moves
    bin/kp  --board flat:7x6 --ep on --promote QRBN --cap 1 --moves < logs/children5.in            # cap 1: (W,L) x4, (D,L)
    bin/kq3 --cap 1 --bound AB --refine --moves < logs/children5.in                                 # exact: W L L W D
    bin/ownref 7 6 {0,1} {0,1} < logs/children5.in                                                  # bound, refine
    bin/kp  --board flat:7x6 --ep on --promote QRBN --cap 2 --threads 2 --moves < logs/rowsF.in     # rows 3, 4 + grandchildren of 1, 2
    bin/kq3 --cap 2 --bound AB --moves --threads 3 < logs/rowsF.in
    bin/kq3 --cap 2 --capw 1 --capb 1 --promb Q --bound A --refine --moves --threads 3 < logs/rows_L.in   # restricted check, L rows
    bin/kq3 --cap 2 --capw 1 --capb 1 --promw Q --bound B --refine --moves --threads 3 < logs/rows_W.in   # restricted check, W rows
    bin/kq3 --cap 2 --bound AB --moves --threads 3 < logs/r5.in                                     # row 5: D D
    bin/kp28 --board flat:7x6 --ep on --promote QRBN --promw Q --capw 1 --cap 2 --threads 3 --moves < logs/r5.in   # B' = D
    bin/kq3 --cap 2 --capb 1 --promb Q --bound A --refine --moves --threads 3 < logs/r5.in          # A' = D
    bin/kq3 --cap 2 --capw 1 --promw Q --bound B --moves --threads 3 < logs/r5.in                   # B' = D

Outputs: `logs/val`, `logs/D`, `logs/E`, `logs/rows`, `logs/r5`, `logs/r`; comparison `scripts/cmp_solvers.py`, `scripts/cmp_own.py`.

Not done: a hand proof of row 5 (a drawing plan for White after Kd2). Not needed for the verdict but it would raise the
label to PROVED. Eight roots: only the (c3, b5) root's Kd2 is affected; the other roots' deviations were not re-run.
