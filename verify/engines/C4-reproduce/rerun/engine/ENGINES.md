# Engine search heuristics versus CGT phenomena

*Workstream engine-analysis, 2026-10-15. Companion files:
[`FAIRY_CYLINDER.md`](FAIRY_CYLINDER.md) (cylinder support design),
[`suite/`](suite/) (tablebase-verified EPD suite), [`run_suite.py`](run_suite.py) (UCI runner).*

**Status of everything below.** No engine was installed or run: plan §8 still has the install decision open. Every
statement about engine *behaviour* is a prediction, and each one comes with the experiment that would test it.
Statements about Stockfish *code* come from reading `official-stockfish/Stockfish` master on 2026-10-15. I read it
through WebFetch, which returns a model-written summary of the page with short verbatim excerpts, not the raw file.
Constants and line-level details can therefore carry transcription errors, and they change every week. Re-read
the files at a pinned commit before quoting any number in a paper. WebFetch calls used: 7 for Stockfish source, plus 3 for GitHub
pages (Fairy-Stockfish issue #753, the mtaktikos repository front page, and its commit page, which returned HTTP 429). I also made read-only `gh api` calls for the fork's files (see `FAIRY_CYLINDER.md`).

---

## 1. The CGT phenomena, in engine language

Throughout, the position is a sum `G = G1 + ... + Gk + T`. Each `Gi` is an independent pawn fight on its own
files. `T` is a frozen king structure, such as the trebuchet W Pg4 / B Pg5 / WK f5 / BK h4, where any king move
drops a pawn, so `T = 0` and it acts as a mutual zugzwang. White is Left and moves to make the value larger.

| Phenomenon | CGT description | What a search engine must "know" |
|---|---|---|
| **Mutual zugzwang** | value `0`: the player to move loses | being on move is a liability |
| **Cold games / numbers** | value `n` (or `1/2`, `1/4`): Left has `n` spare tempi. Every move *costs* the mover, since `G^L < G < G^R` | the static score is an *upper* bound for the mover, not a lower bound |
| **Tempo battles** | sums of numbers and infinitesimals (`↑`, `↑*`, `⇑*`). The sign is decided by a count of spare moves, plus a parity term | an exact count of spare moves over the whole board |
| **Nimbers** | `*`, `*2`, …: first player wins, and `*a + *b = *(a XOR b)` | a parity / XOR invariant across components |
| **Hot games** | switches `±x`, `{+W \| *}`: moving is worth a lot; temperature `t > 0` | "move in the hottest component first" |
| **Sums** | the value is additive and can be computed one component at a time, in time linear in `k` | a search sees one game whose length is the *sum* of the component lengths |

The single most useful observation for what follows:

> **The "null-move observation" is a temperature assumption.** Every static-eval-based pruning rule assumes the
> side to move can do at least as well as its static eval, i.e. that being on move is worth ≥ 0. In CGT terms the
> position is not cold. Stand pat in quiescence, reverse futility pruning and null-move pruning all rest on it.
> - For hot games, and for first-player wins such as `*`, it holds: moving is at least as good as passing, so the
>   bound is safe, merely pessimistic.
> - For numbers it fails, because every move costs the mover something: 1 for an integer, `1/2^k` for a fraction with
>   denominator `2^k`.
> - For a mutual zugzwang (`0`) it fails by the whole game.

A classical-evaluation engine encoded this assumption as a constant **tempo bonus** for the side to move.
From memory, and not re-checked: `Tempo = 28` cp in Stockfish 12's classical evaluation. In CGT language that is a
*fixed positive temperature*. The true "tempo bonus" of a cold position is negative.

---

## 2. Stockfish, heuristic by heuristic

Sources: `src/search.cpp` (`Search::Worker::search<NodeType>`, `qsearch<NodeType>`, `reduction`), `src/evaluate.cpp`
(`Eval::evaluate`, `scale_evaluation`, `simple_eval`), `src/nnue/nnue_architecture.h`, `src/nnue/features/pp_3wide.{h,cpp}`,
`src/syzygy/tbprobe.cpp` (`Tablebases::root_probe`, `root_probe_wdl`, `rank_root_moves`). Step numbers refer to the
`// Step N.` comments in `search()`.

### 2.1 Null-move pruning (Step 10, "Null move search with verification search")
- **Condition, as read:** `cutNode && ss->staticEval + 50*priorNMPFailHigh >= beta - 13*depth - 47*improving + 365
  && !excludedMove && pos.non_pawn_material(us) && ss->ply >= nmpMinPly && beta >= -2000`.
- **Reduction:** `R = 7 + depth/3 + max((staticEval - beta)/256, 0)`.
- **Verification:** if the null search fails high, the score is returned **unverified** whenever `nmpMinPly` is
  set or `depth < 16`. Otherwise a verification search at `depth - R` runs, with NMP disabled until ply
  `nmpMinPly = ply + 3*(depth-R)/4`.

**Interaction with CGT.**
- **P1 (structural, almost certain).** `pos.non_pawn_material(us)` is zero in every king-and-pawn position.
  So **NMP never fires in pure K+P positions**, which covers every position in `suite/` and every Elkies-style pawn sum
  frozen by kings alone. Any zugzwang blindness Stockfish shows on these positions comes from somewhere else
  (§2.3, §2.4). This makes an NMP ablation a clean **negative control**: disabling NMP should change nothing on
  the K+P suite.
- **P2.** In sums frozen by *pieces* (Drummond-Cole's \*2 uses B, N, R, Q; Elkies' constructions freeze pawns with
  pieces), NMP is live for any side that has a piece. A null move is exactly a pass. In a component sum of value
  `0` or a small number, the pass turns a lost zugzwang into a win for the passer. The engine then gets a **false
  fail-high**, and it is accepted unverified at `depth < 16`. Prediction: on piece-frozen zugzwang sums, the depth at
  which the correct move first appears jumps to ≥ 16, or to wherever verification first catches the error. With NMP
  disabled it is set by the length of the tempo battle instead.

### 2.2 Late-move reductions (Steps 14–19; `reduction()`)
- **Formula, as read:** `reductions[d] * reductions[mn]`, where `reductions[i] = 2872/128 * log(i)`. Adjustments
  apply for `ttPv`, `cutNode` (+4026), a TT move that is a capture (+1079), `statScore` (history), and whether this
  is the TT move (−2179).
- **Interaction.**
  - K+P positions have few moves, typically 3–9, so `moveCount` stays small and reductions are mild.
  - The CGT danger is *which* quiet move is late. In a tempo battle the winning move is often the "slow" one:
    - the single step when the double step loses (`↑`: W a2 / B a5 — a2-a4 wins, a2-a3 loses);
    - the non-capture when the capture flips parity.
  - History tables are global per (piece, to-square), with no notion of components. They will reward
    "advancing" pawn moves in general.
- **P3.** The *nodes-to-solve* will be larger when the CGT-winning move is not the most advanced or most forcing pawn
  move. Test: split `suite/cgt_verified.epd` by its `c5` flag `only-slow-winning-move` (38 of 181 positions) and
  compare node-sweep curves (E1).

### 2.3 Futility pruning and razoring (Steps 8, 9, 15)
- **Reverse futility (Step 9), as read:** `!ss->ttPv && depth < 19 (6 when seeking mate) && eval >= beta &&
  (!ttMove || ttCapture) && !is_loss(beta) && !is_win(eval)`, then return if
  `eval - futilityMargin >= beta`. **There is no `non_pawn_material` guard.**
- **Razoring (Step 8):** `allNode && eval < alpha - 342*depth` → return the qsearch value.
- **Move-count and parent futility (Step 15):** quiet moves are skipped after `(3 + depth²)/(2 - improving)` moves,
  or when `staticEval + 119*lmrDepth + ... <= alpha`. SEE pruning at `-23*lmrDepth²`.
- **P4 (main prediction for K+P zugzwang).** Reverse futility pruning, *not* NMP, is the zugzwang-blind cut in
  modern Stockfish's pawn endgames. It returns `eval` (blended toward beta) at a node where the side to move looks
  fine statically, without checking that it has a non-losing move. In a mutual zugzwang the static eval of the side
  to move is at best neutral, so the cut needs `eval ≥ beta + margin`. The failure therefore needs a position
  that is *statically good but zugzwanged*: a pawn up, but every move loses. Our trebuchet positions with
  value `0` and an extra blocked pawn are of exactly that kind. An example is W a2 a3 / B a4 with the trebuchet:
  White is a pawn up, has no pawn move and value `0`, so White to move must move the king and drop g4. Test: E2 (an RFP ablation) on the value-`0` and value `≤ 0` positions with the side to move "materially
  ahead".
- Razoring and parent-node futility act on *low* evals. In tempo positions the eval is nearly flat, so they should
  rarely matter. When they do, they discard quiet tempo moves at the horizon, with the same effect as P3.

### 2.4 Quiescence search (`qsearch`)
- **As read:** the stand-pat score is the static eval, blended toward beta (`(441*bestValue + 583*beta)/1024`) when
  it fails high. Only captures are generated, or evasions when in check, with SEE and futility filters
  (`futilityBase = staticEval + 306`). No quiet checks.
- **Interaction.** Stand pat *is a pass*. In a K+P tempo battle qsearch sees only pawn captures and queen
  promotions, so a horizon node in a zugzwang is scored as if the mover could pass.
- **P5.** Static-eval errors at the horizon are side-to-move-blind exactly where CGT says side to move is everything:
  values `0` and `*`, the numbers `±1/2`, and small switches such as `1/2±1/2`. Test E5 evaluates the same pawn
  configuration with each side to move. From White's point of view the correct evaluation flips sign with the side
  to move for `0` and `*`, and does not flip for `±n` with `n ≥ 1`.

### 2.5 Singular extensions (Step 16)
- **As read:** applies to the TT move at `depth ≥ 6 + ttPv` when the TT value is a non-decisive lower bound from
  `ttDepth ≥ depth - 3`. `singularBeta = ttValue - (59 + 66*(ttPv && !PvNode))*depth/63`. The extension is
  +1/+2/+3, and multi-cut returns early. A negative extension (−3) applies when `ttValue ≥ beta` or `cutNode`.
- **P6 (positive interaction; the comparison at the end is speculative).** CGT positions with a *unique* winning move are exactly where SE triggers. These are
  moves to a P-position when all other options lose, e.g. a2-a4 in `↑`. SE should then extend the critical line
  and shorten the time to solve. Nimber sums often have several winning moves, one in each of several components
  (e.g. `* + * + *`), so SE does not trigger there. Prediction: at equal search length, unique-solution
  positions are solved at lower depth than multi-solution positions. That ordering would reverse the naive
  expectation that more solutions make a position easier. Test: in E1, compare `#solutions = 1` with `#solutions ≥ 2`.
- Caveat: once NNUE scores a line as "decisive" (`is_decisive`, roughly TB-win range), SE is skipped. In our
  positions decisive scores appear only when a promotion or mate is inside the horizon.

### 2.6 NNUE and passed pawns (`nnue_architecture.h`, `features/pp_3wide.*`, `evaluate.cpp`)
- **Current master, as read:**
  - Inputs are three feature sets: `Features::K32Q2` (PSQ), `Features::FullThreats` and `Features::PP_3Wide`.
  - `L1 = 1024` (transformed features), then `fc_0: 1024→32`, `fc_1: 64→32`, `fc_2: →1`, with `LayerStacks = 32`.
- **`PP_3Wide`** is a pawn–pawn **pair** feature set over pawns on ranks 2–7.
  - There are `PawnIds = 2*48`, and `Dimensions = 96*95/2 = 4560` unordered pairs.
  - The partner set for each pawn is `pawn_pair_bb(from)`, defined elsewhere. The name suggests a three-file band,
    but I did not confirm that from code.
  - Both same-colour and opposite-colour pairs are features, oriented by the perspective king (`OrientTBL[ksq]`).
- **What this means.**
  - A pawn's "passedness" (no enemy pawn ahead on its own or adjacent files) is a *conjunction of absences* of
    pairs inside a three-file band. A pair-feature first layer plus an MLP can represent it well. So the Elkies
    convention "passed pawn = decisive" is close to what the net can express directly.
  - **Parity and tempo counts across components are not local.** The sign of `*` versus `0`, or of `↑*` versus `↑`,
    depends on the *parity* of available tempo moves summed over independent files. That is an XOR of
    component-level facts, the classic hard function for a shallow ReLU net. Zhou & Riis's Nim results are the
    closest evidence.
- **P7.**
  - The static NNUE eval of `trebuchet + G` will track the *number* part of `G` reasonably well (counting spare
    pawn moves is close to additive).
  - It will be near chance on the *nimber / infinitesimal* part: `*` vs `0`, `↑` vs `↑*`.
  - So the "parity gap" of Track C1 should already be visible in the static eval, before any search.
  - Test: E3.
- **`scale_evaluation` (as read):**
  - material scaling `v += (521*pawns + npm)*v/90649`;
  - 50-move damping `v -= v*rule50/189`;
  - an optimism term;
  - clamping below the TB range.
  - There is **no** special code for passed pawns, pawn endgames or zugzwang anywhere in `evaluate.cpp` (the WebFetch
    summary checked this, and so did a keyword check on `search.cpp` comments).
  - Damping by `rule50` matters only in king-manoeuvre (loopy) positions. There it makes long king shuffles look
    drawish and pushes the engine toward early pawn moves, which are often the wrong move in a tempo battle.
    **P8 (speculative)**; it needs loopy test positions (Track A8), not the trebuchet suite.
- **Correction history.** Stockfish keeps eval correction histories, including a pawn-structure-keyed entry
  (`pawn_correction_entry`). Inside one search this can learn that a given pawn skeleton is worse than its static
  eval, which is exactly the zugzwang correction. **P11:** this partially compensates for P5 and P7 during
  iterative deepening. Test: ablate it, E2.

### 2.7 Tablebase probing (Step 7; `tbprobe.cpp`)
- **In search (as read):** probe when `piecesCount <= cardinality` (and `depth >= probeDepth` at equal
  cardinality), `rule50 == 0`, and there are no castling rights. The WDL result maps to `±(VALUE_TB - ply)`, or to
  a draw. It cuts if the bound is exact or already decides the window.
- **At the root:** `rank_root_moves` calls `root_probe` (DTZ ranking, `tbRank`), and falls back to `root_probe_wdl`.
  Moves are ranked, not filtered. In-search probing is turned off when DTZ ranking succeeded, or when the root is
  not a win.
- **En passant:** the tables contain no e.p. rights. The search works around this, and the code notes that DTZ can be
  wrong when the best move is an e.p. capture.
- **Interaction.**
  - Every position in `suite/` has ≤ 7 men. **With a 7-man Syzygy set the suite is solved at the root by DTZ
    ranking**, so it must be run without `SyzygyPath`. `run_suite.py` warns when that option is given.
  - For sums with more than 7 men, probing short-circuits a line only after captures bring it down to 7 men.
- **P9.** Syzygy helps a k-component sum only through *capture* lines. Pure tempo battles (no captures) gain
  nothing. If true, this is clean evidence that the difficulty is the search length of the tempo battle, not
  evaluation. Test: E7.
- The `rule50 == 0` condition means a probe happens only right after a pawn move or capture. In pawn sums that is
  almost every node, so this condition costs nothing here.

### 2.8 Transposition table and sums
- Moves in independent components commute. So the TT collapses all interleavings: the number of distinct
  positions is about `∏ |states(Gi)|`, while the number of move sequences grows like a multinomial.
- **P10.** Nodes-to-solve for a `k`-component sum grows roughly like `∏ |states(Gi)|`, which is exponential in `k`.
  CGT costs `Σ |states(Gi)|`, which is linear. The ratio is the headline number for Track C1. Test: E4.

### 2.9 Draws and repetitions (Step 2)
- `value_draw` adds node-dependent jitter (`VALUE_DRAW - 1 + (nodes & 2)`), and `upcoming_repetition` lowers
  `alpha`.
- These matter only for loopy king positions (A8). In the trebuchet suite a repetition can arise only after the
  freeze is broken, and by then the game is usually decided.

---

## 3. Lc0 and AlphaZero-style MCTS

There is no null move, no alpha-beta window and no static-eval pruning, so the temperature assumption of §1 is
absent *from the search*. It moves into the **value head**: every leaf is scored by the network, from the side
to move's point of view, with no quiescence.

- **L1 (zugzwang at leaves).** The value head must recognise zugzwang statically. MCTS corrects a wrong leaf value only
  by expanding through it. In `suite/` the longest pawn-play line in a component is 1–6 plies. The conversion that
  follows (king takes the g-pawn, the pawn promotes) is longer. Lichess reports DTM for 8 of the 42 tier-T1 roots, and there mate is 27–31
  plies away. The parent-to-child DTM steps of 1 show that the unit is plies. With a few hundred visits the tree reaches the
  zugzwang, but not the conversion. Correctness therefore depends on the value head scoring "you must
  move a king here" as lost. **Prediction:** for the trebuchet positions, at `nodes = 1` (policy only), Lc0 plays a king move
  more often than its general strength would suggest. In the tablebase data, king moves lose in most tame
  positions (§4), so this shows up directly as errors. This is a hypothesis; Lc0 trains heavily on endgames,
  with tablebase rescoring.
- **L2 (parity, the Zhou–Riis effect).** For a sum of `k` components, the policy has to point at the component that
  restores a zero nim-sum or the right tempo parity. That is a k-way XOR. **Prediction:** policy top-1 accuracy
  against the CGT-winning set falls with `k` for nimber-heavy sums, and much less for integer sums.
- **L3 (the visit budget is spent on the wrong component).** PUCT spends visits by prior × value. In a sum,
  independent components multiply the effective branching, and the visits are split across interleavings. The TT
  analogue in Lc0 (node reuse and transpositions in recent versions) helps less than alpha-beta's TT, because
  statistics are per edge. **Prediction:** Lc0's nodes-to-solve grows faster in `k` than Stockfish's, at the same
  number of value evaluations.
- **L4.** Lc0 also probes Syzygy (`--syzygy-paths`). The same caveat as §2.7 applies.
- **L5 (cylinder).** A standard Lc0 net has zero-padded convolutions, so the board edge is built in. On the cylinder,
  circular padding along files makes the network exactly translation-equivariant (plan C2). This is the
  cheapest correct architecture change.

---

## 4. What the tablebase suite already says (data, not predictions)

Source: `suite/results.json`, built from 275 positions with ≤ 7 men, each checked against the Lichess tablebase. Every
number below is reproduced by `suite/summarize.py` and `suite/race_nodes.py`. The sample is stratified, not
exhaustive.

**The model.** The trebuchet freezes the kings, so any king move loses. The queenside component is scored by
`cylcgt` on the 4-file flat board.

- **Tame components** (no ±BIG in the canonical form) that are race-insensitive, with the A-trebuchet (94
  positions):
  - The CGT set of winning **pawn** moves equalled the tablebase's in **94/94**.
  - The root result agreed in 92/94. Both exceptions are tablebase *draws* where CGT predicted a loss.
  - With the B-trebuchet (54 positions): pawn sets 50/54, root 52/54.
- **"Any king move loses" is the weak point.**
  - In the tame A-trebuchet positions, 41 of 449 king moves only draw and 7 win.
  - The king next to the e-file can give up its g-pawn and still reach the queenside in time.
  - So `bm` always lists **all** tablebase-winning moves. 22 of the 52 disagreements consist *only* of extra
    winning king moves.
- **Promotion races.**
  - At the 33 depth-1 race nodes, `count` matched the tablebase 30 times, `opponent` 22 and `mover` 9.
  - Over the 72 race-sensitive A4 positions, the root result was right for `count` 60 times, `opponent` 57 and
    `mover` 34.
  - So `count` is the best simple rule, and none is exact. The misses include equal-length races that are draws,
    and two passers beating one.
- **The suite.**
  - 181 verified positions. 126 have a unique winning move, and 38 are "slow-move" positions (P3).
  - The value classes cover numbers, nimbers, infinitesimals, switches and hot ±BIG games.
  - The chance baseline is 22% (random legal mover).

**For engines, this means:**
- Expect the suite's hardest positions to be the slow-move and unique-solution ones (P3, P6).
- An engine that finds a tablebase-winning king move which CGT calls losing is *right*. Those positions are in
  `cgt_disagree.epd` with tablebase `bm`.
- The disagreement file is where engine evaluation and the CGT model are *both* approximate: races, exposed kings,
  kings abandoning the freeze. It is therefore the better test of real chess understanding. The verified file is
  the better test of tempo arithmetic.

## 5. Experiments (all runnable with `run_suite.py` once an engine is installed)

`run_suite.py` sweeps `--nodes`, `--depth` or `--movetime` in a single call and records, for each position, the
*solution depth*: the first depth from which every PV head was a solution.

| ID | Question | Protocol | Predicted outcome |
|---|---|---|---|
| **E1** | Baseline scaling on K+P CGT positions | Stockfish, no Syzygy: `--nodes 100 300 1000 3000 10000 100000 1000000` on `cgt_verified.epd` and `cgt_disagree.epd`. Group by value class (number / nimber / infinitesimal / hot / race), by "the winning move is the slowest move", and by number of solutions | ~100% at ≥10⁵ nodes. Below that, failures concentrate in slow-move and unique-solution positions (P3, P6) |
| **E2** | Which pruning is zugzwang-blind? | Recompile Stockfish with one heuristic disabled at a time: NMP (Step 10), reverse futility (Step 9), razoring (Step 8), LMR (Step 18), SE (Step 16), correction history. Run E1 at fixed depths 6–20 | NMP-off: no change (P1, a negative control). RFP-off: fewer low-depth failures on zugzwang positions (P4). SE-off: unique-solution positions get slower (P6) |
| **E3** | Does the static eval know the CGT value? | Stockfish `eval` (or `go depth 1`) on every suite position and its colour-reversed twin. Regress eval on (number part, nimber part, infinitesimal part) | High correlation with the number part. Near zero for nimber and infinitesimal parts (P7) |
| **E4** | Exponential cost of sums | Sums of `k` certified components with frozen kings, `k = 1…5`. On 8×8 only `k ≤ 2` fits (files a and c, plus the trebuchet). For larger `k`, use **Fairy-Stockfish on a 10- or 12-file board with standard rules** (it supports up to 12×10). Measure nodes-to-solve against `k` | Growth like `∏ states` (P10). On 8×8 (`k ≤ 2`), Lc0's nodes-to-solve grows faster than Stockfish's (L3) |
| **E5** | Side-to-move blindness | Same pawn skeleton, both sides to move, value `0` / `±1/2` / `*` / `1/2±1/2` | Wrong-sign evals at shallow depth for `0` and `*` (P5) |
| **E6** | MCTS priors | Lc0 at `--nodes 1 10 100 800`. Policy top-1 against the tablebase-winning set, and rate of king moves at `nodes=1` | L1, L2 |
| **E7** | Tablebase short-circuit | 8–9-man sums, with Syzygy on and off | Gains only on capture lines (P9) |
| **E8** | Piece-frozen zugzwang | Drummond-Cole-style positions, where pieces freeze pawns so NMP is live | False fail-highs. The solution depth jumps to the NMP verification threshold (P2) |

Notes.
- E2 needs a self-built Stockfish. The cleanest switches are compile-time `#ifdef`s around the named Steps.
- E4 and E8 need positions beyond 7 men, so their ground truth is CGT only. Use `sum_safe` positions only, or the
  A2 workstream's tablebase-resolved values.
- Report every configuration with the engine's exact version string. `run_suite.py` records the UCI `id name`.
