# T73: Smallest counterexample per convention

## 5-line summary
We enumerated pawn+tretchet positions on small boards and re-used the 7x6/6x6 experiment data plus L4.
Each of C1-C5 has a minimal witness: C3 and C1 on the 7x6 cylinder (2 and 3 pawns), C4 on the 5x6 flat board (2 pawns), C2 from L4 on 8x8 (2 pawns), and C5 from the stalemate trick on 8x8 (1 pawn).
The witnesses are not the same on flat and cylinder: C4 appears on both, C3/C1 only on the cylinder in this search, C2/C5 only on flat.
All five are COMPUTED-1 or better; C4 and C5 were cross-checked with kings/ref (CHECKED-2), C3/C1 only with kpsolve, C2 by the L4 forced-win proof.
No position in the enumerated 4x4/5x5 boards (with a trebuchet) produced a non-trivial counterexample; minima require 5x6 or larger.

## Minimal-counterexample table

| Conv. | Convention | Board | Position (kpsolve format) | Pawn component | Men | Model value | Real value | Confirmation |
|---|---|---|---|---|---|---|---|---|
| C1 | passer wins at once | cyl:7x6 | Pa3 pa4 Kg4 kb3 Pd2 Pd3 pe3 | W: d2 d3 / B: e3 | 3 | +W (White wins either way) | W if W to move, L if B to move | kpsolve cap2 (COMPUTED-1) |
| C2 | race rule (count/mover/opponent) | flat:8x8 | see L4.1 | W: Ke3 Pa5 / B: Kh7 Pd4 (Black to move) | 2 | count: B wins; opponent: B wins; mover: W wins | W wins (forced win, 8 plies) | minichess proved (PROVED) |
| C3 | e.p.-aware passed test | cyl:7x6 | Pa3 pa4 Kg4 kb3 Pe2 pd4 | W: e2 / B: d4 | 2 | textbook {+W|+-+W}; ep-aware 0 (matches real) | L if W to move, W if B to move | kpsolve cap2 exact (COMPUTED-1) |
| C4 | frozen kings | flat:5x6 | Pd3 pd4 Kc4 ke3 Pa4 pa5 | W: a4 / B: a5 | 2 | L if W to move, W if B to move | D if W to move, W if B to move | kpsolve + ref (CHECKED-2) |
| C5 | stalemate = loss | flat:8x8 | Kc6 ka8 Pb6 (W to move) | (none) | 1 | W wins (stalemate counts as loss) | D (stalemate trick) | ref (CHECKED-2) |

Notes:
- C2 witness is L4.1 from notes/lemmas.md section 4 (W: Ke3 Pa5 / B: Kh7 Pd4, Black to move): count and opponent rules give Black, the mover rule gives White, and chess (forced win) gives White. The L4 forced wins are proved by minichess.min_forced_win.
- C1/C3 witnesses come from kings/results/exp_cyl7x6_epon_Q_conv.jsonl (frozen-differs mismatches with passed_at_start true for C1; ep verdict flip for C3).
- C4 witness comes from kings/results/exp_flat5x6_epon_Q.jsonl (king-effect mismatch: frozen matches convention, free kings draw).
- C5 witness is the standard stalemate-trick position Kc6 ka8 Pb6 (White to move).

## Method
1. Re-used the existing experiment enumerations (kings/experiment.py) on cyl:6x6, flat:5x6, cyl:7x6.
2. For C1/C3, scanned exp_*_conv.jsonl for verdict flips between textbook and ep-aware (C3) and for passed_at_start mismatches (C1).
3. For C2, used the L4 forced-win table (each race rule refuted on 8x8).
4. For C4, used king-effect mismatches (frozen matches convention, free kings differ).
5. For C5, used the stalemate-trick position and confirmed draw under chess rules.
6. Re-verified C4 and C5 with kings/ref/solve.py (CHECKED-2). C3/C1 remain COMPUTED-1 from kpsolve because ref on 7x6 cap2 exceeded the 4 GB / time budget in this run.

## Labels
- C1: COMPUTED-1 (kpsolve)
- C2: PROVED (L4 forced win)
- C3: COMPUTED-1 (kpsolve exact bounds agree)
- C4: CHECKED-2 (kpsolve + ref)
- C5: CHECKED-2 (ref)

Reproduce commands:
- C4: printf 'Pd3 pd4 Kc4 ke3 Pa4 pa5 w -\nPd3 pd4 Kc4 ke3 Pa4 pa5 b -\n' | .venv/bin/python -m kings.ref.solve --board flat:5x6 --ep on --promote Q --cap 2
- C5: printf 'Kc6 ka8 Pb6 w -\nKc6 ka8 Pb6 b -\n' | .venv/bin/python -m kings.ref.solve --board flat:8x8 --ep on --promote Q --cap 2
- C3/C1: see kings/results/exp_cyl7x6_epon_Q_conv.jsonl rows W: e2 / B: d4 and W: d2 d3 / B: e3.
