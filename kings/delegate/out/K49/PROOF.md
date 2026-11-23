# K49: the ON class of K+P v K on the cylinder (LOOPY §8 item 5)

Not refereed. One agent (K49). Labels as in the brief: PROVED means a hand proof given here. A statement whose proof
uses a fact that was only computed carries that fact's label, and the text says which step is computed.

## 0. Setting and notation

x is a K+P v K position on cyl:W×H in the P model (K40 `PROOF.md`): a promotion is ⊕, Kxp leaves K v K, which is dead
(K40 Lemma 1). T is a finite terminal-free test game (no option of T is ⊕ or ⊖). x ⊞ T is the sum of LOOPY Definition 1.3
with the chess rule that a side in check may not move in T. Only Black can be in check (by the pawn). Convention **(N)**
throughout: a side with no move loses; infinite play is a draw. W ≠ 4 throughout, so White always has a king move
(K40 Lemma 2) and Black never wins any x ⊞ T (K40 Corollary 3).

For a placement y (the three squares) write y_w and y_b for y with White and with Black to move (y_w is legal iff Black is not
in check). Write

- **W_N** for the set of (y, s) that White wins in the bare game x ⊞ 0 under (N). Let ρ(y, s) be the stage at which (y, s)
  enters W_N (least fixed point, LOOPY Definition 1.2). At a White-to-move position of stage ρ White has a move that promotes or
  reaches stage < ρ; at a Black-to-move position of stage ρ every Black move reaches stage < ρ, Kxp is not available, and
  Black has no move only if ρ = 1 (Black stuck: stalemated or mated, a loss under (N)).
- **P_L** = W(x ⊞ dud) = W(x ⊞ off) (LOOPY Theorem 3.11; K40 Proposition 4 checks that its proof survives the check rule).
- For a test game T: **(t, L) ∈ ON_T** iff Left wins on ⊞ T at T-position t with Left to move; **(t, R) ∈ ON_T** likewise with
  Right to move. In on ⊞ T Left may always pass and Right has only his T-moves, so Left wins iff she can force Right to be
  without a T-move. (t, R) ∈ ON_T ⇒ (t, L) ∈ ON_T (Left passes). Left's options at (t, L) are the pass, to (t, R), and her
  T-moves t → t′, to (t′, R); so (t, L) ∈ ON_T iff (t, R) ∈ ON_T or (t′, R) ∈ ON_T for some Left option t′.
- K40's three classes under (N): DEC (W against every test), ON (the signature of on: W against every test except off and dud,
  D against those two) and DUD (D against every test). The tests are the integers −12…12, on, off, dud, over, under, \*, ↑,
  ↓, ±1 and on + \*.

## 1. The one computed fact: no reciprocal zugzwang

**Lemma P (no reciprocal zugzwang under (N)).** For every placement y with Black not in check: if y_b ∈ W_N then y_w ∈ W_N.
Equivalently (contrapositive): if White to move does not win, Black to move does not win either.

Status:
- **CHECKED-2 on cyl:W×H, W ∈ {3, 5, 6, 7, 8}, H ∈ {6, 8}.** It is equivalent to a column of K40's tables: in y_b ⊞ (−1) one
  of Black's options is the pass to y_w ⊞ 0, so "every W_N position with Black to move also wins against −1" (true in K40's
  tables, which are CHECKED-2 against the K40 referee's `vsum`) gives Lemma P. K49's own solver `scripts/kn.c` (written from
  SPEC.md and LOOPY Definitions 1.2, 1.3, 1.5 only) reproduces all of K40's (N) and (C) tables, 0 differing rows of 34 results
  on all 12 boards (`logs/cmp40.log`), and checks Lemma P directly (`scripts/passclose.py`).
- **COMPUTED-1 (kn.c only) on every cyl:W×H with W ∈ {3, 5, 6, 7, 8, 9, 10} and 4 ≤ H ≤ 10**: 0 violations (`logs/passclose.log`).
- **False on 4 files**: 8, 8, 12, 16, 20, 24, 28 violations on cyl:4×4 … cyl:4×10. This is the source of the 4-file anomalies
  of K40 (finite thresholds; White can be stalemated in front of the pawn).
- **PROVED for the pawn on rank H−1** (Proposition 6 below gives the classes there by hand; Lemma P is read off from it).
- No hand proof for lower pawn ranks. That is the gap of this report.

**Lemma P′ (the one-spare reduction). PROVED.** Lemma P holds on a board iff W(x ⊞ (−1)) = W(x ⊞ 0) at every Black-to-move
position not in check. (⇒ is Theorem 1 below with k = 1; ⇐ is the remark above.) So "Black's spares never help" is decided
by one spare.

## 2. Spare tempi (integers)

**Theorem 1 (Black's spares never help, White needs none).** Assume Lemma P on the board. For every (x, s) and every integer n:
W(x ⊞ n, s) ⟺ (x, s) ∈ W_N.

*Status:* PROVED given Lemma P; hence CHECKED-2 for every integer n (not only |n| ≤ 12) on K40's boards, COMPUTED-1 on the other
boards of §1.

*Proof.* (⇒) for n ≤ 0 and (⇐) for n ≥ 0 are the monotonicity of r(G + n) in n (KNOWN; White ignores her tokens, or Black's
options form a subset). The real content is (⇐) for n = −k < 0. White's strategy: in x, play the W_N strategy (a move that
promotes or lowers the stage ρ); never touch the integer (it has no Left move). Invariant: at Black to move, (y, b) ∈ W_N.
- Black moves in x: to (z, w) of stage < ρ(y, b); White replies to stage < ρ(z, w).
- Black spends a spare (legal only when not in check): (y, w) ∈ W_N by Lemma P; White plays her W_N move from there.
- Black has no legal move (no x-move, and no spare left or in check): Black loses (normal play, or mate).
The pair (spares left, ρ) decreases lexicographically every round, so the play is finite and ends with a promotion or with
Black unable to move: a White win. ∎

## 3. Every test game: the lower bound

**Theorem 2 (the bind lower bound).** Assume Lemma P. Let (y, s) ∈ W_N and let t be a position of a terminal-free T.
- (a) s = b: if (t, R) ∈ ON_T then White wins (y, t) ⊞ with Black to move.
- (b) s = w: if (t, R) ∈ ON_T, or if some Left option t′ of t has (t′, R) ∈ ON_T and y_b ∈ W_N, then White wins with White to move.
In particular, if (y_w, y_b) are both in W_N (pairs ON/ON, DEC/DEC, DEC/ON), White wins y_w ⊞ T whenever (t, L) ∈ ON_T.

*Status:* PROVED given Lemma P (so CHECKED-2 / COMPUTED-1 as Lemma P). Properties of T used: only that T is finite and terminal-free
and the predicate (t, R) ∈ ON_T. The check rule only removes Black options.

*Proof.* Let λ be Left's stage-lowering strategy in on ⊞ T. White keeps a virtual position of on ⊞ T and an invariant at every
Black-to-move moment: the x-position is in W_N with Black to move, and the virtual position is (t, R) ∈ ON_T.
- Black moves in x (y_b → z_w, lower stage): the virtual position does not change. White answers with her W_N move in x.
- Black moves in T (t → t′, so he is not in check): virtually Right moved, and λ answers at (t′, L) either with a pass or with a
  T-move t′ → t″. For a T-move White plays it for real; the x-position, still y_b ∈ W_N, is untouched. For a pass White plays her
  W_N move in x from y_w, which is in W_N by Lemma P.
- Black has no legal move: he loses.
Measure: (stage of the virtual position in on ⊞ T, ρ of the x-position), lexicographic. A round with a Black T-move lowers the
first entry; a round with a Black x-move keeps it and lowers ρ. So the play is finite; it ends in a promotion or in a Black with
no move, a White win. (Black can never reach Kxp: W_N positions with Black to move do not allow it.) For (b): if
(t, R) ∈ ON_T White makes her W_N move in x first; otherwise she plays t → t′ and the invariant holds because y_b ∈ W_N. ∎

**Corollary 2a (Right-finite T).** If T has no infinite sequence of consecutive Right moves from t, then (t, R) ∈ ON_T (Left
passes until Right is stuck), so White wins y ⊞ T for every (y, s) ∈ W_N. This covers all integers, \*, ↑, ↓, ±1, under, on and
on + \*. *Status:* as Theorem 2. (Lemma P is not needed for n ≥ 0, where Black has no T-move.)

**Corollary 2b (over). PROVED (no Lemma P needed).** (over, R) ∈ ON_T: Right's only move is to (over, L), where Left moves to 0
and Right is stuck. In Theorem 2 a Black T-move (over → over) is answered by λ's T-move over → 0, never by a pass, so Lemma P is
not used: White wins y ⊞ over for every (y, s) ∈ W_N.

## 4. Every test game: the upper bound

**Proposition 3 (Right reserves). PROVED.** Call a set S of T-positions a *Right reserve* if every s ∈ S has a Right option in S
and all Left options of every s ∈ S lie in S. If t ∈ S and (y, s) ∉ P_L, then y ⊞ T at t is a draw.

*Proof.* Black has a strategy in y ⊞ dud that never enters W(y ⊞ dud) (the complement of a least fixed point is a trap). In
y ⊞ T Black copies it: a White T-move stays in S and is read as White's pass in dud; Black's pass in dud is played as a Right
move into S, which is legal exactly when the dud pass is (Black not in check). If Black had no legal move in y ⊞ T he would have
none in y ⊞ dud either, which is a White win: excluded. So White never wins; Black never wins (K40 Cor. 3). ∎
off and dud are Right reserves, so every ON position draws against them (this is Theorem 3.11 again).

**Theorem 4 (the trichotomy).** Assume Lemma P, W ≠ 4. Then
- P_L ⊆ W_N, and every (x, s) ∈ P_L is W against every T (K40 Proposition 4): **DEC**;
- every (x, s) ∈ W_N ∖ P_L has the ON signature against all of K40's tests and **against every integer**: W against all
  integers, \*, ↑, ↓, ±1, under, on, on + \* (Cor. 2a), over (Cor. 2b); D against off and dud (Prop. 3);
- every (x, s) ∉ W_N is D against every terminal-free T: **DUD**.

*Status:* PROVED given Lemma P; CHECKED-2 on K40's boards; COMPUTED-1 on the further boards of §1.

*Proof of the third item.* Let N′ be the complement of W_N. In x ⊞ on, White to move at y_w ∈ N′: her x-moves reach N′ (y_w ∉ W_N)
and her pass reaches y_b, which is in N′ by Lemma P (contrapositive). Black to move at y_b ∈ N′ has an x-move to N′ or Kxp (a dead
draw), since a Black-to-move position outside W_N is not stuck. So White never wins x ⊞ on. By Theorem 3.11
(W(K ⊞ S) ⇒ W(K ⊞ on), K = x, S = T; its step (2) survives the check rule because White is never in check) White wins no x ⊞ T,
and Black wins none. ∎

So K40's "the class is fixed by r(x ⊞ 0) and r(x ⊞ dud)" is a consequence of Lemma P, and the **rule for the ON class** is:
(x, s) ∈ ON ⟺ (x, s) ∈ W_N and (x, s) ∉ P_L, i.e. White wins the bare normal-play game but not against a Black who may pass.
Both predicates are one-table look-ups; neither is a short formula in king distances (§6).

## 5. ON is not one game: two types, and the counterexample

The ON signature uses tests T with (t, L) ∈ ON_T ⟺ (t, R) ∈ ON_T. Against tests that separate the two movers, ON splits.

**Proposition 5 (on ≠ x for some ON positions).** Let T₀ = {0 | off}. Then (T₀, L) ∈ ON_T (Left moves to 0) and (T₀, R) ∉ ON_T
(Right moves to off). On cyl:8×8:
- `Kc6 Pa7 ka8`, White to move (ON; the placement is ON/DUD): x ⊞ T₀ = D, while on ⊞ T₀ with Left to move is W.
- `Kb6 Pa7 kb8`, Black to move (ON; Black is in check): x ⊞ T₀ = W, while on ⊞ T₀ with Right to move is D.
*Status:* PROVED (Proposition 6 gives both by hand; `logs/zoff_examples_8x8.log` agrees).

**Proposition 6 (the pawn on rank H−1). PROVED** for every cyl:W×H with W = 3 or W ≥ 5, H ≥ 4. Put the pawn p on (f, H−1); let
q = (f, H) be the promotion square and Π the three squares of rank H−2 on files f−1, f, f+1 (the squares from which the White king
guards p while Black's king stands on q). Distances are king distances on the cylinder.

White to move:
- (W1) q not occupied by Black's king ⇒ **DEC**.
- (W2) bk = q and wk within one step of Π ⇒ **ON**; if moreover wk ∈ Π the type is (on, L): r(x ⊞ T) = r(on ⊞ T, L) for every T;
  if wk ∉ Π the type is (on, R): r(x ⊞ T) = r(on ⊞ T, R) for every T.
- (W3) bk = q and wk at distance ≥ 2 from Π ⇒ **DUD**.

Black to move:
- (B1) Black can play Kxp (bk next to p, wk not next to p) ⇒ **DUD**.
- (B2) bk = q (then wk ∈ Π, else B1) ⇒ **ON**, type (on, R) for every T. This is the *bind*.
- (B3) otherwise, if bk can step to q (bk next to q, wk not next to q): the class of (wk, bk = q, White to move) by W2/W3
  (**ON**, type (on, L), or **DUD**).
- (B4) otherwise **DEC**.

COMPUTED check of the rule: 463,616 positions with the pawn on rank H−1 on cyl:W×H, W ∈ {3, 5, 6, 7, 8, 9}, H ∈ {6, 7, 8},
0 exceptions (`scripts/rule_d1.py`, `logs/rule_d1.log`). The type formulas were checked against 217,992 random-T results (counted with repetition over the runs)
with 0 exceptions (`logs/randT.log`, key `d1`).

*Proof.*
- (W1) If q is empty White promotes now. If wk = q, White moves the king to one of (f±1, H), (f±1, H−1): each is next to p and to
  q, so afterwards Black can neither take p nor enter q, and White promotes next move whatever Black does (a T-move included).
  One of the four is legal. bk is not next to q. If bk is on rank ≤ H−2, the two squares (f±1, H) are at rank distance ≥ 2 from
  it. Otherwise bk is on rank H−1 or H at file distance ≥ 2 from f, so W ≥ 5, and a file at distance ≤ 1 from f+1 is at distance
  ≥ 2 from f−1 unless it is f; so bk is next to the squares of at most one side, and the other side's two squares are free.
  W against every T.
- Squares next to p not next to bk = q: (f±1, H) and (f±1, H−1) are next to q, so the White king can guard p only from Π.
- (W3) Whatever White plays (in x or in T), p is unguarded with Black to move and bk next to it: Kxp, a dead draw. D for every T.
- (B2), the bind. Black's x-moves from q: (f±1, H) are attacked by p; (f±1, H−1) are next to wk except, for W ≥ 5, the square on
  the far side when wk = (f∓1, H−2), and after that move q is empty and White promotes; p is guarded. So **every Black x-move loses
  at once**. White's x-moves inside Π (c = (f, H−2) is next to both other squares of Π) keep the bind; any other x-move unguards p,
  and Black then takes it (D). Black is never in check on q. Hence x ⊞ T from the bind is on ⊞ T with Right to move, except
  that Right may also take the pawn whenever Left leaves Π: if (t, R) ∈ ON_T White wins (Theorem 2, where the "pass" is a king step
  inside Π, so Lemma P is not needed); if not, Black plays Right's surviving T-strategy and takes the pawn if White leaves Π:
  D. So r = r(on ⊞ T, R).
- (W2) With wk ∈ Π White's options are: a step inside Π (to the bind with t, Right to move), a step out of Π (Kxp, D), or a
  T-move t → t′ (to the bind with t′). So r = W iff (t, R) ∈ ON_T or some (t′, R) ∈ ON_T, i.e. iff (t, L) ∈ ON_T. With wk one step
  from Π but not in it, a T-move leaves p unguarded (Kxp), so only the step into Π remains: r = r(on ⊞ T, R).
- (B1) Kxp is a king move, legal in check too; D against every T.
- (B3) From the in-check squares (f±1, H) and from (f±1, H−1) the only Black moves that do not allow an immediate promotion are Kxp
  (excluded) and the step to q; a Black T-move (when legal) leaves q empty and White promotes. So r = r(the W2/W3 position, t).
- (B4) Every Black move, in x or in T, leaves q empty or occupied by White's king, and the pawn guarded or out of reach; then W1
  applies. A Black without a move loses. ∎

*Lemma P for the pawn on rank H−1.* The only White-to-move non-wins are W3; there p is unguarded and next to bk, so with Black
to move B1 gives DUD. So Lemma P holds for these placements, by hand.

**What the random tests show beyond the hand proofs (COMPUTED-1, kn.c, `logs/randT.log`).** Random terminal-free T (each of 1–4 nodes,
loopy allowed, at most two options per side per node; `scripts/randT.py`, seeds 1–5, 7, 11) on cyl:3×6, 3×8, 5×6, 5×8, 6×6, 6×8,
7×6, 8×6, 8×8, every legal position against every T:
- Theorem 2 (lower bound): 0 violations. Proposition 3 (reserves): 0 violations.
- Every ON position behaved like (on, L) for every T or like (on, R) for every T; none was neither. ON/ON with White to move:
  always (on, L). ON with Black to move whose White-to-move twin is ON: always (on, R). Black in check: always (on, L). The twin
  pairs DEC/ON (Black to move) and ON/DUD (White to move) split between the two types.
- **CONJECTURE 7.** Every ON position (x, s) on a cylinder with W ≠ 4 satisfies r(x ⊞ T, s) = r(on ⊞ T, L) for every T, or
  r(x ⊞ T, s) = r(on ⊞ T, R) for every T. PROVED for the pawn on rank H−1 (Prop. 6); the lower bounds are Theorem 2; the upper
  bounds are open in general.

## 6. Why no king-distance rule for lower pawn ranks

With the pawn two ranks from promotion the ON set has 103 relative configurations with White to move and 135 with Black to move
(W ≥ 7; 73/115 on W = 5, 88/125 on W = 6), the same for H = 6 and H = 8 (`scripts/top.py 2`). Together with the reduction of
§4 this is a table, not a rule. The feature vector (side to move, pawn rank, file and rank offsets of both kings from the pawn,
side of the pawn, file distance between the kings) separates the classes on every board with 0 conflicts, but it is the whole
position up to symmetry (25,563 vectors on cyl:8×8; `scripts/mine.py`). No shorter rule was found.

## 7. DUD and the fortresses

**Proposition 8 (forced Kxp gives DUD). PROVED.** If Black can force Kxp against a White who may pass at will (x ⊞ on with Kxp
scored as a Black win), then x ⊞ T is a draw for every terminal-free T (W ≠ 4).

*Proof.* Score Kxp as ⊖; call the game x′. Black wins x′ ⊞ on. Mirror step (1) of Theorem 3.11: Black keeps a virtual x′ ⊞ on;
his strategy prescribes x-moves only (on has no Right move), which he plays for real (legal regardless of check); a real White
T-move is read as the virtual pass in on; White's real x-moves are virtual ones. White has no terminal in T. The virtual stage
drops every round, so Black reaches Kxp in x ⊞ T (before any promotion), after which the game is dead (K40 Lemma 1): D. ∎

By Theorem 4, DUD = the complement of W_N (given Lemma P). The converse "DUD ⊆ forced Kxp" is the statement that no fortress
exists. COMPUTED (kn.c, `scripts/fortress.py`, `logs/fortress.log`; K40's counts reproduced):
- no fortress on cyl:3×6, 3×8, 6×8, 7×6, 8×8, 9×6, 9×7;
- fortresses on cyl:5×6 (30), 5×7 (100), 5×8 (170), 7×7 (182), 7×8 (378), 9×8 (522, new).

**Geometry of the fortresses (COMPUTED, every fortress position on those boards).** Both kings stand on the two *back files*,
the files at cyclic distance (W−1)/2 from the pawn's file; for odd W these two files are adjacent to each other. With White to move
the two kings are on the **same** back file, at rank distance ≥ 2. With Black to move they are on **different** back files, at
rank distance ≥ 2, except 10 (5×7) and 20 (5×8) positions on the same file at rank distance 5. The fortress needs height: none
on 7×6, 9×6, 9×7.

*Explanation (partial, not a proof).* Only odd widths have a pair of adjacent back files, so only there can Black's king stand
"opposite" White's king behind the pawn and still be at the pawn's maximal distance on both sides: whichever way White's king
heads round the cylinder, Black's king heads round the other way, symmetrically. White, who may pass, cannot break the symmetry
by a tempo; Black, who may not pass, keeps it by moving along his back file. A hand proof would have to show that every White
attempt (pawn advance included) lets Black keep or restore one of the listed configurations. **Not done: gap.**

## 8. Gaps

1. Lemma P for pawn ranks below H−1 has no hand proof; everything in §§2–4 depends on it beyond rank H−1.
2. Conjecture 7 (two types) is proved only for the pawn on rank H−1.
3. No hand proof that the odd-width fortresses hold, or that even widths have none.
4. The random-T checks use one solver (kn.c); the K40-test-set results are CHECKED-2 (three codes).
