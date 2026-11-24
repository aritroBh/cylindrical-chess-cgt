# K57 proof: the 2 + 3 group of cyl:10×6 has the results of over in every D-sum

AI work (one agent), no human re-derivation, not refereed. PROVED means a complete hand proof below; the facts about
the group that the proof uses are computed, with the labels given in §5.

## 0. Result

- **Proposition 1 (PROVED).** r(0_D ⊞ t, s) ≤ r(ω ⊞ t, s) for White, for every finite D-game T, position t, side s.
  ("over ≥ 0" in D-sums with terminals and loops.)
- **Lemma 2 (PROVED).** An exact over group of Definition 4.8 has the results of over beside every finite D-game T
  (loopy or short, with or without terminals; both roots, both sides to move; each q has the results of T alone)
  provided one extra condition holds on Black's side:
  **(B1)** for every non-shuttle Black move m at a root, the position x_m after it (White to move, with White's e.p.
  right if m is a double step) is a White win beside the integer −1: r(x_m ⊞ (−1), White to move) = W.
  (−1 is the D-game in which Black has one move and White none: White wins although Black may once move elsewhere.)
  Nothing beyond Definition 4.8 is needed on White's side or at the q's.
- **Corollary 3.** The 2 + 3 group H10 = `Kg4 kf6/kg6 Pb3 Pe2 pa5 pb4 pe5` (cyl:10×6) has the results of over beside
  every finite D-game. The hand proof is complete; it uses two computed facts about H10: Definition 4.8 (CHECKED-2, K45)
  and (B1) (CHECKED-2 here: K55's two refereed solvers za and rz, and K57's pr57, agree). So: **PROVED, given CHECKED-2
  computations.** The four exact groups of cyl:8×7 satisfy (B1) by pr57 only (COMPUTED-1), so for them the same
  conclusion is conditional on a COMPUTED-1 fact. Z_O and its flat translates fail (B1) at 1…e5–e4 (and translates),
  as they must (K47: Z_O is not over).
- This replaces K56's condition (T3) on White's side, which H10 fails. K56's one-sided pass game was too pessimistic
  for White's moves, as the brief suspected: Black never needs to "pay" for a bad White move, because Black may give up
  over's passes (Proposition 1) the moment White has made one.

## 1. Setting

As K47, K55, K56. G is the P game of the group's pieces as a component of the D-sum of Definition 1.3 with K40's
convention. A state of G ⊞ T is (g, t, s): a board g of G with its e.p. right, a position t of T, the side s to move.
The mover makes one legal move in G or one option in T. A promotion in G ends the play as a win for the promoter; a
move to the terminal ⊕ (⊖) of T ends it as a White (Black) win, whoever makes it. A side in check in G may not move
in T. A move in T clears the e.p. right in G. A side with no legal move in either component loses. Infinite play is a
draw. r is the least fixed point of Definition 1.2. over_D: positions ω, 0_D; L(ω) = {0_D}, R(ω) = {ω}; 0_D has no
options (Proposition 4.6). T is any finite D-game (Definition 1.1). For a side Y, "Y does at least as well" means the
order L < D < W from Y's side.

KNOWN facts on finite game graphs (least fixed point): (K-a) r = W at a state iff White has a strategy that wins every
play within a bounded number of moves; (K-b) r ≠ L iff White has a strategy against which no play ends in a Black win;
the same with colours exchanged. A strategy that wins (does not lose) from a state only visits states with r = W
(r ≠ L) for its owner.

**Token games.** For colours X ≠ Y and k ∈ {0, 1}: G^X_k is G ⊞ (k tokens of X), i.e. G ⊞ (−k) for X = Black and
G ⊞ k for X = White: X may move elsewhere (spend a token) at most k times, not while in check; spending a token clears
the e.p. right and gives the move to Y; Y has no move elsewhere; a side with no legal move loses; promotions end the
game; infinite play is a draw. Att^X_k is the set of states (board, e.p. right, side to move, tokens left) that Y wins
in G^X_k. With 0 tokens this is G alone under the sum's rule "no move loses"; it contains the P-wins of Y (in P a
stalemate is a draw, here a loss for the stalemated side, which can only help Y when X is stalemated, and when Y is
stalemated Y loses in both). Each state of Att^X_k has an attractor rank; Y has a positional strategy along which the
rank drops at every move of either side.

(P1) If (g, X to move, k tokens) ∈ Att^X_k, k = 1, and X is not in check, then (g, Y to move, no e.p. right, 0 tokens)
∈ Att^X_0 with smaller rank (spending the token is an X option).
(P2) Removing the e.p. right from an X-to-move state removes X options and changes nothing else; if every X option of
the state with the right leads into Y's set, so does every option of the state without it.

**The group.** Black's king shuttles between z0 and z1; roots A, B (Black king on z0, z1), no e.p. right, either side
to move. By Definition 4.8 (over orientation): at each root with Black to move, the shuttle is legal and every other
Black move loses at once in P; at each root with White to move, White has at least one *freeze* (a move that does not
lose at once; no freeze is a promotion) and every other White move loses at once in P; after a freeze, the position q
(Black to move, with Black's e.p. right if the freeze is a double step; also without it; and with White to move) is a
mutual zugzwang: every legal move of the side to move loses at once in P, and each side has a legal move. No king is
in check at the roots or at the q's (Definition 4.8 with K1, K2: the shuttle squares are not attacked by White pawns,
the kings are two apart, and q is legal with either side to move). R = {A, B} ∪ {all q}; φ(A) = φ(B) = ω, φ(q) = 0_D.

## 2. Proposition 1 (over ≥ 0 in D-sums). PROVED

*Claim.* For every finite D-game T, position t and side s: if White has a strategy S0 in 0_D ⊞ T from (0_D, t, s)
that wins (resp. does not lose), White has one in ω ⊞ T from (ω, t, s) that wins (resp. does not lose). Hence
r(0_D ⊞ t, s) ≤ r(ω ⊞ t, s) for White, and if Black wins (does not lose) ω ⊞ t, Black wins (does not lose) 0_D ⊞ t.

*Proof.* White's strategy in ω ⊞ T: while the over-component is ω, at White's turn play S0's move (a move in T: S0 is
a strategy of 0_D ⊞ T, where only T has moves); if Black plays ω → ω, answer ω → 0_D; once the component is 0_D,
follow S0. Deleting from such a play the (at most one) pair "ω → ω, ω → 0_D" and writing 0_D for ω gives a play of
0_D ⊞ T consistent with S0: Black's T-moves are the same; the deleted pair starts and ends at the same position of T
with Black to move. Compare the endings. A terminal of T is reached in both at the same move. White is never without
a move: at White's turn the 0_D-play is at an S0-consistent state with White to move, where a winning or non-losing S0
names a T-move (a stuck White would lose); White's T-options are the same in both games. If Black is to move with no
move: this needs component 0_D (at ω Black can always play ω → ω), and then the 0_D-play also has Black stuck: Black
loses in both. An infinite play stays infinite after deleting two moves. So
every play consistent with White's strategy has, for White, the result of an S0-consistent play or better, and its
length differs by at most 2, so a bounded win stays bounded. ∎

## 3. Lemma 2. PROVED

**Statement.** Let G be an exact over group (Definition 4.8) satisfying (B1). For every finite D-game T, position t,
side s, root x ∈ {A, B} and q: r(x ⊞ t, s) = r(ω ⊞ t, s) and r(q ⊞ t, s) = r(0_D ⊞ t, s).

**Reduction.** It suffices to prove, for each colour Y (X the other colour):
(★) if Y has a strategy S in over_D ⊞ T from (φ(g0), t0, s0) that wins (resp. does not lose), Y has one in G ⊞ T from
(g0, t0, s0) that wins (resp. does not lose).
Then r(over) = W gives r(G) = W (Y = White), r(over) = L gives r(G) = L (Y = Black), and r(over) = D gives non-losing
strategies for both colours in over, hence in G, so r(G) = D.

Y keeps a *virtual* state (o, t, s) of over_D ⊞ T and a strategy S_cur from it that wins (does not lose); at the start
S_cur = S. The real and virtual T-positions and sides to move are equal whenever X is to move, and also at the
moments named below.

### 3.1 Phase 1 (mirror)

Invariant M: real g ∈ R, o = φ(g), same t, same side to move, the virtual state reached by an S_cur-consistent play.
- *Y to move.* S_cur names a move. In T: play it in T (legal: Y is not in check in g ∈ R). ω → 0_D (Y = White, g a root):
  play a freeze; the new g is a q, φ(q) = 0_D. ω → ω (Y = Black, g a root): play the shuttle (legal, captures nothing),
  reaching the other root. At a q, o = 0_D and S_cur names no over-move. M holds again.
- *X to move, X moves in T.* Copy the move in the virtual state (over has no checks, so it is legal there). M holds;
  if it reaches a terminal, both plays end with the same result.
- *X plays the shuttle (X = Black, g a root) or a freeze (X = White, g a root).* Copy ω → ω or ω → 0_D. M holds.
- *X makes any other G-move m.* By Definition 4.8 m loses at once in P (this covers every X move at a q, and every
  non-shuttle, non-freeze move at a root). Go to the entry of phase 2.
- *X has no legal move.* X loses.

### 3.2 Entry into phase 2

Let x be the position after m, Y to move; the virtual state is (o, t, X to move), o = φ(g).

**Case E1: X = White** (Y = Black), m at a root or at a q. Since m loses at once, (x, Black to move) is a Black win in
P, hence in G^W_0; let Black play its winning move r. If r promotes, Black wins. Otherwise the real state is (z, t,
White to move) with (z, White to move, 0 tokens) ∈ Att^W_0. The virtual state before m was (o, t, White to move);
after m and r the real side to move is White again, with the same t.
- If o = 0_D (m at a q): keep the virtual state (0_D, t, White to move) and S_cur.
- If o = ω (m at a root): replace the virtual state by (0_D, t, White to move) and S_cur by a strategy S′ from it that
  wins (does not lose). It exists by Proposition 1: (ω, t, White to move) was S_cur-consistent, so Black wins (does
  not lose) from it, hence also from (0_D, t, White to move).
Set b = 0.

**Case E2: X = Black** (Y = White), m at a q. Then o = 0_D. (x, White to move) is a White win in P, so in Att^B_0.
White answers in G with its winning move (or promotes and wins), to (z, Black to move) ∈ Att^B_0. Virtual state
unchanged ((0_D, t, Black to move)). Set b = 0.

**Case E3: X = Black** (Y = White), m at a root. Then o = ω. By (B1), (x, White to move, 1 token) ∈ Att^B_1. White
answers in G with its Att^B_1 move (or wins at once), to (z, Black to move, 1 token) ∈ Att^B_1. Virtual state
unchanged ((ω, t, Black to move)). Set b = 1.

In every case the real state now has X to move, the same t as the virtual state, and (z, X to move, b tokens) ∈ Att^X_b.

### 3.3 Phase 2 (hybrid)

*b-safe.* A real state (g, X to move) is b-safe if every X G-move from it leads to (g′, Y to move, b tokens) ∈ Att^X_b,
and, if b = 1 and X is not in check, (g, Y to move, no right, 0 tokens) ∈ Att^X_0. Every state of Att^X_b with X to
move is b-safe (definition of the attractor and (P1)); removing the e.p. right keeps b-safety ((P2)).

*Budget.* b = 1 only in Case E3 (Y = White, o = ω); b = 0 otherwise, and then o = 0_D. Y's over-moves that S_cur can
still name: none at 0_D; one (ω → 0_D) for White at ω, after which o = 0_D.

*Invariant H* (whenever X is to move): the virtual state (o, t, X to move) is S_cur-consistent, real and virtual
T-positions are equal, b = 1 iff (Y = White and o = ω), and the real (g, X to move) is b-safe.

*Steps.*
- (a) **X moves in G**, g → g′ (if X is in check, this is X's only kind of move). By b-safety (g′, Y, b) ∈ Att^X_b.
  Y answers in G with its attractor move (or wins by a promotion or mate), to (g″, X, b) ∈ Att^X_b, which is b-safe.
  The virtual state is unchanged. H holds.
- (b) **X moves in T** (so X is not in check). Copy it in the virtual state (legal there). If it is a terminal, both
  plays end alike. Now Y is to move, real G-state (g, Y, no right).
  - If S_cur names a T-move: Y plays it. Y is not in check: the G-board is the one after Y's own last G-move, or after
    the entry, where Y had just moved (E1, E2, E3), or unchanged since phase 1 (g ∈ R). The real state is (g, X, no
    right), b-safe by (P2). H holds. ("Pause".)
  - If S_cur names an over-move: then Y = White, o = ω, b = 1 (Black names none in phase 2: in E1, E2 o = 0_D; in E3
    Y = White). By b-safety and X not in check, (g, W, no right, 0 tokens) ∈ Att^B_0; White plays its attractor move
    there (or wins), to (g′, B, 0) ∈ Att^B_0. Virtually ω → 0_D; now o = 0_D, b = 0, and (g′, B) is 0-safe. H holds.
- (c) **X has no legal move** in G ⊞ T: X loses.

*Y always has a move.* In (a) by the attractor; in (b) because S_cur names one (if S_cur had no move, Y would be
stuck in the virtual play, which S_cur's guarantee excludes).

*Termination of G-moves.* For a b-safe (g, X) let μ be the largest attractor rank among the states its definition
names. Step (a) gives a b-safe (g″, X) ∈ Att^X_b, all of whose successors have rank below rank(g″, X) < rank(g′, Y)
≤ μ. The over-move case of (b) lowers b from 1 to 0. A pause does not raise μ ((P2)). So the pair (b, μ) falls
lexicographically at every G-move of phase 2: phase 2 has finitely many G-moves, and at most one virtual over-move.

*Result.* Every move of the real play is a G-move of phase 1 copied as an over-move or a T-move (also a move of the
virtual play), a G-move of phase 1 that started phase 2, or one of the finitely many G-moves of phase 2. The virtual
play is consistent with S, up to the replacement of S by S′ in Case E1, which happens at most once and keeps the
guarantee (Proposition 1). Hence:
- if the real play is infinite, the virtual play is infinite: a draw in both, allowed when Y only needs "does not lose";
  impossible when S_cur wins (an S_cur-consistent play is finite);
- if the real play ends, it ends by a promotion in G, which can only be Y's (X's G-moves in phase 1 are the shuttle,
  a freeze, or m; in phase 2 they start from b-safe states, whose successors lie in Y's attractor and so are not X
  promotions; m itself loses at once and so is not a promotion), or by a terminal of T, reached also by the virtual
  play, so not X's while S_cur does not lose, or by a side with no move, which is never Y and is a loss for X.
If S wins, the real play is finite, ends in a Y win, and its length is bounded (S's rank, the attractor ranks, one
replacement by S′ with its own rank), which is (K-a). If S does not lose, no real play is a Y loss. This proves (★). ∎

The q-statement: start in phase 1 with g0 = q, o = 0_D. Every X move at q enters phase 2 by E1 or E2.

## 4. Why this is the right strength (the points of the brief)

- **White's side needs nothing beyond Definition 4.8.** K56 let Black keep over's passes after a bad White move and
  then had to pay for each pass with a Black G-move (unlimited budget). Here Black gives the passes up: after White's
  bad move m and Black's P-reply, the virtual over becomes 0_D (Proposition 1: over ≥ 0, so Black loses nothing). Then
  Black never has to move in G unforced. This is idea 1 of the brief in a precise form: a White tempo in t is always
  matched in T by S′, and the only extra White resource, the move m, is answered on the board.
- **Black's side needs one token.** White, after a bad Black move at a root, may still owe over's one move ω → 0_D,
  which S may ask for at a moment chosen by T; that is the one unforced White move. White cannot give over up (that is
  a downgrade for White), so this budget is genuine, and Z_O fails exactly here (1…e5–e4 is saved by one Black
  token), matching K47's finding that all of Z_O's differences from over favour Black.
- **Draws.** Transferred with non-losing strategies; Black's draws beside off at the roots of H10 (the K55 referee's
  observation; x ⊞ off is a draw for …Kf6–e6, …e5–e4, …e5–e3) are harmless: (B1) asks for one token only.
- **Terminals of T** are covered: X's moves in T are always answered by S_cur in T.
- **Matched passes (idea 2)** are not needed; the asymmetric budgets (0 for White's bad moves, 1 for Black's at the
  roots, 0 at q) are what the proof uses.
- **Necessity.** (B1) is not necessary in general: on the K56 referee's abstract toy groups, many exact groups without
  (B1) still have the results of over (findings.txt sec. 3b), while none of the 1,758 with (B1) differs from over
  (COMPUTED-1, a test of the lemma, not part of its proof). For Z_O, failing (B1) goes with a real difference (K47).
- **The K56 erratum** (the pass layers are not monotone in the number of passes) does not touch this proof: it uses
  only the 0- and 1-token games, the step from one token to none through the token move itself ((P1)), and the
  inclusion of P-wins in the token game with the sum's rule (a stalemate of the loser becomes a loss instead of a
  draw, which only adds wins for the winner).

## 5. The computed facts used for H10, and their labels

- Definition 4.8 for H10: K45 (two implementations, ref3m and kp_p confirm): CHECKED-2; K56's pr56 reproduces it.
- (B1) for H10: the ten non-shuttle Black moves at the two roots (…Ke6, …a4, …a3, …e4, …e3 at the f6 root; …Kh6, …a4,
  …a3, …e4, …e3 at the g6 root). For each, r(x_m ⊞ (−1), White to move) = W by:
  - K55's za and rz (refereed for cyl:10×6), run on the positions after the moves (logs/C_za_H10*, C_rz_H10*): W for
    the eight moves without an e.p. right. Their input format has no e.p. right, so for the two double steps …a5–a3
    (where White's b3 pawn may take e.p. on a4) they report the position without the right (L, as expected) and were
    run instead on the position after White's e.p. capture b3xa4, Black to move: W (both solvers, both roots), which
    gives W at x_m because White has that move;
  - pr57 (K57's copy of K56's pr56, which keeps the right): W1 (White wins with Black allowed one pass, stalemate a
    draw, a stronger statement than (B1)) for all ten.
  So (B1) for H10 is CHECKED-2.
- (B1) for the four cyl:8×7 groups: pr56/pr57 only (K56 logs, N1 = yes for every non-shuttle Black root move):
  COMPUTED-1. For Z_O and its flat translates (B1) fails (K56).

**Weakest step.** In the proof: the termination count of phase 2 and the bookkeeping of which side may be asked for an
unforced G-move (the budget). In the corollary: that the computed facts are complete, i.e. that the list of Black root
moves and the e.p. handling are right (two solvers needed the e.p. follow-up by hand).
