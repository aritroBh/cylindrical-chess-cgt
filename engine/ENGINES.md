# Engine search heuristics versus CGT phenomena

*Workstream engine-analysis. First version 2026-10-15 (predictions only); this revision 2026-10-16 adds
measurements. Companion files: [`FAIRY_CYLINDER.md`](FAIRY_CYLINDER.md) (cylinder support design),
[`suite/`](suite/) (tablebase-verified EPD suite), [`run_suite.py`](run_suite.py) (UCI runner),
[`ablation/`](ablation/) (E2), [`experiments/`](experiments/) (E3, E5, E6).*

**Sources and how far to trust them.**
- **Stockfish code.** Every citation is to **Stockfish 19** (tag `sf_19`, commit `edb0d9db`, 2026-09-05), read
  from the local checkout `engine/vendor/Stockfish/` (git-ignored). That is the source of the binary that was
  run. File, function and line numbers refer to that tree. The first version of this file quoted *master* through
  WebFetch summaries. Several of those details are wrong for `sf_19`: the razoring formula, the PSQ feature set,
  the number of layer stacks, and a `scale_evaluation` function that `sf_19` does not have. They are not
  repeated here, and I did not check whether they hold for current master. This revision used no WebFetch
  (the first version used 7 for Stockfish source and 3 for GitHub pages).
- **Measurements.** Each was **computed once**, with one binary and one network per engine, on the suite's
  stratified sample (§5). Stockfish runs are deterministic (1 thread, fixed hash, `ucinewgame` before every
  position). The baseline depth sweep was reproduced exactly: iteration *k* of a depth-16 search equals an
  earlier, separate `go depth k` run in score, nodes and best move, in 1398 of 1398 cases.
- **Ground truth.** It is the Lichess 7-man tablebase for the positions as given. "Twins" (the same men, other
  side to move) were not probed. They are judged against the CGT model only, which is weaker: the tablebase
  disagrees with the model on 4 of the 16 twins a verifier did probe (`verify/engines/C4-theory/twin_results.json`).

---

## 0. Findings in one page

1. **Stockfish's NNUE static evaluation scores first-player wins much like second-player wins: badly for the mover**
   (computed once, 275 positions). Compare the sign of the static eval for the side to move with the tablebase:
   - It is right in 96% of positions whose component is a CGT *number* (43/45), but in only **25% of nimber
     positions** (4/16) and 30% of all N-positions (18/61, where the mover wins).
   - Flip the side to move and Stockfish's eval moves the wrong way in 62% of N-positions. In CGT terms it
     charges the mover a tempo whatever the parity (median −0.30, −0.89 and −0.42 pawns in N, P and L
     positions; about 0 in R), as if the position were a cold game, a number.
   - **Lc0's value head (one node, no search) does much better:** 88% on nimbers (14/16), and the flip goes the
     right way in 97% of N-positions (63/65). §5.3.
2. **In king-and-pawn positions, two of Stockfish's main pruning families are switched off by the code
   itself**, until a pawn promotes somewhere in the tree:
   - null-move pruning (`search.cpp:1011-1012`);
   - all shallow-depth move pruning of Step 15 (`search.cpp:1166`).

   Both are guarded by `pos.non_pawn_material(us)`. Removing them changes no iteration ≤ 5 (null move) or ≤ 2
   (Step 15) of any of the 233 positions. Removing the null move changes no summary number; removing Step 15
   changes one (one more right verdict at depth 8).
   - **Reverse futility pruning is the zugzwang-relevant cut.** Without it, root verdicts are right sooner at
     equal depth (178 → 198 positions at depth 3), mostly infinitesimals and nimbers.
   - At equal node cost the gain shrinks to about 5% and is mixed (§5.2).
3. **The tempo battles that cost Stockfish are about step length, which is parity.** Of its 22 misses at
   depth 1, 14 are ↑ or ⇑\* positions:
   - in ↑ positions it plays the single step when only the double step wins (a2-a3 for a2-a4);
   - in ⇑\* positions it plays the double step when only the single step wins.

   Both of Lc0's policy misses on verified positions are of the ⇑\* kind. These errors go both ways, so they are
   parity blindness, not a bias toward advancing pawns (P3 refined).
4. **The ≤ 7-man suite does not stress either engine's search:**
   - Stockfish 19 picks a winning move in 232/233 positions at 1,000 nodes;
   - Lc0 picks one in 233/233 at 1,000 nodes, and its policy alone in 228/233.

   The CGT-versus-search contrast has to come from sums beyond 7 men, where only CGT gives ground truth (the
   ChessSums benchmark, `bench/`).

The scorecard of all 16 predictions is in §7.

---

## 1. The CGT phenomena, in engine language

Throughout, the position is a sum `G = G1 + ... + Gk + T`. Each `Gi` is an independent pawn fight on its own
files. `T` is a frozen king structure, such as the trebuchet W Pg4 / B Pg5 / WK f5 / BK h4, where any king move
drops a pawn, so `T = 0` and it acts as a mutual zugzwang. White is Left and moves to make the value larger.

| Phenomenon | CGT description | What a search engine must "know" |
|---|---|---|
| **Mutual zugzwang** | value `0`, outcome P: the player to move loses | being on move is a liability |
| **Cold games / numbers** | value `n` (or `1/2`, `1/4`): Left has `n` spare tempi. Every move *costs* the mover | the static score is an *upper* bound for the mover, not a lower bound |
| **Tempo battles** | sums of numbers and infinitesimals (`↑`, `↑*`, `⇑*`). The sign is decided by a count of spare moves, plus a parity term | an exact count of spare moves over the whole board |
| **Nimbers** | `*`, `*2`, …: first player wins, and `*a + *b = *(a XOR b)` | a parity / XOR invariant across components |
| **Hot games** | switches `±x`, `{+W \| *}`: moving is worth a lot; temperature `t > 0` | "move in the hottest component first" |
| **Sums** | the value is additive and can be computed one component at a time, in time linear in `k` | a search sees one game whose length is the *sum* of the component lengths |

The single most useful observation:

> **The "null-move observation" is a temperature assumption.** Every pruning rule based on static evaluation
> assumes the side to move can do at least as well as its static eval, i.e. that being on move is worth ≥ 0. In
> CGT terms, it assumes the position is not cold. Stand pat in quiescence, reverse futility pruning and null-move
> pruning all rest on it.
> - For hot games, and for first-player wins such as `*`, it holds. Moving is at least as good as passing, so the
>   bound is safe, merely pessimistic.
> - For numbers it fails, because every move costs the mover something: 1 for an integer, `1/2^k` for a
>   fraction with denominator `2^k`.
> - For a mutual zugzwang (`0`) it fails by the whole game.

Stockfish 19's evaluation has no explicit side-to-move term. `Eval::evaluate` (`evaluate.cpp:42-68`) blends
the network output with material, optimism and a 50-move damping, and nothing else. The network is evaluated
from the mover's perspective:
- its feature transformer orders the two accumulators as `{side_to_move, ~side_to_move}`
  (`nnue/nnue_feature_transformer.h:232`);
- its PSQT part is the difference of the two (`:235`), which does not depend on who is to move, seen from White's
  side.

So any tempo effect must be *learned* by the positional MLP. §5.3 measures what it learned.

---

## 2. Stockfish 19, heuristic by heuristic

### 2.0 What is active in a pure king-and-pawn position

| Heuristic | Where (`search.cpp`) | Guard relevant here | Active in K+P? |
|---|---|---|---|
| TT cutoff (Step 6) | 872-920 | — | yes |
| Syzygy probe (Step 7) | 922-973 | `piecesCount <= cardinality`, `rule50 == 0`, no castling | only if `SyzygyPath` is set (never for the suite) |
| Razoring (Step 8) | 989-992 | `!PvNode && eval < alpha - 482*depth*depth` | yes |
| Reverse futility (Step 9) | 994-1008 | `!ttPv && depth < 19 && eval >= beta && (!ttMove \|\| ttCapture)` | **yes** |
| Null move + verification (Step 10) | 1010-1044 | **`pos.non_pawn_material(us)`** | **no, until the mover has promoted** |
| Internal iterative reduction (Step 11) | 1048-1052 | `depth >= 6`, no TT move | yes |
| ProbCut (Steps 12-13) | 1054-1104 | captures and queen promotions (`capture_stage`, `position.h:365-376`) | yes, in races |
| Move-count, futility, SEE and history pruning (Step 15) | 1164-1232 | **`pos.non_pawn_material(us)`** (1166) | **no, until the mover has promoted** |
| Singular extensions (Step 16) | 1234-1303 | `depth >= 6 + ttPv`, non-decisive TT bound | yes |
| LMR (Steps 18-19) | 1313-1404 | `depth >= 2 && moveCount > 1` | yes |
| Quiescence (`qsearch`) | 1652-1883 | captures, e.p. and queen promotions only | yes |
| Correction history | 85-107, 1629-1638 | — | yes |

The two guarded rows are a fact of the code, confirmed by experiment (§5.2):
- The null-move build is bit-identical to the baseline through iteration 5 on all 233 positions. It first differs
  at iterations 6-16, in 230 of them.
- The Step-15 build is identical through iteration 2, and first differs at iteration 3 in one position, which has a
  pawn on c6 that can capture onto d7 and promote at ply 3.

### 2.1 Null-move pruning (Step 10, lines 1010-1044)
- **Condition:** `cutNode && ss->staticEval >= beta - 13*depth - 47*improving + 365 && !excludedMove &&
  pos.non_pawn_material(us) && ss->ply >= nmpMinPly && beta >= -2000`.
- **Reduction:** `R = 7 + depth/3 + max((staticEval - beta)/256, 0)` (1017).
- **Verification:** a fail-high is returned **unverified** when `nmpMinPly` is set or `depth < 16` (1027-1028).
  Otherwise a verification search at `depth - R` runs, with NMP disabled until `nmpMinPly = ply + 3*(depth-R)/4`
  (1035-1042).

**Interaction with CGT.**
- **P1, refined after testing.** NMP never fires at a node where the side to move has only king and pawns. In a
  K+P root it can fire only after that side has promoted inside the tree. So an NMP ablation is a near-perfect
  negative control on the K+P suite: no root verdict or best move changed at depths ≤ 16. The first version of
  P1 said "never fires"; the experiment showed it does fire after a promotion.
- **P2 (untested).** In sums frozen by *pieces* (Drummond-Cole's \*2 uses B, N, R, Q; Elkies' constructions freeze
  pawns with pieces), NMP is live for any side that has a piece. A null move is exactly a pass. In a component
  sum of value `0` or a small number, the pass turns a lost zugzwang into a win for the passer. The engine then
  gets a **false fail-high**, accepted unverified at `depth < 16`. Prediction: on piece-frozen zugzwang sums, the
  depth at which the right move first appears jumps to ≥ 16 or to wherever verification first catches the error.
  With NMP disabled, it is set by the length of the tempo battle instead. Test: E8.

### 2.2 Late-move reductions (Steps 18-19; `reduction()`, lines 1885-1888)
- **Base:** `reductions[d] * reductions[mn]`, where `reductions[i] = int(2872/128.0 * log(i))` (713). Then
  `- delta*577/rootDelta + !improving*scale*197/512 + 982`.
- **Adjustments:** for `ttPv` (+929 at 1162, then −3023 − … at 1317), `cutNode` (+4026 + 933 when there is no TT
  move, 1328), TT move a capture (+1079), `cutoffCnt`, the TT move itself (−2179), `statScore` (history,
  1342-1352), and `3*clamp(alpha - eval, -64, 96)`.
- **The reduced depth is `d = max(1, min(newDepth - r/1024, newDepth + 2)) + PvNode`** (1369). So LMR also
  *extends*, by up to 2 plies, moves with good history.
- **Interaction.** K+P positions have few moves, typically 3-9, so reductions are mild. History tables are global
  per (piece, to-square) and know nothing about components.
- **P3, refined.** The prediction was that positions whose only winning move is the "slow" single push are
  harder. The data support a weaker and more interesting claim:
  - Stockfish solves 29/38 slow-move positions from iteration 1 on, against 180/195 others.
  - But its depth-1 errors go **both ways** (§0, item 3). Removing LMR does not help (§5.2).
  - So the difficulty is parity (↑ vs ⇑\*), not the reduction of slow moves.

### 2.3 Reverse futility, razoring, and Step 15
- **Reverse futility (Step 9, 994-1008).** The condition is in the table in §2.0. It returns
  `(661*beta + 363*eval)/1024` if `eval - futilityMargin >= beta`, with
  `futilityMargin = futilityMult*depth - (2789*improving + 335*opponentWorsening)*futilityMult/1024 + |corr|/198435`
  and `futilityMult = min(45 + 4*depth, 85) - 20*!ttHit`. **There is no `non_pawn_material` guard.**
- **Razoring (Step 8, 989-992):** `!PvNode && eval < alpha - 482*depth*depth` → return the qsearch value.
- **Step 15 (1164-1232)** covers move-count pruning `(3 + depth²)/(2 - improving)`, futility for captures and
  quiets, continuation-history pruning and SEE pruning. All of it sits behind `pos.non_pawn_material(us)`, so it
  is off in K+P (§2.0).
- **P4 (main prediction for K+P zugzwang), partly supported.** Reverse futility pruning is the zugzwang-blind cut
  in Stockfish's pawn endgames. It returns at a node where the mover looks fine statically, without checking that
  it has a non-losing move.
  - Measured (§5.2): with RFP off, root verdicts match the tablebase at depth 3 in 198 positions instead of 178,
    and at depth 4 in 210 instead of 195. The gain is largest for infinitesimals (59% → 70% at depth 4,
    85% → 96% at depth 6) and nimbers (88% → 100% at depth 4).
  - But the RFP-off build searches 1.72× the nodes by depth 4. At equal node cost the gain is a 5% geometric-mean
    saving: 32 positions get cheaper and 42 dearer.
  - So the cut is real but cheap to compensate for on these shallow positions.
- Razoring acts on *low* evals. Removing it changes little (§5.2), as predicted.

### 2.4 Quiescence search (`qsearch`, 1652-1883)
- **Stand pat** is the corrected static eval. On a fail high it is blended toward beta:
  `(441*bestValue + 583*beta)/1024` (1744-1754).
- Generated moves are captures, e.p. captures and queen promotions (`capture_stage`), or evasions when in check.
  Other moves are skipped (1814-1816). `futilityBase = staticEval + 306` (1759). SEE threshold −74 (1819).
- When the mover has no legal capture (or evasion), stalemate is tested only if it also has no pawn push and no
  piece, and the last capture took a knight or better (1863-1868). Otherwise qsearch returns the stand-pat
  value. So a K+P node where the mover's only moves are losing king moves is scored as if it could pass.
- **Interaction.** Stand pat *is a pass*. In a K+P tempo battle a horizon node is scored as if the mover could
  pass. Queen promotions are searched, so a race to promote is seen. A breakthrough that is not a capture
  (`b5!` sacrifices) is not.
- **P5, supported (static eval; §5.3).** Static-eval errors at the horizon are blind to the side to move exactly
  where CGT says the side to move decides. Measured: when the side to move flips, Stockfish's White-POV eval
  moves the right way in only 38% of N-positions (25/65), and the right way in 95% of P-positions (20/21).
  That pattern is what a constant negative tempo produces.

### 2.5 Singular extensions (Step 16, 1234-1303)
- **Condition:** the TT move, `depth >= 6 + ttPv`, a non-decisive lower bound from `ttDepth >= depth - 3`, not
  `is_shuffling` (153-160), and not `seekMate` (727: `rootDepth >= 16` and `|score| >= 2000`).
- `singularBeta = ttValue - (59 + 66*(ttPv && !PvNode))*depth/63`, searched at `newDepth/2`.
- The extension is `1 + (value < singularBeta - doubleMargin) + (value < singularBeta - tripleMargin)`. Multi-cut
  returns early (1277-1290). A −3 extension applies when `ttValue >= beta` or at a cut node.
- **P6, not supported.** The prediction was that CGT positions with a unique winning move trigger SE and are
  solved sooner than multi-solution positions.
  - Measured: unique-solution positions are solved at depth 1 *less* often (108/127 against 101/106 by "first
    iteration that stays solved").
  - Removing SE changes no solution and slightly lowers eval accuracy at depths 6-12: 220/228/230 against
    222/229/232. So SE helps a little, as expected, but it cannot act at the depths where these positions are
    decided.

### 2.6 NNUE and passed pawns
- **`sf_19` network** (`nnue/nnue_architecture.h:40-50`):
  - three input feature sets: `HalfKAv2_hm` (king-bucketed piece-square), `FullThreats`, and `PP_3Wide`;
  - `L1 = 1024`, then `fc_0: 1024 → 32`, `fc_1: 64 → 32`, `fc_2: → 1`;
  - 8 PSQT buckets and 8 layer stacks, chosen by `(pieces - 1)/4` (`nnue/network.cpp:153`). Every suite position
    (6-7 men) uses stack 1.
  - The network file is `nn-1a298aa575a0.nnue` (`evaluate.h:36`).
- **`PP_3Wide`** (`nnue/features/pp_3wide.{h,cpp}`) is a pawn-**pair** feature set over pawns on ranks 2-7:
  - `PawnIds = 2*48` and `Dimensions = 96*95/2 = 4560`;
  - the partner squares of a pawn are `PawnPairBB[s]`: its own file plus the adjacent files, ranks 2-7, minus `s`
    (`bitboard.h:130-144`);
  - white-white, white-black and black-black pairs, oriented by the perspective king (`FullThreats::OrientTBL`).
- **What this means.**
  - A pawn's "passedness" (no enemy pawn ahead on its own or adjacent files) is a conjunction of *absences* of
    pair features inside exactly this three-file band. So the Elkies convention "passed pawn = decisive" is close
    to what the first layer can express.
  - **Parity across components is not local.** The sign of `*` against `0`, or of `↑*` against `↑`, depends on the
    parity of spare moves summed over independent files. That is an XOR of component-level facts, a classic hard
    function for a shallow ReLU net. Zhou & Riis's Nim results are the closest evidence.
- **P7, supported for Stockfish, not for Lc0 (§5.3).** Measured on single components, where parity is local:
  - Stockfish's static eval tracks the *number* part well: sign right in 43/45 number positions.
  - It is below chance on first-player wins: 4/16 nimbers, 18/61 N-positions.
  - Lc0's value head gets 14/16 nimbers right. So a network *can* read single-component parity statically. The
    failure is specific to Stockfish's net: its size, its features, or its training data and targets. This
    experiment does not say which.
  - Sums (k ≥ 2), where parity is non-local, are untested (E4).
- **50-move damping:** `v -= v*rule50/199` (`evaluate.cpp:63`). It matters only in king-manoeuvre (loopy)
  positions. There it makes long king shuffles look drawish, which pushes the engine toward early pawn moves.
  **P8 (speculative, untested)**; it needs loopy test positions (plan A8), not the trebuchet suite.
- **Correction history** (`correction_value`, 85-101). The correction is a weighted sum of entries keyed by:
  - pawn structure (×15341), minor pieces (×10569), and the non-pawn pieces of each colour (×12906);
  - continuation entries.

  Each entry is per side to move. It is applied at 840, 850, 1729 and 1740, and updated at 1629-1638 and in
  multi-cut (1281-1287). The pawn-keyed table can learn inside one search that "this whole-board pawn skeleton,
  with this side to move, is worse than its static eval", which is exactly the zugzwang correction. But it is keyed
  by the whole board, not by component.
  - **P11, not supported.** Prediction: it partly compensates for P5 and P7. Measured: removing it is a wash at
    equal cost (33 positions cheaper, 24 dearer, geometric mean 0.96).

### 2.7 Tablebase probing (Step 7; `syzygy/tbprobe.cpp`)
- **In search** (922-973). The probe runs when `piecesCount <= cardinality` (and `depth >= probeDepth` at equal
  cardinality), `rule50 == 0`, and there are no castling rights. The WDL result maps to `±(VALUE_TB - ply)` or a
  draw, and it cuts if the bound is exact or already decides the window.
- **At the root:** `thread.cpp:323` calls `Tablebases::rank_root_moves` (`tbprobe.cpp:1904-1965`).
  - That uses `root_probe` (DTZ ranking, 1790-1863), and falls back to `root_probe_wdl` (1870-1902).
  - Moves are ranked and stably sorted, not filtered.
  - Probing in search is turned off when DTZ ranking succeeded, or when the root is not a win (1953-1955).
- **En passant.** The tables store no e.p. rights. `search()` (1456-1512) probes captures first and does not trust
  the table when every legal move was a capture. The comment at 1452 notes that DTZ is wrong where the best move
  is an e.p. capture.
- **Interaction.**
  - Every position in `suite/` has ≤ 7 men. **With a 7-man Syzygy set the suite is solved at the root by DTZ
    ranking**, so it must be run without `SyzygyPath`. `run_suite.py` warns when that option is given.
  - For sums with more than 7 men, probing short-circuits a line only once captures bring it down to 7 men.
- **P9 (untested).** Syzygy helps a k-component sum only through capture lines; pure tempo battles gain nothing.
  If so, the difficulty is the search length of the tempo battle, not evaluation. Test: E7. It needs Syzygy
  files, which this project does not have (downloading them is out of scope).

### 2.8 Transposition table and sums
Moves in independent components commute, so the TT collapses all interleavings. The number of distinct positions
is about `∏ |states(Gi)|`, while the number of move sequences grows like a multinomial.
- **P10 (untested).** Nodes-to-solve for a `k`-component sum grow roughly like `∏ |states(Gi)|`, exponential in
  `k`. CGT costs `Σ |states(Gi)|`, which is linear. The ratio is the headline number for Track C1. Test: E4.

### 2.9 Draws and repetitions
- `value_draw(nodes) = VALUE_DRAW - 1 + (nodes & 2)` (134). `upcoming_repetition` lowers `alpha` (736-741,
  1662-1667).
- These matter only for loopy king positions (A8). In the trebuchet suite a repetition can arise only after the
  freeze is broken, and by then the game is usually decided.

### 2.10 Other things in `sf_19` that touch these positions
- **ProbCut** (1054-1096) and "small ProbCut" (1100-1104) fire on captures and queen promotions, which in
  pawn races means promotions. Removing them *helped* slightly here (§5.2):
  - positions solved at depth 2: 229 instead of 226;
  - mean solution depth 1.15 instead of 1.24;
  - nodes-to-solve 0.95× (geometric mean).

  One plausible reading: a reduced search after a queen promotion overstates the gain when the opponent
  promotes too. I did not trace this.
- **Hindsight depth changes** (866-870) and **IIR** (1048-1052). Removing IIR changed nothing measurable.

---

## 3. Lc0 and AlphaZero-style MCTS

There is no null move, no alpha-beta window and no static-eval pruning, so the temperature assumption of §1 is
absent *from the search*. It moves into the **value head**: every leaf is scored by the network, from the side to
move's point of view, with no quiescence. The version tested is Homebrew Lc0 0.32.1 with its bundled network
`42850.pb.gz`, on the Metal backend, with default options.

- **L1, refuted on this suite.** The prediction was that at `nodes = 1` (policy only) Lc0 would play king moves
  out of proportion to its strength, because correctness depends on the network seeing "you must move a king
  here" as lost.
  - Measured: its policy move is a tablebase win in **214 of the 216** probed positions that have one.
  - It solves 228/233 suite positions with no search at all. It chose a king move in 24 positions, and those are
    mostly positions where every move loses.
- **L2 (untested; needs sums).** For a sum of `k` components, the policy has to point at the component that
  restores a zero nim-sum or the right tempo parity, a k-way XOR. Prediction: policy top-1 accuracy against the
  CGT-winning set falls with `k` for nimber-heavy sums, and much less for integer sums. On single components
  (k = 1) the value head already gets the parity right (§5.3), so this is now the sharper question.
- **L3 (untested).** PUCT spends visits by prior × value. Independent components multiply the effective
  branching, and statistics are per edge. Prediction: Lc0's nodes-to-solve grows faster in `k` than Stockfish's,
  at an equal number of value evaluations. Test: E4.
- **L4.** Lc0 also probes Syzygy (`--syzygy-paths`); the caveat of §2.7 applies. No tablebases were given.
- **L5 (design).** A standard Lc0 net has the board edge built in. On the cylinder, circular padding along files
  (for convolutions), or file-relative position encodings (for attention), makes the network exactly
  translation-equivariant (plan C2). This is the cheapest correct architecture change.

---

## 4. What the tablebase suite says about the CGT model (data)

Source: `suite/results.json`, 275 positions with ≤ 7 men, each checked against the Lichess tablebase. Numbers are
reproduced by `suite/summarize.py` and `suite/race_nodes.py`. The sample is stratified, not exhaustive. The full
account is in [`suite/README.md`](suite/README.md).

- **Tame components** (no ±BIG in the canonical form), race-insensitive, A-trebuchet (94 positions):
  - the CGT set of winning **pawn** moves equals the tablebase's in **94/94**;
  - the root result agrees in 92/94.
- **"Any king move loses" is the weak point.** In those positions, 41 of 449 king moves only draw, and 7 win.
- **Promotion races.** At the 33 depth-1 race nodes, `count` matched the tablebase 30 times, `opponent` 22 and
  `mover` 9.
- **E.p.-aware passed test** (adopted 2026-10-16).
  - Under `count` it changes **none** of the suite's predicted winning sets, so the EPD files stand as built.
    Checked two ways: `suite/ep_aware_check.py` with sumtest's move generator, and a verifier's minimax
    (`verify/engines/C1-refute/indep_out_epaware.txt`).
  - Under `mover` it changes 20 of 275 sets, and agreement with the tablebase rises from 217 to 236.

---

## 5. Measurements (new in this revision)

### 5.1 Node and depth sweeps (E1)
- **Stockfish 19.** 1 thread, 64 MB hash, no tablebases. Runs are in `runs/`; the depth-16 sweep is in
  `ablation/results/base.json`.

  | limit | best move is a solution (of 233) | root verdict matches the tablebase |
  |---|---|---|
  | depth 1 | 211 | 163 |
  | depth 2 | 226 | 163 |
  | depth 4 | 229 | 195 |
  | depth 8 | 232 | 229 |
  | depth 16 | 233 | 233 |
  | 1,000 nodes | 232 | 229 |
  | 100,000 nodes | 233 | 233 |

  The verdict uses ±150 cp, so it is a crude proxy at low depth.
- **Lc0.** It picks a solution in **233/233** at 1,000, 10,000 and 100,000 nodes, and its root verdict matches in
  233/233 (`runs/lc0/`). A 10⁶-node run was still going when this was written (launched by another session) and
  is not reported.
- **By value class**, Stockfish's root verdict at depths 1/2/4/6/8 is right for:
  - infinitesimals: 30/26/59/85/100%;
  - nimbers: 53/65/88/100/100%;
  - numbers: 79/81/84/93/95%;
  - hot ±BIG: 81/78/91/97/99%.

  Infinitesimals are the last class to come right.
- **Depth-1 misses (22; `ablation/analyze.py` section 6).**
  - 14 are step-length errors in ↑ / ⇑\* positions (§0 item 3).
  - 3 are number positions (±1) where it plays a king move.
  - 2 are `3/2±1/2` switches where it pushes the wrong pawn.
  - 3 are disagreement positions.

### 5.2 Ablations (E2)
Stockfish 19 was rebuilt ten times from the same source: the baseline, plus nine builds with one heuristic
switched off by a compile-time flag (`ablation/sf19_ablate.patch`, `ablation/build.sh`). The baseline rebuild
matches the vendor binary's `bench` node count exactly (2,497,913).

Each build searched all 233 positions to depth 16 (`ablation/run_ablation.py`, 1 thread, 64 MB hash).

| Switched off | First iteration that differs from baseline | Solved at d2 / d3 / d4 | Verdict right at d3 / d4 / d6 | Nodes by depth 4 | Nodes to a stable right verdict (geo-mean vs base) |
|---|---|---|---|---|---|
| — (baseline) | — | 226 / 228 / 229 | 178 / 195 / 222 | 1.00 | 1.00 |
| null move (Step 10) | 6 (most 11-16); 3 never | 226 / 228 / 229 | 178 / 195 / 222 | 1.00 | 1.00 |
| Step-15 pruning | 3 (one position); 1 never | 226 / 228 / 229 | 178 / 195 / 222 | 1.01 | 1.01 |
| **reverse futility (Step 9)** | 2 | 225 / 230 / 230 | **198 / 210 / 228** | **1.72** | **0.95** (32 cheaper, 42 dearer) |
| razoring (Step 8) | 2 | 226 / 228 / 229 | 180 / 195 / 223 | 1.01 | 0.96 |
| singular extensions | 4 | 226 / 228 / 229 | 178 / 195 / 220 | 1.00 | 1.02 |
| ProbCut (Steps 12-13) | 2 | **229 / 231 / 231** | 180 / 194 / 223 | 1.02 | 0.97 |
| LMR (Steps 18-19) | 2 | 215 / 227 / 228 | 177 / 187 / 220 | 0.86 | 1.10 |
| correction history | 1 | 225 / 228 / 230 | 183 / 193 / 222 | 0.98 | 0.96 |
| IIR (Step 11) | 4 | 226 / 228 / 229 | 178 / 196 / 222 | 1.00 | 0.97 |

Reading:
- On this suite every heuristic matters by at most about 10% at equal cost.
- The two code-guarded families are inert, as §2.0 says.
- RFP is the cut whose removal improves root verdicts most at equal depth, as P4 predicted: +20 at depth 3, where
  the next best (correction history) gives +5. Its extra cost roughly cancels the gain.
- These positions are shallow (median nodes-to-solve ≤ 10), so the ablations would need deeper positions, i.e.
  sums, to show large effects.

### 5.3 What the networks know before any search (E3, E5)
Material: the 275 tablebase-probed positions and their 275 twins with the other side to move (all legal).
Labels:
- the tablebase root, for the originals;
- the CGT outcome class `o(G)` of the component (count rule): L = White wins either way, R = Black either way,
  N = the mover wins, P = the mover loses.

The two evaluators are:
- **Stockfish 19's static evaluation:** the `eval` command, "Final evaluation (white side)". The raw NNUE gives
  the same counts.
- **Lc0's value head:** `go nodes 1`, i.e. one network evaluation of the root.

| Group (win/loss roots only) | n | Stockfish static eval: sign right for the mover | Lc0 value head: sign right |
|---|---|---|---|
| all | 258 | 190 (74%) | 226 (88%) |
| L (White wins either way) | 149 | 128 (86%) | 140 (94%) |
| R | 35 | 33 (94%) | 34 (97%) |
| P (mover loses) | 13 | 11 (85%) | 12 (92%) |
| **N, nimber** (`*`) | 16 | **4 (25%)** | **14 (88%)** |
| N, hot with a passed pawn at stake (±BIG) | 28 | 9 (32%) | 15 (54%) |
| N, other (small switches, …) | 17 | 5 (29%) | 11 (65%) |
| tame, race-insensitive numbers | 45 | 43 (96%) | 41 (91%) |
| tame, race-insensitive infinitesimals | 29 | 16 (55%) | 23 (79%) |

**Flip test, judged against the CGT model.** When the side to move flips, the White-POV evaluation should rise
for N (White wins only when it moves) and fall for P:

| CGT outcome | n | Stockfish moves the right way | Lc0 moves the right way |
|---|---|---|---|
| N | 65 | 25 (38%) | 63 (97%) |
| P | 21 | 20 (95%) | 20 (95%) |

Stockfish's median White-POV change, eval(White to move) − eval(Black to move), is −0.30 pawns for N, −0.89
for P, −0.42 for L and −0.02 for R.
- So in these structures its network charges the mover a tempo whatever the parity, except where Black wins
  either way. That is the right instinct for numbers and zugzwangs, and the wrong one for nimbers.
- Lc0's medians are +777 cp (N) and −622 cp (P).

Example: `8/8/p7/5Kp1/6Pk/1P6/8/8 w` (W b3 / B a6, value `*`, b4 is the only win).
- Stockfish statically gives −3.55 for White to move, and −0.96 with Black to move.
- Lc0 gives +510 cp and −267 cp. CGT and the tablebase say White to move wins.

Caveats:
- One net per engine.
- A stratified sample; small groups (16 nimbers).
- The twins are judged against the model, not the tablebase.
- Stockfish's `eval` excludes the correction history, which search adds. That history is what P11 was about,
  and §5.2 found it a wash.
- Lc0's network does far more computation per evaluation than Stockfish's NNUE, which is built for millions of
  incremental evaluations per second. They were also trained differently. I make no claim about *why* Lc0 does
  better.

### 5.4 Lc0 policy (E6)
At one node, the move Lc0 plays is a solution in 228/233 suite positions. The misses:
- two are verified ⇑\* positions where the double step only draws and Lc0 plays it (`cgt042` d2-d4, `cgt175`
  a2-a4);
- three are disagreement positions where the tablebase's only drawing move is a king move and Lc0 plays a
  losing pawn move instead.

On slow-move positions (only a single push wins) the policy solves 36/38, against 192/195 for the rest.

---

## 6. Experiments: status

| ID | Question | Status | Where |
|---|---|---|---|
| **E1** | Baseline scaling on K+P CGT positions | **done** (Stockfish depth and node sweeps; Lc0 node sweeps) | §5.1, `runs/`, `ablation/results/base.json` |
| **E2** | Which pruning is zugzwang-blind? | **done** for 9 switches, to depth 16 | §5.2, `ablation/` |
| **E3** | Does the static eval know the CGT value? | **done** on single components | §5.3, `experiments/static_eval.py` |
| **E4** | Exponential cost of sums | not done: needs > 7 men, so CGT-only ground truth; on 8×8 only k ≤ 2 fits with a trebuchet; larger k needs Fairy-Stockfish on 10-12 files | ChessSums (`bench/`) |
| **E5** | Side-to-move blindness | **done** (flip test; twins against the model) | §5.3 |
| **E6** | MCTS priors | **done** at 1 node | §5.4, `experiments/lc0_value.py` |
| **E7** | Tablebase short-circuit | not done: needs Syzygy files | — |
| **E8** | Piece-frozen zugzwang (NMP live) | not done: needs Drummond-Cole-style positions with ground truth | — |

The protocol of each open experiment is unchanged from the first version:
- **E4:** sums of `k` certified components with frozen kings, nodes-to-solve against `k`, `sum_safe` positions
  only.
- **E7:** 8-9-man sums with Syzygy on and off.
- **E8:** solution depth against the NMP verification threshold of 16.

---

## 7. Prediction scorecard

| ID | Prediction (short) | Status |
|---|---|---|
| P1 | NMP never fires in K+P | **refined**: never fires until the mover has promoted inside the tree; an inert control on the suite (§5.2) |
| P2 | Piece-frozen zugzwang sums give false NMP fail-highs | untested (E8) |
| P3 | Positions won only by a slow move are harder | **refined**: harder at depth 1 (29/38 vs 180/195), but the errors go both ways (↑ and ⇑\*), so the cause is parity, and LMR is not to blame |
| P4 | Reverse futility pruning is the zugzwang-blind cut | **partly supported**: better verdicts at equal depth without it; about 5% at equal cost |
| P5 | Horizon evals ignore the side to move where it decides | **supported** for Stockfish's static eval (flip test) |
| P6 | Unique-solution positions are solved sooner thanks to SE | **not supported** (SE is inactive at the depths that matter) |
| P7 | Static eval tracks numbers, not nimbers | **supported for Stockfish** (96% vs 25%); **not for Lc0** (88% on nimbers); sums untested |
| P8 | 50-move damping biases loopy king play | untested (needs A8 positions) |
| P9 | Syzygy helps sums only through captures | untested (E7) |
| P10 | Nodes-to-solve exponential in the number of components | untested (E4) |
| P11 | Correction history compensates for P5/P7 | **not supported** (a wash, §5.2) |
| L1 | Lc0 policy over-plays king moves in trebuchet positions | **refuted** (214/216 policy moves win) |
| L2 | Lc0 policy accuracy falls with k on nimber sums | untested; sharper now that k = 1 is solved |
| L3 | Lc0's nodes-to-solve grows faster in k than Stockfish's | untested (E4) |
| L4 | Syzygy caveat for Lc0 | design note |
| L5 | Circular padding gives exact equivariance on the cylinder | design note (plan C2) |

---

## 8. Reproduce

Run everything from the project root, one command per block.

The binaries are git-ignored:
- `engine/vendor/Stockfish/src/stockfish` is Stockfish 19 at tag `sf_19`;
- `engine/vendor/sf19_ablate/bin/sf_*` are the ablation builds;
- Lc0 is `/opt/homebrew/bin/lc0`, version 0.32.1.

Build the ten Stockfish variants (offline, about 15 s each):

```bash
sh engine/ablation/build.sh
```

Run one variant on the suite to depth 16, here the baseline (about 30 s; reverse-futility-off takes about 50 s):

```bash
.venv/bin/python engine/ablation/run_ablation.py --depth 16 --bin base=engine/vendor/sf19_ablate/bin/sf_base
```

Print every number in §5.1 (depth part), §5.2 and the P3/P6 splits:

```bash
.venv/bin/python engine/ablation/analyze.py
```

Run the static-eval experiment (seconds; writes `experiments/results/static_eval.json`):

```bash
PYTHONPATH=. .venv/bin/python engine/experiments/static_eval.py --engine engine/vendor/Stockfish/src/stockfish
```

Ask Lc0 for its one-node value and policy (about 20 s):

```bash
PYTHONPATH=. .venv/bin/python engine/experiments/lc0_value.py --engine /opt/homebrew/bin/lc0 --nodes 1
```

Print the side-by-side tables of §5.3:

```bash
.venv/bin/python engine/experiments/compare.py
```

Score the earlier node and depth sweeps:

```bash
.venv/bin/python engine/runs/analyze_sf.py engine/runs/sf19_nodes.json engine/runs/sf19_depth.json
```

```bash
.venv/bin/python engine/runs/analyze_sf.py engine/runs/lc0/lc0_nodes_1000.json engine/runs/lc0/lc0_nodes_10000.json engine/runs/lc0/lc0_nodes_100000.json
```

Check the suite against the e.p.-aware passed test (offline, under 1 s):

```bash
PYTHONPATH=. .venv/bin/python engine/suite/ep_aware_check.py
```

`experiments/compare.py` also prints the §5.4 policy counts, the slow-move split and the miss list.
