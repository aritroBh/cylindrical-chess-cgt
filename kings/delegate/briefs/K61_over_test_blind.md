# K61: blind proof of an exact test for "has the results of over"

**Output directory:** `kings/delegate/out/K61/` (create it if it does not exist). Write only there. Do **not** edit any
existing file. Do not run git.

Two statements about exact over groups in sums with decisive terminals are proposed for the theory note. You are an
independent check from outside the vendor that proposed them, and you see the statements only. Everything you need is
in this file. Prove each statement, or refute it with a concrete counterexample.

**Read only:** this file; `kings/SPEC.md` (the move rules of king-and-pawn chess, if you want the chess origin of the
abstract model below); and `delegate/COMMON.md`, rules 5 and 7 only (ignore its "Read first" list). **Do not open**, at
any time during this task: `kings/theory/`, `kings/delegate/out/` other than `kings/delegate/out/K61/`,
`kings/delegate/briefs/` other than this file, `notes/`, `RESULTS.md`, `RESEARCH_PLAN.md`, `paper/`, `dist/`, or the
git history. They contain material on these statements that would make your check not blind.

## 1. Definitions

### 1.1 D-games, play, results

**D-game.** A *D-game* is a finite set X of positions with, for each x ∈ X, finite option sets L(x) and R(x) contained
in X ∪ {⊕, ⊖}. ⊕ is the terminal "White has won", ⊖ the terminal "Black has won". White = Left (options L), Black =
Right (options R). A D-game is *short* if its move graph on X is acyclic, *loopy* otherwise. A *finite D-game* is any
D-game in this sense: short or loopy, with or without terminals; a move of Black to ⊕ (or of White to ⊖) is allowed.

**Play and results.** Play alternates from (x, s), s the side to move. A move to ⊕ or ⊖ ends the play with that
result. A side with no option loses. Infinite play is a draw. r(x, s) = W if White can force a White win in finitely
many moves, L if Black can, D otherwise. r is written from White's side and ordered L < D < W. On a finite game graph r
is the least fixed point of retrograde analysis.

### 1.2 Sums

**D-sum.** For components A₁, …, A_k the sum A₁ ⊞ … ⊞ A_k has tuples as positions; a move is a move in one component;
a move to ⊕ or ⊖ in any component ends the whole play; a side with no move in any component loses; infinite play is a
draw. A move in a component other than the one under discussion is a move *elsewhere*.

### 1.3 over_D, 0_D, under_D, and the test games T_N

- **over_D:** positions ω and 0_D; L(ω) = {0_D}, R(ω) = {ω}, 0_D has no options. (Black may pass at ω forever; White
  has one move ω → 0_D, after which nobody can move there.) So r(0_D ⊞ t, s) = r(t, s).
- **under_D:** the colour mirror: positions ω̄ and 0̄; L(ω̄) = {ω̄}, R(ω̄) = {0̄}, 0̄ has no options. (White may pass at
  ω̄ forever; Black has one move ω̄ → 0̄, called the *freeze* of under.)
- **T_N** (N ≥ 0): the short D-game with positions u_0, …, u_N and z; L(u_i) = {u_{i+1}} for i < N, L(u_N) = {⊕};
  R(u_i) = {z} for every i; z has no options.

### 1.4 Abstract groups (the chess model, abstracted)

A *group* G is a finite directed game graph that models the P game (promotion model) of a king-and-pawn position:

- *Boards.* A finite set of boards. A *state* of G is (g, e, s): a board g, a side s to move, and a flag e saying
  whether s holds an *e.p. right* at g.
- *Moves.* For each state a finite list of legal moves of s. A move either *promotes* (it ends the play at once as a win
  for s: in a sum, a move to s's terminal) or leads to a board g′ with the other side to move. A move may be a *double
  step*: then the other side holds the e.p. right at g′; otherwise it holds none. Some moves of s at g (the *e.p.
  moves*) are legal only when s holds the right.
- *Check.* For each board and each side, a predicate "that side's king is in check at g". No legal move of s leads to
  a board where s is in check (no move into one's own check). In particular the side not to move is never in check at
  a reachable state.
- *P alone* (the group with nothing beside it): a side with no legal move loses if it is in check (mate) and draws
  otherwise (stalemate); a promotion wins for the promoter; infinite play is a draw. "In P" values use these rules.
- *The group as a component of a D-sum.* The group is the game above, with these rules beside other components:
  a promotion is a move to the promoter's terminal (it ends the whole sum); a side in check may not move elsewhere (it
  must move in G); a move elsewhere clears the e.p. right that the mover held in G (the same holds for a pass or a
  freeze in under_D or over_D, which are moves elsewhere); a side with no legal move in any component loses (so a side
  that is stalemated in G but can move elsewhere is not stuck, and one with no move anywhere loses although stalemate
  is a draw in P alone).

### 1.5 Exact over groups

A group G is an *exact over group* if it has two *roots* A and B (boards), a Black *shuttle* move A → B and B → A, and,
with "a move of side X loses at once" meaning "the state after it, with the other side Y to move (and Y's e.p. right if
the move was a double step), is a win for Y in P alone":

- (O0) no king is in check at A, B, or at any q below; the roots carry no e.p. right;
- (O1) at both roots with Black to move, the shuttle is legal and every other legal Black move loses at once (none
  promotes);
- (O2) at both roots with White to move, White has at least one move that does not lose at once (a *freeze*), and no
  White move at a root promotes;
- (O3) after each freeze, the board q, with Black to move (with Black's e.p. right if the freeze was a double step),
  has a legal Black move and every legal Black move loses at once (none promotes);
- (O4) the same board q with White to move (no right) has a legal White move and every legal White move loses at once
  (none promotes).

So every White move at a root that is not a freeze loses at once, and each q is a mutual zugzwang of P. The
*q-states* are q with Black to move (with and without the right of a double-step freeze) and q with White to move.

A *bad Black move* is a non-shuttle Black move m at a root (Black to move). x_m denotes the state after it: White to
move, with White's e.p. right if m is a double step.

**Has the results of ω.** G has the results of ω beside every finite D-game if, for every finite D-game T, position t
and side s, r(ρ ⊞ t, s) = r(ω ⊞ t, s) for both roots ρ (no e.p. right) and r(q ⊞ t, s) = r(0_D ⊞ t, s) for every
q-state.

### 1.6 The auxiliary game Aux(x)

For a state x of G with White to move, **Aux(x)** is played on G ⊞ under_D from (x, ω̄), White to move, with the sum's
rules of 1.2 and 1.4 for every finite play (White's pass ω̄ → ω̄ and Black's freeze ω̄ → 0̄ are moves elsewhere: not
allowed while the mover is in check, and they clear the mover's e.p. right; promotions end the play; a side with no
move loses), and one change: **an infinite play is a White win if White made infinitely many passes ω̄ → ω̄ in it, and
a Black win otherwise.** "White wins Aux(x)" means White has a strategy that wins every play consistent with it.

## 2. The statements

Let G be an exact over group as a component of a D-sum (1.4, 1.5).

**Statement A.** G has the results of ω beside every finite D-game if and only if

> **(C)** for every bad Black move m (at either root), every finite D-game T and every position t of T:
> r(x_m ⊞ t, White to move) ≥ r(ω ⊞ t, Black to move).

(The comparison on the right is with **Black** to move in ω ⊞ t.)

**Statement A0 (part of A).** For every exact over group, with no further condition: every q-state has the results of
0_D, and r(ρ ⊞ t, s) ≤ r(ω ⊞ t, s) for both roots, every finite D-game T, position t and side s.

**Statement B.** Let K be the number of states (g, e, s) of G. For a bad Black move m the following are equivalent:
1. (C) holds at m (for every finite D-game T and position t);
2. White wins Aux(x_m);
3. r(x_m ⊞ u_0, White to move) = W in T_N for every N ≥ 0;
4. r(x_m ⊞ u_0, White to move) = W in T_N for some N ≥ K.

**Statement B3.** G has the results of ω beside every finite D-game if and only if, for both roots ρ,
r(ρ ⊞ u_0, Black to move) = W in T_K.

## 3. Readings to fix

Say in `PROOF.md`, at the top, which reading you use for each point; if a statement holds in one reading and fails in
another, say so and give the counterexample.

- **R1 (side to move).** In (C) the left side has White to move (with White's e.p. right after a double step m), the
  right side Black to move. Check that every comparison you use respects this.
- **R2 (no move loses, stalemate).** "Loses at once" in 1.5 is judged in P alone (stalemate a draw); everything in a
  sum, in Aux and in T_N uses the sum's rule (a side with no move anywhere loses).
- **R3 (checks).** A side in check may not move elsewhere, which includes passing or freezing in under_D and over_D
  and moving in T, even to a terminal of T.
- **R4 (e.p. right).** The right belongs to the side to move and lapses after any move of that side, in G or elsewhere.
- **R5 (draws).** r has three values. "≥" in (C) is in the order L < D < W. In Aux there are no draws: an infinite play
  with finitely many White passes is a Black win.
- **R6 (the class of T).** Every finite D-game: loopy or short, terminals for either side (suicides included), White
  options and Black options, positions with no options; every position t is a start.
- **R7 (the model).** The statements are about the abstract groups of 1.4. If you think a statement fails only for
  abstract groups that no king-and-pawn position can realise, say so, but a counterexample in the abstract model
  counts.

## 4. Task

Write `PROOF.md`, your own complete argument, in this order.

1. **Readings.** Your choice for R1 to R7 and any further ambiguity you find.
2. **Statement A0** and **Statement A**: complete proofs (both directions of A), or a concrete counterexample: an
   explicit exact over group (boards, moves, checks, e.p. rights), a finite D-game T, a position t and a side s.
3. **Statement B**: a complete proof of every implication you need for the equivalence, or a counterexample. If you use
   a known theorem about infinite games, state it exactly, give a reference, and check that its hypotheses hold here
   (in particular how finite plays that end by a promotion, a terminal or a side with no move are encoded).
4. **Statement B3**: a proof or a counterexample.
5. **Where the rules enter.** A list of every place in your argument where each of these is handled: checks; the e.p.
   right; stalemate in P versus no-move-loses in sums; promotions as terminals; terminals of T; loopy T and infinite
   play; draws.
6. **The weakest step** of your own argument, and why.

If a statement is false or needs a hypothesis, give the smallest counterexample you can, the repaired statement, and a
proof of the repaired statement.

Computation is optional. If you use any (for example a small program on abstract groups and small D-games), write it
yourself in `kings/delegate/out/K61/`, label its results COMPUTED-1, and give the exact reproduce command. Do not run any
existing solver of the repository.

Then write `REPORT.md`. Its first section is a short summary: one line each for A0, A, B, B3, and your recommended label
for each. Then the readings, the list of item 5 in brief, and the weakest step. Label every claim **PROVED**,
**CHECKED-2**, **COMPUTED-1** or **CONJECTURE**.

## Rules

`delegate/COMMON.md`, rules 5 and 7. Light computation only (minutes, under 1 GB). No file over 50 MB; no installs, no
network. Never use pkill, killall, `kill -- -1` or any pattern kill. Delete binaries at the end. The repository is
public: no personal data, relative paths only.
