# K33 blind packet: definitions and statements only (extracted from kings/theory/LOOPY.md at commit 774036f)

Proofs, remarks, examples and labels discussion are omitted on purpose. Do not read LOOPY.md itself until Phase 2.

## From §1.2 (Definitions 1.1–1.4)

### 1.2 Games with decisive terminals, and four models

**Definition 1.1 (D-game).** A *D-game* is a finite set X of positions with, for each x ∈ X, finite option
sets L(x) and R(x) contained in X ∪ {⊕, ⊖}.
- ⊕ is the terminal "White has won". ⊖ is the terminal "Black has won".
- The D-game is *short* if the directed graph of moves on X is acyclic, and *loopy* otherwise.
- ∅ denotes a position with no options.

**Definition 1.2 (play and results).**
- Play alternates from (x, s), where s is the player to move.
- A move to ⊕ or ⊖ ends the play with that result.
- A player with no option loses (*normal play*).
- Infinite play is a draw.
- r(x, s) = W if White can force a White win in finitely many moves, L if Black can, and D otherwise.

KNOWN: on a finite game graph these values are the least fixed point computed by retrograde analysis
([S] ch. VI; this is also what kpsolve computes). A short D-game has no draws (Zermelo).

**Definition 1.3 (sum with chess semantics).** For D-games A₁, …, A_k, the sum A₁ ⊞ … ⊞ A_k works as follows.
- Its positions are tuples.
- A move is a move in one coordinate.
- A move to ⊕ or ⊖ in *any* coordinate ends the *whole* play. This is "the first decisive event ends the
  game".
- A player with no option in any coordinate loses.

**Definition 1.4 (BIG translation).** For a short D-game A and an integer B ≥ 1, A^B is the short CGT game
obtained by replacing ⊕ with the integer B and ⊖ with −B. For a sum, (A₁ ⊞ … ⊞ A_k)^B := A₁^B + … + A_k^B
(the disjunctive CGT sum). In this sum a ±B summand does **not** end play: the other components continue.


## Definition 1.10

**Definition 1.10 (tempo counts, threats, dominance).** Let Y = (y₁, …, y_k) be a position of a sum of short
D-games.
- **Tempo counts.** M_L(y) is the largest number of Left moves in any sequence of moves from y (moves by
  both sides, in any order, not necessarily alternating), counting a final move into a terminal. M_R(y) is
  defined the same way for Right. Both are monotone: M(y′) ≤ M(y) whenever y′ is reachable from y.
  - For a sum, M_L(Y) is the sum of the M_L of the coordinates: the coordinates are played independently, so a
    longest sequence of Left moves in the sum is the concatenation of longest sequences in the coordinates.
    (The other reading — stop counting at the first terminal of the whole sum — gives a smaller number, so a
    hypothesis stated with it would be weaker; the proofs below use this component reading, and the count of
    the opponent's moves in the proof of Theorem 1.11(b) is exactly this one. Revised after review: R2 item 9.)
  - In the pawn game every White move advances a White pawn by at least one rank, so
    M_W ≤ Σ_white pawns (H − rank) ≤ (H − 2)p for p legal White pawns. That is ≤ 6p, so ≤ 48 on 8 ranks when
    p ≤ 8, and ≤ 6p in general; BIG = 256 exceeds 6p whenever p ≤ 42. The count ignores a final Z-move, so
    add 1 where a move inside the king group is possible (revised after review: R2 item 9).
- **Threats.** τ(y) ⊆ {+, −} contains + iff some position reachable from y without passing a terminal has an
  option ⊕ **by either player**; it contains − iff some such position has an option ⊖ by either player. So a
  move into the opponent's terminal is a threat for the opponent, and a suicide counts for the side that
  gains from it. Like M, τ is monotone: τ(y′) ⊆ τ(y) whenever y′ is reachable from y.
  - This is the τ of `notes/lemmas.md` (Definition 2.0) and of `lemmas/common.py: threats`, which count a
    passer created by either side's move. The earlier version of this note counted only Left options to ⊕ and
    Right options to ⊖, and was therefore blind to suicides (revised after review: R1 item 1, R2 item 1).
- **First-event dominance.** Y is *first-event dominant for B* if the following holds for every Y′ reachable
  from Y without passing a terminal, and every option y′_j → σ (σ ∈ {⊕, ⊖}, by either player):
  - the CGT position σB + Σ_{i≠j} (y′_i)^B is won by σ's player whoever moves first;
  - here σB means +B if σ = ⊕ and −B if σ = ⊖.


## Theorem 1.11 (statement only; the short case)

**Theorem 1.11 (sums). PROVED for (a); (b) PROVED after repair (revised after review: R1 item 1, R2 item
1); (c) PROVED after repair (R2 item 2).**
- **(a)** If Y is first-event dominant for B, then the outcome class of Σ y_i^B equals the D-result pair of
  ⊞ y_i.
- **(b)** Y is first-event dominant for B if both of the following hold:
  - *pairwise safety:* no reachable Y′ has two different coordinates with + ∈ τ(y′_i) and − ∈ τ(y′_j), with
    the τ of Definition 1.10 (an option to ⊕ or ⊖ counts whoever makes it);
  - *the bound:* B > max(M_L(Y), M_R(Y)).


## Definition 3.1

**Definition 3.1 (pass reservoirs).** Each reservoir is a D-game with a single position ω.
- **on_D:** L(ω) = {ω}, R(ω) = ∅. White can pass forever; Black has no move.
- **off_D:** the mirror image.
- **dud_D:** L(ω) = R(ω) = {ω}.

## §3: setting, conventions and definitions for sums with loopy components

**Sums with loopy components.** Everything here is about D-games in the
sense of Definition 1.1, with loopy components allowed, the sum ⊞ of Definition 1.3 (the first decisive event ends the
whole play, infinite play is a draw) and the loopy CGT translation y^B, which is Definition 1.4 used verbatim for loopy components (Definition 1.4 states it for short
ones; ⊕ ↦ the chain +B, ⊖ ↦ −B; the translated components have no terminals, and Σ y_i^B is the ordinary disjunctive sum under normal play, with draws by
infinite play). First-event dominance (below) is Definition 1.10 restated for loopy components.
- *Conventions.* "σ wins at a position" means "σ forces a win in finitely many moves", i.e. the position is in the least
  fixed point W_σ of Definition 1.2; ρ(v) is its stage. W_L ∩ W_R = ∅ (KNOWN). "G + n" is G with n extra Left tokens (the
  integer n; only the number of unused tokens matters, and Right cannot touch them). "Left wins G + n second" means that
  (G + n, Right to move) ∈ W_L. For a component G, reach(G) is the set of nodes reachable from the root without passing a terminal;
  the reachable tuples of a sum are the product of the reach sets, since the coordinates move independently.
- A node has an *event of sign σ* if one of its options (by either player) is the terminal σ (a suicide counts, as in
  Definition 1.10). A *frontier position* of (Y′, j, σ), with Y′ a reachable tuple and an event of sign σ at y′_j, is
  σB + Σ_{i≠j} (y′_i)^B.
- Y is *first-event dominant for B* if every frontier position is a σ-win whoever moves first (for short components this is
  Definition 1.10).
- *Reserves.* For a node y and B ≥ 1: λ_B(y) is the least C ≥ 0 such that Left wins y^B + C second (Right moves first), and ρ_B(y)
  the least C ≥ 0 such that Right wins y^B − C second; ∞ if there is none. Λ_B(G) and P_B(G) are the maxima over reach(G).
- A component is a *stopper* if the graph on (node, mover) with edges (x, L) → (x^L, R), (x, R) → (x^R, L) has no cycle
  (no infinite alternating play from a reachable node). on, off, over, under are stoppers, dud is not.


## Theorem 3.7 (statement only)

**Theorem 3.7 (loopy bridge).** (K21, 2026-10-27). If Y is first-event dominant for B, then for every reachable tuple Y′ and both
movers the D-result of ⊞ y′_i equals the outcome of Σ (y′_i)^B (W, D or L). No shortness or stopper hypothesis.


## Lemma 3.8a (statement only)

**Lemma 3.8a (subadditivity).** (K21, 2026-10-27). If Left wins G_1 + n_1 second and G_2 + n_2 second (any loopy normal-play games), Left wins
G_1 + G_2 + (n_1 + n_2) second; and if Left wins G + n second she wins G + m second for m ≥ n. So the reserve of a sum is at most the
sum of the reserves, for λ and for ρ.


## Theorem 3.8 (main statement) (statement only)

**Theorem 3.8 (reserve criterion; the loopy Theorem 1.11(b)).** (K21, 2026-10-27). Let Y = (G_1, …, G_k), B ≥ 1. If for every j and every σ for which
some reachable node of G_j has an event of sign σ,

  Σ_{i≠j} Λ_B(G_i) ≤ B − 1 (σ = +),  Σ_{i≠j} P_B(G_i) ≤ B − 1 (σ = −),

then Y is first-event dominant for B, so by Theorem 3.7 the D-result of ⊞ is the CGT outcome of Σ y_i^B at every reachable position.

## Theorem 3.11 (statement only)

**Theorem 3.11 (sandwich).** (K21, 2026-10-27). Let K be any D-game (loopy allowed) and S a D-game none of whose options is a terminal of its own mover (no Left option ⊕, no Right
option ⊖; suicides are allowed, as for the deleted Z-moves of a frozen group; every terminal-free S qualifies, stopper or not). Then for every k, s and mover:

  (k, mover) ∈ W(K ⊞ off) ⇒ (k, s, mover) ∈ W(K ⊞ S) ⇒ (k, mover) ∈ W(K ⊞ on),
  (k, mover) ∈ L(K ⊞ on) ⇒ (k, s, mover) ∈ L(K ⊞ S) ⇒ (k, mover) ∈ L(K ⊞ off),

and W(K ⊞ off) = W(K ⊞ dud), L(K ⊞ on) = L(K ⊞ dud). Call P_L(K, mover) = "Left wins K ⊞ off" (Left can force a decisive event against a Right who may pass) and
P_R(K, mover) = "Right wins K ⊞ on". For short K these are the predicates Λ and Ρ of Theorem 3.4.


