# K51 blind packet: definitions and the statement of Theorem 3.4 only (from kings/theory/LOOPY.md at commit ef1314c3)

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



## Definition 3.1

**Definition 3.1 (pass reservoirs).** Each reservoir is a D-game with a single position ω.
- **on_D:** L(ω) = {ω}, R(ω) = ∅. White can pass forever; Black has no move.
- **off_D:** the mirror image.
- **dud_D:** L(ω) = R(ω) = {ω}.


## Theorem 3.4 (statement only)

**Theorem 3.4 (outcome rules with passes).** Let G be a short D-game under normal play, and write x
for its positions.

- **(a) Both sides may pass (G ⊞ dud_D).** Define predicates by induction over G's acyclic order:
  - Λ_L(x) ⟺ some Left option of x is ⊕, or is a position x^L with Λ_R(x^L);
  - Λ_R(x) ⟺ Λ_L(x), and every Right option x^R of x is ⊕ or satisfies Λ_L(x^R).

  Then r(x, s) = W iff Λ_s(x). Define Ρ_R and Ρ_L symmetrically for Black; r(x, s) = L iff Ρ_s(x).
  Otherwise r(x, s) = D. Consequences:
  - having the move never hurts: Λ_R ⇒ Λ_L, so there is no zugzwang;
  - if G has no terminals, every position is drawn;
  - in words, **a side wins iff it can force a decisive event against an opponent who may pass at any time;
    otherwise the game is drawn.**
- **(b) Only White may pass (G ⊞ on_D).** There are no draws. Define:
  - Ρ′_R(x) ⟺ some Right option of x is ⊖, or is a position x^R with Ρ′_L(x^R);
  - Ρ′_L(x) ⟺ Ρ′_R(x), and every Left option x^L of x is ⊖ or satisfies Ρ′_R(x^L).

  Then r(x, s) = L iff Ρ′_s(x), and r(x, s) = W otherwise. In words, **Black wins iff Black can force a
  decisive event against a White who may pass at any time.** Black cannot pass, so it loses whenever it runs
  out of moves. White can never be in zugzwang.
- **(c) Only Black may pass (G ⊞ off_D).** The mirror image of (b).

