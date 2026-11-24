# W10: T91 referee findings applied to `dist/tog/supp_src/s12b_extra.tex`

Files changed: `dist/tog/supp_src/s12b_extra.tex` (261 -> 285 lines), one string in
`dist/tog/tools/build_supplement.py` (the new-string argument of the REP call for the S2 (V2) sentence; REP call and
old string untouched). Driver copied to `delegate/out/W10_t91_fixes/test_s12b.tex` (absolute paths, identical to W7's).
Nothing committed or added.

All counterexamples in the report were checked by hand. All 14 findings are right and all were applied, most with my
wording to keep the file's style and keep every claim exact.

## Mathematical findings

### 1. A.18(b),(c) false in the actual sum when the blocker cannot wait - applied, my wording
Check: one position x, L(x) empty, R(x) = {+}, Black to move, only White can wait, no suicides. lambda_L(x) false, so
lambda_R(x) false; Black cannot pass and its only move is +. Old (b) is false. Correct.
Old: "(b) If lambda_s(x) fails, Black has a strategy that uses only moves of G and passes, under which no play reaches
+, whatever White does (...); in particular White does not force ... (c) The same holds with the colours exchanged,
varrho in place of lambda."
New: "(b) Let lambda_s(x) fail, and grant Black a pass at every Black turn (a pass changes only the side to move). Then
Black has a strategy that uses only moves of G and passes, under which no play reaches +, whatever White does (moves of
G, passes, suicides); in particular White does not force a decisive event against a passing opponent from (x,s). If
Black can wait in Z, this is a strategy in G+Z itself. (c) Parts (a) and (b) also hold with the colours exchanged,
varrho in place of lambda; in (b) White is granted the pass, and the strategy is one in G+Z if White can wait."
Proof: "Black passes" -> "Black uses its granted pass"; last sentences now: the forcing-test plays are plays of the
granted game in which Black's strategy is allowed; if Black can wait the granted pass is Z's pass.
Why true: the invariant argument only ever needs a Black pass, now granted; the forcing test grants the opponent a pass
by definition, so the "in particular" is unaffected.

Every use of A.18(b),(c) re-checked:
- A.18a(a), White's statements: Black's blocker; both can wait. Text: "which is a strategy in G+Z since Black can wait".
- A.18a(a), Black's statements: White's blocker from (c). Text: "whose blocking strategy for White is a strategy in G+Z
  since White can wait".
- A.18a(a), draw: both blockers, both legal.
- A.18a(b) (only White waits): uses (c)(a) (Black's forcer, G-moves only) and (c)(b) (White's blocker; White can wait;
  text says so). Black's blocker is not used.
- A.18a(c): mirror of (b); only Black's blocker, and Black can wait there.
- The "iff forces against a passing opponent" clauses use only the "in particular" parts (forcing test, pass granted
  by definition).
- A.18b uses no blocker legality.
So each of the three cases is fully proved by what is printed.

### 2. "short" must be acyclic - applied, referee's substance, my wording
Check: one position, R(x) = {x}, L(x) empty, only White can wait: Black loops, White passes, infinite play; contradicts
A.18a(b) if a self-loop is allowed. Correct.
Old: "G is short if no sequence of moves between positions, made by either side in any order, returns to a position it
has left. Then such a sequence visits distinct positions, so it has fewer than h moves, ...; and the positions can be
listed so that every option of a position comes before it."
New: "G is short if the directed graph on its positions, with an edge from x to every position in L(x) cup R(x), is
acyclic; a move from x to x is a cycle. Then a sequence of moves between positions, made by either side in any order,
visits distinct positions, so it has at most h-1 moves, ...; and the positions can be listed so that every option of a
position that is itself a position comes before it."
Dependent sentences adjusted: Predicates ("an order that lists every option that is a position before the position it
is an option of"); Sums ("a move between tuples moves one coordinate forward in its listing and keeps the others");
A.18(a) proof "fewer than h" -> "at most h-1"; A.18a(b) proof: "every Black move is a move of G between positions, or a
move to a terminal (in G or a suicide), which ends play. The moves of G between positions in a play, by either side,
are at most h-1, since passes leave the position of G unchanged and G is short. So Black makes at most h moves ...".
Why true: an acyclic graph on h vertices has no path with more than h-1 edges; passes do not move G's coordinate.
Matches the note's Definition 1.1.

### 3. Predicates are forcing predicates - applied, my wording
Check: x with no options, only White can wait: White wins with either side to move, lambda_s(x) false. Correct.
Old: "The subscript names the side to move: lambda will mean that White wins, varrho that Black wins."
New: "The subscript names the side to move (L for White, R for Black). By Lemma A.18, lambda_s(x) says that White forces
a decisive event against a passing opponent from (x,s), and varrho_s(x) the same for Black; this is the condition for
winning when the opponent can wait (Theorem A.18a), but not in general."
Why true: A.18(a),(b) give the forcing equivalence; A.18a gives the win when the opponent can wait (lambda in cases
(a),(c); varrho in (a),(b)); the example shows the rest.

### 4. A.18b and the S2 wording - applied, my wording (insertion, not full replacement)
Check: L(x) = {+}, R(x) = {-}, White to move: Black reaches - against an always-passing White, but varrho_L(x) fails
and White wins by +. Correct; refutes the compulsory-pass reading.
Old: "... are the D-game Z, whose suicides never enter a strategy above."
New: "... are the D-game Z: a side that can wait may pass at any of its turns, and every other move of Z is a suicide,
an immediate win for the opponent. The forcing and blocking strategies above never prescribe a suicide, and each of them
covers an opponent who plays one. ``Against a passing opponent'' means against an opponent who chooses at each turn
between a move of G and a pass, not one who must pass: if G has one position x with L(x)={+} and R(x)={-}, and White is
to move, Black reaches - against a White that always passes, yet varrho_L(x) fails and White wins by moving to +."
Rest of A.18b (Black wins only at a terminal in (b); chess caveat) retained. Why not the full replacement: the old text
matched each S2 phrase to G and Z correctly; the insert adds exactly the referee's new content.

### 5. Capture onto the passer's file - applied, my wording
Check: cyl 8x8, White Kh1 Pc6 Pc3, Black Kh8 Pb4, Black to move: H1 (b4 at rho 4 < 6; c7, c8 empty), H2 (g, a free),
H3 (t = h7), H4 (no White pawn on b, d), H5 (d = e = 2, mu = 3) hold, and b4xc3 lands on f behind c6. Correct.
Old: "If q is on f, it stands behind p, since by (H1) no pawn stands on f ahead of p at y and none has entered since;
the landing square is behind p, and (I) is kept."
New: "If q is on f, it stands behind the square of p at y by (H1), and p only advances; so the landing square, the
square of q or, e.p., the square behind it, is behind p, and (I) is kept."
Parenthesis: "at that pawn's rank" -> "at the rank of the captured pawn, or one rank lower after an e.p. capture".
Why true: q never moves under Pi; H1 puts every pawn on f behind p at y; e.p. lands on the square q skipped.

### 6. Step 4 equality of positions - applied, my wording
Check: after a double step of p the real game has an (unusable) right and a side to move, G_omega neither. Correct.
Old: "Let a play follow Pi. After any number of moves, the position without p is the position that G_omega(y;p)
reaches by the same pawn moves of omega: beta's other pawns and both kings have not moved, and p was never captured
(Step 3)."
New: "Consider a play that follows Pi, up to its first king move or promotion, the promoting move included. After each
move of the play, the pieces other than p stand on the same squares as after the same pawn moves of omega, in the same
order, in G_omega(y;p): the kings and beta's other pawns have not moved, the same pawns of beta have been captured in
both, and p was never captured (Step 3). We compare the moves in order." Square/e.p. argument kept (see 14).
Why true: only placement is needed to show each omega pawn move is a G_omega move; G_omega has no check test (11).

### 7. S2 sentence - applied in build_supplement.py along the referee's wording
Referee's side example (cyl 8x6, White Ka1 Pc4, Black Kd5 Pg3, Black to move) checked: c4 checks d5; H1-H4 hold
(t = e5); with c4 removed g3-g2-g1 takes 2 = e moves, so H5 fails though Black's only legal moves are losing king
moves. Shows H5 is a test on G_omega; no text change needed for it.
Old new-string: "For (V2) we prove a local test only with frozen kings \lab{S} (Proposition~A.19 of
Section~\ref{S-kingslong}): a passed pawn then wins the frozen-king game if, besides conditions on checks, stalemates
and its own nearby pawns, its path is empty and no enemy pawn, passed or not, can promote first."
New new-string (one sentence): "For (V2) we give a sufficient test in the frozen-king game \lab{S} (Proposition~A.19 of
Section~\ref{S-kingslong}): the side credited after a context move that makes a passed pawn wins that game if it has
an e.p.-aware passed pawn with a clear path, the king-safety, escape-square and nearby-pawn conditions of
Proposition~A.19 hold, and, with this pawn removed, no sequence of enemy pawn moves promotes within the enemy turns
available before its promoting push."
Why true: A.19a with A.19: H1 = e.p.-aware passed + clear path, H2 king safety, H3 escape square, H4 nearby pawns, last
clause = H5 (mu_omega >= e+1, e = enemy turns before the d-th push). No necessity, no "only". File parses (ast).
Supplement not rebuilt, so supp/s02.tex still shows the old sentence.

## Wording findings

### 8. Lead-in - applied, my wording
New: "This subsection proves two statements of Section S-kings: Theorem thm:loopy on outcomes with spare moves (Theorem
A.18a), and the frozen-king test for (V2) (Proposition A.19 and Corollary A.19a). They are Theorem 3.4 and Proposition
2.11 with Corollary 2.11a of the working note kings/theory/LOOPY.md in the code copy. We use the notation of Parts
A.I--A.III and cite items A.1--A.17 of the previous subsection. Every further definition is given here, and every proof
is a hand proof. The one computed statement (in Remark A.19b) is marked as such and is used nowhere."
Dropped: "whose proofs are not in the previous subsection", "where further results and the computer checks are
recorded". Kept the provenance clause and "hand proof".

### 9. Forcing definition - applied, my wording
New: "To test forcing from (x,s), let the opponent sigma-bar choose at each of its turns any move of G or a pass
(whether or not sigma-bar can wait in Z), and let sigma choose only moves of G. Then sigma forces a decisive event
against a passing opponent from (x,s) if sigma has a strategy under which every such play reaches the terminal of sigma
after finitely many moves. Since the opponent always has a pass, sigma cannot win such a play by leaving it without a
move." Same meaning, quantifiers in order.

### 10. Draw case - applied, my wording
Old: "If neither ... holds, neither side wins, which is a draw." New adds: ": each side, by its blocking strategy,
avoids defeat against every play of the other, and when both follow these strategies the play never ends."
Why true: each blocker avoids the other's terminal and always has a move (both can wait).

### 11. State, G_omega rules, king distance - applied
- "with side s to move and its right" -> "with side s to move and with the e.p. right, if any, created by the double
  step that led to y (Part A.I)".
- G_omega: now "by the pawn rules of Part A.I, with the kings as obstacles and with no test of check, and may capture
  e.p. only as the first move, only if s=omega, and only with the right of y (by (H1) that right allows no capture of
  p)". The parenthesis is mine: a right against p has no omega pawn beside p by H1, so deleting p loses nothing.
- H3: "king distance" -> "king distance (the larger of the file distance and the difference of ranks)"; not defined in
  s12a_core.tex (only file distance, line 17).

### 12. Stopping time - applied, my wording
- Setting: "If p moves at every turn of beta, then omega makes exactly e moves before the d-th move of p." -> "If play
  reaches the d-th move of p and p has moved at every turn of beta, then omega has made exactly e moves before that
  move."
- A.19 last sentence: "Every move of Pi is legal, and beta wins no later than the d-th move of p, which promotes." ->
  "Every move of Pi is legal when it is due, and every play in which beta follows Pi ends with a win for beta, at the
  latest with the d-th move of p, which promotes."
- Step 5 now: "Let a play follow Pi. Before the d-th move of p, omega has at most e turns. If omega makes a king move at
  one of them, beta wins at once. Otherwise its moves there are pawn moves, and by Step 4 and (H5) none of them
  promotes, since e < mu_omega(y;p). By Step 1, omega always has a legal move, the king move to t, so it is neither
  stalemated nor checkmated, and beta is never in check; by Step 3, beta always has the move of Pi. So a play that has
  not ended with a king move of omega reaches the d-th move of p, which is legal by Step 3 and promotes, and beta wins."

### 13. Scope of A.19b - applied
- "It is independent of the race rule: whoever W credits, the corollary asks for a pawn of that side that passes
  (H1)--(H5)." -> "For any fixed race rule, the corollary applies the test to the side that W credits at that move; a
  different rule can change the side to be tested."
- "So Corollary A.19a supplies (V2) ..." -> "Thus, when the test passes at every move that Corollary A.19a quantifies
  over, the corollary supplies (V2) for Theorem A.11 in the form of Remark A.12(b) with F, and not for P or chess."
  (Referee's "checking A.19a at every relevant move" omitted that the check must succeed.) The referee's aside about
  (V3)/Z-pawn moves was not added: not about A.19.

### 14. One right, two captures - applied, my wording
Check: cyl 8x8, White Kh1 Pc6 Pe4, Black Kh8 Pd4 Pf4, Black to move after e2-e4: H1-H5 hold for c6 (d = e = 2,
mu = 3, t = h7), and both d4xe3 and f4xe3 e.p. are legal. Correct.
- Step 2: "so the only such capture is the one offered at y when s=omega, of a pawn q != p, covered above" -> "so any
  such capture is made at the first turn from y, with s=omega, using the right of y against a pawn q != p; it is covered
  above."
- Step 4: "The only e.p. capture of omega is the one offered at y, as its first move (Step 2), which G_omega allows." ->
  "Any e.p. capture by omega uses the right of y at omega's first move (Step 2), and the same capture, by the same pawn,
  is allowed in G_omega."
- A.19b: "the e.p. capture offered at the start" -> "any e.p. capture available at the first move".

## Statement changes
- Definition of short: acyclic, self-loop excluded explicitly (finding 2); removes only the ambiguous self-loop case,
  where the old statements were false.
- Lemma A.18(b),(c): now in the game with the blocker granted a pass, plus "a strategy in G+Z if the blocker can wait"
  (finding 1). Weaker than the old (false) statement; the "in particular" no-forcing claim is unchanged.
- Lemma A.18(a); Theorem A.18a(a),(b),(c); Corollary A.19a: unchanged.
- Proposition A.19: hypotheses unchanged except king distance now defined; conclusion reworded, same strength.
- Forcing and G_omega definitions: same meaning, reworded (G_omega says "no test of check" explicitly).

## Test compile
`nice -n 15 tectonic -X compile --only-cached --outdir delegate/out/W10_t91_fixes/build
delegate/out/W10_t91_fixes/test_s12b.tex`: no errors, no undefined references. Only warnings: hyperref "Suppressing
link with empty target" for the driver's stub labels (S-kings, thm:loopy), as in W7. **5 pages**; page 5 holds only
the last two lines of A.19b (W7 had 4). Trimming about three lines would restore 4.

## Unsure
- Page count 4 -> 5 (two-line spill).
- S2 sentence says "the side credited after a context move that makes a passed pawn"; "the credited side" is a shorter
  alternative if S2 should not mention context moves there.
- Some source lines exceed 120 characters (no effect on output).
- Supplement not rebuilt: supp/s02.tex and supplement.pdf still carry the old S2 sentence.
