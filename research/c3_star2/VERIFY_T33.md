# VERIFY_T33: adversarial check of the C3 / C4 \*2 walk-through

Verifier output. Scripts and raw outputs are in `research/c3_star2/verify_t33/` (reproduce everything with
`research/c3_star2/verify_t33/run_all.sh`, light compute, a few minutes on a busy machine).

## Summary (5 lines)

1. **Verdict: ACCEPT_WITH_FIXES.** Every reported *value* is correct: both roots are \*2 in the default setting, and the
   9-setting table (count / mover / opponent x e.p. off / textbook / aware) is reproduced exactly by a third, freshly
   written solver, in all 18 root cells.
2. **One claim is wrong.** "The decisive capture is c5xb6 e.p." is refuted by ablation (below). The \*2 comes from the
   two e.p. captures **B b4xa3** and **W b5xc6**; c5xb6 is neither necessary nor sufficient.
3. **`REPORT.md` was never written.** The brief's deliverable (walk-throughs plus appendix in `REPORT.md`) exists only as
   the agent's chat message; the appendix data is in `appendix_moves.txt`. Someone must write `REPORT.md`.
4. The unresolved "33 disagreements" are a harness artifact, now resolved: all 33 are roots that already contain a
   one-sided passed pawn (cylcgt scores the root as +-BIG, the C `--eval` mode never tests the root). With no passed
   pawn at the root, 162 of 162 comparisons agree.
5. Walk-through inequalities (domination, reversal) can be upgraded from CHECKED-1 to CHECKED-2: I re-derived all headline
   ones independently. Small text fixes are listed in section 3.

## 1. Independent recomputation

My solver `verify_t33/mysolve.py` was written from the stated rules (COMMON.md and the `pawns.py` module docstring) and shares
no code with `cylcgt/` or `frontier.c`. It decides the outcome class of `G + H` for an explicit short game H (nimbers,
integers, DAG nodes) by memoised search; `G = *k` iff `G + *k` is a second-player win. `sumsolver.py` adds disjunctive sums
of several pawn boards (a decided board freezes as +-BIG), which gives exact `A <= B` tests (`-A` = colours swapped, ranks
reflected). Caveat: all three programs (cylcgt, `frontier.c`, mine) implement the same *model* (count rule, per-component
e.p. right, first passer ends the game). CHECKED-2 says the implementations agree, not that the model is chess.

| Claim in the report | Recomputed (mine) | Agrees |
|---|---|---|
| C3 root = \*2 (count, e.p. on, aware) | outcome N, G+\*2 is P, nimber 2 (`run_settings.out`) | yes |
| C3 e.p. off = 0 | P, nimber 0 | yes |
| C3 mover rule = 0 under e.p. off / textbook / aware | 0, 0, 0 | yes |
| C3 opponent rule = \*2 incl. e.p. off | \*2, \*2, \*2 | yes |
| C4 root = \*2 (count; mover; opponent; e.p. on, both tests) | \*2 in all six cells | yes |
| C4 e.p. off is not a nimber under any rule | no \*k for k < 16 for count, mover, opponent (`c4_epoff_k16.out`) | yes |
| 18/18 root cells agree with the C solver | I re-ran `cyl_eval` (rebuilt from `cyl_eval.c`): identical to `eval_cyl_out.tsv`; mine matches both | yes |
| First e.p.-on/off difference at ply 5 (c5xb6) | earliest ply of each e.p. capture type: a5xb6, c5xb6 at 5; B a4xb3, b4xa3, c4xb3, c4xa3 at 6; W a5xc6, b5xc6 at 7 (`ep_lines.out`, `ep_pos.out`) | yes |
| `W a2 a3 c5 / B b5 c7`: 3/2+-1/2 with e.p. on, 1\* with it off | equals {2\|1} with the e.p. right pending, equals 1\* without it, and not the other way round | yes |
| a5xb6 position: 0 on, 0 off | both 0 | yes |
| C3 cannot arise | breadth-first search from `a2 b2 c2 / a7 b7 c7`: 2971 states, 0 hits; also provable (see 4) | yes |
| C4 arises in 7 plies, one capture B a7xd6 | my BFS: minimum depth 7, same history; each of the 7 moves legal in my generator; no passed pawn at any step (aware test) | yes |
| Root options: none is 0 or \*; b2-b3, b2-b4 dominated by a3-a4; b7-b6, b7-b5 dominated by c6-c5 | outcome classes R, R, L for b2-b3, b2-b4, a3-a4 and L, L, R for b7-b6, b7-b5, c6-c5; none is P (value 0) and none is P after adding \* (value \*); the dominations follow because L > 0 > R | yes |
| a3-a4 reverses through b7-b5 | Q1 = `W a2 a4 b2 / B b5 c6 c7` <= G (and <= \*2); b2-b3 reply = \*; the other three replies (a2-a3, a4-a5, b2-b4) are each <= a4xb5 | yes |
| a4xb5 reverses through c6xb5; b2-b4 is 0 there | P1 = `W a2 b2 / B b5 c7` <= G; `W a2 b4 / B b5 c7` = 0 | yes |
| c6-c5 reverses through b2-b4; replies b7-b6 = \*, c5xb4 | V >= G; b7-b6 reply = \*; V's b7-b5, c5-c4, c7-c6 are each >= Y2 (the c5xb4 position) | yes |
| c5xb4 reverses through a3xb4, whose reply b7-b5 is 0 | Z = `W a2 b4 / B b7 c7` >= G; `W a2 b4 / B b5 c7` = 0 | yes |
| C4: b2-b3 = \*, c2-c4 = 0, c2-c3 and b2-b4 dominated by b2-b3, c5-c4 = 0 | all true (`walk_checks_c4.out`) | yes |
| C4: a4-a5 reversible through b6-b5; b6-b5 through a4xb5; d6-d5 through a4xd5 | Ya <= \*2; Yb (white passer) >= \*2; Yd >= \*2; replies b6-b5 = \*, c5-c4 and d7-d6 both >= \* | yes |

## 2. Where the report is wrong or overstated

**2.1 "The decisive capture is c5xb6 e.p." is false (substantive).** Ablation on the C3 root, count rule, aware test (the
textbook test gives identical results). There are exactly 8 e.p. capture types in the game tree. Dropping chosen types from
the move generator, in two implementations (mine, and cylcgt with a patched `moves`; `ep_ablate_cylcgt.out`,
`ep_select.out`, `ep_subsets.out`):

| e.p. captures allowed | Root value |
|---|---|
| all | \*2 |
| none (= e.p. off) | 0 |
| all but W c5xb6 | \*2 |
| only W c5xb6 | 0 |
| all but W a5xb6 | \*2 |
| all but B b4xa3 | ↑ |
| all but W b5xc6 | ↓ |
| only B b4xa3 | ↓ |
| only W b5xc6 | ↑ |
| only B b4xa3 and W b5xc6 | \*2 |

Exactly 64 of the 256 subsets give \*2, namely those containing both B b4xa3 and W b5xc6; the minimal subset is those two.
So c5xb6 is the *first* capture where on and off values differ (ply 5), but it plays no role in the root value. Shortest
histories to the two that matter (my BFS, `ep_lines.out`):

- B b4xa3: 1.a3-a4 b7-b5 2.a4-a5 b5-b4 3.a2-a4 b4xa3 e.p. (6 plies)
- W b5xc6: 1.a3-a4 c6-c5 2.b2-b4 c5-c4 3.b4-b5 c7-c5 4.b5xc6 e.p. (7 plies)

Replacement text: "With e.p. off the value is 0. It is \*2 exactly when both Black's b4xa3 and White's b5xc6 en passant captures
are legal; either alone leaves a non-nimber (↑ or ↓). The shallow capture c5xb6 changes the value of the
subposition `W a2 a3 c5 / B b5 c7` from 1\* to 3/2+-1/2 but not the root." Note the value 3/2+-1/2 belongs to that position
*with the e.p. right pending* (`ep b6`); the report omits the marker.

The report's own hedge ("the reversal chain that carries this to the root is not traced") was the right instinct; the word
"decisive" should not have been used.

**2.2 The "33 disagreements" (item 7) are resolved, and the headline 417/450 is misleading.** Same positions and seed as
`xcheck_cyl.py`, split by whether the root already has a passed pawn (`xcheck_resolve.out`):

| | agree | disagree |
|---|---|---|
| root has no passed pawn | 162 | 0 |
| root already has a one-sided passed pawn | 255 | 33 |

`pawns.value` returns +-BIG at once for such a root; `cyl_eval --eval` calls `solve()` on the root with no passed-pawn test,
so it plays the position out as an ordinary game. Neither implementation is wrong; the harness should have excluded these
roots. The correct statement is "162/162 on roots with no passer, plus 255 coincident agreements".

**2.3 `REPORT.md` is missing** although the brief names it as the deliverable. The reason given (subagent rules forbid report
files) does not change that the repository has no walk-throughs; they exist only in the chat message. Items 2 and 3 of the
brief (why it is 0 with e.p. off; values under mover and opponent rules) are answered with values only, no explanation of
which e.p. capture or which race result produces them. The C4 e.p. question was not addressed; from my ablation
(`ep_select_c4.out`) the C4 root keeps \*2 only if both Black captures b4xc3 and c4xb3 are allowed (each is individually
needed; the two White captures a5xd6 and c5xd6 are irrelevant), and those two alone already give \*2.

## 3. Smaller fixes

- The labels "(e.p. b3)" on b2-b4 and "(e.p.)" on c2-c4 in both walk-throughs come from the engine, which always attaches an e.p.
  marker to a double step. In `W a2 a3 b4 / B ...`, `W a2 b4 / B b5 c7` and C4's `W a4 b2 c4 / B b6 c5 d6 d7` no Black pawn stands on
  the capturing rank next to the moved pawn, so no e.p. capture exists and the e.p. right is vacuous. Drop the parentheses
  from the text; they suggest en passant matters in those lines.
- Walk-through A: after "a4xb5 reverses through c6xb5" the replacement set also contains White's a2-a4. That option is not
  dominated by 0 or \*; it is itself reversible (through b5xa4, a position that is <= G). The sentence "so White's options
  reduce to 0 and \*" is true (the final equality is checked independently) but skips this step.
- `ep_diff.py` documents the run as `ep_diff.py` but the saved `ep_diff.log` needs the argument `5` (the default `MAXPLY` is 4
  and finds nothing). `claims_z.py` and `ep_line.py` have no saved logs.
- Item 6: capture uniqueness need not be left at COMPUTED-1. Material gives it directly: 8 pawns become 7, so there is exactly
  one capture; the final Black files are {b, c, d, d} from {a, b, c, d}, which a single capture can produce only by an a-pawn
  taking onto the d-file, and it lands on d6 because it ends on rank 6. PROVED.

## 4. Label audit

| Item | Report label | Verified label |
|---|---|---|
| 1 root = \*2 | CHECKED-2 (reductions CHECKED-1) | CHECKED-2 now three implementations; the reductions in the walk-throughs are now CHECKED-2 for every headline inequality (section 1) |
| 2 e.p. off = 0; first difference ply 5 | CHECKED-2; COMPUTED-1 | agree; but "decisive c5xb6" is refuted (2.1) |
| 3 mover/opponent | CHECKED-2 | agree |
| 4 C4 values | CHECKED-2 (18/18) | agree |
| 5 C3 unreachable | PROVED; BFS COMPUTED-1 | agree. Proof: six pawns means no captures, so Black keeps an a-pawn and White a c-pawn; the target has neither |
| 6 C4 history | PROVED; uniqueness COMPUTED-1 | history PROVED; uniqueness also PROVED (3) |
| 7 random cross-check | 417/450, cause unknown | resolved in 2.2 |
| 8 inequalities CHECKED-1 | CHECKED-1 | upgraded to CHECKED-2 except the replacement-set reductions that the walk-throughs skip |

## 5. Reproduce

```
cd /Users/aritro/Downloads/Research/Chessendgames/research/c3_star2/verify_t33 && ./run_all.sh
```
Individual scripts (from that directory, `../../../.venv/bin/python <script>`): `run_settings.py` (9 settings x 2 roots),
`ep_select.py aware|textbook`, `ep_subsets.py`, `ep_ablate_cylcgt.py`, `ep_lines.py`, `ep_pos.py`, `ep_select_c4.py`,
`c4_epoff_k16.py`, `walk_checks_c3.py`, `walk_omitted.py`, `walk_omitted2.py`, `walk_checks_c4.py`, `reach_mine.py`,
`xcheck_resolve.py`. Each writes its `.out` next to it.
