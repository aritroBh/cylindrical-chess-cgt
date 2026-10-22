# VERIFY_T34: adversarial check of the n+3 ring minimum on C3 and C4

Verifier: independent agent, 2026-10-22. Subject: the T34 task agent's text report (no REPORT.md exists) and the
files in `research/ring_min_independent/`.

## Summary (5 lines)

1. **Verdict: ACCEPT_WITH_FIXES.** Every headline number was recomputed and agrees; the fixes are about the missing
   REPORT.md and two wording points, not about the mathematics.
2. A third solver of mine (pure Python, written from the brief, structured differently from `ring.c` and
   `ring_check.py`) reproduces all ring counts, all value-class counts and the *2 lists, on C3 (<= 6 pawns) and
   C4 (<= 7 pawns).
3. The project's own `cylcgt` (canonical-form values, a different algorithm) agrees with my solver on **all 34,310
   C3 ring classes and all 48,741 C4 ring classes with <= 6 pawns**, 0 disagreements; it finds exactly one *2 on
   C3 and none on C4 up to 6 pawns.
4. The agent's `ring.c` recompiles, and its `data/*.txt` files reproduce byte for byte. Its sensitivity table
   (textbook, no e.p., race rules) reproduces in every row except the "lapse" row, which I did not recompute.
5. No refutation found. The claim "no *2 ring below n+3 pawns for n = 3, 4" holds under the default convention
   (count rule, e.p. on, e.p.-aware passed test) and only there; the report says so itself.

## 1. What is missing

`REPORT.md` is not in the directory. The agent says the Write tool refused it. The substance exists only as the text
report relayed to me. Before anything cites this task, REPORT.md has to be written (5-line summary first, as
`delegate/COMMON.md` requires). `run_all.sh` still says "Reproduces every number in REPORT.md".

## 2. What I recomputed, and how

All commands run from the project root with `.venv/bin/python`, under `nice -n 10`, at most two heavy processes at
once, peak RSS under 450 MB. My files are in `research/ring_min_independent/verify_t34/`.

My solver is `verify_t34/vt34_solver.py`. I read the agent's code before writing mine, so it is not blind, but it is a
separate program: the board is a flat string, the passed test uses the per-file highest-enemy / lowest-enemy rank,
the rings are enumerated as products of per-file configurations with a cheap root filter, and the outcome of
S + *h is computed by plain negamax over (board, e.p. right). It never imports `cylcgt`.

### 2.1 Ring counts (exact, my own enumeration)

| board | pawns | placements | classes | agent | agree |
|---|---|---|---|---|---|
| C3 | 3 | 330 | 70 | 330 / 70 | yes |
| C3 | 4 | 4,740 | 865 | 4,740 / 865 | yes |
| C3 | 5 | 34,170 | 5,970 | 34,170 / 5,970 | yes |
| C3 | 6 | 160,515 | 27,405 | 160,515 / 27,405 | yes |
| C4 | 4 | 1,490 | 225 | 1,490 / 225 | yes |
| C4 | 5 | 32,752 | 4,404 | 32,752 / 4,404 | yes |
| C4 | 6 | 336,992 | 44,112 | 336,992 / 44,112 | yes |
| C4 | 7 | 2,220,008 | 285,090 | 2,220,008 / 285,090 | yes |

Classes are up to rotation and reflection of the files only (colour swap is not quotiented, which matters on C4).
Reproduce: `vt34_solver.py 3 6` (14 s) and `vt34_solver.py 4 7` (209 s, 412 MB peak). Outputs:
`vt34_c3_p6.out`, `vt34_c4_p7.out`, `vt34_c4_p7.time`.

### 2.2 Value classes and the *2 lists (default convention)

| board | pawns | classes: 0 / *1 / *2 | agent |
|---|---|---|---|
| C3 | 4 | 43 / 22 / 0 | same |
| C3 | 5 | 46 / 16 / 0 | same |
| C3 | 6 | 380 / 170 / **1** (6 placements) | same |
| C4 | 4 | 23 / 13 / 0 | same |
| C4 | 5 | 66 / 30 / 0 | same |
| C4 | 6 | 724 / 320 / **0** | same |
| C4 | 7 | 1,556 / 512 / **2** (16 placements) | same |

I checked the identity of the *2 rings by canonicalising under rotation and reflection:

- C3: my representative `W b2 c2 c3 / B a6 a7 b7` is the same class as the claimed `W a2 a3 b2 / B b7 c6 c7` (orbit
  size 6). This class is its own colour-swap partner, which is why C3 has exactly one.
- C4: my two representatives, `W b4 c2 d2 / B a6 a7 c6 d5` and `W b3 c4 d2 d3 / B a5 b7 c7`, are the same two
  classes as the agent's `W a4 b2 c2 / B b6 c5 d6 d7` (the claimed ring) and `W a4 b3 d2 d3 / B a7 b7 c5`. They are
  colour-swap (plus rank-flip) partners of each other. Orbit size 8 each, 16 placements.

### 2.3 Cross-check with the project's `cylcgt` (different algorithm: canonical forms)

I ran `cylcgt.pawns.value` on **my** enumeration (not the agent's list), comparing `cgt.show` with my class.

| scan | rings | disagreements | time | outputs |
|---|---|---|---|---|
| C3, 3 to 6 pawns | 34,310 | 0 | 306 s | `cylcgt_c3_le6.out` |
| C4, 4 to 6 pawns | 48,741 | 0 | 976 s | `cylcgt_c4_le6.out` |

cylcgt's counts agree with the solver's: C3 6 pawns 380 zeros, 170 stars, 1 *2; C4 6 pawns 724 zeros, 320 stars,
0 *2. The agent's `cmp_cylcgt.py` reran with the same four *2 lines (`cmp_cylcgt_rerun.out`). Note the agent's "four
*2 rings" are three classes: its fourth position `W b2 c2 d4 / B a6 a7 b5 c6` is a second representative of the
claimed C4 class.

The 285,090 seven-pawn C4 classes were not scanned with cylcgt (the agent compared 50 of them, plus the four
positions above).

Reproduce:
```
V=research/ring_min_independent/verify_t34
nice -n 10 .venv/bin/python $V/vt34_solver.py 3 6 --dump DUMP3
PYTHONPATH=. nice -n 10 .venv/bin/python $V/vt34_cylcgt_scan.py 3 6 DUMP3
nice -n 10 .venv/bin/python $V/vt34_solver.py 4 6 --dump DUMP4
PYTHONPATH=. nice -n 10 .venv/bin/python $V/vt34_cylcgt_scan.py 4 6 DUMP4
```

### 2.4 The agent's own artefacts

- `cc -O2 -Wall -Wno-unused-function ring.c` compiles clean. Rerunning C3 and C4 with `--list` and `--all`: the
  output files `data/c3_all.txt`, `data/c4_all.txt`, `data/c3_star2.txt`, `data/c4_star2.txt` are **byte identical**
  (`cmp`) to the agent's.
- Runtime and memory as reported: C3 0.23 s and 11 MB, C4 4.7 s wall and 135 MB peak (agent: 0.26 s, 5.6 s,
  about 135 MB). The Python re-implementation's recorded peak RSS was 327,565,312 bytes (agent: 328 MB).
- Both claimed rings give bits `0xcf` (heap 2 is a second-player win) in `ring --pos`.

### 2.5 Sensitivity table (the agent's item 5)

I recomputed every row with my solver, except the "lapse" row.

| setting | C3 *2 classes by pawn count | C4 | agrees |
|---|---|---|---|
| textbook passed test | 5 at 6 pawns | 1 at 6, 2 at 7 | yes |
| no e.p. | 4 at 6 | none up to 7 | yes |
| race "mover wins" | none up to 6 | 3 at 6, 2 at 7 | yes |
| race "opponent wins" | 2 at 4, 2 at 6 | 2 at 6, 2 at 7 | yes |
| e.p. lapses on a heap move | not recomputed | not recomputed | not checked |

I found these outputs equal row by row (also the 0 and *1 columns): `vt34_c3_variants.out`,
`vt34_c4_variants.out`. The lapse variant exists only in `ring.c`. It does not bear on the headline: `cylcgt` keeps
the e.p. right across moves in other components, which is the default of `ring.c`.

## 3. Rule audit (looking for a shared misreading)

I compared the agent's rules with `cylcgt/pawns.py`.

- Double step and e.p. right (set only when an enemy pawn stands beside the landing square, valid for one board
  move, kept across a heap move): same as cylcgt.
- E.p.-aware passed test (only the pawn on its rank 4 or 5 that can really be taken): same.
- Count rule: opponent of the mover wins ties. cylcgt's `promote_distance` skips a passed pawn that has a friendly
  pawn ahead on its file, `ring.c` takes the minimum over all passed pawns. These agree always: the pawn ahead is
  also passed and no farther from promotion, and the e.p.-capturable pawn can never have a friendly pawn behind it
  on its file (it came from rank 2 or 7).
- Distances (rank 2 or 7 counts 5), pawns on W rank 7 / B rank 2 always passed (so the enumeration range W 2..6,
  B 3..7 loses nothing): correct.
- The test "G = *2 iff G + *2 is a second-player win" is the standard theorem for short games, and the
  +-BIG leaves are decisive against a nim heap.

I found no misreading. The 0-disagreement cylcgt scans are the strongest evidence, since cylcgt shares no code with
any of the three solvers.

## 4. Label audit

| label in the report | verdict |
|---|---|
| C3: CHECKED-2 | justified, and stronger than stated: agent C, agent Python, my Python and cylcgt (all 34,310 classes) agree |
| C4 (no *2 at <= 6): CHECKED-2 | justified: three solvers plus cylcgt on all 48,741 classes |
| C4 (exactly two *2 classes at 7) | justified by the three solvers (full enumeration); cylcgt only on the two classes found and 50 samples |
| "n+3 for n = 3 and n = 4" | holds under the default convention only; the report says so, and the table shows other conventions give n+1, n+2 or no *2 |
| "I make no claim for n >= 5 (CONJECTURE)" | correct |
| sensitivity table (no label given) | single implementation in the agent's own work (`ring.c`); now CHECKED-2 for all rows except lapse |

The agent's own caveat ("both solvers are mine, so they share my reading of the brief") was honest and necessary:
without the cylcgt scan, "CHECKED-2" rested on the agent's two programs plus a 291-ring sample. The scan above is
what makes the label safe.

## 5. Problems and fixes

1. **REPORT.md missing.** Write it from the text report (and point to `verify_t34/` for the extra checks).
2. **Miscount.** "It returns *2 for all four *2 rings above": the report lists three distinct classes (one on C3,
   two on C4). The four tested positions include a second representative of the claimed C4 ring.
3. **Quotient not stated near the claim.** "Exactly 1" and "exactly 2" classes are up to rotation and reflection of
   the files, not colour swap; on C4 the two classes are colour-swap partners. State this in the headline.
4. **Lapse row** has not been independently recomputed; label it COMPUTED-1.
5. **Rule 1 of COMMON.md.** I ran read-only `git status` and `git log -1` to see whether `paper/` was touched
   (no tracked file under `paper/` shows as modified; several untracked build files there are not attributable to
   T34). No git write was made. Nothing in the T34 directory suggests the agent touched `paper/`.

Nothing else: no file over 50 MB (largest 11.4 MB), no `ring` binary left behind, no process was killed or signalled
by me.
