# K4: K+P vs K as a loopy combinatorial game, with and without edges

Brief: [../../briefs/K4_gafni_cylinder.md](../../briefs/K4_gafni_cylinder.md). Who did what:
- built by a Sonnet 5.5 agent, after three free-model attempts failed;
- checked by two independent Sonnet re-implementations (`verify_A/`, `verify_B/`), an audit, a fix round and a
  re-audit (workflow `wf_f7ea64f3-30f`);
- report written by the orchestrating session from the verified numbers, because subagents may not write
  report files.

Every table quoted below is printed by `mkreport.py` and checked by `claims.py`.

## Summary

1. **What was computed.** K+P vs K on flat and cylinder boards 3×4, 4×4, 3×5, 4×5 and 5×5, as a loopy game in
   normal play. Each quiet placement (neither king in check) is summed with 16 test games, and its signature
   (32 results) is compared with 26 candidate values. That is 20,556 placements in all. The 3×3 board was not
   computed: `kings/SPEC.md` needs at least 4 ranks.
2. **Checks pass (CHECKED-2).** With stalemate scored as a draw, the product solver agrees with kpsolve on all
   294,749 positions, with 0 differences. All 10 CGT sanity facts pass. Two independent re-implementations
   reproduce every placement's signature, class and difference test, again with 0 differences.
3. **No number or infinitesimal occurs (CHECKED-2).** Every placement is one of:
   - a decisive White win;
   - on (indistinguishable from on + \*);
   - off (likewise off + \*);
   - dud;
   - unmatched.

   No placement matches 0, ±1, ±2, \*, ↑, ↓, ±1/2, the switch ±1, over, under, 1 + \*, {on | 0}, or any other
   candidate. "Black wins against every test" never occurs. off is exactly the White-stalemated pattern, so it is
   an artefact of the stalemate-loses rule.
4. **Edges (CHECKED-2).** Between 12.5% and 20.5% of the placements present on both boards change class when the
   edges go. on is more frequent on the cylinder at every size. The three odd-width cylinders (3×4, 3×5, 5×5) are
   insensitive to every finite test game. Flat boards and 4-file cylinders have a few placements with finite tempo
   thresholds.
5. **Gafni and Proposition 4.3.** on + \* occurs on 3×4, flat and cylinder, but only tied with on; {on | 0} and
   1 + \* do not occur. This is measured against a second-hand summary, and the source was not located. No
   placement is an integer class. That is consistent with LOOPY.md Proposition 4.3 but does not test it (§5).

## 1. Conventions (read these first)

- **Normal play in the sum.** A side with no move in x ⊞ T loses; infinite play is a draw.
  - So a **stalemate is a loss**, unlike chess.
  - With T = 0, this changes the value of 171 of the 722 K+P vs K positions on flat 3×4, and 1,574 of 12,224 on
    flat 5×5. The check-1 table in §6 gives the count for every board.
  - x ⊞ 0 differs from the chess result at between 18.6% (flat 5×5) and 33.4% (flat 3×4) of quiet placements.
- **In-check rule.** A move in T is illegal while the mover is in check, so a checkmate in x ends the sum.
  "WHITE-WINS-ALL" therefore means a forced mate, a promotion that leads to mate, or a stalemate win.
  - Of these, 8 per flat board, and 20 on each 4-file cylinder, are chess "White to move wins, Black to move
    draws" placements whose sum win comes from stalemate.
- **16 test games, not 17.** The brief says "17 games, 34 results" but lists 16 games: 0, 1, 2, −1, −2, \*, ↑, ↓,
  1/2, −1/2, ±1, on, off, dud, over and under. No 17th game was invented, and signatures have 32 entries. This
  error is the orchestrator's, in the brief.
- **Signature equality is not CGT equality.** The 16 tests do not separate on from on + \*, or off from off + \*.
  The difference test x ⊞ (−V) (7,270 tests, all second-player survivals, all D/D) is a consistency check only,
  because x is not a stopper. Nothing here says "x = on" or "x = dud".
- **Rules.** All four promotions; no promotion was ever capped (asserted). Moves come from `kings/ref/solve.py`.
  The peak RSS of `gafni.py` was 84 MB.

## 2. Classes per board

Counts of quiet placements (CHECKED-2: the builder, `verify_A` and `verify_B` agree on every placement).

| board | quiet | WHITE-WINS-ALL | on/on+\* | off/off+\* | dud | unmatched, T-dependent | unmatched, T-independent (W first wins, B first draws) |
|---|---:|---:|---:|---:|---:|---:|---:|
| flat 3×4 | 338 | 141 | 47 | 4 | 18 | 59 | 69 |
| cyl 3×4 | 234 | 99 | 63 | 0 | 18 | 9 | 45 |
| flat 4×4 | 1000 | 506 | 76 | 4 | 58 | 156 | 200 |
| cyl 4×4 | 840 | 380 | 92 | 8 | 24 | 188 | 148 |
| flat 3×5 | 962 | 374 | 206 | 4 | 70 | 116 | 192 |
| cyl 3×5 | 738 | 270 | 216 | 0 | 72 | 18 | 162 |
| flat 4×5 | 2708 | 1222 | 394 | 4 | 190 | 390 | 508 |
| cyl 4×5 | 2376 | 996 | 456 | 8 | 116 | 356 | 444 |
| flat 5×5 | 5900 | 3104 | 598 | 4 | 466 | 718 | 1010 |
| cyl 5×5 | 5460 | 2630 | 810 | 0 | 250 | 670 | 1100 |

BLACK-WINS-ALL is 0 on every board. The other 21 candidates match 0 placements on every board.

**What the classes are in chess terms** (chess result = kpsolve with stalemate a draw; Appendix A of
`mkreport.py`):
- **off/off+\*** is exactly the set of quiet placements where White, to move, has no legal move and is not in
  check: White's king stands on the top rank directly in front of its own pawn, so the pawn cannot move, and the
  Black king covers the king's other squares. Examples are `Ka4 Pa3 kc3` (flat 3×4) and
  `Ka5 Pa4 kc4` (flat 5×5); every one is a chess draw.
  - It needs a corner file on a flat board.
  - On a cylinder it occurs only for width 4, because one king covers three consecutive files.
- **dud** is always a chess draw.
- **on/on+\*** is a chess draw for 100% of its placements on cyl 3×4 and cyl 3×5, where the sum turns a draw into
  a White win because stalemate now wins. On other boards the chess-draw share is lower: 35% on cyl 4×4, 51% on
  cyl 4×5, 46% on cyl 5×5, and 58%–87% on the flat boards. The rest are chess wins that need Black to run out of
  spare moves.
- **Unmatched, T-independent** placements are chess "White to move wins, Black to move draws" positions; no test
  game changes their result.

## 3. What changes when the edges go

| size | placements quiet on both boards | change class | on/on+\*: flat → cyl |
|---|---:|---:|---|
| 3×4 | 234 | 48 (20.5%) | 47 → 63 (13.9% → 26.9%) |
| 4×4 | 840 | 160 (19.0%) | 76 → 92 (7.6% → 11.0%) |
| 3×5 | 738 | 92 (12.5%) | 206 → 216 (21.4% → 29.3%) |
| 4×5 | 2376 | 418 (17.6%) | 394 → 456 (14.5% → 19.2%) |
| 5×5 | 5460 | 1046 (19.2%) | 598 → 810 (10.1% → 14.8%) |

- Every cylinder-quiet placement is flat-quiet; the converse fails, because the kings can be adjacent across the
  seam.
- **A class on one board only:** off/off+\* on flat 3×4, flat 3×5 and flat 5×5. On 3×4 and 3×5 the same
  placements are illegal on the cylinder, because the kings touch across the seam. On 5×5, `Ka5 Pa4 kc4` and
  `Ka5 Pa4 kc5` are off on the flat board and WHITE-WINS-ALL on the cylinder.
- **Most common changes on 3×4:**
  - 16 placements go from unmatched (T-dependent) to on. An example is `Ka1 Pa2 kc4`, chess W/D on the flat
    board and D/D on the cylinder.
  - 8 go from unmatched (T-independent) to WHITE-WINS-ALL, for example `Ka3 Pc2 kb1`.
  - 8 go the other way, for example `Ka4 Pc2 ka1`.
- `mkreport.py` §4 gives the full list of changes per size, with an example placement for each.

## 4. Tempo: integer scan x ⊞ n, n = −10 … 10

| board | placements whose result changes with n | thresholds at n = |
|---|---:|---|
| flat 3×4 | 10 of 338 | −1, 0 |
| cyl 3×4 | 0 of 234 | — |
| flat 4×4 | 22 of 1000 | −1, 0 |
| cyl 4×4 | 24 of 840 | −1, 0 |
| flat 3×5 | 38 of 962 | −2, −1, 0 |
| cyl 3×5 | 0 of 738 | — |
| flat 4×5 | 86 of 2708 | −2, −1, 0 |
| cyl 4×5 | 68 of 2376 | −2, −1, 0 |
| flat 5×5 | 86 of 5900 | −2, −1, 0 |
| cyl 5×5 | 0 of 5460 | — |

- Every change lies between n = −2 and n = 1, never beyond ±2. Every change is between a draw and a White win;
  no profile contains a Black win.
  - Example: flat 3×4 `Ka3 Pa2 kc3` gives DD DD DW WW WW for n = −2 … 2.
  - In words: one spare White move, or two spare Black moves, act like an unbounded supply.
- **Odd-width cylinders.** Every placement on cyl 3×4, 3×5 and 5×5 gives the same result against all 11 finite
  test games and every n (COMPUTED-1, checked by both verifiers).
  - A plausible reason is that a king can lose a tempo by triangulating around the seam (CONJECTURE).
  - Only widths 3, 4 and 5 were tested.

## 5. Gafni, and LOOPY.md Proposition 4.3

**Gafni** (against a second-hand summary; the source was not located). `notes/lit_cgt_chess.md` reports on\*,
{on | 0} and 1\* on 3×3 and 3×4.
- Here, on + \* occurs on flat 3×4 (47 placements) and cyl 3×4 (63), but only as the class on/on+\*, which the
  tests cannot split.
- {on | 0} and 1 + \* occur on neither 3×4 board, nor on any other board. Reading "1\*" as 1 + \* is an
  interpretation.
- This neither confirms nor contradicts Gafni, whose conventions are unknown. His 3×3 board is outside our SPEC.
- `notes/lit_cgt_chess.md` claims its author read Gafni's full text. That contradicts
  `notes/novelty_check/REPORT.md` ("could not be located"), and the main project should reconcile the two.

**Proposition 4.3** (no finite king tempo in isolated groups, as repaired):
- No placement is an integer class (CHECKED-2).
- That is *consistent with* Proposition 4.3 but *does not test it*:
  - a pawn-supplied integer would also be an integer class;
  - the proposition concerns safe king steps inside a group whose opponent is frozen, and whole-board K+P vs K
    placements do not meet its hypotheses.
- Finite thresholds at n ∈ {−2, −1, 0} do occur on flat boards and 4-file cylinders (§4).
- So this data neither proves nor refutes Proposition 4.3, and "no finite tempo was found" would be false.

## 6. Checks

**Check 1** compares the product solver with kpsolve, with T = 0 and stalemate a draw (CHECKED-2).

| board | K+P vs K | K+officer vs K, K vs K | differences |
|---|---:|---:|---:|
| flat 3×4 | 722 | 4830 | 0 |
| cyl 3×4 | 522 | 2868 | 0 |
| flat 4×4 | 2112 | 14572 | 0 |
| cyl 4×4 | 1816 | 12164 | 0 |
| flat 3×5 | 2024 | 11604 | 0 |
| cyl 3×5 | 1602 | 7509 | 0 |
| flat 4×5 | 5648 | 32944 | 0 |
| cyl 4×5 | 5040 | 28440 | 0 |
| flat 5×5 | 12224 | 72038 | 0 |
| cyl 5×5 | 11430 | 64640 | 0 |
| **all** | **43,140** | **251,609** | **0** |

768 legal K+P vs K positions are reached from no quiet placement. All of them have Black to move, in check from
the pawn: 660 with the pawn on rank 2, 66 on rank 3 and 42 on rank 4. (The docstring of `check1.py` says
"second-rank pawn" for all of them, which is wrong for 108.)

**Check 2** covers 10 known CGT facts, all passing in the builder and in both verifiers:
- second-player wins: 1 + (−1), \* + \*, ↑ + ↓, and 1/2 + 1/2 + (−1);
- Left wins either way: on + (−2), and over alone;
- draws either way: on + off, and dud + 1;
- Right wins either way: over + (−1/2);
- first player wins: ↑ + \*.

## 7. Verification

- **verify_A** used its own graph closure, test games, product and least-fixed-point solver, and borrowed only the
  reference move generator. It matched all 20,556 placements in signature, matched set, decisive class,
  difference test and chess result, with 0 differences. It also matched 293,981 graph nodes against kpsolve,
  again with 0 differences.
- **verify_B** used its own move generator written from SPEC, its own test games and its own C solver. It matched
  all 20,556 placements with 0 differences, and matched 294,749 positions against kpsolve with 0 differences.
  - Its legal sets equal kpsolve's.
  - Its test games are bisimilar to the builder's.
  - A negative control, swapping −1/2 for \*, produced mismatches, so the comparison can fail.
- **xrun.py**, a second retrograde core by the same author, agrees on 878,832 comparisons with 0 mismatches.
  It shares the move generator and test games, so it checks the solver only.
- **Audit issues, all real:**
  - the missing REPORT.md, now written here;
  - the 16-versus-17 count (§1);
  - the stalemate convention (§1–2);
  - the wording on tempo and Proposition 4.3 (§4–5);
  - the on+\* tie and the Gafni wording (§5);
  - the CHECKED-2 labels;
  - the weak difference test (§1);
  - 3×3 not covered (§1);
  - the 768-position wording (§6);
  - a truncated percentage (§1 now quotes 18.6%–33.4%).

  None was rejected.
- **Re-audit:** a from-scratch rerun of verify_A and verify_B against the final files gave 0 differences.
  `claims.py` passes, and `mkreport.py` exits 0.

## 8. Reproduce

From the project root (about 13 minutes; nearly all of it is `xrun.py`):

    sh kings/delegate/out/K4/run.sh

`run.sh` lists every step: build kpsolve, check 2, `gafni.py` per board, `xrun.py`, `tempo_scan.py`, the
tables, `claims.py` and `mkreport.py`. Every number above is printed by:

    PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K4/mkreport.py

The verifier reruns are `sh kings/delegate/out/K4/fixlogs/run_verifiers.sh`.

Not committed, because they are regenerated by the commands above:
- the kpsolve inputs and outputs in `check1/`;
- `verify_B/work/`, `verify_B/rerun_copy/` and `audit_rerun/`;
- `verify_A/rows_*.json`;
- the compiled binaries.
