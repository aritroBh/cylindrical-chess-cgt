# Results so far (2026-10-21)

Plan: [RESEARCH_PLAN.md](RESEARCH_PLAN.md). This page lists what the 2026-10-15/16 run established and how
strongly.
- **Verified** means two independent implementations agree **and** adversarial checkers could not break the
  claim. Every checker so far was written by a Claude model; the OpenCode route to a non-Claude implementation
  failed.
- **Computed once** means one program produced the number.
- **Proved** means one model wrote a proof. No second model or human has re-derived it yet.

**Conventions (decided 2026-10-16).**
- A pawn that can still be taken en passant is **not** passed: `cylcgt.pawns.PASSED_RESPECTS_EP = True`.
  - Merged into `main` on 2026-10-21 (commit d3d080e). `PASSED_RESPECTS_EP = False` restores the old test.
  - Results below that predate this switch are marked *(textbook test)*.
- Kings are modelled explicitly in `kings/` (plan item A8; see §7).

## 1. The \*2 question (Elkies' open problem): the candidate does not survive

The candidate was `W a2 c2 / B b7 d7` on files a–d, frozen by a trébuchet (W g4 / B g5, WK f5, BK h4).

| Check | Result | Status |
|---|---|---|
| Value under the paper's convention, textbook passed test | \*2 under race rules "count" and "mover"; **0** under "opponent". The same with e.p. off | verified (cylcgt, `sumtest/`, Codex rules in `atlas/flat8/census`, `lemmas/`) |
| Value under the adopted convention (e.p.-aware passed test) | **{2±1 \| −2±1}** (mean 0, temperature 2), not \*2. Mechanism: a2–a4 is met by b4×a3 e.p. | verified: cylcgt now agrees with `sumtest/`'s e.p.-aware mode on all 55,195 test positions (§4) |
| Robustness of the \*2 to the race rule | only 4 of its 224 race positions change the value when flipped alone; all come after a capture. A 6-position certificate fixes \*2 whatever the other races do | verified (`atlas/flat8/certificate.json`, `lemmas/` L4.2) |
| Sum model vs whole-board game | equal for this position: its tree never splits into components before a passer (Theorem 2.3). Not true in general without hereditary sum-safety (`research/star2_frontier_recheck/`) | proved |
| 8×8 embedding geometry (kings f5/h4) | no checks, no stalemate, every king move drops that side's g-pawn | proved; exhaustive check |
| Real chess, both sides to move (Lichess 7-man tablebase + exact search) | the side to move wins (outcome N), as \*2 predicts | proved by certificate (`realchess/results/cert_root_*.json`) |
| Real-chess oracle value: the pawn tree with tablebase results at its end positions | **never \*2 (or 0) in the adopted e.p.-aware tree, however draws and unresolved end positions are treated**: the bounds force Left stop ≥ 1 and Right stop ≤ −1. Counting draws as Black wins, it is **exactly {2±1 \| −2±1}** in both trees. In the textbook tree \*2 is excluded only when draws count as wins for one side | values computed once; end-position results checked two ways ([realchess/REPORT.md](realchess/REPORT.md)) |
| Real-chess root move tables | Black to move: only 1...b5 wins (complete). White to move: 1.c4 wins; 1.a3, 1.c3 and all king moves lose; 1.a4 unresolved. The model predicts exactly c4 and b5 | checked two ways |
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
  - At least 18,137 of the 231,071 values change, and 4,070 change outcome ([atlas/flat8/rerun/REPORT.md](atlas/flat8/rerun/REPORT.md)).
    The first count (21,441 and 4,068) compared raw display strings and was wrong in both directions.
  - So within flat boards of ≤4 files and ≤6 pawns, the only route to \*2 was the e.p. artefact.

**The other \*2 candidates** ([realchess/certify/REPORT.md](realchess/certify/REPORT.md)). Each is \*2 only
under one non-default rule, and each needs 10 men.
- `W a3 b3 c2 / B b5 b7 c6` is **refuted**: its real-chess oracle value is > 0 under every treatment (checked two
  ways).
- For three others the tablebase contradicts the race verdicts their \*2 depends on. Their oracle values cannot
  be settled with 7-man tablebases.
- No \*k candidate fits in 7 men or fewer.
- An independent C solver (`atlas/flat8/rerun/`, no shared code) agrees with cylcgt on all 231,071 records under
  both passed tests (checked two ways).

**What this means.** A \*2 made only of kings and pawns on 8×8 is **still open**. Within the searched space
(flat, ≤4 files, ≤6 pawns) no candidate survives the e.p.-aware convention, and none survives real chess. The
negative result is publishable: it shows exactly where the convention breaks.

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
- **King and pawn vs king** (two solvers: `kings/kpsolve` and `atlas/cylinder/kpk`; they agree on all 326,640
  cylinder positions, and on the flat board differ only on the 6 rook-underpromotion positions;
  `delegate/checks/kpk_crosscheck.py`).
  - **Win rates.** White to move wins 78.89% on the cylinder against 76.51% flat. Black to move: 55.88%
    against 58.09%.
  - **Changed results.** 16,538 flat draws become cylinder wins, among them the rook-pawn draw Ka6, Pa5 vs Ka8,
    and 15,930 flat wins become cylinder draws.
  - **Mutual zugzwangs.** 216 on the cylinder, 160 flat.

## 3. The 2025 paper, re-audited (verified)

A blind re-transcription of every diagram matches the solver's input on every pawn square. A pixel scan
confirmed it independently. The kings, and diagrams 2.3 and 5.1, were checked against the images only
([notes/diagram_audit.md](notes/diagram_audit.md)). Three verifiers checked each audit claim. Corrected
verdicts are in [notes/audit.md](notes/audit.md):
- **Correct:**
  - 2.1, 2.2, 2.3, 3.2, 4.1, 4.3;
  - 5.1, the cylinder trébuchet: a mutual zugzwang **only because of the seam**, and a real one with explicit kings (two independent king-and-pawn solvers);
  - the 7.1 c- and f-files;
  - the 7.2 king zugzwang, but **only under the convention**. In real chess, White to move draws with Kd5, Ke5 or
    Kf5, and only Black to move loses (`kings/kpsolve`, confirmed by the Lichess tablebase).
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
- **Lc0 v0.32.1 on the suite** (bundled network, Metal; [engine/runs/lc0/analysis.md](engine/runs/lc0/analysis.md)).
  - **Perfect at every budget.** At 1k, 10k, 100k and 1M nodes all 233 best moves win and all 233 evals match the
    tablebase, in every CGT class.
  - **Lc0 never shows the shallow-depth class effect** that Stockfish shows. Caveat: 216 of the 233 positions are
    wins, so the 17 draws are the real test. Lc0 calls all 17 draws at 1k nodes; Stockfish 19 at 1k rates one +183.
  - **The suite is too easy for both engines.** That again points to ChessSums beyond 7 men for a real contrast.

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
  - **The most robust target is 1/8.** `W a2 a3 b2 / B a6 b5 b6` is 1/8 under all 9 settings (3 race rules × e.p.
    off / textbook / aware) and every race outcome (checked two ways, `atlas/flat8/rerun/`). Its mirror
    `W a2 b2 b3 / B a5 a6 b6` has the same value and a reachable pawn structure. 8×8 FEN with the trébuchet:
    `8/8/pp6/p4Kp1/6Pk/1P6/PP6/8 w` (10 men). This is model-level only, not real-chess certified.
  - ↑²\* at `W a2 b2 b6 / B a6 b7 c5` is equally robust.
  - The other surviving positions pass necessary 8×8 legality conditions only.
  - tiny(x) for non-integer x and tiny(1↑) do not occur under either test. tiny(2) appears under the e.p.-aware test.
- **Cylinder value atlas** ([atlas/cylinder/REPORT.md](atlas/cylinder/REPORT.md); computed once, outcomes
  cross-checked by an independent minimax):
  - **Scope:** 1,223,689 positions (≤5 pawns, widths 3–8) with 10,369 distinct values.
  - **Cut lemma (proved):** cutting a cylinder at an empty file gives a flat board with the same value. So
    cylinder-only values come only from rings, positions with a pawn on every file.
  - **Cylinder-only values:** 53 values occur only on cylinders, among them 3/4 and 1/4±1/4. All come from 3- and
    4-file rings.
  - **Corrected by a verifier:** the atlas claimed that none of these values is robust to the race rule.
    - The 3-file ring values do depend on the race rule.
    - The 4-file ring values, such as {3/2±1/2 \| −3/2±1/2}, do not; they change only when e.p. is switched off.
    - No value is cylinder-only under all six race/e.p. settings.
  - All of this uses the textbook passed test. The re-run under the e.p.-aware test is pending.
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

## 6b. New on 2026-10-21

- **Toward a real-chess 1/8** (`realchess/targets18/`). Position: the robust 1/8, `W a2 b2 b3 / B a5 a6 b6`,
  beside the trébuchet, FEN `8/8/pp6/p4Kp1/6Pk/1P6/PP6/8 w`.
  - **Small end positions.** All 302 sides with at most 7 men (290 one-sided, 12 races) are resolved against
    the tablebase. Of the 290 one-sided sides, 283 agree with the model, 5 disagree and 2 are draws.
  - **Bounds.** With only these exact results fixed, the oracle value lies in [−1/2, 3/4].
  - **The decisive set.** A greedy minimal-support search shows the value is **exactly 1/8** whenever 8
    unresolved end positions (5 with 8 men, 3 with 9) go as the model predicts. The other 312 open ones may be
    anything.
  - **Update.** After resolving the 8-man sides (7 agree, 1 disagrees: with Black to move in
    `W a3 a5 / B b4 b5`, Black wins) and 2 more sides, the bounds are [−1/2, 3/8±1/8] and only **4** decisive
    end positions remain (three with 9 men, `W b2 b5 / B a5 b4` with 8). They are being solved exactly with
    `kings/kpsolve` on the flat 8×8 board (queen promotions only, so not yet a full-chess certificate).
  - **kpsolve so far** (`realchess/targets18/apply_kpsolve.py`):
    - `W b2 b5 / B a5 b4`, White to move: White wins, exact, as the model says.
    - The same position with Black to move is undecided at one promotion (bounds L..W). A two-promotion
      run is going (`kp_eighth_cap2.*`).
    - `W a2 b4 b5 / B a5`, which is no longer decisive: White wins with either side to move.
    - **The three 9-man positions (2026-10-21, 20:35).** All 6 sides are exact (the two promotion bounds
      agree) and match the model:
      - `W a2 a5 b2 / B a4 b5`: White wins, with either side to move.
      - `W a3 a5 b2 / B a4 b5`: White wins, with either side to move.
      - `W a3 b4 / B a6 b3 b5`: Black wins, with either side to move.
      - The run took 2 h 12 min: 29.8 G states, peak footprint 26 GB (`kp_eighth_9man.out`).
    - **New bounds: 0 ≤ O ≤ 1/8.** Only one decisive side is open: `W b2 b5 / B a5 b4`, Black to move.
      - If it is a White win (the model's verdict), O = 1/8 exactly.
      - If it is a draw or a Black win, O stays in [0, 1/8].
      - Reproduce: `PYTHONPATH=. .venv/bin/python realchess/targets18/apply_kpsolve.py
        realchess/targets18/min_support_after2.json realchess/targets18/kp_eighth_{8man,9man}.out`.
      - Caveat: queen promotions only. A full certificate also needs a `--promote QRBN` rerun.
  - **Sensitivity.** Each of the 7 open sides must go as the model says. Changing any single one of them unpins
    the value (the lower bound drops to 0, ↑\* or below).
  - ↑²\* and tiny(1): every resolved end position agrees with the model, and the lower bound already equals the
    target value. 10 and 12 end positions with 9–10 men still decide them. The one 8-man end position on both
    lists, `W b4 b6 / B a4 b7`, was solved by kpsolve on Oct 22 (queen promotions, exact, Black wins, as the model
    says; `realchess/targets18/r7_driver.log`).
  - **Status.** Resolution continues. The same pipeline is queued for ↑²\*
    and tiny(1).
- **Paper.** A full draft is in `paper/` (Overleaf-ready; `paper/main.pdf`, 18 pages): "Pawn Endgames Without
  Edges: Exact Combinatorial Game Values, Real-Chess Certification, and Tablebases on the Cylindrical
  Chessboard".
- **Wave 2 of delegated research** (`delegate/briefs/T8–T15`), launched with `delegate/run.sh wave2` and, after
  the codex quota resets, `delegate/run.sh codex`:
  - T8: the \*2 frontier search;
  - T9: Möbius strip and Klein bottle boards;
  - T10: king-and-pawn tablebases on the cylinder;
  - T11: thermography and atomic weights;
  - T12: odd-circumference cylinders;
  - T13: engines on ChessSums;
  - T14: Dawson variants;
  - T15: novelty check.

- **Independent non-Claude re-check** (`verify_ext/codex/`, Codex).
  - A stdlib solver written from the rules alone reproduces all five headline values in all nine settings.
  - It finds no \*k with 2 ≤ k ≤ 292 among 793,299 placements on widths 1–4.
  - Its self-check, re-run here, gives 27 PASS.
- **Review log of external reports:** [delegate/REVIEW.md](delegate/REVIEW.md).

## 6c. New on 2026-10-22

- **Rings: the first ring \*2 on Cn has n+3 pawns for n = 3, …, 6** (default setting; values CHECKED-2,
  minimality C1).
  - On C6, a scan of every nine-pawn ring finds exactly six \*2, three positions and their color-reversed twins,
    among them `W a4 c4 d2 e2 / B b6 b7 d6 e5 f6`.
  - No ring with eight pawns or fewer is \*2 on C6.
  - Paper §VIII; open problem 3 asks about C7 with ten pawns.
- **\*3 rings in non-default settings (CHECKED-2: the C scanner, and cylcgt with and without component
  splitting).**
  - C4, 8 pawns, opponent rule, e.p. off: `W a5 b3 c2 d2 / B a7 b5 c6 d4` and its twin `W a5 b3 c4 d2 / B a7 b7 c6 d4`.
  - C3, 10 pawns:
    - count rule, e.p. off: `W a2 a3 b2 b3 c3 / B a6 a7 b6 b7 c6` and `W a2 a4 b2 b3 c3 / B a5 a7 b6 b7 c6`;
    - opponent rule, e.p. on: `W a2 a3 b2 b3 c3 / B a6 a7 b6 c6 c7` and `W a2 a4 b2 b3 c3 / B a5 a7 b6 c6 c7`.
  - No \*3 occurs in the default setting in any scope searched. Paper §VIII has one sentence.
  - Checks: `delegate/checks/c3p10/`, `delegate/checks/c4p8/`.
- **C3, 10 pawns, default setting:** 741,110 rings, two of them \*2 (twins):
  `W a2 a5 b2 b4 c2 / B a7 b5 b6 c4 c7`. CHECKED-2.
- **Scanner bug fixed** (`research/star26_rings/BUGFIX_frontier_split1.md`).
  - Cause: a stale memo-table pointer.
  - It crashed large runs, but never changed a value.
  - The crashed runs are re-run with `frontier_split1_fixed`; details in [delegate/REVIEW.md](delegate/REVIEW.md).

- **Round 7 (Sonnet/Haiku workflow; see [delegate/REVIEW.md](delegate/REVIEW.md)).**
  - **Positions A and B are one \*2:** B is A with the colours reversed and the files mirrored. All 12 decisive
    8-man end positions of their real-chess trees agree with the model; the oracle bounds stay open until the
    9–11-man sides are solved.
  - **\*3 with e.p. off on six files** (scanner, cylcgt, Codex): 16 positions, 8 up to colour reversal. Twelve are
    the 4-file candidate (\*2) plus a \* group, so \*3 = \*2 + \*. With the aware test they are not nimbers.
  - **\*3 in the default setting, as a sum:** `W a4 b3 d2 d3 f4 / B a7 b7 c5 f6` (position A plus a \* group) on
    flat 6×8 is \*3 by three programs. No single-component default \*3 is known.
  - **Ring minimum on C3 and C4 is now CHECKED-2:** independent solvers and full cylcgt scans.
  - **The C3 ring \*2 needs two e.p. captures,** B b4×a3 and W b5×c6. Without the first it is ↑, without the
    second ↓.
  - **Möbius 8×8:** KPK is won from 78.94% of positions with White to move (cylinder 78.89%). CHECKED-2.
  - **Proof audit:** Thm 3 and Thm 8 got precise statements and sketches, and Conj 4 is now a Corollary [AI].
    Repo defects in `kings/theory/LOOPY.md` were passed on to the maintainers of that note.

- **C7 (2026-10-22 afternoon).** The first ring \*2 on C7 has ten pawns: no nine-pawn ring is \*2 (scanner, and
  T43's independent solver over 19,961,100 classes). The five-a-side ten-pawn rings include 63 \*2 and
  **8 single-component \*3 in the default setting**: the first default-setting \*3 that is not a sum. The scanner,
  T43's solver and cylcgt (whole board) agree on all 8; 6 stay \*3 as sums. Example:
  `W a2 a5 c4 e2 f2 / B a7 b4 d7 e5 g7`. So n+3 holds for n = 3, …, 7.

- **A real-chess 1/8 (2026-10-22, 15:48).** The cap-2 kpsolve run (6.1×10^10 states, 15.6 h, queen promotions)
  shows White wins `W b2 b5 / B a5 b4` with Black to move (exact, W W). With every decisive end position now
  exact, `apply_kpsolve.py` pins the oracle value: **O = 1/8** (queen promotions only, frozen kings; C1).
  Still open: a rerun with underpromotions for a full-chess certificate.

- **Round 10 (2026-10-22 evening).**
  - **The wall rings are \*2 for every n ≥ 5, in the whole-board game** (proved [AI], finite checks CHECKED-2).
    - Families: O_n = `W23B4, B5, W2B5, (W3,B5)^k` and E_n = `B5, W2B5, W35B6, W2, (B4,W2)^(m+1)`, with n+3 pawns.
    - Proof: delete the losing wall moves, then show that two more wall files leave the reduced game unchanged.
      This reduces everything to two graphs of 144 and 104 nodes plus n < 17.
    - Refereed SOUND by OpenCode beam-free (T51), a non-Claude model. A Sonnet verifier with its own engine
      accepted it, asking only for label and scope fixes.
    - As sums of components it is still checked only to n = 12, because wall captures split the ring.
    - `research/ring_family_proof/`.
  - **No \*4 found (T49).**
    - All 134,920,191 one-component ten-pawn positions on five files: 75 \*2, 3 \*3, nothing higher.
    - All 48,649,934 eleven-pawn positions on four files: 9 \*2, 1 \*3.
    - Root counts are reproduced exactly by an independent count. This is under the scanner's e.p. convention,
      which keeps an e.p. right across components.
    - The 13 minimal \*3 cores are each a \*2 plus a \*1 pair (CHECKED-2). Two of the four C7 \*3 ring classes are
      primitive.
    - `research/star4_hunt/`.
  - **C8 breaks the n+3 pattern: the first ring \*2 on C8 has ten pawns (n+2).**
    - No nine-pawn ring is \*2. The scanner and `c8check_gen` agree over all 7,039,362 classes (CHECKED-2).
    - The ten-pawn 5+5 split has 18 \*2 and 2 \*3 classes (scanner, C1). Example:
      `W a3 b3 c3 d2 f2 / B b6 d5 e5 g4 h5`, \*2 in cylcgt both as a sum and whole-board (CHECKED-2).
    - All splits are done; every hit is in the 5+5 split. One ring from each of the 11 colour-reversal classes is
      confirmed by cylcgt, sum and whole-board: 10 \*2 and 1 \*3, `W a4 c3 d3 e2 g2 / B b7 c6 e5 f5 h4` (CHECKED-2).
    - T52 (OpenCode) is looking for an n+2 family on C9 and up.

## 6d. New on 2026-10-23 to 10-27

- **Rings with n+2 pawns for every n >= 10 (whole-board, [AI]).**

  | Family | Value | n | Reduced graph | Proof note | Referee |
  |---|---|---|---|---|---|
  | P_n = W5 B7 W4 W4B7 B6 W3B6 (W2 B4)^k | \*2 | even n >= 8 | 813 nodes | PROOF.md | Codex T53, SOUND |
  | Q_n = W4 B7 (B4 W2)^k W3B6 W3 W2B5 B5 W2 B4 | \*3 | even n >= 8 | 7,968 nodes | PROOF_Q.md | Codex T62, SOUND |
  | R_n = W5 B7 (W2 B4)^k W2 W3B6 W3 W2B5 B5 W2 B4 | \*2 | odd n >= 11 | 429 nodes | PROOF_odd.md | Codex T63, SOUND |
  | Qo_n = W4 B7 (W2 B4)^k W2 W3B6 W3 W2B5 B5 W2 B4 | \*3 | odd n >= 11 | 1,287 nodes | PROOF_odd.md | Codex T63, SOUND |

  - PROOF_odd.md uses c = 6 and n0 = 19. A Sonnet workflow accepted it with fixes, with C1 on six programs and C2 on
    five. The Codex referee T63 is queued.
  - Both odd families fail at n = 9, so the C9 minimum (11 pawns?) is open: T54b on Codex and a C9 enumerator
    workflow.
  - As sums of components, P_10 is \*2, Q_10 is \*3 and R_11 is \*2 (cylcgt). Qo_11 as a sum is running
    (`research/sum_model_rings/`).
  - The Codex referee T63 found PROOF_odd.md SOUND (`research/ring_n_plus_2_check/odd/REPORT.md`).
  - **C9 with 10 = n+1 pawns: 7 rings with signature \*2 in split 5+5 (COMPUTED-1, `research/c9_rings/`),** being
    verified. Verified on 2026-10-27, see the next bullet.
- **Least pawns in a ring \*2: n+3 (n = 3..7), ten (n = 7..10), n (n = 10..60), all CHECKED-2** (`research/c9_rings/REPORT.md`;
  the independent engine E agrees for M_10..M_60, O_11..O_59 in `research/ring_n_proof/logs/base_N_60.log`).
  - C9: no 9-pawn ring is \*2 or \*3 (948,860 rings; rg and OpenCode's engine; two enumerators). 7 of the 44,960,428
    ten-pawn rings are \*2: rg, Codex's independent.py, OpenCode's engine and cylcgt (whole and sum) agree. CHECKED-2.
  - C10: M_10 = B4 W2 B6 W2 W3 B6 B7 W3 B7 W5 is \*2 with one pawn per file (CHECKED-2). It is the only one among the
    4.3M ten-pawn rings (COMPUTED-1).
  - C11: O_11 = B4 B7 W5 B7 W3 B7 B6 W3 W2 B6 W2 is \*2 (CHECKED-2). It is the only one among the 15,461,385
    eleven-pawn rings in splits 4+7 and 5+6, and none is \*3 (COMPUTED-1). The ring counts for C10 and C11 equal an
    independent transfer-matrix and Burnside counter.
  - Families: M_n = (B4 W2)^((n-8)/2) B6 W2 W3 B6 B7 W3 B7 W5 (even n) and O_n = B4 (B7 W5)^((n-9)/2) B7 W3 B7 B6 W3 W2
    B6 W2 (odd n) are \*2 for every n = 10..60 (COMPUTED-1, rg; n = 10..14 CHECKED-2). Their reduced graphs are constant
    (441 / 2132 nodes, no flag), and the insertion isomorphism holds from n = 18 / 19 on. Proof note: T65 (OpenCode,
    `research/ring_n_proof/PROOF_N.md`). **PROVED [S] for every n**: referees T67 (Kilo, logic, fixes applied) and T66
    (Codex, SOUND, own independent checker, `research/ring_n_check/`).
  - The paper (§VIII, intro, conclusion) now says "ten for 7 <= n <= 10 [C2], n for 10 <= n <= 60 [C1]".
- **Rings \*3 with n+1 pawns on every C_n, 11 <= n <= 59** (`research/c9_rings/star3/REPORT.md`).
  - C11: no eleven-pawn ring is \*3 (COMPUTED-1, exhaustive), and two twelve-pawn rings are (CHECKED-2). So the least is
    n+1 there.
  - Families T_n = (B4 W2)^((n-10)/2) B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2 (even n = 12..58) and S_n = B4 B6 W3
    (W2 B4)^((n-11)/2) W6B7 W3 B7 B6 W3 W2 B6 W2 (odd n = 13..59) are \*3 (rg; CHECKED-2 for n <= 15).
  - Reduced graphs: T has 1305 nodes, S has 40445; no flag; the insertion isomorphism holds from 20 / 25 on. Proof note:
    T69 (OpenCode, `research/star3_proof/PROOF_S3T3.md`). **PROVED [S] for every n >= 12** as nim-heap outcome
    equivalence; referees T71 (Kilo) and T70 (Codex, own checker), fixes applied.
  - M_10 and O_11 are \*2 as sums of components too (cylcgt, `research/sum_model_rings/npawn_values.txt`). Qo_11 is \*3
    both as a sum and as a whole (`odd_values.txt`).
- **C12 with 12 pawns (exhaustive, 140,587,958 rings; COMPUTED-1; counts match the independent counter):** no ring is \*3,
  so the least ring \*3 on C12 has 13 = n+1 pawns. Three rings are \*2 (M_12, its reversal, one self-reverse), so the
  n-pawn \*2 ring is unique only on C10 and C11. C10 with 11 pawns: 3 rings \*2, none \*3
  (`research/c9_rings/work/c12p12_totals.txt`, `c10p11_totals.txt`).
- **C9 ring hits are \*2 as sums too** (cylcgt, the H1 reversal, H3 and H4; H1 whole \*2; H2 sum and whole queued).
- **No \*4.** None among T56's 14,090 candidates (329 are \*3, 178 \*2), nor among 1,280 C10 wall rings.
  - The ★4 hunt workflow (`research/star4_rings/{core_wall,grow,two_core}/REPORT.md`) found no ★4 and nothing above
    ★3 in about 23.6M rings. Those are 23.2M core-in-wall rings, 128,791 grown from known ★3 rings (4,723 new ★3)
    and 207,975 two-core rings, all C1, with hits re-checked by the unmodified rg.
  - Two cores separated by walls: whenever the ring is a nimber (1,513 of 1,890 rings) it equals the nim-sum of the
    two cores' values, with no exception. The other rings are decisive, from a coupling that disappears once a wall
    has 7 to 11 files.
  - So a ★4 ring would need a single core worth ★4 on its own. None was found up to width 6.
- **Twisted tablebases.** A and B agree exactly under A's ray rule. KRK wins every position on the Möbius strip and
  on RP² but only 0.66% on the Klein bottle (CHECKED-2). See `research/twisted_tablebases/COMPARE.md`.
  - **Audit 2026-11-22** (`research/mobius_repair/REPORT.md`). The older T9 code (`research/mobius/mobius_replica.c`,
    `kpsolve_mob.c`) overflows its ray arrays (`[64][8][8]`, rays reach 15 squares; UBSan confirms). A and B do not.
    With the arrays fixed, T9 matches A on 22 of 22 rows and B on 26 of 26: Möbius KRK 147,776 of 147,776 won, Klein
    KRK 960 of 145,344 = 0.66%. T9's old 0.79% and its legal counts are superseded. Möbius KPK (78.94%) is unchanged.
- **Frontier discrepancy resolved 2026-11-22** (`research/star2_frontier_recheck/REPORT.md`). Under the opponent rule
  with the e.p.-aware test, `W a3 b3 c2 e2 / B a6 c5 d5 e3` and `W a6 b4 c4 e3 / B a7 c7 d6 e6` are ★2 on the whole
  board (C scan, sumtest whole mode, cylcgt with splitting off) and ⇑, ⇓ as sums (cylcgt, sumtest component mode).
  Neither program has a bug: the roots are not hereditarily sum-safe. Smallest witness `W a3 e2 / B b4 d3 e3`. Under
  the count rule both are ★2 in both models.
- **Pawn rings on the Moebius strip 2026-11-22** (`research/mobius_rings/REPORT.md`; two solvers by one agent agree
  on every ring, the older `research/mobius/mob_pawns.py` confirms 51 of the 66 hits; **CHECKED-2**: Codex's
  independent solver T77, `research/mobius_rings_check/`, agrees on the eight example rings, the ring counts and
  every scan below the least). Whole-board game, 8 ranks, count rule, e.p.-aware; a capture across the seam
  flips rank and direction.
  - Least pawns in a root ring \*2: 6, 8, 6, 8, 8, 8 for n = 3..8 (cylinder: 6, 7, 8, 9, 10, 10). Lower than the
    cylinder for n = 5..8, higher at n = 4. At n = 8 it is n, the fewest a ring can have (cylinder: only from n = 10).
  - Examples: n = 3 `W3B6 W2B7 W4B5`; n = 5 `B6 W3 B5 W2 W3B7`; n = 7 `B6 W2 W3 B6 B7 W3 W6B7`;
    n = 8 `B7 W3 W3 B6 W3 B6 B6 W2`.
  - \*3 with 9 pawns on n = 5 (`B67 W4 W2B6 W2B5 W5B7`) and n = 6; the cylinder C5 has no \*3 with up to 9 pawns.
  - Exhaustive: n = 3 with 3..10 pawns, n = 4 with 4..9, n = 5 with 5..9, n = 6 with 6..9, n = 7 with 7..8, n = 8
    with 8. Root rings only (default directions); rotations are not symmetries of root rings.
- **Sum vs whole, ring families 2026-11-22** (`research/sum_vs_whole_families/table.tsv`; C1, cylcgt only). In all 24
  (family, n) pairs solved in both models the canonical values are equal: wall rings odd 5..11 and even 6..10, F 7..10,
  P 8, 10, N1 9..11, M_10, O_11, R_11 (all \*2), Q 8, 10 and Qo_11 (\*3); Qo_9 and R_9 have the same complex value in
  both. Nothing above n = 11 in both models; T_n and S_n not run. No change to the paper's statements.
- **Sum vs whole census 2026-11-22** (`research/sum_whole_census/REPORT.md`; C1, totals recounted from the raw rows
  by a second script). Every passer-free flat position with 2 to 6 pawns on widths 3, 4, 5 (599,098 up to mirror and
  colour swap), all three race rules, both passed-pawn tests.
  - Hereditarily sum-safe: S and W never differ in outcome (0 of 540,503, e.p.-aware; 0 of 539,893, textbook).
  - Not hereditarily sum-safe (count, e.p.-aware): 11,300 of 58,595 differ (19.3%); overall 1.89%. Mover 1.54%,
    opponent 2.02%: the count rule is not special here.
  - All differences are on width 5 with two root components. Widths 3 and 4 (40,262 and 154,813) and the cylinders
    C4 (60,447, up to 6 pawns) and C5 (14,883, up to 5 pawns) have none.
  - Smallest: `W a5 d3 / B b6 e4`, sum P, whole board N under every rule (two locked pairs; checked with cylcgt and
    sumsolver). Three programs agree on 4,000 sampled positions per test.
  - `sum_safe()` True with S != W: 0 except 8 one-component roots under textbook + mover.
- **Paper fact-check round 11.** 15 findings confirmed and applied (`delegate/REVIEW.md`).

- **Cross-check brought in line with the default passed-pawn test (2026-11-22; found by the T79 audit).** The
  independent minimax in `crosscheck/` used only the textbook passed-pawn test, so the README command reported 24 of
  the 1,070 single components disagreeing once the engine's default became e.p.-aware. The minimax now has its own
  e.p.-aware test, written from the rule. Both settings rerun: 1,070 of 1,070 single components agree under each;
  12 (e.p.-aware) and 10 (textbook) multi-component cases differ, as before, from the cross-component race rule and the
  e.p. right across components (`crosscheck/REPORT.md`, "Run 2026-11-22"). CHECKED-2. The paper's sentence is unchanged.
- **T79, reviewer's-eye audit by Codex (report kept local, not tracked: it quotes the identifiers it found).** A clean copy failed at the first README
  command (no setup step; added). The tracked files (2.3 GB) cannot be made anonymous by term replacement alone: 64
  paths must be left out. 18 raw CLI transcripts with session identifiers or unrelated personal context are no longer
  tracked. The two review PDFs carry no identifier.

- **Möbius pawn rings on 9 to 11 files, and families (2026-11-22; `research/mobius_rings_n/REPORT.md`).**
  - Exhaustive scans, two programs byte-identical on every ring: n = 9 with 9 pawns, 2,729,517 rings, no \*2;
    n = 10 with 10 pawns, 17,146,529 rings, 2 \*2 orbits; n = 11 with 11 pawns, 109,358,578 rings, 1 \*2 orbit;
    n = 9 with 10 pawns, 133,597,405 rings, 9 \*2 orbits and 1 \*3 orbit (`B5 W3 W4 B7 B7 W3 W2 W2B7 B7`).
    The old counts for n = 7 and 8 reproduce exactly.
  - So the least ring \*2 on the strip is 6, 8, 6, 8, 8, 8, 10, 10, 11 for n = 3..11 (cylinder: 6, 7, 8, 9, 10,
    10, 10, 10, 11). CHECKED-2: the independently written checker agrees on every hit, and its own scan of the
    nine-pawn rings on nine files finds no \*2 (5,459,034 orbits under its group of order 2, exactly twice ours;
    `results/check_n9_p9_enum.out`, run by the main session).
  - Three families stay \*2: `(B4 W2)^m B6 W2 W3 B6 B7 W3 B7 W5` (n = 2m+8, one pawn per file, m = 1..12),
    the same with a last file `B7` (n = 2m+9, m = 1..11), and `B6 W2 W3 B6 B7 W3 (B7 W5)^m W6B7` (n = 2m+7,
    n+1 pawns, m = 0..12). Three programs agree for n <= 21 (CHECKED-2), two for n <= 32 (COMPUTED-1). Node counts
    grow by a constant per step (1251, 1239, 719), so a pumping proof looks feasible (CONJECTURE for all n). Superseded on 2026-11-23: the three families are proved for every n (see the entry "Möbius ring families proved for every width" below).
    One pawn per file therefore gives \*2 on the strip for every n from 10 to 32, on eight files by an isolated
    ring, and never on nine.
  - Not done: n = 12 with 12 pawns (scan running), n = 10 with 11 pawns, any \*3 family.
  - In Section VIII of both versions, supplement S6.4, conclusion.

- **Boards of other heights (2026-11-22; `research/tall_boards/REPORT.md`).** Single-component positions with every
  file occupied (rings on cylinders), no passed pawn, R = 5..12 ranks, ordinary boards of 3 and 4 files and cylinders
  of 3, 4, 5 files, by increasing pawn count: 1,833,497,669 positions solved by a new C solver (`tw.c`).
  - **No \*4:** the only nimbers are \*0, \*1, \*2 (831 positions) and \*3 (77). COMPUTED-1.
  - **Height matters and the minima are not monotone.** R = 5: no \*2 on any of the five boards (all positions
    solved). R = 6: \*2 with 6 pawns (`W a2 b2 d2 / B a5 c5 d5`, 4 files). R = 7: \*2 with 4 pawns
    (`W a2 c2 / B c3 b6`, 3 files) and \*3 with 6 (`W a2 c2 d3 / B c3 b6 c6`, 4 files). On the cylinder of 3
    files and 9 ranks the home position `W a2 b2 c2 / B a8 b8 c8` is \*2. Full table in the report and in supplement
    S6.5. The 48 minimum positions agree with cylcgt (CHECKED-2; the main session re-ran seven); minimality and
    "none" are COMPUTED-1.
  - Validation: 16,000 random positions (2,000 per R) agree with cylcgt on the full 8-letter signature; the R = 8
    column reproduces the stored counts (48,649,934 roots on 4 files with 11 pawns; 134,920,191 on 5 files with 10).
  - Not covered: positions with an empty file, flat boards of 5+ files, cylinders of 6+ files, R > 12, and the
    pawn counts above each "none up to p" cell.
  - In Section VIII of both versions (one sentence in the 10-page text) and the conclusion's question on \*4.
  - **Independent check T80 (Codex, own solver from the rules; `delegate/out/T80/REPORT.md`).** All eight named
    positions agree. The complete scans for R = 5 (five boards), R = 6 (five boards) and R = 7 (3 files, flat and
    cylinder), 2,381,595 positions, give the same count of every nimber and the same minima; no nimber above \*3.
    CHECKED-2 for those rows. One difference: on cyl 5, R = 6, `tw.c` counts 1,786,651 roots and 345 zeros, Codex
    1,786,371 and 340; the extra 280 are in two impossible 20-pawn splits (1+19, 2+18). No table entry changes; the
    grand total of positions is therefore quoted as "about 1.8 billion".

- **Engines on ChessSums: result withdrawn (2026-11-23; `research/engine_baselines/REPORT.md`).** A referee asked for a
  random baseline for "Stockfish finds a winning move in 26.5-28.0% of 200 sums". Computing it showed the test is
  flawed. `engine/runs/chesssums/embed.py` drops the king group into any free squares: in 163 of the 200 positions it
  shares a file with component pawns; 72 positions list a model-winning move that is illegal on the board and 61
  have no legal winning move; 27 have more than eight pawns of one colour and Stockfish exits on them. A uniformly
  random legal move scores 23.7% and a random pawn move 49.0%. On the 37 positions without a shared file the engines
  get 23 of the 25 that have a winning move; on the 13 with the group clear of the pawn files and their neighbours,
  13 of 13 at every budget. COMPUTED-1. The paper's Section XII and the introduction no longer claim that engines
  miss winning moves on sums. The suite result (233 positions, Table of accuracy by value class) reproduces in every
  cell and stands; restricted to the 180 positions where model and tablebase agree, infinitesimals are still
  the hardest class at depth 1 and 2 (30% and 26%, n = 27; intervals overlap nimbers and "other").
  A clean rerun would need embeddings built with room for the kings.

- **Sum cross-check rerun under the e.p.-aware test (2026-11-23; `research/sumtest_epaware_rerun/REPORT.md`).** The
  only recorded run predated the engine's switch to the e.p.-aware test and showed 13,176 cases (109,157 pairs)
  differing. Rerun with both sides e.p.-aware: 0 of 2,483,775 pairs differ, in each of the solver's three modes; the
  textbook and e.p.-off controls are also 0; mixing the two tests across the sides reproduces the old 13,176 and
  109,157 exactly. So the paper's sentence in Section XIII is true as written and now has a log. CHECKED-2.
- **Möbius ring families proved for every width (2026-11-23; `research/mobius_rings_proof/PROOF.md`).** F1
  `(B4 W2)^m B6 W2 W3 B6 B7 W3 B7 W5` (n = 2m+8) and F2 = F1 + `B7` (n = 2m+9) are *2 for every m >= 1, and F3
  `B6 W2 W3 B6 B7 W3 (B7 W5)^m W6B7` (n = 2m+7, n+1 pawns) for every m >= 0, as whole-board games against nim-heaps.
  So one pawn per file gives a ring *2 on the strip for every n >= 10. Proof: the cylinder's insertion argument, with
  the ten-file arc around the cut kept clear of the seam; base case m = 5 (reduced games of 435, 417, 435 positions,
  no e.p. flag, zone clear of the arc). The seam only changes the base graph (the pawns on both sides of it never
  move; 435 nodes against the cylinder's 441). Written by an Opus agent; I reran all its finite checks (same
  numbers). Codex referee T82 (`delegate/out/T82/REPORT.md`): HOLDS WITH FIXES, two wording fixes applied (pattern
  files belong to one wall with one phase; Lemma 1 for non-terminal roots); its own program reproduces every number
  of the base case and of m = 0..7, and its unreduced minimax gives NNPN for m = 1..13 (RNRR, NNRR at m = 0 for F1,
  F2). Label in the paper: S (AI-written, AI-refereed); base case CHECKED-2. Side finding: `mob2` in batch mode can
  reuse a memo entry across widths; the scans ran one width per process and are not affected.
- **Self-contained proofs of the four S results (2026-11-23; `dist/tog/supp_src/s12a_core.tex`, supplement S12.1).**
  Items A.1 to A.17 prove by hand, from their own definitions, the validity theorem (A.11), its corollary (A.13), the
  certificate theorem in the promotion game (A.16) and sum safety (A.7). Written by an Opus agent; I read it; two
  referees so far. Kings-session Opus referee A (A.11 to A.17): sound, minor fixes applied ((C3) reworded to match
  (L3); A.13 lists A.7's hypotheses; mapping to the long note corrected). Codex T81 (`delegate/out/T81/REPORT.md`):
  all four hold with fixes, applied: promotion inside the pawn games had to be pinned down (on four ranks a double
  step promotes; on five ranks `W a2 b2 / B b4`, a2-a4 then a4-a5 promotes inside a sum); the
  induction of A.7 runs over positions with their actual side to move; A.13 holds per side to move (example where the
  hypotheses hold for Black to move only: `W Kb6 c7 / B Ka8 a5`); the bound N(X) <= n(H-1)(H-2)/2 = 168 on 8x8. Its
  census on four files and six ranks: 9,070 flat and 13,724 cylinder qualifying roots, 45,588 comparisons of S and W,
  0 differences (one program, its own).
  **Wording error found in the paper and fixed:** the paper said S(X) re-splits and then replaces components with a
  passed pawn; the engine (`cylcgt/pawns.py`, `value`) and the theorem test the moved component first and split only
  if no pawn is passed. Split-first is a different model: `W b2 d6 / B c7`, c7xd6 gives +BIG-BIG = 0 there but a race
  White wins in W and in the engine. Fixed in Section V of both versions; the threat definition now says "either side
  in any order"; the sum-safety and validity theorems state that X has no passed pawn; the 10-page text's certificate
  sentence now says "with only Z on the board ... promotes or mates within h moves of its reply".
  Kings referee B (A.1 to A.7): A.1, A.4, A.5, A.6 sound; its fix for promotion is the one adopted: as in the engine,
  a pawn on its last rank stays a pawn and is passed under every test, so a promoting move ends W and freezes its
  component in S, and sum safety needs no height condition (its sample: 985 HSS roots, 386 of them on four- and
  five-rank boards, S and W agree on all; one run). The validity theorem keeps H >= 5 (no promoting move from a
  position without a passed pawn). Both gaps the appendix author reported in the long kings note were confirmed and
  repaired there (kings commit 435ccdc7: Theorem 1.11(c) now assumes (E); re-split components inherit "no threat");
  the supplement's copy of the note carries the repair. Whether Theorem 1.11(c) holds without (E) is open.
  The kings session then revised the note for Codex's three points (kings commit ef1314c3: order of operations in S,
  the last-rank convention, Theorem 1.14 per side to move, threats by moves in any order); the supplement copy
  carries those edits too (supplement 95 pages). K50 (`kings/embed_check.py`, referee pending): strict mode certifies
  none of the 23 separated ChessSums positions, because the stalemate clause of the certificate fails for every
  trébuchet; a certified engine test set would have to use other king groups. The engine-on-sums test stays future
  work.
- **Round of 2026-11-23 (delegated audits and a third mock review; reports under `delegate/out/R1_...` to `R7_...`).**
  R1 (Opus) re-read appendix A.1 to A.9 after the last-rank convention: sound, four wording fixes; its own brute
  force (flat boards up to 5 files by 6 ranks, all nine settings, up to 2+2 pawns, and 3+3 in the default setting)
  finds S = W on every position satisfying HSS and (E), and its split-first control differs in 98 to 320 cases per
  board. R2 and R7 (Sonnet) audited pointers, labels and the long version: stale lines fixed in supplement S3, S4,
  S10, the README and the submission files. **Correction:** the least number of pawns in a Möbius ring *2 is n for
  every n >= 10 (a ring has at least n pawns and one per file suffices, proved); an earlier line called n >= 12 open.
  The 12-file scan was therefore stopped at 50 of 128 parts (one *2, the family member). R6 (Opus), a mock review
  formed without reading earlier ones: major revision; its spot checks of sum safety (S12.1) and of the wall and
  n-pawn ring proofs (S13, S14) found them sound. Applied from it: the validity theorem is per side to move and on
  boards of at least five ranks; the bound on BIG is stated as moves of one side in any sequence of pawn moves; a
  pawn on its last rank counts as passed (Section II); the abstract says "state when frozen kings give the chess
  result"; several sentences reworded. Left for the author: human verification of the S proofs, Table I (corrections
  to an unpublished study), and the code package name in the supplement while the repository is public.

## 7. Pending

**Verification gaps.** 35 adversarial verifiers were cut off by the Claude usage limit. Not verified:
- the real-chess oracle values;
- the certification of the other candidates;
- the flat-board claims C1, C2 and C4–C6;
- three cylinder-atlas claims;
- two lemma checks.

The completeness critic did not run either. The rest of the verdicts are in each REPORT.md claim table.

**Delegated to external AI CLIs** (briefs in `delegate/`; outputs go to the directories named there):
- independent non-Claude re-verification of the §1 headline results;
- re-deriving the `notes/lemmas.md` proofs;
- the Elkies-target certification (`atlas/targets/`, left partial);
- the cylinder atlas under the e.p.-aware test;
- ML baselines on ChessSums and Dawson's chess (`.venv-ml`);
- a completeness review.

**ChessSums v2 is ready** ([bench/REPORT.md](bench/REPORT.md)).
- **Library:** 418 components, each with the same value under both passed tests, all race rules and e.p. on/off.
- **Data:** 26,000 rows. Their outcomes were confirmed by whole-board alpha-beta, and 4,887 also by Codex's minimax.
- **Baseline cost:** alpha-beta that ignores the decomposition grows about 4–9× in nodes per added component.

**A8, explicit kings** ([kings/REPORT.md](kings/REPORT.md)):
- **The convention often fails on small boards.** 159 of 500 testable components mismatch: 107 because of the
  kings, and 52 because of the pawn convention itself.
- **When it is exact.** Conditions (V1)–(V4) are given (Theorem 1.14, proved by one model and reviewed).
  - A king that can shuttle without loss is a loopy game (`on`, `off`, `dud`), not 0.
  - The trébuchet's zero is context-dependent.
- **Solver check.** `kings/kpsolve` agrees with an independent solver on 1,418,480 positions.
- **Real chess.** Both trébuchets are real mutual zugzwangs. The 7.2 king group is not (confirmed by Lichess).
- **K+P vs K without edges (K4, CHECKED-2; [kings/delegate/out/K4/REPORT.md](kings/delegate/out/K4/REPORT.md)).**
  - Setup: normal play (stalemate loses), boards 3×4 to 5×5, flat and cylinder, 20,556 quiet placements, each
    summed with 16 test games.
  - Every placement is a decisive win, on, off, dud or unmatched; no number or infinitesimal occurs. off is
    exactly the White-stalemated pattern.
  - Removing the edges changes the class of 12.5–20.5% of placements. Paper §IV-D has one sentence.
  - Gafni's on\*, {on|0} and 1\* do not occur (on + \* only tied with on). The Gafni thesis itself was not located.
- **Canonical values by difference games (K5b, CHECKED-2; [kings/delegate/out/K5b/REPORT.md](kings/delegate/out/K5b/REPORT.md)).**
  - `sumtest/sumsolver.py`, which computes no canonical forms, finds G − V to be a second-player win for 72
    of 81 target × setting pairs: 1/8 (×3), 1/16, ↑², ↑²\*, tiny(1), a2 c2 / b7 d7 and the C3 ring \*2.
  - The other 9 contain ±BIG and are not testable this way.
  - Caveat: sumsolver is also Claude-written. K5, a free-model "independent" engine, was a copy of cylcgt and is
    rejected.

**Lc0** at 1M nodes finished: 233/233 best moves win and 233/233 evals match (commit 1cc5ebb).

## 8. Decisions

Answered 2026-10-16:
- **E.p.:** respect it (done).
- **Kings:** model them explicitly (A8 done; see §7 and [kings/REPORT.md](kings/REPORT.md)). The exact 7×6 per-move
  tally is deferred: it needs about 9 GB at cap 2, over the shared-machine limit, and cap 1 proved unreliable.
- **Mentor:** no contact with Prof. Morley yet.
- **Installs:** Stockfish 19 is built; Lc0 v0.32.1 is installed through Homebrew with its bundled network. PyTorch and MLX are in the separate `.venv-ml`.
- **Repository:** private GitHub repo `aritroBh/cylindrical-chess-cgt` (approved 2026-10-21); push only when asked.

## 7. How well the model predicts real chess (2026-10-28/29, research avenues; all COMPUTED-1, skeptic-checked)

- **Flat 8x8** (`research/flat_xtarget_census/`): 2,049 decisive trebuchet+pawn positions with known real results (11 targets):
  the model (e.p.-aware, count) agrees on 1,896 = 92.5% (Wilson 91.3-93.6; positions are not independent). End-position
  sides 90.2%, internal nodes 96.9%. Count beats mover (83.0%) and opponent (83.7%), McNemar p < 1e-24. e.p.-aware beats
  textbook on internal nodes (22 vs 0, p = 5e-7). A2 reproduced (268/14/13). 230 decisive positions rest only on Lichess
  8-man categories; without them 95.1%.
- **Small boards** (`research/agreement_census/`): per board, testable placements beside a frozen trebuchet: cyl:6x6 13/26,
  flat:5x6 23/26 (published layout), cyl:5x5 49/71 (compact layout, no buffer). 37 of 39 mismatches are king effects
  (frozen = model), 23 with a real draw.
- **Why the passer convention fails** (`research/v2_mechanisms/`): all 34 V2 failures on cyl:7x6 are one step-past race (a
  blocked enemy pawn steps level, becomes passed and promotes first). A certified-passer test (square-rule distance) removes
  all 52 convention failures; mismatches 159 -> 128 of 500, no new errors; all 128 left are king effects. Soundness:
  no false certification in 158,544 enumerated positions (sketch proof, unrefereed).
- **Draws** (`research/draw_model/`, T72 OpenCode): of 39 real draws, scoring draws as dud reproduces 21, as 0 or {on|off} none.
- **Convention witnesses** (`research/convention_ladder/`, T73 OpenCode): one witness per convention (C1 passer wins at
  once and C3 e.p. test on cyl:7x6; C4 frozen kings on flat:5x6, CHECKED-2; C2 race rule on 8x8, PROVED by L4; C5
  stalemate on 8x8, CHECKED-2). Mostly from existing data, so minimality is NOT established.
- **Square-rule passer test S** (T74 Kilo referee, `research/v2_mechanisms_check/`): SOUND WITH FIXES; the rule holds
  (0 failures in 158,544 cases, COMPUTED-1) but the proof sketch leaves the e.p.-after-push and blocked-pawn lower-bound
  steps unargued. Status: COMPUTED-1, proof incomplete.
  **Update 2026-11-22:** complete hand proof by T75 (OpenCode, `research/v2_mechanisms_proof/PROOF_S.md`), refereed SOUND
  WITH MINOR FIX by T76 (Kilo; scope H >= 4, applied). Status: PROVED [S] in the frozen-king pawn game.
  **Refuted 2026-11-22:** Lemma 1 of that proof is false and S is not sound in general. Counterexample (found by
  the supplement editor, confirmed here with `research/v2_mechanisms/pawngame.py`): flat 3 files x 8 ranks,
  `W a4 b6 / B c7`, Black to move. S certifies White (n = 4 < d = 5), but 1... cxb6 2. a5 bxa5 and White has no
  move. An enemy pawn two files away captures onto the file next to the runner. Both AI referees missed it; the
  exhaustive check had at most 2 files at 8 ranks. Status now: heuristic, COMPUTED-1 on the small boards checked.
  The paper's claim (the rescoring: 52 failures removed, 128 left) is a computation on 6-rank boards and stands.
  Supplement S16 now gives the definition, the checks and the counterexample instead of the proof.
- **When the trebuchet unfreezes** (`research/trebuchet_unfreeze/`, avenue 4; COMPUTED-1, skeptic-corrected):
  - The 3 refuted P4 contexts (H*, H*2, H0 on cyl:7x6) fail through the rule "a promotion wins at once": requiring the
    new queen to be safe AND no counter-promotion reproduces chess at all 12 roots (root level only; node level differs
    on 302/49,087 and 673/57,757). QRBN vs Q and the stalemate rule change nothing. H0 is a seam effect (flat: convention holds).
  - A tempo test in the frozen model (the mover wins now and after a pass) predicts whether a king move fails to lose:
    96.5% CV on 7,755 king moves on cyl:6x6 (baseline 60.9%). Static features on the 8x8 suite: 83.1% vs 77.4% baseline.
  - The frozen zero fails in 91 of 1,913 resolved random cyl:6x6 positions (4.8%; about 6.6% if the 87 unrun or killed
    positions fail like the resolved cap-2 ones), 135 of 179 failures being chess draws. No good position-level rule found.
  - Several cap-2 batches exceeded the 4 GB target (up to 5.3 GB peak); the limit is restated for later runs.
- **Referee T78, one-sided extension of Corollary 3.8b** (Codex, `delegate/out/T78/REPORT.md`, 2026-11-22; its
  `referee.py` rerun by the planner, same counts). Verdict: correct as stated when "K has no minus event" is read
  over all followers of every K_i and both players; false if read at the root only (S = on, K = {|{|minus}}).
  B >= 1 + M_R(K) suffices for `on`, B >= 1 + M_L(K) for `off`. Exhaustive: 94,456 reservoir/multiset pairs (at most
  3 short components, 5 option edges), 25,296 meet the hypotheses, 0 failures (COMPUTED-1). Supplement S12 updated;
  `kings/theory/LOOPY.md` not edited.
- **Explicit-king sum test** (`research/sum_truth_cyl/REPORT.md`, section "12 GB runs (2026-11-22)", avenue 5;
  COMPUTED-1, one solver; pair data and model outcomes rechecked by the planner). 19 two-component sums on cyl:8x6
  with real kings (anchors Pa3 pa4 Kh4 kb3, components on files d and f), `kpsolve --ep on --promote Q --cap 1`,
  2.6 to 7.6 GB each. 38 positions (either side to move): 19 exact, all 19 equal the model sum's outcome; 19 are
  bounds that contain it; 0 contradictions. 7 pairs are exact for both movers (P21, N1, N4, N6, N7, N8, N9), 5 for
  one. Every P-class (zero) sum is bounds only. Cap 2 gave no answer (two runs stopped at 12 GB, two at the time
  limit). Components alone: 13 of 14 run, 19 of 26 sides exact, 0 mismatches (the agent's first table reported 4
  mismatches; that was a file-name collision on the case-insensitive file system, corrected in the report).
  Earlier pilot (4 GB limit): 0 of 50 pairs finished; frozen-king stand-in 50 of 50; K12 e.p. roots 56,402
  regenerated, 51,050 certified with 0 disagreements.
