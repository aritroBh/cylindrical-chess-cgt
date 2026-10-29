## 5. The search

### 5.1 Ranges that ran

Every placement of both kings (on the files a..F) and of at most w White and b Black pawns on the files a..F, ranks 2..H−1, was classified (section 2.1), twice: with root passers excluded (the brief's filter: "strict") and allowed. A pawn count "w+b" means every placement with at most w White and at most b Black pawns (so ≤ 3+3 contains ≤ 3+2 and ≤ 2+3; the colour-and-rank flip of the board maps 2+3 to 3+2). Source: `fin2/runs/*.json` (own re-run, rebuilt binary) or, where marked "earlier", the earlier attempt's output of the same source (byte-identical binary).

@@SEARCH_TABLE@@

How to read the table.
- Reading A (passes) is the meaningful one for on, off, dud, over and under; reading B (plain P) is meaningful for frozen and dud (section 3).
- "dud roots (groups)": the number of roots labelled dud and, in brackets, the number of different closures (distinct groups before the symmetry reduction of section 6).
- **over and under: 0 in every row.**
- The tempo-signature census (below) is independent of the structural classifier.

### 5.2 What was asked, what ran, what did not fit

| asked by the brief | boards | result |
|---|---|---|
| ≤ 3+2, ≤ 2+3 and ≤ 3+3 on 3 files | cyl:8×6, cyl:7×6 | ran (≤ 3+3 and ≤ 4+4), both readings |
| ≤ 2+2 and ≤ 3+2 on 4 files | cyl:8×6, cyl:7×6 | ran (≤ 3+2 and ≤ 3+3), both readings |
| cyl:8×8 "if it fits" | 3 files ≤ 3+2, 4 files ≤ 2+2 ran | 3 files ≤ 3+3 needs a 4.86 GB table, 4 files ≤ 3+2 needs 4.48 GB: do not fit under 3 GB |

Beyond the brief, and completed: 5 files ≤ 2+2 (cyl:7×6, 8×6); 3 files ≤ 4+4 (cyl:7×6, 8×6); 3 files ≤ 3+2 on cyl:7×7 and cyl:8×7; flat 7×6, 3 files ≤ 2+2.
@@EXTRA_RUNS@@

The table size is the number of layers times 2·N² bytes (N = number of squares). Ranges that were not run because the table exceeds 3 GB: cyl:8×6, 5 files ≤ 3+3 (5.4 GB); cyl:7×7 and cyl:8×7, 3 files ≤ 4+4 (6.1 and 8.0 GB), 4 files ≤ 3+3 (5.6 and 7.3 GB); cyl:8×8, 3 files ≤ 3+3 (4.9 GB), 4 files ≤ 3+2 (4.5 GB). Ranges that fit and were not run (not asked for): cyl:8×8 with 5 files ≤ 2+2 (1.6 GB), cyl:7×7 and cyl:8×7 with 4 files ≤ 3+2 (1.0 and 1.3 GB) and 5 files ≤ 2+2.

### 5.3 Tempo-signature census (no structural assumption, no passes)

For every root the 16 outcomes (side to move, and the contexts "one private White tempo move", "one private Black tempo move", "one shared move", in all 8 combinations) are computed in plain P, and compared with the signatures of the six abstract games zero, on, off, dud, over, under. This does not use the labels of section 2. Note that the signature of dud is the all-draw vector, so the "dud" column only says "draws in all 16 contexts" and is not a dud test.

@@TEMPO_TABLE@@

On 3 files ≤ 3+3 no root has the over (or under) signature. On 4 files ≤ 2+2 there are over-signature roots; they are the candidates tested in section 7.3.

## 6. The groups found

### 6.1 Over and under

**No over or under group was found** in any range of section 5.1 (structural classifier, reading A, root passers excluded or allowed), and none on 3 files ≤ 3+3 by the tempo-signature census. Candidates that are close in some sense:
- 20 distinct groups with the over signature on 4 files ≤ 2+2 (10 on cyl:7×6 and 10 on cyl:8×6 up to symmetry, from 20 over-signature roots per board; the colour-and-rank flip maps the over signature to the under signature);
- the *near-over* roots of the structural classifier: Black has a safe shuttle and every White safe move leads to a frozen state, but the closure condition fails elsewhere (@@NEAR_COUNTS@@).

All are tested in section 7.3.

### 6.2 Dud

Distinct dud groups, up to file translation (cylinder), file mirror and the colour-and-rank flip: **@@DUD_COUNTS@@** (readings A or B, root passers allowed; the full list with the confirmation result of each is `fin2/dud_groups.md`). Every group is listed there with notation in full (43, 40, 25 and 9 groups). Beside contexts (section 7.1): 31 groups on cyl:7×6 and 28 on cyl:8×6; at the root only (section 7.5): the other 12 + 12 + 25 groups (cyl:7×6, cyl:8×6, cyl:8×8).

*Without a root passer* (the brief's filter):
- cyl:8×6, 5 files, ≤ 2+2 pawns: two groups that are dud in **both** readings, A and B (CHECKED-2 for the move lists):
  - **G8a = `Kb2 kc4 Pa3 Pe2 pa4 pe3`** (blocked pairs a3/a4 and e2/e3 on files four apart; White shuttles b2–c2, Black c4–d4);
  - **G8b = `Kb3 kc5 Pa4 Pe3 pa5 pe4`** (the same one rank higher).
  `cylcgt.passed` is false for both pawn sets. Four combined king states each, 8 roots each, all (D, D); 72 legal moves at the 16 roots: 16 shuttles that draw, 56 deviations that lose (`logs/g8_moves_*.txt`; `kp_p` and `ref3m` give the same values and move lists). Every deviation loses by force in 11 to 21 plies (the earlier attempt's `scripts/depth2.py`, not re-run here, `logs/g8a_pv.txt` has the principal variations; also against free passes, reading A, by the classifier).
- cyl:7×6: the same two placements are dud in plain P only (reading B) and the window leaves no context file (7 files = 5 + 2 buffer files), so they are confirmed in the empty context only.
- cyl:8×6, 3 files: `Ka2 kc4 Pa4 Pc2 pa5 pc3` is dud in plain P (reading B) without a root passer, but it is **not** equal to dud_D beside contexts (section 7.1).
- cyl:7×6 and cyl:8×6, 5 files ≤ 2+2 (reading B): further no-passer groups, listed in `dud_groups.md`.

*With a root passer* (blockaded by a king, as in Z_B): the families D2 `Ka1 ka4 Pb4 Pc3 pb3 pc4`, D2m `Ka1 ka6 Pa3 Pb4 pa4 pb3`, D3 `Ka1 ka6 Pa3 Pb4 Pc3 pa4 pb3 pc4`, **Z_B on the cylinder** (`Kb2 ka4 Pa3 Pb4 pb3 pc4`, canonical form `Ka2 kb4 Pa4 Pb3 pa3 pg4` on 7×6), and groups made of one of these and extra blocked pairs on further files. On flat 7×6 (≤ 2+2 pawns, 3 files) the census finds four dud groups: Z_B, its mirror, D2 and `Ka1 ka5 Pa4 Pb3 pa3 pb4`.

## 7. Confirmation

Method (P model, exact, `kp_p --pmodel`, the private build `fin2/bin/kpp`): each group is put beside pawn-only contexts G on the files at distance at least 2 from the group's files (so no context pawn can ever meet a group pawn or attack a group square, Lemma 2.2), on one file or on two non-adjacent files, with no capture possible. For a dud group every king state of the shuttle closure (found by the moves that `kp_p` values as draws) and both sides to move are tested. The prediction is the brute-force value of G ⊞ dud_D (G ⊞ over_D, G ⊞ under_D) of Theorem 3.4(a) and Proposition 4.6, by `confirm.py` (D-model solver written for the earlier attempt, re-read; it uses the pushes and double steps of G only, a promotion is a decisive event, a player without a move loses, infinite play is a draw). "Agree" means `kp_p` returns an exact value (A = B) equal to the prediction. Four named contexts are always included: empty, a blocked pair (mutual zugzwang), a one-move pair, a gap pair; the others are random with up to 3 pawns.

### 7.1 Dud groups (P model)

@@CONF_DUD@@

### 7.2 Exhaustive single-file contexts

For a group, a context file X and every one of the 3^(H−2) assignments of {empty, White pawn, Black pawn} to the squares X2..X5 (`scripts/ctx_exh.py`):
@@CTX_EXH@@

### 7.3 Over and under candidates (P model, root only)

@@CONF_OVER@@

### 7.4 Chess (kpsolve)

Private build `fin2/bin/kp` (rebuilt byte-identically in `r3/bin/kp`) (`cc -O2 -o kp kings/kpsolve.c -lpthread`); every run through `heavy.sh` with a watchdog (3 GB, 1100 s); result `A B` = lower and upper bound from White's point of view, A = B means exact. Runs are at cap 1, and at cap 2 where stated; the chess prediction is that of the D-model (the P and chess models can differ, Theorem 3.2‴ needs (A_Q)).

@@CHESS@@

@@R3@@

## 8. Verdicts

@@VERDICTS@@

## 9. Reproduce

All commands run in `kings/delegate/out/K15/fin2` (abbreviated; paths relative to it), PYTHONPATH = the repository root, Python = the repository's `.venv/bin/python` where `cylcgt` is needed.
```
cc -O2 -o bin/grp ../grp.c
cc -O2 -o bin/kp   kings/kpsolve.c -lpthread
cc -O2 -o bin/kpp  kings/delegate/out/K7/scripts/draft/kp_p.c -lpthread        # run with --pmodel
c++ -O2 -std=c++17 -o bin/ref3m kings/delegate/out/K23/verify/ref3m.cpp         # boards: cyl:8x6 or flat7x6 (quirk)
# census (one run = both root-passer variants; B = --nopass, A = default)
bin/grp [--nopass] [--flat] --W 8 --H 6 --F 5 --wmax 2 --bmax 2 --sp-variants --out runs/NAME > runs/NAME.json
bin/grp --tempo --W 7 --H 6 --F 4 --wmax 2 --bmax 2 --out runs/NAME > runs/NAME.json
# one root
bin/grp [--nopass] --flat --W 7 --H 6 --F 3 --wmax 2 --bmax 2 --classify "Kb2 ka4 Pa3 Pb4 pb3 pc4 w -"
# Z_B regression
./scripts/zb_regression_final.sh ; python3 scripts/depth.py ../final/logs/zb_roots.in ; python3 scripts/oneply_confusion.py val/flat76_B_roots.tsv 3000
# P-model confirmation
python3 conf2.py gen cyl:8x6 dud cf/g_strictA_8x6.txt cf/strictA8 --nctx 40 --seed 11 --allstates
bin/kpp --board cyl:8x6 --ep on --cap 0 --pmodel < cf/strictA8.chunk.aa > cf/strictA8.chunk.aa.out ; python3 conf2.py cmp cf/strictA8 cf/strictA8.out
python3 scripts/ctx_exh.py cyl:8x6 dud g "Kb2 kc4 Pa3 Pe2 pa4 pe3"
# chess
kings/delegate/heavy.sh scripts/wd.sh chess/X.pid 3000000 1100 bin/kp --board cyl:8x6 --cap 1 --threads 2 < chess/G8a_alone.in
# this attempt (r3), all in kings/delegate/out/K15/r3:
cc -O2 -o bin/grp ../grp.c ; cc -O2 -o bin/kp kings/kpsolve.c -lpthread ; cc -O2 -o bin/kpp kings/delegate/out/K7/scripts/draft/kp_p.c -lpthread
c++ -O2 -std=c++17 -o bin/ref3 kings/delegate/out/K23/verify/ref3.cpp ; c++ -O2 -std=c++17 -o bin/ref3m kings/delegate/out/K23/verify/ref3m.cpp
scripts/rerun.sh                                   # census re-runs, compared with fin2/runs
python3 scripts/sample_ref3.py c8x6 cyl:8x6 100 8  # seeded samples (c7x6 seed 7, strictA8 seed 9, 50 lines); then scripts/run_ref3_unlocked.sh and scripts/cmp_ref3.py c8x6 c7x6 strictA8
python3 scripts/chunkrun.py cyl:8x8 data/notrun_cyl_8x8.in data/notrun_cyl_8x8.out 2 --moves
python3 scripts/ctxexh_chunked.py cyl:8x6 over g "Kd5 kb5 Pa3 Pb2 Pd2 pa4 pc5 pd4" logs/ctxexh_surv_chunked.txt 4 3     # Z*, file g; f and cyl:7x6 likewise
bin/kp --board cyl:7x6 --cap 1 --threads 2 --moves < data/cyl7_states.in                                           # D2, D2m in chess (through heavy.sh)
python3 scripts/mkchess_r3.py ; python3 scripts/mkadditions.py ; python3 scripts/mkedits.py ; (cd ../fin2 && python3 scripts/assemble.py)
# checks of the classifier
scripts/passer_layers.py, scripts/passer_check.py, scripts/xcheck2.sh, the dumprand comparison in logs/ (see the commands in section 3)
```

## 10. Files

In `kings/delegate/out/K15/`: `FINDINGS.md` (this file), `EDITS.md` (proposed edits of LOOPY, replaces the old one), `summary.json`, `fin2/` (the earlier attempt's tree, reused after the audit: `scripts/` classifiers, harnesses and queue scripts; `logs/` tables, depth and move lists, run logs; `runs/` census JSON and candidate lists; `cf/*.cmp.txt`, `cf/*.table.json` confirmation results; `chess/` inputs, outputs and logs of the kpsolve runs; `dud_groups.md` every dud group; `body_*.md` parts of this report), and `r3/` (this attempt: `scripts/`, `logs/`, `data/` root checks and Z\* inputs and outputs, `xs/` the ref3 samples, `runs/` the census re-runs; `zstar_summary.json`). Bulk batches (confirmation inputs and outputs, root dumps, validation dumps) and all binaries were deleted at the end; the scripts above rebuild them (`confirm`/`conf2.py gen` regenerate the confirmation inputs; the Python classifier's outputs `pyv/p_*.tsv` and `final/chk/py_np_5x6_pa1.tsv` and the root dumps in `val/` were deleted as well, and `pycheck.py`, `pycheck_np.py` and `grp --dumproots` regenerate them; so `r3/scripts/cmp_ref3.py` and `fin2/scripts/xcheck2.sh` need that regeneration first). The older attempts (`final/`, `v2/`, `f3/`, `pyv/`, `val/`, `runs/`, `conf/`, root files of `K15/`) are not part of this report.
