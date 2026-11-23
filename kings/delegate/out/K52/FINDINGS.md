## Five-line summary

1. **PROVED.** Theorem 1.11(c) holds with its stated hypotheses. The stopped tempo count in Definition 1.10 requires a new frontier argument.
2. **PROVED.** Dropping (E) is false. On flat 5×7 a six-pawn position gives 𝓡 in S and 𝓝 on the whole board. **COMPUTED-1.** A second witness disagrees with the entitled side to move.
3. **PROVED.** Theorem 1.14(i) works per starter from a pre-event root. Its unrestricted wording admits an already-terminal root for which D credits White and Black promotes first in P.
4. **PROVED.** Part (ii) supplies all of 1.11(c)'s hypotheses. Part (iii) follows for the certified starter because (i) gives a winner. The later bridges require no inference to the opposite starter.
5. **COMPUTED-1.** All 10,960 passer-free roots in the requested ranges satisfy HSS and (E). All agree under each of the three race rules. The failing-(E) stratum is empty.

## The two en passant witnesses

Line numbers throughout refer to `kings/theory/LOOPY.md` in the reviewed checkout. W denotes whole-board play with a global right. Outcome letters use lines 250–259, so 𝓡 means Black wins with either starter. All pawn examples use the adopted e.p.-aware passed test. The witnesses use the count race rule. Commands at the end reproduce the examples and the census.

**PROVED — lines 478–480.** On flat 5×7 take White a4, b3, e2 and Black a5, b4, e4. White has just played a2–a4. The right belongs to Black on a3. The a/b group is locked except for Black's b4×a3 e.p. That capture leaves a black passer on a3, so the group is {|−256} = −257. The e-file is a single move for either player, worth *. Either push locks the file. S is −257 + *, a Black win whoever starts.

In W, White starting plays e2–e3. The right expires, both groups lock, and Black has no move. Black starting wins immediately by capturing e.p. Thus o(W) = 𝓝. The position and its immediate double-step predecessor are passer-free. The e-file can never produce a threat, a/b has only two files and cannot split into two nonempty groups, and the rank-distance budget of either side is at most 3·5 < 256. This proves HSS and (B) throughout. (E) fails at the root. The only discrepant entry here has White moving first with a right created by White. The theorem is about an outcome pair and includes that entry.

**COMPUTED-1 — disagreement also on the ordinary chess turn.** Same board and same last move. White a4, b2, b3, e2, e4 against Black a5, b4, b6, e6, **Black to move**. S is 𝓝 and W is 𝓛. The a/b group has value −1. The e-file has value {2 | 1}. In S Black plays e6–e5, retaining the right in a/b and leaving −1 + 1 = 0 with White to move. In W the three Black options b6–b5, b4×a3 e.p. and e6–e5 all give White a win. White has winning replies a4×b5, b2×a3 and e2–e3 respectively. The same two-file and single-file geometry proves HSS, the distance bound is at most 5·5 < 256, and a2–a4 from the passer-free predecessor genuinely creates the right. Both witnesses start with a flag. The result concerns the theorem as stated and does not settle the additional restriction of a flag-free initial root.

**Replacement for 478–480.** “Assume (E) on the indicated any-order reach. The conclusion can fail without (E), even with HSS, the bound and a passer-free root. On flat 5×7, after a2–a4, W a4 b3 e2 / B a5 b4 e4 gives o(S) = 𝓡 and o(W) = 𝓝.” The earlier bounded searches in lines 790–808 remain observations about their search spaces. Neither this pawn counterexample nor a failure of HSS proves failure of a fully certified real-king bridge.

## Theorem 1.11(c), step by step

The mathematical verdicts below are **PROVED** by the arguments here. Numerical engine checks of specified positions are **COMPUTED-1**. A GAP marks an inference for which the printed proof needs an argument. A FALSE verdict concerns the identified assertion.

| LOOPY lines | Step | Verdict and reason |
|---|---|---|
| 232–249 | Last-rank convention | **SOUND** on legal pawn placements. There is no square ahead and an enemy pawn alongside on that rank would be on its own first rank. A pawn on its last rank has no move. Every promotion therefore gives a passer, and can also free an enemy passer. |
| 302–314 | Order of operations | **SOUND for the move recursion.** `pawns._child` scores a two-colour race across the entire moved component. Otherwise `value` returns a one-colour score before splitting. Only a child with no passer is split. An untouched summand keeps its flag. The separate behaviour of a direct call at a terminal root is discussed below. |
| 398–419 | Any-order moves and the meaning of a threat | **SOUND** for any order and for including a suicide made by either player. **FALSE** that the scored-terminal definition always gives the same τ as `common.threats`. A race has one credited terminal. The code records both colours with passers. |
| 469–482 | Hypotheses | **SOUND** as sufficient conditions, under either choice of τ described below. The proved equality is of outcomes. The separate roles of the four hypotheses are given below. |
| 484–487 | Unfolding S | **SOUND** as a raw disjunctive game form before the first freeze. **GAP** in the description of general states. Spending a token produces B−1, outside a multiset containing only ±B. A live tuple can in general carry separate flags. Write “a tuple of live components with their local rights and integer stacks initially of size B; spending a token reduces a stack's magnitude by one.” Use the displayed move form before canonical simplification. |
| 488–493 | Beneficiary spends positive stacks, opponent plays pawns | **SOUND.** A positive integer offers only Left moves. **FALSE** under literal scored τ that “a race needs both threats.” What is required is that a freeze against the beneficiary would exhibit an adverse scored terminal. |
| 493–499 | Inheritance by re-split daughters | **SOUND.** An ordinary push or double step cannot disconnect the occupied files. Any splitting capture, including e.p., clears the flag. At the split all siblings are passer-free. Play the daughter's putative threat sequence alone, leaving its siblings motionless and flag-free. The same event with the same mover and score occurs in the parent. Prefix the splitting capture. Consecutive moves of the same player must be allowed in this argument. Without a split one just prefixes the move. |
| 500–506, 513–515 | Charging every subsequent opponent move to the stopped M | **GAP.** After a later freeze in one daughter, S can continue in a sister. Play in their original D-coordinate stopped at that event. (E) handles flags, but does not remove the stopping rule. “Its moves are moves of D” is **FALSE** if read as one continuing D-play. The token calculation is **SOUND** given a bound on total moves, but the printed proof has not established that bound. Use the quiet-move proof below. |
| 507–508 | Induction measure | **SOUND.** Use the sum of all remaining distances to promotion. Every pawn move reduces it, including a capture, a double step or a promotion. |
| 509–513 | Both models give the nonterminal child | **SOUND** up to deletion of inert flags. For one component the active flag is treated identically. For multiple components, (E) makes any retained old flag unusable. Erasing it neither adds a passer nor changes any option or successor. A freshly made usable flag belongs to the component that moved. By hereditary reach the induction hypothesis applies to the child. |
| 513–515 | No pre-frontier right available for a later opponent e.p. capture | **SOUND** in the stated application. If another component survives there were at least two at the parent, so (E) excludes such a usable right. A right created by the freezing move is in the frozen component, and the stack player makes no later pawn move. This fact alone does not bound a stopped count. |
| 516–520 | Beneficiary, HSS, application of the bound | **SOUND** that the credited sign is a threat, so HSS excludes the adverse sign in every other component. **FALSE** that both scored signs must occur in a race. **FALSE** in general that the re-split M(Y) ≤ M(X). Use M(Y″) ≤ M(Y) < B directly from (B) at Y. See the example below. |
| 521–523 | Agreeing race scores and minimax | **SOUND with (E).** No unaffected component can acquire a passer merely by losing its flag. Thus all passers are in the moved component and the same mover and local distances determine the score. This also covers the mover and opponent rules. Matched child winners, including the no-option loss, give the two starter entries. |
| 525–529 | Re-grouping the D-game | **SOUND** for a D-game with one global e.p. flag. Regrouping does not change the game graph. An independent-coordinate product that retains local flags requires the pre-event identification under (E). |

**PROVED — replacement for the tempo argument at 488–506 and 513–520.** Fix the first positive freeze; the negative case is the colour reverse. Left spends positive tokens. Call a Black move *quiet* here if it does not freeze its live component, captures included. In each component C still live at the frontier, project Black's subsequent play onto C and its daughters, and omit Black's freezing moves. The quiet moves form a legal sequence in the single, unsplit, stopped D-game on C:

1. Omitting a freeze leaves that daughter in its last passer-free position. It is never played again. Its files are separated from every subsequently played sister. Leaving it there cannot affect the squares or blockers of the retained moves.
2. An initial right of C, if relevant, is available for its first local move. A split clears the flag. From then on Black is the only pawn mover, so no move creates a right for Black. Retaining or dropping a later local flag cannot change the legality of a Black move.
3. Check the stopping rule inductively. Every daughter immediately after a retained move is locally passer-free, and a parked daughter was passer-free when parked. The only extra passer a global flag expiry could expose in this projected play is a Black pawn previously protected from being called passed by its own double step. A White double-step flag present initially has been consumed by the first move of C, before C can have flag-bearing sisters. Loss of protection alone therefore gives a **Black-only** passer. Its first occurrence would be a reachable Black terminal of C, contrary to the no-adverse-threat assumption. This argument works even for literal scored-terminal τ.

Hence at most M_Black(C) quiet Black moves come from C. Sum this over the surviving frontier components. Their total quiet count q is less than B by (B) at the parent and by discarding its moved component. Every other Black move freezes a component and supplies a fresh +B. Just before a Left turn following q quiet moves and f freezes, Left has spent at most q + f tokens. At least B − q + (B−1)f ≥ 1 remain. Left always has a move. Each Black move advances a pawn and only finitely many are possible; Black loses first. This supplies the frontier result with the original stopped tempo hypothesis. Replacing M by a bound that allows play past passers, such as the rank-distance budget, gives a shorter proof under a stronger numerical hypothesis.

**COMPUTED-1 — false monotonicity at 519.** Flat 5×6, e.p. off, W a2 a3 c2 d2 d3 e3 / B a4 b3 d4. Before c2×b3 the stopped M_Black is 1 in the one component. After the nonterminal capture the daughters have Black counts 1 and 1. In either daughter the Black capture creates a White passer. The re-split sum of counts is 2. HSS and (E) hold. Monotonicity at line 402 applies inside a fixed graph. Dropping the last comparison to M(X) at 519 costs no hypothesis.

**PROVED — replacement for 416–422, 492–494 and 517–519.** Distinguish “can reach a terminal credited to Black” from “can reach a position with a black passer.” For example, on flat 8×8 W b2 d6 / B c7, c7×d6 gives both colours a passer; both distances are five and White wins the tie. While c7 stays put, White can advance the b-pawn. If Black later takes it on b6, the white d6 passer has two steps left and the black b6 passer has five. If Black instead takes d6, the b-pawn is at least as fast as the black d6 pawn, with White winning ties. A black push frees d6, whose remaining distance is smaller than the black pawn's. Any White capture of c7 removes the only black pawn, and d6–d7 produces a White passer while c7 is still held by the b-pawn or loses the race to d7. Thus there is no Black-scored terminal (`examples.py` checks the full tree). Suggested wording: “For the pawn implementation τ records each colour with a passer at the first event, both in a race. This contains the scored-terminal τ of Definition 1.10. In the proof it suffices that the credited sign belongs to τ.” In every proof line use only the credited sign. The operational HSS test can reject more roots under these definitions.

### Necessity, boundaries and short boards

- **PROVED — (HSS), 475–476.** It cannot be dropped uniformly. Flat 5×6, W a4 d4 / B b5 e5, e.p. off. Either starter wins W by an immediate capture. Each pair has value {B | −B} because each side can capture for its own terminal and every move is terminal. The two identical switches are negatives of each other, so S = 0. (E), the bound for B = 256 and the passer-free root all hold. An unsafe position can still give the right answer by accident.
- **PROVED — (B), 477.** The exact threshold is sufficient. One component with no subsequent split needs only B ≥ 1 by 1.9 even when its tempo count is larger. A size restriction matters for a uniform theorem with variable B or unrestricted boards. Take W a4 / B b5 on one component and, on a separated file d, W d2 / B d3 and a rear black pawn. The front pair is locked and the rear pawn supplies n Black-only tempi, giving −n. On flat 4×7, a rear pawn on d6 gives n = 2; take B = 1. With White to move, a4×b5 wins W. Every White option in S goes to at most B−n = −1, so White loses. The construction is HSS with e.p. off. For fixed B on an unrestricted height, put the rear pawn on rank B+5 and use height B+7, giving n = B+1. On the actual `kings/SPEC.md` boards (dimensions at most 8×8), B = 256 automatically exceeds even the packing bound 8(1+2+3+4+5+6) = 168 per side. No independent counterexample to this automatic hypothesis is possible there.
- **PROVED — (E), 478–480.** The six-pawn example proves it cannot be deleted from a uniform statement. Its failure alone need not change an outcome, for example if the other component is already locked and has no moves.
- **PROVED — root condition, 469–471.** A single credited colour at a terminal root is harmless: `value` checks global passedness and returns its signed BIG. The restriction matters if both colours already have passers. Flat 8×8 W a2 / B h7 gives +B − B = 0. The mover who made the event is unspecified, `common.W` rejects that root, and any separately specified decisive winner would give a constant winner, unlike 𝓟. If both passers are in one component, `_value` can instead raise `RaceError`. Replace “S, W and D are defined on every board height” (239) by “The promotion recursion is defined at every supported height from a passer-free root; initial races require a separate convention.”
- **PROVED — heights 4 and 5, 232–249.** On four ranks W a2 / B b3 is passer-free and a2–a4 promotes in one move. The adjacent b3 is not on the victim's rank, so the retained flag is inert. Both sides now have passers, White is at distance zero and wins the count race. On five ranks, from W a2 b2 / B b4 the move a2–a4 leaves a4 e.p.-capturable and neither side passed. The **White** option a4–a5 is decisive in the any-order tree. It is not White's turn immediately after its own double step in alternating chess. For H ≥ 5 a legal mover with an opponent-created flag cannot promote from a passer-free position: a last-rank capture would require an enemy pawn on its own first rank, a double step stops short, and a pawn one step from promotion is already passed unless it is itself the vulnerable pawn. This reconciles the two examples. In S/D a promoting race follows the selected race rule; in P the promoter wins immediately, an issue for (V2).

**Recommended label for 1.11(c): PROVED with the frontier replacement above.** The printed proof has a tempo GAP and two false subsidiary assertions. The unrestricted deletion of (E) is refuted.

## Theorem 1.14, step by step

**PROVED — missing initial-terminal case, 582–611, 625–634.** (V2) covers only an event *reached by a move* from a pre-event node. If the pawn context already has a passer and W/D credits it immediately, there is no such node. On cyl 8×6 take Ka1, ka6, White c2 d4, Black d3, Black to move, with the a-file king group as in P11. White's d4 is passed; Black's d3 is blocked in the passed test by c2. D credits White. Black plays d3–d2 and then d2–d1 promotes. White has no one-move promotion, check, capture of d2 or way to block d1 in between. Thus Black wins P. This works with free kings. If Definition 1.5 is read as allowing only pre-event initial nodes, the offending instance is outside its domain, but that domain restriction must appear in the setup.

**Replacement for 590–596 and 605.** “Fix a starter s and an initial position before the first context event. Alternatively, if the convention already credits a terminal at X, specify its beneficiary and require X, with starter s, to be a P-win for that beneficiary. In this second case the conclusion of (i) follows directly from the root certificate.” A starting race needs an explicit scoring convention as well. P11 already makes the corresponding root check.

| LOOPY lines | Step | Verdict and repair |
|---|---|---|
| 605–612 | Quantification, no draws, example | **SOUND** per certified starter on the pre-event domain, **FALSE** for unrestricted credited terminal roots. “No draws” is the optimal result at (X,s). In the example Black has only a5–a4; c8=Q mates. White starting can promote at once, violating (V3). Nothing licenses the other starter. Only context passers count here; c7 belongs to Z. |
| 625–626 | Delete Z, then shortness | **SOUND** from a pre-event root. Delete the terminal suicides on paths from this starter by Lemma 1.7, including the case where the only option is deleted. The remaining pawn game is short. Read the component product here with a global flag, or identify it along those paths using (V1a)'s (E). |
| 627–629 | Realize the winning strategy, cover replies | **SOUND.** A winning player never chooses its own suicide. (V1a)'s equality of moves and successors also makes its chosen pawn move legal in chess. Every legal reply of the loser is covered. Induction on the played prefix keeps the argument on chess-reachable nodes of this starter. |
| 630–632 | Terminal sign along the strategy | **SOUND.** All replies at a loser node preserve the winner. A terminal taken by either side must be credited to the winner. This includes a scored race. |
| 633 | Play ends at such a terminal | **SOUND** before the first event. Nonterminal pawn moves strictly decrease the distance potential. Use (V1b) and (V1a) in the **undeleted** game: a side stranded after suicide deletion still has an actual legal move and must take a losing terminal. |
| 634 | Transfer to P | **SOUND** for an event reached by a move, by (V2). **GAP** if invoked for an initial terminal; use the separate root clause above. |
| 613–620, 635–640 | Part (ii) and re-grouping | **SOUND** using the repaired frontier proof. The pawn root is explicitly passer-free. The all-orders (V4) gives HSS and (B); (E) is separately quantified on that same reach. Neither condition is inferred from alternating chess play. The pawn-only equality supplies a full D/S pair; (i) transfers just its s-entry to P. Applying (i) a second time with the opposite starter justifies the P pair if the stated assumptions hold there too. |
| 335–340, 621–622, 641 | Part (iii) | **SOUND** after the root qualification in (i). **FALSE** that (A_Q) alone says equality: it is the implication “P-win for σ ⇒ chess-win for σ”. It says nothing about a P-draw. Replace the proof by “By (i) the fixed starter has a P-winner σ. By (A_Q)(X,s) this σ wins chess from the same root and starter, hence the two entries agree.” |

**PROVED — downstream starter audit.**

| Use | What is certified |
|---|---|
| Sharp form, 646–669, 671–692 | A P-position includes its side. The finite-rank induction proves a win for each member of the certified set, including its designated root. No certificate for the opposite turn follows or is needed. |
| Chess bridge after 3.2, 1746–1773 | π preserves the turn. The White strategy, Black replies and no-stalemate check are along play from that X. A colour-mirrored statement is a separate instance. |
| Theorem 3.2‴, 2196–2237 | (a) starts with explicit s. (b) covers every **regular side-labelled position** and requires both punishment hypotheses there. Two punished colours do not imply coverage of two initial starters. A result for the opposite initial turn requires it to be regular or to satisfy the hypotheses as a new root. No inference to that turn occurs in the statement. |
| P11, 115, 2965 | Treat a solver root as (X,s), exactly as the row defines its counts. Its terminal certificates include the root if needed and use the actual starter and beneficiary. The S clause additionally requires a passer-free pawn root, HSS, the tempo bound and (E) on the any-order pawn reach. State those quantifiers explicitly if printing an equality with o(W) or o(S): “the entry for s; both entries if separately certified.” An initial race needs the root-credit convention noted at 115. |
| P12, 116, 1167–1186, 2966 | The frozen win, its strategy and all opponent king deviations are at nodes from one specified starter. The contrapositive and the chess implication use that same starter. No second-start certificate is needed. |

**Recommended labels.** **1.14(i): PROVED for pre-event or separately certified terminal roots; FALSE as an unrestricted assertion about already-credited roots.** **1.14(ii): PROVED** under its printed hypotheses and the repaired proof of 1.11(c). **1.14(iii): PROVED** on the corrected domain using (i) and the one-way (A_Q) for that starter. Its one-line “tautology” proof omits (i). In using a solver for (A_Q), note the existing inconsistency at line 345: as line 294 explains, `--frozen` computes F; a comparison to P needs a free-king P solver.

## Exhaustive comparison

**COMPUTED-1.** All labeled placements with 0–2 White and 0–2 Black pawns on interior ranks, with disjoint squares, were generated for each board. The empty position is included once per board. A legal-position pawn on its last rank is already passed, so none can be missing from the passer-free count. For each placement the program tries no flag and every flag possible after a geometrically valid last double step (victim on its landing square, start and transit squares vacant). Geometrically valid but unusable flags are shown separately. These are model states with two starter entries, without an initial-array retrograde requirement. Files, colours and symmetric placements retain their labels.

`check.py` uses a memoized all-orders recursion: at each nonterminal it checks `common.pairwise_safe` using the implementation's two-sign race threats and checks (E) for a usable flag in multiple components. Both conditions must persist at every child. It compares `cgt.outcome(pawns.value(...))` with the non-CGT, global-flag alternating minimax `common.alt_outcome`. Neither scoring nor the move generator is independently reimplemented; the evidence label is COMPUTED-1. Fresh processes isolate rules and boards. Memoization of the already-interned pure integer constructor changes no value.

| Board | No flag | Inert flag | Usable flag | HSS + (E) | HSS failing (E) | S/W disagreements in either stratum |
|---|---:|---:|---:|---:|---:|---:|
| Flat 3×4 | 27 | 0 | 0 | 27 | 0 | 0 |
| Flat 3×5 | 191 | 0 | 60 | 251 | 0 | 0 |
| Flat 3×6 | 717 | 268 | 132 | 1,117 | 0 | 0 |
| Flat 4×4 | 53 | 0 | 0 | 53 | 0 | 0 |
| Flat 4×5 | 403 | 0 | 120 | 523 | 0 | 0 |
| Flat 4×6 | 1,543 | 688 | 264 | 2,495 | 0 | 0 |
| Cylinder 3×4 | 37 | 0 | 0 | 37 | 0 | 0 |
| Cylinder 3×5 | 271 | 0 | 120 | 391 | 0 | 0 |
| Cylinder 3×6 | 1,027 | 324 | 264 | 1,615 | 0 | 0 |
| Cylinder 4×4 | 73 | 0 | 0 | 73 | 0 | 0 |
| Cylinder 4×5 | 565 | 0 | 224 | 789 | 0 | 0 |
| Cylinder 4×6 | 2,173 | 936 | 480 | 3,589 | 0 | 0 |
| **Total per rule** | **7,080** | **2,216** | **1,664** | **10,960** | **0** | **0** |

**COMPUTED-1.** The table holds separately for count, mover and opponent, giving 32,880 rule/root comparisons. There are no disagreements to list in the requested census. The two out-of-range disagreements above are separate count-rule checks. To compare with the earlier 1,306, select the six configurations listed at 246–249, take only the no-flag column, and remove one empty root from each.

**PROVED — why the failing-(E) stratum is empty.** A usable right requires two opposing pawns alongside. With just those two in their component, the would-be capturer has no enemy pawn strictly ahead and is already passed. A passer-free component with a usable right thus needs at least three pawns. Any second passer-free component needs both colours. Five pawns are required, and captures cannot increase the material from a four-pawn root. For the HSS count, if four pawns form two passer-free components, each is a pair. On at most four files at least one pair must occupy only one file, as two disjoint two-file runs would need a gap. An opposing pair on one file in a passer-free position can only approach and lock, so carries no threat. The same arguments apply to every nonterminal descendant, including any re-split.

## Reproduce from the repository root

The first command checks the named pawn examples, including both counterexamples, the re-split tempo inequality, the race definitions and the short-board promotions. The second emits the complete census, all mismatching positions if any, and peak RSS in bytes on macOS. After shape, width, height and flag kind, row fields are passer-free roots, HSS+(E), HSS failing (E), disagreements passing (E), disagreements failing (E). The checked outputs are in `count.txt`, `mover.txt` and `opponent.txt`. Hand verifications and the general bounds above use the displayed moves and inequalities.

```sh
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.
.venv/bin/python kings/delegate/out/K52/examples.py
for rule in count mover opponent; do
  for shape in flat cyl; do
    for files in 3 4; do
      for ranks in 4 5 6; do
        nice -n 10 .venv/bin/python kings/delegate/out/K52/check.py "$shape" "$files" "$ranks" --rule "$rule"
      done
    done
  done
done
```
