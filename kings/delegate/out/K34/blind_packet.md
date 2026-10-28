# K34 blind packet: definitions and statements only (extracted from kings/theory/LOOPY.md at commit 774036f)

Proofs, remarks, checks and verification notes are omitted on purpose. Do not read LOOPY.md itself until Phase 2.

## §1.2 (Definitions 1.1–1.5)

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

**Definition 1.5 (four models of a king-and-pawn position X).**
- **C(X), chess.** The rules of `kings/SPEC.md`: checkmate wins, stalemate is a draw, infinite play is a draw.
- **P(X), the promotion model.** Chess, except that the first promotion ends the game as a win for the
  promoter. Stalemate and infinite play are still draws.
  - `kpsolve --frozen` computes the frozen-king model F of Corollary 2.7′ (a king move loses at once for the mover), not P. P itself, with free kings, is computed by K7's build `kings/delegate/out/K7/scripts/draft/kp_p.c` (its flag is `--pmodel`; `kings/kpsolve.c` has no such flag) and by the independent solvers of K19 and K24 (revised after K24, 2026-10-27: this line used to say that `--frozen` computes P).
- **D(X), the decisive-event model.** A D-game. Its positions are the positions before the first decisive
  event. Its terminals are the decisive events:
  - a passer appears (as in `cylcgt`), with races scored by a race rule;
  - a punished move in the king group (§2). Under (V3) of Theorem 1.14 *every* move inside Z is a punished
    move, so the king group then contributes only suicides and is deleted by Lemma 1.7; the setup of
    Theorem 1.14 and this definition agree under (V3) (revised after review: R2 item 10).
- **S(X), the BIG convention.** The BIG value of X: at every node of the game tree the position is split
  into its components (files separated by an empty file, and an empty file stays empty), each component is
  translated separately, and the translations are summed; a component with a passer is worth ±BIG, races being
  scored by the race rule. This is the value `cylcgt.pawns.value` computes (COMPUTED-1, `cylcgt/pawns.py`).
  - *What S(X) is not* (revised after review: R2 item 2): it is not the BIG translation D(X)^B of the D-game of
    §1.2, in which the components are those of the root and the first decisive event ends the whole play.
    `cylcgt` re-splits at every node, and a passer freezes only its own component, so the two differ as soon
    as a component splits. Example: flat 7×6, e.p. on, count rule, `W: b2 d3 f2 / B: c4 c5 e5 g5` is one
    component at the root, yet o(S) = 𝓝 while the decisive-event result is 𝓡 (COMPUTED-1, `lemmas/common.py`:
    o(S) = N, o(W) = R).
  - The re-splitting is why (V4) of Theorem 1.14 has to be checked hereditarily; see Theorem 1.11(c).

The models are connected by bridges, each with its own hypotheses:

*Notation.* o(G) is the outcome class of a CGT game G (𝓛, 𝓡, 𝓝, 𝓟); W(X) is the whole-board convention game
of a pawn position X, in which the first passer ends the game (`notes/lemmas.md`); S(X) is the BIG value of
§1.5; and HSS, hereditary sum-safety, is the hypothesis (HSS) of Theorem 1.11(c). (Revised after review:
R1 item 11: §6 used o(W(X)) and "hereditarily sum-safe" without defining them.)

```
S  --Thm 1.11(c) (V4)-->  D  --Thm 1.14 (V1-V3)-->  P  --(A_Q)(X)-->  C
```

**Axiom (A_Q)(X) (per-position hypothesis, checked by kpsolve).** For a fixed position X: if X is a P-win
for σ, then X is a C-win for σ.
- **FALSE as a general statement (revised after review: R1 item 6, R2 item 8).** cyl:7×6 `Ke2 Pb5 ka5 w -` is
  a P-win (b6=Q at once; `kpsolve --frozen` gives W W) and a chess draw (exact D D: every White move draws);
  flat:4×4 `Kd1 Pb3 ka3 w -` is the same (b4=Q is met by Kxb4). So (A_Q) is not an axiom: it is a hypothesis
  to be checked at each position, and every "PROVED in P" claim below is a chess claim only where it holds.
- *Evidence for:* the cylinder KQK tables agree in two independent solvers ([RESULTS.md](../../RESULTS.md) §2:
  KQK is 100% won on the 8×8 cylinder).
- *Evidence against, in general:* L4.4 of `notes/lemmas.md` is a promotion race lost to a promotion with check.
- *Settled by:* kpsolve with `--cap 1` computes C exactly whenever its bounds agree (A = B), and `--frozen`
  computes P; the two runs decide (A_Q)(X) for that X.


## Definition 2.1

**Definition 2.1 (king group, buffer).** A *king group* Z consists of:
- a set F_Z of files (an arc on a cylinder);
- both kings and some pawns, the Z-pawns, all on F_Z.

All other pawns, the *context*, stand on files at distance ≥ 2 from F_Z. The files at distance exactly 1
are pawn-free; they are the *buffer*. A *Z-move* is a move of a king or of a Z-pawn.
- On the 7×6 cylinder with F_Z = {a, b, c}, the buffer is {d, g} and the context lies on {e, f}.

## Lemma 2.2 (statement only)

**Lemma 2.2 (buffer invariance). PROVED.** Before the first promotion:
- no pawn ever stands on a buffer file;
- context pawns stay on context files, and Z-pawns stay on F_Z;
- hence a king standing on F_Z is never attacked by a context pawn, and a context pawn never attacks a
  square of F_Z.

## Definition 2.5

**Definition 2.5 (decisive punishment, in chess terms).** A Z-move m of side s, made at a chess position Y
(context plus Z), is *decisively punished* if the opponent s̄ has a forced win in P (or in C) from the
position after m. The win must hold against every defence of s:
- s's moves in the context, including creating passers, starting races and capturing en passant;
- s's king going anywhere, back into Z or into the context;
- s promoting;
- s steering for stalemate.

"Whatever the other components contain" means: for every context in the class one claims the zero for.
Theorem 2.4(b) needs this only at positions where s is losing the context.

## Definition 3.1

**Definition 3.1 (pass reservoirs).** Each reservoir is a D-game with a single position ω.
- **on_D:** L(ω) = {ω}, R(ω) = ∅. White can pass forever; Black has no move.
- **off_D:** the mirror image.
- **dud_D:** L(ω) = R(ω) = {ω}.

Their CGT analogues are on = {on | }, off = { | off} and dud = {dud | dud} (KNOWN: [WW] ch. 11 "Games
Infinite and Indefinite"; [S] ch. VI). Also KNOWN [S, ch. VI]:
- on exceeds every number;
- on, off and over are stoppers, while dud is not;
- G + dud is a draw for every G in which only running out of moves decides the game.

## Proposition 3.2 (statement only)

**Proposition 3.2 (a shuttling king is a pass). PROVED.** Let Z be a king group and z ↔ z′ two non-capturing
White king moves inside F_Z, with:
- in both z and z′, every Black Z-move a suicide in the D-model;
- the two shuttle moves legal in every context, which Lemma 2.2 guarantees, since they stay on F_Z.

Then, in the D-model and for a short context G, r(G ⊞ Z) ≥ r(G ⊞ on_D), with equality if White has no other
Z-moves. (Two shuttles, one for each king: Proposition 3.2′ below.)

## Theorem 1.14, sharp form (setting and statement only)

*Setting.*
- A *P-position* is a chess position before the first promotion, with the side to move. σ is one side and σ̄ the
  other. A *P-win for σ* is a forced win in finitely many moves (the least fixed point, as in Definition 1.2):
  a promotion by σ or a checkmate of σ̄. Stalemate and infinite play are not wins. The defining clauses are:
  - with σ to move, a position is a P-win if σ has a legal move that promotes or leads to a P-win;
  - with σ̄ to move, a position is a P-win if σ̄ is not stalemated (it has a legal move, or it is in check) and
    every legal move of σ̄ leads to a P-win (so none of them promotes).
- Fix a D-game D (Definition 1.1, possibly loopy) and a map π from P-positions to the positions of D that keeps
  the side to move. For D(X) of Definition 1.5, π is the identity. D(X) can be fixed in two ways, and the theorem
  below holds for both and for any other D:
  - (a) every Z-move is a terminal for the opponent of the mover, as under (V3);
  - (b) Z is a loopy component. Its terminals are the P-punished Z-moves (Definition 1.5), and its other
    Z-moves are ordinary options: the shuttle of Z_onT1 is `on_D`.

  For the chess bridge after Proposition 3.2, D = G ⊞ on_D and π sends both shuttle states to ω. For the two-sided
  bridge (Theorem 3.2‴), D = G ⊞ dud_D and π sends all four combined king states to ω.
- A legal chess move y → y′ is a *D-move* if it does not promote and π(y′) is a D-option of π(y). Legal chess
  moves that are not D-moves may exist, and so may D-options that are not legal chess moves (the move Kd5 of
  §5.4 when e4 covers d5). Both are allowed.
- W_σ is the set of D-positions (x, s) from which σ forces a D-win in finitely many moves: the least fixed
  point of "(x, σ) ∈ W_σ if some option is the σ-terminal or lies in W_σ; (x, σ̄) ∈ W_σ if every option is the
  σ-terminal or lies in W_σ" (with no option, σ̄ loses by normal play). ρ(x, s) is the stage at which (x, s)
  enters, and ρ = ∞ outside W_σ. So every option of a σ̄-node of W_σ is the σ-terminal or lies in W_σ with
  smaller ρ, and every σ-node of W_σ has such an option. Write ρ(y) for ρ(π(y), side to move at y).

*Statement.* A legal move is *closing* if it promotes with σ or leads to a P-win for σ. A set N of P-positions is
*σ-certified* if ρ(y) < ∞ for every y ∈ N and, for every y ∈ N:
- **(S1)** (σ to move) σ has a legal move that is closing, or is a D-move to some y′ ∈ N with ρ(y′) < ρ(y);
- **(S2)** (σ̄ to move) every legal move of σ̄ is closing, or is a D-move to some y′ ∈ N;
- **(S3)** (σ̄ to move) σ̄ is not stalemated.

**Theorem 1.14, sharp form.** If a σ-certified set N contains X, then X is a P-win for σ.

## Proposition 3.2′ (statement only)

**Proposition 3.2′ (two shuttling kings are a dud). PROVED (new, K14, 2026-10-27; revised after the K14 referee,
2026-10-27: the D-model part was re-checked by one referee (same model family) and by two brute-force implementations,
on short and loopy G).**

*Two-shuttle component.* Let Z be a D-game with four distinct positions (a, b), a ∈ {z, z′}, b ∈ {w, w′}. Write ā for
the other of z, z′ and b̄ for the other of w, w′. In chess z, z′ and w, w′ are the two shuttle squares of the White and
the Black king, and the four positions are the four combined king states. In each of the four positions:
- **(T1)** (ā, b) is a Left option (White's shuttle);
- **(T2)** (a, b̄) is a Right option (Black's shuttle);
- **(T3)** every other Left option is ⊖ (a suicide);
- **(T4)** every other Right option is ⊕ (a suicide).

Z may have further positions. Let G be any D-game (short or not) and x a position of G.
- **(a) Equality.** Under (T1)–(T4), for all four states (a, b) and both sides to move, r(G ⊞ Z) at (x, (a, b)) equals
  r(G ⊞ dud_D) at (x, ω). For short G the value is given by Theorem 3.4(a): a side wins iff it can force a decisive
  event against an opponent who may pass at any time, and otherwise the game is drawn. There is no zugzwang
  (Λ_R ⇒ Λ_L), and a G without terminals is a draw.
- **(b) Further Z-moves.** Under (T1), (T2), (T4) (White may have further Z-moves, of any kind, even to new positions),
  r(G ⊞ Z) ≥ r(G ⊞ dud_D) in the order L < D < W. Under (T1), (T2), (T3), r(G ⊞ Z) ≤ r(G ⊞ dud_D). If both sides have
  further moves there is no comparison in general. The inequalities can be strict (a further White option ⊕ at
  (z, w) makes G = 0 a White win, against D for dud_D).
- **(c) Half-slice.** Suppose only (T2) and (T4) hold, and only at (z, w) and (z, w′), and everything else in Z is
  arbitrary. If r(G ⊞ dud_D) = W at (x, ω) for a side to move s, then r(G ⊞ Z) = W at (x, (z, w)) and at (x, (z, w′))
  for the same s. Mirror: (T1), (T3) at (z, w) and (z′, w) transfer a Black win. So *a win needs only the half of the
  four states in which the winner's king stands still*; the draws, and the exact equality (a), need all four.
- **(d) Each shuttle arrow is needed.** Take G = 0 (one position, no options), where r(G ⊞ dud_D) = (D, D).
  - *Opposition.* Delete the diagonal state (z′, w′) (the kings would touch). Then (z′, w) has no Black shuttle and
    (z, w′) has no White shuttle; their only options are suicides. At (z, w) the pair is (W, L): White to move goes to
    (z′, w) and Black must suicide, Black to move goes to (z, w′) and White must suicide. The first player wins.
  - *One arrow.* Delete Black's shuttle at (z′, w) only: the pair at (z, w) is (W, D).
  - *Every arrow.* Deleting any one of the eight shuttle arrows from an otherwise exact Z changes the result in a
    positive fraction of random instances, and at G = 0 it changes the result at all four states (the referee's table of
    all eight deletions; COMPUTED-1).


## Lemma B (statement only)

**Lemma B (the winner of G ⊞ dud_D never passes).** Let (x, ω, σ) be in W^σ of G ⊞ dud_D, entering at stage n. Then
some option that makes it enter at stage n is a G-move (a σ-terminal of G or a position (x′, ω) with σ̄ to move and
stage ≤ n − 1).

## Lemma 3.2″ (statement only)

**Lemma 3.2″ (four-state geometry; PROVED).** Let z ≠ z′ and w ≠ w′ be empty squares of F_Z, z, z′ adjacent and w, w′
adjacent, such that (K1) no Black Z-pawn attacks z or z′ and no White Z-pawn attacks w or w′, and (K2) the king distance
d(a, b) ≥ 2 for all four (a, b) (the kings never touch). Then, in every context (files at distance ≥ 2 from F_Z), with
the Z-pawns unmoved and the kings on {z, z′} and {w, w′}: neither king is in check, both shuttle moves are legal
(whatever the other king's square), and each side has a legal move, so nobody is stalemated.

## Theorem 3.2‴ (statement only)

**Theorem 3.2‴ (chess bridge for two shuttles; PROVED in P, conditional on the stated hypotheses; the chess statement adds
(A_Q)(X) as always).** Let X be a K+P position
with a king group Z satisfying (K1), (K2), the kings on {z, z′} and {w, w′}, and a context with D-model G (the pawn-only
game of Definition 1.5, with the e.p. flag as in the Remark). Let D = G ⊞ dud_D, with π sending a chess position to
(x, ω) and keeping the side to move. A *regular* position is one reachable from X by D-moves (matching context moves and
the two shuttles). Assume, at every regular position:
- **(V1a-ctx)** the legal context moves of the side to move are exactly G's options for that side, with the same
  resulting positions (e.p. through condition (E)); the shuttle is the pass;
- **(V2-ctx)** every decisive event of G leads to a P-win for its beneficiary (automatic for a pawn-only G scored by
  promotions);
and write **(Pun_s)** for: *every legal move of s that is neither a context move nor s's shuttle (a king move off the
shuttle, a Z-pawn move or capture) is decisively punished (Definition 2.5): the position after it is a P-win for s̄.*
- **(a) Win transfer.** Suppose r_D(x, ω, s) = W. Let Σ be a rank-lowering White strategy in D (by Lemma B it never
  passes) and N the set of chess positions arising when White plays Σ as chess moves and Black plays any legal D-move.
  If (Pun_Black) holds at the nodes of N with Black to move, then White wins X in P. White's king stays on its square, so
  only the two states (a, w), (a, w′) occur; White's shuttle and the square z′ are not used. The mirror statement for a
  Black win needs (Pun_White) at the nodes of N with White to move.
- **(b) Exactness.** If (Pun_White) and (Pun_Black) hold at all regular positions, the P-result of every regular
  position equals r_D(π(y)), draws included. In particular, if G has no decisive event, X is a draw in P.


