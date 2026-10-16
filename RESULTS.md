# Results so far (2026-10-16)

Plan: [RESEARCH_PLAN.md](RESEARCH_PLAN.md). This page lists what the 2026-10-15/16 run established and how
strongly.
- **Verified** means two independent implementations agree **and** adversarial checkers could not break the
  claim. Every checker so far was written by a Claude model; the OpenCode route to a non-Claude implementation
  failed.
- **Computed once** means one program produced the number.
- **Proved** means one model wrote a proof. No second model or human has re-derived it yet.

**Conventions (decided 2026-10-16).**
- A pawn that can still be taken en passant is **not** passed: `cylcgt.pawns.PASSED_RESPECTS_EP = True`.
  - The fix is on branch `ep-aware-passed`. It will be merged into `main` when the resumed workflow ends; until
    then the main checkout still runs the old test, so that earlier claims stay reproducible.
  - Results below that predate this switch are marked *(textbook test)*.
- Kings are to be modelled explicitly (plan item A8, in progress).

## 1. The \*2 question (Elkies' open problem): the candidate does not survive

The candidate was `W a2 c2 / B b7 d7` on files a–d, frozen by a trébuchet (W g4 / B g5, WK f5, BK h4).

| Check | Result | Status |
|---|---|---|
| Value under the paper's convention, textbook passed test | \*2 under race rules "count" and "mover"; **0** under "opponent". The same with e.p. off | verified (cylcgt, `sumtest/`, Codex rules in `atlas/flat8/census`, `lemmas/`) |
| Value under the adopted convention (e.p.-aware passed test) | **{2±1 \| −2±1}** (mean 0, temperature 2), not \*2. Mechanism: a2–a4 is met by b4×a3 e.p. | verified: cylcgt now agrees with `sumtest/`'s e.p.-aware mode on all 55,195 test positions (§4) |
| Robustness of the \*2 to the race rule | only 4 of its 224 race positions change the value when flipped alone; all come after a capture. A 6-position certificate fixes \*2 whatever the other races do | verified (`atlas/flat8/certificate.json`, `lemmas/` L4.2) |
| Sum model vs whole-board game | equal: the tree never splits into components before a passer (Theorem 2.3) | proved |
| 8×8 embedding geometry (kings f5/h4) | no checks, no stalemate, every king move drops that side's g-pawn | proved; exhaustive check |
| Real chess, both sides to move (Lichess 7-man tablebase + exact search) | the side to move wins (outcome N), as \*2 predicts | proved by certificate (`realchess/results/cert_root_*.json`) |
| Real-chess value: the pawn tree with tablebase results at its end positions | **excluded from being \*2.** Of 65 end positions resolved, 3 are first-player wins and 2 are draws. The model scores all 5 as won for one side, and one flips from a Black win to a White win | computed once (`realchess/results/comp_Wa2c2_Bb7d7_oracle_pure.json`); *final real-chess report pending* |
| The same FEN on the 8-file cylinder | the freeze fails: 1.a3 checks Kh4 across the seam. No \*k (k ≥ 2) with ≤ 5 pawns can be frozen on the 8-file cylinder (0 of 40 placements) | computed once (`atlas/cylinder/`) |

**Why it fails.** The convention "first passed pawn wins" breaks in three places:
- **En passant.** A pawn that double-steps past an enemy pawn counted as passed before the opponent's legal
  e.p. capture. This is now fixed in cylcgt, and the \*2 goes away with it.
- **Frozen kings.** In real chess the trébuchet kings are not always frozen. Across 94 tablebase-checked
  positions, 41 of 449 king moves draw and 7 win (`engine/suite/`).
- **Race rules.** None of count, mover or opponent is exact chess. `notes/lemmas.md` L4 gives a forced-win
  counterexample for each.

**Searching for other \*k (flat 8-rank boards, widths 1–4, up to 6 pawns, 231,071 positions).**
- *Textbook test:* the only \*k with k ≥ 2 is the candidate above. No \*3 or \*4 occurs. No \*2 holds under all
  six race/e.p. settings. Three more \*2s exist, each under a single non-default setting
  ([atlas/flat8/REPORT.md](atlas/flat8/REPORT.md); verified two ways).
- *E.p.-aware test (count rule; computed once, `atlas/flat8/compare_ep_aware.out`):*
  - **No \*k with k ≥ 2 occurs anywhere in scope.** The nimber census goes from 6,470 zeros, 3,891 stars and one
    \*2 to 6,724 zeros, 4,042 stars and no \*2.
  - 21,441 of the 231,071 values change, 4,068 of them in outcome.
  - So within flat boards of ≤4 files and ≤6 pawns, the only route to \*2 was the e.p. artefact.

**What this means.** A \*2 made only of kings and pawns on 8×8 is still open. The negative result is
publishable: it shows exactly where the convention breaks. Real-chess certification of other candidates is
*pending*.

## 2. Mating without corners: 4-man tablebases on the cylinder and torus (verified)

Two independent solvers agree on every position of all 24 tables, about 607 million values, for both sides
to move ([tablebase/replica/REPORT.md](tablebase/replica/REPORT.md)).

| Material (cylinder 8×8) | White to move: share won | Longest mate (moves) |
|---|---|---|
| KQK | 100% | 10 |
| KRK | 2.80%: **no forced mate** | 3 |
| KBBK, opposite-coloured bishops | **100%** | **14** |
| KBNK | 0.0245%: **draw** | 2 |
| KNNK | 0.0077% | 1 |
| KRBK | 99.74% | 13 |
| KRRK | 100% | 8 |
| KQRK | 100% | 5 |

- **Torus.** KQ, KR, KBB, KBN and KNN against a lone king are all 0% won, and KRB vs K is 0.022%.
- **Muller.** The bishop pair forcing mate on the cylinder contradicts H.G. Muller's published claim.
- **Novelty.** We found no earlier tablebase for these boards.
- **King and pawn vs king** (one implementation, `atlas/cylinder/kpk`). On the cylinder the classic flat
  rook-pawn draw (Ka6, Pa5 vs Ka8) is a win.

## 3. The 2025 paper, re-audited (verified)

A blind re-transcription of every diagram matches the solver's input on every pawn square. A pixel scan
confirmed it independently. The kings, and diagrams 2.3 and 5.1, were checked against the images only
([notes/diagram_audit.md](notes/diagram_audit.md)). Three verifiers checked each audit claim. Corrected
verdicts are in [notes/audit.md](notes/audit.md):
- **Correct:**
  - 2.1, 2.2, 2.3, 3.2, 4.1, 4.3;
  - 5.1, the cylinder trébuchet, a mutual zugzwang **only because of the seam**;
  - the 7.1 c- and f-files, and the 7.2 king zugzwang.
- **Correct only with en passant:** 3.1.
- **Wrong:**
  - 4.2 is one rank off.
  - 7.1 a/h is {+W \| \*}, not 1.
  - 7.2's pawn part is not ±1.
  - 7.3 is decided at move 0.
  - 7.3's {c,d} part is tiny(1), not 1.
  - §1's knight squares are wrong.
- **§8, Dawson's chess, is wrong in three ways** (verified, `dawson/`):
  - its move rule allows no first move;
  - its Grundy recurrence matches the true values at only 31 of n = 0..300;
  - its cylinder outcomes are wrong for 56 values of n ≤ 300.

  Replacement text: `dawson/section8_corrected.tex`.

Every value in the audit is **unchanged** under the e.p.-aware convention (re-run 2026-10-16).

## 4. The solver itself

- **Agreement with an independent solver** (verified). `cylcgt` agrees with a from-scratch brute-force solver
  (`sumtest/`) on every outcome prediction. The test set:
  - 55,195 positions (≤2 pawns a side, 3–5 files), × 3 race rules × 15 reference games;
  - e.p. on: 2,483,775 predictions under the adopted e.p.-aware test (both sum modes) and the same number
    under the textbook test;
  - e.p. off: 2,483,775 predictions.
- **Single components.** It agrees with Codex's whole-board minimax on 1,070/1,070 of them (`crosscheck/`).
- **Three defects found, all fixed or documented:**
  - **En passant in the passed-pawn test.** Fixed: `PASSED_RESPECTS_EP`.
  - **`sum_safe()` is a heuristic, not a certificate** (checked two ways, `notes/lemmas.md` L2.2).
    - Example: `W b2 d4 g3 h5 / B a7 c7 f7 g4` on the 8×8 cylinder (e.p. off) passes, yet the sum model gets
      the winner wrong.
    - The proved replacement is the "hereditarily sum-safe" test (`lemmas/common.py`, Theorem 2.1). All 1,297
      such positions in a random sample of 1,500 agree.
  - **An e.p. right can survive moves elsewhere** in a multi-component sum. The sum is exact only when no
    position with two or more components carries a usable e.p. right (condition (E), L1.6–1.7).
- **Not a solver defect, a misuse.** The partizan values that `cylcgt/dawson.py` prints are not additive. The
  Grundy value of octal 0.137 is the correct invariant (L5.4).

## 5. Engines

- [engine/ENGINES.md](engine/ENGINES.md) makes 16 predictions about how Stockfish and Lc0 search fails on
  zugzwang, tempo battles and nimbers, and designs 8 experiments.
  - Stockfish's null-move pruning never fires in king-and-pawn endings, because it requires pieces.
  - Reverse futility pruning is the predicted zugzwang-blind cut.
- **Test suite.** Both files are tablebase-checked legal 8×8 positions:
  - `engine/suite/cgt_verified.epd`: **181 positions** whose winning moves follow from CGT and are confirmed
    by the Lichess tablebase;
  - `engine/suite/cgt_disagree.epd`: the 52 positions where CGT and the tablebase disagree.
- **Stockfish 19 on the suite.** Official release `sf_19`, built locally in `engine/vendor/` (git-ignored);
  1 thread, 64 MB hash, no tablebases. Runs and analysis are in `engine/runs/`.
  - **It solves all 233 positions at 100k nodes, and 232/233 already at 1k nodes.** At ≤7 men these
    positions are easy for a modern engine. The CGT-versus-engine contrast has to come from larger sums,
    beyond the tablebase, where only CGT gives ground truth. That is the ChessSums benchmark.
  - **At shallow depth, accuracy depends on the CGT value class.** The table gives the share of Stockfish
    evaluations that match the tablebase result:

| CGT class | n | depth 1 | depth 2 | depth 4 | depth 6 | depth 8 | depth 12 |
|---|---|---|---|---|---|---|---|
| hot (±BIG switch) | 68 | 81% | 78% | 91% | 97% | 99% | 100% |
| number | 57 | 79% | 81% | 84% | 93% | 95% | 98% |
| switch | 37 | 73% | 78% | 89% | 100% | 100% | 100% |
| **infinitesimal** | 27 | **30%** | **26%** | **59%** | 85% | 100% | 100% |
| other tame | 20 | 60% | 50% | 75% | 95% | 100% | 100% |
| **nimber** | 17 | **53%** | 65% | 88% | 100% | 100% | 100% |

  Infinitesimals and nimbers, which are tempo and parity fights, are the ones the static evaluation
  misreads at low depth. CGT predicts exactly that. Hot positions and numbers are read correctly early.
  This is one engine on a small sample, so it is a pilot result.
- **Cylinder engine.** The only public cylinder fork of Fairy-Stockfish (mtaktikos/CylindricalChess)
  appears, from reading its code, to miss checks, pins and en passant across the seam.
  [engine/FAIRY_CYLINDER.md](engine/FAIRY_CYLINDER.md) gives a corrected design.
- **Lc0:** being run on the same suite by the [tablebase session](#local_154533a8-61ae-4b6f-bed4-5dcf1d9bafff).

## 6. Other new results (model level unless stated)

- **Elkies' other targets on flat 8-rank boards** ([atlas/flat8/REPORT.md](atlas/flat8/REPORT.md)). Counts are
  under the textbook test (verified two ways) → the e.p.-aware test (count rule, computed once):

  | Target | Textbook | E.p.-aware | Example that survives the switch |
  |---|---|---|---|
  | 1/8 | 13 | 9 | `W a2 b4 c4 / B a7 b7 d6` |
  | 1/16 | 3 | 2 | `W a2 b2 c3 / B b5 b6 c7` |
  | 1/32 | 1 | **0** | — |
  | ↑² = {0 \| ↓\*} | 5 | 2 | `W a2 b2 d4 / B a7 c6 d7` |
  | ↑²\* = {0,\* \| ↓} | 10 | 10 | `W a2 b2 b6 / B a6 b7 c5`: the same under every race rule and e.p. setting, under both tests |
  | tiny(1) | 13 | 16 | `W a2 b2 b6 / B a6 b7 c6` |

  - **Two textbook-test results did not survive the switch:**
    - The "best reachable 1/8", `W a2 b2 d2 / B a5 c4 d7`, becomes −3/2±3/2.
    - The best ↑², `W a3 c5 d4 / B a7 b7 d7`, becomes {3/4 \| ↓\*}.
  - The surviving positions pass necessary 8×8 legality conditions only. Their robustness to the race rule under the
    new test has not been checked yet.
  - tiny(x) for non-integer x and tiny(1↑) do not occur under either test. tiny(2) appears under the e.p.-aware test.
- **Cylinder value atlas** ([atlas/cylinder/REPORT.md](atlas/cylinder/REPORT.md); computed once, outcomes
  cross-checked by an independent minimax):
  - **Scope:** 1,223,689 positions (≤5 pawns, widths 3–8) with 10,369 distinct values.
  - **Cut lemma (proved):** cutting a cylinder at an empty file gives a flat board with the same value. So
    cylinder-only values come only from rings, positions with a pawn on every file.
  - **Cylinder-only values:** 53 values occur only on cylinders, among them 3/4 and 1/4±1/4. All come from 3- and
    4-file rings, and none is robust to the race rule.
- **Dawson's chess** ([dawson/REPORT.md](dawson/REPORT.md)):
  - **Cylinder ring rule (proved; checked for n ≤ 22).** The first player on a full 3×n cylinder wins iff
    g(n−3) = 0.
  - **Normal play (classical, reproduced).** Period 34, last exception n = 51.
  - **Misère play,** Dawson's original 1935 question (verified):
    - An independent implementation reproduces the Plambeck–Siegel partial quotient for strips ≤ 32: order 638,
      with 109 P-positions.
    - It agrees with exhaustive search on 7.4 million positions.
    - The next quotient did not converge.
    - Misère Dawson's chess remains unsolved.
- **Structural lemmas** ([notes/lemmas.md](notes/lemmas.md)): component decomposition, the HSS theorem, the
  trébuchet freeze lemma and the ring reduction are proved. The tests in `lemmas/` found no counterexample to
  any of them.

## 7. Pending

- **Workflow `wf_3dfce063-f42`:**
  - the final real-chess report;
  - real-chess certification of other candidates;
  - the Elkies-target certification;
  - the ChessSums benchmark and RL reward (`bench/`);
  - the remaining adversarial verification;
  - a completeness review.
- **A8, explicit kings (loopy CGT):** in the [tablebase session](#local_154533a8-61ae-4b6f-bed4-5dcf1d9bafff),
  in `kings/`.
- **Re-running the textbook-test atlases under the e.p.-aware test:**
  - flat 8-rank, count rule: done (§1, §6);
  - the cylinder atlas and the mover/opponent rules: not yet.
- **ML track (C3/C4):** waits for the PyTorch/MLX install.

## 8. Decisions

Answered 2026-10-16:
- **E.p.:** respect it (done).
- **Kings:** model them explicitly (A8 started).
- **Mentor:** no contact with Prof. Morley yet.
- **Installs:** Stockfish 19 is built; Lc0 is with the tablebase session.

Still open:
- **PyTorch/MLX:** confirm here before installing. Each is a download.
