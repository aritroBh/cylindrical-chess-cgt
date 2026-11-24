# K64. A board bound for the ladder and the limits of finite testing

## Readings

**PROVED** below means a deduction from the supplied definitions and Facts A0, A and B. All counts and outcomes below have that label. There are no solver results.

- **R1.** Results are from White's perspective. Condition (C) compares White to move *after* a bad Black move with Black to move *before* a move at ω. A White pass gives Black the move on the same board with no right.
- **R2.** The tests in (O1)–(O4) use P alone, including stalemate as a draw. In a D-sum, including the sums with −1 and the ladders, and in finite Aux play, a side with no move anywhere loses.
- **R3.** Check forbids every move elsewhere, including an immediate win in the test game. No legal group move leaves its mover in check.
- **R4.** The e.p. right belongs to the mover and expires upon moving. A double step gives the next mover a new right. A right only adds moves. A move available only with the right is an e.p. move in this abstract model.
- **R5.** The result order is L < D < W. A forced win must be finite in the ordinary sums. Both a draw and a White win suffice to match a lower bound of D.
- **R6.** The size of a D-game counts its positions, excluding the two decisive terminal symbols. E1 includes every start, both movers, both roots and all q-states. Options may be cyclic or go to either terminal, regardless of who moves.
- **R7.** The promotion exclusions in (O1)–(O4) apply at the named states. The proofs also hold if the exclusions extend to every state of a root or freeze board. Both sharpness examples below obey this stronger restriction.

## Statement D

### D1. The cutoff is the number of boards outside E — PROVED

Fix the post-move state x with White to move. Write U = P(x) ∖ E(x) and n = |U|. For g in P(x), write h(g) for the Black-to-move state on g with no right. This is the successor of *every* legal White pass at g and belongs to Z(x).

For S contained in U define an auxiliary ordinary win/loss/draw game. Start with the group and one unused Black token (−1). While the token is unused, White has an extra immediate winning option at the unchecked White states whose board is in S. Everything else follows the sum rules. In particular Black can spend the token only when unchecked, and spending it clears the right and removes all extra options. Let F(S) be the set of states in Z(x), **with their specified mover and the token still unused**, from which White can force a finite win. After a token expenditure the continuation is the full group with an inert component. It need not stay in Z(x).

Three properties give the cutoff.

1. F is monotone in S, since White can ignore an added option. F(∅) is exactly the White-winning set beside −1. At every reachable unchecked White state on a board of E(x), White therefore already wins with no extra options. Granting an immediate win at any of those states leaves the winning set unchanged. In a strategy using such a grant, substitute the winning −1 continuation at its first use.
2. Define S₀ = U and Sⱼ₊₁ = {g in U such that h(g) belongs to F(Sⱼ)}. At a live ladder stage with j ordinary White advances left before the terminal option, the White-winning set on Z(x) is F(Sⱼ), for **either** current mover. For j = 0 the unchecked White advance wins immediately, and a legal Black cut to z has exactly the effect of spending the token. Property 1 removes the redundant grants on E(x). For the induction step, a legal White advance on g hands the next stage to Black at h(g). It is winning precisely when that successor is in F(Sⱼ). Before the first advance, ordinary group moves stay in Z(x), and a Black cut has the same continuation as before. A forced-win strategy can use an advance only into a winning successor. Conversely, replace the first use of a winning grant by the actual advance and a winning continuation. On a board of E(x), White can always use the −1 strategy, treating a Black cut as spending the token. This proves the induction even if play before an advance can cycle. Neither direction counts an infinite wait as a finite win.
3. S₁ is contained in S₀. Monotonicity then makes the sequence decreasing. Equality at any step makes it constant thereafter. Otherwise each strict step removes at least one board. If there are n strict steps, Sₙ is empty and cannot decrease further. Thus F(Sₙ) = F(Sⱼ) for all j ≥ n, and F(Sₙ) is contained in each earlier winning set. This includes n = 0.

At u₀ of Tⱼ there are exactly j ordinary advances left. Winning Tₙ from (x, White) is therefore equivalent to winning every ladder from that start. Fact B identifies the latter with (C) at m. The subtraction uses the universal quantifier in E(x) only over the specified reachable unchecked White states. The winning status of a group move need not be independent of the right.

### D2. The bounds b and b − 1 — PROVED, both attained

U is a set of boards, so |U| ≤ b. For the improvement, play P alone from x. By the definition of a bad Black move, White has a forced finite win there. Follow one play of a winning strategy. Its end is a White promotion or Black checkmate. Stalemate could not end that play.

If the play ends in checkmate, the final board has Black in check. Every White-to-move state of Z(x) was entered by a legal Black group move, including x itself. Hence Black is safe on every such board. The mate board is outside P(x).

If the play ends in a White promotion, consider the board immediately before it. If White is in check there, the board is outside P(x). Otherwise that state is in Z(x). If no White e.p. move promotes, the promotion is available without a right and with a right, at every reachable White state on the board. It wins immediately beside −1, so the board lies in E(x). In either case at least one board is outside U.

**Sharpness construction (PROVED).** Use five boards A, B, q, p, e with no checks. The following lists are exhaustive. Ordinary arrows clear the right. A double step is explicitly marked.

| Board | White moves | Black moves |
|---|---|---|
| A | q | B, or a double step to p |
| B | q | A |
| q | e | a double step to p |
| p | e, plus the promotion specified below | A |
| e | none | promote, or move to e, q or p by an ordinary move |

In the first group, the White promotion at p is legal **only** as an e.p. move. In the second it is an ordinary promotion legal with or without a right. In both groups take the bad move A → p, so x is White to move on p **with** the right.

To verify exactness in P, at either root White can freeze to q. Black there must give White the promotion on p with the right. White at q without a right must instead give Black the promotion on e. The non-shuttle Black move from A also gives White the promotion. There are no other root moves to test.

All five boards lie in P(x). From x White can go to e, where Black's ordinary moves reach e, q and p with White to move and no right. From x White can also pass, then Black can go from p to A, giving White the move. A White pass on A followed by the Black shuttle reaches B with White to move. These are reachability paths, so Black is free to decline an available promotion.

Beside −1, White to move on e has no move. From q, White must give Black the promotion on e. From either root, after White goes to q Black can spend the token and leave White to move on q. These four boards are all outside E(x). In the first group, the reachable no-right White state on p also loses beside −1, since its only move is to e. Thus |U| = 5 = b. In the second group every White state on p wins immediately, so |U| = 4 = b − 1. If desired both equalities persist for every b ≥ 5 by adding boards without moves and ordinary Black arrows from e to each of them. Each new board is reachable with White to move and loses beside −1. These equalities concern the board counts in D2.

### D3. A single root test for a given board count — PROVED

At (ω, u₀) with Black to move, White wins every finite ladder. Keep ω active and advance the ladder on every White turn until White can take ⊕. A Black cut instead gives White the move at (ω, z), where White freezes ω and leaves Black without a move. This also covers an immediate cut.

Universal agreement therefore implies both stated root wins in T_b. Conversely, if both roots win for White with Black to move there, **every** bad move from either root gives White a winning continuation from (x_m, u₀), White to move. By D2 its cutoff is at most b. D1's stabilization gives a win at that cutoff, hence (C) at m. This applies to every bad move, including vacuously if there are none. Fact A gives the required universal agreement, including the q-states.

## Statement E

### E0. Exactness of Λ_N — PROVED

Neither root nor q has a checked king. Each root has just one White move, to q. Black at q must move to p and White promotes. White at q must move to e and Black promotes. This verifies the two sides of the zugzwang and the freeze at each root. The only non-shuttle root move for Black is A → c₁. White there can go to q, force Black to p and promote. Thus A → c₁ loses in P alone, as required. None of the named root or q moves promotes.

### E1. All games of at most N positions — PROVED

By Fact A it suffices, for every position t of such a game T, to prove the inequality

> r(c₁ ⊞ t, White) ≥ r(ω ⊞ t, Black).

Imagine Black first passes at ω in the comparison game. If the right side is W, the successor (ω, t, White) is still winning for White. If the right side is D, White can still avoid losing at that successor. A right side of L requires nothing.

While the chain is active, follow the corresponding White strategy at ω. Keep the same test position and mover in both plays. A test move is copied literally, including its terminal result. A White freeze of ω is implemented by cᵢ → q. At that point Fact A0 gives exactly the result of the inert component with the same test position and **Black** to move. Switch to a strategy securing the required result there. Each Black chain move is represented by a Black pass at ω. It hands White the turn on the next chain board, or on e after the Nth chain move.

**Winning case.** At each winning White turn use a strategy minimizing the worst-case number of plies to a White win. This number is finite at each winning state of the finite sum. Indeed, the tree of a winning strategy is finitely branching and would have an infinite branch if its depth were unbounded. Minimum winning time strictly decreases on the chosen White move and on every Black reply, as follows by taking a minimum at White turns and a maximum at Black turns. Thus the same active-ω state with the same mover cannot recur during the simulation. Reaching e would give N + 1 White-to-move visits with ω active, counting the initial visit and the visit after each of the N simulated Black passes. All these visits would need distinct test positions. This exceeds the size of T. Indefinite simulation is likewise impossible by the decreasing winning time. White therefore wins in finite play, either through the test or after a freeze.

**Nonlosing case.** Choose a White strategy avoiding a Black win in the comparison game. Such a strategy exists in a draw on a finite graph: outside Black's forced-win region White can choose a continuation outside it or a White terminal, and Black cannot force entry in one move. As long as the simulation continues, an infinite play is a draw, and a terminal or a White freeze preserves the lower bound. If the Nth Black chain move reaches e, let v be the unchanged test position. Immediately *before* that move the comparison was at (ω, v, Black) under the nonlosing strategy. Black therefore had no test move to ⊖ at v. From (e, v, White), play e → p. If Black plays p → e, repeat with the same v. A Black move in T to a nonterminal leaves White on p with an immediate promotion. A Black move to ⊕ wins for White directly. These exhaust Black's choices because the move to ⊖ was excluded at this particular v. White thus secures at least a draw. This argument needs no limit on the duration of a drawn play.

The two comparisons and the trivial L case prove (C) game by game. Fact A now gives both roots for both movers, and Fact A0 covers every q-state.

### E2. Two failures with explicit results — PROVED

In both rows Black moves first.

| Test and position | Root A of Λ_N | ω |
|---|---|---|
| C_N at N | D | W |
| T_{N+1} at u₀ | D | W |

For ω in C_N, White keeps ω active and decrements whenever the counter is positive. When White receives 0, freeze ω, leaving Black without a move. Black can only pass or shorten the countdown by cutting to 0. For ω in the ladder the strategy is the one from D3.

For the **upper bound D at A**, Black starts A → c₁. At a chain board a White group move to q gives Black a cut in the test as long as it is live (positive counter in C_N, any uⱼ in the ladder). The cut leaves White at q with an inert test. White must play q → e, and Black promotes. If instead White moves in the test, Black advances along the chain. On White's ith chain turn, for 1 ≤ i ≤ N, the counter before moving is N − i + 1, or the ladder position is uᵢ₋₁. Thus a cut after a White group move is always available at that point, and no White test move there is yet terminal. After N test moves and N chain replies, White is on e with counter 0 or ladder position u_N. In T_{N+1} the move from u_N is still an ordinary advance. Any such test move at e allows Black to promote immediately. After e → p Black replies p → e, retaining the same test position. This gives Black a strategy against a White win.

For the **lower bound D at A**, on a White turn at a root or cᵢ, use a White test move whenever one exists, taking ⊕ if available. If the test is inert, play to q. Black then has only q → p, so White promotes. While White uses the test, Black at a root or chain board can only shuttle, enter or advance the chain, or cut the test. A cut leaves White at the same group board with an inert test and the preceding winning reply. If White receives e, play e → p and repeat if Black returns. Either test gives Black no terminal option at all. A Black test move at p therefore lets White promote. This strategy avoids a Black win, which proves the claimed draws.

### E3. No finite family — PROVED

Given any finite family, take N to be the larger of 1 and the maximum of its position counts, using N = 1 for an empty family. By E0 and E1, Λ_N is exact over and agrees with ω on the entire family. By E2 it fails universal agreement. In particular, even a single finite loopy game cannot characterize universal agreement. If “decides” allows an arbitrary decision rule based on the tested comparison results, a positive instance is obtained by deleting A → c₁ from Λ_N. The roots and q still satisfy exactness, there are no bad moves, and Fact A gives universal agreement. The positive and negative instances give identical root and q outcomes on the chosen family.

## Where the rules enter — PROVED

| Rule | Use in the proof |
|---|---|
| Check | D1 grants a test advance only to unchecked White and a cut only to unchecked Black. D2 excludes a Black mate board from P(x) because a legal Black move cannot leave Black in check. |
| E.p. | In D1 all White pass successors on a board coincide, but moves in the group can still depend on the right. In D2 an ordinary promotion works in both versions. The paired examples show exactly how a right-only promotion can use up the last board. |
| Stalemate and no-move losses | D2 uses P stalemate as a draw to deduce mate from a terminal immobility win. In D3 and E2, freezing with an inert test wins by leaving Black without any move. |
| Promotions | The tests for exactness use P wins at the specified post-move states. In sharpness and E the decisive promotions occur away from the roots and q. White's immediate promotion at p also secures the draw strategy in E1 against a nonterminal Black test move. |
| Test terminals | D1 treats the top ladder move as a global White win. E1 copies terminals of either sign literally. At e it separately excludes a Black option to ⊖ and handles a Black option to ⊕. |
| Loopy tests | E1 counts test positions only along a forced finite win, where winning time decreases. A drawn simulation may repeat a test position indefinitely. E3 needs E1 for cyclic games as well as finite trees. |
| Draws | The D1 sets ask only about W, as Fact B permits. E1 treats D separately. E2 gives strategies for both sides of each claimed draw. |

## Weakest step — PROVED

The step most sensitive to turn order is the exit from c_N in E1. Knowing that White can avoid losing at (ω, v, White) *after* a pass would not by itself rule out a Black winning terminal at v. The needed evidence is the preceding simulated state (ω, v, Black), which the nonlosing strategy actually reached. Black could have chosen that terminal instead of the pass. Only after excluding it can White safely hand Black the move by e → p.

## Reproduction

**PROVED.** All counts, bounds and results are symbolic deductions above, with the move tables and strategies specified in full. No numerical experiment or solver is used. To display the complete derivations for every number from the project root, run `cat kings/delegate/out/K64/PROOF.md`.
