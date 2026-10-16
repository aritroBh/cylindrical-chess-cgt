# Structural lemmas for pawn endgames on flat boards and cylinders (workstream A1)

*Written 2026-10-15 to 16 by Claude (Opus) for the continuation of "Analysis of Chess Endgames on a Cylindrical
Chessboard" (2025). Test code: [`lemmas/`](../lemmas/). Every number below has a reproduce command in §7.*

**Status of the proofs.** One model wrote every proof here. RESEARCH_PLAN §4 (rule 3) requires a second
model and a human to re-derive a proof before it is published. None of these proofs has been re-derived yet.

Each lemma also has a falsification test. The tests found no counterexample to any statement labelled
*Theorem* or *Proposition*. They did find counterexamples to three assumptions the project was using: the
`sum_safe()` flag, the sum model with live en-passant rights, and the partizan values of Dawson's chess.

**Labels used below**

- **Theorem (convention):** proved here. It is a statement about the pawn-only game or the frozen-king game.
  It says nothing about real chess.
- **Proposition (chess):** proved here, about real chess positions. "Modulo KQK" means the proof uses one
  imported fact: K+Q against a bare K is a win unless the bare king can take the queen at once or is
  stalemated.
- **Computed once:** one implementation produced the result.
- **Checked two ways:** two independent implementations agree.
- **Heuristic:** a claim about real chess that is not proved.

---

## Summary

| # | Statement | Kind | Evidence |
|---|---|---|---|
| L0 | Rotations and reflections of the files preserve values. Colour reversal negates them. | Theorem (convention) | proof; 1,192 random checks |
| L1.1–1.4 | An empty file stays empty. Components are intervals on a flat board; on a cylinder they are arcs or a single ring. An arc component has the same value as the same pawns on a flat strip of its own width. | Theorem | proof; 1.5 million moves and 622 arcs checked |
| L1.5 | A value that occurs on the cylinder C_n but not on the flat board F_n is the value of a **ring** position, one in which every file holds a pawn. | Theorem | follows from L1.4 |
| L1.6 | In the pure pawn game, a position is the disjunctive sum of its components, provided no position with two or more components has a usable e.p. right (condition (E)). | Theorem | proof; 274 random sums |
| L1.7 | Without (E) the sum can be wrong, outcome included. | Counterexample | computed once |
| L2.1 | The ±BIG sum model gives the right winner if the position is *hereditarily sum-safe* (HSS) and BIG exceeds the number of moves either side can make. | Theorem (convention) | proof; all 1,297 HSS positions in a random sample of 1,500 agree |
| L2.2 | `pawns.sum_safe()` is **not** a correct test. It returns True on single components whose sum-model outcome is wrong. | Counterexample | checked two ways (with Codex's `crosscheck/minimax.py`) |
| L2.3 | If no reachable non-terminal position splits into components, the sum model equals the whole-board game exactly. The \*2 candidate is such a position. | Theorem; computation | proof; full tree enumerated |
| L3.1 | Geometry of the 8×8 embedding (WK f5, BK h4, W g4, B g5, component on a–d): no checks, no stalemate, and every king move drops that side's g-pawn. | Proposition (chess) | hand proof; exhaustive check of all 405 + 225 configurations |
| L3.2 | Scoring a king move as ∓BIG gives the same value however the king move is modelled, for positions strictly between −BIG and BIG. | Theorem | proof; 127 random checks |
| L3.3 | Freeze lemma: adding the losing king moves never changes the outcome. It leaves the value unchanged under a "BIG-interior" condition. | Theorem (convention) | proof; 400 random positions |
| L3.4 | \*2 candidate: sum model = whole-board game = frozen-king game = **\*2** (count and mover rules) or **0** (opponent rule). This holds with e.p. on and off, on the 4-file strip and on 8×8. | Computation | value computed once (one CGT engine, three model recursions); outcome N checked two ways |
| L3.5 | The bare trebuchet WK f5 Pg4 / BK h4 Pg5 is a real mutual zugzwang on the flat board. | Proposition (chess), modulo KQK | computed once (forced-win search, 14 plies) |
| L3.6 | The paper's §5.1 cylinder trebuchet is a mutual zugzwang only because of the seam. | Proposition (chess) | exhaustive legal-move check |
| L4.1 | None of the race rules (count, mover, opponent) is exact chess. | Proposition (chess), modulo KQK | 5 forced-win proofs |
| L4.2 | The \*2 depends on 4 individual race verdicts, and also on combinations of the others. | Computation | computed once |
| L5.1–5.2 | Dawson's chess on a 3×n ring: every first move forces a 5-ply sequence that opens the ring into a full strip of n − 3 files. | Theorem | proof; exhaustive check for n ≤ 22 |
| L5.3 | The ring's Grundy value is mex{G(n−3)}, where G is the Grundy function of octal 0.137. The first player wins iff G(n−3) = 0. | Theorem (with the classical flat theorem) | checked for n ≤ 22 |
| L5.4 | The partizan CGT value of Dawson's chess is not its Grundy value (D₅ = \*, but G(5) = 3), and adding partizan values gives wrong winners. | Counterexample | checked two ways (with `cylcgt/dawson.py`) |

**What changes for the project**

1. **Do not use `sum_safe()` to certify sums (L2.2).** Use the HSS test (`lemmas/common.py: hereditarily_safe`),
   or compute the whole-board game W directly.
2. **Restrict the cylinder-only search to ring positions.** By L1.5, a cylinder value that is absent from the flat
   board of the same width comes from a ring position. The atlas (A3) can search only those.
3. **The \*2 is a theorem of the convention only.** It needs the "count" or "mover" race rule. Four race
   positions are individually decisive (§4, Proposition 4.2). That list is what A2 must check in real chess.
4. **Analyse Dawson's chess as an impartial game of forced "macro-moves".** The partizan values printed by
   `cylcgt/dawson.py` belong to a different game (L5.4).

---

## 0. Setting and notation

**Boards.** A board is B = (n, m, κ, ε): n files, m ranks, κ ∈ {flat, cylinder}, ε ∈ {e.p. on, e.p. off}.
Files are 0, …, n−1 (a = 0). On a cylinder they are read mod n. Two files are *adjacent* if they differ by
1, mod n on a cylinder. N(f) is the set of files adjacent to f. On a cylinder we assume n ≥ 3, so that N(f)
has two elements, neither of them f.

**Positions.** A pawn position is X = (P_W, P_B, e). P_W and P_B are disjoint sets of squares (f, r) with
1 ≤ r ≤ m. The e.p. right e is either empty or a triple (t, c, s): t is the target square, c is the square of
the pawn that has just double-stepped, and s is the side allowed to capture. These are the generalised
positions of `cylcgt`, so pawns may stand on ranks 1 and m.

**Moves** (exactly `cylcgt.pawns.moves`). They are stated for White; Black's are the mirror image, with
direction −1 and start rank m − 1.

- (M1) Push: (f, r) → (f, r+1) if that square is empty.
- (M2) Double step: (f, 2) → (f, 4) if (f, 3) and (f, 4) are empty. With e.p. on, it creates the right
  ((f, 3), (f, 4), B).
- (M3) Capture: (f, r) → (g, r+1) with g ∈ N(f) and a black pawn on (g, r+1); that pawn is removed.
- (M4) En passant: if e = (t, c, W) and t = (g, r+1) with g ∈ N(f), then (f, r) → t and the pawn on c is
  removed.

A child never inherits its parent's right. Its right is empty unless the move was a double step.

**Move potential.** Let M_W(X) = Σ over white pawns of (m − r), M_B(X) = Σ over black pawns of (r − 1), and
Φ = M_W + M_B. Every move lowers Φ by at least 1. Every White move lowers M_W by at least 1, and no Black move
raises M_W. Hence:

- the move graph is finite and acyclic;
- every play has at most Φ(X) moves;
- White makes at most M_W(X) moves and Black at most M_B(X), in any sequence of moves by either side.

All games below are therefore short games.

**Passed pawns, terminals, races.**
- A white pawn (f, r) is *passed* if no black pawn stands on a file of {f} ∪ N(f) at a rank greater than r.
  Black is symmetric. pass_W(X) means some white pawn is passed.
- X is *W-terminal* if pass_W(X) and not pass_B(X). B-terminal is symmetric. X is a *race* if both hold.
- A race created by a move of side μ is scored by the rule ρ:
  - ρ = mover: μ wins.
  - ρ = opponent: the other side, ν, wins.
  - ρ = count: let d_s be the smallest promotion distance of a passed front pawn of s, with a double step from
    the start rank counted as one move (`pawns.promote_distance`). Then ν wins iff d_ν ≤ d_μ.

**The four games.** BIG = 256. ±BIG denote canonical integers. Left = White, Right = Black.

- **P(X), the pure game.** No passer rule. P(X) = { P(X') : White moves | P(X') : Black moves }.
- **W(X), the whole-board convention game.**
  - W(X) = +BIG if X is W-terminal and −BIG if X is B-terminal.
  - Otherwise W(X) = { ŵ(X') | ŵ(X'') }, where X' runs over the positions after a White move and X'' over the
    positions after a Black move. Here ŵ(Y) is the race score (±BIG) if the move to Y created a race, and W(Y)
    otherwise.
  - E.p. rights are global. White's options are generated from X with a Black right deleted, because that
    right expires when White moves. Black's options are generated likewise.
- **S(X), the sum model** (= `cylcgt.pawns.value`).
  - S(X) = ±BIG if exactly one side has a passer.
  - Otherwise S(X) = Σᵢ C(Xᵢ) over the components Xᵢ (§1).
  - C(Z) = { ĉ(Z') | ĉ(Z'') }, with Z' and Z'' as above. ĉ(Z') is the race score if the move created a race,
    and S(Z') otherwise.
  - Rights live inside their component.
- **WF(X), the frozen-king game.** Like W, but every non-terminal node gets one extra Left option −BIG
  ("White moves a king") and one extra Right option +BIG.

**Outcomes.** o(G) ∈ {L, R, N, P}. G ⧏ H means "not H ≤ G", that is, G < H or G is confused with H.

**Lemma 0.1 (CGT outcome = alternating play).** o(W(X)) is the outcome of the whole-board convention game
played with alternating moves, for either side starting.

*Proof.* Induction on Φ. The terminal value +BIG, which is also every race won by White, is a Left win
whoever starts; −BIG is a Right win. At a non-terminal node, Left wins moving first iff some Left option is a
Left win when Right moves next. This is the minimax recursion. A Black right is deleted from White's options;
in alternating play White never moves while that right is live, so this does not affect the outcome. ∎

*Test:* `test_L2_big.py` (T2) compares o(W) with a CGT-free minimax (`common.alt_winner`) on every sample.
On 8-rank boards it also compares with `crosscheck/minimax.py`.

### L0. Symmetries — Theorem (convention)

Let σ be any automorphism of the file-adjacency graph: a rotation or reflection of the cycle C_n, or the
reflection of the path. Let X* be the colour reversal of X: (f, r) ↦ (f, m+1−r), colours swapped, and the
right's side swapped. Then, for every rule ρ:

- S(σX) = S(X) and W(σX) = W(X);
- S(X*) = −S(X) and W(X*) = −W(X).

*Proof.* The maps commute with the move rules M1–M4 and preserve passedness. Colour reversal swaps the start
ranks 2 and m − 1, so it maps White's double steps to Black's, and it maps rights to rights. Promotion
distances are exchanged between the sides, and each rule is symmetric in the two sides; for "count", ties go to
the side to move in both pictures. Every model is defined by the same recursion on both sides of each
equation. For colour reversal use −{A | B} = {−B | −A}. Induction on Φ finishes the proof. ∎

*Test:* `test_L1_components.py` (L0): 1,192 checks over S and W, all rules, flat and cylinder. No failure.

---

## 1. L1 — Empty files, components, arcs and rings, en passant

**Lemma 1.1 (an empty file stays empty).** If X → X' is a move, then Occ(X') ⊆ Occ(X), where Occ is the
set of files holding a pawn.

*Proof.* A push or double step stays on its file. A capture or e.p. capture lands on a file g ∈ N(f) that
holds an enemy pawn before the move: on the target square for a capture, on square c for e.p. (c is on the same
file as t). So every file occupied after the move was occupied before. ∎

**Lemma 1.2 (locality).**
- (a) A move of a pawn on file f changes only squares on files {f} ∪ N(f).
- (b) Whether that move is legal depends only on those squares and on e.
- (c) Whether a pawn on file f is passed depends only on the pawns on {f} ∪ N(f).

*Proof.* Read off M1–M4 and the definition of a passed pawn. ∎

**Definition 1.3 (components).** The occupancy graph Γ(X) has vertex set Occ(X) and an edge between adjacent
files. A component of X is the restriction X|K of X to the files of a connected component K of Γ(X). The right
goes with the component that contains the file of its target.

- On a flat board, K is an interval {a, …, b}. Files a − 1 and b + 1 are empty or off the board.
- On a cylinder, either Occ(X) = ℤ_n and K = ℤ_n (the single **ring component**), or K is an **arc**
  {a, a+1, …, a+k} (mod n) with k ≤ n − 2, whose neighbours a − 1 and a + k + 1 are empty. They are the same
  file when k = n − 2.

By Lemma 1.1, components only split and never merge, and arcs never close into a ring. A ring opens into an arc
the first time a capture empties a file (§5 is the extreme case).

**Lemma 1.4 (arc = strip).** Let X be a position whose occupied files form one arc K = {a, …, a+k} of C_n, or
one interval of a flat board. Let ψ map a + i ↦ i. Then ψ is an isomorphism from the move graph of positions
reachable from X on B to the move graph of positions reachable from ψX on the flat strip F_{k+1} (same ranks,
same e.p. flag). It preserves passed pawns, races, promotion distances and rights. Hence P, W, WF and S each
take the same value on X and on ψX.

*Proof.* By Lemma 1.1, every file outside K is empty in every position reachable from X. Take a pawn on file
f ∈ K and a neighbour g of f.
- If g ∈ K, then ψ(g) is the matching neighbour of ψ(f) on the strip.
- If g ∉ K, no pawn ever stands on g. So no capture or e.p. capture can land there, and g never blocks a passed
  pawn. On the strip, the matching neighbour is missing, with the same effect.

So the moves correspond one to one, and so do passed pawns (Lemma 1.2(c)). Promotion distances depend only on
ranks. The four values are defined by the same recursion on both sides. ∎

**Corollary 1.5 (embedding; why rings matter).**
- (a) Let X be a cylinder position with at least one empty file and no passer. Then S(X) = Σᵢ S(X̃ᵢ), where the
  X̃ᵢ are flat strips of total width ≤ n − 1.
- (b) Lay those strips side by side on the flat board F_n, one empty file apart. The result has the same move
  graph, the same S and the same W (apply the proof of 1.4 to all the arcs at once).
- (c) Hence every value of S or W that occurs on C_n but not on F_n is the value of a position in which every
  file of C_n holds a pawn: a single ring component.

The research plan's claim A1(ii) is (c). It means the cylinder-only atlas (A3) need only enumerate ring
positions.

It also explains the remark in RESEARCH_PLAN §1.3 that the \*2 "disappears on the cylinder". On C₄ the
candidate `W a2 c2 / B b7 d7` is a ring (files a and d become adjacent), and its value there is
{3/2±1/2 | −3/2±1/2}. On C₅ and C₈ it is an arc, and its value is \*2 again, by Lemma 1.4. So the remark comes
from comparing boards of equal width. It is not a cylinder effect. (Computed with `common.S` and `common.W`.)

*Tests:* `test_L1_components.py`
- (L1.a/b) 1,547,195 moves from random positions; every move satisfies Lemmas 1.1 and 1.2(a), and passers are
  the OR of the components' passers.
- (L1.c) 622 arc and interval components: S and W are identical, as canonical games, to the relabelled flat
  strip.
- No failure in either.

**Theorem 1.6 (disjunctive decomposition, pure game).** Let X have components X₁, …, X_k with k ≥ 2. Assume
condition **(E)**: e.p. is off, or no position Y reachable from X that has two or more components carries a
*usable* right. A right is usable if the entitled side has an e.p. capture available. Then

  P(X) = P(X₁) + … + P(X_k).

*Proof.* Pawns never leave their component's files. A capture lands on a file holding an enemy pawn, which is
in the same component. Each component also keeps at least one pawn, since a capture removes one pawn but the
capturer remains. So every Y reachable from X has at least k components, and Y|Kᵢ is a position on the files
of Kᵢ.

We prove P(Y) = Σᵢ P(Y|Kᵢ) for every reachable Y, by induction on Φ(Y). By Lemma 1.2, the White moves of Y
are exactly the White moves of the Y|Kᵢ, each leaving the other components unchanged. A right that White may
use lies in the same component as the capturing pawn, because the target's file is adjacent to the
capturer's file. Moves are therefore matched one to one with the options of the sum.

The only possible difference is a right left behind. Suppose Y holds a right in Kⱼ and the move is in Kᵢ,
i ≠ j. In Y the right expires. In the sum it stays in P(Y|Kⱼ). Y has at least two components, so by (E) the
right is not usable. Then Y|Kⱼ with and without the right have the same options, since only e.p. captures
depend on the right and children never inherit it. So their P-values are equal. Each option of P(Y) and the
matching option of the sum are therefore equal by induction. The same holds for Black. ∎

*Remark.* The proof uses nothing about P except its move recursion. For W and S it breaks down at the first
passer, because a passer ends the whole game. That is the subject of L2.

**Proposition 1.7 (e.p. breaks the sum).** Take the flat 6×6 board with e.p. on and
Y = `W: a4 f4 / B: b4 e5`, where White has just played a2–a4, so Black may take b4×a3 e.p. this move only.
Y has components {a, b} and {e, f}.

- Whole board: P(Y) = {0 | −4, −3±2}, outcome **N**.
- Sum of the components: P(`W a4 / B b4`, right on a3) + P(`W f4 / B e5`) = −2\* + (−1±2) = {−1\* | −5\*},
  outcome **R**.

With Black to move (the real chess situation) both say Black wins. They differ with White to move, which is the
case that arises inside larger sums. In the sum, the right survives Black's moves on e/f, so Black can take
e.p. later. Chess forbids that. *Computed once* (`common.pure`, built on `pawns.moves`).

**Open question 1.8 (stale rights at the root).** Do positions with *no* live right ever violate the identity?
We searched 49,610 positions systematically and 53,732 at random. Each had two components, and one component
held an e.p. motif: a pawn on its start rank next to an enemy pawn on the double-step rank. The identity
P(X) = Σ P(Xᵢ) held for every one. *Computed once.*

A heuristic explanation, not a proof: let Q be the position after White's double step and Black's immediate
e.p. capture. If Q ≤ X, then in both models the double-step option is reversible through Q and is replaced by
the Left options of Q. Q has no live right, so the stale right is never seen from X. We have not shown that
Q ≤ X always holds when it matters.

*Tests:* `test_L1_components.py` (L1.d–f) checks 274 random multi-component sums (115 with e.p. off, 159 with
e.p. on and (E)); none fails. A further 100 sums with e.p. on but without (E) all satisfied the identity at the
root, and the script checks the counterexample of 1.7. `search_ep_roots.py` runs the 1.8 searches.

---

## 2. L2 — When may passed pawns be replaced by ±BIG inside sums?

In real chess, or in the whole-board convention game W, the first passed pawn ends the whole game. In the sum
model S, a component that gets a passer is frozen into the integer ±BIG, and play continues in the other
components. A later −BIG can then cancel the earlier +BIG. This is the source of the 10 disagreements in
`crosscheck/REPORT_after_fix.md`.

**Definition 2.0 (threats, safety).**
- The threat set τ(X) ⊆ {+, −} contains + iff some position reachable from X has a white passer. "Reachable"
  means by moves of either side in any order, stopping at the first position that has a passer. − is defined
  the same way for Black.
- τ is monotone: τ(Y) ⊆ τ(X) when Y is reachable from X.
- τ(X) is the union of the τ(Xᵢ) over the components. Passers are local, and before the first passer each
  component can be played on its own.
- X is **pairwise safe** if no two *different* components Xᵢ, Xⱼ have + ∈ τ(Xᵢ) and − ∈ τ(Xⱼ).
- X is **hereditarily sum-safe (HSS)** if every non-terminal position reachable from X, X included, is
  pairwise safe.

Two easy special cases are HSS: τ(X) ⊆ {+} or τ(X) ⊆ {−} (only one side can ever get a passer), and positions
that never split (L2.3). `common.threats` computes τ by memoised recursion over the move graph, and
`common.hereditarily_safe` tests HSS.

**Theorem 2.1 (outcome faithfulness of ±BIG).** Let X be non-terminal and HSS. Assume (E) from §1, and
BIG > max(M_W(X), M_B(X)). Then

  o(S(X)) = o(W(X)) = the alternating-play outcome of the whole-board convention game.

*Proof.*

*Step 0: a game form for S.* Unfold `pawns.value`. S(X) is the value of a game form F whose positions are
pairs (Y, N), where Y is a pawn position (the live components) and N is a finite multiset of frozen integers
±BIG. Its value is Σ (live components) + Σ N. A move is either a move in an integer summand, or a pawn move in a
live component Z. If the pawn move creates a passer or a race inside Z, then Z's pawns leave Y and the score
±BIG joins N. Otherwise Z is replaced by its new components. Under (E), the local and global e.p. rights give
the same options, as in the proof of 1.6. So at any (Y, ∅), the pawn moves of F are exactly those of the
whole-board game.

*Step 1: frontier.* Let (Y, {σBIG}) be a position of F in which no live component has a (−σ)-threat and
BIG > M_{−σ}(Y). Then σ wins F(Y, {σBIG}) whoever moves first.

Take σ = +; the case σ = − is symmetric. Left's strategy is to move in the integer summand every turn
(k → k − 1), which is possible while k ≥ 1. Right cannot move in a positive integer. Integers frozen later are
+BIG, because a −BIG would need a − threat, and a race needs both threats. So every Right move is a black pawn
move in a live component, and Right has at most M_B(Y) moves in total. Left needs at most M_B(Y) + 1 moves and
has at least BIG ≥ M_B(Y) + 1. Right runs out first.

*Step 2: induction.* We prove o(F(Y, ∅)) = o(W(Y)) for every non-terminal Y reachable from X, by induction on
Φ(Y). Take a move of Y, made in component Z.
- If the child is non-terminal, both models give the child, and the induction hypothesis applies.
- If the move creates a σ-passer, or a race scored σ, then W gives the number σBIG, which σ wins whoever starts.
  F gives (Y'', {σBIG}), where Y'' consists of the other components of Y. Here σ ∈ τ(Z): Z reaches the passer
  in one move, and for a race both signs are in τ(Z). Y is pairwise safe (HSS), so no other component of Y has a
  (−σ)-threat. Step 1 applies, because M(Y'') ≤ M(X) < BIG. So σ wins this option as well.
- Race scores agree: before the move Y had no passer, a move changes one component, and passedness is local
  (Lemma 1.2). So all passers of the child lie in Z, and the promotion distances are the same in both models.

Outcomes are determined by the outcomes of the options, so o(F(Y, ∅)) = o(W(Y)). Lemma 0.1 gives the
alternating-play statement. ∎

*Remarks.*
1. The bound is mild. With at most p pawns of each colour on m ranks, M ≤ (m − 1)p. That is 56 for p = 8 on an
   8×8 board, far below 256.
2. The theorem is about outcomes, not values. Even for HSS positions, S(X) and W(X) are often different games.
   Example: on the flat 4×5 board with e.p. off, X = `W: a2 c2 / B: a4 d4` has components {a} and {c, d}. Only
   {c, d} has threats, so X is HSS. W(X) = ±BIG, but S(X) = {BIG\*, {BIG\* | −BIG\*} | −BIG\*, {BIG\* | −BIG\*}}.
   The tempo move on the a-file survives in S after the passer, but not in W. Both values have outcome N.
   ±BIG is a device for getting winners right. It does not give a canonical "value" of a position that contains
   threats. The exact framework for "the first passer ends everything" is affine normal play (Larsson,
   Nowakowski and Santos 2025; RESEARCH_PLAN A0).

**Counterexample 2.2 (`pawns.sum_safe` is not a correct criterion).** `sum_safe()` looks only at the top-level
components, and only at the canonical forms of their values. A single component is always "safe". This misses
cancellations inside nested sums, after the component splits.

Example (8×8 cylinder, e.p. off, count rule): X = `W: b2 d4 g3 h5 / B: a7 c7 f7 g4`.
- X is one component (files f, g, h, a, b, c, d), so `sum_safe(X)` is True.
- o(S(X)) = **R**, but o(W(X)) = **N**.
- o(W) agrees with the minimax in `lemmas/common.py` and with Codex's independent `crosscheck/minimax.py`.
  **Checked two ways.**
- Three of White's four moves and one of Black's six lead to children where S and W already disagree in
  outcome.
- One mechanism: from `W: b5 d4 g3 / B: c6 f6 g4 h6`, the position splits into {b, c, d} and {f, g, h}. Each part
  has both threat signs. S gives R; W gives L.

The table lists every counterexample we found. All are single components with `sum_safe` True, and all fail
HSS, as Theorem 2.1 requires.

| Board | Position | Rule | o(S) | o(W) | Found by |
|---|---|---|---|---|---|
| 8×8 cyl, e.p. off | `W: b2 d4 g3 h5 / B: a7 c7 f7 g4` | count | R | N (= minimax = crosscheck) | search, seed 13 |
| 8×8 cyl, e.p. off | `W: b3 f4 g5 / B: a5 b6 f5 h6` | count | N | L (= minimax = crosscheck) | search, seed 13 |
| 8×8 cyl, e.p. off | `W: b2 c5 d4 f3 / B: c7 d6 e7 g6` | count | L | N (= crosscheck) | search, seed 13 |
| 8×8 cyl, e.p. on | `W: a2 c4 e4 h2 / B: a6 b5 d7 e7` | count | R | N (= crosscheck) | search, seed 11 |
| 8×8 cyl, e.p. on | `W: a5 b6 d2 e2 / B: a7 c7 e7` | count | L | N (= minimax = crosscheck) | time-limited search, seed 12 |
| 8×7 cyl, e.p. off | `W: c2 g2 h4 / B: a5 b6 f5 g6` | count | R | N (= minimax; no crosscheck on 7 ranks) | random scan |
| 7×6 flat, e.p. on | `W: b2 d3 f2 / B: c4 c5 e5 g5` | count | N | R (= minimax) | T3 |
| 8×8 cyl, e.p. on | `W: a3 e2 e4 h6 / B: a4 a5 f5 g7` | opponent | N | L (= minimax) | T3 |
| 6×8 flat, e.p. off | `W: b2 d4 f4 / B: b7 c5 e5 e7` | opponent | R | N (= minimax) | T3 |

"search" is `search_sum_safe.py`. It found 1 counterexample in 489 single components with seed 11, and 3 in 763
with seed 13. "T3" is the random scan in `test_L2_big.py`. The rows marked "minimax" were also re-checked by the
regression test T4 (the first, second, fifth and sixth rows) or by T3 itself.

These are not the "multi-component" failures the cross-check reported. Those 10 are re-examined in T5: all
have `sum_safe` False and HSS False, and o(W) equals the cross-check's exact outcome.

**Corrected criterion.** Use HSS (Theorem 2.1) together with (E) and the move bound. If a position is not HSS,
compute W, the whole-board game, which is exact under the convention by Lemma 0.1.

We found no counterexample to `sum_safe` of the second kind: a multi-component position where it returns True,
HSS fails, and the outcome is wrong (see T3 counts). But we have no proof that canonical simplification cannot
hide a threat.

**Theorem 2.3 (no split ⇒ S = W).** Suppose no non-terminal position reachable from X has two or more
components. Then S(X) = W(X) as canonical games, for every rule.

*Proof.* For each such position, `pawns.value` takes the branch with one component. There `_value` and `_child`
apply the same terminal test, race score and e.p. stripping as the definition of W. Induction on Φ. ∎

*Application.* Enumerate the tree of the \*2 candidate `W a2 c2 / B b7 d7` on the 4-file strip:
- e.p. on: 1,075 reachable positions, 405 of them non-terminal, and **none** of the non-terminal ones has two
  components;
- e.p. off: 835 and 225, likewise.

So S = W for the candidate by Theorem 2.3, under every rule, and the candidate is HSS. The test also found S = W
node by node.

*Tests:* `test_L2_big.py`
- T1, T2: 1,500 random non-terminal positions (seed 1; 4–8 files, 6–8 ranks, flat and cylinder, all three
  rules).
  - 1,297 are HSS, and o(S) = o(W) for all 1,297, as Theorem 2.1 says.
  - Of the 203 that are not HSS, 48 disagree.
  - o(W) equals the CGT-free minimax on all 1,500 positions, and Codex's crosscheck on the 158 positions it can
    handle (8 ranks, count rule).
- T3: `sum_safe` is True on 1,425 positions. 3 of these disagree, all single components that fail HSS (the last
  three rows of the table). 77 multi-component positions have `sum_safe` True but fail HSS; all 77 agree.
- T4: the counterexamples, as a regression test, printing the nested nodes where opposite threats meet.
- T5: the 10 cross-check positions.

---

## 3. L3 — The trebuchet freeze

**The embedding.** Let Y be a pawn configuration on files a–d of the flat 8×8 board, with file e empty. Add the
trebuchet: WK f5, BK h4, white pawn g4, black pawn g5. For the \*2 candidate:

FEN `8/1p1p4/8/5Kp1/6Pk/8/P1P5/8 w - - 0 1`.

As pawn positions, the g-pair is its own component. It is dead: g4 and g5 block each other, and there is no
enemy pawn on f4/h4 or f5/h5 to capture. Neither pawn is passed. So W, WF and S of the 8×8 pawn position equal
those of Y on the 4-file strip (Lemma 1.4; test A4 confirms all six values).

**Proposition 3.1 (geometry, real chess).** Take any chess-legal pawn configuration Y on a–d (pawns on ranks 2–7
only), and either side to move, in the 8×8 position above. Then:
- (i) Neither king is in check.
- (ii) White always has the legal king moves Kf6 and Kg6, and Black always has Kg3 and Kh3. So the position is
  never stalemate. White's king moves are among e4, e5, e6, f6, g6; Black's are g3 and h3.
- (iii) No king move captures a pawn.
- (iv) After any king move, the opponent's king can take the mover's g-pawn at once. After that capture the
  capturer has a passed pawn and the mover has none, provided Y has no passer.
- (v) The legal pawn moves on a–d are exactly the model's moves M1–M4.

*Proof.*
- (i) A pawn attacks only the two adjacent files, so pawns on a–d attack squares on files a–e only. The kings
  stand on f and h. g4 attacks f5 (its own king) and h5. g5 attacks f4 and h4 (its own king).
- (ii) White's king moves from f5:
  - f4 is attacked by g5.
  - g5 is defended by Kh4.
  - g4 holds White's own pawn.
  - e4, e5 and e6 are attacked only if a black pawn stands on d5, d6 or d7.
  - f6 and g6 are attacked by nothing: no black pawn stands on e7, g7 or h7, and Kh4 is not adjacent to them.

  Black's king moves from h4:
  - h5 is attacked by g4.
  - g4 is defended by Kf5.
  - g5 holds Black's own pawn.
  - g3 and h3 are attacked by nothing: no white pawn stands on f2, g2 or h2, and Kf5 is not adjacent to them.
- (iii) The only pawns next to a king are g4 and g5, and those captures are illegal as shown in (ii).
- (iv) None of e4, e5, e6, f6, g6 is adjacent to g4, and no white pawn on f3 or h3 defends it. So ...Kxg4 is
  legal: no white piece attacks g4 after the capture. Then g5 has no white pawn ahead of it on f, g or h, so it
  is passed. White has no passer, because Y has none and g4 is gone. Black's moves Kg3 and Kh3 are symmetric:
  Kxg5 is legal and g4 becomes passed.
- (v) No piece other than the kings and the g-pawns stands near a–d, and no king is ever in check (i). So no
  pawn move is illegal for pin or check reasons, and the chess pawn rules equal M1–M4. ∎

*Exhaustive check* (`test_L3_trebuchet.py`, B1). It uses the small legal-move generator `lemmas/minichess.py`.
That generator matches published perft counts on three flat-board positions: the start position to depth 3,
CPW "position 3" to depth 4 (e.p., checks, pins), and a promotion test position to depth 3
(`test_minichess.py`). Its cylinder mode has no published perft to check against. The check covers:

- every non-terminal configuration reachable from the candidate: 405 with e.p. on, 225 with e.p. off;
- both sides to move in each, 2,493 + 1,395 king moves in total.

In every case (i)–(v) hold, and the king destinations are exactly {e4, e5, e6, f6, g6} and {g3, h3}.

**Modelling the king moves.** By 3.1(iv), every king move allows the opponent an immediate move into a position
that is −BIG (resp. +BIG) under the convention. WF records each king move as that number.

**Lemma 3.2 (robustness of the king-move model).** Let G = {Gᴸ | Gᴿ} with −BIG ≤ G ≤ BIG. Let K_L be any game
with a Right option equal to −BIG, and K_R any game with a Left option equal to +BIG. These model a king move
"faithfully": the king may step back, play on, and so on. Then

  {Gᴸ, K_L | Gᴿ, K_R} = G.

Moreover {Gᴸ, −BIG | Gᴿ, +BIG} = G iff −BIG ⧏ G ⧏ BIG.

*Proof.* We use the reversibility rule twice. If a Left option X of a game H has a Right option Xᴿ ≤ H, then X
may be replaced by the Left options of Xᴿ. The mirror rule holds for Right options.
- Let H = {Gᴸ | Gᴿ, K_R}. Adding a Right option can only lower a game, so H ≤ G ≤ BIG. K_R has the Left option
  BIG ≥ H, so K_R is reversible in H. It is replaced by the Right options of the integer BIG, of which there
  are none. Hence H = G.
- Let G' = {Gᴸ, K_L | Gᴿ, K_R}. Adding a Left option can only raise a game, so G' ≥ H = G ≥ −BIG. K_L has the
  Right option −BIG ≤ G', so K_L is reversible in G'. It is replaced by the Left options of −BIG, of which there
  are none. Hence G' = H = G.
- The second statement is the gift-horse principle: {Gᴸ, X | Gᴿ} = G iff X ⧏ G. The "only if" half holds
  because every Left option of a game is ⧏ that game. Apply it to −BIG on the Left, then to +BIG on the Right
  of the resulting game, which still equals G. ∎

So, strictly inside (−BIG, BIG), it does not matter whether a king move is scored −BIG, modelled in full detail,
or simply omitted.

**Theorem 3.3 (freeze lemma, convention).** For every non-terminal pawn configuration Y:
- (a) o(WF(Y)) = o(W(Y)).
- (b) If every non-terminal Y' reachable from Y is *BIG-interior* (−BIG ⧏ W(Y') ⧏ BIG), then WF(Y) = W(Y).

*Proof.*
- (a) Induction on Φ. The extra Left option −BIG is a Right win whoever starts. So it never makes "Left wins
  moving first" true. If Left has no pawn move, Left loses moving first in both games: in W Left has no move, and
  in WF its only move is to −BIG. The extra Right option +BIG is symmetric. All other options agree in outcome by
  induction.
- (b) Induction. Terminal nodes agree by definition. At a non-terminal node, WF(Y') = {W(Y'ᴸ), −BIG | W(Y'ᴿ), BIG}
  by induction. This equals W(Y') by the gift-horse step of Lemma 3.2. ∎

*Corollary (value(board) = value(component)).* In the 8×8 embedding the convention value of the board is WF(Y).
- Its outcome always equals that of W(Y).
- Its outcome equals that of S(Y) when Y is HSS and satisfies (E) and the move bound (Theorem 2.1).
- Its value equals W(Y) under (b), and also S(Y) when Y never splits (Theorem 2.3).

*Tests* (`test_L3_trebuchet.py`, A1–A3), on 400 random positions on 3–5 files:
- (a) never fails, and both o(W) and o(WF) match a CGT-free minimax.
- WF ≠ W as games in 94 of the 400. All 94 violate the BIG-interior condition, as (b) predicts.
- The smallest example found: flat 2×5, `W: a2 b2 / B: b4`, e.p. off. W = {BIG | ±BIG}, while
  WF = {BIG, {BIG, BIG\* | BIG} | BIG, ±BIG}. Both are L.
- 127 checks of Lemma 3.2 at the root, with K_L = {W(Y) | −BIG} ("the king may step back"), all pass.

**Computation 3.4 (the \*2 candidate in all models).**

| e.p. | rule | S (4 files) | W | WF | S (8×8) | W (8×8) | WF (8×8) |
|---|---|---|---|---|---|---|---|
| on | count | \*2 | \*2 | \*2 | \*2 | \*2 | \*2 |
| on | mover | \*2 | \*2 | \*2 | \*2 | \*2 | \*2 |
| on | opponent | 0 | 0 | 0 | 0 | 0 | 0 |
| off | count / mover | \*2 | \*2 | \*2 | \*2 | \*2 | \*2 |
| off | opponent | 0 | 0 | 0 | 0 | 0 | 0 |

The hypothesis of Theorem 3.3(b) **fails** for the candidate. Its tree has 10 non-terminal nodes with e.p. on (8
with e.p. off) where W(Y') ≤ −BIG or W(Y') ≥ BIG. One example is `W: a2 c5 / B: b7 d7`, with
W = {±BIG | −BIG} ≤ −BIG. WF differs from W at those nodes, yet the root values agree. So "WF = \*2" is a direct
computation, not a consequence of the lemma. *Computed once.* There is one CGT engine (`cylcgt/cgt.py`) and
three model recursions; W and WF are new code in `lemmas/common.py`, which uses `pawns.moves` and `pawns.passed`.
Codex's independent `crosscheck/minimax.py` confirms the outcome N (count rule; 4 and 8 files; e.p. on and off).
It cannot confirm the value \*2, which needs the options' values, not only the winner.

### What happens when the component becomes terminal

1. **A passer appears.** The convention stops the game at ±BIG. In chess play continues, and the kings are no
   longer bound to the trebuchet. The defender may give up its g-pawn to run at the passer.
   - The defender's king may stand inside the passer's square. This is a heuristic count, by the square rule,
     with the king to move.
   - The white king on f5 is two files from d. Of the 566 single-passer children in the candidate's tree (e.p.
     on), 108 have the frozen enemy king inside the passer's square.
   - For races, 125 of 224 have a frozen king inside an enemy passer's square (B4). In those positions "passer =
     win" is not obviously chess.
2. **The side to move has no pawn move (zugzwang).** In the pawn-only game that side loses by normal play. In
   pawn-only chess it would be **stalemate, a draw**. The frozen kings change this: by 3.1(ii) the side to move
   always has a legal king move, so it is never stalemated. By 3.1(iv) every king move gives up the g-pawn.
3. **The bare trebuchet is a real loss for the side to move (Proposition 3.5, modulo KQK).** On the flat board
   with nothing else on it, the side not to move forces a KQK leaf in 14 plies. Forced-win search, `minichess`,
   B2:
   - White to move: `Kf5-e4 Kxg4 Ke3 Kg3 Ke4 g4 Kf5 Kf3 Kg5 g3 Kh4 g2 Kg5 g1=Q`.
   - Black to move: `Kh3 Kxg5 Kg3 Kf5 Kh4 g5 Kh5 g6 Kh6 Kf6 Kh5 g7 Kh4 g8=Q`.

   With pawns on a–d this is **not verified**. The defender's king may attack the a–d pawns instead, and a–d
   pawn moves give spare tempi in the K+P fight. This is for A2: Stockfish, or a 6–8-man tablebase.
4. **Dead component** (no pawn moves for either side, value 0). Whoever must move plays a king move and loses the
   g-pawn, as in item 2.

### What fails in real chess

| Phenomenon | Convention | Chess |
|---|---|---|
| A side has no move | it loses | stalemate is a draw. The trebuchet's spare king moves turn it into a loss (3.1(ii), 3.5). |
| One side has a passed pawn | immediate win (±BIG) | the defending king may catch it (square rule), possibly after giving up the trebuchet pawn |
| Both sides have passers | race rule | depends on kings, checks and whether the new queen stops the other pawn (L4) |
| Promotion | ends the game | a new queen interacts with everything, including the trebuchet kings |
| King moves | lose at once | lose a pawn. Shown to lose for the bare trebuchet (3.5); not shown with a–d pawns present |

### Proposition 3.6 (the cylinder trebuchet of paper §5.1)

On the 8×8 cylinder take WK h5, BK b4, W a4, B a5 (`test_L3_trebuchet.py`, B3).

- Neither king is in check.
- **White** (Kh5) attacks a4, a5 and a6 *across the seam*, and also g4, g5, g6, h4, h6.
  - Legal moves: Kg4, Kg5, Kg6, Kh6, Ka6.
  - Kh4 is illegal: the a5 pawn attacks h4 across the seam.
  - Kxa5 is illegal: Kb4 defends a5.
  - Every legal move leaves a4 en prise to ...Kxa4.
- **Black** (Kb4) attacks a3, a4, a5, b3, b5, c3, c4, c5.
  - Legal moves: Ka3, Kb3, Kc3, Kc4, Kc5.
  - Kb5 is illegal: a4 attacks it.
  - Kxa4 is illegal: Kh5 defends a4 across the seam.
  - Every legal move leaves a5 en prise to Kxa5.

So it **is** a mutual zugzwang under the convention (the audit's corrected row 5.1 agrees). It relies on the seam
three times: Kh5 guards a4, Kh5 attacks a5, and a5 controls h4. Read on a flat board, the same diagram is not a
trebuchet, because ...Kxa4 is legal.

Whether the side to move really loses on the cylinder is **not verified**. The search needs a cylinder KQK
table. The project's 4-man prototype says KQK is won on the cylinder, but that is a single implementation.

*As a freeze for a component:* the kings attack the files g, h, a, b and c. A component cut off from both kings
and from the a-pawns must therefore lie on d–f, with c and g empty. That is at most 3 files, against 4 for the
flat embedding.

---

## 4. L4 — The race rules are not chess

In the pawn-only model there are no kings. So every way a race rule can be wrong in chess involves either a king
or the newly promoted queen. In each example below, the rules are applied as if the side *not* to move had just
made the move that started the race. "Proved" means `minichess.min_forced_win` found a forced win (checkmate or a
KQK leaf) within the stated depth, with every defence searched, under-promotions included. Then the other side
has no forced win. All positions are on the flat 8×8 board.

| # | Position, side to move | d_W, d_B | count | mover | opponent | Chess (proved) | Phenomenon |
|---|---|---|---|---|---|---|---|
| 4.1 | `W: Ke3 Pa5 / B: Kh7 Pd4`, Black | 3, 3 | B | W | B | **W wins** in 8 plies: `...d3 Kxd3`, then a8=Q | square rule: the defending king catches the passer |
| 4.2 | `W: Kh8 Pa6 / B: Kb6 Pd3`, White | 2, 2 | W | B | W | **B wins** in 6 plies: `a7 Kxa7 Kg7 d2 Kh7 d1=Q` | square rule: the king takes the faster pawn |
| 4.3 | `W: Kh8 Pa7 / B: Kb7 Ph3`, White | 1, 2 | W | B | W | **B wins** in 6 plies: `a8=Q+ Kxa8 Kg7 h2 Kh7 h1=Q` | king next to the promotion square |
| 4.4 | `W: Kd5 Pa7 / B: Kb6 Ph2`, White | 1, 1 | W | B | W | **B wins** in 6 plies: `a8=Q h1=Q+` skewers the king on d5 and the queen on a8; under-promotions also lose | promotion with check |
| 4.6 | `W: Ka4 Pg7 / B: Ka6 Pg2`, White | 1, 1 | W | B | W | **W wins** in 3 plies: `g8=Q`, then Qxg2 or Qxg1 | the new queen stops the other pawn |
| 4.5 | `W: Ka3 Pc7 / B: Kh6 Pf2`, White | 1, 1 | W | B | W | no forced win for either side within 6 plies (bounded search, **not** a proof of a draw) | both sides queen, Q vs Q |

**Proposition 4.1.** Each of the three rules gives the wrong winner on at least one legal 8×8 king-and-pawn
position. "count" and "opponent" fail on 4.1–4.4; "mover" fails on 4.6. *Proof:* the forced wins in the table,
modulo KQK. ∎

Example 4.5 shows the typical tie. Both pawns queen, and "first to queen wins" is false unless the first queen
controls the other promotion square or arrives with check. Standard endgame theory treats such Q vs Q positions
as usually drawn. We do not claim a draw here.

The count rule assumes that the first new queen always stops the other pawn. Example 4.6 shows a case where it
does. Example 4.4 shows a case where the second pawn promotes with check instead and wins. We have no *proved*
example where the first queen simply fails to stop the other pawn and the game is drawn. Proving a draw needs a
Q vs Q or Q vs P tablebase, which this workstream does not have.

**Proposition 4.2 (the \*2 hinges on races).** The candidate is \*2 under "count" and "mover" and 0 under
"opponent" (Computation 3.4). Its tree contains 224 distinct race children (child, mover) with e.p. on and 206
with e.p. off. (`pawns.race_hits` reports 398 and 224, because it counts edges into race children.) Flipping a
*single* race verdict away from "count" changes the value of W at the root in exactly 4 cases, the same with
e.p. on and off:

| Race position (after the move) | Mover | count verdict | Value if flipped |
|---|---|---|---|
| `W: a2 b5 / B: d7` | W | W | ↓ |
| `W: a2 / B: c4 d7` | B | B | ↑ |
| `W: a3 b5 / B: d6` | W | W | ↓ |
| `W: a3 / B: c4 d6` | B | B | ↑ |

In all four, the count verdict is "the mover wins".
- If these four are won by the mover and **every other** race is lost by the mover, the value is still \*2.
- If these four are lost by the mover and the rest follow "count", the value is 0.
- If these four are won by the mover and the other races are decided at random, the value is \*2 in 157 of 200
  trials with e.p. on (156 of 200 with e.p. off). The other trials give ↑, ↓ or 0.

Each of the four is decisive on its own, with every other race decided by "count". But fixing these four does
not fix the value for every assignment of the other races. *Computed once.*

*Heuristic hand check of the four critical races*, in the 8×8 embedding (kings f5/h4):
- In the two White-mover races, Black's d-pawn needs 5 moves. Kf5 is inside its square. White's b5-pawn needs 3
  moves, and Kh4 is far outside its square.
- In the two Black-mover races, Black's c4-pawn needs 3 moves, and Kf5 is outside its square (distance 4 to c1).
  White's a-pawn needs 5 moves.

So the count verdict looks like the chess result in all four. This is **not verified**. The trebuchet pawns,
spare tempi and the a–d pawns could change it.

---

## 5. L5 — Dawson's chess on the 3 × n cylinder

**Rules** (derived from the pawn rules, not from the paper's §8 text).
- The board has 3 ranks and n files, flat (the strip D_n) or cylindrical (the ring R_n).
- White pawns stand on rank 1, Black pawns on rank 3, and rank 2 is empty.
- A pawn moves one square forward, or captures one square diagonally forward. Files wrap on the ring.
- **Captures are compulsory.** Play is normal: a side with no move loses.
- With 3 ranks there are no double steps and no promotions that matter.

**Lemma 5.1 (macro-move).** Let n ≥ 3 and start from the full ring R_n. Suppose White pushes on file f. Then:
- Plies 2–5 are forced captures, all on the square (f, 2).
  - Ply 2: Black takes with (f−1, 3) or (f+1, 3).
  - Ply 3: White recaptures with (f−1, 1) or (f+1, 1).
  - Ply 4: Black takes with its remaining neighbour.
  - Ply 5: White takes with its remaining neighbour.
- Every choice leads to the same position:
  - files f − 1 and f + 1 are empty;
  - file f holds a blocked pair, W(f, 2) and B(f, 3);
  - every other file is untouched.
- Black is then to move and has no capture.

The same holds for a first move by Black, with the dead pair W(f, 1), B(f, 2).

*Proof.* Follow alternating play. We show by induction that before each of plies 2–5:
- (a) rank 2 holds exactly one pawn, on (f, 2), and it belongs to the side that has just moved;
- (b) every pawn of the side to move stands on its home rank (rank 3 for Black, rank 1 for White);
- (c) the pawns of the side to move that attack (f, 2) are exactly its pawns on f − 1 and f + 1 not yet used in
  the sequence: two before plies 2 and 3, one before plies 4 and 5.

These hold after ply 1. A pawn on its home rank attacks only squares on rank 2. So by (a) and (b), the captures
available are exactly the captures on (f, 2) by the pawns in (c). Captures are compulsory, so the move is one of
them. Such a capture puts the capturer on (f, 2) in place of the captured pawn, and removes the capturer from
its file f ± 1. So (a)–(c) hold before the next ply. The neighbours in (c) exist and are distinct because n ≥ 3,
so f − 1 ≠ f + 1. Black's original pawn on (f, 3) stands on file f, so it never attacks (f, 2).

After ply 5 every pawn of files f − 1 and f + 1 has been used and removed. White's pawn stands on (f, 2) and
Black's original pawn on (f, 3). Black's pawns are all on rank 3, and only the square (f, 2) on rank 2 is
occupied; its attackers would stand on f ± 1, which are empty. So Black has no capture. The four choices
(which neighbour captures first, at plies 2 and 3) lead to the same position. ∎

**Theorem 5.2 (the ring opens into a strip).** For n ≥ 3, every first move on R_n leads, after its forced
continuation, to D_{n−3} plus an inert file. D_{n−3} is the full flat strip on files f+2, …, f−2. With the
opponent of the first mover to move, it is D_{n−3} + 0.

*Proof.* By Lemma 5.1, files f ± 1 are empty. The dead pair on f can never move: its pawns block each other, and
their capture squares lie on f ± 1, which stay empty by Lemma 1.1, read in Dawson's chess. The remaining files
form an arc of length n − 3 bordered by empty files. The proof of Lemma 1.4 applies verbatim to Dawson's moves.
The isomorphism matches captures with captures, so it also preserves the compulsion rule. Hence the arc is the
flat strip D_{n−3}. ∎

**Theorem 5.3 (Grundy value of the ring).** Let G be the Grundy function of octal 0.137. From a heap of k you may
remove 1 token only if k = 1, remove 2 tokens leaving one heap, or remove 3 tokens leaving at most two heaps.
Then:
- alternating play on R_n is a first-player win iff G(n−3) = 0;
- in the macro-move (impartial) model, R_n has Grundy value mex{G(n−3)}, which is 1 if G(n−3) = 0 and 0
  otherwise.

*Proof.* We use the classical analysis of flat Dawson's chess (see Berlekamp, Conway and Guy, *Winning Ways*).
Quiet positions are sums of full strips separated by empty or dead files. Macro-moves act on them as 0.137 acts on
heaps, by the same argument as Lemma 5.1:
- a push in the middle of a strip removes three files;
- a push at a strip's end gives a 3-ply sequence that removes two files;
- an isolated file is removed by one push.

During a macro-move the other strips are quiet: they have no captures. So global compulsion acts locally, and
alternating play coincides with the impartial game. By Theorem 5.2 the only macro-move of R_n leads to the heap
n − 3. (Our tests confirm the flat statement directly from the pawn rules: alternating play on D_n is a
first-player win iff G(n) ≠ 0, for n ≤ 22.) ∎

The values agree with the paper's §8 formula Ring(n) = mex(G(n − 3)). The paper's *rule text* ("remove a pawn
whose neighbours are empty") permits no first move, and should be replaced by this derivation (audit, row §8).
G is ultimately periodic with period 34 (Dawson's Kayles). So Ring(n) is ultimately periodic as well. We have
not re-derived that periodicity here.

**Counterexample 5.4 (the partizan CGT value is the wrong invariant).** Give each side the compulsion over its
own captures, in a single component: this is how `cylcgt/dawson.py` and our second implementation compute values.

| n | D_n partizan value | Grundy value G(n) | R_n partizan value | mex{G(n−3)} |
|---|---|---|---|---|
| 3 | \*2 | \*2 | \* | \* |
| 4 | 0 | 0 | 0 | 0 |
| 5 | **\*** | **\*3** | 0 | 0 |
| 6 | \* | \*1 | 0 | 0 |
| 7 | **\*2** | **\*1** | \* | \* |

D₅ is \* but G(5) = 3, and D₇ is \*2 but G(7) = 1. In each case both values are first-player wins, so a single
strip's outcome is right. Sums are not. Of the 36 two-strip boards checked (two full strips on one board, one
empty file apart, at most 13 files), the Grundy XOR predicted the alternating-play winner every time. The sum of
partizan values predicted it wrongly three times:
- D₁ + D₅: a first-player win (G = 1 ⊕ 3 = 2), but the partizan sum \* + \* = 0 predicts a second-player win;
- D₂ + D₅: the same, with G = 1 ⊕ 3 = 2;
- D₅ + D₆: the same, with G = 3 ⊕ 1 = 2.

The reason: compulsory capture is a global rule, and a position with a capture pending is not a disjunctive
summand. The CGT value lets the opponent answer elsewhere while a capture is pending. Alternating play never
does. **Checked two ways** for the single-strip values with n ≤ 6 (our implementation and `cylcgt/dawson.py`). The
values for n = 7 and the alternating-play sums are computed once.

*Tests:* `test_L5_dawson.py`
- Lemma 5.1 for every first move and every line, 3 ≤ n ≤ 22.
- Theorem 5.2: the end positions equal D_{n−3} as partizan games, n ≤ 7.
- Theorem 5.3: alternating-play outcomes of R_n and D_n against G, n ≤ 22.
- Two-strip boards against G(a) ⊕ G(b).
- Agreement with `cylcgt/dawson.py`.

---

## 6. What this means for the \*2 candidate (A2)

Proved or computed:
- Under the convention, the 8×8 position `8/1p1p4/8/5Kp1/6Pk/8/P1P5/8` has value \*2 in every model we have (S, W,
  WF), with the count or mover race rule. Under the opponent rule it has value 0.
- The trebuchet geometry is sound: no checks, no stalemate, every king move drops a pawn (Proposition 3.1).
- The bare trebuchet is a real mutual zugzwang (Proposition 3.5).

Not proved: that the position is \*2 *in chess*. The gaps, in order of risk:
1. **Races.** The value depends on how races are decided. Four race positions are individually decisive (§4),
   and other races matter in combination. Each must be resolved in real chess with the trebuchet kings on the
   board.
2. **Passers that are not wins.** In 108 of 566 single-passer children (e.p. on), a frozen king stands inside the
   passer's square.
3. **King sorties.** After a king move the opponent wins the g-pawn. We have not shown that this wins when a–d
   pawns are present.
4. **Value versus outcome.** Even with every race and passer verdict confirmed, a certificate needs every option
   of the 8×8 position to have the right chess outcome. To show the value is \*2 rather than merely "N", add a
   second, independent \*2 (for example the colour-reversed copy, which is −\*2 = \*2) on a wider board. The sum
   must be a **second-player** win, because \*2 + \*2 = 0. The plan's test "\*2 + \* is a first-player win"
   cannot tell \*2 from 0, because 0 + \* = \* is also a first-player win. Two copies of the 4-file component, the
   separating empty files and a trebuchet need about 13 files.

---

## 7. Reproduce

Run from the project root. Each command prints its counts and ends with `FAILURES: 0` when nothing breaks. The
counts quoted above come from these runs. The times are for an idle machine; under load they can be several
times longer.

Check the small chess move generator against published perft counts (about 1 minute):

```bash
PYTHONPATH=. .venv/bin/python lemmas/test_minichess.py
```

Lemmas L0 and L1 (about 6 minutes):

```bash
PYTHONPATH=. .venv/bin/python lemmas/test_L1_components.py --n 600 --seed 20261015
```

Lemma L2 (about 10 minutes):

```bash
PYTHONPATH=. .venv/bin/python lemmas/test_L2_big.py --n 1500 --seed 1
```

The 8×8 `sum_safe` counterexamples (about 10 minutes each):

```bash
PYTHONPATH=. .venv/bin/python lemmas/search_sum_safe.py --seed 11 --n 489
```

```bash
PYTHONPATH=. .venv/bin/python lemmas/search_sum_safe.py --seed 13 --n 763
```

Open question 1.8, systematic search (about 3 minutes):

```bash
PYTHONPATH=. .venv/bin/python lemmas/search_ep_roots.py family
```

Open question 1.8, random search (about 6 minutes):

```bash
PYTHONPATH=. .venv/bin/python lemmas/search_ep_roots.py random --seed 5 --n 53732
```

Lemma L3 (about 5 minutes); `--deep` adds the forced-win search B2:

```bash
PYTHONPATH=. .venv/bin/python lemmas/test_L3_trebuchet.py --n 400 --deep
```

Lemma L4 (about 4 minutes):

```bash
PYTHONPATH=. .venv/bin/python lemmas/test_L4_races.py
```

Lemma L5. The partizan value of R_7 needs about 6 GB of memory; use `--cgt-nmax 6` to skip it:

```bash
PYTHONPATH=. .venv/bin/python lemmas/test_L5_dawson.py --nmax 22 --cgt-nmax 7
```

Fast pytest versions of every test (10 tests, about 4 minutes):

```bash
PYTHONPATH=. .venv/bin/python -m pytest -q lemmas
```

## 8. Open questions

1. Does the pure-game sum identity hold for every position with no live e.p. right (1.8)?
2. Is there a multi-component counterexample to `sum_safe` of the canonical-form kind (§2)? Is HSS also
   *necessary* in some useful sense?
3. A sharper sufficient condition for WF = W that covers the candidate, whose tree has non-interior nodes (3.4).
4. Real-chess status of the four critical races, of the single-passer children, and of king sorties with a–d
   pawns present (§6). This is A2's task.
5. Is the cylinder trebuchet (3.6) a real mutual zugzwang? This needs a verified cylinder KQK table.
