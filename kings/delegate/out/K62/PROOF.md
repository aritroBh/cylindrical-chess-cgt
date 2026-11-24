# K62: ladder length, no finite test family, fixed boards, counters

AI work (one agent), 2026-11-24. Not refereed. No human re-derivation. Labels: **PROVED** = complete hand proof in this
file; **COMPUTED-1** = one program (mine, `src/`); **CONJECTURE** = believed, not proved; **KNOWN** = cited result.
Solver results are never PROVED. New statements are numbered 4.20 to 4.23 as proposed for `kings/theory/LOOPY.md`.

## 0. Short answers

1. **Ladder length (Q1).** Yes: for every N ≥ 1 there is an exact over group and a bad Black move m such that White
   wins x_m ⊞ u_0 in T_n for every n < N and loses it (value L) in T_N (**PROVED**, Proposition 4.21). The sharp bound
   (**PROVED**, Theorem 4.20): if (C) fails at m, the first failing ladder index N\*(m) is at most |P(x_m) \ E(x_m)|,
   the number of boards g such that the state (g, Black to move, no right) is reachable from x_m by a White pass in
   Aux before the freeze, not counting boards at which White, to move and not in check, already wins beside −1. So
   N\*(m) ≤ b (the number of boards), and N\*(m) ≤ b − 1 when no e.p. move of White promotes (always in chess).
   Hence T_b (T_{b−1} in chess) decides (C), in place of T_K with K ≈ 4b. Both bounds are attained: N\* = b (with
   e.p. promotions) for every b ≥ 4 (M1) and b ≥ 5 (M2); N\* = b − 1 (without e.p.) for every b ≥ 5 (M1) and b ≥ 6
   (M2). Smallest numbers of boards (table in §2.6; M1 = the K61 model, where a move may return to the same board):
   with e.p. rights max(4, N) boards; without e.p. rights max(5, N + 1) boards, all tight. For chess-like move graphs
   (M2: every move changes the board) the same except N = 3, 4: without e.p. 6 boards (5 impossible without checks;
   with checks open), with e.p. 5 boards (4 open). Sharper (Theorem 4.20(b)): N\*(m) ≤ |P \ (E ∪ S_∞)|, boards from
   which Black can escape some ladder.
2. **No universal finite family (Q2, the main question). PROVED, Theorem 4.22.** For every N ≥ 1 the exact over
   group Λ_N (N + 5 boards, no checks, no e.p.) has the results of ω beside every finite D-game with at most N
   positions, and does not have them beside the chain C_N (N + 1 positions, no terminals, short) nor beside T_{N+1}.
   So for every finite set F of finite D-games, Λ_N with N = max_{T∈F} |T| has the results of ω beside every game of
   F but not beside every finite D-game. Consequently no single finite D-game U, loopy or not, is universal, not even
   in the weak form "G has the results of ω iff both roots, Black to move, have the result of ω beside U" (at any
   position of U). The countable family {T_N : N ≥ 0} is universal (Theorem 4.18(c) / Corollary 4.19(i)). The bound
   "N positions" is sharp for Λ_N (C_N has N + 1). Scope note: the failures that escape every finite family are
   the "win half" of (C); the "draw half" is decided by the single loopy game under_D (K60 §3, remark; Λ_N passes it).
3. **Fixed boards (Q3). PROVED, Corollary 4.23.** For every exact over group of king-and-pawn chess on a w × h board
   (flat or cylinder) with at most p pawns a side: it has the results of ω beside every finite D-game iff both
   roots, Black to move, are White wins beside u_0 of T_M, M = (wh)²(wh + 1)^{2p}. On the real groups where the
   ladder index is known: Z_O (cyl:8×6) fails at its one bad move 1…e5–e4 with N\* = 2 (W beside T_0, T_1; L beside
   T_2 … T_6; CHECKED-2 in K60), and its d4 root test fails from T_2; H10, the four cyl:8×7 groups and the five flat
   8×7 groups satisfy (B1), hence (C), so every ladder gives the right answer (N = 0 suffices).
4. **What a counter needs in chess (Q4).** In all constructions the counter is a chain of Black quiet moves after
   the bad move, at each of which White's only non-losing reply is a tempo elsewhere, because White's board move (a
   freeze into a mutual zugzwang) would let Black answer elsewhere. In chess this is a Black king walk or pawn march
   of n steps during which White's freeze stays available and the walking piece is dead in every zugzwang it
   creates. See §5.

## 1. Setting, notation, readings

### 1.1 The model

The model is the K61 packet §1 (abstract groups, D-sums, exact over groups (O0)–(O4), Aux), with the reading that an
e.p. right only adds moves: every move legal without the right is legal with it, with the same successor
(Theorem 4.18, remark (2); K61 §1 R4). States are (g, f, s): board g, flag f = 1 iff the side s to move holds a
right. r(·) is the value of a sum position (W > D > L, White's view). "Beside an inert component", written **H**: the
group alone with the sum's rules (a promotion ends the play, no move anywhere loses); h(σ) is the value of state σ in
H. A *q-board* is a board reached by a freeze.

**Lemma 1 (P-wins are H-wins). PROVED.** If side Y wins state σ in P alone, Y wins σ in H.
*Proof.* P and H have the same move lists. Every play consistent with a P-winning strategy of Y ends after finitely
many moves with a promotion by Y or with X (the other side) in check and without a move. Both end H with Y's win
(in H a side with no move loses). ∎
So in every exact group: h(q-state with Black to move) = W, h(q, 0, White) = L (O3, O4), h(root, 0, White) = W
(freeze, then O3), and h(root, 0, Black) = W (every Black root move leads to a P-win for White: bad moves by O1, the
shuttle by O2 and O3 at the other root).

### 1.2 Readings

- **Promotions at roots and q's.** (O1)–(O4) name the states (root, no right, either side), (q, Black, freeze's
  right) and (q, White, no right). The *strict* reading forbids promotions at every state of a root board or a
  q-board; the *literal* reading only at the named states. All constructions below satisfy the strict reading; the
  lower bounds of §2.5 use it. Under the literal reading a 3-board exact group fails (C) (§2.5, Example 2.5.4).
- **M1 / M2.** The K61 model allows a move from a board to the same board, and two moves of one state with the same
  successor (Codex uses such edges, K61 §2). *M1* is that model. *M2* is the chess-like model: every move changes
  the board, and two different moves of one state never lead to the same state (they differ in board or right). All
  theorems hold in both. Only the smallest board counts of §2.6 depend on the reading, and the table gives both.
- **Positions of a D-game** are its non-terminal positions; |T| is their number.

### 1.3 The ladder sets

Fix a bad Black move m and x = x_m (White to move, with White's right if m is a double step). Write **B₀** for the
set of right-free Black-to-move states (g, 0, Black).

- **S_n** (n ≥ 0) is the set of group states σ such that σ ⊞ u_0 in T_n, with σ's side to move, is a White win.
  S_∞ = ∩_n S_n. **N\*(m)** = least n with x ∉ S_n (∞ if none). By Theorem 4.18(c), (C) holds at m iff N\*(m) = ∞.
- **Layer game Y(R)** for R ⊆ B₀: the group with the sum's rules and two exits. White, to move and not in check,
  may *advance*: the layer ends, and it is a *success* iff (g, 0, Black) ∈ R, g the current board. Black, to move and
  not in check, may *cut*: the layer ends, and it is a success iff h(g, 0, White) = W. A promotion ends the layer
  (success iff White promoted). A side with no group move and no exit loses (success iff that side is Black).
  Infinite play is not a success. **F(R)** is the set of states from which White can force a success in finitely
  many moves. F is monotone in R. F(∅) is the set of states from which White wins σ ⊞ y in the D-game −1
  (positions y, z; R(y) = {z}, no other options): an advance that cannot succeed is never useful.
- **Z(x)**: the set of group states reachable from x by group moves of either side and by White passes
  (σ = (g, f, White), White not in check, to (g, 0, Black)). **P(x)**: the boards g for which some (g, f, White) ∈ Z(x)
  has White not in check (so (g, 0, Black) ∈ Z(x)). **E(x)** ⊆ P(x): the boards g ∈ P(x) such that every
  (g, f, White) ∈ Z(x) with White not in check lies in F(∅). For a set X of boards, B_X = {(g, 0, Black) : g ∈ X}.

**Lemma 2 (ladder recursion). PROVED** (Codex's recursion, K61 §3, re-derived). S_0 = F(B₀) and S_{n+1} = F(S_n ∩ B₀).
The S_n decrease.
*Proof.* In σ ⊞ u_0 of T_n the moves are: group moves; White's u_0 → u_1 (or u_0 → ⊕ if n = 0), allowed iff White is
not in check, clearing White's right; Black's u_0 → z, allowed iff Black is not in check, clearing his right. After
u_0 → u_1 the position is (g, 0, Black) beside u_1, and the part of T_n at and above u_1 is a copy of T_{n−1} at u_0;
so White wins there iff (g, 0, Black) ∈ S_{n−1}. After u_0 → ⊕ White has won. After u_0 → z the component z has no
options, so the rest is H from (g, 0, White). A promotion ends the play; a side with no move anywhere loses (it has no
group move and, being in check, no ladder move). So the plays of σ ⊞ u_0 up to the first ladder move are the plays of
Y(R) with R = B₀ (n = 0) or R = S_{n−1} ∩ B₀ (n ≥ 1), with the same ends, and White forces a finite win in the sum
iff she forces a finite success in the layer (follow a success strategy, then a winning strategy of the exit's
continuation; conversely a finite winning strategy of the sum reaches, on every consistent play, a promotion, a stuck
Black, or an exit whose continuation it wins). By monotonicity S_1 = F(S_0 ∩ B₀) ⊆ F(B₀) = S_0, and inductively
S_{n+1} = F(S_n ∩ B₀) ⊆ F(S_{n−1} ∩ B₀) = S_n. ∎

**Lemma 3 (localisation and E-reduction). PROVED.** For R ⊆ B₀: (i) F(R) ∩ Z(x) = F(R ∩ B_{P(x)}) ∩ Z(x).
(ii) For g ∈ E(x): F(R) ∩ Z(x) = F(R \ {(g, 0, Black)}) ∩ Z(x). Hence F(R) ∩ Z(x) = F(R ∩ B_{P(x)\E(x)}) ∩ Z(x).
*Proof.* A layer play from a state of Z(x) uses group moves only until it exits, so it stays in Z(x), and every
advance it makes is from a White-to-move state of Z(x) with White not in check, into (g, 0, Black) with g ∈ P(x).
This gives (i). For (ii), "⊇" is monotonicity. Let σ ∈ Z(x) ∩ F(R) with success strategy τ. Let τ′ follow τ until
the play first reaches a White-to-move state ρ at board g with White not in check; ρ ∈ Z(x), so ρ ∈ F(∅) because
g ∈ E(x); from ρ follow a success strategy for F(∅), which never advances successfully, so it succeeds for every R′.
An advance into (g, 0, Black) can only be made at such a ρ, so a τ′-consistent play either never reaches such a ρ (it
is τ-consistent and never advances into (g, 0, Black)) or succeeds from ρ inside F(∅). So σ ∈ F(R \ {(g, 0, Black)}).
Apply (ii) to each g ∈ E(x) in turn. ∎

## 2. Question 1: ladder length

### 2.1 The bound

**Theorem 4.20 (the ladder length is at most the number of pass boards). PROVED.** Let G be an exact over group, m a
bad Black move, x = x_m, P = P(x), E = E(x).
(a) (C) holds at m iff x ⊞ u_0, White to move, is a White win beside T_N for N = |P \ E| (and then for every N).
(b) If (C) fails at m, then N\*(m) ≤ |P \ (E ∪ S_∞)|, where S_∞ here means the boards g with (g, 0, Black) ∈ S_∞.
(c) |P \ E| ≤ b, the number of boards of G. If no e.p. move of White promotes (in particular in chess, where an e.p.
capture never reaches the last rank), then |P \ E| ≤ b − 1.
(d) Consequently Corollary 4.19(i) holds with T_K replaced by T_b, and by T_{b−1} when no e.p. move of White
promotes: G has the results of ω beside every finite D-game iff both roots, Black to move, are White wins beside u_0
of that ladder.

*Proof.* Put Z = Z(x), X = P \ E, R̂_n = S_n ∩ B_X for n ≥ 0 and R̂_{−1} = B_X. B_X ⊆ Z. By Lemmas 2 and 3,
S_{n+1} ∩ Z = F(R̂_n) ∩ Z for every n ≥ −1 (for n = −1: S_0 ∩ Z = F(B₀) ∩ Z = F(B_X) ∩ Z). The R̂_n decrease.
*Stabilisation:* if R̂_j = R̂_{j+1}, then S_{j+1} ∩ Z = S_{j+2} ∩ Z, hence R̂_{j+1} = R̂_{j+2} (both are the
intersections with B_X ⊆ Z), and so on: S_n ∩ Z is constant for n ≥ j + 1. Strict decreases R̂_{j} ⊋ R̂_{j+1}
can happen at most |X| times starting from |R̂_{−1}| = |X|, so the first equality occurs at some j ≤ |X| − 1, and
S_n ∩ Z is constant for n ≥ |X|.
(a) If x ∈ S_{|X|} then x ∈ S_n for all n ≥ |X|, in particular for n = K, so (C) holds by Theorem 4.18(c) ((4) ⇒ (1)).
The converse is Theorem 4.18(c) ((1) ⇒ (3)).
(b) Let N = N\*(m) < ∞. If N = 0 there is nothing to prove. If N ≥ 1, x ∈ S_{N−1} \ S_N, so S_{N−1} ∩ Z ≠ S_N ∩ Z,
so R̂_{N−2} ≠ R̂_{N−1}. Since equality propagates, all N steps R̂_{−1} ⊋ R̂_0 ⊋ … ⊋ R̂_{N−1} are strict. Each removes at
least one state of B_X, and a removed state lies outside some S_j, hence outside S_∞. So N ≤ |X \ S_∞|.
(c) One state (g, 0, Black) per board: |X| ≤ b. For the second claim: x is a P-win for White (O1), so a White
P-winning play from x ends with a White promotion at a board p or with Black mated at a board k. Black is in check
at k, so no state (k, ·, White) is reachable (no move into one's own check; x itself arises from a Black move):
k ∉ P. If the promotion is not an e.p. move, it is legal at every state (p, f, White) (rights only add moves), so
every (p, f, White) ∈ Z with White not in check lies in F(∅) (White promotes at once): p ∈ E or p ∉ P. Either way
some board is outside X.
(d) As Corollary 4.19(i): "⇒" by Theorem 4.18(c) ((1) ⇒ (3)) at t = u_0 and Black's root move being any bad m (or
directly: r(ω ⊞ u_0, Black) = W in every T_N); "⇐": for each bad m, r(x_m ⊞ u_0, White) ≥ r(ρ ⊞ u_0, Black) = W
beside T_b (m is a Black option), and b ≥ |X|, so x_m ∈ S_b ⊆ S_{|X|} gives (C) at m by (a); then Theorem 4.18(b). ∎

*What the bound counts.* Not the number of states K, not the number of boards, and not the number of Black-to-move
states reachable from x_m, but the number of boards whose right-free Black-to-move state Black can be left in after a
White pass (P), less the boards where White, to move, never needs to pass (E), less (in (b)) the boards from which
Black cannot escape any ladder (S_∞). Each ladder rung beyond the first can only be "used up" by Black's reaching a
new such board.

### 2.2 The route lemma (exact ladder index of a construction)

**Lemma 4 (route lemma). PROVED.** Let x be a White-to-move state with White not in check. Let V be the smallest set
of states containing x such that: for a White-to-move state (g, f, White) ∈ V, (g, 0, Black) ∈ V; for a Black state
β ∈ V that is not an *exit*, every successor of every Black group move at β is in V. Here β = (g, 0, Black) is an
*exit* if Black promotes at β or h(g, 0, White) = L. Assume:
(V1) no king is in check at any state of V;
(V2) every non-exit Black state (g, 0, Black) ∈ V has no promoting move and h(g, 0, White) = W;
(V3) every White group move from a White state of V leads to a state at which Black promotes at once, or to a
Black-to-move state (g′, f′, Black) with Black not in check and h(g′, 0, White) = L.
Let d be the least number of White states on a path x = w_1, β_1, w_2, β_2, …, w_d, β_d in V, where β_i is the state
after White's pass at w_i, w_{i+1} is reached by a Black move at β_i, and β_d is an exit (d = ∞ if there is none).
Then x ⊞ u_0, White to move, is a White win in T_n for n < d and a Black win (value L) in T_n for n ≥ d.
*Proof.* n < d: White advances at every turn (legal by (V1)). Black's turns are at non-exit states (an exit needs d
advances before it), where by (V2) he cannot promote and a cut gives White a win in H; so he moves in the group,
staying in V. White's (n + 1)-th advance is u_n → ⊕, made at the latest at w_d, before Black stands at an exit. Each
Black move is followed by an advance, so the play ends within 2n + 3 moves. n ≥ d: Black follows a shortest path.
If White ever makes a group move at a White state of V, by (V3) Black promotes, or cuts (the ladder is not cut yet,
Black is not in check) and wins H. If White advances each time, her d-th advance is u_{d−1} → u_d (not ⊕, since
d ≤ n), and Black, at the exit β_d, promotes or cuts and wins H. White has no other moves. ∎

### 2.3 Constructions

All constructions have no checks, every state of each has a legal move (so P and H agree everywhere), and roots
A, B with the shuttle A ↔ B (single steps) and White's freezes A → q, B → q (single steps). "→" is a single step,
"⇒" a double step (the other side then holds the right). Only the moves listed exist.

**Γ2(k, R) (e.p. family, valid in M1 and M2).** Boards A, B, q, c_0, …, c_k (b = k + 4); R ∈ {∅, A, AB}.
White: roots → q; c_i → q (every i); q ⇒ c_0; at (c_0, White, right) an e.p. promotion.
Black: shuttle; A → c_0 (the bad move m); q ⇒ c_0; at (c_0, Black, right) an e.p. promotion; the route:
R = ∅: c_i → c_{i+1} (i < k), c_k → q. R = A (k ≥ 1): c_0 → A, A → c_1 (a second bad move of A), c_i → c_{i+1}
(1 ≤ i < k), c_k → q. R = AB (k ≥ 1): c_0 → A, B → c_1 (a bad move of B), then as for A. Variant "end P" (k = 0,
R = ∅): c_0 with Black to move promotes, instead of c_0 → q.
*h-values.* (q, 0, Black): only q ⇒ c_0, then White promotes e.p.: W. (q, 0, White): only q ⇒ c_0, Black promotes
e.p.: L. (c_i, f, White) and (root, 0, White): the move to q leaves (q, 0, Black): W.
*Exact.* (O0) no checks; the roots are reached by single steps. (O1) bad moves of A and B lead to (c_0, White, 0) or
(c_1, White, 0), both W. (O2) the only White root move is the freeze, to (q, 0, Black) = W, so it does not lose; no
White root move promotes. (O3)/(O4): the only Black and White moves at q (no right; freezes are single steps) lose
at once and do not promote. Promotions occur only at c_0 (strict reading).
*Ladder index of m.* V: White states (c_i, White, 0), (A or B, White, 0), (q, White, 0); exits: (q, 0, Black)
(h(q, 0, White) = L) and, for "end P", (c_0, 0, Black). (V2): (c_i, 0, Black) and (root, 0, Black) do not promote
(the e.p. promotion needs Black's right) and have h(·, 0, White) = W. (V3): White's moves are c_i → q and roots → q,
leading to (q, 0, Black) with h(q, 0, White) = L, and q ⇒ c_0, after which Black promotes. The route is forced: from
(c_0, 0, Black) the only moves go forward along the route or back to an earlier state (A → c_0, the shuttle back), so
the shortest path to the exit visits every route state once: d = (k + 1) + |R| + 1. By Lemma 4,
**N\*(m) = k + 2 (R = ∅), k + 3 (R = A), k + 4 = b (R = AB), and 1 for "end P"**, and the value beside T_{N\*} is L.

**Γ(0, R) (e.p., M1 only; 4 boards).** As Γ2(0, ∅) except: R = A: c_0 → A and a bad move A ⇒ q of A; R = AB:
c_0 → A and a bad move B ⇒ q of B; and at (q, White, right) an extra e.p. move to (q, 0, Black) (a move to the same
board, so M1 only), which makes the bad move ⇒ q lose at once ((q, 0, Black) = W). V gains the White state
(q, White, 1), whose moves (q ⇒ c_0: Black promotes; the e.p. move: to (q, 0, Black), an exit-type state) satisfy
(V3). The route c_0 → A [→ B] ⇒ q is forced: **N\*(m) = 3 (R = A), 4 = b (R = AB)** on 4 boards.

**Π(k, R) (no e.p., M1 and M2).** Boards A, B, q, p, c_0, …, c_k (b = k + 5). p is hot: whoever is to move at p
promotes. White: roots → q; c_i → q; q → p. Black: shuttle; A → c_0 (m); q → p; the route as in Γ2 with c_k → q;
"end P": c_0 promotes. h: (q, 0, Black) = W (q → p, White promotes), (q, 0, White) = L, (c_i, 0, White) = W.
Exactness as for Γ2. In Lemma 4, (q, 0, White) ∈ V has the single move q → p, after which Black promotes (V3), and
(p, ·, ·) ∉ V. **N\*(m) = k + 2, k + 3, k + 4 = b − 1 for R = ∅, A, AB; 1 for "end P"**; value L.

**Π_self(3), Π_self(4) (no e.p., M1 only; 5 boards).** Boards A, B, q, p, y; p hot; White: roots → q, y → q,
q → p; Black: shuttle, q → p, y → q, B → y, and the bad move B → B (Π_self(3)) or A → A (Π_self(4)). (y, 0, White)
= W (y → q), so B → y loses at once; B → B and A → A lead to a root with White to move, = W. Routes: from (B, White)
via B → y → q, d = 3; from (A, White) via the shuttle to B, then B → y → q, d = 4 (A's other moves go back).
**N\* = 3 and 4** on 5 boards.

**Example 2.3.1 (the basic counter, for orientation).** Π(k, ∅) "with end P at c_k" (Black promotes at c_k instead
of c_k → q) gives N\* = k + 1: White must pass k + 1 times while Black walks c_0 → … → c_k, and Black's promotion at
c_k beats White's (k+2)-th advance.

### 2.4 Proposition 4.21 (ladder lengths are unbounded; sharpness). PROVED

(a) For every N ≥ 1 there is an exact over group with a bad Black move m and N\*(m) = N, value L beside T_N:
Γ2 "end P" (N = 1), Γ2(0, ∅) (N = 2), Γ2(1, ∅), Γ2(1, A), Γ2(1, AB) (N = 3, 4, 5), and Γ2(N − 4, AB) (N ≥ 5), with
max(4, N) boards up to N = 2 and from N = 5, and 5 boards for N = 3, 4; without e.p.: Π (end P, N = 1; Π(0, ∅),
N = 2; Π(1, ∅), Π(1, A), Π(1, AB), N = 3, 4, 5; Π(N − 4, AB), N ≥ 5), with 5, 5, 6, 6, N + 1 boards.
(b) The bounds of Theorem 4.20(c) are attained: N\* = |P \ E| = b for Γ2(k, AB), k ≥ 1 (and Γ(0, AB)); N\* = |P \ E|
= b − 1 for Π(k, AB), k ≥ 1.
*Proof.* §2.3 (Lemma 4). For (b): in Γ2(k, AB), P = all boards (every board's White state is on the route), and E = ∅
(the route states (c_i, White, 0), (root, White, 0), (q, White, 0) are not in F(∅): beside −1 Black cuts after White's
freeze, or White is at q). In Π(k, AB) the same with P = all boards and E = {p}. ∎

### 2.5 Lower bounds on the number of boards. PROVED

**2.5.1** In every exact over group the q-boards differ from A and B, so b ≥ 3; under the strict reading b ≥ 4.
*Proof.* If a freeze led to a root board ρ, then (ρ, 0, White) would be a q-state, all of whose White moves lose at
once (O4), whereas ρ has a freeze (O2), which does not. P-wins exist (O3), so some play ends with a promotion or a
mate. A mate needs a king in check, impossible at roots and q-boards (O0); under the strict reading there are no
promotions there either. ∎

**2.5.2 Without e.p. rights (checks allowed), every exact over group with at most 4 boards satisfies (C).**
*Proof.* Without double steps every board has just the two states that (O1)–(O4) name, so the strict and literal
readings agree. By 2.5.1 there is exactly one q-board q and one further board y, which carries every winning terminal: a
White promotion at (y, White) or Black mated at y (and Black's terminals). The bad moves lead to (A, White),
(B, White) or (y, White) (not (q, White): it is a P-loss for White, O4). If (y, White) is reachable, Black is not in
check at y, so White's terminals are promotions at (y, White) (a single state: no rights). White's Aux strategy: at a
root, pass (no check at roots); at (y, White), promote. Black, after a pass, is at a root: his moves lead to root
White states or (y, White); his freeze leaves (root, 0, White) with h = W (Lemma 1). So every play ends in a White
win or is infinite with a White pass at every White turn: White wins Aux, and (C) holds (Theorem 4.18(c)). ∎
So without e.p. rights a failing group has ≥ 5 boards, and by Theorem 4.20(c) N\* ≤ b − 1, i.e. b ≥ N + 1.

**2.5.3 M2, no checks, no e.p., 5 boards ⇒ N\* ≤ 2.**
*Proof.* Boards A, B and q-boards, and the others carry the promotions (2.5.1). Two q-boards leave one board y with
White's promotion at (y, White); in M2 a bad move cannot lead to a root with White to move (A → A is excluded, a
non-shuttle move A → (B, White, 0) duplicates the shuttle's successor, and there are no double steps), so x = (y,
White), where White promotes: (C) holds. So one q-board q and two boards y, p. If White promotes at both (y, White)
and (p, White), every x promotes. So say White promotes at (p, White) and not at (y, White); x = (y, White), and
a := N\*(m). *Roots stay in S_j for j < a:* by induction on j, (ρ, 0, White) ∈ S_j (advance; for j ≥ 1 it lands in
(ρ, 0, Black) ∈ S_{j−1}), and (ρ, 0, Black) ∈ S_j (Black's moves go to a root with White to move, to (y, White) ∈ S_j
as j < a, or to (p, White), where White promotes; a cut leaves h(ρ, 0, White) = W). p ∈ E or p ∉ P (White promotes
at once). In the proof of Theorem 4.20(b) the N steps remove states of B_X at distinct steps 0, …, a − 1, and a root
state can only be removed at a step ≥ a; so the removed states lie in {(q, 0, Black), (y, 0, Black)}: a ≤ 2. ∎

**2.5.4 Example (literal reading only).** Three boards A, B, q, no checks. Black: shuttle; A ⇒ B and B ⇒ q (bad);
q ⇒ A. White: roots → q; q ⇒ q. E.p. moves: at (A, White, right) White promotes; at (q, Black, right) Black promotes;
at (q, White, right) White may move to (q, 0, Black). Exact under the literal reading (the promotions are at states
that (O1)–(O4) do not name) and N\* = 2 at A ⇒ B (COMPUTED-1, `three_board_literal`; the hand check is the route
lemma with the route B ⇒ q). Under the strict reading it is not exact.

### 2.6 Smallest numbers of boards

Least b for which some exact over group has a bad move with N\*(m) = N (strict reading; e.p. = e.p. rights allowed,
including e.p. promotions; "no e.p." = no double steps; checks allowed in both, but no construction uses them):

| N | no e.p., M1 | no e.p., M2 | e.p., M1 | e.p., M2 |
|---|---|---|---|---|
| 1 | 5 (Π end P) | 5 | 4 (Γ2 end P) | 4 |
| 2 | 5 (Π(0,∅)) | 5 | 4 (Γ2(0,∅)) | 4 |
| 3 | 5 (Π_self(3)) | 6 (Π(1,∅)); 5 impossible without checks | 4 (Γ(0,A)) | 5 (Γ2(1,∅)); 4 open |
| 4 | 5 (Π_self(4)) | 6 (Π(1,A)); 5 impossible without checks | 4 (Γ(0,AB)) | 5 (Γ2(1,A)); 4 open |
| ≥ 5 | N + 1 (Π(N−4,AB)) | N + 1 | N (Γ2(N−4,AB)) | N |

Lower bounds: 2.5.1 (≥ 4), 2.5.2 (≥ 5 without e.p.), Theorem 4.20(c) (≥ N, and ≥ N + 1 without e.p. promotions),
2.5.3. With checks and without e.p., in M2, N = 3, 4: 5 or 6 (open). Every entry is tight except the ones marked open.
**PROVED** (constructions §2.3; lower bounds §2.5 and Theorem 4.20). Checked by program: §6.

## 3. Question 2: no finite family of D-games is a test

### 3.1 The group Λ_N

Boards A, B, q, p, e, c_1, …, c_N (N + 5 boards), no checks, no double steps.
White: A → q, B → q (freezes); q → e; c_i → q (every i); e → p; at p White promotes.
Black: shuttle A ↔ B; A → c_1 (the only bad move m); q → p; c_i → c_{i+1} (i < N), c_N → e; at e Black promotes;
p → e.
Every state has a move, so P = H. *Values:* (p, White) = W, (e, Black) = L. (e, White): only e → p; (p, Black): only
p → e: this pair loops with no other move, so both are D. (q, Black): only q → p, then White promotes: W.
(q, White): only q → e, then Black promotes: L. (c_i, White): c_i → q gives (q, Black) = W: W. (A or B, White): the
freeze gives W.
*Exact.* (O0) no checks, no rights. (O1) the shuttle is legal; A → c_1 leads to (c_1, White) = W. (O2) the freeze
gives (q, Black) = W, so it does not lose; no root promotion. (O3), (O4) the single moves at q lose at once and do
not promote. The q-states are (q, Black) and (q, White). **PROVED.**

### 3.2 Theorem 4.22

**Theorem 4.22 (no finite test family). PROVED.**
(i) Λ_N has the results of ω beside every finite D-game T with |T| ≤ N (both roots, either side, every position;
both q-states have the results of 0_D).
(ii) Λ_N does not have the results of ω beside the short chain C_N (positions 0, 1, …, N; L(i) = {i − 1},
R(i) = {0} for i ≥ 1; position 0 has no options; N + 1 positions, no terminals) nor beside T_{N+1}: at the top of
C_N, and at u_0 of T_{N+1}, the root A with Black to move has value D, while ω with Black to move has value W.
(iii) Hence for every finite set F of finite D-games, Λ_N with N = max_{T ∈ F} |T| has the results of ω beside
every game of F and not beside every finite D-game. In particular no single finite D-game U (loopy or short, with or
without terminals) is universal, and not even the root test "both roots, Black to move, have the result of ω beside
U at u" (for a fixed position u, or for all positions) characterises the groups with the results of ω.
(iv) The countable family {T_N : N ≥ 0} is universal: G has the results of ω beside every finite D-game iff it has
them beside every T_N (Corollary 4.19(i); by Theorem 4.20(d), beside T_b already).

*Proof of (i).* By Theorem 4.18(b), game by game, it suffices to prove (C) beside T at m: for every t ∈ T,
r(x ⊞ t, White) ≥ r(ω ⊞ t, Black), x = (c_1, White). If the right side is L there is nothing to prove. Otherwise let
S be a White strategy in over_D ⊞ T from (ω, t, Black): for the value W, the attractor strategy of White's
finite-win region of the finite graph over_D ⊞ T (along a consistent play the attractor rank decreases at every move,
so no state repeats); for the value D, a strategy that never loses. White plays in x ⊞ T with a *shadow* play of
over_D ⊞ T, consistent with S, which starts at (ω, t, Black) with a virtual Black shuttle ω → ω, giving (ω, t, White).
Invariant (while the group is at some c_i): the real state is (c_i, t′, s) and the shadow state is (ω, t′, s), same t′
and s.
- Real White to move at (c_i, t′): S's move at (ω, t′, White). A move in T (a terminal included) is played for real.
  If S plays ω → 0_D, the shadow is (0_D, t′, Black); White plays c_i → q for real, reaching (q, t′, Black), and from
  now on plays a strategy realising r(q ⊞ t′, Black) = r(t′, Black) (Theorem 4.18(a)) = r(0_D ⊞ t′, Black), which is
  W (resp. ≥ D) because the shadow state is S-consistent.
- Real Black to move at (c_i, t′): a Black move in T (a terminal included) is copied into the shadow; a counter move
  c_i → c_{i+1} (i < N) is copied as the shuttle ω → ω. Black has no other move at c_i. The move c_N → e is
  treated below.
Both sides always have the moves needed (White: c_i → q; Black: the counter or the shuttle), no checks interfere, and
T-terminals have the same effect in both plays. Each real counter move is a shadow shuttle, and the shadow has one
more shuttle (the virtual one).
*Value W.* S-consistent plays visit every shadow state at most once, and shuttles are made at states (ω, t″, Black):
at most |T| shuttles, so at most |T| − 1 ≤ N − 1 real counter moves. Reaching e needs N counter moves, so the real
play stays at the c_i's until it switches at q or ends. While the group is at a c_i neither side is ever stuck (White
has c_i → q, Black has a counter move, and in the shadow ω gives White ω → 0_D and Black the shuttle), so a play
before the switch ends only by a terminal of T, which the S-consistent shadow makes ⊕. An S-consistent play is
finite, hence so is the real play before the switch (each real move is a shadow move, except that no real move
corresponds to the virtual shuttle). After a switch White wins by Theorem 4.18(a). So every consistent real play is a
finite White win; the strategy has finite memory and the game is finitely branching, so the win is forced within a
bounded number of moves (König).
*Value D.* As above, except that infinite plays are allowed (draws) and the real play may reach e: Black plays
c_N → e at (c_N, t″, Black) while the shadow is at (ω, t″, Black). Since S never loses, t″ has no Black option ⊖
(else Black wins the shadow at once). Now White plays: at (e, t‴, White), ⊕ if t‴ has a White option ⊕, else e → p.
At (p, t‴, Black) Black's options are p → e (back), or a move in T, after which White promotes at p; a move to ⊖ is
impossible because t‴ = t″ until Black moves in T. So the play loops between e and p (a draw) or White wins. In every
other case the real play copies an S-consistent shadow play (a draw if infinite) or switches at q. So r ≥ D. ∎

*Proof of (ii).* C_N: r(ω ⊞ N, Black) = W: White answers a shuttle at position i ≥ 1 by i → i − 1, a shuttle at 0 by
ω → 0_D, and Black's move i → 0 by ω → 0_D; in each case Black is finally stuck. In Λ_N, Black at the root plays
m, reaching (c_1, N, White); Black's strategy: answer a White move in C_N by the counter move; answer White's c_i → q
by moving in C_N to 0, after which White's only move is q → e and Black promotes. White's T-moves and Black's counter
moves alternate, so at (c_j, ·, White) the chain is at N − j + 1 ≥ 1, and a freeze always meets a chain position from
which Black can move to 0. After White's N-th chain move Black plays c_N → e, reaching (e, 0, White): White has no
chain move (position 0 has no options), so she must play e → p, and Black's p → e repeats forever (Black has no
chain move at 0 either; a move elsewhere is impossible). So
r(A ⊞ N, Black) ≤ r(x ⊞ N, White) ≤ D < W. T_{N+1}: r(ω ⊞ u_0, Black) = W (Theorem 4.18(c), (1) ⇒ (3) proof). In
Λ_N, Black plays m and walks the counter; White's advances are N at c_1, …, c_N; at (e, White) her advance would be
the (N + 1)-th, u_N → u_{N+1}, not ⊕, after which Black promotes; e → p loops as above; a freeze c_i → q is answered
by a cut, and h(q, White) = L. So the value is ≤ D. Both values are exactly D (White can always loop). Λ_N passes
T_n for n ≤ N: the first half of the proof of Lemma 4 (which uses only (V1) and (V2)) applies with the exit
(e, Black) (Black promotes) after the N + 1 White states c_1, …, c_N, e, so x ⊞ u_0 is a White win. Beside T_n,
(C) at t = u_i is the same statement for T_{n−i} (the ladder above u_i is a copy of T_{n−i}), and at t = z it reads
r(x ⊞ z, White) = h(x) = W; so (C) holds beside T_n, and Theorem 4.18(b) gives the results of ω beside T_n. ∎

*Proof of (iii) and (iv).* (iii): by (i) and (ii); for the root test, Λ_N passes U entirely, so in particular at the
roots, while it fails beside C_N. (iv): Corollary 4.19(i) and Theorem 4.20(d). ∎

*Sharpness and scope.* (i) is sharp for Λ_N (C_N has N + 1 positions). Λ_N's failure is in the "win half" of (C):
x ⊞ t is a draw where ω ⊞ t is a White win. The "draw half" of (C) (r(ω ⊞ t, Black) ≥ D ⇒ r(x ⊞ t, White) ≥ D for all
T) is equivalent to White not losing x ⊞ under_D (K60 §3, remark "The draw part alone", PROVED there and confirmed by
the K60 referee; not re-derived here), so one loopy game decides that half for every group; Λ_N passes under_D.
The proof of (i) shows why no finite game can decide the win half: a game with n positions lets Black use at most
n − 1 tempo moves before White has won or frozen, and Λ_N's Black needs N of them.

*Remark (CGT reading).* After m, the counter behaves like a Black reserve of N tempi that ends in a draw loop.
Beside T, the reserve matters only if White's win in ω ⊞ T needs more than |T| − 1 Black passes answered, which never
happens. C_1 is \*, and Λ_1 fails beside it; C_2 at position 2 is ↓, and Λ_2 fails beside it.

## 4. Question 3: fixed boards

**Corollary 4.23 (one ladder for all groups on a board). PROVED.** Let w, h, p ≥ 1 and M = (wh)²·(wh + 1)^{2p}.
For every exact over group G of king-and-pawn chess on the w × h board (flat or cylinder) with at most p pawns a side,
taken as the P game of its own pieces in a D-sum: G has the results of ω beside every finite D-game iff both roots,
Black to move, are White wins beside u_0 of T_M. (Any M ≥ b(G) − 1 works, b(G) the number of boards of G.)
*Proof.* A board of G is a placement of the two kings and at most p pawns of each colour: at most (wh)² king
placements and at most Σ_{i ≤ p} C(wh, i) ≤ (wh + 1)^p pawn sets per colour, so b(G) ≤ M. Apply Theorem 4.20(d)
(for "⇐": a White win of x_m ⊞ u_0 beside T_M gives one beside T_{|P \ E|}, since |P \ E| ≤ b ≤ M and the S_n
decrease, Lemma 2; "⇒": Theorem 4.18(c)). In chess an e.p.
capture never promotes, so T_{b−1} already suffices. ∎
*Known values.* Z_O (cyl:8×6): its only failing bad move, 1…e5–e4 at d4, has N\* = 2 (W beside T_0, T_1; L beside T_2
to T_6), and the root test fails from T_2 at the d4 root and from T_3 at the d5 root (K60 §6 and Corollary 4.19,
CHECKED-2). H10, the four groups of cyl:8×7 and the five flat 8×7 groups of Corollary 4.17 satisfy (B1), so (C)
holds at every bad move (Corollary 4.19(ii)) and every ladder T_N passes; the smallest sufficient N is 0. So on every
real group computed so far N ≤ 2 suffices; for real groups b is in the millions, so the Büchi form of Theorem 4.18(c)
stays the practical test, and Theorem 4.20 matters only as a bound.

## 5. Question 4: what a counter needs in chess

In Γ2, Π and Λ_N the counter is Black's route c_0 → c_1 → … after the bad move: at each step White's only non-losing
answer is a tempo elsewhere, because White's board move, the freeze into a mutual zugzwang, lets Black answer
elsewhere and leaves White in zugzwang; Black's route ends where Black wins (at q, where Black waits elsewhere and White is
in zugzwang: Γ2, Π) or where White is caught in a board loop (Λ_N). In chess this would be a Black king walk, or a Black pawn march of n quiet steps,
during which (a) White's freeze stays available and stays a mutual zugzwang after each step, and (b) the walking
piece has no move in those zugzwangs (else Black would have spare tempi and the zugzwang would fail). Exactness
constrains only the roots and the q's, so nothing in Definition 4.8 forbids such a counter beyond the bad move; but
(b) is restrictive, since a piece that can make n quiet moves while White waits usually still has a move after the
freeze. Whether a real exact group with N\* ≥ 3 exists is OPEN (no search was made). What to search for: exact over groups with a bad Black root move m for which x_m ⊞ u_0 is a White win beside T_2 but Aux is lost
(equivalently, N\*(m) ≥ 3), computed with the layer recursion of Lemma 2 on the group's own graph; the likely shape is
a Black king that walks toward a blocked pawn chain while White's king and pawn freeze keeps an opposition zugzwang at
every step.

## 6. Computations (COMPUTED-1)

Own code in `src/` (nothing copied): `k62lib.py` (least-fixed-point solver; D-sums with checks, rights, promotions,
the no-move rule; exactness O0–O4; Aux as a Büchi game by the nested fixed point νZ.μY; ladders; Z, P, E, S_n),
`k62families.py` (the constructions), `k62q1.py`, `k62q2.py`, `k62chain.py`. Commands (from the repository root):

- `.venv/bin/python kings/delegate/out/K62/src/k62q1.py families` → `logs/q1_families.log`: 97 (group, bad move)
  rows over Γ2, Γ, Π, Π_self, Λ_1..Λ_6 and the literal 3-board group: every group exact (the literal one under the literal reading); N\* (by ladder solves) as
  stated in §2.3 and §3; Aux lost exactly when N\* is finite (Büchi solver vs ladders up to n = 4b + 2 ≥ K); the
  value beside T_{N\*} is L (Γ, Γ2, Π) and D (Λ_N); N\* ≤ |P \ (E ∪ S_∞)| ≤ |P \ E| ≤ b, ≤ b − 1 without e.p.
  promotions; the chain R̂_n stabilises as in the proof; x ∈ S_{|P\E|} iff Aux is won. 0 violations.
- `.venv/bin/python kings/delegate/out/K62/src/k62q1.py random S 1500` for S = 11, 12, 13 → `logs/q1_random.log`:
  4,500 random exact groups (4 to 8 boards; models plain, checks, e.p., checks + e.p.), 7,778 bad moves, 493 failing
  (C) (N\* from 0 to 4); the same checks: 0 violations. N\* = |P \ (E ∪ S_∞)| occurred (e.g. 4 = 4).
- `.venv/bin/python kings/delegate/out/K62/src/k62q2.py ladders 5` → `logs/q2_ladders.log`: Λ_1..Λ_5 beside T_0..T_7:
  passes iff n ≤ N; the full results-of-ω check and (C) agree; all pass under_D; beside T_{N+1} the root A, Black to
  move, is D and ω is W.
- `.venv/bin/python kings/delegate/out/K62/src/k62q2.py small2 4` → `logs/q2_small2.log`: every D-game with 1 or 2
  positions, unreduced (options any subsets of the positions and both terminals), up to relabelling: 64 + 32,896
  games. Λ_1 fails 128 of the 2-position games (first: \*), Λ_2..Λ_4 pass all.
- `.venv/bin/python kings/delegate/out/K62/src/k62q2.py small3 5` → `logs/q2_small3.log`: every D-game with 3 positions
  (hence every one with at most 3), reduced (Lemma 5 below), up to relabelling: 89,613 games. Λ_1 fails 3,868, Λ_2
  fails 384 (first: the game 0, \* = {0 | 0}, ↓ = {\* | 0}, i.e. C_2), Λ_3, Λ_4, Λ_5 pass all; the full check and (C) agree on every game.
- `.venv/bin/python kings/delegate/out/K62/src/k62q2.py random 21 3000 6` → `logs/q2_random.log`: 3,000 random loopy
  D-games (2 to 9 positions, terminals for both sides, suicides) against Λ_1..Λ_6: no game with |T| ≤ N separates
  Λ_N (0 violations of (i)); full check = (C) on all.
- `.venv/bin/python kings/delegate/out/K62/src/k62chain.py 6` → `logs/q2_chains.log`: Λ_N passes C_1..C_{N−1} and
  fails C_N, …, C_8 (N ≤ 6).

So Λ_5 has the results of ω beside every D-game with at most 3 positions and beside T_0, …, T_5 (and beside every
game with at most 5 positions, by (i)), and is separated from ω by C_5 and T_6.

**Lemma 5 (the reduction used for 3 positions). PROVED.** In every D-sum, (a) deleting a White option ⊖ (or a Black
option ⊕) of T changes no value; (b) if ⊕ ∈ L(t), replacing L(t) by {⊕} changes no value (and likewise ⊖ ∈ R(t)).
*Proof.* (a) A move to one's own losing terminal loses at once; it is never better than another move, and if it is
the mover's only move anywhere, the mover loses with it and without it (no move anywhere loses). (b) Where White may
use L(t) (not in check), the move to ⊕ wins at once whatever else L(t) contains; where she may not, neither set is
usable. ∎ So the reduced enumeration (per side and position: the winning terminal alone, or a set of positions)
covers all D-games with at most 3 positions.

Resources: every run under 45 s and under 70 MB (`/usr/bin/time -l` in the logs).

## 7. Open

- With e.p. rights in M2, whether 4 boards allow N\* = 3 or 4 (5 suffice).
- With checks and without e.p. in M2, whether 5 boards allow N\* = 3 or 4 (6 suffice).
- Whether a real king-and-pawn exact group has N\* ≥ 3 (§5).
- Whether some *countable but sparser* family than {T_N}, or a finite family relative to a bound on |P \ E|, is
  natural; Theorem 4.20 gives the family {T_N : N ≤ β} for groups with |P(x_m) \ E(x_m)| ≤ β at every bad move.

## 8. Where the rules enter

- **Checks.** Lemma 2: advances and cuts are moves elsewhere, forbidden in check. Theorem 4.20(c): a mate board is
  not in P (Black cannot move into check, so no White-to-move state there). Lemma 4 (V1). 2.5.1 (no check at roots and
  q's). 2.5.2 (a mate at y makes (y, White) unreachable). Λ_N, Γ2, Π have no checks.
- **E.p. rights.** Z and P use the right-free Black states only, because a White pass clears White's right and
  Black receives none. Theorem 4.20(c): rights only add moves, so a non-e.p. promotion is available at every flag
  of its board; an e.p. promotion is exactly what lets the bound reach b (Γ2). Lemma 4: exits and h use the
  right-free state after a cut. Γ2's promotions need Black's or White's right after q ⇒ c_0.
- **Stalemate vs no-move-loses.** Only (O1)–(O4) use P. All constructions have a move at every state, so P = H.
  Lemma 1 (P-win ⇒ H-win) for the h-values of roots and q's.
- **Promotions.** Terminals for the promoter in every sum, in Y(R), in Aux. Strict reading for 2.5.
- **Terminals of T.** Copied in the shadow (Theorem 4.22(i)); the D case uses that a non-losing S never lets Black
  reach ⊖ at once; Lemma 5.
- **Loopy T, infinite play.** Theorem 4.22(i): the attractor strategy bounds shuttles for W; draws transfer for D,
  including the e–p loop. Λ_N's failure is a draw, not a loss.
- **Draws.** (C) compares three values; Λ_N shows a W-versus-D failure that no finite game detects, while Γ2 and Π fail
  with L (and are detected by under_D as well: x ⊞ ω̄, White to move, is L for them, D for Λ_N; COMPUTED-1).
