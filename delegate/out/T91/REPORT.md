# T91 referee report

## Summary

**PROVED** — A.18(b) can prescribe an illegal Black pass. Its blocking conclusion holds in the game that grants the blocker a pass.  
**PROVED** — A.18a uses the blocker only when that pass is available. Its winners, draws and one-sided move bound are correct for an acyclic context.  
**PROVED** — A.18b gives the S2 outcome statement when a “passing opponent” may also play any legal context move and a pass preserves the entire context.  
**PROVED** — A.19 and A.19a give a sufficient frozen-king test on both boards. The timing test searches enemy pawn sequences on the board with the candidate removed.  
**CHECKED-2** — With White Ka1, Pc2 against Black Ka6 on the eight-file, six-rank cylinder, White to move, two independent promotion-game solvers give a draw with mobile kings.

## Verdicts

| Item | Verdict | Reason |
|---|---|---|
| A.18 | **Mathematical error** | Part (b), read as a strategy in the stated sum, is false. The symmetric claim in (c) needs the same qualification. Part (a) is sound. |
| A.18a | **Sound with wording fixes** | The note's acyclicity definition should be restored. With it, the strategies prove all three cases, including non-loss against arbitrary play in the draw case. |
| A.18b | **Sound with wording fixes** | Correct for optional passes and immediate terminal losses in the model. Forcing against an opponent obliged to pass is a different test. |
| A.19 | **Sound with wording fixes** | All five hypotheses suffice. Step 4 needs agreement of piece placement on pawn-move prefixes. Its unrestricted equality of positions is too strong. |
| A.19a | **Sound as printed** | With “context move” understood as a legal move at the chess position, A.III supplies the prerequisites for A.2(c). Both possible beneficiaries are covered. |
| A.19b | **Sound with wording fixes** | Certification works with each race rule, although the beneficiary can change. The free-king draw was reproducible. |

The mathematical verdicts and counterexamples below are **PROVED** by the arguments given unless a computational label is attached. Line numbers and quotations refer to `dist/tog/supp_src/s12b_extra.tex` unless another file is named. Quotes are rendered as mathematics, with source line breaks joined.

## Mathematical findings and exact replacements

1. **Lines 56–62, 76–86, A.18(b,c) — false in the actual sum when the blocker cannot wait.** “If λₛ(x) fails, Black has a strategy that uses only moves of G and passes, under which no play reaches ⊕, whatever White does.” Take one context position, L(x) empty, R(x) = {⊕}, Black to move. Give only White a pass and give neither side a Z-suicide. Both White predicates are false, but Black's only legal move immediately reaches ⊕. The auxiliary opponent at lines 38–41 could pass here. The proof silently uses that privilege. This counterexample still gives the winner predicted by A.18a(b).

   **Replace (b) and (c) with:** “(b) If λₛ(x) fails, grant Black a pass on every Black turn. Black then has a strategy using G-moves and passes that avoids ⊕ against all White G-moves, passes and suicides. Consequently White cannot force a decisive event against an opponent allowed to pass. The blocking strategy is legal in the original sum whenever Black can wait there. (c) Parts (a) and (b) also hold with the colours exchanged and ϱ in place of λ.” In the proof replace “If λL(y) fails, Black passes” with “If λL(y) fails, Black uses its granted pass.”

2. **Lines 20–23, 43–44 — the definition of short must exclude a self-loop.** “Returns to a position it has left” permits the reading that one must first visit a *different* position. Give Black a self-loop in a one-position G, White no G-move, and only White a pass in Z. Repeated Black loops and White passes give infinite play, contradicting A.18a(b) under that reading. The recursion would also depend on itself. Definition 1.1 of the note explicitly says “acyclic.”

   **Replace lines 20–23 from “G is short” with:** “G is short if the directed graph on its positions, using the nonterminal options of both sides as edges, is acyclic. Thus a path of position-to-position moves has at most h−1 edges, where h is the number of positions, and the positions admit an ordering in which every nonterminal successor precedes its source.” At line 43 replace “every option” with “every nonterminal successor.”

3. **Lines 52–54 — the predicates are forcing predicates, not general winner predicates.** “λ will mean that White wins, ϱ that Black wins.” Take G with no options at x. If only White can wait, White wins with either starter and λ is false with either starter. That win can come from Black running out of moves.

   **Replace the sentence with:** “The subscript names the side to move (L for White, R for Black). The predicates λ and ϱ characterize the ability of White and Black, respectively, to force their own terminal against an opponent allowed to pass (Lemma A.18).”

4. **Lines 124–131 — answer to the first S2 implication.** “Let a side that can wait pass at any time” and “let every other move in Z lose” give the claimed result **yes**, with the definitions at lines 25–41. A player can choose a pass on *any of its own live turns*, including when it has no G-move. A pass is always optional. A Z-suicide may be played by the adversary and is an immediate terminal win for the other player. Deleting this option changes an otherwise forced suicide into a no-move loss for the same player. A move lost in isolated Z would need a separate argument to treat it as lost with the context present. Even a known losing continuation in chess cannot be assigned the abstract move bound without counting that continuation.

   The qualification “against a passing white” matters. In the one-position game L(x) = {⊕}, R(x) = {⊖}, with White to start, Black reaches ⊖ against an always-passing White. White actually wins immediately by playing ⊕. This refutes the compulsory-pass reading for both pass regimes. The pure pass leaves every coordinate of G unchanged, including any stored e.p. flag or history governing future moves. A chess shuttle expiring a usable right requires a separate correspondence of available moves and outcomes. The caveat at lines 129–131 is warranted.

   **Replace lines 124–129 through “The theorem is about the D-game.” with:** “Apply Theorem A.18a(b) when only White can wait and A.18a(a) when both can wait. Here the components form the short decisive-terminal sum G. A waiting player may choose a pass on any turn, and every non-pass move in Z gives the opponent an immediate terminal win. Against a passing opponent means against every choice between a legal G-move and a pass. The forcing and blocking strategies never prescribe a Z-suicide, and each covers an adversary who chooses one. With only a White pass, Black must force ⊖ to win, while White can also win when Black runs out of moves.” Retain the chess caveat.

5. **Lines 209–220 — capture onto the passer's file is possible.** “No pawn stands on f ahead of p at y and none has entered since.” If this means entry onto f, it is false. On the eight-file, eight-rank cylinder take White Kh1, Pc6, Pc3 against Black Kh8, Pb4, Black to move, no right. All hypotheses hold (t = h7, d = e = 2, μω = 3). Black can play b4×c3 onto f behind the passer. If “entered” means entry *ahead* of p, that is the inductive hypothesis and the sentence is unnecessary. The direct argument only concerns the stationary victim. An enemy capture onto a neighbouring file is exactly where H4 matters.

   **Replace lines 211–214 from “Second” through “(I) is kept” with:** “Second, each surviving β-pawn q other than p still occupies its initial square. If q is on f, (H1) puts it strictly behind the initial square of p, and p only advances. A capture of q therefore lands behind p, on q's square or, en passant, one rank farther back in the β-coordinate. Thus (I) is preserved.” At lines 218–220 replace “at that pawn's rank” with “at the victim's rank, or one rank lower en passant.”

6. **Lines 225–231 — Step 4 claims more than the timing proof uses.** “After any number of moves, the position without p is the position that Gω(y;p) reaches by the same pawn moves of ω.” Full states need not agree. For example, a double push of p can create an unusable right, while the comparison game has made no move. The side to move is also omitted in the enemy-only game. Taken past a terminal king move, even agreement on king squares is false. The required projection is one-way and can include the final enemy promoting move. The note's Step 4 states this as inclusion of moves.

   **Replace lines 225–227 through “(Step 3).” with:** “Consider a prefix following Π before any king move or promotion, allowing its last move to be an ω-pawn promotion. Delete p and omit β's pushes. After each ω-pawn move, the remaining pawns and both kings occupy the same squares as after the corresponding sequence in Gω, up to the instant of promotion. To see that this sequence is allowed, compare its moves in order.” Keep the square and e.p. argument at lines 227–231.

7. **Lines 151–156, 253–257 — answer to the second S2 implication.** “(H5) counts every pawn of ω, passed or not, and every sequence of ω's moves with p removed.” **Yes as a summary of this sufficient test**, if “no enemy pawn … can promote first” refers to that comparison game with the correct move order. A.19a applies the test to a post-adjudication position. “Local” can mean a test *at that position*, but H5 may depend on pawns far outside the strip, on a capture by a formerly non-passed pawn, or on one pawn clearing the route for another. Testing individual unobstructed push distances or just today's passers does not implement H5.

   Absence of an earlier *actual* enemy promotion along Π also suffices in conjunction with H1–H4, directly by Steps 1–3 and the count. It is a weaker assumption than H5 when the comparison uses the pawn rules of A.I. On the eight-file, six-rank cylinder take White Ka1, Pc4 against Black Kd5, Pg3, Black to move, no right. Pc4 checks Kd5. H1–H4 hold (t = e5); Black's only legal replies are losing king moves. With p deleted, g3–g2–g1 promotes in e = d = 2 moves, so H5 fails. This distinguishes a statement about actual play from a prescription for evaluating the test. It is an example for A.19, without the separated context of A.19a.

   **Exact replacement for the proposed S2 sentence:** “For (V2) we give a sufficient test in the frozen-king game. If the credited side has an en-passant-aware passed pawn with a clear path and satisfies the king-safety, escape-square and nearby-pawn conditions of A.19, it wins provided that, with this pawn removed, no sequence of enemy pawn moves can promote within the enemy turns available before its promoting push.” This refers to e consecutive enemy moves in Gω and permits equal move counts when the beneficiary starts. It makes no claim of necessity or of novelty for mobile kings.

## Wording findings and exact replacements

8. **Lines 4–9, introduction.** “In the code copy” and “every proof is a hand proof” read as working-note provenance. **Replace lines 4–9 with:** “Theorem A.18a proves the outcome rule for spare moves in Section S2. Proposition A.19 and Corollary A.19a give the frozen-king test for (V2). The proofs use Parts A.I–A.III. Remark A.19b includes a separate computational example.” A bibliographic citation can carry the historical attribution.

9. **Lines 38–41, forcing.** “Ends with the terminal of σ, after finitely many moves, every play” obscures the quantifiers. **Replace the definition with:** “To test forcing from (x,s), allow the opponent to pass on every turn or to choose any of its G-options. The forcing side may choose only its G-options. It forces its terminal if it has a strategy under which every such play reaches that terminal in finitely many moves.” The no-option rule still applies to the forcing side. This also distinguishes absence of a move from reaching a terminal.

10. **Lines 106–109, draw.** “Neither side wins, which is a draw” meets the formal definition. To make the strategic content explicit, **replace lines 107–109 from “If neither” through “which is a draw” with:** “If both predicates fail, Black's blocking strategy prevents a White win and its colour-reversal prevents a Black win. Each blocker can always move. Hence each side can avoid defeat against all opposition, and when both block, play is infinite and drawn.” Blindly passing need not be safe.

11. **Lines 137–156, state and comparison rules.** “With side s to move and its right” and “ω's pawns step, double step and capture by the pawn rules” leave the input right and treatment of check easy to misread. **Replace “with side s to move and its right” with:** “with s to move and the e.p. right, if any, created by the preceding legal double step.” **Replace lines 153–154 through “right of y” with:** “Use the pawn moves of Part A.I, with both kings as uncapturable obstacles and without a king-safety test. Allow an e.p. capture only on the first move, if s = ω and y offers that capture of a surviving β-pawn.” Deleting p is safe here by H1. For H3, **replace “at king distance at least 2” (line 164) with** “at king distance (the maximum of file distance and absolute rank difference) at least 2”. Part A.I defines file distance for both boards.

12. **Lines 147–149, 171–173, 233–237, stopping time.** “ω makes exactly e moves before the d-th move of p” assumes that move occurs. “If ω is checkmated on the way” is a redundant branch because t is legal on every live ω turn, including one in check. **Replace lines 148–149 from “If p moves” with:** “If play reaches the d-th push and p has moved on every β-turn, ω has made exactly e moves before that push.” **Replace the last sentence of the proposition with:** “At every live β-turn the prescribed push is legal. If the game is still live at the d-th push, that push promotes and wins.” **Replace lines 233–237 with:** “Before the scheduled d-th push, ω has at most e turns. A legal king move by ω ends play with a β-win. Otherwise its moves are pawn moves and none can promote in time, since e < μω by (H5) and Step 4. Step 1 gives ω a legal move on every live turn, and Step 3 gives β its prescribed push. Thus any play still live reaches the d-th push, whose promotion wins immediately.”

13. **Lines 253–261, scope of the remark.** “It is independent of the race rule” can suggest the same move is certified for the same side under every rule. **Replace that sentence with:** “For any fixed race rule, apply the test to the side credited by W at that move. A different rule can change the side to be tested.” **Replace “So Corollary A.19a supplies (V2) for Theorem A.11” with:** “Thus checking A.19a at every relevant move supplies (V2) for Theorem A.11”. Its existing qualifier restricting the conclusion to F should follow. By A.12(b), immediate loss is automatic for a *king* move in F. Z-pawn moves, and hence (V3) as a whole, still require their own verification.

14. **Lines 215–217, 229–230, 255–256, one right can offer two captures.** “The only such capture is the one offered at y” is accurate about *when* the right can be exercised but suggests a unique move. On the eight-file, eight-rank cylinder, White Kh1, Pc6, Pe4 against Black Kh8, Pd4, Pf4, Black to move just after e2–e4, satisfies H1–H5 for c6 (t = h7, e = 2, μω = 3). Both d4×e3 e.p. and f4×e3 e.p. are legal first moves, removing the same pawn. The proof covers both. **Replace “the only such capture is the one offered at y when s = ω, of a pawn q ≠ p, covered above” with:** “any such capture must be made on the first turn from y, with s = ω, using its initial right against a pawn q ≠ p.” **Replace the sentence starting “The only e.p. capture” at line 229 with:** “Any e.p. capture by ω uses the initial right on its first move (Step 2), so the same choice of capturing pawn is available in Gω.” At line 256 replace “the e.p. capture offered at the start” with “any e.p. capture available on the first move.”

## Proof and citation audit

| Proof lines | Assessment of the printed step |
|---|---|
| 65–74 | Sound. The bound uses a G-move on each White turn. |
| 76–84; 86 | Gap in the game specification, false in general in the actual sum. Sound with a blocker allowed to pass. Colour reversal inherits the same qualification. |
| 103–109; 111–119; 121 | Sound in all three cases with acyclic G. Each application of the blocking argument grants the required pass. |
| 179–189 | Steps 0 and 1 sound on live positions. |
| 191–205; 207–220 | Step 2 sound. The induction only needs the stationary victim argument and covers either initial e.p. capturer. |
| 222–223 | Step 3 sound. |
| 225–231 | Step 4's unrestricted position equality is false. The projected pawn-move inclusion and the resulting lower bound are sound. |
| 233–237 | Step 5 sound. The mate-of-ω branch is unreachable under H3. |
| 248–250 | Sound with the inherited A.III hypotheses. |

**PROVED — A.18 through A.18b.** Lines 13–19 give disjoint winning conditions, normal-play loss on no option, and a draw for infinite play. Lines 25–36 give a simultaneous tuple of component states, a move in one coordinate, and immediate termination for either terminal, including a suicide. Acyclic component graphs have an acyclic product of this kind because a position-changing move advances one coordinate in its order. Lines 43–54 then give a well-founded recursion. The same-position dependency is evaluated second. “Every” on an empty option set is true and “some” is false.

At lines 65–74 the forcing player chooses a witnessing G-option. Opponent passes and G-options preserve the indicated predicate or end in the forcing player's terminal. An opponent Z-suicide ends in that terminal too. There are at most h−1 nonterminal G-moves and at most one final move to a terminal. The forcing player consequently makes at most h moves. Alternation permits at most one additional opponent move beyond that player's count, so 2h+1 bounds total plies. A nonpassing opponent can instead run out of moves, whereas an opponent granted a pass cannot. Lines 76–86 preserve the complementary invariant: if the own-turn White predicate is false, a Black pass works; otherwise failure of the universal clause gives a Black G-reply. White passes are covered by the contrapositive of λR ⇒ λL. The sole legality issue is finding 1.

At lines 102–121 both blockers have their passes in (a). In (b) every nonterminal Black move consumes a G-edge, and Black can make at most one additional final move, in G or Z. Hence Black makes at most h moves, every play has at most 2h+1 plies, and finite branching gives a finite game tree with a winner at every leaf. White's blocker is legal and cannot lose to immobility. In (c) interchange the colours. At an empty G with no Z-suicides, if both can pass they draw indefinitely. If only White can pass, Black loses at once when starting, or after one White pass when White starts. “Having the move never hurts” in (a) follows for wins and losses from both predicate implications. No inference here uses ordinary ±BIG component arithmetic.

**PROVED — A.19, hypotheses and Steps 0–3.** Lines 135–169 use the e.p.-aware test of A.I, including an adjacent enemy beside a just-double-stepped pawn; a textbook passer alone is insufficient. H1 checks the full path including the last square and both kings. H2 and H3 refer to files initially free of pawns of *both* colours, which stay pawn-free by **A.1** (core 31–39). En passant lands on the *file* of the removed pawn. At lines 179–189 this proves both that β's king is safe, including after a push, and that t stays free and safe for ω's king. A legal losing move counts in F, so even an ω player whose only escape is a king move cannot claim stalemate. β in turn always has its push. No pass is granted in F.

At lines 191–205, H1 starts both the path and turn-dependent strip invariants. A single push clears any old right. After a double push, every enemy strip pawn is strictly below the arrival rank, so even a newly created right against p is unusable. At lines 207–223 an enemy push stays on its file and lowers its rank. An ordinary capture of p would require an adjacent enemy one rank higher on ω's turn, forbidden by Jω. For other victims, the same-file landing is behind p (finding 5); on a neighbouring file the stationary victim has rank at most ρ₀+1 by H4. The e.p. landing is one rank lower. An enemy pawn entering the strip this way can threaten the route later only if it violates that bound. An enemy double step may offer β a right, but Π always pushes. The only e.p. capture ω can actually make uses y's initial right as its first move, with s = ω and a victim other than p. H1–H4, not an assumption that every passer stays passed, secure the push at each live turn.

**PROVED — A.19, Steps 4–5 and board geometry.** At lines 225–237 each actual enemy pawn move, including a possible promotion, is legal in the pawn-only comparison sequence after deleting p. An initial e.p. reply is retained. All stationary victims and all obstacles other than p are accounted for. A capture creating a faster enemy passer, or vacating a square for a different enemy pawn, therefore contributes to μω. H5 rules out every promoting sequence of length at most e. From ρ ≥ 3 the push count is H−ρ. From ρ = 2 it is one double push plus H−4 singles, hence H−3. The enemy receives d turns if moving first and d−1 otherwise, also when d = 1. There is no queen-specific legality, check, or mate assumption: every legal promotion choice wins immediately in F. Each geometric step uses only existing distance-one neighbours, file occupancy and king distance. On the cylinder the seam supplies a neighbour; on a flat edge the absent neighbour supplies neither captures nor attacks. Thus the flat statement has the same proof and does not rest on the flat-board sweeps.

**PROVED — A.19a,b and references to the core.** A.III (core 225–235, 247–261) assumes H ≥ 5, no initial passed pawn in the *context*, and legal pre-event play. At Q use that initial assumption. At any later Y in R(Q), a passed context pawn would already have ended the pre-event path. A Z-pawn promotion would have required a Z-move; a context promotion would itself have been decisive by **A.2(a)** in the argument of **A.11** (core 282–286). For the event move itself use **A.2(c)** (core 55–67) on the context, with no passer and an absent right or one made by the side not to move. No context pawn can therefore promote on μ. This uses the structural observation in A.11's proof, without assuming (V2) to prove (V2). The post-move pawn is tested on the *whole* board. If the credited player made μ its opponent starts, so e = d; if its opponent made μ the credited player starts, so e = d−1. A.19 then gives the required F-win at that successor. Quantifying over every such event is precisely the F version of (V2) in **A.12(b)** (core 289–295). It establishes one condition of A.11. The named core items are used within their hypotheses; the introduction's “A.1–A.17” describes the numbering, not seventeen dependencies.

**PROVED — comparison with the removed note.** Definitions 1.1–1.3 and 3.1 give precisely the acyclic context, decisive sum and pure self-loop needed here. Theorem 3.4 already marks the outcome result proved. The condensation adds optional immediate suicides (legitimate), a quantitative upper bound (valid), and an auxiliary blocking claim (needs finding 1). It correctly omits the separate chess bridge's assertion that a product pass resets the context's e.p. flag (note 1590–1592). Proposition 2.11 (1306–1400) contains all H1–H5 and expressly states that the flat proof carries over. No protective pawn hypothesis was lost. Corollary 2.11a (1402–1412) spells out the count-rule beneficiary; A.19a allows any W-adjudicated beneficiary. This is a genuine, justified generalization: once β is named the proof never uses the scoring formula. The note also proves a different test for mobile kings under extra assumptions (1503–1516 and Theorem 2.11K); a claim that frozen kings are the *only known* case would be erroneous. Its empirical draw at line 1509 remains marked computational in A.19b. No sweep or conjecture became a premise of either proof.

## Reproduction and limits

Run the following from the project root. To recover the numbered source and the historical statements used for all line references and symbolic bounds:

```sh
nl -ba dist/tog/supp_src/s12b_extra.tex
nl -ba dist/tog/supp_src/s12a_core.tex
nl -ba dist/tog/supp_src/s12_kings.md | sed -n '42,73p;1306,1422p;1503,1558p;1564,1573p;1590,1592p;1636,1678p'
nl -ba dist/tog/supp/s02.tex | sed -n '21,25p;51,63p'
```

**CHECKED-2 — A.19b, P only.** Both commands below evaluate the same mobile-king, first-promotion-wins game, with White to move. The first uses the compiled P solver and the second a separate Python move generator and retrograde solver. Both give a draw. The two bounds printed by the compiled solver are a single implementation's result. **PROVED — F at the same root.** Choose t = a5. H1–H4 hold, Black has no pawn (μω = ∞), and in F its only legal replies are losing king moves.

```sh
nice -n 15 kings/delegate/out/K21/verify/r2/kp_p --board cyl:8x6 --ep on --pmodel --promote QRBN --cap 0 --threads 1 <<'POS'
Ka1 ka6 Pc2 w -
POS
PYTHONPATH=. nice -n 15 .venv/bin/python -B kings/delegate/out/K16/scripts/pyp.py cyl:8x6 'Ka1 ka6 Pc2 w -'
```

**COMPUTED-1 — small regression check for the examples.** The following checks the actual Black move in finding 5, the available Black replies in finding 7, and the move clocks, and both initial e.p. captures in finding 14. The rank bound in each μ calculation follows because the sole enemy pawn starts off its double-step rank and can decrease its rank by at most one per move; an unobstructed promoting line of that length exists. The option sets in findings 1–4 are fully specified and their one-position outcomes can also be reproduced below.

```sh
PYTHONPATH=. nice -n 15 .venv/bin/python -B - <<'PY'
import runpy
rules = runpy.run_path("kings/delegate/out/K16/scripts/pyp.py")
board = rules["Board"]("cyl:8x8")
start = rules["parse"](board, "Kh1 kh8 Pc6 Pc3 pb4 b -")
capture = rules["parse"](board, "Kh1 kh8 Pc6 pc3 w -")
assert ("move", capture) in rules["moves"](board, start)
assert 8 - 6 == 2 and 4 - 1 == 3   # White pushes, enemy minimum
start = rules["parse"](board, "Kh1 kh8 Pc6 Pe4 pd4 pf4 b e3")
for remaining in ("pd4", "pf4"):
    after_ep = rules["parse"](board, f"Kh1 kh8 Pc6 pe3 {remaining} w -")
    assert ("move", after_ep) in rules["moves"](board, start)
board = rules["Board"]("cyl:8x6")
start = rules["parse"](board, "Ka1 kd5 Pc4 pg3 b -")
assert rules["in_check"](board, start, 1)
moves = rules["moves"](board, start)
assert moves and all(child[1] != start[1] for _, child in moves)
assert 6 - 4 == 3 - 1 == 2          # enemy starts and wins a timing tie in the pawn comparison

# Normal play at a single context vertex. A pass hands the same vertex to
# the opponent. A repeated turn is drawn unless a player can force an exit.
def result(options, turn):
    wins = {}
    for _ in range(2):
        for side in ("W", "B"):
            other = "B" if side == "W" else "W"
            successors = [wins.get(other) if m == "pass" else m for m in options[side]]
            if side in successors:
                wins[side] = side
            elif all(w == other for w in successors):
                wins[side] = other
    return wins.get(turn, "D")

assert result({"W": ["pass"], "B": ["W"]}, "B") == "W"  # forced suicide
assert result({"W": ["pass"], "B": []}, "W") == "W"
assert result({"W": ["pass"], "B": ["pass"]}, "W") == "D"
assert result({"W": ["pass"], "B": ["B"]}, "W") == "B"  # White obliged to pass
assert result({"W": ["pass", "W"], "B": ["B"]}, "W") == "W"
PY
```

The proof review used the TeX sources and the named sections of the note. It did not test typesetting or cross-reference resolution in a built supplement, rerun the historical sweeps, audit the solvers generally, or establish a chess outcome for the free-king example. The frozen and mobile-king games were kept distinct. All computational checks were local and serial. The sandbox declined the requested nice adjustment; the small jobs ran at the inherited priority.
