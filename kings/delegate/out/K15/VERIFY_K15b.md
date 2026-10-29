# VERIFY_K15b: referee report on K15 (over and dud groups on the cylinder)

Referee K15b, 2026-10-29 (edits tagged 2026-10-27 as the brief requires). Files: this report, `verify/EDITS.md` (3 replacement blocks), `verify/summary.json`, scripts and logs in `kings/delegate/out/K15/verify/`. Nothing outside `verify/` was written. No earlier referee files existed; nothing was reused except K15's own inputs (`final/logs/zb_roots.in`, `fin2/chess/G8_states.in`, `r3/data/cyl7_states.in`, `fin2/dud_groups.md`, stored chess outputs).

## 1. Verdict

ACCEPT WITH FIXES. The mathematical content holds: Z_B and G8a/G8b values, the dud census, the zero over/under result, the Z* refutation, the chess results. What fails is bookkeeping:
1. The headline group counts 43 / 40 / 25 / 9 are not invariants. Recounted from whole closures: 24 / 23 / 14 / 7 up to symmetry.
2. The tempo-signature census is not plain P (stalemate counted as a loss, tempo moves allowed in check). Its "20 over-signature roots per board" become 4 (cyl:8x6) and 6 (cyl:7x6) in plain P.
3. "80 runs" is 80 table rows from 20 ranges; only the 40 reading-A rows can output over.
4. The edits attribute the one-ply flaw to the Appendix A scratch search, whose script does not exist; that is unsupported.
5. The flat 7x6 groups (9) are not in `dud_groups.md`, contrary to FINDINGS 6.2.
6. FINDINGS says the 1,296-position context test is COMPUTED-1 with a 50-position ref3 sample; it is now CHECKED-2 in full.

## 2. What I built

- `mysolve.cpp` (mine, written from the definitions in FINDINGS 2.1, no code from `grp.c`, `kpsolve.c`, `cylcgt`, `ref3`): exact retrograde solver of model P with real kings on a W x H cylinder or flat board, e.p. included, per pawn layer, both readings (A: pass is a move, illegal in check; B: none, stalemate draw); classifier frozen / on / off / dud / over / under / check / threat / leak / mixed with closures; relaxed over/under test; depth-to-promotion search; pawn-closure `--reach` mode; tempo mode `mysolve_t.cpp`.
- Independent oracles for values: `ref3`, `ref3m` (K23, written from SPEC), `kpp` (shares source with kpsolve), `kp` (kpsolve). Rebuilt privately in `verify/bin/` (deleted at the end).
- Reproduce: `cd verify; c++ -O2 -std=c++17 -o bin/mysolve mysolve.cpp; ./runcmp.sh NAME "<grp args>" "<my args>" [nopass]` (runs grp and mine, compares label per root); `mine_only.sh`; `groupcount.py`; `groupcheck.py`.

## 3. Claim by claim

### 3.1 Z_B regression (claim 1)
- Own classifier, flat 7x6, ≤ 2+2, plain P: 41 dud roots, 52 frozen; Z_B `Kb2 ka4 Pa3 Pb4 pb3 pc4` is dud at all four king states. Reading A: label "mixed" at the same four roots. Same dud labels on cyl:7x6 and cyl:8x6 (plain P). CHECKED-2 (my solver against `grp`, zero label differences on all 479,586 roots; `runs/flat76_B22*.json`).
- Depth to forced promotion after each of the 26 deviations (my own search, `mysolve --depth`): 3 plies for 4 moves, 5 for 2, 7 for 6, 9 for 8, 11 for 6. Exactly K15's table. No deviation is an immediate event.
- Not re-run: the brief's one-ply classifier (`oneply.py`) and the numbers "12 of 26 accepted as shuttles", "none of 41 flat dud roots found", "18 of 52 frozen". The 12 are geometrically the king moves Kb2-a1/b1/c1 and Kb5-a6/b6/c6, which are non-capturing, in-file and reversible, so the statement is plausible. NOT_CHECKED.
- `cylcgt.passed`: true for Z_B (`W: a3 b4 / B: b3 c4`), false for G8a and G8b (checked directly). The no-passer filter does reject Z_B.

### 3.2 Z_B on the cylinders (claim 2)
`kpp` and `ref3m` on the 8 roots, cyl:7x6 and cyl:8x6: same root values and same move lists; 38 moves, 8 draw, 30 lose for the mover, wrap moves included (`zb_cyl_*.out`). CHECKED-2.

### 3.3 G8a, G8b in P (claim 3)
`kpp` against `ref3m`, 16 roots: identical; 72 moves, 16 draw, 56 lose; no pawn move at any root (`g8.*.out`). My classifier: dud in both readings. CHECKED-2.

### 3.4 G8a, G8b in chess (claim 4)
I re-ran kpsolve cap 2 through `heavy.sh` (`chess/g8_c2.out`, 132 s, no "capped promotions" line): 16 roots exact (D, D), the 72 move values equal the P lists, and equal K15's stored output. COMPUTED-1 stands (one solver family). The cap-1 context table (7.4 of FINDINGS) was checked against the stored `.out` files only: five of six contexts agree, the racing-passer context gives W W / W L as stated.

### 3.5 Beside contexts (claim 5)
Own predictor of r(G ⊞ dud_D) (a pawn-only game on file g, both sides may pass at will, promotion wins) against `ref3` (independent solver) on **all 1,296** positions (G8a, G8b x 4 king states x 2 sides x 81 assignments of file g): 0 differences (496 W, 496 L, 304 D). Upgrade to CHECKED-2 for this set. The 640 random-context positions were not re-run (COMPUTED-1).

### 3.6 Dud groups and counts (claim 6)
- All 108 listed groups (43+40+25 of `dud_groups.md`) are dud in plain P by my classifier; exactly the ones marked A+B (8, 10, 9) are also dud in reading A (`runs/groupcheck.tsv`). CHECKED-2 for the labels.
- The confirmation split 18 (A+B, all agree) / 41 (B only, 7 differ) re-derives from the table in `dud_groups.md`. One differing group, `Ka2 kc4 Pa4 Pc2 pa5 pc3` (cyl:8x6, no root passer), checked by `ref3`: with `Pe2 pe3` beside it all four king states of the closure are W, the dud_D prediction is D. CHECKED-2.
- **Counts: REFUTED as stated.** My whole-closure census over the same ranges (A and B, root passers allowed; `runs/*.dud`, `groupcount.py`):

| board | dud roots | closures | connected groups | up to colour flip | up to translation, mirror, flip | K15 claims |
|---|---|---|---|---|---|---|
| cyl:7x6 | 1671 | 97 | 74 | 50 | 24 | 43 |
| cyl:8x6 | 1655 | 91 | 68 | 47 | 23 | 40 |
| cyl:8x8 | 588 | 42 | 40 | 27 | 14 | 25 |
| flat 7x6 (F=3, ≤3+3) | 119 | 16 | 10 | 7 | 7 | 9 |

  The census root counts agree with K15's table range by range; the disagreement is only in how roots are grouped. K15 identifies a group by the smallest state of its forward closure and then canonicalises one representative root under symmetry; forward closures of different roots overlap, and a representative root need not map to the representative of its image, so the number depends on state order. On flat 7x6 the same roots give 10, 9, 7 or 7 under four natural conventions. The ranges I did not run (cyl:7x7, 8x7, cyl:7x6 F=4 3+2 and F=5 2+2) only add roots already inside the larger ranges for the same boards except 7x7/8x7, which K15 says have none.
- FINDINGS 6.2 says the 9 flat groups are listed in `dud_groups.md`; the file has three sections (43, 40, 25).

### 3.7 No over or under (claim 7)
Own census, reading A, root passers allowed: 0 over, 0 under, 0 self-check violations in 16 of the 20 ranges (cyl:8x6: F=3 ≤3+3 and ≤4+4, F=4 ≤3+2, ≤3+3, ≤4+2, F=5 ≤2+2 and ≤3+2; cyl:7x6: F=3 ≤3+3 and ≤4+4, F=4 ≤3+3 and ≤4+2, F=5 ≤3+2; cyl:8x8: F=3 ≤3+2, F=4 ≤2+2; flat 7x6 ≤2+2 and ≤3+3). Frozen and dud counts equal K15's table in every one (and in plain P for the same 16). Labels equal root by root, `grp` against mine, in 12 runs (flat 7x6 ≤2+2 A and B, ≤3+3 A; cyl:7x6 and 8x6 F=3 ≤3+3 A and B; cyl:8x6 F=4 ≤2+2 A and B, F=4 ≤3+2 A and B, F=5 ≤2+2 A and B). A relaxed test (ignore check, threat and leak at A- and Z-states) also finds none. Not run: cyl:7x7, cyl:8x7, cyl:7x6 F=4 ≤3+2 and F=5 ≤2+2 (NOT_CHECKED, they lie in the table as "earlier" or "rerun").
- No hidden cut-off: closure limit 6000 never reached (`closure_too_big` is 0 in every JSON), mine allowed 20,000 and never hit it; near-over root counts per run are at most 28, below the print limit of 40.
- Label: COMPUTED-1 for the counts, CHECKED-2 for the classifier (second implementation agrees). Two caveats, not errors: "80 runs" is 80 table rows from 20 ranges (40 processes), and the 40 plain-P rows say nothing about over (K15 says so in the body, the edit should too). The test is structural (bisimilar to over_D on the group files, kings on those files at the root); "no over exists" is not claimed, correctly.

### 3.8 Classifier agreement (claim 8)
The Python cross-checks (772,188 and 634,628 roots) could not be re-run (their dumps were deleted). They are replaced by my C++ solver: zero label differences on the roots of the 12 root-by-root runs above (about 40 million roots in total), CHECKED-2, in both readings, on flat and cylinder boards.

### 3.9 Z* (claim 9)
- `kpp` and `ref3m`: Z* is (W, W) at both roots on cyl:8x6 and cyl:7x6; White's only non-losing move is d2-d3; all six Black moves lose.
- Own predictor of r(G ⊞ over_D) (file of ≤ 3 context pawns; Black passes forever until White plays ω → 0; a player without a move loses) against `ref3` on cyl:8x6: file g 130 of 130 agree; file f 127 of 130, the three differences are `Pf3 pf4 pf5` (Black to move), `Pf2 pf4 pf5` (White to move), `Pf2 pf3 pf4` (Black to move), predicted W, solved L. CHECKED-2 for all 260 positions (cyl:7x6 file f not re-run).
- The over-like candidates are the same under plain-P rules: see 3.10.

### 3.10 Tempo-signature census (FINDINGS 5.3, EDIT text)
- My plain-P tempo solver (stalemate draw, no tempo move in check) has ctx 0 equal to `ref3` at 600 of 600 sampled roots. K15's `grp --tempo` has ctx 0 different from `ref3` at 166 of 1,500 sampled roots (flat 7x6): it treats stalemate as a loss and lets a tempo move be played in check. FINDINGS 5.3 says "plain P".
- Result with plain-P rules: no over signature on 3 files ≤ 3+3 (cyl:7x6, 8x6), as K15. On 4 files ≤ 2+2, root passers allowed: over signature at 6 roots (cyl:7x6) and 4 roots (cyl:8x6), under likewise; all four cyl:8x6 roots are among K15's 20, including both survivors `Kc4 kd6 Pd3 Pd5 pa5 pd4` and `Kb4 ka6 Pa3 Pa5 pa4 pd4`. K15's counts 20 / 20 and the dud-signature counts (33,836; 35,268; 12,418; 13,215) are not reproduced; their refutation beside contexts was not re-run (COMPUTED-1 stays). The qualitative negative result survives.

### 3.11 D2, D2m in chess (claim 9b)
Stored cap-1 chess output re-analysed against my own `kpp` P lists: per group 116 draws agree, of 108 P-losing deviations 52 lose in chess (exact), 52 draw (exact), 4 undecided at cap 1. I also re-ran kpsolve cap 1 (`chess/d2_c1.out`): byte-identical to K15's file. COMPUTED-1.

### 3.12 Conjecture 4.7 (claim 10)
The wording "no over group known, second half unsupported, 'none exists' not claimed" is supported by 3.7, 3.9, 3.10. Label CONJECTURE is right.

## 4. Edits
- OLD blocks: all eight of K15's occur exactly once in the current LOOPY.md.
- Accepted unchanged: status row C4.7, section 3 text, 5.7 cylinder bullet, status row P3.2prime, section 7 dud bullet. Checked their numbers (38 moves / 8 / 30; (W, L) at cap 1 on cyl:7x6; G8 chess at cap 2; five of six contexts) against the evidence above.
- Replaced (see `verify/EDITS.md`): C4.7 (run count wording, K15b recheck, tempo-census caveat, Z* wording, Appendix A attribution), section 8 item 2 (context test upgraded, group counts restated, K15b counts), Appendix A (no claim about code that was not kept).
- Why Appendix A: K15's reason is the flaw of `K15/classify.py` (OpenCode), which is not the Appendix A script. What can be said is that one-ply tests label Z_B "other"; that is already what K15 measured with `oneply.py`.

## 5. Limits of this referee
Independence: my solver shares only the written definitions (and the brief's model) with K15; both read the same definition of "safe move", of the closure and of over, so a wrong definition would not show. The model rules (e.p., stalemate, promotion) were fixed by me from SPEC and agree with `ref3` at 600 sampled roots and with `kpp`/`ref3m` on every move list I compared. Not re-run: cyl:7x7/8x7 rows, the 640 random contexts, near-over/near-under groups and their context tests (only Z* was), the 49 root-only groups (covered by the 108-group check of 3.6, not by their K15 route), chess context runs other than G8 cap 2 and D2/D2m.
