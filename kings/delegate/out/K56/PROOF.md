# K56 proof: a local criterion that forces the results of over in every D-sum

AI work (one agent), no human re-derivation. Refereed by a second agent (`VERIFY.md`): every step of the main proof
(Lemma 2) is sound. Labels as in LOOPY: PROVED means a complete hand proof below.

Erratum (referee, 2026-11-23): the monotonicity claim in §1 (Att^X_∞ ⊆ Att^X_1 ⊆ Att^X_0, "more passes only help X")
is false: a side with a pass left must pass where a side with none is stalemated, a draw (`verify/src/mono.py`). The
main proof never uses it. The sentence "pass-robust exact ⇒ tempo-exact" in §2 rests on it and is withdrawn;
pass-robust exactness is still sufficient, by the same proof with an unlimited budget for both sides. The ranks for
different pass budgets are to be read in one game whose states record the passes left, as §1 says.

## 0. Summary

- The brief's criterion ("pass-robust exact": every move that loses at once in Definition 4.8 still loses when the
  mover may pass as often as he likes) is **sufficient** for the results of over beside every finite D-game, terminals
  allowed (Lemma 2 below, PROVED). But it is much stronger than needed.
- The proof shows exactly how many passes each kind of move must survive. A Black move at q, and a White move at q,
  need **no** pass (Definition 4.8 already gives this). A Black move at a root needs **one** Black pass. A White
  non-freeze move at a root needs either **unlimited** White passes, or **zero** passes after a Black pass in reply.
  This weaker criterion ("tempo-exact", Definition 1) is also sufficient (Lemma 2, PROVED). It is the weakest
  criterion this proof method gives.
- Two-sided passes ("the winner may pass too") give the same condition as one-sided passes (Remark 4). Draws need no
  separate treatment (Lemma 2 transfers non-losing strategies as well as winning ones). Test games with terminals
  are covered.
- Part A (findings.txt): none of the nine groups is pass-robust or tempo-exact. In every group the White side fails:
  some White non-freeze move at a root is saved by one White pass, or by unlimited passes, and is not lost after a
  Black pass. In Z_O and its two flat translates the Black side fails too (1…e5–e4 at the d4 root is saved by one
  Black pass), which is the mechanism K47 found. In the 2 + 3 group the Black side passes.
- So the lemma does not decide whether the 2 + 3 group is over. What is missing is named in §5.

## 1. Setting and definitions

**The sum.** As in K47 and K55: G is the P game of the group's own pieces (Definition 1.5) as a component of a D-sum
(Definition 1.3) with K40's convention. A state of G ⊞ T is (g, t, s): g a board of G with its e.p. right, t a
position of T, s the side to move. The mover plays one legal move in G, or one option in T. A promotion in G ends the
play as a win for the promoter; a move to the terminal ⊕ (⊖) of T ends it as a White (Black) win, whoever makes it.
A side in check in G may not move in T. A move in T clears the e.p. right in G. A side with no legal move in either
component loses (in G alone a stalemate is a draw of P; in the sum it is a loss only if the side has no move in T
either). Infinite play is a draw. r(·) is the least fixed point of Definition 1.2. over_D has positions ω and 0_D,
L(ω) = {0_D}, R(ω) = {ω}, 0_D has no options (Proposition 4.6). T is any finite D-game (Definition 1.1): loopy or
short, with or without terminals.

KNOWN facts used (finite game graphs, least fixed point): (K-a) r(state) = W iff White has a strategy that wins every
play within a bounded number of moves; (K-b) r(state) ≠ L iff White has a strategy against which no play ends in a
Black win (stay outside Black's attractor); the same for Black. Both are standard ([S] ch. VI; LOOPY Definition 1.2).

**Pass games.** For a colour X, Y the other colour and k ∈ {0, 1, 2, …} ∪ {∞}: P^X_k is P on the group's pieces in
which X may pass at most k times (k = ∞: any number of times). A pass is allowed only when X is not in check; it
leaves the board unchanged, gives the move to Y and clears the e.p. right. Y never passes. A promotion wins for the
promoter, checkmate loses, a side with no legal move and no pass allowed is stalemated (a draw), infinite play is a
draw. Att^X_k ⊆ {states} is the set of states (board, e.p. right, side to move, passes left) that Y wins in P^X_k; we
write (g, s) ∈ Att^X_k for "with k passes left". Att^X_0 = "Y wins in P alone". For each state of Att^X_k Y has a
positional strategy with a rank ρ ∈ ℕ that drops by at least 1 at each move of either side (KNOWN, attractor ranks).
Monotonicity: Att^X_∞ ⊆ … ⊆ Att^X_1 ⊆ Att^X_0 (more passes only help X).

Two closure facts, both immediate from the definition of the attractor:
- (P1) If (g, X, k passes left) ∈ Att^X_k and X is not in check, then (g, Y, no e.p. right, k − 1 left) ∈ Att^X_{k−1}
  (the pass is one of X's options; for k = ∞, k − 1 = ∞), with smaller rank.
- (P2) If (g, X, with an e.p. right) ∈ Att^X_k then (g, X, no e.p. right) ∈ Att^X_k with rank not larger: X's
  options without the right are a subset of those with it and lead to the same states; if the subset is empty, X is
  either in check (checkmated: Y wins) or not in check (then X may pass if k ≥ 1, an option already counted; if k = 0
  this is a stalemate, see the next paragraph).

*Stalemate.* The edge case of (P2) with k = 0 (X's only moves are e.p. captures, and the right is lost by a move
elsewhere) is the only place where the pass game's "stalemate is a draw" and the sum's "no move loses" differ in a
way that matters. We never need Att^X_0 at such a state: see the "b-safe" invariant in §3, which asks only that X's
G-moves lead into Y's set and is preserved by losing the right.

**Over groups (Definition 4.8, over orientation).** Black's king shuttles between z0 and z1, White's king stands on a
fixed square; roots A, B (Black king on z0, z1), each with either side to move, no e.p. right. A *freeze* is a White
move at a root that does not lose at once in P; its position is q (Black to move, with Black's e.p. right if the
freeze is a double step), and (O1) to (O4) hold. R = {A, B} ∪ {all q} (q with or without the right; with either side
to move), φ(A) = φ(B) = ω, φ(q) = 0_D.

**Definition 1 (tempo-exact over group; K56).** An exact over group (Definition 4.8) is *tempo-exact* if:
- (T1) no king is in check at A, B or any q, with either side to move;
- (T2) for every non-shuttle Black move m at a root, with x the position after it (White to move): either
  (N1) (x, W) ∈ Att^B_1 (White wins although Black may still pass once), or
  (V1) White is not in check in x and (x, B, no right) ∈ Att^B_1 (Black's move, then a White pass, still loses for
  Black, even with one Black pass left);
- (T3) for every non-freeze White move m at a root, with x the position after it (Black to move): either
  (N∞) (x, B) ∈ Att^W_∞ (Black wins although White may pass at will), or
  (V0) Black is not in check in x and (x, W, no right) ∈ Att^W_0 (White's move, then a Black pass, still loses for
  White in P alone).
Nothing beyond Definition 4.8 is asked at q.

(T1) already follows from Definition 4.8 with K1, K2 (pawns do not attack the king squares of the roots, the kings
are two apart, and (O4) makes q with White to move legal, so the freezing pawn does not check); the program checks it.

**Definition 1′ (pass-robust exact, the brief's form).** Every move that Definition 4.8 requires to lose at once
(non-shuttle Black moves and non-freeze White moves at the roots, every move at every q) loses in P^X_∞, X the mover.
Pass-robust exact ⇒ tempo-exact: Att^X_∞ ⊆ Att^X_1 ⊆ Att^X_0 gives (N1), (N∞) and the q-conditions.

## 2. The lemma

**Lemma 2 (K56). PROVED.** Let G be a tempo-exact over group. For every finite D-game T (terminals allowed), every
position t of T, each root x ∈ {A, B}, each q, and each side s:
  r(x ⊞ t, s) = r(ω ⊞ t, s)  and  r(q ⊞ t, s) = r(0_D ⊞ t, s) = r(t, s).
In particular this holds for pass-robust exact groups.

*Reduction.* By (K-a), (K-b) it suffices to prove, for each colour Y:
(★) if Y has a strategy S in over_D ⊞ T from (φ(g0), t0, s0) that wins (resp. does not lose), then Y has a strategy
in G ⊞ T from (g0, t0, s0) that wins (resp. does not lose).
Indeed: if r(over) = W, (★) for Y = White gives r(G) = W. If r(over) = L, the same for Black. If r(over) = D, both
colours have non-losing strategies in over ⊞ T, so by (★) both have them in G ⊞ T, and r(G) = D.

Fix Y and S, X the other colour. Y's strategy in G ⊞ T keeps a *virtual* state (o, t, s) of over_D ⊞ T that is
reached from (φ(g0), t0, s0) by a play consistent with S; the T-coordinate and the side to move of the real and
virtual states are always equal at the moments named below. There are two phases.

## 3. The proof of (★)

**Phase 1 (mirror).** Invariant M: g ∈ R, o = φ(g), real T-position = virtual T-position, same side to move.
- *Y to move.* S names a move. A T-move: play it in T (legal: Y is not in check, (T1)). The over-move ω → 0_D (Y =
  White, g a root): play a freeze of g (each root has one by (O2); it is not a promotion; the new g is a q). The
  over-move ω → ω (Y = Black, g a root): play the shuttle (legal by (O1); it captures nothing, so the new g is the
  other root). In each case M holds again. 0_D has no options, so S never names an over-move at a q.
- *X to move, X moves in T.* The same move is legal in the virtual state (over has no checks): copy it. M holds.
  If it is a move to a terminal, both plays end with the same result (and it is not X's terminal unless S loses).
- *X to move, X plays the shuttle (X = Black at a root) or a freeze (X = White at a root).* These are X's over-moves
  ω → ω and ω → 0_D: copy them virtually. M holds.
- *X to move, X makes any other G-move m.* By Definition 4.8 every such m loses at once; go to phase 2 (entry).
- *X has no legal move in G ⊞ T.* Then X loses: good for Y. (If X has no move in the virtual state but has G-moves in
  the real one, they are moves of the previous item.)

**Budget.** In phase 2 the virtual over-position o decides how often Y may later have to make an unforced G-move:
b(White, ω) = 1, b(Black, ω) = ∞, b(·, 0_D) = 0. Reason: an unforced G-move by Y happens only when S names an
over-move for Y; White's only over-move is ω → 0_D, once, after which o = 0_D has no options; Black's is ω → ω, which
S may name any number of times; at 0_D S names none. (X's over-moves are never copied in phase 2, so o changes only
by Y's own over-moves.)

**b-safe.** A real state (g, X to move) is *b-safe* if every X G-move from it leads to a state (g′, Y) ∈ Att^X_b
(b passes left) and, in case b ≥ 1 and X is not in check, (g, Y, no right) ∈ Att^X_{b−1}. Any (g, X) ∈ Att^X_b
is b-safe ((P1) and the definition of the attractor). If (g, X, right) is b-safe so is (g, X, no right) (fewer X
G-moves, same pass target). This is the only property of X-to-move states used below.

**Phase 2 (hybrid).** Data: the real G-state, the virtual (o, t), b = b(Y, o). Invariant H, checked whenever X is to
move in G ⊞ T: the virtual state has X to move with the same t and is S-consistent, and the real (g, X) is b-safe.

*Entry.* X has just played m from g ∈ R (virtual (o, t, X to move), o = φ(g)); x = the position after m, Y to move.
Two ways in, matching (N) and (V) of Definition 1, and the trivial ones at q:
- (N) Y answers m in G with its strategy from (x, Y) ∈ Att^X_b, b = b(Y, o). This needs (x, Y) ∈ Att^X_b:
  for m a Black move at a root, b(White, ω) = 1: this is (N1); for a White move at a root, b(Black, ω) = ∞: (N∞);
  for any move at a q, b = 0: this is "m loses at once", i.e. (O3)/(O4) of Definition 4.8. After Y's answer
  (g′, X) ∈ Att^X_b, so it is b-safe; the virtual state is unchanged (X to move): H holds. (m and the answer form a
  "null round" of the virtual play.)
- (V) X's move m is copied virtually as X's over-move o → o′ (X = Black: ω → ω; X = White: ω → 0_D; at a q there is
  none, so (V) is not used there). Now the virtual state is (o′, t, Y to move), the real one (x, Y to move), and
  b = b(Y, o′). Y follows S from the virtual state:
  - S names a T-move: Y plays it in T (legal: Y is not in check in x, by the hypotheses of (V1), (V0)). Now X is to
    move and the real G-state is (x, X, no right). For X = Black (V1): b(White, ω) = 1 and (x, B, no right) ∈ Att^B_1,
    so it is 1-safe. For X = White (V0): b(Black, 0_D) = 0 and (x, W, no right) ∈ Att^W_0, so it is 0-safe. H holds.
  - S names an over-move. For X = White, o′ = 0_D and Black has none. For X = Black, o′ = ω and S may name White's
    ω → 0_D: White must move in G from (x, W). By (V1) and (P1) (Black is not in check in x, since Black just moved),
    (x, W, no right) ∈ Att^B_0; White's moves from (x, W) include those from (x, W, no right) and lead to the same
    states, so White plays its Att^B_0 move. The virtual state becomes (0_D, t, X to move), b = 0, and the real
    (g′, B) ∈ Att^B_0 is 0-safe. H holds.

*Steps, with H holding and X to move.*
- (a) X moves in G, g → g′. By b-safety (g′, Y) ∈ Att^X_b; Y answers with its Att^X_b strategy, to (g″, X) ∈ Att^X_b,
  which is b-safe; the virtual state is unchanged. (A null round. If the answer is a promotion or mates, Y wins.)
  If m gave check, the answer is a G-move anyway, as required.
- (b) X moves in T (not in check, else not allowed). Copy it virtually; both states have Y to move with the same t
  (or the play has ended at a terminal, with the same result in both). The real G-state is (g, Y, no right).
  - If S names a T-move, Y plays it (Y is not in check: the G-board has not changed since Y's last move or since the
    entry, and Y's own move cannot leave Y in check; at entry (V) assumed it). Real (g, X, no right): b-safe, because
    (g, X) was b-safe and losing the right keeps b-safety. H holds. (A "pause": Y spends no G-tempo.)
  - If S names an over-move (only possible while o = ω, i.e. b ≥ 1): by b-safety and X not in check,
    (g, Y, no right) ∈ Att^X_{b−1}; Y plays its strategy move there, to (g′, X) ∈ Att^X_{b−1}. For Y = White the
    virtual move is ω → 0_D and the new budget b(White, 0_D) = 0 = b − 1. For Y = Black it is ω → ω and the budget
    stays ∞ = ∞ − 1. In both cases (g′, X) is b-safe for the new b. H holds.
- (c) X has no legal move in G ⊞ T: X loses.

*Termination and result.* For a b-safe state (g, X) let μ be the largest attractor rank among the states its
conditions name ((g′, Y) ∈ Att^X_b for X's G-moves, and (g, Y, no right) ∈ Att^X_{b−1}). Step (a) replaces it by a
b-safe (g″, X) ∈ Att^X_b whose successors have rank < rank(g″, X) < rank(g′, Y) ≤ μ; an unforced Y move in step
(b) either lowers b (Y = White) or, for b = ∞, gives (g′, X) with all successor ranks below rank(g, Y, no right) ≤ μ;
a pause does not raise μ (the loss of the e.p. right removes X moves only). So (b, μ) falls lexicographically at
every G-move of phase 2, and phase 2 contains finitely many G-moves. Every other
move of the real play is a T-move that is also a move of the virtual play, and so is every virtual over-move made in
phase 2. Hence:
- if the real play is infinite, the virtual play is infinite after finitely many steps of phase 2, or the real play
  never leaves phase 1 and the virtual play is the same play with ω/0_D in place of R; either way the virtual play is
  an infinite S-consistent play;
- if the real play ends, it ends by a promotion in G (only Y's: X's G-moves go from b-safe states into Y's attractor,
  which contains no state where X can promote, and in phase 1 the only X G-moves are the shuttle, the freeze and moves
  of the entry), by a terminal of T (also reached by the virtual play), or by a side without a legal move. Y always
  has a move: in phase 1 by M, in phase 2 by the Att strategy or by S (if S had no move, Y would lose the virtual play
  at once, against "S does not lose"). X without a move loses.
If S wins, every S-consistent play ends finitely in a Y win, so the virtual play cannot be infinite and cannot end in
X's terminal; so the real play is finite and is a Y win, and its length is bounded (the virtual part by S's rank, the
G-moves of phase 2 by the attractor rank), which is (K-a). If S only does not lose, an infinite real play is a draw
and a finite one is a Y win. This proves (★), and Lemma 2. ∎

The statement for q: start in phase 1 with g = q, o = 0_D; the same proof applies (only the q-conditions are used
until the play reaches a root, which it can only do through X's moves at q, all of which enter phase 2).

## 4. Points the brief asked to settle

- **Draws on both sides.** Handled by (★) for non-losing strategies; no separate argument. Example: over ⊞ off is a
  Black win (White has one move, ω → 0_D, then none); over ⊞ dud is a draw; Lemma 2 gives the same for G.
- **A winner who must answer a check.** Y answers every X G-move in G (step (a)), so a check is always answered on
  the board; Y moves in T only after X moved in T, when Y is not in check; the (V) entries assume Y not in check.
- **The two roots having different freezes.** Irrelevant: φ maps every q to 0_D, and the proof uses only "some freeze
  exists at each root" and the conditions at each q.
- **Free passes for the mover, or for both sides?** For the attractor of Y it makes no difference (Remark 4). What
  matters is *how many* passes, and that depends on the kind of move (budget b): 0 at q, 1 for Black at a root, ∞ (or
  the (V0) alternative) for White at a root. The brief's "unlimited passes for every move" is sufficient and far too
  strong: it fails for the 2 + 3 group already at q and at Black's root moves, where Lemma 2 needs nothing (q) or one
  pass (roots), and where the K55 referee observed draws against off, which are harmless.
- **Test games with terminals.** Covered: X's T-moves are always answered by S in T (pauses), so a race in T is
  conducted as in over ⊞ T; Y never has to leave T unattended except for finitely many G-moves that answer X's own
  G-moves (null rounds) or that S itself asked for.

**Remark 4 (two-sided passes, unlimited). PROVED.** If in P^X_∞ Y may also pass (whenever not in check), Y's
winning set is unchanged. Proof: induction on the rank of Y's winning strategy in the two-sided game. If at (g, Y)
the strategy passes, X is not in check in the resulting (g, X, no right) (in a state with Y to move, X's king is not
attacked), so X may pass back, reaching (g, Y, no right) with smaller rank. By induction Y wins there without ever
passing; its first move there is also legal at (g, Y) (the e.p. right only adds moves) and leads to the same state.
If the strategy does not pass at (g, Y), apply the induction to each reply of X. ∎
For finite k the two games can differ (with k = 0, a Y pass may put X in zugzwang). Lemma 2 needs only the one-sided
games. In the sum the asymmetry is real: Y's T-moves are not free, which is why the proof lets Y move in T only as S's
answer to an X move in T.

**Remark 5 (what is not claimed).** Tempo-exactness is sufficient, not necessary. In particular nothing here says
that a group failing (T3) differs from over in some sum.

## 5. Why the lemma does not settle the 2 + 3 group, and what is missing

In the 2 + 3 group (cyl:10×6) (T1), (T2) and the q-conditions hold, but (T3) fails at five White root moves
(Kg4–f3 at both roots, e2–e4 at the f6 root, e2–e3 and Kg4–g3 at the g6 root): each is saved by one White pass
(Kg4–g3: only by unlimited passes, a draw) and is not lost after a Black pass in reply (V0 fails). The step that
breaks is the budget of Black: after White's bad move and Black's answer, S may ask Black for the over-pass ω → ω any
number of times, and each such request must be met by a Black G-move that keeps Black's win; against a White who
passes, Black cannot always find one. Two ways to close the gap, neither done here:
- show that against over ⊞ T Black never needs ω → ω more than once after White has declined to freeze (then (T3)
  would need only (x, B) ∈ Att^W_1, which may hold); or
- map White's bad move to a third over-like position (an "over with a debt"), which needs a value for the position
  after the move, i.e. a comparison of loopy D-games that §3 of LOOPY does not provide.
The 2 + 3 group's failures at White's side are therefore a gap of the proof method, not evidence against equality;
the D-sum computations in findings.txt (sec. 3) found no test game separating it from over.
