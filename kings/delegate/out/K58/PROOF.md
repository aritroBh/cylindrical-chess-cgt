# K58. Comparing a king shuttle with over

## 1. Readings

**PROVED** below with the following interpretations. In this note W and L always name the winner from White's point of view, even on Black's turn. A *nonloss* for a player means that player can guarantee a win or a draw.

| Item | Interpretation |
| --- | --- |
| R1 | Use (O1)–(O4) as transcribed. Reflection of the ranks reverses pawn direction and maps the two starting ranks and promotion ranks to their counterparts. Swapping colours sends the White shuttle to the Black shuttle and the Black freeze to the White freeze. Attack relations and king distances are preserved, including across the cylinder seam. Thus K1 excludes White pawn attacks on either shuttle square and Black pawn attacks on the stationary White king. K2 separates that king from both shuttle squares. The side receiving the e.p. right after a freezing double step becomes Black. These are precisely the stated mirror conditions. |
| R2 | There are two root placements. Each starts with either player to move and no e.p. right. |
| R3 | A losing move gives the opponent a finite forced win **in P alone**. That win can take several moves. Stalemate in P is a draw. |
| R4 | The assertion about q is contextual equality of results with the optionless game. On Black's turn use the freeze flag, if any. On White's turn use no flag. Treating q as literally optionless would contradict (O3) and (O4), as illustrated in §6(d). |
| R5 | A checked player must answer on the board. This excludes even a winning terminal elsewhere. |
| R6 | A board e.p. right belongs only to the player about to move. Any outside move by its holder clears it. |
| R7 | The test in (B1) is the sum with one optional Black move to an empty component. Black must obey the check restriction to use it. Replacing this test by the empty component fails in the abstract example of §6(a). |
| R8 | T is an arbitrary finite D-game, with any start, loops, empty option sets and terminals of either colour available to either player. |
| R9 | The board can be flat or cylindrical, of any size allowed by the brief, with only the group's kings and pawns. No solver bounds enter the proof. |
| R10 | Both versions of each q are independent admissible starts. The proof also covers the same placement after the flag has expired. |

**PROVED.** An outside move changes the global turn. When such moves leave the group untouched, its piece placement stays fixed and any old flag expires. A winning promotion ends play immediately, including a promoting double step on a short board. A freeze is any root move that does not lose in P alone, so (O3) and (O4) apply to every choice of freeze. No choice of a preferred freeze is part of the hypotheses.

## 2. Proposition 4.14

**PROVED.** Give White a strategy in t guaranteeing a win or a nonloss, for the specified starter. Follow it in T. If Black first uses the self-loop at ω, answer immediately with ω → 0. These two moves leave exactly the old t with Black again on turn. Resume the strategy. There can be only one such pair. If Black was already out of moves in T, Black now loses.

Deleting the pair from any continuing play recovers play in T, with the same mover at every T move and the same result at any terminal. Infinite play projects to infinite play. A winning strategy therefore still forces a finite win, and a nonlosing strategy still excludes a loss. For r(t,s) = L the inequality is automatic. Since 0 has no moves, this proves the assertion for all three values and both starters.

## 3. Lemma 4.15

**PROVED.** We transfer two kinds of strategy, one guaranteeing a win and one guaranteeing a nonloss. The finite-game result convention in the brief gives each side a nonlosing strategy at a draw. Thus it suffices to transfer White's win at W, Black's win at L, and both nonlosses at D from the model to the board. In particular we never infer equality of draws just from a one-sided comparison.

### An opponent who leaves q

**PROVED.** The following reply strategy will also be used at a root. Call the player whose guarantee we are transferring A, and the opponent B. Suppose B has just chosen a board move, after which A has a winning strategy in P alone. Suppose also that A has the desired strategy in t **with B to move**. It is now A's actual turn. Make the first move of the board strategy, honoring the actual flag and answering any check. A decisive board win finishes the game. Otherwise, at B's next turn both recorded games have B to move. Thereafter answer each move by B in the game in which B played, using its recorded strategy.

Here is why these replies exist. A move in T reaching a terminal ends the actual play with that terminal's colour. After any other T move the prescribed T reply is legal on the board side of the sum. B could start the outside move only from an unchecked position, and the preceding legal board move left A's own king safe. No piece moved during B's outside move, so A is free to answer outside. A board move by B is answered using the winning P strategy, which includes any required check evasion. At a B-turn between replies, outside play may erase a B e.p. right still recorded in the board strategy. This can only remove a possible B board move. Every real B board move is legal in the record, and after that move the new flag agrees exactly. In particular A can use any e.p. capture prescribed in the reply.

If B has no moves in one record, the other may still be played. A does not declare a win just because one record has run out of B moves. If B has no actual move, B loses. A checkmate delivered by the board strategy prevents all outside moves. A P winning strategy cannot end in a P stalemate. Any infinite real play has infinitely many moves in at least one record. The winning board strategy excludes an infinite board play. The outside strategy excludes an infinite T play when a win is required, and allows a draw when only a nonloss is required. These facts prove the claimed guarantee, including against a player who switches components arbitrarily often.

**PROVED.** Both kings are safe at q. After a legal freeze White's king is safe, and (O4) requires the same placement to be legal with White to move, so Black's king is also safe. To transfer a strategy from 0 ⊞ t at q, A plays the T strategy until B first plays on the board. On Black's turn any available board move is covered by (O3), including a legal e.p. capture. If the flag has expired, each remaining move has the same successor as it had with the flag present. On White's turn (O4) applies. Hence after B's move the two premises of the reply strategy hold. The T record is still at B's turn because B moved on the board. If B never plays there, the play follows T. This works even if B had no T move and played on the board to postpone a normal-play loss. It proves equality with 0 for each q and either starter.

### Root play and White's non-freezes

**PROVED.** From either root, record a play of ω ⊞ T. While the board is at a root, a Black shuttle represents the self-loop and a White freeze represents ω → 0. Both root placements support these moves, have no flag, and by K1 and K2 have neither king in check. Outside moves are consequently available exactly as in the model. If A's strategy prescribes a shuttle, make the legal shuttle. If it prescribes a freeze, take any freeze. If B freezes, accept B's choice. After a freeze use the q result just proved, with the resulting t, side and flag. A strategy's continuation after that history gives the requisite guarantee from 0 ⊞ t. As long as there is no departure from these moves, finite terminals match and an infinite play also gives an infinite model play.

If White departs by a non-freeze when transferring **Black's** guarantee, (O2) and the definition of freeze give Black a P win in the resulting board position. At the moment before the departure, Black had the desired guarantee in ω ⊞ t **with White to move**. Proposition 4.14 gives Black that same guarantee in t with White to move: if the model result is L then t has result L, and if it is at most D then t has result at most D. Apply the reply strategy with Black as A. There is no corresponding need to test White's non-freezes against a reservoir.

### A Black non-shuttle and the single move in −1

**PROVED.** Now transfer **White's** guarantee. Just before Black departs, save White's strategy in ω ⊞ t, with **Black to move**. Call this the outside record. After the actual non-shuttle move, start a second record from the resulting board position beside −1, with **White to move** and the actual e.p. right. By (B1) White can force a finite win in this second record. Play its first move on the real board. White has no move in −1, so this is a legal board move even if White was checked. Stop on a decisive win. Otherwise both records now await Black.

Maintain this arrangement at the beginning of each succeeding Black turn. The real T position equals the T position in the outside record. The real board equals the board in the second record, except that a recorded Black e.p. right may have expired in the real game. The reservoir is unspent as long as the outside record still has ω. The replies are as follows.

1. **Black moves on the board.** Record the move in the second record. It is legal there, even if the recorded position gave Black an additional e.p. option. Follow the (B1) reply on the board. The outside record does not advance.
2. **Black moves in T.** Record that move in the outside record. A terminal there ends the real game with exactly its indicated result. If White's reply is a move in T, make it. Neither player has changed the board placement and any old real flag is gone.
3. **Black moved in T and White's prescribed reply is ω → 0.** Record that freeze in the outside record. In the second record, charge Black's just-played outside move to the single Black move in −1. It is available because the model has not frozen before. It is legal because the actual outside move shows Black was not in check, and check depends on the common placement. Making the reservoir move clears the recorded Black flag as the actual move did. Now take White's prescribed (B1) board reply in the real sum. The outside record is at 0 ⊞ t with Black to move, and the second record again awaits Black unless the reply ended the game.

In the last case the real White board move serves as the tempo of the model freeze. The model can request this only once. No virtual Black shuttle is needed after the departure. If step 2 calls for an outside reply, White's own king was safe just before Black moved outside and is still safe. If step 1 delivers check, the board reply handles it. A reachable White turn in the winning (B1) record always supplies a board reply unless play has already ended.

A record that ends by Black having no move may be left idle. A real Black board move would also have been a legal move in the board record. If a virtual reservoir move is called for, its legality was just shown in step 3. Likewise every real Black T move is available in the outside record. Thus a record that ran out of moves is never asked for a reply to an unavailable Black move. A real Black player unable to move loses, irrespective of either record's remaining options. Every real Black move advances at least one record. An infinite play would have an infinite projection in one of them. The (B1) record forces a finite win, so only the outside record can have an infinite projection, and only if White's guarantee allows a draw. This proves that White retains her guarantee.

**PROVED.** At the roots the only departures by an opponent were the two just handled. At q either opponent's departure was handled directly. The win and nonloss transfers therefore give equality of the full results at the four root starts and both starts of every q, for every finite T. Neither stated theorem requires repair.

## 4. Where the chess and D-game rules enter

- **PROVED — Checks.** K1 and K2 allow outside moves at the roots, and legality of both turns does the same at q. In both reply strategies the board responder follows a legal board strategy, including forced evasions. An outside exchange begins on a Black or White opponent turn on which moving elsewhere was legal and leaves the responder's king safe. This also certifies the legality of charging the −1 move. Checkmate prevents even a terminal move elsewhere.
- **PROVED — En passant.** Roots and shuttles have no flag. (O3) uses the flag after a freezing double step, (O4) uses none, and (B1) starts from the full successor of the Black departure. A departure by White is also evaluated with its actual successor flag. A responder gets the fresh flag immediately after an on-board double step. During outside exchanges only an option of the waiting opponent can expire in a saved board position. Charging −1 clears exactly that opponent's flag.
- **PROVED — Stalemate and losing moves.** The solo certificates concern forced wins under P, where reaching stalemate would draw. No non-promoting losing move is replaced by a terminal. In the real sum and in the (B1) test one checks for no moves across all legal components. One record with no opponent move may be idle while another continues.
- **PROVED — Promotions and T terminals.** Any promotion ends the whole sum for its mover. Exactness excludes a promoting freeze, and a winning promotion cannot count as a losing departure. A T terminal ends the actual and recorded plays together. Its colour specifies the result even when the mover commits suicide.
- **PROVED — Loops and draws.** The proof permits infinite root shuttling and allows loops in T. The neutralizing pair in Proposition 4.14 occurs at most once. After a departure an infinite actual play requires an infinite recorded play. Winning strategies exclude that possibility in their own record. Transferring a nonloss for each side gives equality at D.

## 5. The weakest step

**PROVED.** The step most vulnerable to an incorrect turn or flag is step 3 after a Black departure. The outside record still having ω certifies that −1 is unspent. The actual T move certifies that the recorded Black king was safe even if the flags differ. The reservoir move now puts **White** on turn on the recorded board with the old Black flag cleared, exactly the conditions for the real reply. A solo win from the departure supplies none of this extra tempo.

## 6. Are the hypotheses right?

### (a) Dropping (B1)

**PROVED in an abstract model.** Use the following complete group graph. Each cell lists all moves of its player. All positions are unchecked, there are no flags, and ⊕ and ⊖ represent promotions. The root pair models a legal shuttle with no attack on either king. This is a move-graph model. It omits square placements, pawn directions, and the constraints that actual piece geometry places on simultaneous move lists. No claim of a flat or cylindrical chess realization is made.

| Placement | White options | Black options |
| --- | --- | --- |
| r₀ | q | r₁, x |
| r₁ | q | r₀, x |
| q | x | p |
| x | q | ⊖ |
| p | ⊕ | ⊖ |

**PROVED.** At q, White must go to x and Black promotes. Black must go to p and White promotes. Thus (O3) and (O4) hold, with legal moves on both turns. The sole White root move freezes to q and wins in P, giving (O2). Each Black non-shuttle goes to x with White to move. White plays to q, Black goes to p, and White promotes. This proves (O1). In x ⊞ (−1) White must still go to q, where Black instead spends the reservoir move. White must go to x, and Black promotes. Thus (B1) fails. No branch of these solo certificates relies on stalemate.

**PROVED.** Take the ordinary star as T. Its positions are t and e, with L(t) = R(t) = {e} and L(e) = R(e) = ∅. Start with Black. In ω ⊞ t, if Black takes the star, White freezes and Black is stuck. If Black passes at ω, White takes the star. Black must now pass at ω, White freezes, and Black is stuck. The result is W.

At either real root beside the same t, Black moves to x. If White takes the star, Black promotes at x. If White plays x → q, Black takes the star, White must play q → x, and Black promotes. The result is L. This is a strict reversal using a single outside move available to either player. It witnesses the need for an extra hypothesis in the abstract implication from (O1)–(O4). Whether chess geometry alone forces (B1), or precludes every such failure of contextual equivalence, is left open by this example.

### (b) White non-freezes and (c) moves at q

**PROVED.** (b) No additional White-side condition is needed. The saved Black guarantee in ω ⊞ t descends to t by Proposition 4.14, with White still on turn there. The P winning reply to the non-freeze then suffices. (c) No reservoir test at q is needed for either player. Its model coordinate has no moves to simulate. After a departure the P winning responder can answer in the board or T according to where the opponent played. The expired-flag case only removes an opponent option.

### (d) Dependence on readings and repairs of altered statements

**PROVED.** R7 matters if the test is weakened to a win beside 0. The example in (a) passes that weaker test by a forced promotion, yet reverses W to L. Restoring the single optional Black tempo suffices by §3. R4 matters if “is 0” is taken to assert identity of move graphs. For a nonvacuous abstract example delete the x option from both **Black root** rows of the table, retaining x everywhere else. Exactness still holds and (B1) is vacuous. Both players have a move at q and neither has one at 0. Contextual equality, proved in §3, is the valid replacement for literal identity.

**PROVED.** Several other changes of reading leave the result comparison intact. Restricting the board family, restricting T (for instance, forbidding suicides), or requiring the q assertion only after an actual freeze gives special cases. An unflagged Black start at q is already covered. Requiring an immediate winning promotion or mate as the reply to a losing move would strengthen the solo certificate. Reading a certificate instead as a forced win on the board with an empty outside component under sum rules also suffices: use that winning record in the reply strategy, leaving it idle if Black or White as opponent has no board move. The proof as stated respects the literal check and flag rules in R5 and R6 throughout. It does not require that every possible change to those rules give a different outcome.

### Reproducing the finite example

**COMPUTED-1.** The optional independent-of-the-repository calculation below checks the table in (a) under sum rules. Outcomes in each pair are ordered White starter, then Black starter. The solo certificates above end by promotion under P. The assertions of the two theorems are proved by strategies, independently of the calculation.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python kings/delegate/out/K58/check.py
```

| Group | Outside | Result pair |
| --- | --- | --- |
| q | empty | LW |
| x | empty | WL |
| x | −1 | LL |
| r₀ | star | WL |
| r₁ | star | WL |
| q | star | WL |
| ω | star | WW |
| 0 | star | WL |
