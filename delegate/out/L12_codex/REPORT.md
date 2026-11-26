## Five-line verdict

- **CHECKED-2** — L4 matches the theorem. Both seven-pawn positions equal `*2` by default and both lose that value under every stated exclusion.
- **CHECKED-2** — L5 matches the numerical theorem. All 2,048 race assignments give exactly `1/8`. The Lean comment claiming the value check certifies race-list completeness is false.
- **CHECKED-2** — L6 gets both outcomes right. The full paper proposition says more than Lean checks. A legal two-ply prefix witnesses the omitted failure of hereditary sum-safety.
- **COMPUTED-1** — The kernel declarations cover three of the four default L4 starting-player cases, the default L5 identity and both L6 whole-board outcomes. The other published checks use compiled decisions.
- **PROVED** — Unknown fuel cannot certify equality or inequality in these tests. Already-passed input positions are a genuine exception to the public outcome routines' advertised semantics. Every named root is passer-free.

## Reproduce

Run from the project root. **P** regenerates [the independent transcript](results.txt). Arguments `A B`, `eighth`, or `X` after the script name select a claim. **L** prints the actual declaration dependencies and the referee's Lean probes, including the race-table coverage check, into [the Lean transcript](lean-output.txt). Neither command builds the project. For a source-line citation below, run `nl -ba PATH` on the named file. Lean filenames without a directory prefix are relative to `lean/CylChess/`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. nice -n 15 .venv/bin/python delegate/out/L12_codex/referee.py > delegate/out/L12_codex/results.txt
(cd lean && nice -n 15 lake env lean ../delegate/out/L12_codex/Audit.lean) > delegate/out/L12_codex/lean-output.txt
```

## L4 — seven-pawn star-two theorem

**PROVED by inspection.** Compare `dist/tog/sections/08_star2.tex:46–49,69–74` with `Claims/L4_Star2.lean:14–46`. A is White a4 b3 d2 d3 against Black a7 b7 c5. B is White b4 c2 d2 against Black a6 a7 c6 d5. Both are on the ordinary eight-file, eight-rank board, initially without an e.p. flag. The empty files outside a–d stay empty. The default is aware/count. The exclusions quantify over all three race rules with e.p. off and over all three e.p. options with the opponent rule, including their overlap. Every listed setting denotes a real case. The formal value is the component-sum value defined in the paper. The extra theorem covers the remaining positive A/B table entries. None of these statements concerns real kings, accessibility from a chess starting position, the neighboring census theorem, or the older candidate. See `Claims/Common.lean:6–20`, `Rules.lean:54–58,156–174`, `Game.lean:30–37,154–178` and `dist/tog/sections/02_rules.tex:79–86`.

**CHECKED-2** (P, compare the Lean declarations above). Each cell in the last column is the outcome of the **difference** for A and B respectively. P means the starter loses, L means White wins both starts, and R means Black wins both starts. The independent component and unsplit board computations gave the same column.

| E.p. option | Race rule | Paper and Lean, A and B | Independent A, B |
|---|---|---|---|
| aware or textbook | count or mover | both equal `*2` | P, P |
| off | count or mover | neither equals `*2` | R, L |
| aware, textbook or off | opponent | neither equals `*2` | L, R |

**PROVED by inspection.** One docstring overstates its lemma. `Claims/L4_Star2.lean:20–22` describes component counts **and** absence of passers. The statement checks only the counts. The default `IsValue` check itself checks the two passer guards, and P checks them independently in each setting. The numerical theorem is unaffected.

## L5 — one eighth and arbitrary race assignments

**PROVED by inspection.** The displayed position in `dist/tog/sections/07_targets.tex:48–62` is the actual `posG` in `Claims/L5_Eighth.lean:23–36` on the ordinary board. White has a2 b2 b3 and Black has a5 a6 b6. A separate declaration checks the file-reflected position in the nine named settings. The universal assignment declaration concerns the displayed position. `Game.lean:47–73` recursively swaps players to negate a game and constructs `1/8 = {0 | 1/4}`. The two-mover difference test is exact. The nine settings are the full product of the constructors in `Rules.lean:156–168`.

**CHECKED-2** (P and L). Both independent model evaluations gave P for the difference in every named setting. P also tested each assignment in the sum model, with a bit per assignment and a win/loss search for each starter. Reachable open descendants here always have exactly one component, which the bit search asserts. Keys identify the reached position, including a usable e.p. flag, and the mover. Allowing separate winners for different movers also covers assignments that depend on the position alone. The table overrides race adjudication, so the dummy count setting in `Claims/L5_Eighth.lean:57–70` does not restrict the set of assignments.

| E.p. option | Reachable keys, Lean / referee | Assignments | Paper and Lean | Referee, difference is P |
|---|---:|---:|---|---:|
| aware | 9 / 9 | 512 | every assignment | 512 |
| textbook | 10 / 10 | 1,024 | every assignment | 1,024 |
| off | 9 / 9 | 512 | every assignment | 512 |

**COMPUTED-1, reproducible counterexample** (L). `Claims/L5_Eighth.lean:12–15,40–55` suggests a successful value check establishes completeness of the generated table. Pass **an empty table** to the same `Search.isValue` on `posG`: it still returns true for aware, textbook and off. Dropping any single key from the all-White table also still returns true. A missing race makes that *move* unknown. A known winning alternative settles its parent (`Search.lean:39–49`). The generator has a separate limit of 100,000 queue iterations and returns its accumulated keys without signalling exhaustion. The count theorem at `Claims/L5_Eighth.lean:72–82` counts the keys returned by that generator. Neither root success nor list length alone proves every reachable key is in it.

**CHECKED-2** (P and L). The actual lists are complete on these roots. [Audit.lean](Audit.lean) separately walks every move of both colors from the displayed position, follows every quiet component, rejects any missing race, and rejects exhausted fuel. It accepts each generated list and rejects each empty list. [referee.py](referee.py) discovers the keys independently without a queue cap and uses exhaustive binary assignments. **PROVED:** A definite minimax result with a partial table also survives any completion of that table. A certified win needs one known winning option, and a certified loss needs all options known losing. Induction on the successful search justifies both. Thus the empty-table experiment actually supports race-independence. The formal theorem as written quantifies over winner lists on generated keys, without a general Lean theorem relating those lists to arbitrary total functions on reachable races.

## L6 — the sum counterexample

**PROVED by inspection.** `dist/tog/sections/05_sums.tex:19–39,55–59` and `Claims/L6_SumCounter.lean:15–32` give identical pawns, topology, settings and both starting players. X is White b2 d4 g3 h5 against Black a7 c7 f7 g4, on the eight-file cylinder with e.p. off and count races. The occupied run is f–g–h–a–b–c–d, with e empty. The shape theorem asserts one component and no passer for either side. Its outcome theorems assert the following.

| Model | Paper | Lean predicate, mover wins (White / Black) | Independent winners (White starts / Black starts), P |
|---|---|---|---|
| S, BIG = 256 | Black wins both starts | false / true, fast search | Black / Black |
| W | first player wins | true / true, specification | White / Black |

**CHECKED-2** (P for the independent outcomes, L for trust). The `S` result at 256 uses `Search.S`. The additional specification theorem at `Claims/L6_SumCounter.lean:34–40` uses BIG = 24 and fuel 100. That is a separate instance. The independent result above used 256. The distance-to-promotion sums from the listed squares give upper bounds of 18 White and 21 Black pawn moves, as the source comment says.

**PROVED, with replay in P.** The full proposition also asserts that X is not hereditarily sum-safe. Lean explicitly leaves this out at `Claims/L6_SumCounter.lean:11`. Play **h5–h6, a7×h6** across the seam. No passer has appeared. The remaining components occupy b–d and f–h.

- In b–d, **d4–d5, c7–c5** leaves White's d5 pawn passed. The black pawn on c5 is level with it.
- In f–h, **h6–h5, h5–h4, g3×h4** leaves Black's g4 pawn passed. The white pawn has left g3. No earlier move in either line produced a passer.

Definition `def:hss` explicitly permits either side to move in any order when establishing reachability, so the consecutive Black moves are permitted. The two threat lines start at the same quiet split and use distinct components. The paper's omitted conclusion follows directly.

## Rules, bounded search and trust

| Status | Source | Finding |
|---|---|---|
| **PROVED by inspection** | `Rules.lean:81–89,181–198,213–260`; paper `02_rules.tex:4–9,43–47,70–73` | Ranks stop at the edges. Only the cylinder joins a/h. Single and home-rank double pushes require clear squares. Captures take enemy pawns. A double push records the arrival square only when its skipped square can be captured onto. A subsequent move clears or replaces the flag. The capturer must be the victim's enemy. |
| **PROVED by inspection** | `Rules.lean:268–319`; paper `02_rules.tex:26–40` | The blocker test uses strictly ahead, including neighbors. Only the aware test excludes a legally e.p.-capturable pawn. Count favors shortest empty-board promotion distance, with a home double step and ties to the nonmover. The extra front-pawn filter preserves the minimum here. A friendly pawn ahead of a passed pawn is at least as close, and any enemy that could take that front pawn e.p. would already block the rear pawn's textbook test. |
| **PROVED by inspection** | `Rules.lean:342–371`, `Game.lean:116–133,185–207`; paper `05_sums.tex:21–29` | S adjudicates the moved component before splitting, rejoins the terminal file runs across the seam, and preserves other components and their flags. Integer threats can cancel. W adjudicates immediately after a move on the whole board. An e.p. flag survives a move in another summand under disjunctive addition. All L6 runs disable it. |
| **PROVED** | `Game.lean:135–152,161–180,200–207`; `Search.lean:39–64,74–80,87–105` | Zero fuel gives unknown. A win requires a certified option, a loss requires every option certified losing, and no options is a loss. Equality requires two actual mover losses in the negated-target sum. Inequality requires at least one actual mover win. A cutoff cannot satisfy either test on a quiet root by masquerading as a result. A full-tree depth bound of 400 is unnecessary. |
| **PROVED by inspection** | `Search.lean:17–35,51–84,86–110` | The sum key is the normalized component list plus mover. Pawns include both colored lists, direction and e.p. square. Reference trees and the signed integer total are retained. The whole-board key is the full position plus mover. Settings, board, BIG and assignment are fixed for a fresh top-level cache. Fuel can be omitted because only definite answers enter it. Distinct component orders can miss a cache hit without changing an answer. Low-level stateful helpers require a memo originating in the same environment. |
| **COMPUTED-1** (L) | `Search.lean:7–13,26–33,51–68`, `SearchAgrees.lean:55–75` | “Same outcomes” needs a qualification at equal finite fuel. On the sum of +1 and −1, White to move with fuel 1, the specification returns unknown and the fast search returns a definite loss by cancelling to zero. Cancellation preserves the mathematical short game. The agreement file checks a finite family, plus selected eighth cases. It contains no general equivalence proof. |
| **COMPUTED-1** (L) | `Game.lean:154–171,194–207`; paper `02_rules.tex:27–30` | S, W and the inequality test assume an open root but do not enforce it. With a single White pawn on a8, White to move, the paper assigns +256 immediately. S and W both return a mover loss and `notValue` even certifies inequality to +256. They only adjudicate a pawn position *after* a move. `isValue` guards both colors at entry. P checks that the issue does not arise at the named roots. |

**COMPUTED-1** (L). The following is the full trust breakdown for the requested claim files. All native rows printed `propext` and their own `_native.native_decide.ax_1_1`. The two fast-search native declarations, `eighth_all_assignments` and `sumcounter_S`, additionally printed `Classical.choice` and `Quot.sound`. Every kernel declaration listed below printed only `propext`. Importing a module containing a native theorem did not add that theorem's native axiom to an independent kernel declaration.

| Claim | `native_decide` (compiled decision) | `decide +kernel` |
|---|---|---|
| L4 | shape, default A/B, e.p.-off exclusions, opponent exclusions, extra positive settings (`Claims/L4_Star2.lean:21–46`) | Default difference loses for A/White, B/White, B/Black (`Claims/KernelL4_{A_white,B_white,B_black}.lean:7–9`). No A/Black kernel declaration. These are individual outcome statements. |
| L5 | displayed and mirrored positions in nine settings, counts, all assignments (`Claims/L5_Eighth.lean:30–36,76–82`) | Displayed position, default full identity (`Claims/KernelL5.lean:9–10`). |
| L6 | shape, W, fast S at 256, specification S at 24 (`Claims/L6_SumCounter.lean:21–40`) | Both W starters (`Claims/KernelL6.lean:13`, `Claims/KernelL6Black.lean:9`). No S kernel declaration. |

**COMPUTED-1** (source scan below, L for dependencies). No hand-written axiom, admitted proof, unsafe definition, partial recursion, implementation override or external declaration appeared on these claims' project dependency paths. The `partial def loop` in `lean/MoveList.lean:104` is an executable I/O loop outside those imports. The standard library supplies the hash map. List quantifiers in the claims range over explicit nonempty constructor lists, and the claim theorems have no false position/setting hypothesis.

```sh
rg -n '\b(sorry|sorryAx|admit|axiom|unsafe|partial|implemented_by|extern)\b' lean --glob '*.lean'
```

## Independent method and limits

**PROVED.** The Python checker represents a pawn position by its occupied squares and its e.p. flag. It generates both players' moves from the paper, adjudicates passers, and recurses without fuel. The only reference games needed are zero, smaller nimbers and the negative dyadic chain. Every ordinary move decreases the remaining pawn distance or reference-tree height. For the whole-board comparison with a reference, a terminal integer of magnitude 256 dominates the remaining reference tree, so its sign gives the whole-board winner. The program imports no project solver.

**PROVED.** To handle integer summands exactly, let A and B denote the smallest integer shift k for which White wins G+k with White or Black starting, respectively. White's winning shifts are upward closed by the order on short games. For all non-bank options, let U be the minimum child B-threshold over White's moves and V the maximum child A-threshold over Black's moves, subtracting any integer earned on that move. Empty extrema are +∞ and −∞. White can also spend one unit when k>0. Black can spend one when k<0. Hence A = min(U, max(1, B+1)) and B = max(V, min(0, A−1)). Substitution eliminates the same-position thresholds, giving A = min(U, 1+max(0,V)) and B = max(V, min(0,U−1)). At k=0 these thresholds decide both starting players. This accounts for every integer move without a 256-ply pass chain. The separate assignment bit search uses ordinary existential/universal minimax directly.

**COMPUTED-1, scope of this run.** I wrote the independent rules and threshold search from the paper before reading the Lean implementation. The later exhaustive assignment check reuses only my pawn rules. I inspected source and queried the existing Lean 4.36.0 compiled modules with `lake env lean`. I did not rebuild, repeat expensive kernel reductions, audit the compiler or standard library, or check claims about real chess, legality of the historical setups, Möbius play, or the larger census. No network, installs or git commands were used. The sandbox reported `setpriority: Operation not permitted` for the requested nice setting, so the priority change could not be verified.
