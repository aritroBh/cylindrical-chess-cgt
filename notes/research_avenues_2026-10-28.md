## Summary (what is established, biggest gaps)

1. **Solvers are trustworthy.** kpsolve agrees with kings/ref on 1.42M positions and with the KPK atlas on all 326,640 cylinder positions. cylcgt agrees with sumtest on 4.97M predictions. Lichess agrees on 42 of 45 positions, and the other 3 are inside kpsolve's bounds (CHECKED-2).
2. **The model is proved correct inside its own conditions.** Theorem 1.14 (V1)-(V3) and Prop 1.15 are PROVED. Theorem 2.7 holds only in the model P (first promotion wins), so each chess claim still needs its own check. Spare king tempi give on/off/dud values (Thm 3.4).
3. **Measured agreement with real chess is decent but scattered.** Small boards: 341/500 = 68%, of which 107 failures are king effects and 52 are convention failures. One flat 8x8 tree: 91-95% of 295 nodes. Suite: 78% of 233 positions. The samples differ, none is an enumerated class, and none has confidence intervals.
4. **Known real-chess anchors.** 1/8 is exact with queen-only promotion and frozen kings (C1). The QRBN cap-1 rerun of the 8-man positions has finished (`realchess/targets18/qrbn_8man.out` is identical to `kp_eighth_8man.out`, but that run only met its two bounds). The cap-2 QRBN run was killed by a reboot (`qrbn_cap2.out.tmp` is empty). For the seven-pawn *2 (A/B), all 12 decisive 8-man end positions agree with the model, while 168 (A) and 159 (B) end positions with 9 or more men are open.
5. **Ring and nimber theory is strong, but only in the whole-board model.** Wall and ring families are [AI]/PROVED whole-board. Sum-model values are checked only up to n≈12-14. No *4 has been found.
6. **Gap: no headline accuracy number** over a closed, enumerated class with a stated denominator.
7. **Gap: failures are not attributed by mechanism.** The 34 "passer does not win at once" failures on 7x6 and the 3 P4 refutations (H*, H*2, H0) have never had their causes examined.
8. **Gap: no predictive rule for when the trebuchet unfreezes.** At the 8-man nodes, 1292 of 1431 king moves are unresolved. In the suite, 41 of 449 king moves draw and 7 win.
9. **Gap: additivity has never been tested against explicit-king chess on sums.** There is no room for two components on flat 8x8, and the 56,402 K12 e.p. roots were excluded.
10. **Gap: draws have no principled value.** "Draw = 0" gives an interval and "Black must win" is unpinned. Separately, `notes/novelty_check/REPORT.md` §5 wrongly says misère Dawson is "solved". It is open (this is a fix for the user; this task was read-only).

## Ranked avenues (deduplicated across the 4 surveys)

Weighting: a = justifies or tests the model ×3, b = novelty ×2, c = feasibility ×2, d = uses existing tools ×1. Maximum total is 40.

| Rank | Avenue | a | b | c | d | Total | Why |
|---|---|---|---|---|---|---|---|
| 1 | Exhaustive agreement census on closed small-board classes, with Wilson CIs | 5 | 3 | 5 | 5 | 36 | Gives the missing headline accuracy number, with a stated denominator |
| 2 | Smallest-counterexample ladder for each convention (C1-C5), flat vs cylinder | 5 | 4 | 4 | 4 | 35 | Shows each of (V1)-(V4) is necessary, using named minimal examples |
| 3 | Mechanisms behind the 34 V2 failures, plus a square-rule corrected passer test | 5 | 3 | 4 | 5 | 34 | The cheapest route to a corrected model |
| 4 | When does the trebuchet unfreeze: (V3) margin, local criterion, P4 diagnosis | 5 | 4 | 3 | 4 | 33 | The central bridge from the model to chess. It could yield a (V5) condition |
| 5 | Explicit-king test of the sum theorem on cylinders, plus the 56,402 e.p. K12 roots | 5 | 4 | 3 | 4 | 33 | The only possible real-chess evidence for additivity |
| 6 | Offline multi-target flat 8x8 census, ranking the race rules empirically | 4 | 2 | 5 | 5 | 31 | Independent flat accuracy from zero new web traffic |
| 7 | Draw-aware model: loopy/affine values for draws and king groups | 4 | 5 | 3 | 3 | 31 | Draws are the largest outcome class the model does not account for |
| 8 | Positions A/B: resolve the 9-11-man end positions, Sandwich bounds | 4 | 5 | 2 | 4 | 30 | Would decide whether the first real *2 holds |
| 9 | Sum-model (not whole-board) values of every ring family, for all n | 3 | 4 | 4 | 5 | 30 | Either upgrades the ring theory or finds where the sum model fails |
| 10 | Full-chess 1/8: finish the cap-2 QRBN run (cap-1 is done and matches) | 4 | 4 | 2 | 5 | 29 | One step from a full-chess CGT value. Needs about 20 GB and 16 h |
| 11 | Engine vs model vs exact solver, accuracy against number k of star components (ChessSums) | 2 | 4 | 4 | 5 | 27 | A benchmark that does not exist yet. The current suite is too easy |
| 12 | Nim-sum theorem for separated cores, with a coupling criterion | 2 | 4 | 4 | 5 | 27 | Narrows the *4 search and gives structural theory |
| 13 | Independent 8-man check with Lichess Op1 (flat only, needs user OK) | 4 | 4 | 2 | 2 | 26 | A third-party oracle. Bulk traffic needs approval |
| 14 | Rigorous thermography with BIG as a parameter | 2 | 3 | 4 | 4 | 24 | Upgrades a weak C1 section |
| 15 | Möbius pawn atlas and sum safety across the twisted seam | 2 | 4 | 3 | 4 | 24 | Tests the model where orientation breaks |
| 16 | Locality / window lemma, making the pumping proofs uniform | 1 | 4 | 4 | 4 | 23 | Turns the T_n/S_n C1 results into PROVED |
| 17 | Learning CGT sums (Z2^m DeepSets, circular-padded CNN) | 1 | 3 | 5 | 4 | 23 | ML-workshop result |
| 18 | Elkies cyclic-word game, plus a ring-rule analogue | 1 | 4 | 4 | 4 | 23 | Never studied |
| 19 | Resolve the star2_frontier C-mask vs cylcgt discrepancy | 2 | 1 | 5 | 5 | 23 | A cheap fix of a C1 inconsistency |
| 20 | Repair the twisted-board tablebases (ray overflow), with the ray rule as a variable | 1 | 2 | 5 | 5 | 22 | Fixes results computed on corrupted arrays |
| 21 | Primitive *4 by mex-guided search | 1 | 5 | 2 | 4 | 21 | Long shot with a high payoff |
| 22 | Small dyadics and open Elkies values on wider boards and cylinders | 1 | 4 | 3 | 4 | 21 | Widens the census scope |
| 23 | Dawson on 4xn, 5xn and Möbius: debris decomposition | 1 | 3 | 4 | 4 | 21 | Extends the 3xn theory |
| 24 | Cylinder ring atlas C5-C8 with 6-8 pawns | 1 | 3 | 3 | 5 | 20 | Where cylinder-only values would appear |
| 25 | Misère Dawson quotient (Q33 and beyond) | 1 | 5 | 1 | 4 | 19 | Open for 90 years, low odds |
| 26 | Five-man pawnless cylinder tablebases | 1 | 3 | 3 | 4 | 19 | Practical, but outside the model |
| 27 | Cylinder perft and circular-padded CNN | 1 | 2 | 4 | 3 | 18 | A useful artefact for the community |
| 28 | More ranks (9-12), and a torus pawn game | 1 | 3 | 3 | 4 | 17 | Needs a design decision from the user (the torus needs loopy semantics) |

All paths below were checked with `ls`. The proposed output folders do not exist yet.

**Common resource rules for every brief:**
- At most 2 heavy processes, each started with `nice -n 15`, each under 4 GB RSS (check with `/usr/bin/time -l`).
- Never use pkill, killall or pattern kills. Stop only your own PID, recorded in a `.pid` file.
- Compress raw output when the job is done, and keep logs in `logs/`.

---

### 1. Exhaustive agreement census → `research/agreement_census/`
- **Goal:** one headline accuracy number for the default model (e.p.-aware, count rule), measured over an enumerated class.
- **Question:** take every W≤2/B≤2 pawn placement (then ≤3/≤3 where it fits) beside a frozen trebuchet, both sides to move, on cyl:4x4, cyl:5x5, flat:5x6 and cyl:6x6. What fraction does the model predict correctly against exact kpsolve? Give a Wilson 95% CI per cell, split by outcome class L/R/N/P × race/non-race × pawn count × promotion set (Q vs QRBN).
- **Method:**
  1. Diff `kings/results/exp_cyl6x6_epon_Q.jsonl` against `exp_cyl6x6_epon_QRBN.jsonl`. This costs no compute.
  2. Re-aggregate `exp_*_conv.jsonl`. The files hold 42 + 42 + 812 = 896 components.
  3. Generate the full position sets for cyl:4x4 and cyl:5x5 with `kings/experiment.py`.
  4. Run `kings/kpsolve --board cyl:5x5 --ep on --cap 2 --threads 2`, then repeat with `--frozen`.
  5. Compute the model side with `kings/conventions.py` (cylcgt).
  6. Count races as their own class, not as excluded rows. Skip cyl:7x6 (cap 2 needs about 9 GB).
- **Success:** a TSV with one row per position and a summary table with CIs. Each mismatch is labelled king effect (frozen = model ≠ real) or convention (frozen ≠ model). The 6x6 and 5x6 figures reproduce the published 13/26 and 23/26.
- **Read first:** `kings/REPORT.md` §4, `kings/experiment.py`, `kings/analyze.py`, `kings/conventions.py`, `kings/results/exp_cyl6x6_epon_Q_summary.json`.
- **Agent:** a Claude agent running existing tools, plus a 30-line aggregation script. The census itself is a short compute job (well under 1 CPU-hour per board).

### 2. Smallest counterexample per convention → `research/convention_ladder/`
- **Goal:** a minimal-counterexample table showing each of (V1)-(V4) is necessary.
- **Question:** for each convention, find the position with fewest men on the smallest board where toggling only that convention flips the real result. The conventions are: C1 passer wins at once; C2 race rule (count / mover / opponent); C3 e.p.-aware test; C4 frozen kings; C5 stalemate = loss. Is the answer the same on flat and on cylinder?
- **Method:**
  1. Enumerate by increasing man count (2-6 pawns plus the trebuchet) on cyl:4x4, cyl:5x5, flat:4x5 and flat:5x5.
  2. For each position compute the cylcgt class under 3 race rules × e.p. on/off, plus `kpsolve --frozen` and plain kpsolve, all at cap 2, Q and QRBN.
  3. Record the first instance per category.
  4. Seed the search with the failure lists in `kings/results/FAILURES.md` and `exp_cyl7x6_epon_Q_conv.jsonl`.
  5. Re-verify every minimal example with `kings/ref/solve.py`.
- **Success:** a table with one row per convention: the minimal position (FEN), board, man count, model value, real value, and confirmation from the second solver. Report it even if some minima coincide with lemma L4.
- **Read first:** `kings/results/FAILURES.md`, `kings/conventions.py`, `kings/ref/solve.py`, `kings/theory/LOOPY.md`.
- **Agent:** an external CLI agent (Codex) writing the enumerator independently. A Claude agent then cross-checks it with kings/ref.

### 3. Mechanisms behind the 34 V2 failures, and a corrected passer test → `research/v2_mechanisms/`
- **Goal:** find out whether a computable local test repairs (V2).
- **Question:** in the 34 7x6 components where the model says ±BIG but frozen-king play disagrees, which mechanism applies? Candidates: the king catches the pawn, stalemate, the passer is captured, a blockade, the promotion square is covered, checks during a race, or underpromotion. Does a square-rule or promotion-certificate test remove most of the 52 convention failures?
- **Method:**
  1. Extract the 34 records from `kings/results/exp_cyl7x6_epon_Q_conv.jsonl`. No 7x6 diagnosis file exists; only 6x6 and 5x6 have one.
  2. Run `kpsolve --board cyl:7x6 --cap 1 --moves --frozen` on each root, one at a time. Cap 1 gives two bounds; escalate to cap 2 only for roots that fit under 4 GB.
  3. Read the line of play up to the first passer and label the mechanism with a script plus a manual check.
  4. Implement the corrected test in a scratch copy of `conventions.py` inside the new folder. Do not edit the original.
  5. Re-score all 500 testable components and report the change.
- **Success:** a mechanism histogram summing to 34, plus the mismatch count before and after the corrected test.
- **Read first:** `kings/REPORT.md` §4-6, `kings/results/exp_cyl6x6_epon_Q_diagnosis.jsonl` (the format to copy), `kings/analyze.py`, `kings/results/analyze_7x6.log`.
- **Agent:** a Claude agent running existing tools.

### 4. When does the trebuchet unfreeze? (V3) margin and P4 diagnosis → `research/trebuchet_unfreeze/`
- **Goal:** a predictive local criterion for "the frozen trebuchet really is 0 in chess", and the cause of the P4 refutations.
- **Question:**
  - (a) Which single rule change restores the convention in the 3 refuted P4 contexts (H*, H*2, H0)? The options are QRBN instead of Q, stalemate scored differently, or seam checks.
  - (b) Over the suite and over sampled small-board positions, does a geometric feature predict when a king move draws or wins? Candidate features: king-to-component distance, race length, reserve tempi, and the horizon h.
- **Method:**
  - (a) Rerun `kings/positions/theory_P4_cap2.txt` with `kpsolve --board cyl:7x6 --cap 1`, varying Q/QRBN and `--moves`. Compare with `kings/results/theory_P4_cap2_moves.txt` and the K23 data.
  - (b) Run `kpsolve --board flat:8x8 --cap 1 --moves` on `engine/suite/cgt_disagree.epd` and `cgt_verified.epd`, keeping only the ≤7-man trebuchet positions. Check memory on a single position first. Use `engine/suite/tbcache` and make no new Lichess requests.
  - Then sample 2,000 trebuchet + component positions on cyl:6x6 and fit one-feature and two-feature rules.
- **Success:**
  - (a) A named cause for each of the 3 refuted contexts.
  - (b) A rule with stated accuracy, a confusion matrix, and the smallest counterexample per h.
- **Read first:** `kings/theory/LOOPY.md` (rows P2.10(b), P4, P4.3), `kings/results/PREDICTIONS.md`, `kings/delegate/out/K23/summary.json`, `kings/delegate/out/K20`, `engine/suite/README.md`.
- **Agent:** a Claude agent running existing tools. Part (b) sampling is a moderate compute job.

### 5. Explicit-king sum test on cylinders → `research/sum_truth_cyl/`
- **Goal:** the first real-chess evidence that component values add.
- **Question:** take pairs of non-race components that each match the model on their own. Does the outcome class of the CGT sum (sum_safe True) match exact kpsolve with real kings on cyl:8x6? Separately, do the 56,402 excluded K12 e.p. roots show any disagreement?
- **Method:**
  1. Pick 50 random pairs from the matching rows of `kings/results/exp_cyl7x6_epon_Q_conv.jsonl` and embed them in cyl:8x6 beside the trebuchet.
  2. Compute the cylcgt sum value.
  3. Run `kpsolve --board cyl:8x6 --cap 1` (bounds), and run cap 2 only on positions that fit under 4 GB.
  4. Separately, regenerate the e.p. roots with `kings/delegate/out/K12/gen.py` and check them with `checker.py` in e.p. mode.
- **Success:** a pair-level agreement table. Every disagreement is classified as a component error, a sum (interaction) error, or a king effect. Also a pass/fail count for the e.p. roots.
- **Read first:** `kings/delegate/out/K12/REPORT.md`, `sumtest/REPORT.md`, `kings/delegate/out/K20`, `cylcgt/pawns.py`.
- **Agent:** a Claude agent running existing tools. This is a long compute job, so run it as a pilot first.

### 6. Offline multi-target flat 8x8 census → `research/flat_xtarget_census/`
- **Goal:** a flat-board accuracy estimate that does not rest on the A2 tree alone, and an empirical ranking of the race rules.
- **Question:** across the 1/8 and tiny(1) targets, positions A/B and the refuted *2 candidates, what are the agree, disagree and draw counts per end-position side and per node? Break them down by race rule (count / mover / opponent) × passer test (textbook / e.p.-aware). Which features predict disagreement?
- **Method:**
  1. Run `realchess/compare_nodes.py` and `final_summary.py` with `solve_candidate.py --offline`, using the `realchess/kb.py` cache, `realchess/targets18/` and `research/star2_oracle/`.
  2. Make zero web requests. Fail closed on any cache miss.
  3. Fit a logistic or decision-stump summary over man count, a-file pawns, race, and e.p. availability.
- **Success:** a per-target table, a rule ranking with CIs, and a reproduction of the A2 figures (268 agree / 14 disagree / 13 draws).
- **Read first:** `realchess/REPORT.md`, `realchess/kb.py`, `realchess/compare_nodes.py`, `realchess/results/comp_Wa2c2_Bb7d7_nodes_vs_model_offline.json`.
- **Agent:** a Claude agent running existing tools. Light CPU.

### 7. Draw-aware model with loopy values → `research/draw_model/`
- **Goal:** replace the three ad-hoc draw treatments with a principled one.
- **Question:** score draws three ways: (i) as 0, (ii) as dud, (iii) as {on|off}, assigned by which side can shuttle (Thm 3.4). Which treatment best reproduces the 13 real-draw nodes, the 3 draw terminals, the 6 proven drawing king moves, and the drawing king moves in the suite? Does it pin the A2 oracle value to a single value?
- **Method:**
  1. Collect the draws from `realchess/results/comp_Wa2c2_Bb7d7_*` and from `engine/suite/results.json`.
  2. Run `kpsolve --moves` on each draw to read off the shuttle structure.
  3. Write a scratch scorer, with `realchess/oracle_value.py` as the base, using loopy sum rules from LOOPY T3.7/T3.8.
  4. For the K4 K+P-vs-K placements, cluster the (onside, offside) pairs.
- **Success:** the reproduction rate of each treatment, and either a single oracle value under (iii) or a proof that (iii) is ill-defined there.
- **Read first:** `kings/theory/LOOPY.md` (Thm 3.4, T3.7, T3.8), `kings/delegate/out/K4`, `realchess/oracle_value.py`, `realchess/REPORT.md` (the draw-treatment section).
- **Agent:** an external CLI agent (OpenCode or Kilo) writing the loopy scorer independently. A Claude agent supplies the data.

### 8. Positions A/B end positions with 9 or more men → `research/star2_AB_ends/`
- **Goal:** decide whether the seven-pawn *2 holds in real chess.
- **Question:** how many of the 168 (A) and 159 (B) open end positions with 9 or more men agree with the model? Do the Sandwich bounds O⁻ and O⁺ pin the value at *2, or exclude it?
- **Method:**
  1. Sort `research/star2_oracle/open_A_9plus_fens.txt` and `open_B_9plus_fens.txt` by man count and remaining pawn moves.
  2. Confirm the board embedding from `research/star2_oracle/REPORT.md` and `to_kp.py`: flat 8x8 if the tree is flat.
  3. Run `kings/kpsolve --board flat:8x8 --ep on --cap 1 --threads 2` on the 9-man positions one at a time, measuring the memory of the first one. If a single position exceeds 4 GB, stop and report it to the user rather than continue.
  4. Recompute the bounds with `research/star2_oracle/apply.py` and `min_support_*.py`, so that only the essential positions need to be solved.
- **Success:** each essential end position labelled, updated `bounds_A.json` and `bounds_B.json` written in the new folder, and a verdict: *2, not *2, or still open with the remaining count.
- **Read first:** `research/star2_oracle/REPORT.md`, `research/star2_oracle/min_support_A.json`, `realchess/pin.py`, `realchess/targets18/apply_kpsolve.py`.
- **Agent:** a long compute job. Hand the heavy positions to Codex under the delegation rule, with the no-pkill rule in its brief.

**Notes outside the top 8:**
- Avenue 10 (1/8 with QRBN) is half done. The cap-1 QRBN run finished in 5776 s, 2.4e10 states, and its output is identical to the queen-only run. Only the cap-2 run is left, at about 20 GB or more. Ask the user to schedule it on a clear machine.
- Avenue 13 (Lichess Op1) needs the user's OK for bulk traffic.
- Avenue 28 (torus pawns) needs a design decision from the user.
- The linked session "Replicate 4-man cylinder/torus tablebases" stopped on a session limit (it resets at 4:30am America/Chicago). It was not retried here.