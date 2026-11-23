# T81L: LOOPY edits after the Codex referee T81, as revised by the T81L referee (2026-11-23)

Replaces `kings/delegate/out/T81L/EDITS.md`. Edits 2, 3, 4, 7 unchanged; 1, 5, 6, 8, 9 fixed; 6b and 10-15 new
(knock-on changes found by the referee). See `VERIFY.md`.

### EDIT 1: state the promotion convention of the pawn models (question 2)
<<<<<<< OLD
- **Players.** White = Left, Black = Right.
=======
- **Promotion in the pawn models S, W and D (revised after T81, 2026-11-23).** A pawn that reaches its last rank, by a
  step, a capture or (on four ranks) a double step, stays there as a pawn with no moves. Such a pawn is passed under
  every test, the textbook test and the e.p.-aware one: no square lies ahead of it, and an enemy pawn beside it on
  that rank would stand on its own first rank, which no pawn does. So every promoting move is a decisive event: a
  passer, or a race scored by the race rule. This is what `cylcgt.pawns` does (`passed` and `moves`; COMPUTED-1 on
  flat 4 ranks `W a2 / B b3`, where a2–a4 is a race scored for White with the pawn left on a4, and on flat 5 ranks
  `W a2 b2 / B b4`, where after a2–a4 nobody is passed under the e.p.-aware test and White's option a4–a5 is scored
  +BIG; neither raises). With this convention S, W and D are defined on every board height, and no result of §1
  needs a bound on H. A bound is needed only for the statement that the side to move at a passer-free position,
  whose e.p. right (if any) was made by the opponent, has no promoting move: it holds for H ≥ 5 (PROVED: a double
  step from rank 2 lands on rank 4 < H, and a capture onto the last rank would need an enemy pawn on its own first
  rank, so a promoting move is a step from the rank before the last; a pawn of the mover there has nothing ahead of
  it but the last rank, so it passes the textbook test, and it cannot fail the e.p. clause, since the double-stepped
  pawn is the opponent's; so the position was not passer-free) and fails for H = 4 (`W a2 / B b3`, White to move:
  a2–a4). Comparison on 4- and 5-rank boards, every passer-free root with at most 2 + 2 pawns of flat 3×4, 4×4,
  3×5, 4×5 and cyl 4×4, 4×5 that satisfies (HSS) and (E) (1,306 roots, 488 of them with a pawn on its last rank
  reachable): o(S) = o(W) at all of them (COMPUTED-1, one run, reproduced by the T81L referee,
  `kings/delegate/out/T81L/findings.txt`).
- **Players.** White = Left, Black = Right.
>>>>>>> NEW

### EDIT 2: D(X) uses the same convention (question 2)
<<<<<<< OLD
  - a passer appears (as in `cylcgt`), with races scored by a race rule;
=======
  - a passer appears (as in `cylcgt`), with races scored by a race rule; a promotion is a passer, by the convention of
    §1.1 (revised after T81, 2026-11-23);
>>>>>>> NEW

### EDIT 3: order of operations in S: test the moved component, then split (question 1)
<<<<<<< OLD
  scored by the race rule. This is the value `cylcgt.pawns.value` computes (COMPUTED-1, `cylcgt/pawns.py`).
=======
  scored by the race rule. This is the value `cylcgt.pawns.value` computes (COMPUTED-1, `cylcgt/pawns.py`).
  - *Order of operations (revised after T81, 2026-11-23).* After a move in a component, the passed test is applied
    to the whole moved component (all pawns on its files) **before** it is re-split. If exactly one side has a passer
    there, the whole component becomes that side's ±BIG; if both have one, the race rule scores the whole component
    as one ±BIG; only if nobody is passed is it re-split. The other summands are untouched and keep their rights.
    Splitting first is a different model: flat 8×8 `W b2 d6 / B c7` is one component; after c7×d6 the passers b2
    and d6 stand on separated files, and split-first gives +BIG − BIG = 0, while the race rule (count: 5 moves each,
    the tie goes to White, the non-mover) gives +BIG. Engine S and W: 𝓛; split-first: 𝓝, so Black moving first wins
    there and loses in W (COMPUTED-1, `kings/delegate/out/T81L/findings.txt`). The proof of Theorem 1.11(c) uses the
    order stated here.
>>>>>>> NEW

### EDIT 4: Theorem 1.11(c) assumes a passer-free root and uses check-before-split (question 1)
<<<<<<< OLD
Let X be a pawn position, let S(X) be its
=======
Let X be a pawn position with no passed pawn (revised after T81, 2026-11-23: at a root with passers of both
colours in different components the engine sums +BIG and −BIG to 0, which is not the D-result; S tests the moved
component before re-splitting it, §1.5), let S(X) be its
>>>>>>> NEW

### EDIT 5: a threat is reached by moves of either colour in any order (Codex caution on the frontier step)
<<<<<<< OLD
- **Threats.** τ(y) ⊆ {+, −} contains + iff some position reachable from y without passing a terminal has an
=======
- **Threats.** In this definition and in Theorem 1.11, "reachable" means by a sequence of options of either player
  in any order, not necessarily alternating, as for M (revised after T81, 2026-11-23: the frontier step in the proof
  of Theorem 1.11(c) prefixes a split move to a threat sequence of a daughter component, which needs this reading;
  `lemmas/common.py: threats` computes it).
  τ(y) ⊆ {+, −} contains + iff some position reachable from y without passing a terminal has an
>>>>>>> NEW

### EDIT 6b: the hypotheses of Theorem 1.14 are read per starter
<<<<<<< OLD
after review: R2 items 2, 5 and 8).** Assume:
=======
after review: R2 items 2, 5 and 8).** The hypotheses (revised after T81, 2026-11-23: in (V1)–(V3), "reachable from
X" means by chess play from X with a fixed side s to move first, as in the conclusion below; (V4) is used only in
(ii), which states its reach):
>>>>>>> NEW

### EDIT 6: Theorem 1.14 holds per side to move (question 3)
<<<<<<< OLD
Then, with either side to move:
=======
Then, for each side s to move at X such that (V1)–(V3) hold at every chess position reachable from X with s moving
first (revised after T81, 2026-11-23: the hypotheses hold per starter, and so do the conclusions. Flat 8×8,
`Kb6 Pc7 / Ka8 Pa5`, king group on files a–c, empty context: with Black to move the only legal move is a5–a4 (a7 and
b7 are covered by Kb6, b8 by c7), a suicide answered by c8=Q mate, so (V1)–(V3) hold and P = D = White wins; with
White to move c8=Q mates at once, a legal Z-move that is not a suicide, so (V3) fails, and the normal-play result of
the empty sum (Z deleted) is a loss for White while P is a White win. PROVED by hand):
>>>>>>> NEW

### EDIT 7: (i) is a statement for the starter s
<<<<<<< OLD
- **(i)** P(X) = D(X). There are no draws, and the result is the normal-play result of G₁ ⊞ … ⊞ G_k (Z
=======
- **(i)** P(X) = D(X) with s to move. There are no draws, and the result is the normal-play result of G₁ ⊞ … ⊞ G_k (Z
>>>>>>> NEW

### EDIT 8: (ii) needs a passer-free root, and (V4) and (E) on the any-order reach of Theorem 1.11(c)
<<<<<<< OLD
- **(ii)** If (V4) holds, the outcome class of S(X) — the BIG value of the pawn components, with the king
=======
- **(ii)** Suppose that the pawn part of X (Z deleted) has no passed pawn, and that (V4) and condition (E) hold at
  every position reachable from it by pawn moves of either side in any order before the first decisive event (the
  reach of Theorem 1.11(c) and of `lemmas/common.py: hereditarily_safe`; revised after T81, 2026-11-23: (V1a) gives
  (E) only on chess play from the starter, and Theorem 1.11(c) needs a passer-free root). Then o(S(X)), with S(X)
  the BIG value of the pawn components and Z deleted, is the outcome class of the D-result pair of G₁ ⊞ … ⊞ G_k
  (Z deleted), and its entry for s to move is the result of P(X) with s to move. Where (V1)–(V3) hold for both
  starters, the outcome class of S(X) — the BIG value of the pawn components, with the king
>>>>>>> NEW

### EDIT 9: proof of (ii) per starter, citing the hypotheses of (ii), not (V1a)
<<<<<<< OLD
- **(ii)** By (i), the D-result pair of X is the D-result pair of D(X), and re-splitting does not change
  that pair (it re-groups the same positions and options). By Theorem 1.11(c), with (V1a) supplying (E)
  (revised after the s12a referee, 2026-11-23), (V4) supplying (HSS) and
  the bound, the outcome class of S(X) is the outcome class of that D-result pair.
=======
- **(ii)** Re-splitting does not change the D-result pair of G₁ ⊞ … ⊞ G_k (it re-groups the same positions and
  options). By Theorem 1.11(c), with the hypotheses of (ii) supplying the passer-free root and (E), and (V4)
  supplying (HSS) and the bound, the outcome class of S(X) is the outcome class of that D-result pair. By (i), its
  entry for a starter s at which (V1)–(V3) hold is the result of P(X) with s to move; if they hold for both
  starters, the pair is the result pair of P(X) (revised after T81, 2026-11-23: per starter, and (E) from the
  hypothesis of (ii), not from (V1a); earlier revision after the s12a referee, 2026-11-23).
>>>>>>> NEW

### EDIT 10: status table, T1.11(c): (E) now comes from T1.14(ii), not (V1a)
<<<<<<< OLD
every use goes through T1.14, whose (V1a) contains (E).
=======
every use goes through T1.14(ii), which assumes (E) on the any-order reach (revised after T81, 2026-11-23: (V1a) gives (E) only on chess play from the starter; (c) also needs a passer-free root, and S tests the moved component for passers before re-splitting it, §1.5).
>>>>>>> NEW

### EDIT 11: status table, T1.14(ii)
<<<<<<< OLD
| T1.14(ii) | GAP → PROVED after repair: (V4) is stated hereditarily on the re-split components of the context, Z deleted, with the corrected τ |
=======
| T1.14(ii) | GAP → PROVED after repair: (V4) is stated hereditarily on the re-split components of the context, Z deleted, with the corrected τ. Revised after T81, 2026-11-23: (V4) and (E) on the any-order reach, a passer-free root, and the conclusion per starter |
>>>>>>> NEW

### EDIT 12: summary table, T1.14 per starter
<<<<<<< OLD
| T1.14 | Validity: (V1)–(V3) give P = D (no draws), (V4) gives o(S) = P, and (A_Q)(X) gives C = P |
=======
| T1.14 | Validity, per side to move: (V1)–(V3) for that side give P = D (no draws), (V4) and (E) on the any-order reach at a passer-free root give o(S) = P, and (A_Q)(X) gives C = P (revised after T81, 2026-11-23) |
>>>>>>> NEW

### EDIT 13: P11 status row: the o(S) clause needs a passer-free root
<<<<<<< OLD
the o(S) clause adds HSS with Theorem 1.11(c) and Theorem 1.14(ii).
=======
the o(S) clause adds HSS with Theorem 1.11(c) and Theorem 1.14(ii), at roots without a passed pawn (revised after T81, 2026-11-23: at a root with passers of both colours in different components S sums +BIG and −BIG to 0, and HSS holds there vacuously).
>>>>>>> NEW

### EDIT 14: P11 prediction row: the o(S) clause needs a passer-free root
<<<<<<< OLD
also = o(S(X)) when hereditarily sum-safe.
=======
also = o(S(X)) when hereditarily sum-safe and X has no passed pawn (revised after T81, 2026-11-23).
>>>>>>> NEW

### EDIT 15: §7 item 4: where (E) is assumed
<<<<<<< OLD
Theorem 1.14(V1a)
     assumes it.
=======
Theorem 1.14(V1a)
     assumes it on chess play from the starter, and Theorem 1.14(ii) on the any-order reach (revised after T81,
     2026-11-23).
>>>>>>> NEW
