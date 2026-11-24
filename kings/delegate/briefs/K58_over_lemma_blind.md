# K58: blind proof of Proposition 4.14 (over ≥ 0 in D-sums) and Lemma 4.15 (an exact over group with (B1) has the results of over)

**Output directory:** `kings/delegate/out/K58/` (create it if it does not exist). Write only there. Do **not** edit any
existing file. Do not run git.

Two statements about the value over in sums with decisive terminals are proposed for the theory note. You are an
independent check from outside the vendor that proposed them, and you see the statements only. Everything you need is
in this file. Prove each statement, or refute it with a concrete counterexample.

**Read only:** this file; `kings/SPEC.md` (the move rules of king-and-pawn chess on flat and cylinder boards); and
`delegate/COMMON.md`, rules 5 and 7 only (ignore its "Read first" list). **Do not open**, at any time during this task:
`kings/theory/`, `kings/delegate/out/` other than `kings/delegate/out/K58/`, `kings/delegate/briefs/` other than this
file, `notes/`, `RESULTS.md`, `RESEARCH_PLAN.md`, `paper/`, `dist/`, or the git history. They contain material on these
statements that would make your check not blind.

## 1. Definitions (from `kings/theory/LOOPY.md`, quoted or tightly paraphrased)

### 1.1 D-games, play, results (Definitions 1.1 and 1.2)

**Definition 1.1 (D-game).** A *D-game* is a finite set X of positions with, for each x ∈ X, finite option sets L(x)
and R(x) contained in X ∪ {⊕, ⊖}.
- ⊕ is the terminal "White has won". ⊖ is the terminal "Black has won".
- The D-game is *short* if the directed graph of moves on X is acyclic, and *loopy* otherwise.
- ∅ denotes a position with no options.

White = Left (options L), Black = Right (options R). A *finite D-game* is a D-game in this sense (finitely many
positions); it may be short or loopy, and it may have terminals or none. A move of Black to ⊕ (or of White to ⊖) is
allowed by the definition; it is a suicide.

**Definition 1.2 (play and results).**
- Play alternates from (x, s), where s is the player to move.
- A move to ⊕ or ⊖ ends the play with that result.
- A player with no option loses (*normal play*).
- Infinite play is a draw.
- r(x, s) = W if White can force a White win in finitely many moves, L if Black can, and D otherwise.

r is written from White's point of view, and results are ordered L < D < W. On a finite game graph these values are the
least fixed point computed by retrograde analysis (KNOWN; Siegel, *Combinatorial Game Theory*, ch. VI). A short D-game
has no draws.

### 1.2 D-sums (Definition 1.3)

**Definition 1.3 (sum with chess semantics).** For D-games A₁, …, A_k, the sum A₁ ⊞ … ⊞ A_k works as follows.
- Its positions are tuples.
- A move is a move in one coordinate.
- A move to ⊕ or ⊖ in *any* coordinate ends the *whole* play. This is "the first decisive event ends the game".
- A player with no option in any coordinate loses.

Results of a sum position are r of Definition 1.2 applied to the sum. A move in a coordinate other than the one under
discussion is called a move *elsewhere*.

### 1.3 The promotion model P (Definition 1.5, the part needed)

**P(X), the promotion model.** Chess (the rules of `kings/SPEC.md`: checkmate wins, stalemate is a draw, infinite play
is a draw), except that the first promotion ends the game as a win for the promoter. Stalemate and infinite play are
still draws.

Here the pieces are kings and pawns only; the board is flat or a cylinder (files a and the last file glued), of any
width and height; en passant is on (a position carries an e.p. target square or none; the right exists only for the
opponent's very next move after a double step). "In P alone" means the P game of the pieces with nothing beside it.

### 1.4 A king-and-pawn group as a component of a D-sum (the convention of the "Value in sums" item)

A group, *as a component of a D-sum*, is the P game of its own pieces, with this convention (quoted): "a promotion is a
terminal for the promoter, a side in check may not move elsewhere, a move elsewhere clears the e.p. right, a side with
no move loses, Definition 1.2". Its moves that do not promote are therefore real moves, not terminals: a move that
loses in P alone is not replaced by a terminal. Spelled out:
- the positions of the component are king-and-pawn positions of the board (with side to move and e.p. right), as
  reachable in P;
- a promotion by a side is a move to that side's winning terminal (⊕ for White, ⊖ for Black), so it ends the whole sum;
- a side whose king is in check must move in the group (it may not move in any other component);
- a side that moves elsewhere loses any e.p. right it had in the group;
- in the sum, a side with no legal move in any component loses (so a checkmated side loses, and a side that is
  stalemated on the board but can move elsewhere is not stuck; a side stalemated on the board with no move elsewhere
  loses, although stalemate is a draw in P alone).

### 1.5 over_D, ω and 0_D (Proposition 4.6, statement only)

**over_D.** The D-game with positions ω and 0_D, with L(ω) = {0_D}, R(ω) = {ω}, and L(0_D) = R(0_D) = ∅. So Black can
pass forever at ω (ω → ω), White has one move ω → 0_D that ends Black's passing, and 0_D has no options.

**Proposition 4.6 (over with decisive terminals; statement only).** If White wins G moving second, then White wins
G ⊞ over_D with either side to move.

Since 0_D has no options for either side, r(0_D ⊞ t, s) = r(t, s) for every D-game T, position t and side s.

### 1.6 The integer −1 as a D-game

From Definition 4.1 (reservoir R_n^W: positions ρ_n, …, ρ₀ with L(ρ_i) = {ρ_{i−1}} for i ≥ 1, L(ρ₀) = ∅, no Black
options; as a CGT game it is the integer n), with colours exchanged and n = 1: **−1** is the D-game with positions ρ₁
and ρ₀, R(ρ₁) = {ρ₀}, R(ρ₀) = ∅, and no White options anywhere. Black has exactly one move in it, once.

**"x is a White win beside −1"** (x a group position with a side to move) means r(x ⊞ ρ₁, s) = W, where the group is a
component as in 1.4 and s is the side to move in x. So White wins, although Black may once move elsewhere (in −1),
subject to the rules of 1.4 (Black may not use it while in check, and using it clears Black's e.p. right). A draw is
not a White win.

### 1.7 Exact over groups (Definition 4.8, with the conditions it uses)

**Geometry (K1), (K2)** (from Lemma 3.2″): (K1) a pawn does not attack the squares of the enemy king named; (K2) the
king distance d(a, b) = max(file distance, rank distance) (cyclic file distance on a cylinder) is at least 2 between the
two kings' squares named, so the kings never touch.

**Definition 4.8 (exact under and over groups in P), as written in LOOPY.** "Let White's king shuttle on an adjacent pair
z (K1 holds) and Black's king stand on one square b0 with K1 and K2 against both z squares. Call it an *exact under
group* if, in P:
- (U1) at both White-to-move roots every non-shuttle White move loses at once (the position after it is a Black win),
  and the shuttle is legal;
- (U2) at both Black-to-move roots Black has a move that does not lose at once (a *freeze*);
- (U3) after each freeze, a position q (with the e.p. flag if the freeze is a double step), White to move has a legal
  move and every legal White move loses at once;
- (U4) the same q with Black to move (no flag): q is a legal position, Black has a legal move and every legal Black
  move loses at once. So q is a mutual zugzwang, the position 0_D of Definition 4.4. If the freezing pawn gives check,
  q with Black to move is not legal and (U4) fails.

A promotion by Black is a decisive event, not a freeze to 0: a group in which some freeze is a promotion is not exact.
The colour mirror (ranks flipped, colours swapped) is an *exact over group*. Dropping (U4) gives a *loose* under group:
after the freeze only White is in zugzwang."

**The exact over group, written out (our transcription of the colour mirror; see Reading R1).** A group of kings and
pawns on a board (no other pieces anywhere) in which Black's king shuttles on an adjacent pair z = {z₀, z₁} and White's
king stands on one square w₀, with (K1): no White pawn attacks z₀ or z₁, and no Black pawn attacks w₀; and (K2):
d(w₀, z₀) ≥ 2 and d(w₀, z₁) ≥ 2. The *roots* are the two positions with Black's king on z₀ or on z₁ (all other pieces
fixed, no e.p. right), each with either side to move: four root positions. The *shuttle* is Black's king move between
z₀ and z₁. The group is an *exact over group* if, in P alone:
- (O1) at both Black-to-move roots every non-shuttle Black move loses at once (the position after it is a White win),
  and the shuttle is legal;
- (O2) at both White-to-move roots White has a move that does not lose at once (a *freeze*);
- (O3) after each freeze, a position q (with Black's e.p. right if the freeze is a double step), Black to move has a
  legal move and every legal Black move loses at once;
- (O4) the same q with White to move (no e.p. right): q is a legal position, White has a legal move and every legal
  White move loses at once. So q is a mutual zugzwang (the position 0_D). If the freezing pawn gives check, q with
  White to move is not legal and (O4) fails.
- A promotion by White is a decisive event, not a freeze: a group in which some freeze is a promotion is not exact.

**"Loses at once."** A move of side X loses at once if the position after it, with the other side Y to move (and Y's
e.p. right if the move was a double step), is a win for Y in P alone (Definition 1.5, so stalemate there is a draw, and
a draw is not a loss). By (O2) every White move at a White-to-move root that is not a freeze loses at once, since a
freeze is by definition any move that does not lose at once, and (O3), (O4) are then required of every freeze. A root
may have several freezes, and each gives its own q.

### 1.8 "Has the results of"

A group position x (with side to move) *has the results of* a position y of a D-game if r(x ⊞ t, s) = r(y ⊞ t, s) for
every finite D-game T, every position t of T and each side s to move, with the group as a component as in 1.4. So the
roots having the results of ω means r(root ⊞ t, s) = r(ω ⊞ t, s), and q having the results of 0_D means
r(q ⊞ t, s) = r(0_D ⊞ t, s) = r(t, s).

## 2. The two statements

**Proposition 4.14 (over ≥ 0 in D-sums).** For every finite D-game T, every position t of T and each side s to move,
White does at least as well in ω ⊞ t as in 0_D ⊞ t (over_D of Proposition 4.6):
r(ω ⊞ t, s) ≥ r(0_D ⊞ t, s), in the order L < D < W.

**Lemma 4.15.** Let G be an exact over group of Definition 4.8, as the P game of its own pieces in a D-sum (Definition
1.3 with the convention of 1.4), and suppose

- **(B1)** for every non-shuttle Black move m at a root (Black to move), the position after m (White to move, with
  White's e.p. right if m is a double step) is a White win beside −1 (White wins although Black may once move
  elsewhere).

Then for every finite D-game T, loopy or short, with or without terminals, both roots have the results of ω and every q
the results of 0_D, with either side to move.

## 3. Readings to fix

LOOPY leaves the following points open or states them only by reference. Say in `PROOF.md`, at the top, which reading
you use for each; if a statement holds in one reading and fails in another, say so and give the counterexample.

- **R1 (the over group).** Definition 4.8 writes out the under group only and defines the over group as its colour
  mirror. The (O1) to (O4) and (K1), (K2) of §1.7 are our transcription. In particular we read "K1 holds" for the
  shuttling king as "no enemy pawn attacks either shuttle square", and "K1 and K2 against both z squares" for the
  other king as "no enemy pawn attacks w₀, and d(w₀, z_i) ≥ 2". Check that the transcription is the mirror.
- **R2 (roots).** LOOPY says "both roots" in Lemma 4.15 and "both White-to-move roots" in Definition 4.8. We read a
  root as one of the two placements (Black's king on z₀ or z₁), each with either side to move, and the roots as
  carrying no e.p. right.
- **R3 ("loses at once").** Definition 4.8 says "the position after it is a Black win" (mirror: a White win), "in P".
  We read this as a win in P alone, where stalemate is a draw, not in a sum, where a stalemated side may move
  elsewhere or loses. The sum convention of 1.4 differs from P alone exactly there and at checks.
- **R4 (0_D in Definition 4.8).** Definition 4.8 calls q "the position 0_D of Definition 4.4", but Definition 4.4 is the
  CGT game over = {0 | over}; 0_D is defined with over_D in Proposition 4.6. We read q "having the results of 0_D" as in
  §1.8. We read q with Black to move as carrying Black's e.p. right when the freeze was a double step, and q with White
  to move as carrying none, as (O3) and (O4) say.
- **R5 (a side in check and moves elsewhere).** "A side in check may not move elsewhere" is read as: it may not move in
  any other component, even to a terminal ⊕ or ⊖ there. In a D-sum only the group can give check.
- **R6 (who loses the e.p. right).** "A move elsewhere clears the e.p. right" is read as: the right held by the side to
  move lapses when that side moves elsewhere, as it lapses after any move of that side in chess.
- **R7 (−1).** We read "−1" as the D-game R₁ for Black of §1.6 (one Black move, no White options, no suicides).
- **R8 (the class of T).** "Every finite D-game T" is read as Definition 1.1 with no further restriction: T may be
  loopy, may contain ⊕ and ⊖ as options of either side (suicides included), may have positions with no options, and
  every position t of T is allowed as a start.
- **R9 (the board).** Definition 4.8 does not fix the board. We read the statements as holding for every exact over
  group on any flat or cylinder board (the SPEC.md bound of at most 8 files belongs to the solvers, not to P), with
  nothing but the group's pieces on the board.
- **R10 (the start of a q).** Lemma 4.15 speaks of "every q, with either side to move". We read this as both positions
  of (O3) and (O4) as starting positions of the sum, not only as positions reached from a root by a freeze.

## 4. Phase 1 (the only phase): prove or refute, blind

Write `PROOF.md`, your own complete argument, in this order.

1. **Readings.** Your choice for R1 to R10, and any further ambiguity you find (state it and your choice).
2. **Proposition 4.14.** A complete proof, or a concrete counterexample: an explicit finite D-game T (positions and
   option sets), a position t and a side s with r(ω ⊞ t, s) < r(0_D ⊞ t, s). Cover loopy T, draws and terminals of T.
3. **Lemma 4.15.** A complete proof, or a concrete counterexample: an explicit exact over group that satisfies (B1) on
   a named board (or, if you work abstractly, an explicit abstract game that models one, stating exactly which features
   of chess it omits), together with T, t, s and the result that differs. Cover all four roots and every q, both sides
   to move, and the three results W, D, L (not only wins).
4. **Where the chess rules enter.** An explicit list of every place in your argument where each of these is handled:
   checks (and the rule that a side in check may not move elsewhere); the e.p. right (at the roots, after a double
   step, after a move elsewhere, in q and in (B1)); stalemate (a draw in P alone, a loss in a sum, and the difference
   between "loses at once" in P alone and losing in the sum); promotions as terminals; terminals of T (⊕ and ⊖ reached
   by either side, suicides included); loopy T and infinite play; draws.
5. **The weakest step.** Name the single step of your own argument you trust least, and why.
6. **Are the hypotheses right?** Answer each with an argument or an explicit example:
   - (a) Is (B1) needed at all? Either show that Lemma 4.15 holds for every exact over group without (B1), or give an
     exact over group (or an abstract model of one, as in item 3) that fails (B1) and does not have the results of over.
   - (b) Is any condition missing on White's side, that is, about White's non-freeze moves at the roots, which Definition
     4.8 only requires to lose at once in P alone?
   - (c) Is any condition missing at the q positions, whose moves Definition 4.8 only requires to lose at once in P
     alone?
   - (d) Does the conclusion need any reading of §3 in an essential way (would it fail under another reading)?

If either statement is false or needs a hypothesis, give the smallest counterexample you can and the repaired
statement, and prove the repaired statement.

Computation is optional. If you use any (for example a small program on abstract toy groups and small D-games), write it
yourself in `kings/delegate/out/K58/`, label its results COMPUTED-1, and give the exact reproduce command. Do not run
any existing solver of the repository.

Then write `REPORT.md`. Its first section is a 5-line summary of what you established: one line each for Proposition
4.14, Lemma 4.15, the role of (B1), conditions on White's side and at the q's, and your recommended label for each
statement. Then the readings you chose, the list of item 4 in brief, the weakest step, and the answers to item 6. Label
every claim **PROVED**, **CHECKED-2**, **COMPUTED-1** or **CONJECTURE**.

## Rules

`delegate/COMMON.md`, rules 5 and 7. Light computation only (minutes, under 1 GB). No file over 50 MB; no installs, no
network. Never use pkill, killall, `kill -- -1` or any pattern kill. Delete binaries at the end. The repository is
public: no personal data, relative paths only.
