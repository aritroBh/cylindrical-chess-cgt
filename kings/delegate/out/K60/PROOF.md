> **Notes from the referee (K60 verify, 2026-11-23), wording only; no statement or proof step changes.** (1) The e.p.
> bullet says White's right is the same in V1 and in the real play; after a pass answered by a freeze it is not, which
> does no harm to the argument. (2) "4·|boards| states" counts each board together with its e.p. right. (3) The remark
> after B3 that the smallest working N is 0 to 2 is superseded by §6, where N up to 5 is needed.

# K60: an exact test for "has the results of over"

AI work (one agent), not refereed, no human re-derivation. Labels: PROVED = complete hand proof below; COMPUTED-1 =
one program (mine, `src/`); KNOWN = standard result with a reference. Solver results are never PROVED.

## 0. Short answer

Let G be an exact over group (Definition 4.8), taken as the P game of its own pieces in a D-sum (Definition 1.3 with
K40's convention, as in Lemma 4.15). For a non-shuttle Black move m at a root write x_m for the position after m,
White to move, with White's e.p. right if m is a double step.

- **Theorem A (PROVED).** G has the results of ω beside every finite D-game (both roots, either side to move) iff
  **(C)**: for every such m, every finite D-game T and position t,
  r(x_m ⊞ t, White to move) ≥ r(ω ⊞ t, **Black** to move) (White's order L < D < W).
  The q's have the results of 0_D for every exact group, with no condition, and Black always does at least as well
  beside the group as beside ω (Proposition A0). In K57's proof of Lemma 4.15, (B1) is used only in Case E3 (Black's
  bad root move) and in the token budget b = 1 of phase 2 that E3 creates; under (C), Case E3 is replaced by "White
  switches to an optimal strategy of G ⊞ T from the real state", and phase 2 is needed only with b = 0.
  The comparison with ω ⊞ t **White** to move, (C_W), is sufficient but not necessary (Proposition A2: a group with
  (B1), hence with the results of ω, where x_m ⊞ t is a White loss and ω ⊞ t, White to move, a White win).
- **Theorem B (PROVED).** (C) at m holds iff White wins the auxiliary game **Aux(x_m)**: x_m ⊞ under_D, White to move
  (under_D = the colour mirror of over_D: White may pass ω̄ → ω̄, Black may once freeze ω̄ → 0̄, both subject to the
  sum's rules: not in check, clearing the e.p. right), with the D-sum rules for finite plays and one change: **an
  infinite play is a White win iff White passed in under infinitely often** (a Büchi condition). Equivalently, iff
  r(x_m ⊞ u_0, White to move) = W in the finite D-game T_N (u_0, …, u_N, 0; White u_i → u_{i+1} for i < N and
  u_N → ⊕; Black u_i → 0), for one, or every, N ≥ K, where K is the number of (board, e.p. right, side) states of the
  group. So (C) is decided on the group's own finite graph (a Büchi game of size 4·|boards|), and
  **one test game suffices**: G has the results of ω beside every finite D-game iff both roots, Black to move, are White
  wins beside u_0 of T_K (Corollary B3). (B1) is the special case "White wins Aux without ever passing" (Corollary B2).
- **Example (PROVED).** A 10-board abstract exact group G1 (§5) fails (B1) and has the results of ω: after its bad
  Black move, White's winning idea is to *pass first* (in Aux), which puts Black in zugzwang on the board.
- **Real groups (COMPUTED-1, aux60).** H10: Aux is a White win after all ten bad Black root moves. Z_O (cyl:8×6): Aux
  is a White win after every bad Black root move except 1…e5–e4 at the d4 root, where it is a loss; so Z_O fails (C)
  exactly there, as K47 and K57 imply. See §6 for the numbers. No known real group has the results of ω without (B1).

## 1. Setting

As K57 §1. A state of G ⊞ T is (g, t, s): board g with its e.p. right, position t of T, side s to move. The mover makes
one legal move in G or one option in T. A promotion ends the play as a win for the promoter; a move to ⊕ (⊖) ends it as
a White (Black) win, whoever makes it. A side in check may not move in T. A move in T clears the e.p. right. A side with
no legal move anywhere loses. Infinite play is a draw. r is the least fixed point (Definition 1.2). over_D: positions
ω, 0_D; L(ω) = {0_D}, R(ω) = {ω}. under_D: positions ω̄, 0̄; L(ω̄) = {ω̄}, R(ω̄) = {0̄}. Roots A, B (Black king on
z0, z1), no e.p. right. By Definition 4.8 with K1, K2: no king is in check at the roots or at the q's; Black's
shuttle is legal; every other Black root move loses at once in P; White has a freeze at each root, every other White
root move loses at once in P; at each q every legal move of the side to move loses at once in P and each side has one.

KNOWN facts used (finite game graphs): (K-a) r = W iff White has a strategy that wins every consistent play within a
bounded number of moves; (K-b) r ≠ L iff White has a strategy no consistent play of which is a Black win; colours
exchanged likewise. A winning (non-losing) strategy stays winning (non-losing) from every consistent state.
(K-c) Büchi games on finite graphs are determined, and both players have positional winning strategies (Büchi 1969,
McNaughton 1993, Zielonka 1998; textbook: Grädel, Thomas, Wilke (eds.), *Automata, Logics, and Infinite Games*, LNCS
2500, 2002, ch. 2).

"Has the results of ω" means: r(root ⊞ t, s) = r(ω ⊞ t, s) for both roots, every finite D-game T, every t and s.

## 2. Theorem A

**Proposition A0 (PROVED; K57's proof, cases E1 and E2).** For every exact over group, every finite T, t and s:
(i) r(q ⊞ t, s) = r(0_D ⊞ t, s) for every q (Black to move with or without the right of a double-step freeze, and White
to move); (ii) r(root ⊞ t, s) ≤ r(ω ⊞ t, s) (White's order) for both roots.

*Proof.* K57 §3 proves (★) for each colour Y. Read it with Y = Black, X = White: phase 1 and Case E1 never use (B1),
and phase 2 then runs with b = 0. This transfers every Black win and every Black non-loss from over_D ⊞ T to G ⊞ T, at
the roots and at the q's, which is (ii) and half of (i). For the other half of (i), Y = White at a q: phase 1 at a q
has o = 0_D, every Black move there enters phase 2 through Case E2 (b = 0), never E3. Again no (B1). ∎
(I re-read K57 §3.1–3.3 line by line for this: (B1) occurs only in Case E3 and in the budget b = 1, which only E3 sets.)

**Theorem A (PROVED).** G has the results of ω iff (C) holds for every non-shuttle Black move m at either root.

*Necessity.* Fix m at root ρ, T and t. The root (ρ, t, Black to move) has Black not in check, and m is a legal Black
option leading to (x_m, t, White to move) (with White's e.p. right if m is a double step; the right belongs to White,
who is to move). The least fixed point gives r(ρ ⊞ t, B) ≤ r(x_m ⊞ t, W) (a Black-to-move value is at most the value
of each option, in White's order). With r(ρ ⊞ t, B) = r(ω ⊞ t, B) this is (C).

*Sufficiency.* By Proposition A0 it suffices to transfer White's wins and White's non-losses from (ω, t0, s0) to
(ρ0, t0, s0) for a root ρ0. Use K57 §3 with Y = White, X = Black, with one change. Phase 1 is unchanged (the mirror:
shuttle = ω → ω, freeze = ω → 0_D; Black's T-moves copied; White's T-moves and freezes from S_cur). Black's moves that
leave phase 1 are: a move at a q (Case E2, unchanged, b = 0), or a non-shuttle Black root move m. In the latter case
(K57's E3), the real state is (x_m, t, White to move) and the virtual state (ω, t, Black to move) is S_cur-consistent,
so r(ω ⊞ t, B) = W (resp. ≥ D) for the guarantee being transferred. By (C), r(x_m ⊞ t, W) ≥ r(ω ⊞ t, B). **White
forgets the virtual game and plays, from the real state, a strategy of G ⊞ T that realises r(x_m ⊞ t, W)**: it wins
(resp. does not lose). The real play is an S_cur-consistent prefix (bounded by S's bound when S wins) followed by a
play of that strategy (bounded when it wins), so a win is won within a bounded number of moves (K-a), and a non-loss
is never lost (K-b). ∎

*Where (B1) was used and how (C) replaces it.* K57 Case E3 needs (x_m, White, 1 token) ∈ Att^B_1, so that White can
answer Black's board moves on the board and still afford the one unforced board move that S_cur may ask for (ω → 0_D)
at a moment chosen through T. (C) asks directly for what that construction delivers: that White does as well from the
real state as the virtual state allows. Nothing else in K57's proof changes. The Black-to-move value of ω ⊞ t is the
right comparison because the virtual state at E3 has Black to move (Black has just moved in the real game, not in the
virtual one); the necessity proof shows it cannot be weakened.

**Proposition A1 (PROVED).** r(ω ⊞ t, B) ≤ r(ω ⊞ t, W) for every T, t. So (C_W): r(x_m ⊞ t, W) ≥ r(ω ⊞ t, W) for all
m, T, t, implies (C). *Proof.* ω → ω is a Black option at (ω, t, B) leading to (ω, t, W). ∎

**Proposition A2 ((C_W) is not necessary; PROVED).** The abstract exact group G2 below satisfies (B1), so it has the
results of ω (Lemma 4.15), but (C_W) fails at its bad Black move beside the D-game t0 with L(t0) = {t1}, R(t0) = {⊖},
L(t1) = {⊕}, R(t1) = ∅.
G2 (boards A, B, q, qb, qw, x, w, w2; no checks, no double steps). White: A → q, B → q, q → qw, qb → ⊕, x → w, w → ⊕,
w2 → ⊕. Black: A → B, A → x, B → A, q → qb, qw → ⊖, x → ⊖, w → w2.
*Exactness.* q, Black to move: only q → qb, after which White promotes: W. q, White to move: only q → qw, Black
promotes: L. So q is a mutual zugzwang, and A → q, B → q are freezes (White's only root moves). Black's root moves:
the shuttle and A → x; x, White to move: x → w, then Black's only move w → w2 and White promotes: W in P. So (O1)–(O4)
hold. *(B1).* x ⊞ (−1), White to move: x → w; Black either plays w → w2 (White promotes) or spends the token (White,
at w, promotes). W. *(C_W) fails.* r(ω ⊞ t0, W) = W: White plays t0 → t1; Black's only option at (ω, t1, B) is the
pass ω → ω; White plays t1 → ⊕. r(x ⊞ t0, W) = L: if White plays x → w, Black plays t0 → ⊖; if White plays t0 → t1,
Black (at x, not in check) promotes. (Consistently with (C): r(ω ⊞ t0, B) = L, Black plays t0 → ⊖.) ∎
The point: x_m is a position where Black, to move, would win at once; White to move must answer on the board first.
ω with White to move has no such obligation. Comparing with ω White to move is therefore too strong.

## 3. Theorem B: (C) is decided by a Büchi game on the group's graph

Fix x = x_m. **Aux(x)** is played on the states (g, u, s) of G ⊞ under_D (g a board with its e.p. right, u ∈ {ω̄, 0̄}),
starting at (x, ω̄, White). Moves: board moves (legal in P, with checks; a promotion ends the play as a win for the
promoter); White's pass ω̄ → ω̄ (only if White is not in check; clears the right); Black's freeze ω̄ → 0̄ (only if Black
is not in check; clears the right). A side with no move loses. An infinite play is a **White win iff it contains
infinitely many White passes**, a Black win otherwise.

**Theorem B (PROVED).** Let K be the number of states (g, s) with u = ω̄ (boards with e.p. right, times two sides; any
upper bound will do, e.g. 4 × the number of boards). For N ≥ 0 let T_N be: positions u_0, …, u_N and 0; White options
u_i → u_{i+1} (i < N), u_N → ⊕; Black options u_i → 0 for every i; 0 has none. The following are equivalent:
(1) (C) holds at m; (2) White wins Aux(x); (3) r(x ⊞ u_0, W) = W in T_N for every N; (4) r(x ⊞ u_0, W) = W in T_N for
some N ≥ K.

*(2) ⇒ (1).* Let σ be a strategy of White in Aux(x) that wins (in the Büchi sense) from (x, ω̄, W). Let T, t be given
and let S be a strategy of White in over_D ⊞ T from (ω, t, B) that wins (resp. does not lose); we build a White strategy
in x ⊞ T from (x, t, W) that wins (resp. does not lose). White keeps two virtual games: V1 = the Aux play (real board
plus a virtual under-component) and V2 = the over_D ⊞ T play (a virtual over-component plus the real T). A virtual
"mirror Black" makes Black's moves in the virtual components: a White pass in V1 (ω̄ → ω̄) is mirrored by a Black pass in
V2 (ω → ω); a White freeze in V2 (ω → 0_D) is mirrored by a Black freeze in V1 (ω̄ → 0̄). Invariants (proved by the
case list): (I1) when the real side to move is White, V1 has White to move and V2 has Black to move; when it is Black,
both have Black to move; (I2) ω̄ is present in V1 iff ω is present in V2; (I3) V1's board equals the real board, except
that V1 may still record a Black e.p. right that a real Black T-move has cleared; V2's T-position equals the real one;
(I4) V1 is σ-consistent and V2 is S-consistent.
- Real White to move at the start or after a real Black board move: play σ's move in V1. A board move is played for
  real. A pass ω̄ → ω̄ (White not in check):
  mirror Black passes in V2, so V2 has White to move; S answers either with a T-move, played for real, or with
  ω → 0_D, mirrored by Black's ω̄ → 0̄ in V1 (legal: Black is not in check, since the board last changed by a Black
  move or is x, reached by Black's move m; ω̄ present by I2), after which σ answers with a board move (ω̄ is gone),
  played for real.
- Real Black moves on the board: the same move in V1 (legal there: V1 has at least the real options, I3). σ answers;
  continue as in the previous item. (So σ chooses freely only at the start and after Black's board moves; there the
  board last changed by a Black move, m or a later one, so Black is not in check, which the mirror freeze needs.) If Black gave check, σ answers on the board (the sum's rule holds in Aux too).
- Real Black moves in T (so Black is not in check): the same move in V2 (Black to move there, I1). S answers: a
  T-move, played for real (White is not in check: the board last changed by White's own move, or is x and σ has already
  moved, or σ passed at it, which needs White not in check); or ω → 0_D, mirrored by Black's ω̄ → 0̄ in V1 (legal: Black
  was not in check, the board is unchanged), after which σ answers with a board move, played for real.
- e.p.: a real T-move clears the real right; in V1 the right of a waiting Black is cleared only by the mirror freeze;
  removing the right only removes Black options (I3). White's right is the same in V1 and real: White's T-moves and
  passes clear it in both.
White always has a move (σ and S name one; a stuck White would lose the respective virtual game). Each real move is
followed by a bounded chain of virtual moves (at most: pass, mirror pass, S's answer, mirror freeze, σ's answer).
Ends. A board promotion by Black, or White stuck, would be a Black win of V1, excluded by σ; ⊖ in T would be a Black
win of V2, excluded by S; Black stuck in the real game loses. Infinite real play: if it has infinitely many T-moves,
V2 is infinite — impossible when S wins, a draw when S only does not lose; otherwise V1's play is infinite, eventually
board-only, and it has only finitely many White passes (each pass is followed by an S-move in V2, and V2 can have only
finitely many moves if S wins); a σ-consistent Aux play cannot be like that. So if S wins, every consistent real play
is finite and a White win; the strategy uses finite memory, the game is finitely branching, so by König's lemma the
wins are bounded (K-a). If S does not lose, no consistent real play is a Black win (K-b). Hence (1). ∎

*(1) ⇒ (3).* (C) at t = u_0 needs r(ω ⊞ u_0, B) = W. White's strategy in over_D ⊞ T_N from (ω, u_0, B): answer every
Black pass ω → ω at u_i (i < N) with u_i → u_{i+1}; at (ω, u_N, W) play u_N → ⊕; answer Black's u_i → 0 with ω → 0_D,
after which Black, at (0_D, 0, B), has no move and loses. Black has no other options. The play ends within 2N + 3
moves. ∎

*(3) ⇒ (4)* is trivial.

*(4) ⇒ (2).* Suppose White does not win Aux(x). By (K-c) Black has a positional strategy β that wins Aux from
(x, ω̄, W). Let H be the graph of Aux restricted to the states reachable from (x, ω̄, W) when Black follows β (all White
edges, Black's β-edges). **No White pass edge lies on a cycle of H**: otherwise White could walk to it and repeat the
cycle forever, a β-consistent infinite play with infinitely many passes (the cycle has no terminal), which β does not
allow. So every pass edge joins two different strongly connected components of H, and along any path the components
visited never repeat; hence every β-consistent play has fewer than K passes (passes join states with u = ω̄, and there
are at most K of these). Now let Black play β in x ⊞ T_N, N ≥ K, through the identification φ: (g, u_i, s) ↦ (g, ω̄, s),
(g, 0, s) ↦ (g, 0̄, s): Black's freeze ω̄ → 0̄ is played as u_i → 0; White's u_i → u_{i+1} is read as a pass. The
options correspond exactly (same check rule, same clearing of the right, same no-move rule), except White's u_N → ⊕,
which needs N ≥ K passes on a β-consistent play and is never available. So every play of x ⊞ T_N consistent with β is
the image of a β-consistent Aux play: it ends in a Black win, or is infinite (a draw). Hence r(x ⊞ u_0, W) ≠ W. ∎

**Corollary B1 (decidability; PROVED).** "G has the results of ω beside every finite D-game" is decided by finitely
many Büchi games on the group's own graph (one per non-shuttle Black root move), each with 4·|boards| + O(1) states,
solvable in polynomial time (e.g. the classical attractor iteration; implemented in `src/k60lib.py`, `src/aux60.cpp`).

**Corollary B2 ((B1) ⇒ (C); a second proof of Lemma 4.15; PROVED).** If x ⊞ (−1) is a White win, White wins Aux(x)
without ever passing: Aux restricted to "White never passes" is exactly x ⊞ (−1) (Black's freeze is Black's one move
elsewhere, under the same rules). With Theorems A and B this re-proves Lemma 4.15. (C) is weaker than (B1) exactly by
White's option to pass before Black has frozen.

**Corollary B3 (one test game; PROVED).** Let K be as above. G has the results of ω beside every finite D-game iff
r(ρ ⊞ u_0, Black to move) = W in T_K for both roots ρ. *Proof.* ⇒: r(ω ⊞ u_0, B) = W ((1) ⇒ (3) above). ⇐: for every
bad Black move m at ρ, r(x_m ⊞ u_0, W) ≥ r(ρ ⊞ u_0, B) = W (Black option), so (4) holds, so (C) holds at m (Theorem B),
so G has the results of ω (Theorem A). ∎
K is large for real groups (millions), so for them the Büchi form is the practical one. On the toy groups the smallest
N that works is 0, 1 or 2 (§6).

**Remarks.**
- *Why the Büchi scoring.* x ⊞ under_D with draws as draws is too weak (White surviving it is necessary, not
  sufficient), and with "infinite play = White loss" too strong (White winning it outright is sufficient, not
  necessary): COMPUTED-1, §6. In a real context, White's passes in under correspond to Black passes in over that S must
  answer; S wins, so it cannot answer forever, and an infinite run of White passes never happens in the real game.
  That is what the scoring credits to White. (This is the loopy "difference game" x − over = x + under, with the
  onside-type scoring for White's passes.)
- *The draw part alone.* Surviving Aux in the ordinary sense (x ⊞ under_D, White to move, r ≠ L) is equivalent to
  the D-half of (C) (r(ω ⊞ t, B) ≥ D ⇒ r(x ⊞ t, W) ≥ D): necessity with T = under_D (r(ω ⊞ ω̄, B) = D), sufficiency by the
  proof of (2) ⇒ (1) with σ only non-losing. (PROVED; not needed for the theorems.)
- *Checks and e.p. in Aux.* Aux is a game on the P graph of the group with the sum's rules, so checks, the clearing of
  the right by passes and freezes, mate and stalemate (a side with no move, in check or not, loses: the sum's rule) are
  part of it. P's stalemate-draw rule enters only through Definition 4.8.

## 4. What the theorems do not give

- No fixed finite family independent of the group: Corollary B3's test game T_K grows with the group. Whether a fixed
  finite family (independent of the group) suffices is OPEN. On the toy groups the family k·↓ is not exact for k ≤ 4
  (§6), and the T_N needed reaches N = 5; I have no proof either way.
- Theorem A/B concern D-sums of the P game of the group's pieces. They say nothing about P contexts (which K47 found
  not to behave as D-sums) or chess.

## 5. The example G1: fails (B1), has the results of ω (PROVED)

Boards A, B (roots), q, qb, qw, x, x2, y, z, y2; no checks, no double steps, no e.p. moves.
White: A → q, B → q, q → qw, qb → ⊕, x → y, x2 → ⊕, y → y2, z → ⊕.
Black: A → B, A → x, B → A, B → x, q → qb, qw → ⊖, x → x2, y → z, y2 → ⊖.

*Exact.* P-values (White's view): qb, z, x2 with White to move: W (promotion); qw, y2 with Black to move: L. y with
Black to move: only y → z: W. y with White to move: only y → y2: L. x with White to move: only x → y (Black to move,
W): W. x with Black to move: only x → x2: W. q with Black to move: only q → qb: W; q with White to move: only q → qw:
L. So q is a mutual zugzwang, both sides have moves there, all of them lose at once. At each root White's only move
is the freeze to q; Black's moves are the shuttle and the move to x, which loses at once (x, White to move, is W).
No checks, so Definition 4.8 holds (q with either side to move is legal).

*(B1) fails.* x ⊞ (−1), White to move: White's only move is x → y. Black spends the token: (y, White to move) with no
token left; White's only move is y → y2, and Black promotes. So x ⊞ (−1) is a Black win.

*Aux(x) is a White win.* White passes (not in check): (x, ω̄, Black to move). Black's options: x → x2, after which White
promotes; or the freeze, after which (x, 0̄, White): x → y, Black's only move y → z (Black has no move elsewhere), White
promotes. Every play ends in a White win within 5 moves.

So by Theorems A and B, G1 has the results of ω beside every finite D-game (both roots, either side) and each q the
results of 0_D, although it fails (B1). For instance beside \*: r(ω ⊞ \*, B) = W, and in G1 beside \* with Black to
move Black's move to x is answered by White taking \* (White's "pass"): Black at x must play x → x2 and loses.

*K58's witness fails (C).* In K58's group (r0, r1, q, x, p), Aux(x) is a Black win: if White passes, Black promotes at
x; if White plays x → q, Black freezes and White's only move q → x lets Black promote. Consistently, K58 shows the group
differs from ω beside \*.

## 6. Computations (COMPUTED-1)

Own code: `src/k60lib.py` (least-fixed-point solver, D-sums, Definition 4.8, (B1), Büchi solver and Aux), `src/k60games.py`
(test games, toy generators, T_N, the hand examples G1 = `example_nob1`, G2 = `example_cw`, K58's group), `src/validate.py`
(toy validation), `src/explore.py`, `src/witness.py` (exploration), `src/aux60.cpp` (Aux and (B1) for real groups; its move
generator and graph builder are copied from the K57 referee's `vgsum.cpp`, the rest is new). Logs in `logs/`.

**Toy validation** (`validate.py`, seeds 11, 12, 13; each: 1,500 random exact groups (random move graphs repaired
towards Definition 4.8) and 1,000 from an adversarial family (a random gadget region behind the bad Black root moves),
plus G1, G2 and K58's group). Toy groups model checks (no move elsewhere in check, no move into check, mate a loss
and stalemate a draw in P) and e.p. rights (double steps, extra moves for one turn, cleared by a move elsewhere).
Battery per group: 281 finite D-games (34 named: integers, \*, \*2, ↑, ↓, on, off, dud, over, under, ±1, ±2, tiny,
miny, terminal threats, …; 91 sums of two and five of three; 150 random games of ≤ 5 positions, loopy, with terminals)
and T_{4n} (n = number of boards). Totals over the three seeds:
- 7,509 exact groups (4,246 with a check somewhere, 7,274 with a double step, 3,067 with e.p.-only moves),
  83,127,655 compared results; 21,556 bad Black root moves.
- Theorem A on the battery (results of ω on the battery ⇔ (C) on the battery at every bad move): 0 violations.
  Proposition A0 (each q has the results of 0_D): 0 violations.
- Aux ⇒ (C) on the battery: 0 violations. (C) on the battery ⇒ Aux: 0 violations. Aux ⇔ x ⊞ T_{4n} White win:
  0 violations. (B1) ⇒ Aux: 0 violations.
- Aux wins at 19,155 bad moves, losses at 2,401; 1,604 Aux wins without (B1). 6,358 groups have the results of ω on the
  battery; 872 of them fail (B1); 866 of them fail (C_W) on the battery (Proposition A2's phenomenon is common).
  1,151 groups differ from ω on the battery, every one with an Aux loss.
- Smallest N with x ⊞ T_M agreeing with Aux for all M ≥ N (M ≤ 4n): 0 at 19,428 bad moves, 1 at 1,204, 2 at 837,
  3 at 67, 4 at 18, 5 at 2.
- k·↓ (k copies of ↓) as a test (x ⊞ k·↓, White first, a White win): disagrees with Aux at 365 bad moves for k = 1, 135
  for k = 2, 5 for k = 3, 3 for k = 4. So no small fixed k·↓ is an exact test on these toys (evidence only; §4).
- Peak memory 26 MB, about 300 s per seed.

**Real groups** (`aux60`, K57 referee's move generator, P game of the group's pieces with e.p. rights; sum's rules).
- H10 (cyl:10×6, 4,360,884 nodes): all ten bad Black root moves: (B1) W, Aux WIN. 3 Büchi iterations; 0.89 GB, 3.5 s.
- Z_O (cyl:8×6, 6,496,367 nodes): Aux WIN at ten of the eleven bad Black root moves, LOSS at 1…e5–e4 at the d4 root,
  which is also the only (B1) failure (my token solver agrees with the K57 referee's vgsum output there). 4 Büchi
  iterations; 1.30 GB, 5.6 s. So Z_O fails (C) exactly at 1…e5–e4.
- Second check of that failure with a different solver (the K57 referee's `vgsum` sum solver beside T_0 … T_6, same
  move generator): x ⊞ u_0 with x after 1…e5–e4 at the d4 root, White to move, is W beside T_0, T_1 and **L beside
  T_2 … T_6**; by Theorem B ((1) ⇒ (3)) one non-W already refutes (C). Corollary B3's root test: the d4 root, Black to
  move, is L beside T_2 … T_6, the d5 root W beside T_0 … T_2 and L beside T_3 … T_6 (Black shuttles to d4 first). The
  x after e5–e4 at the d5 root stays W beside T_0 … T_6, matching its Aux WIN. 1.84 GB, 13 s.
  Label: two solvers (Büchi attractors in aux60; retrograde D-sum in vgsum) on one shared move generator.
