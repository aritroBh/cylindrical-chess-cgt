# K64: blind proof of a bound on the test ladder and of "no finite test family"

**Output directory:** `kings/delegate/out/K64/` (create it if it does not exist). Write only there. Do **not** edit any
existing file. Do not run git.

Two statements about exact over groups in sums with decisive terminals are proposed for the theory note. You are an
independent check from outside the vendor that proposed them, and you see the statements only. Everything you need is
in this file. Prove each statement, or refute it with a concrete counterexample.

**Read only:** this file; and `delegate/COMMON.md`, rules 5 and 7 only (ignore its "Read first" list). **Do not open**,
at any time during this task: `kings/theory/`, `kings/delegate/out/` other than `kings/delegate/out/K64/`,
`kings/delegate/briefs/` other than this file, `kings/REPORT.md`, `kings/CHECKLIST.md`, `notes/`, `RESULTS.md`,
`RESEARCH_PLAN.md`, `paper/`, `dist/`, or the git history. They contain material on these statements that would make
your check not blind.

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

### 1.7 Conventions and facts you may use without proof

- **The e.p. rule.** A right only adds moves: every move of s that is legal at (g, no right, s) is legal at
  (g, right, s) and has the same result.
- **−1** is the D-game with positions a, 0′: R(a) = {0′}, L(a) = ∅, 0′ without options (one Black token).
- **Fact A0.** For every exact over group every q-state has the results of 0_D, and r(ρ ⊞ t, s) ≤ r(ω ⊞ t, s) for both
  roots, every finite D-game T, position t and side s.
- **Fact A.** G has the results of ω beside every finite D-game iff **(C)**: for every bad Black move m, every finite
  D-game T and every position t, r(x_m ⊞ t, White to move) ≥ r(ω ⊞ t, Black to move). This holds game by game: G has
  the results of ω beside a given T iff (C) holds for that T.
- **Fact B.** For a bad Black move m these are equivalent: (C) holds at m; White wins Aux(x_m);
  r(x_m ⊞ u_0, White to move) = W in T_N for every N ≥ 0; the same for some N ≥ K, K the number of states of G.

## 2. The statements

**Statement D (a shorter ladder).** Let G be an exact over group with b boards, m a bad Black move, x = x_m. Let Z(x)
be the set of states reachable from x by group moves of either side and by White passes (a pass: at a state with White
to move and not in check, to the same board with Black to move and no right). Let P(x) be the set of boards g at which
some White-to-move state of Z(x) has White not in check, and E(x) ⊆ P(x) the boards g at which every such state is a
White win beside −1 (the group ⊞ −1 from that state and a, White to move, under the sum's rule).

- (D1) (C) holds at m iff r(x ⊞ u_0, White to move) = W in T_N for N = |P(x) \ E(x)|.
- (D2) |P(x) \ E(x)| ≤ b, and ≤ b − 1 if no e.p. move of White promotes.
- (D3) So G has the results of ω beside every finite D-game iff r(ρ ⊞ u_0, Black to move) = W in T_b for both roots ρ.

**Statement E (no finite test family).** For N ≥ 1 let Λ_N be the group with boards A, B, q, p, e, c_1, …, c_N, no
checks, no double steps and no e.p. moves, and exactly these moves. White: A → q, B → q, q → e, c_i → q (every i),
e → p, and a promotion at p. Black: A → B, B → A (the shuttle), A → c_1, q → p, c_i → c_{i+1} (i < N), c_N → e, a
promotion at e, and p → e. Let C_N be the D-game with positions 0, 1, …, N, L(i) = {i − 1} and R(i) = {0} for i ≥ 1,
and 0 without options.

- (E0) Λ_N is an exact over group with roots A, B and one freeze board q.
- (E1) Λ_N has the results of ω beside every finite D-game with at most N positions.
- (E2) Λ_N does not have the results of ω beside C_N (N + 1 positions), nor beside T_{N+1}: give the position, the side
  to move and both results.
- (E3) Hence no finite set of finite D-games, and no single finite D-game (short or loopy), decides "has the results of
  ω beside every finite D-game" for every exact over group.

## 3. Readings to fix

Say in `PROOF.md`, at the top, which reading you use for each point; if a statement holds in one reading and fails in
another, say so and give the counterexample.

- **R1 (side to move).** Check the side to move in every comparison, and that a pass leaves Black to move with no right.
- **R2 (no move loses, stalemate).** "Loses at once" in 1.5 is judged in P alone (stalemate a draw); everything in a
  sum, in Aux, beside −1 and in T_N uses the sum's rule (a side with no move anywhere loses).
- **R3 (checks).** A side in check may not move elsewhere (pass, freeze, move in T or in −1).
- **R4 (e.p. right).** The right belongs to the side to move, lapses after any move of that side, and only adds moves.
- **R5 (draws).** r has three values, L < D < W.
- **R6 (the class of T in E1).** Every finite D-game with at most N positions: loopy or short, terminals for either
  side (suicides included), every position a start, both sides to move; roots and q-states as in 1.5.
- **R7 (promotions in 1.5).** (O1)–(O4) forbid promotions only at the states they name. If a statement depends on
  whether promotions are also forbidden at other states of a root board or a q-board, say so.

## 4. Task

Write `PROOF.md`, your own complete argument, in this order: the readings; Statement D (D1, D2, D3), with a proof or a
concrete counterexample (an explicit group, bad move and N), and, if D holds, whether the bounds of D2 can be attained;
Statement E (E0 to E3), with a proof or a counterexample (for E1: an explicit D-game with at most N positions, a
position and a side); a list of where checks, the e.p. right, stalemate against no-move-loses, promotions, terminals of
T, loopy T and draws enter; and the weakest step of your own argument.

If a statement is false or needs a hypothesis, give the smallest counterexample you can, the repaired statement, and a
proof of the repaired statement.

Computation is optional. If you use any, write it yourself in `kings/delegate/out/K64/`, label its results COMPUTED-1,
and give the exact reproduce command. Do not run any existing solver of the repository.

Then write `REPORT.md`: one line each for D1, D2, D3, E0, E1, E2, E3 with your recommended label; the readings; the
weakest step. Label every claim **PROVED**, **CHECKED-2**, **COMPUTED-1** or **CONJECTURE**.

## Rules

`delegate/COMMON.md`, rules 5 and 7. Light computation only (minutes, under 1 GB). No file over 50 MB; no installs, no
network. Never use pkill, killall, `kill -- -1` or any pattern kill. Delete binaries at the end. The repository is
public: no personal data, relative paths only.
