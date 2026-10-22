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
| Sum model vs whole-board game | equal: the tree never splits into components before a passer (Theorem 2.3) | proved |
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
  - **Perfect at 1k, 10k and 100k nodes.** At every budget all 233 best moves win and all 233 evals match the
    tablebase, in every CGT class. The 1M-node run is still going (114/233 so far, all correct).
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
  - **Small end positions.** All 306 sides with at most 7 men are resolved against the tablebase: 283 agree with
    the model, 5 disagree and 2 are draws.
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
    target value. 11 and 13 end positions with 8–10 men still decide them.
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

**Lc0** at 1M nodes stopped at 114/233 positions, all correct.

## 8. Decisions

Answered 2026-10-16:
- **E.p.:** respect it (done).
- **Kings:** model them explicitly (A8 started).
- **Mentor:** no contact with Prof. Morley yet.
- **Installs:** Stockfish 19 is built; Lc0 v0.32.1 is installed through Homebrew with its bundled network. PyTorch and MLX are in the separate `.venv-ml`.
- **Repository:** local only, with no remote and nothing pushed. It stays private.
