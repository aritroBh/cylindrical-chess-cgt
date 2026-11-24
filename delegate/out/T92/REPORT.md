# T92 referee report

## Summary

**PROVED** — A.18 grants the blocker the pass it needs. One sentence comparing complete plays needs a correction.  
**PROVED** — All three cases of A.18a use legal strategies. Acyclicity gives both printed move bounds.  
**PROVED** — A.18b gives the S2 spare-move result with an optional pass that preserves the entire context.  
**PROVED** — A.19 gives the frozen-king win. Step 4 needs an explicit endpoint and H3 an absolute rank difference. Step 5 is sound.  
**PROVED** — A.19 with A.19a implies the exact S2 sentence below. **CHECKED-2** — The mobile-king example in A.19b is a draw.

## Verdicts

| Item | Verdict | Reason |
|---|---|---|
| A.18 | Sound with wording fixes | The invariant proves (a), (b) and their colour reversals. A forcing-test play can stop earlier than a play in the augmented sum. |
| A.18a | Sound as printed | In (a) both blockers can wait. In (b) only White blocks, and in (c) only Black blocks. |
| A.18b | Sound as printed | An opponent can choose any legal context move or a pass. A suicide ends the game immediately. |
| A.19 | Sound with wording fixes | The projection through an enemy promoting move suffices. A terminal king move must be excluded. |
| A.19a | Sound as printed | A.2(a,c) and the pre-event argument of A.11 justify applying A.19 at the legal successor for either beneficiary. |
| A.19b | Sound as printed | The test is per credited side and per event. Its scope and the mobile-king example are correct. |

## T91 disposition

**PROVED** for the mathematical assessments. Quotations below render TeX as mathematics and join source lines. Line numbers refer to `dist/tog/supp_src/s12b_extra.tex` unless indicated.

| T91 | Revised text | Assessment |
|---|---|---|
| 1 | 65–70. “If Black can wait in Z, this is a strategy in G ⊞ Z itself.” | Resolved. Black receives a pass in the auxiliary game, White in the colour reversal. The new proof sentence at 91–93 needs the separate correction below. |
| 2 | 20–21. “G is short if the directed graph on its positions, with an edge from x to every position in L(x) ∪ R(x), is acyclic; a move from x to x is a cycle.” | Resolved. The recursion at 46–52 uses the correct order. The sum paragraph reverses its direction in words. |
| 3 | 57–59. “By Lemma A.18, λₛ(x) says that White forces a decisive event against a passing opponent from (x,s), and ϱₛ(x) the same for Black; this is the condition for winning when the opponent can wait (Theorem A.18a), but not in general.” | Resolved. This permits a win by opponent immobility when that opponent cannot wait. |
| 4 | 145. “In (b) Black can win only at a terminal, since White always has a pass, so ‘Black wins’ means ‘Black forces ⊖’; White may also win because Black runs out of moves.” | Resolved. Lines 139–148 give optional passes, immediate suicides, the compulsory-pass counterexample and the chess e.p. caveat. |
| 5 | 232–233. “If q is on f, it stands behind the square of p at y by (H1), and p only advances; so the landing square, the square of q or, e.p., the square behind it, is behind p, and (I) is kept.” | Resolved. The victim is stationary. H4 separately bounds entry onto a neighbouring file, including the lower e.p. landing rank. |
| 6 | 245–246. “Consider a play that follows Π, up to its first king move or promotion, the promoting move included.” | Partly resolved. Equality now concerns squares. The next sentence says “After each move of the play”, so specify which terminal endpoint is included. |
| 7 | Builder 74–78. Full replacement sentence quoted below. | Resolved. The pawn is removed, every enemy sequence counts, and the time budget respects the starter. |
| 8 | 7–9. “Every further definition is given here, and every proof is a hand proof. The one computed statement (in Remark A.19b) is marked as such and is used nowhere.” | Partly resolved, editorial only. The opening identifies both results. The working-note provenance and hand-proof commentary remain. |
| 9 | 42–43. “Then σ forces a decisive event against a passing opponent from (x,s) if σ has a strategy under which every such play reaches the terminal of σ after finitely many moves.” | Resolved. Lines 40–41 specify the two move sets before the strategy quantifier. |
| 10 | 118–120. “If neither λₛ(x) nor ϱₛ(x) holds, neither side wins, which is a draw: each side, by its blocking strategy, avoids defeat against every play of the other, and when both follow these strategies the play never ends.” | Resolved. Both blockers always have a move and prevent complementary terminals. |
| 11 | 182–184. “ω’s king has a neighbouring square t at king distance (the larger of the file distance and the difference of ranks) at least 2 from β’s king such that no pawn of either colour stands on the file of t or on a file at distance 1 from it.” | Partly resolved. Lines 155–157 and 168–174 correctly specify the initial right, fixed kings and absence of a check test in the comparison. H3 should specify the absolute difference. |
| 12 | 165–166. “If play reaches the d-th move of p and p has moved at every turn of β, then ω has made exactly e moves before that move.” | Resolved. Lines 190–193 allow an earlier win. Step 5 eliminates enemy promotion and accounts for every live turn. |
| 13 | 276–278. “For any fixed race rule, the corollary applies the test to the side that W credits at that move; a different rule can change the side to be tested.” | Resolved. Lines 283–285 also require success at every relevant move before inferring frozen-king (V2). |
| 14 | 251–252. “Any e.p. capture by ω uses the right of y at ω’s first move (Step 2), and the same capture, by the same pawn, is allowed in Gω.” | Resolved. Lines 235–237 require the **first turn from y**, with s = ω and victim q ≠ p. Either eligible capturer can use that right. Lines 278–279 agree. |

## Remaining changes

1. **Lines 28–30, direction of the listing (PROVED).** At 23–24 every nonterminal successor comes *earlier*. Replace the clause “moves one coordinate forward in its listing and keeps the others” with **“moves one coordinate to an earlier position in its listing and leaves the others fixed”**. The sum of the coordinate indices then strictly decreases.

2. **Lines 91–93, complete plays versus prefixes (PROVED).** “The plays of the definition of forcing, with White forcing, are plays of this game in which Black uses only moves of G and passes, so Black’s strategy is allowed there, and White does not force a decisive event against a passing opponent.” Take an optionless context, White to move, and give White a pass in Z. The forcing test ends immediately with White unable to move. The empty play is only a prefix in the augmented sum. Replace the quoted sentence with **“Black’s prescribed replies are legal in the forcing test. Every White G-move preserves the blocking conclusion, and if White to move has no G-option the test ends without reaching ⊕. Thus White cannot force ⊕.”** The pass grant and the “if Black can wait” qualification stand.

3. **Lines 182–184, king distance (PROVED).** In the H3 sentence quoted in row 11, replace “the larger of the file distance and the difference of ranks” with **“the maximum of the file distance and the absolute difference of the ranks”**. This makes the distance symmetric. A.I supplies the flat or cyclic file distance.

4. **Lines 245–249, endpoint of Step 4 (PROVED).** Row 6 quotes the endpoint. The next sentence claims agreement “After each move of the play”. A legal king move to t ends F with the king on t, while the comparison king stays at its initial square. Replace both sentences, through “(Step 3)”, with **“Take a prefix following Π that contains no king move or promotion, except that its last move may be an ω-pawn promotion. Delete p and omit β’s pushes. The remaining pawn moves can be played in order in Gω(y;p), with the same squares occupied by the surviving pawns and both kings after each move, counting a promoting pawn on its arrival square.”** Keep the move-by-move justification at 248–253.

5. **Lines 5–9, introduction (editorial).** “They are Theorem 3.4 and Proposition 2.11 with Corollary 2.11a of the working note `kings/theory/LOOPY.md` in the code copy.” Keep the opening sentence at 4–5. Replace the remainder through “used nowhere” with **“The proofs use Parts A.I–A.III. Remark A.19b records a separate computational example.”**

## Proof checks and the S2 sentence

**PROVED — Blocking and bounds (73–96, 113–134).** In A.18(a) every White turn uses a G-option. At most h−1 moves change the context and at most one more reaches a terminal. Thus White has at most h moves, and alternation gives at most 2h+1 plies. In (b) a Black pass or the chosen G-reply preserves failure of λ or wins immediately. A White pass is covered by contraposition of λᵣ ⇒ λₗ. Part (c) exchanges colours. In A.18a(a) both blockers always have a move and exclude opposite terminals. In (b) every nonterminal Black move consumes a context edge, so the same h and 2h+1 bounds hold for **every play**. The finite tree has a winner at every leaf. White’s blocker excludes a Black win when ϱ fails. In (c) the same argument applies with Black blocking.

**PROVED — Frozen kings (199–273).** Steps 0–1 use A.1 to preserve the empty files protecting β’s king and the escape t, even if ω is in check. Steps 2–3 bound each capture by its victim’s rank and exclude a usable right against p after a double step. Every scheduled push is legal. In Step 5 an enemy king move loses immediately. An earlier enemy promotion would project by Step 4 to a sequence of at most e moves, contradicting H5. The mover has a legal move on every live turn, so play otherwise reaches promotion. In A.19a the pre-event context has no passer, H ≥ 5 and the right has legal provenance. A.2(c) therefore excludes promotion on the event move itself, independently of (V2).

**Exact S2 string**, `dist/tog/tools/build_supplement.py` 74–78, with the decoded TeX and embedded line breaks preserved:

~~~tex
For (V2) we give a sufficient test in the frozen-king game \lab{S} (Proposition~A.19 of Section~\ref{S-kingslong}): the side credited
after a context move that makes a passed pawn wins that game if it has an e.p.-aware passed pawn with a clear
path, the king-safety, escape-square and nearby-pawn conditions of Proposition~A.19 hold, and, with this pawn
removed, no sequence of enemy pawn moves promotes within the enemy turns available before its promoting push.
~~~

**PROVED — Yes, in the stated (V2) setting.** A.19a identifies β with the side credited by W at the legal successor. H1 tests its candidate on the whole board using the **e.p.-aware** convention. H2–H4 are the three named conditions. With p removed, “no sequence” is exactly μω > e in the comparison game at 168–174. The enemy gets d turns if it moves first and d−1 otherwise. The cited labels resolve in the supplement sources. No new undefined symbol or stronger theorem conclusion was found.

**Reproduce from the project root.** The first four commands give the proof text, bounds, cited hypotheses and S2 wording. The last two independently reproduce the A.19b mobile-king draw. For the frozen example take t = a5. Black has no pawn and every legal Black move is a losing king move.

~~~sh
nl -ba dist/tog/supp_src/s12b_extra.tex
nl -ba dist/tog/supp_src/s12a_core.tex
rg -n -A4 'we give a sufficient test' dist/tog/tools/build_supplement.py dist/tog/supp/s02.tex
rg -n -F -e 'label{S-kings}' -e 'label{thm:loopy}' -e 'label{S-kingslong}' dist/tog/supp/s{02,12}.tex
nice -n 10 kings/delegate/out/K21/verify/r2/kp_p --board cyl:8x6 --ep on --pmodel --promote QRBN --cap 0 --threads 1 <<'POS'
Ka1 ka6 Pc2 w -
POS
PYTHONPATH=. .venv/bin/python -B kings/delegate/out/K16/scripts/pyp.py cyl:8x6 'Ka1 ka6 Pc2 w -'
~~~
