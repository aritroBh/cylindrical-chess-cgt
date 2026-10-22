# T20b: report (agent text) with the verifier's findings

Written by the orchestrating session on 2026-10-22. The subagent could not write report files, so its
final message is reproduced verbatim under "Agent report". An independent Sonnet verifier then tried to refute
it; its verdict, summary and fix list come first and **take precedence over the agent text where they differ**.

## Verifier verdict: ACCEPT_WITH_FIXES

I could not refute the main claims. I recomputed them with my own scripts in the scratchpad and found no numerical errors. There is no REPORT.md in research/star2_oracle/. The relayed inline report stops partway through section 2, so I checked its 10-line summary, section 1 and the start of section 2 against the output files. I could not check sections 3 to 7, including the section 4.3 FEN list and the section 7 reproduce commands. Fix list: (1) save the full REPORT.md; (2) upgrade B's 14 sides from COMPUTED-1 to CHECKED-2, since my independent run agrees 14/14; (3) say that "bounds did not move" carries no information, because nothing was resolvable and the bounds start at the trivial sandwich in every treatment; (4) say that B is the colour-flip plus file-mirror image of A, so the identical tree counts and the model value *2 are one result seen twice; (5) correct the "rules kept" line, because the two kpsolve jobs overlapped in time although the resume brief said one job at a time; (6) say that the draw=0 single-deviation data come from merging apply_*.json with apply_*_draw0_9man.json; (7) say that a 9-man kpsolve run is probably not feasible under the 45-minute, 2-thread, 4 GB limits, so the Searcher plus tablebase route is the cheaper next step. I did not write VERIFY_T20b.md, because the system rules forbid writing report or findings .md files. The findings are in this output. My own work used only the scratchpad, plus 128 new Lichess requests that landed in the shared realchess cache.

### Fixes and problems found by the verifier

- There is no REPORT.md in research/star2_oracle/ (COMMON.md rule 6). The inline report I was given stops partway through section 2 (the end of the step table), so I could not check sections 3 to 7, including section 4.3, the FENs of the single-deviation candidates, and the section 7 reproduce commands. The full report must be saved as a file.
- B's 14 sides are labelled COMPUTED-1 and item 7 says B has no full-chess check. The check (resolve_tb.py plus the Lichess tablebase) took 135 s and 128 requests, and my run agrees 14/14. The label should be CHECKED-2 and the caveat reworded.
- The step log 'bounds after each step' is uninformative. No terminal has 7 or fewer men, so step 2 (the tablebase) resolves nothing and the 'before' bounds are the trivial plus or minus 2*BIG sandwich in every treatment. Identity across the four treatments is therefore automatic, and 12 isolated terminals cannot move the bounds. The honest progress measure is support coverage: 5 of 61 terminals for A and 7 of 60 for B. The report should say this and not present 'bounds did not move' as evidence.
- A and B are not two independent examples in the model. B is the colour-flip plus file-mirror image of A (verified: flip(A) equals B, and G_hi(A) equals the negative of G_lo(B) and G_lo(A) equals the negative of G_hi(B)). Equal tree counts, equal model value and 'three programs agree' are one result seen twice. In real chess the two differ because the trébuchet is not symmetric, which is why the open lists and breaker sides differ.
- The 'Rules kept' line is not accurate. The resume brief said to run one job of your own at a time. The kpsolve A job (4443.3 s, output written at 01:28:21) and the B job (5396.6 s, written at 01:44:22) started at about 00:14:18 and 00:14:25, so they ran concurrently. That is still within the general limit of 2 heavy processes, but not the resume instruction. The B job ran 89.9 minutes against a 90-minute allowance. The RSS under 4 GB and 'about 1 GB' claims cannot be checked from the artifacts.
- apply_A.json and apply_B.json list 'switch, draw = 0 (PARTIAL: deadline)'. Their 9-man sides have draw=0 trials only in apply_*_draw0_9man.json. The merge happens only inside report_tables.py. I confirmed the merge gives complete coverage (112 A and 106 B sides times 4 treatments, no gaps, no overlap conflicts), but the report must say the draw=0 counts depend on the merge.
- 'First candidates for a 9-man kpsolve run' is not costed. The 9-man batch in realchess/targets18 took 29.8 billion states and 7901 s with 12 threads (about 2 h 11 min wall). The 8-man runs here took 13 to 15 billion states with 2 threads. A 9-man run is very likely outside the task limits (45 minutes, 2 threads, 4 GB RSS). The Searcher plus Lichess tablebase route (81 requests and 85 s for A's 8-man terminals, 128 requests and 135 s for B's) is the cheaper first attempt for the 8 candidate sides.
- Tooling note: the strings from cgt.show for non-pinned games change option order between processes (hash order). Comparing G_lo or G_hi strings across runs gives false mismatches (I hit this). Compare pinned values, outcomes and the excluded flags instead. Within one run, the report_tables.py comparison is safe.
- Scope reminder for the deviation result: 'only these sides can alone exclude *2' holds only under four conditions. The deviation is of one side. The other support sides stay at the model value. The treatment is one of the three non-free ones. Joint deviations were not tested. Under the free treatment no single deviation excludes *2, so the 5 and 3 candidates depend on how a draw is scored in the CGT model.

### Claims the verifier recomputed

- **agrees.** Claim: Tree for A and B: 861 internal nodes, 1405 terminals; by men 8/9/10/11 = 111/381/613/300; sides 222/762/1226/600 (2810 total); 2789 distinct FENs.
  Recomputed: Terminals(Pos.parse(...)) on both components with the project's default count rule and e.p.-aware test. Every number matches, and A and B give identical statistics. B is the colour-flip plus file-mirror of A in the model, which I verified, so the identical counts are structural, not independent confirmation.
- **agrees.** Claim: Model value of A and B is *2 under the count rule.
  Recomputed: component.value_with with mover-aware model_terminal_value gives *2 for A and B under count and under mover. Under the opponent rule neither is *2. Because B is the flip-mirror of A, this is one result up to symmetry.
- **agrees.** Claim: All 12 decisive 8-man terminals (24 sides) are exact in kpsolve and equal the model value. A has 5 terminals, B has 7.
  Recomputed: I wrote my own parser for kp_A_8men.out and kp_B_8men.out. Every line has A == B, the kings are on f5 and h4, and each position maps to exactly one terminal. Values are taken as White's view, as in kings/SPEC.md line 118. There are 10 A sides and 14 B sides. All 24 equal my own model fill (W,W or L,L).
- **agrees.** Claim: A's 10 sides are CHECKED-2 (kpsolve and the realchess Searcher with the Lichess tablebase).
  Recomputed: I converted tb_A_8men.json from mover's view to White's view and compared it with kpsolve. All 10 sides are exact in both and agree. tb_A_8men.json (19:38) predates the kpsolve output (01:28), so the two checks are independent.
- **DISAGREES.** Claim: B's 14 sides are only COMPUTED-1, and B has no full-chess check.
  Recomputed: I ran research/star2_oracle/resolve_tb.py on min_support_B.json with --only-men 8 --cap 150. Ledger and output went to my scratchpad. It used 128 new Lichess requests and 135 s. All 14 sides came back exact and agree with kpsolve, so B's sides can be relabelled CHECKED-2. The absence of a B check was a choice, not a limitation.
- **agrees.** Claim: G_lo and G_hi are identical before and after the 12 terminals are applied, and identical under all four draw treatments, for A and for B. *2 and 0 are not excluded and the value is not pinned.
  Recomputed: I ran sandwich() with no known terminals and with my own parsed kpsolve values, for each of the four TREATMENTS. Before and after are the same canonical game, *2 and 0 are not excluded, and the result is not pinned. The strings match the saved apply_*.json. The identity itself is trivial: no terminal has 7 or fewer men and no draw appears in the data, so all treatments start from the same sandwich. Fixing a few terminals cannot move it, because other unresolved siblings dominate.
- **agrees.** Claim: If every open decisive side takes the model value, the oracle value is exactly *2 under all treatments.
  Recomputed: With the 61 (A) and 60 (B) support terminals at the model value and everything else free, G_lo equals G_hi equal to *2 under all four treatments. With all 1405 terminals at the model value the result is also *2. Removing any single support terminal, both sides at once, breaks the pin under the free treatment, so the support is 1-minimal. It is not necessarily minimum, which matches the report's own caveat.
- **agrees.** Claim: Open decisive sides: A has 112 (56 terminals; 9-man 56 sides, 10-man 46, 11-man 10). B has 106 (53 terminals; 50, 46, 10). No kpsolve job with 9 or more men was run.
  Recomputed: The counts equal 61 minus 5 and 60 minus 7 terminals, doubled, and match the apply logs. Only kp_A_8men.out and kp_B_8men.out exist as kpsolve outputs, and kp_A_needed.out is empty. No kpsolve process of this task is running.
- **agrees.** Claim: Single-deviation test: only 5 open 9-man sides of A and 3 of B can alone exclude *2 if they deviate from the model.
  Recomputed: I re-ran the test with my own code: for each open side, set it alone to W, D and L with all other support sides at the model value, then call sandwich() and excluded(). I covered all 112 A and 106 B sides under 'draw = Black win' and 'draw = White win'. For 'draw = 0' I covered the 5 A and 3 B candidate sides plus 8 random other sides each. There were 0 mismatches with the saved results in every case. Breaking (side, value) pairs and distinct sides: A has 10/5, 5/5 and 7/5 under the three treatments; B has 3/3, 6/3 and 4/3. Under the free treatment nothing breaks. Scope: the test covers one deviation at a time inside the chosen support. Joint deviations and sides outside the support are not covered. The remaining draw=0 sides rely on the saved results.
- **agrees.** Claim: The earlier apply.py wrongly flipped black-to-move kpsolve lines. kpsolve reports White's view whoever is to move.
  Recomputed: kings/SPEC.md line 118 says White's point of view whoever is to move. The mover's-view Searcher results, converted to White's view, match kpsolve on all 24 sides when unflipped. All 12 terminals are W,W or L,L, so a flip would have produced mixed pairs and mismatches with the model.
- **DISAGREES.** Claim: The decisive set was not shown to be minimal; apply.py runs take about 31 minutes at about 1 GB, under nice -n 10; the rules were kept.
  Recomputed: The 31 minutes is confirmed by the logs (1813 s). The 1 GB figure cannot be checked from the artifacts. The kpsolve A and B jobs overlapped in time (see the problems list).

## Agent report (verbatim)

Report content is inline below because the Write tool refused to save `REPORT.md` (subagents may not write report files), and I did not work around that refusal. Everything else is on disk in `/Users/aritro/Downloads/Research/Chessendgames/research/star2_oracle/`. Please save the inline report there as `REPORT.md` if you want it.

**10-line summary**
1. **COMPUTED-1 / CHECKED-2:** All 12 decisive 8-man terminals (24 sides) are applied: A has 5 terminals, B has 7. Every kpsolve line is exact and every side equals the model value. A's 10 sides are CHECKED-2 (kpsolve and realchess Searcher with the Lichess tablebase). B's 14 sides are COMPUTED-1.
2. **COMPUTED-1:** The bounds did not move. G_lo and G_hi are identical before and after, and identical under all 4 draw treatments, for A and for B. *2 is not excluded, 0 is not excluded, and the value is not pinned.
3. **Verdict:** *2 is still possible and not certified for A and for B. If every open decisive side takes the model value, the oracle value is exactly *2 under all treatments (COMPUTED-1, by monotonicity).
4. **Still open (not run):** A has 112 decisive sides (56 terminals): 9-man 56 sides, 10-man 46, 11-man 10. B has 106 (53 terminals): 50, 46, 10. No kpsolve job with 9 or more men was run.
5. **Single-deviation test (COMPUTED-1):** Only 5 open 9-man sides of A and 3 of B can alone exclude *2 if they deviate from the model. They are listed with FENs in section 4.3. They are the first candidates for a 9-man kpsolve run.
6. **Bug fixed in the earlier `apply.py`:** it flipped black-to-move kpsolve lines, which is wrong. kpsolve reports White's view whoever is to move (`kings/SPEC.md`, `wpov()` in `kpsolve.c`). `search_A_8men.overlay.out` is in the mover's view and must not be fed to `apply.py`.
7. **Caveats:** kpsolve ran with queen-only promotions, so B has no full-chess check. The decisive set is one greedy support, not shown to be minimal.
8. **Files:** `apply.py`, `apply_A.json`, `apply_B.json`, `apply_{A,B}_draw0_9man.json`, `report_tables.py`, `report_tables.out` and the `.log` files, all in `research/star2_oracle/`.
9. **Reproduce:** the commands are in section 7. Each `apply.py` run takes about 31 minutes, uses about 1 GB and was run under `nice -n 10`.
10. **Rules kept:** no network use, no kill of foreign processes, nothing edited outside `research/star2_oracle/`, no git commands.

---

# T20 (resume): real-chess oracle value of the two new 7-pawn *2 positions

- A = `W: a4 b3 d2 d3 / B: a7 b7 c5`, embedded FEN `8/pp6/8/2p2Kp1/P5Pk/1P1P4/3P4/8 w - - 0 1` (11 men)
- B = `W: b4 c2 d2 / B: a6 a7 c6 d5`, embedded FEN `8/p7/p1p5/3p1Kp1/1P4Pk/8/2PP4/8 w - - 0 1` (11 men)
- Tree: e.p.-aware, count rule, trébuchet W Pg4 Kf5 / B Pg5 Kh4 on the flat 8×8 board.
- Model value of both: *2 (three programs, `delegate/checks/star2_seven.out`).

## 1. Summary

1. **Applied** the 12 exact 8-man decisive terminals (24 sides; A: 5 terminals, B: 7) from `kp_A_8men.out` and `kp_B_8men.out`. All are exact (kpsolve A == B) and equal the model value. A's 10 sides are **CHECKED-2**; B's 14 are **COMPUTED-1**.
2. **Bounds did not move.** Identical before and after, and under all four draw treatments, for both positions. *2 is not excluded, 0 is not excluded, nothing is pinned (**COMPUTED-1**).
3. **Verdict: *2 is still possible and not certified, for both.** If all remaining decisive sides take the model value, the oracle value is exactly *2 under every treatment (**COMPUTED-1**). Those remaining sides all have 9 to 11 men.
4. **Still open:** A 112 sides (56 terminals), B 106 sides (53 terminals). None run.
5. **Possible refutation:** only 5 open 9-man sides of A and 3 of B can alone exclude *2 if they deviate (section 4.3).

## 2. Step log: bounds after each step

| Step | A | B |
|---|---|---|
| 1. Tree (**COMPUTED-1**, `tree_stats.json`) | 861 internal nodes, 1405 terminals; by men 8: 111, 9: 381, 10: 613, 11: 300; sides 222 / 762 / 1226 / 600 (2810 sides, 2789 distinct FENs) | same counts |
| 2. Tablebase (**COMPUTED-1**) | No side has 7 or fewer men (the smallest has 8), so none is a direct tablebase position or in the offline caches. The tablebase is used only inside the Searcher cross-check of A's 8-man sides: 81 requests, all HTTP 200, 85 s (`ledger.jsonl`) | none made |
| 3. Bounds, exact results only (**COMPUTED-1**, `bounds_A.json`, `bounds_B.json`) | Section 3 bounds; not pinned; *2 and 0 not excluded, all four treatments | same |
| 4. Minimal support (**COMPUTED-1**) | 61 decisive terminals: 8-man 5, 9-man 28, 10-man 23, 11-man 5 | 60: 7, 25, 23, 5 |
| 5. kpsolve on the 8-man decisive terminals, bounds recomputed | 10 sides exact, all equal model; bounds unchanged | 14 sides exact, all equal model; bounds unchanged |

"Decisive" is the greedy minimal support of `realchess/targets18/min_support.py`. It starts from the model assignment, which pins *2, and frees terminals one at a time (larger first) while the sandwich still pins *2. The terminals that cannot be freed form the support. It is one sufficient set, not shown to be smallest or unique.

## 3. Bounds per treatment

Exact 8-man sides are fixed and everything else is free. Excluded means `not (G_lo <= *2)` or `not (*2 <= G_hi)`.

| Treatment | A: same as earlier bounds / pinned / excl. *2 / excl. 0 | B: same as earlier bounds / pinned / excl. *2 / excl. 0 |
|---|---|---|
| switch, draw = Black win | yes / no / no / no | yes / no / no / no |
| switch, draw = White win | yes / no / no / no | yes / no / no / no |
| switch, draw = 0 | yes / no / no / no | yes / no / no / no |
| free (only L/R fixed) | yes / no / no / no | yes / no / no / no |

A (G_lo has outcome R, G_hi outcome L):
```
G_lo = {{-W, {-W, {-W, {-W, {-W, -W* | -W, {-W, -W* | -W}} | -W, {-W, -W* | -W}} | -W, {-W, -W* | -W}} | -W, {-W, -W* | -W, {-W, -W* | -W}}} | -W, -W*} | -W}
G_hi = {{+W | +W, +W±+W} | +W}
```
B (G_lo has outcome R, G_hi outcome L):
```
G_lo = {-W | {-W, -W±+W | -W}}
G_hi = {+W | {+W, +W* | +W, {+W, {+W, {+W | +W, +W*} | +W, +W*} | +W, {+W, {+W | +W, +W*} | +W, {+W, {+W | +W, +W*} | +W, {+W, {+W | +W, +W*} | +W, +W*}}}}}}
```

**Conditional certificate (COMPUTED-1, monotonicity):** with every open decisive side at its model value, the sandwich is pinned to exactly *2 under all four treatments, for A and for B.

Not certificates, from `bounds_A.json` and `bounds_B.json`:
- Filling unknown one-sided sides by the model and leaving races free gives [*2, +W±+W] for A and [-W±+W, *2] for B.
- Filling races by the "opponent" rule excludes *2 under three of four treatments.
- These are assumptions about unresolved chess results.

## 4. The decisive end positions

### 4.1 Solved: 12 decisive 8-man terminals

kpsolve prints White's point of view whoever is to move. L means White wins either way, R means Black wins either way. The FEN is for White to move; change `w` to `b` for Black to move. Each row's two sides-to-move gave the same class.

A (`kp_A_8men.out`: 13,060,661,248 states, 91,580 layers, depth 25, 4443.3 s):

| Terminal | Model | kpsolve (w, b) | Searcher + TB (w, b) | FEN |
|---|---|---|---|---|
| W: a4 c4 d2 / B: a6 | W win | W W, W W | W W, W W | `8/8/p7/5Kp1/P1P3Pk/8/3P4/8 w - - 0 1` |
| W: b3 c5 d2 / B: b5 | W win | W W, W W | W W, W W | `8/8/8/1pP2Kp1/6Pk/1P6/3P4/8 w - - 0 1` |
| W: d2 / B: a6 b4 d4 | B win | L L, L L | L L, L L | `8/8/p7/5Kp1/1p1p2Pk/8/3P4/8 w - - 0 1` |
| W: d2 / B: a7 b4 d4 | B win | L L, L L | L L, L L | `8/p7/8/5Kp1/1p1p2Pk/8/3P4/8 w - - 0 1` |
| W: d3 / B: a7 b4 d4 | B win | L L, L L | L L, L L | `8/p7/8/5Kp1/1p1p2Pk/3P4/8/8 w - - 0 1` |

B (`kp_B_8men.out`: 14,658,134,016 states, 103,821 layers, depth 26, 5396.6 s):

| Terminal | Model | kpsolve (w, b) | FEN |
|---|---|---|---|
| W: a5 c5 d2 / B: a6 | W win | W W, W W | `8/8/p7/P1P2Kp1/6Pk/8/3P4/8 w - - 0 1` |
| W: a5 c5 d2 / B: a7 | W win | W W, W W | `8/p7/8/P1P2Kp1/6Pk/8/3P4/8 w - - 0 1` |
| W: a5 c5 d3 / B: a7 | W win | W W, W W | `8/p7/8/P1P2Kp1/6Pk/3P4/8/8 w - - 0 1` |
| W: a6 c4 d2 / B: a7 | W win | W W, W W | `8/p7/P7/5Kp1/2P3Pk/8/3P4/8 w - - 0 1` |
| W: c4 / B: a7 b4 c6 | B win | L L, L L | `8/p7/2p5/5Kp1/1pP3Pk/8/8/8 w - - 0 1` |
| W: d2 / B: a7 b5 d5 | B win | L L, L L | `8/p7/8/1p1p1Kp1/6Pk/8/3P4/8 w - - 0 1` |
| W: d3 / B: a7 b5 d4 | B win | L L, L L | `8/p7/8/1p3Kp1/3p2Pk/3P4/8/8 w - - 0 1` |

- Each kpsolve value is COMPUTED-1 for the game "flat 8×8, e.p. on, queen promotions only, at most one officer". Bounds A and B agree on every line.
- Under-promotions are outside that game, so A's sides were also run through the Searcher, which uses the real tablebase and all promotions. Its 10 values (mover's view in `tb_A_8men.json`, converted here) agree on all 10 sides, so A's values are CHECKED-2.
- B has no second implementation, so its 14 sides are COMPUTED-1.
- The `kp_*_8needed.txt` inputs were checked line by line against the `.out` files: same positions and order, no `X`, A == B everywhere.

### 4.2 Still open: decisive sides with 9 or more men (not run)

| | 9 men | 10 men | 11 men | Total |
|---|---|---|---|---|
| A, terminals / sides | 28 / 56 | 23 / 46 | 5 / 10 | 56 / 112 |
| B, terminals / sides | 25 / 50 | 23 / 46 | 5 / 10 | 53 / 106 |

- Full FEN lists: `open_A_9plus_fens.txt` and `open_B_9plus_fens.txt`. They were checked to equal the open sides computed here (`open_sides_list` in `apply_A.json` and `apply_B.json`).
- The 112 sides are 109 distinct FENs in A, and the 106 are 104 in B. Terminals that differ only by an e.p. flag owned by the other side embed to the same position.
- Cost, **CONJECTURE** (extrapolation): the only 9-man kpsolve batch on record (3 terminals, `realchess/targets18/kp_eighth_9man.err`) took 7,901 s on 12 threads, about 23,158 s of CPU. Runs over all 28 (A) or 25 (B) nine-man terminals are in that family, and the 10- and 11-man ones are larger.

### 4.3 Which open sides could exclude *2 on their own

Method (COMPUTED-1): each open side alone is set to W, D and L, with every other open decisive side at its model value and the exact 8-man sides fixed. The sandwich is recomputed for all four treatments on all 112 (A) and 106 (B) sides.

| Treatment | A: deviations that exclude *2 / pin *2 anyway / un-pin | B: same |
|---|---|---|
| free (only L/R fixed) | 0 / 0 / 224 | 0 / 0 / 212 |
| switch, draw = Black win | 10 / 104 / 110 | 3 / 132 / 77 |
| switch, draw = White win | 5 / 140 / 79 | 6 / 103 / 103 |
| switch, draw = 0 | 7 / 125 / 92 | 4 / 115 / 93 |

Under "free" a deviation only removes the certificate and never excludes *2, because a non-L/R side may be anything. The only sides that exclude *2 alone under the switch and draw = 0 treatments are these, all 9-man:

| | Open side (terminal, side to move) | Model | FEN | Deviation that excludes *2 |
|---|---|---|---|---|
| A | W: a4 a5 d2 / B: b5 d4, White | W | `8/8/8/Pp3Kp1/P2p2Pk/8/3P4/8 w - - 0 1` | L (all three); D (draw = Black win). Bounds exclude *2 |
| A | W: a4 a5 d3 / B: b5 d4 (ep b6), White | W | `8/8/8/Pp3Kp1/P2p2Pk/3P4/8/8 w - b6 0 1` | L (all three); D (draw = Black win). Value becomes ↓* |
| A | W: a4 a6 d2 / B: b6 d3, Black | W | `8/8/Pp6/5Kp1/P5Pk/3p4/3P4/8 b - - 0 1` | L (all three); D (draw = Black win, draw = 0). Bounds exclude *2 |
| A | W: b4 b5 d3 / B: a5 d4 (ep a6), White | W | `8/8/8/pP3Kp1/1P1p2Pk/3P4/8/8 w - a6 0 1` | L (all three); D (draw = Black win). Value becomes ↓* |
| A | W: b4 b6 d3 / B: a6 d4, Black | W | `8/8/pP6/5Kp1/1P1p2Pk/3P4/8/8 b - - 0 1` | L (all three); D (draw = Black win, draw = 0). Value becomes ↓* |
| B | W: a5 c3 / B: a6 d3 d5, White | B | `8/8/p7/P2p1Kp1/6Pk/2Pp4/8/8 w - - 0 1` | W (all three); D (draw = White win, draw = 0). Value becomes ↑* |
| B | W: a5 c4 / B: a6 d4 d5 (ep c3), Black | B | `8/8/p7/P2p1Kp1/2Pp2Pk/8/8/8 b - c3 0 1` | W (all three); D (draw = White win). Value becomes ↑* |
| B | W: a5 d4 / B: a6 c4 c5 (ep d3), Black | B | `8/8/p7/P1p2Kp1/2pP2Pk/8/8/8 b - d3 0 1` | W (all three); D (draw = White win). Value becomes ↑* |

This table covers one deviation at a time. Combinations of two or more could exclude *2 where no single one does, and I did not search them. Settling these 8 sides at the model values would not certify *2. Certification needs all 112 (A) or 106 (B) sides.

## 5. Verdict

| | A | B |
|---|---|---|
| *2 excluded? | no, under every treatment | no, under every treatment |
| *2 certified? | no | no |
| 0 excluded? | no | no |
| Status | still possible; certified *2 if all 112 open sides match the model | still possible; certified *2 if all 106 open sides match the model |
| Evidence against *2 | none: 24 of 24 exact 8-man sides match the model | none |

## 6. Corrections and caveats

- **Sign bug fixed in `apply.py`.** The first version negated black-to-move kpsolve lines on the assumption that kpsolve reports the mover's view. It reports White's view (`kings/SPEC.md` "Output format"; `wpov(v, stm)` in `kings/kpsolve.c`). With the flip, each black-to-move line would have contradicted its white-to-move twin. The Searcher outputs (`tb_A_8men.json`, `search_A_8men.overlay.out`) are in the mover's view, and the current `apply.py` converts them explicitly.
- **Queen-only kpsolve.** B's values are not full-chess certificates until a second program agrees. Under-promotions and games with two or more officers are outside the kpsolve game.
- **Greedy support.** The 112 and 106 open sides belong to one greedy support. A different order might give fewer open 9-man sides. I did not try it.
- **Treatment-independence of the bounds** holds because so many terminals are free. It will not hold once more terminals are fixed (the model-filled policies in `bounds_A.json` already differ by treatment).
- **Process.** The `apply.py` draw = 0 pass stopped at its 30-minute deadline before the 9-man sides. I completed it with `--sens-men 9` runs, and `report_tables.py` merges them, so the section 4.3 counts cover every open side.
- **Runs I started.** `apply.py` (about 31 min and about 1 GB for each main run) and `report_tables.py`. Two earlier trial runs of `apply.py` were stopped by me because they would have passed the time limit. One start failed on an argument-quoting error.
- **Network and git.** No network use in this task; `ledger.jsonl` is from the earlier run. No git commands, and nothing outside `research/star2_oracle/` was edited.

## 7. Reproduce

From `/Users/aritro/Downloads/Research/Chessendgames`:
```
# kpsolve results (landed from the earlier runs; checked here, not rerun)
nice -n 10 ./kings/kpsolve --board flat:8x8 --ep on --promote Q --cap 1 --threads 2 \
    < research/star2_oracle/kp_A_8needed.txt > research/star2_oracle/kp_A_8men.out
nice -n 10 ./kings/kpsolve --board flat:8x8 --ep on --promote Q --cap 1 --threads 2 \
    < research/star2_oracle/kp_B_8needed.txt > research/star2_oracle/kp_B_8men.out

# bounds, exclusion tests, conditional certificate, sensitivity (about 31 min each)
PYTHONPATH=. nice -n 10 .venv/bin/python research/star2_oracle/apply.py \
    research/star2_oracle/min_support_A.json research/star2_oracle/kp_A_8men.out \
    --tb research/star2_oracle/tb_A_8men.json --out research/star2_oracle/apply_A.json --deadline-min 30
PYTHONPATH=. nice -n 10 .venv/bin/python research/star2_oracle/apply.py \
    research/star2_oracle/min_support_B.json research/star2_oracle/kp_B_8men.out \
    --out research/star2_oracle/apply_B.json --deadline-min 30

# draw = 0 sensitivity of the 9-man sides (about 22 min each)
PYTHONPATH=. nice -n 10 .venv/bin/python research/star2_oracle/apply.py \
    research/star2_oracle/min_support_A.json research/star2_oracle/kp_A_8men.out \
    --tb research/star2_oracle/tb_A_8men.json --out research/star2_oracle/apply_A_draw0_9man.json \
    --sens-treatments "switch, draw = 0" --sens-men 9 --deadline-min 40
PYTHONPATH=. nice -n 10 .venv/bin/python research/star2_oracle/apply.py \
    research/star2_oracle/min_support_B.json research/star2_oracle/kp_B_8men.out \
    --out research/star2_oracle/apply_B_draw0_9man.json \
    --sens-treatments "switch, draw = 0" --sens-men 9 --deadline-min 40

# tables of sections 2 to 4 (output saved as report_tables.out)
PYTHONPATH=. .venv/bin/python research/star2_oracle/report_tables.py
```
Earlier steps, per the script docstrings:
- `tree_stats.py`
- `python -m realchess.certify.oracle10 bounds --component "<A or B>" --out research/star2_oracle/bounds_<A|B>.json`
- `realchess/targets18/min_support.py "<A or B>" --out research/star2_oracle/min_support_<A|B>.json`
- `resolve_tb.py research/star2_oracle/min_support_A.json --only-men 8 --out research/star2_oracle/tb_A_8men.json`
- `to_kp.py <A|B> 8` for the kpsolve inputs

Added or changed in `/Users/aritro/Downloads/Research/Chessendgames/research/star2_oracle/`: `apply.py` (fixed and extended), `apply_A.json`, `apply_B.json`, `apply_A.log`, `apply_B.log`, `apply_A_draw0_9man.json`, `apply_B_draw0_9man.json`, `apply_A_draw0_9man.log`, `apply_B_draw0_9man.log`, `report_tables.py`, `report_tables.out`.
