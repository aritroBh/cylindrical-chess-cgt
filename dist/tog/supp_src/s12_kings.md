**How the statements were checked.** The labels are used as follows. PROVED: a hand proof is given in this section. CHECKED-2: a finite computation on which two or more independently written programs agree. COMPUTED-1: a computation by one program. CONJECTURE: a statement supported by evidence only. KNOWN marks a result from the literature, cited and not proved again. The hand proofs were checked by AI referees; no human referee has checked them yet. A referee from a different model vendor than the writer checked the sharp form of Theorem 1.14, Theorem 2.7, Corollary 2.7′, Lemma 2.9 (an audit of the written proof), Proposition 2.11, Theorem 2.11K, Proposition 3.2′, Lemma 3.8a and Theorems 3.7, 3.8 and 3.11; the other proofs were checked by referees of the writer's model family. Below, a check is mentioned only where a specific computation supports a specific claim. References to §4–§8 and to Appendix A are to later parts of the source note, which are not reproduced here.

## 1. Chess semantics versus CGT semantics

### 1.1 Notation

- **Board.** W files × H ranks, flat or cylinder, with the rules of `kings/SPEC.md`. d(x, y) is the king
  distance: max(file distance, rank distance), with cyclic file distance on a cylinder.
- **Players.** White = Left, Black = Right.
- **Result pairs.** (r_w, r_b) lists the result with White to move, then with Black to move. Each entry is
  W, D or L **from White's point of view**, as kpsolve prints them.
- **Outcome classes** of a short CGT game (KNOWN; *Winning Ways* [WW] ch. 1, Siegel [S] ch. I–II):
  - 𝓛 = (W, W);
  - 𝓡 = (L, L);
  - 𝓝 = (W, L): the first player wins;
  - 𝓟 = (L, W): the second player wins.

  Short games have no draws.

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
  - `kpsolve --frozen` computes the frozen-king model F of Corollary 2.7′ (a king move loses at once for the mover), not P. P itself, with free kings, is computed by a separate build of the solver, `kp_p` (its flag is `--pmodel`; `kings/kpsolve.c` has no such flag), and by two further, independently written solvers.
- **D(X), the decisive-event model.** A D-game. Its positions are the positions before the first decisive
  event. Its terminals are the decisive events:
  - a passer appears (as in `cylcgt`), with races scored by a race rule;
  - a punished move in the king group (§2). Under (V3) of Theorem 1.14 *every* move inside Z is a punished
    move, so the king group then contributes only suicides and is deleted by Lemma 1.7; the setup of
    Theorem 1.14 and this definition agree under (V3).
- **S(X), the BIG convention.** The BIG value of X: at every node of the game tree the position is split
  into its components (files separated by an empty file, and an empty file stays empty), each component is
  translated separately, and the translations are summed; a component with a passer is worth ±BIG, races being
  scored by the race rule. This is the value `cylcgt.pawns.value` computes (COMPUTED-1, `cylcgt/pawns.py`).
  - *What S(X) is not:* it is not the BIG translation D(X)^B of the D-game of
    §1.2, in which the components are those of the root and the first decisive event ends the whole play.
    `cylcgt` re-splits at every node, and a passer freezes only its own component, so the two differ as soon
    as a component splits. Example: flat 7×6, e.p. on, count rule, `W: b2 d3 f2 / B: c4 c5 e5 g5` is one
    component at the root, yet o(S) = 𝓝 while the decisive-event result is 𝓡 (COMPUTED-1, `lemmas/common.py`:
    o(S) = N, o(W) = R).
  - The re-splitting is why (V4) of Theorem 1.14 has to be checked hereditarily; see Theorem 1.11(c).

The models are connected by bridges, each with its own hypotheses:

*Notation.* o(G) is the outcome class of a CGT game G (𝓛, 𝓡, 𝓝, 𝓟); W(X) is the whole-board convention game
of a pawn position X, in which the first passer ends the game (`notes/lemmas.md`); S(X) is the BIG value of
§1.5; and HSS, hereditary sum-safety, is the hypothesis (HSS) of Theorem 1.11(c).

```
S  --Thm 1.11(c) (V4)-->  D  --Thm 1.14 (V1-V3)-->  P  --(A_Q)(X)-->  C
```

**Axiom (A_Q)(X) (per-position hypothesis, checked by kpsolve).** For a fixed position X: if X is a P-win
for σ, then X is a C-win for σ.
- **FALSE as a general statement.** cyl:7×6 `Ke2 Pb5 ka5 w -` is
  a P-win (b6=Q at once; `kpsolve --frozen` gives W W) and a chess draw (exact D D: every White move draws);
  flat:4×4 `Kd1 Pb3 ka3 w -` is the same (b4=Q is met by Kxb4). So (A_Q) is not an axiom: it is a hypothesis
  to be checked at each position, and every "PROVED in P" claim below is a chess claim only where it holds.
- *Evidence for:* the cylinder KQK tables agree in two independent solvers (`RESULTS.md` §2:
  KQK is 100% won on the 8×8 cylinder).
- *Evidence against, in general:* L4.4 of `notes/lemmas.md` is a promotion race lost to a promotion with check.
- *Settled by:* kpsolve with `--cap 1` computes C exactly whenever its bounds agree (A = B), and `--frozen`
  computes P; the two runs decide (A_Q)(X) for that X.

### 1.3 Two lemmas about options

**Lemma 1.6 (option monotonicity). PROVED.** Let A′ be obtained from a D-game A by adding Left options or
deleting Right options at some positions. Then r_{A′}(x, s) ≥ r_A(x, s) for all x and s, in the order
L < D < W.

*Proof.*
- Every White strategy in A is a White strategy in A′, because White has at least the same options there.
- Every Black reply in A′ is also available in A, because Black's options there are a subset.
- So a strategy that forces a win in A forces it in A′, and a strategy that avoids losing in A avoids losing
  in A′. ∎

**Lemma 1.7 (suicide deletion, normal play only). PROVED.** Deleting a Left option equal to ⊖ (a "suicide")
does not change any result. The same holds for Right options equal to ⊕.

*Proof.* r(x, Left) is the best result over Left's options, and a move to ⊖ yields L, the worst.
- If Left has another option, the maximum is unchanged.
- If ⊖ was Left's only option, deleting it leaves Left with no option. Under normal play Left then loses:
  the result is L again. ∎

**Remark 1.8 (what the trébuchet is for).** In chess the second case of Lemma 1.7 fails: a side with no
legal move is **stalemated**, which is a draw.
- The convention's normal-play rule "a side with no pawn move loses" is therefore correct in chess only
  because the king group always offers that side a legal move, and that move is a suicide.
- The trébuchet's real job is to turn stalemate into a loss.
- §5.4 gives a position where a context pawn takes away the only suicide square. The convention says
  "White wins" and the truth is a draw.

### 1.4 What BIG can and cannot do

**Theorem 1.9 (one component). PROVED.** For a short D-game A and every B ≥ 1, the outcome class of A^B at
x equals the D-result pair of A at x.

*Proof.* Induction on the height of x.
- The integer B ≥ 1 is in 𝓛. Moving first, Left moves to B − 1 ≥ 0, where Right has no move. Moving second,
  Right has no move at all.
- Likewise −B is in 𝓡.
- So an option to ⊕ (resp. ⊖) in A corresponds to an option in 𝓛 (resp. 𝓡) in A^B. That is exactly
  "White wins (resp. loses) from it whoever moves next".
- An option to a non-terminal y has matching classes by induction.
- "Left wins moving first" holds iff some Left option is won by Left with Right to move, in both games.
  The same holds for Right.
- A player with no option loses in both games. ∎

In one component of the D-model the convention cannot go wrong: after the first ±B nothing else happens.
Trouble needs at least two components (compare L2.3 of `notes/lemmas.md`). That is *not* true of the re-splitting model S of §1.5: there a single component can still fail, because
a passer in one sub-part does not end its sibling, so trouble needs a later split, not two components. Example:
flat 7×6, e.p. on, count rule, `W: b2 d3 f2 / B: c4 c5 e5 g5` is one component at the root, yet o(S) = 𝓝 while
the decisive-event result is 𝓡 (COMPUTED-1, `lemmas/common.py`).

**Definition 1.10 (tempo counts, threats, dominance).** Let Y = (y₁, …, y_k) be a position of a sum of short
D-games.
- **Tempo counts.** M_L(y) is the largest number of Left moves in any sequence of moves from y (moves by
  both sides, in any order, not necessarily alternating), counting a final move into a terminal. M_R(y) is
  defined the same way for Right. Both are monotone: M(y′) ≤ M(y) whenever y′ is reachable from y.
  - For a sum, M_L(Y) is the sum of the M_L of the coordinates: the coordinates are played independently, so a
    longest sequence of Left moves in the sum is the concatenation of longest sequences in the coordinates.
    (The other reading — stop counting at the first terminal of the whole sum — gives a smaller number, so a
    hypothesis stated with it would be weaker; the proofs below use this component reading, and the count of the opponent's moves in the proof of Theorem 1.11(b) is exactly this one.)
  - In the pawn game every White move advances a White pawn by at least one rank, so
    M_W ≤ Σ_white pawns (H − rank) ≤ (H − 2)p for p legal White pawns. That is ≤ 6p, so ≤ 48 on 8 ranks when
    p ≤ 8, and ≤ 6p in general; BIG = 256 exceeds 6p whenever p ≤ 42. The count ignores a final Z-move, so
    add 1 where a move inside the king group is possible.
- **Threats.** τ(y) ⊆ {+, −} contains + iff some position reachable from y without passing a terminal has an
  option ⊕ **by either player**; it contains − iff some such position has an option ⊖ by either player. So a
  move into the opponent's terminal is a threat for the opponent, and a suicide counts for the side that
  gains from it. Like M, τ is monotone: τ(y′) ⊆ τ(y) whenever y′ is reachable from y.
  - This is the τ of `notes/lemmas.md` (Definition 2.0) and of `lemmas/common.py: threats`, which count a passer created by either side's move. A τ that counted only Left options to ⊕ and Right options to ⊖ would be blind to suicides.
- **First-event dominance.** Y is *first-event dominant for B* if the following holds for every Y′ reachable
  from Y without passing a terminal, and every option y′_j → σ (σ ∈ {⊕, ⊖}, by either player):
  - the CGT position σB + Σ_{i≠j} (y′_i)^B is won by σ's player whoever moves first;
  - here σB means +B if σ = ⊕ and −B if σ = ⊖.

**Theorem 1.11 (sums). PROVED.**
- **(a)** If Y is first-event dominant for B, then the outcome class of Σ y_i^B equals the D-result pair of
  ⊞ y_i.
- **(b)** Y is first-event dominant for B if both of the following hold:
  - *pairwise safety:* no reachable Y′ has two different coordinates with + ∈ τ(y′_i) and − ∈ τ(y′_j), with
    the τ of Definition 1.10 (an option to ⊕ or ⊖ counts whoever makes it);
  - *the bound:* B > max(M_L(Y), M_R(Y)).

*Proof.*
- **(a)** Induction on the total height.
  - At a reachable non-terminal Y′, each option of the CGT sum is one of two kinds.
    - A move in some y′_j to a non-terminal position. The induction hypothesis applies to it.
    - A move to the integer σB in coordinate j, giving σB + Σ_{i≠j} (y′_i)^B. By dominance this is in 𝓛 if
      σ = ⊕ and in 𝓡 if σ = ⊖. That is exactly the status of the D-option "σ wins now".
  - No other options exist, because no integer summand is present yet.
  - So the options correspond one to one with the D-options of Y′, with the same "won by Left with Right to
    move" status. The same holds on the Right side.
  - A player with no option loses in both.
- **(b)** Take σ = ⊕; the case σ = ⊖ is symmetric.
  - Let Y′ be reachable from Y without passing a terminal, and let y′_j → ⊕ be the option, made by either
    player. Since the option exists, + ∈ τ(y′_j) (Definition 1.10: an option counts whoever makes it). By pairwise safety no other coordinate has − ∈ τ(y′_i); by monotonicity of τ no other coordinate can
    ever reach ⊖, so no option of the sum Σ_{i≠j}(y′_i)^B is −B. This step needs the τ of Definition 1.10: a τ that counted only Left options to ⊕ would be blind to a ⊕ entered by Right.
  - The frontier position is B + Σ_{i≠j}(y′_i)^B, and the positive integer B has canonical form {B−1 | } (a
    Left-only stack of B moves, [WW] ch. 2), so Right has no move in it.
  - Left's strategy: on every turn, play in a positive integer summand (the B created by the event, or a +B
    created later), and never in a component.
  - Right's moves are all moves in the components, and there are at most M_R(Y) of them: the moves in one
    coordinate form a sequence of moves in that coordinate, so the total is at most Σ_{i≠j} M_R(y′_i) ≤ M_R(Y)
    (M is monotone, and for a sum M is the sum over the coordinates). A Right move into a terminal can only
    create another +B, because −B is unreachable.
  - Left needs at most M_R(Y) + 1 moves: one reply to each Right move, plus one more if Left moves first at
    the frontier. The first stack has B ≥ M_R(Y) + 1 moves, so Left has a move at every turn of its own.
    The stack can reach 0 = { | } only with Left's last move: reaching 0 takes B ≥ M_R(Y) + 1 Left turns, so
    by then Right has made M_R(Y) moves, the most it can make, and Right, to move, has no move. Right runs out of moves first and loses, whoever started. ∎

**(c) The re-splitting version.** Let X be a pawn position, let S(X) be its
BIG value computed with re-splitting (§1.5), and let D(X) be the decisive-event game of X, in which the
position is split into its components at every node, a move is a move in one component, and the first decisive
event ends the play. Suppose:
- **(HSS)** at every position Y reachable from X before the first decisive event, the components of Y are
  pairwise safe (Definition 1.10: an option to ⊕ or ⊖ counts whoever makes it); and
- **(B)** BIG exceeds every tempo count of every such Y.

Then the outcome class of S(X) is the outcome class of the D-result pair of D(X).

*Proof.* Unfold S(X) as a game form F whose positions are pairs (Y, N), where Y is a pawn position (the live
components) and N is a finite multiset of frozen integers ±B. A move is either a move in an integer summand or
a pawn move in a live component Z; if that move creates a passer (or a race) in Z, then Z leaves Y and ±B joins
N; otherwise Z is replaced by its new components. This is `cylcgt.pawns.value` unfolded.
- **Frontier.** Let (Y, {σB}) be a position of F in which no live component has a (−σ)-threat and
  B > M_{−σ}(Y), where M_{−σ} is the tempo count of the opponent of σ (M_L for White, M_R for Black). Then σ
  wins F(Y, {σB}) whoever moves first. Take σ = +; the case σ = − is symmetric. σ's strategy is to move in the
  positive integer summand on every turn, which is possible while it has a move left; the opponent cannot move
  in a positive integer (its canonical form is {B−1 | }), and every integer frozen later is +B, because a −B
  would need a − threat and a race needs both threats. So every opponent move is a pawn move in a live
  component, and the opponent has at most M_{−σ}(Y) moves in all. σ needs at most M_{−σ}(Y) + 1 moves (one
  reply to each opponent move, plus one if σ moves first), and the first stack has B ≥ M_{−σ}(Y) + 1, so σ
  has a move at every turn of its own and the opponent runs out of moves first. The stack can reach
  0 = { | } only with σ's last move: that takes B ≥ M_{−σ}(Y) + 1 turns of σ, so by then the opponent has made
  all M_{−σ}(Y) of its moves.
- **Induction.** o(F(Y, ∅)) = o(D(Y)) for every non-terminal Y reachable from X, by induction on the total
  number of pawn moves Φ(Y). Take a move of Y, made in component Z.
  - If the child is non-terminal, both models give the child and the induction hypothesis applies.
  - If the move creates a σ-passer, or a race scored σ, then D gives the terminal σ, which σ wins whoever
    starts. F gives (Y″, {σB}), where Y″ consists of the other components of Y. Here σ ∈ τ(Z): Z reaches the
    passer in one move, and for a race both signs are in τ(Z). Y is pairwise safe by (HSS), so no other live
    component has a (−σ)-threat, and the frontier step applies because M_{−σ}(Y″) ≤ M_{−σ}(Y) ≤ M_{−σ}(X) < B.
    So σ wins this option too.
  - Race scores agree: before the move Y had no passer, a move changes one component only, and passedness is
    local, so all passers of the child lie in Z and the promotion distances are the same in both models.
Outcomes are determined by the outcomes of the options, so o(F(Y, ∅)) = o(D(Y)). ∎

Re-splitting does not change the D-result: it only re-groups the same positions and options, and the D-result
of Definition 1.2 depends on the game graph and the terminals, not on the grouping. So the D-result pair of
the re-splitting D(X) is the one used in Theorem 1.14(i).

Theorem 1.11(b) is the fixed-sum version of L2.1: its coordinates are the components of the root and never
split. The re-splitting version is (c) above, and the test "hereditarily sum-safe" of `notes/lemmas.md` is
(HSS), not pairwise safety at the root: it re-checks the re-split components at every reachable position, and it
uses the either-player τ.

**Proposition 1.12 (opposite threats cancel for every B). PROVED.** Let A = {⊕ | ∅} and A′ = {∅ | ⊖}.
- **In chess semantics,** A ⊞ A′ is 𝓝: whoever moves wins at once.
- **In the BIG translation,** A^B + A′^B = {B | 0} + {0 | −B} = 0, which is 𝓟, for every B ≥ 1.

*Proof of the BIG part.*
- Left moving first has two choices.
  - Left goes to B + {0 | −B}. Right answers −B, the total is B − B = 0, and Left is to move and loses.
  - Left goes to {B | 0} + 0. Right answers 0, and Left loses again.
- Right moving first loses by symmetry. So the sum is a 𝓟-position, and a 𝓟-position equals 0 (KNOWN:
  [WW] ch. 1, [S] ch. II). ∎

The 10 multi-component disagreements in `crosscheck/` and the counterexamples to `sum_safe` in L2.2 of
`notes/lemmas.md` are pawn-game instances of this mechanism.

**Proposition 1.13 (BIG must be at least the tempo count; sharp). PROVED.**
Let A′ = { | ⊖} be a Black threat (no Left option at all) and R_n be n consecutive one-shot White moves with
no terminals (the integer n).
- **In chess semantics,** A′ ⊞ R_n is 𝓡 for every n ≥ 1: White can only spend tempi, and Black plays ⊖ when
  on move. (For n = 0 White has no move at all; the D-model scores that as a loss for White, while chess
  scores it as a stalemate, a draw.)
- **In the BIG translation,** A′^B = { | −B} = −B − 1 (KNOWN: {| x} = x − 1 for a number x, [WW] ch. 1), so
  { | −B} + n has three regimes:
  - 𝓡 if n ≤ B;
  - 𝓟 if n = B + 1;
  - 𝓛 if n ≥ B + 2.
- **The other reading of ∅.** With A′ = {∅ | ⊖}, where ∅ is the dead position of Definition 1.1, the
  translation is {0 | −B} and the regimes are different: {0 | −B} + n is 𝓝 for n ≤ B and 𝓛 for n ≥ B + 1
  (COMPUTED-1, `cylcgt.cgt`, B = 4: N, N, N, N, N, L, L, L for n = 0..7). The two readings must not be mixed: with both at once, the claim is false.

*Proof of the BIG part.* { | −B} + n is the integer n − B − 1, and the outcome class of an integer m is 𝓛 if
m ≥ 1, 𝓟 if m = 0 and 𝓡 if m ≤ −1.
- Right moving first goes to n − B. Left, to move, wins iff n − B ≥ 1.
- Left moving first goes to n − 1 + { | −B}. Right answers n − 1 − B. Left, to move, wins iff
  n − 1 − B ≥ 1. ∎

So BIG must be large compared with the tempo counts. In Proposition 1.13 the BIG outcome is right exactly when
n ≤ B, and Theorem 1.11(b) asks for B > M, so that the owner of the stack wins even when it must move first.
With BIG = 256 and pawns only, B > M holds as long as p ≤ 42, since M ≤ 6p (and M ≤ 48 on 8 ranks when
p ≤ 8). With a shuttling king the tempo count is infinite, and no BIG works (§3).

### 1.5 The exact validity statement

Fix a K+P chess position X, cut into pawn components G₁, …, G_k and a king group Z with a buffer (Definition
2.1). Fix the D-model of §1.2: its decisive events are passers in the components (races by a race rule) and
the moves inside Z.

**Theorem 1.14 (validity of the convention). PROVED.** Assume:
- **(V1) non-interaction and no stalemate.** At every chess position Y reachable from X before the first
  decisive event:
  - (a) the legal chess moves of the side to move are exactly its D-options, with the same resulting
    positions. This includes en passant obeying condition (E) of L1.6 in `notes/lemmas.md`, and no checks;
  - (b) the side to move has at least one legal move.
- **(V2) decisiveness.** Every decisive event reached by a move from such a Y leads to a position that is a
  P-win for the event's beneficiary.
- **(V3) frozen Z.** Every legal move inside Z, by either side, is a decisive event for the opponent: a
  suicide.
- **(V4) hereditary sum-safety.** At every position Y reachable from X before the first decisive event:
  - the pawn components of Y, re-split as the files split (an empty file stays empty, so a component may split
    into two), with the king group Z deleted, are pairwise safe: no two different components carry + ∈ τ and
    − ∈ τ, where τ counts options to ⊕ or ⊖ by **either** player (Definition 1.10);
  - BIG exceeds every tempo count of Y.

Then, with either side to move:
- **(i)** P(X) = D(X). There are no draws, and the result is the normal-play result of G₁ ⊞ … ⊞ G_k (Z
  deleted).
- **(ii)** If (V4) holds, the outcome class of S(X) — the BIG value of the pawn components, with the king
  group Z deleted — equals the outcome class of the D-result pair of P(X).
- **(iii)** Under (A_Q)(X) (the per-position hypothesis of §1.2, checked by kpsolve), C(X) = P(X). This is a tautology: (A_Q)(X) says exactly this.

*Proof.*
- **(i)** By (V3), Z contributes only suicides to D, so by Lemma 1.7 D(X) is the D-result of ⊞ G_i. D is
  short, so it has no draws.
  - Let σ be the D-winner (for the given side to move). σ plays a D-winning strategy. That strategy never
    plays a Z-move, because Z-moves are σ's suicides.
  - By (V1a), every chess move of the loser σ̄ is a D-option.
  - Under a winning strategy, the loser never has an option to its own terminal: at a loser-to-move position
    every option leads to a σ-win. So the play can end only in a σ-terminal, made by σ, or by σ̄ as a
    suicide (a Z-move, or a pawn move that gives σ a passer).
  - The play does end. The components are short, and (V1b) excludes "no move".
  - By (V2) the terminal position is a P-win for σ, so σ wins P.
- **(ii)** By (i), the D-result pair of X is the D-result pair of D(X), and re-splitting does not change
  that pair (it re-groups the same positions and options). By Theorem 1.11(c), with (V4) supplying (HSS) and
  the bound, the outcome class of S(X) is the outcome class of that D-result pair.
- **(iii)** Definition of (A_Q)(X). ∎

**Sharp form (PROVED).**

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

*Proof.* We show by induction on ρ(y) that every y ∈ N is a P-win for σ. Let y ∈ N, and assume the claim for all
members of N of smaller ρ.
- *σ to move.* Take the move of (S1). If it is closing, y is a P-win by the clause above. Otherwise it leads to
  y′ ∈ N with ρ(y′) < ρ(y), a P-win by the induction hypothesis, so y is a P-win.
- *σ̄ to move.* By (S3), σ̄ has a legal move or is in check. Consider any legal move of σ̄. By (S2) it is
  closing, so it does not promote and leads to a P-win; or it is a D-move to some y′ ∈ N. In the second case π(y′)
  is a D-option of the σ̄-node π(y) of W_σ, and it is a position of D, not a terminal, so ρ(y′) < ρ(y) by the
  definition of ρ, and y′ is a P-win by the induction hypothesis. So σ̄ is not stalemated
  and every legal move of σ̄ leads to a P-win: y is a P-win. (If σ̄ has no legal move, it is checkmated and the
  condition is vacuous.)

ρ takes values in the natural numbers, so the induction covers N. ∎ The proof is also a strategy: σ plays
rank-lowering D-moves until a closing move, and then plays a winning strategy of the P-position reached. Every
move lowers ρ or ends the D-phase, so the win takes finitely many moves.

*Reading in the vocabulary of Theorem 1.14.* Take a D-winning strategy Σ of σ that lowers ρ at every σ-move,
and let N be the P-positions that occur when σ plays Σ as legal chess moves and σ̄ plays any legal D-move.
- (S1) is (V1a) for the winner, along Σ only: Σ's move is a legal chess move **and the resulting position is the
  prescribed D-successor** (this is what "the same resulting positions" means; it excludes a king move that
  captures a context pawn or steps onto a buffer file). If Σ prescribes a σ-terminal, the move must be a P-win:
  this is (V2) at the winner's terminals. The winner may move in Z: the shuttle of Z_onT1 is a Z-move that is an
  ordinary D-option, legal in every context by Lemma 2.2 (Proposition 3.2). The claim "σ never plays a Z-move"
  belongs to the proof of (i), where (V3) makes every Z-move a suicide, and is not used here. The winner's other
  legal moves are never played and need no hypothesis.
- (S2) is (V1a) for the loser, together with (V2) and (V3): every legal move of σ̄ at a node of N is a D-move
  or a P-loss for σ̄. In reading (a) every Z-move of σ̄ is a σ-terminal, so (S2) says that **every legal Z-move
  of σ̄ is a P-loss**: this is the strong form of (V3), for all legal Z-moves and not only
  those played, because σ̄ chooses. In reading (b) an unpunished Z-move of σ̄ (a loser that owns a shuttle) is a
  D-move and needs no punishment: this is the loser's shuttle in Theorem 3.2‴, and with it the loser's stalemate
  (S3) cannot occur. A decisive event that σ̄ makes for σ is a closing move, which is (V2).
- (S3) is (V1b) restricted to the loser's nodes of N. Checkmate of σ̄ is a P-win, so only stalemate must be
  excluded. The normal-play rule of D, "no option loses", is never used.
- Checks need no separate hypothesis: the loser's moves are legal chess moves, and the winner's are legal by (S1).
- Existence is what is needed: N depends on the choice of Σ. In P2 + H\* White's e3–e4 stalemates Black (§6),
  so N has to be built from the shuttle Ka6.

The conclusion is a strategy win in P, not a normal-play result; the claim "the result is the normal-play result
of G₁ ⊞ … ⊞ G_k (Z deleted)" belongs to (i). Lemmas 1.6 and 1.7 are not used: Z is not deleted, and the winner's
extra legal moves are simply not played. Exhibiting N at a concrete position is a separate check, which this
paragraph does not do for any position of §6 beyond what the text says there. The chess bridge after Proposition
3.2 is the instance D = G ⊞ on_D. Its proof uses the sharp form, not the proof of (i), whose "σ never moves in Z" step does not cover White's shuttle.

*Sharpness of (S1)–(S3)* (examples from this note).
- **(S3).** P1a with real kings, `Ka5 Pb4 Pc5 Pe2 Pe4 / kc6 pb5 pe5` (§5.4; PROVED by enumeration, kpsolve
  (D, D)). The convention reads it as (W, W), and so does D, where Black's only option is
  the suicide Kd5. In chess Kd5 is illegal, Black has no legal move and is not in check, so (S2) holds vacuously
  and (S1) holds (the shuttle Ka6), yet the position is a draw. Only (S3) fails.
- **(S2), a legal Z-move of the loser that is not a P-loss.** 7.3 (§5.3), P8 `Kc6 Pb5 kb4 pc5` (kpsolve (W, W),
  PROVED in P): the convention (reading (a)) gives (L, W), but White's Z-move b5–b6=Q (f7–f8=Q on 8×8) is a legal
  move of the loser that wins. P2 + H0, `Ka5 Pb4 Pc5 kc6 pb5 Pe3 pe4` (kpsolve (W, W)): reading (a) gives (L, W)
  and White's Ka6 is not a P-loss; reading (b) is the one that applies (Proposition 3.2). P4 with H0 is not an instance of (S2) in P: H0 is G1 of P13, Black to
  move is lost in P, so Black's sorties Kd3 and Kd2 are P-losses and the position is (L, W) as predicted (CHECKED-2,
  three implementations agree). In C, kpsolve with cap 2 gives a draw instead of (L, W), so there the sorties do not
  lose (COMPUTED-1 in C). That is a chess-only effect, outside this list; its cause was not examined.
- **(S2), a decisive event that is not a P-win (V2).** Races (L4.1 of `notes/lemmas.md`, modulo KQK) and §5.5,
  `Ka4 Pb2 kc5 pb3 w -` = (D, D): Black's Kc5 is scored as a White passer in D but is not a P-win (CONJECTURE,
  scratch evidence, kpsolve agrees). For the winner, the same failure removes closing moves: in 7.3 a Black
  passer is a ⊖ in D and loses to f8=Q in P.
- **(S1).** For an abstract D the need is trivial: with no legal move realising Σ's step, nothing transfers. For
  the natural D(X), `Ka2 kb4 Pa3 pa4 Pd2 pe3 b -` (cyl:6×6; CHECKED-2, table of §1.5) is an isolated counterexample: σ = Black is the D-winner and is in check, its only legal moves are the four king moves (Z-moves), none of them is a D-move and none is a P-win for Black, and Σ's step (e3–e2, a context move) is illegal, so (S1) fails and P(X) is a White win. That is the same failure as the clause "no checks" of (V1a). A failure of (S1) with no check at the root is not known.

*Relation to Theorem 2.4.* Theorem 2.4 is a statement inside D (G short and under normal play, Z a king group, σ
never moving in Z). The sharp form compares P with D and lets σ move in Z. Neither is a special case of the
other. Both say that a winning strategy of a model transfers to the real game when every real move of the loser
is a model move or loses on the spot.


**Why "exact" does not mean "iff".** (V1)–(V4) are sufficient, and none can be dropped (table below; for the clause (E) of (V1a) this is a CONJECTURE). But no condition on local data can be *necessary*: the convention is
sometimes right by accident.
- In §5.4, literal pawn-only scoring gets Z_onT1 + context right because it calls c5 passed. It gets the
  stalemate trap wrong for the same reason.
- So the exact answer to "when does the convention hold?" is: whenever (V1)–(V4) hold, plus accidents. The
  accidents are not detectable without solving the position.

**Each hypothesis is needed** (for (V1a) the clause "no checks" is needed, CHECKED-2, by an isolated counterexample; for its clause (E) "needed" is a CONJECTURE). Each can fail and change the result.

| Hypothesis | Counterexample (where in this note or the project) |
|---|---|
| (V1b) no stalemate | §5.4: the only suicide square is covered, and the position is a draw instead of a win (PROVED). The isolated failure needs (V3) to hold, so use the frozen model, where (V3) holds by fiat: `--frozen` gives `Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5` as (D, D), with every king move L, while the convention reads Z as 0 and the context as +1, i.e. (W, W) (COMPUTED-1, `kings/kpsolve --frozen`). With real kings the same position also violates (V3): Ka6 and Kg4–g6 are legal Z-moves that are not suicides |
| (V1a) non-interaction | **The clause "no checks": needed, CHECKED-2 (the position is small enough that a hand proof of P = White wins is possible, but none is given).** cyl:6×6 `Ka2 kb4 Pa3 pa4 Pd2 pe3 b -`. Z = Ka2, kb4 and the locked pair Pa3/pa4 on F_Z = {a, b}; context Pd2/pe3 on d, e; buffer c, f. The Z-pawn a3 checks kb4, so Black's only legal moves are the four king moves Kb5, Kc5, Kc4, Ka5 (Z-moves), and every one loses in P with real kings: P(X) = White wins (CHECKED-2: three independently written solvers agree, `kp_p --pmodel`, `refp.py` and `ref3m`, the last written from the rules `kings/SPEC.md` only). D, with Z deleted, lets Black play e3–e2 or e3×d2, a passer at once, so D(X) = Black wins with Black to move (and White wins with White to move: outcome class N; CHECKED-2: a separately written D-solver and `cylcgt` o(S) both give N). The whole-board D-solver D_whole and the fixed-sum D-solver D_fix give the same pair at X, White to move White wins and Black to move Black wins, so they agree with the value N, and they show no (E) violation at X (COMPUTED-1: one program; the separately written D-solver reproduces N but was not run as D_fix or D_whole). So P(X) ≠ D(X). Here (V1b) holds (4 legal moves), (V2) and (V3) hold at every chess-reachable position (X alone, because every legal move is a Z-move, and all four lead to P-wins for White), and (V4) holds at X (COMPUTED-1: the exact (HSS) test, a stronger variant of it and the tempo test all pass at X; the tempo test is the bound of Definition 1.10, (H − 2)·n + 1 < BIG with n the number of pawns, so it covers the tempo half of (V4); a separately written program re-ran this test only for the twin below, which has the same context, and not for X). The twin with kb5 (no check) satisfies (V1)–(V4) at every chess-reachable position (checked by a second, separately written program) and P = D for both sides to move (White to move: White wins, Black to move: Black wins), so the check is the only cause. Whether X is retrograde-legal (the last White move must have been a capture onto a3, such as Pb2×a3) was not examined; Theorem 1.14 speaks of a K+P chess position and all solvers treat X as legal. A deeper context, `Kb6 kb3 Pa2 pa3 Pd2 Pe3 pe5 b -` (twin kb2; 4 chess-reachable positions with Black to move and 6 with White to move), behaves the same (CHECKED-2: kp_p and ref3m agree: X = White wins; twin, White to move: White wins, Black to move: Black wins; D = N in the separately written D-solver and in `cylcgt`). With frozen kings (V3 by fiat) `Ka1 kb4 Pa3 pa4 Pd2 pe3 b -` behaves the same (CHECKED-2: `kpsolve --frozen` and `ref3m --frozen`: White wins; twin kb5: Black wins with Black to move). Statistics of a systematic search (CHECKED-2 as counts: a second program reproduces every figure below with its own generator, its own D and `ref3m`): frozen, 514/514 (flat:6×6 and cyl:7×6, ≤ 2+2 pawns on 3 context files), 411/411 (cyl:6×6, ≤ 3+3 pawns on 2 files) and 6/6 (cyl:5×6, one context file) contexts where Black wins D moving first give P ≠ D at the checked root; real kings, 781 (cyl:6×6), 3780 (flat:6×6), 3657 (cyl:7×6) layouts (≤ 2+2 pawns) with P = White wins ≠ D = Black wins, of which 257, 1362 and 1210 have a twin that satisfies all of (V1)–(V4) with real kings (cyl:5×6, one context file, ≤ 3+3: 0 hits). King sorties (41 of 449 tablebase king moves draw and 7 win, `engine/suite/`, `RESULTS.md` §1) are (V2)/(V3) failures. The clause **(E)**: no isolated counterexample, see Proposition 1.15(b) (CONJECTURE that (E) is not needed when (HSS) holds, in the searched boundary only) |
| (V2) decisiveness | Races: L4.1 of `notes/lemmas.md` (forced wins, modulo KQK). A dropped pawn that does not lose: §5.5 |
| (V3) frozen Z | 7.3: f7–f8=Q is available at once (§5.3) |
| (V4) dominance | Proposition 1.12 (cancellation, for every B) and Proposition 1.13 (tempo above B) |

**Proposition 1.15 (what (V1a) can mean in the structured class). (a) PROVED. (b) The counts are CHECKED-2 as counts; the generalisation is a bounded CONJECTURE.**
Let X be as in Definition 2.1 (kings and Z-pawns on F_Z, context on files at distance ≥ 2, buffer empty, no officer) and let
Y be a chess position reachable from X by legal moves in which no Z-move has been made.
- **(a)** Then the legal chess moves of the side s to move that are not Z-moves are exactly its context pawn moves (with
  the global e.p. right) if s is not in check at Y, and there are none if s is in check at Y. Whether a given side is in
  check is the same at every such Y: it is decided at X. In particular there are no pins (no slider exists before the first
  promotion), no checks arise after the root (context pawns never attack F_Z by Lemma 2.2, and kings and Z-pawns have
  not moved), and a king never blocks or captures a context pawn in one move. Read for the moves outside Z (the Z-moves are
  the suicides of (V3), not D-moves of the pawn game; Lemma 1.7), (V1a) therefore fails at some Y iff **(check)** the side
  to move at some Y is in check from a Z-pawn, or **(E)** fails (the persisting local right of a component is the only other
  difference between chess moves and D-options). *Proof.* A context pawn move is illegal only if it leaves the mover's king
  attacked. With no sliders the only attackers are pawns. Context pawns attack only buffer and context squares
  (Lemma 2.2), so after a context move the attackers of the king are the same Z-pawns as before. If s is in check, a
  context move would have to capture the checking Z-pawn, which lies on F_Z, while every square a context pawn can capture
  on is at distance ≥ 1 from F_Z, or block, which a pawn check cannot be. En passant is also a context move: the capturer
  lands on the victim's file (Lemma 2.2), so it cannot capture a Z-pawn either. The remaining difference between
  D-options and chess moves is the right that persists in a component of the sum while another component is played: that
  is (E). ∎ (The check status of a given side is the same at every Y, so "fails at some Y" is "fails at X" for (check).)
- **(check) is needed: CHECKED-2.** Example in the table row of §1.5 (`Ka2 kb4 Pa3 pa4 Pd2 pe3 b -`, cyl:6×6; three independent solvers agree on P, a separately written D-solver gives N). The side in check has only Z-moves, so under (V3) it loses
  in P, while D lets it play in the context. This is a solver result, not a hand proof.
- **(b) (E): a negative result with its exact search boundary.** In the structured class a chess position with a pending
  right at the root, or one reached later, and ≥ 2 components, violates (E). Boundary of the searches (reproduced by a second program with its own generator and its own D): contexts on ranks 2 to H−1 only; at most 3 context files (4 in the (E) search);
  ≤ 2, 3, 4 or 5 pawns per side as stated; Z = one locked pair Pa(r)/pa(r+1), Black king on b(r+1), White king on a or b; the
  search with a right at the root is on flat:8×6 with a gap file and the right in the root only.
  - Roots with a fresh e.p. right for the side to move: contexts on files c, d, f, g of flat:8×6 (F_Z = {a}, buffer b),
    ≤ 5 + 5 pawns: 313,476 contexts, 39,696 roots, 39,600 with ≥ 2 components. At each of these 39,600 roots the persisting e.p. right violates (E), because a right that stays pending in one component while another is played is not a D-option. This does not contradict the 0 differences on the HSS roots below: the two readings (chess e.p. and the sum with persisting rights) can differ only where (E) fails, and on the HSS roots they still agree. Contexts on c to f of
    flat:6×6, ≤ 3 + 3 pawns: 3,036 roots, 192 with ≥ 2 components, no difference.
  - Roots without a right: contexts on c to f of flat:6×6, ≤ 3 + 3 pawns, 20,102 contexts: 752 roots in which (E) is violated
    (some reachable position has ≥ 2 components and a genuine e.p. capture), and D_fix = D_whole at all of them. (A looser test that also counts a later ordinary capture of a just-double-stepped pawn gives 1,128; such a capture is not an (E) violation. The 752 is reproduced by the second program.) Not
    completed: cyl:7×6 ≤ 3 + 3, and flat:6×6 ≤ 4 + 4 (stopped after about 60,000 contexts, no difference seen; that partial run has 5,017 E-violating roots, and the 0 differences are over those 5,017 roots; COMPUTED-1, not reproduced by the second program, and counted with the looser e.p. test that gives 1,128 above).
  - Result: the whole-board D (chess e.p.) and the sum D with persisting rights differ in 48 roots of the ≤ 5 + 5 run (16
    in the ≤ 4 + 4 run), all in flat:8×6, none of them hereditarily sum-safe (HSS false: opposite threats in different
    components); `kp --frozen` gives P = D_whole in 32 of the 48 and P = D_fix in 16, which says nothing about (V1a) under (V4)
    because HSS fails in all 48. Among the 5,584 HSS roots of the ≤ 5 + 5 run there is no difference (o(S) = D_whole in all of
    them), and none among the 2,560 HSS multi-component roots of the ≤ 4 + 4 run. So no isolated counterexample for (E) was
    found, and when (HSS) holds the sum reading and the chess reading agreed on every searched root. CONJECTURE that (E) can be
    dropped under (V4), in this boundary only; this (E) search tested (HSS) only, not the second half of (V4), "BIG exceeds every tempo count".

---

## 2. Frozen king groups

**Definition 2.1 (king group, buffer).** A *king group* Z consists of:
- a set F_Z of files (an arc on a cylinder);
- both kings and some pawns, the Z-pawns, all on F_Z.

All other pawns, the *context*, stand on files at distance ≥ 2 from F_Z. The files at distance exactly 1
are pawn-free; they are the *buffer*. A *Z-move* is a move of a king or of a Z-pawn.
- On the 7×6 cylinder with F_Z = {a, b, c}, the buffer is {d, g} and the context lies on {e, f}.

**Lemma 2.2 (buffer invariance). PROVED.** Before the first promotion:
- no pawn ever stands on a buffer file;
- context pawns stay on context files, and Z-pawns stay on F_Z;
- hence a king standing on F_Z is never attacked by a context pawn, and a context pawn never attacks a
  square of F_Z.

*Proof.*
- A pawn changes file only by capturing on an adjacent file, landing on the square of an enemy pawn or
  officer. A king cannot be captured.
- For en passant, the capturer lands on the file of the captured pawn.
- There are no officers before the first promotion.
- So a pawn can enter a buffer file only by capturing an enemy pawn already on it. Buffer files start
  pawn-free, so by induction on the number of moves none ever holds a pawn.
- Pawns attack only the two adjacent files. ∎

**Theorem 2.3 ({−B | B} = 0 for every integer B ≥ 1). PROVED**
(also KNOWN: the simplicity theorem, [WW] ch. 2, [S] ch. II, since 0
is the simplest number strictly between −B and B).

*Direct proof.* The proof uses B ≥ 1: for
B = 0 the game is {0 | 0} = \*.
- Left moving first goes to −B. Right, to move, moves to −(B − 1), and Left then has no move in a
  non-positive integer and loses.
- Right moving first loses by symmetry.
- A 𝓟-position equals 0 (KNOWN, [WW] ch. 1). ∎

So "every White Z-move gives Black a passer and vice versa" makes Z = {−BIG | +BIG} = 0 in the convention.
The real content is in what "gives a passer" must mean in chess.

**Theorem 2.4 (freeze theorem). PROVED.** Let G be a short game scored under normal
play, so that G has no draws, and let Z be a king group, possibly loopy. The sum G ⊞ Z is the game on positions
(Y, z): a move is a G-move in the context or a Z-move (a move of a king or of a Z-pawn inside the group); a
G-position with no G-move left is a loss for the side to move, while in the sum the side to move may still have
Z-moves. Assume Z's state changes only through Z-moves.
- **(a)** Suppose every Z-move, in every state of Z and in every context reachable from the root, leads to a
  position won by the opponent of the mover. Then r(G ⊞ Z) = r(G) at every reachable (Y, s).
- **(b)** It is enough that this holds at the positions (Y, s) reached under some winning strategy of the
  G-winner σ at which the loser σ̄ is to move.
- **(c) (strategy transfer, for a G that may draw.)** Let G be a game that may draw, and let σ be a side with a
  strategy in G that never loses (it wins every line except those that draw). Suppose that, at every position
  reached under that strategy, every Z-move of the opponent σ̄ is decisively punished (Definition 2.5) and that
  σ never needs to move in Z. Then σ does not lose G ⊞ Z; and if σ's strategy in G wins every line, then σ wins
  G ⊞ Z.

In chess, assume also (V1b): the side to move always has a legal move.

*The P-game of the context is **not** covered, and the theorem is false for it.* The P-model keeps stalemate as a draw, so "G has no draws" fails there and the step "since G has no draws the results agree" is not available. Counterexample: cyl:7×6,
`Ka4 Pb3 Pe3 kc3 pb4 pe4` (Z_T + H0). The context G = {Pe3, pe4} has no move for either side, so it is (D, D)
under P; `kpsolve --frozen` gives (L, W), and there the hypothesis of (a) holds by fiat (king moves lose and
the Z-pawns have no moves); with real kings, White to move is L (exact) (COMPUTED-1, `kings/kpsolve`).

*Proof of (b).*
- σ plays its winning strategy in G and never moves in Z, so Z stays in its initial state.
- Whenever σ̄ is to move, the G-position is lost for σ̄. If σ̄ moves in Z, σ wins by hypothesis.
- G-play is finite, so one of three things happens:
  - a σ-terminal is reached, and σ wins;
  - σ̄ has no G-move and must move in Z, and σ wins;
  - σ̄ has no move at all, and σ̄ loses by normal play.
- In chess the last case is stalemate, which (V1b) excludes.
- So the G-winner wins G ⊞ Z, and since G has no draws the results agree. (a) is a special case. ∎

*Proof of (c).* σ plays its strategy of G, read in the sum, and never moves in Z, so Z stays in its initial
state. Whenever σ̄ moves in G, σ answers as in G. Whenever σ̄ moves in Z, σ wins by the hypothesis, since that
Z-move is decisively punished. The G-play is finite, since G is short. If σ̄ never moves in Z, the play is a
line of G under σ's strategy: it ends in a σ-win, or in a draw of G, so σ does not lose. If σ̄ does move in Z, σ
wins. ∎

**Definition 2.5 (decisive punishment, in chess terms).** A Z-move m of side s, made at a chess position Y
(context plus Z), is *decisively punished* if the opponent s̄ has a forced win in P (or in C) from the
position after m. The win must hold against every defence of s:
- s's moves in the context, including creating passers, starting races and capturing en passant;
- s's king going anywhere, back into Z or into the context;
- s promoting;
- s steering for stalemate.

"Whatever the other components contain" means: for every context in the class one claims the zero for.
Theorem 2.4(b) needs this only at positions where s is losing the context.

**Definition 2.6 (local certificate LC_T).**

*Data.*
- Y is a position as in Definition 2.1 with s to move: both kings on F_Z, the Z-pawns on F_Z, the context on files
  at distance ≥ 2 from F_Z, the buffer empty, no officer, no promotion yet. An e.p. right carried by Y is cleared by m. The proof of (a) does not
  use that Y is chess-legal: it uses that m and r are legal moves (see (b)).
- m is a legal Z-move of s that is not a promotion. It may take s's king off F_Z.
- r is a legal reply of s̄ to m that is not a promotion, is a Z-move, and leaves s̄'s king on F_Z. The standard r
  is a king capture of a Z-pawn of s. (If s̄ can promote at once there is nothing to certify: that is a P-win.)
- Q is the position after m and r, with s to move. T ≥ 1 is an integer.
- The *window* is the sequence s, s̄, s, s̄, … from Q. So s̄'s t-th move after r comes after s's t-th move, and
  s̄ must have won by its T-th move.
- The *projection* π(R) of a position R is R with every pawn deleted that stands off F_Z, of both colours. The
  kings (wherever they stand), the Z-pawns, the side to move, and an e.p. right whose target square is on F_Z
  are kept. Put Q_Z = π(Q).
- In (a), r is a Z-move, so an e.p. right carried by Q has its target on F_Z. In the window form (b) the
  target may be anywhere, and (L2) accounts for it.

LC_T(m) holds at Y if some such reply r satisfies (L1), (L2) and (L3).

- **(L1) local forced promotion against a passing defender.** The *local game* L_T(Q_Z) is played on the same
  board (same files and ranks, flat or cylinder) from Q_Z with s to move, by the rules of chess, with these
  changes:
  1. *Promotion (P semantics).* The first promotion by either side ends the game. A promotion by s is a win for
     s, whatever happens to the new piece: it is a **failure** for s̄. A promotion by s̄ is a win for s̄ if the
     new queen cannot be captured at once, that is, if no legal move of s captures it. An unsafe
     promotion ends the game as a failure for s̄.
  2. *Passes.* s may pass at any turn in which it is not in check, as often as it likes (k = ∞). s̄ may not
     pass. A pass changes only the side to move and clears the e.p. right.
  3. *Confinement.* s̄'s king may only step onto squares of F_Z. s̄'s pawn moves are not restricted; by Lemma 2.2
     they stay on F_Z.
  4. *Mate and stalemate.* If s is in check and has no legal move, s is mated and s̄ wins. With unlimited
     passes s can never be stalemated in the local game. If s̄ has no permitted move at its turn (checkmate,
     stalemate, or only king moves that leave F_Z), that is a failure for s̄.
  5. *Time.* s̄ must win with one of its first T moves, by a promotion as in 1 or by a move that mates s.
     Anything else is a failure.

  (L1) holds if s̄ has a strategy that wins L_T(Q_Z) against every behaviour of s, passes included.
  **(L1_P)** is the weaker condition in which every promotion by s̄ is a win (no queen clause). Theorem 2.7 holds
  with (L1_P) in place of (L1); the queen clause is for the chess statement (A_Q).
  - The unlimited budget models the fact that s's spare moves in the context are not known in advance; the real
    defender's options are a subset of the k = ∞ game's, and its only gain from having fewer options is
    stalemate, which (L3) excludes. So the single game with k = ∞ is used, not one game for every finite k.
  - A clause "s with no legal move and no pass left is stalemated, which counts as a failure for s̄" would have no content for k = ∞. Stalemate enters in two places only: a stalemate of s̄ is a failure (rule 4),
    and a stalemate of the *real* s is excluded by (L3).
- **(L2) no faster counter-promotion by a context pawn.** Let Q° be Q with s̄'s king and all Z-pawns of both
  colours deleted. s's king and the context pawns of both colours stay. Let μ_s be the least number of
  consecutive s-moves (s̄ never moves) after which a context pawn of s promotes in Q°, and ∞ if none can. The
  moves are chess moves: a king may not step onto a square attacked by a pawn of s̄, an s̄ context pawn stays
  where it is unless s captures it, and no e.p. right exists except the one described next. If Q carries an
  e.p. right whose target square is **off F_Z**, Q° keeps it: s may use it at its first move, and only then
  (the capture lands on the target and removes the s̄ pawn that has just double-stepped). A right whose target
  is on F_Z concerns Z-pawns only, which Q° has deleted, so it is dropped. In (a) Q carries no right of the first
  kind. Then **μ_s ≥ T + 1**.
  - μ_s is a breadth-first search over s's king and context pawns. A king move that captures an s̄ context
    blocker is one of the moves, so the king's help is counted, and so is the e.p. capture just described.
  - **Which s-pawns are counted.** Only the context pawns. s's Z-pawns are not counted by (L2): their
    promotions belong to the local game, where s̄'s Z-pieces stay on the board and a promotion by s is a failure
    for s̄. The alternative, in which μ_s counts s's king and all pawns, Z-pawns included, with s̄'s Z-pieces removed, is not used. Reasons:
    - The proof needs (L2) only for the promotions that (L1) cannot see, and what (L1) deletes is the context.
    - That count is not a lower bound for a Z-pawn: deleting s̄'s Z-pieces can raise or lower it (in one example 3 moves against the real 2).
    - As a hypothesis it is stronger than needed. `Ke6 ka1 Pc4 pb3 pc5`, White to move (cyl:7×6), is a Black
      win in P. Black's local win has T = 2 (b2, b1=Q), no White context pawn exists, but that count gives μ_s = 2 for White's Z-pawn c4 once Black's c5 is deleted, although c5 locks it. (L1), (L2), (L3) as stated all hold; the stronger (L2) fails.
    - With context pawns only, Proposition 2.10(a) needs no Z-pawn proviso: s's Z-pawns are covered by (L1),
      whatever their distance from promotion (a promotion by s is a failure for s̄ in the local game).
    - Anyone who wants the stronger hypothesis may assume both; the theorem holds a fortiori.
  - **μ_s ≥ T + 1 is the exact bound for P.** Step 4 shows that s promotes no earlier than its (T + 1)-th turn, and
    s̄ queens on its T-th move, which follows s's T-th turn. With μ_s = T, s promotes first (example below).
  - **(L2⁺)**, μ_s ≥ T + 2, is only a margin, and it does not give a chess win. With μ_s = T + 1, s promotes at once
    after s̄ queens (queen against queen, not against a pawn on its seventh rank). With μ_s = T + 2, s̄ has one move
    with its new queen, and a draw can still follow. No margin of μ_s replaces (A_Q) at the position (examples in
    "What Theorem 2.7 does not give").
- **(L3) no stalemate of s in the window.** A *guided strategy* of s̄ is a strategy in the real game that at each
  of its turns plays a Z-move (a king step onto a square of F_Z, a move of a Z-pawn, or a promotion) whose
  projection is a winning move of L_T(Q_Z) at the projected position, with the remaining time. s̄ never moves a
  context pawn. (A winning strategy of the local game, read in the real game, is guided.) (L3) asks for a
  guided strategy such that, in every real play from Q in which s̄ follows it and s plays legal moves as it
  likes, s is never stalemated at one of its turns in the window. A mate of s ends the play in s̄'s favour and
  is not excluded.
  - (L1) cannot see (L3): it lets s pass, while the real s has only the context moves that exist. The danger is
    a context pawn taking away king squares that are free in Q_Z, or the context running out of moves.
  - **Sufficient local condition (L3_F).** In every line of L_T(Q_Z) in which s̄ plays only winning moves, s has
    at each of its turns before s̄'s win a legal Z-pawn move or a legal king move onto a square of F_Z. By
    Lemma 2.2 nothing off F_Z occupies or attacks a square of F_Z, so that move is legal in every real position
    reached as well.
  - The simpler sufficient condition (L3′) (every square within distance T + 1 of s's king lies on F_Z) can never apply for T ≥ 2 on a 3-file group, because the ball of radius T + 1 spans at least 5 files while |F_Z| = 3.
  - For T = 1, (L3) is a single check: s is not stalemated at Q.

**Theorem 2.7 (sufficiency of the certificate). PROVED (in P).** Without the e.p. clause of (L2), (b) is false; see the example in the list "The conditions cannot be dropped" below.
- **(a)** If LC_T(m) holds at Y, with reply r, then s̄ has a forced win in P after m: it plays r and then wins
  with one of its next T moves. So m is decisively punished in P.
- **(b) Window form.** The proof does not use how Q arose. Let Q be a position with s to move which is
  chess-legal, or which arises from a position Y of Definition 2.1 by legal moves m and r as in (a), and in which
  every pawn is a Z-pawn on F_Z or a context pawn on a context file, the buffer is empty, there is no officer,
  s̄'s king stands on F_Z, and no s̄ context pawn attacks s's king (automatic if s's king is on F_Z). Q may
  carry an e.p. right with its target anywhere: (L2) counts a right whose target is off F_Z, and π keeps a
  right whose target is on F_Z. If (L1),
  (L2) and (L3) hold at Q, s̄ has a forced win in P from Q. This is the form used in §5.3 and P8, with Q = Y.
  The window form does not cover a legal position in which s is in check from an s̄ context pawn that has just
  moved (s's king on a context or buffer file): there (I4) fails, and the theorem says nothing.

*Proof.* Fix a guided strategy ρ of s̄ with the property (L3). s̄ plays r and then ρ. Only Z-moves are made
by s̄, and its king stays on F_Z. Consider any real play from Q in which s plays legal moves, and write R for
the real positions in it.

- **Step 0: invariants.**
  - (I1) Every pawn is a Z-pawn on F_Z or a context pawn on a context file; the buffer is empty. This is Lemma
    2.2, applied from Q (from Y in (a)); it holds for every legal play before the first promotion. In (b) s's king
    may stand off F_Z, so Q need not be a position of Definition 2.1; but the proof of Lemma 2.2 uses only the pawn
    placement and the empty buffer, not where the kings stand, so it applies from Q.
  - (I2) No context pawn of either colour attacks a square of F_Z. A pawn attacks only adjacent files, and a
    context file is at distance ≥ 2 from F_Z. Also, a Z-pawn can capture only on F_Z or on the buffer, which is
    empty, so its captures take Z-pawns (or e.p.).
  - (I3) s̄'s king stands on F_Z.
  - (I4) s̄'s context pawns never move and are only removed (by s). No s̄ context pawn ever attacks s's king:
    none does at Q (m was legal, r changes no context pawn; in (b) this is a hypothesis), the set of squares
    they attack only shrinks, and a king never steps onto an attacked square. So s is in check at R iff an s̄
    Z-pawn attacks its king, iff s is in check in π(R).
  - (I5) *E.p. rights.* A right created by s̄ comes from a Z-pawn double step, since s̄ plays Z-moves only, so its
    target is on F_Z, and only Z-pawns of s can use it (a context pawn is not adjacent to F_Z). A right created by
    s concerns an s pawn, so it is of no use to an s context pawn. If its target is on F_Z, s̄'s Z-pawns may use it,
    and the local game accounts for this (π keeps such a right). If its target is off F_Z, no s̄ pawn that s̄
    moves can use it, and π drops it. So the only e.p. capture that an s context pawn can ever make is the
    one of the right carried by Q, if its target is off F_Z, and it can be made at s's first turn only.
- **Step 1: s's moves are local moves.** Let R have s to move. π(R) is a position of L_T(Q_Z) reached with s̄
  playing winning moves only (by induction on the play). A legal real move of s is one of three kinds.
  - *A king move* to d. Legal in R: d is not occupied by an own pawn, not adjacent to s̄'s king, not attacked by
    an s̄ pawn after the capture (if any), and if s is in check the move removes the check. Every condition
    holds in π(R): the kings are the same, the pawns present are a subset, and the checkers are Z-pawns by (I4).
    A capture of a context pawn becomes a plain king move in π(R). So the move is legal in π(R) and the
    projection of the result is the local result.
  - *A Z-pawn move* (step, double step, capture of an s̄ Z-pawn, e.p. capture of an s̄ Z-pawn, promotion). The
    squares involved lie on F_Z or on the empty buffer, and F_Z holds the same pieces in R and π(R) by (I1). King
    safety is as in the previous case. So it is legal in π(R) with the same result. In particular a promotion of
    a Z-pawn of s is a promotion by s in the local game.
  - *A context-pawn move.* It changes only context pawns, so π(R) is unchanged except for the side to move; an
    e.p. right it creates has a target off F_Z and is dropped by π, as a pass does. The e.p. capture of the right
    of Q (target off F_Z, I5) is such a move too: it moves an s context pawn and removes an s̄ context pawn. A
    context move is legal only if s is not
    in check: the checkers are s̄ Z-pawns (I4), and a context pawn can neither capture on F_Z (I2) nor block a
    pawn check. So s is not in check in π(R) and the pass is allowed. (A context promotion is treated in Step 4.)
  So the projection of the play is a play of L_T(Q_Z) in which context moves are passes. Real s-turns and local
  s-turns correspond one to one, as do s̄'s moves.
- **Step 2: s̄'s permitted local moves are legal real moves.** Let R′ have s̄ to move, and let μ̃ be a permitted
  move of s̄ at π(R′): a king step onto a square of F_Z, a Z-pawn move, or a promotion. Then μ̃ is legal in R′.
  - F_Z holds the same pieces in R′ and π(R′), and so does the e.p. right on F_Z (it comes from a Z-pawn double
    step, and only Z-pawns can capture it, because the squares next to F_Z are F_Z and the empty buffer).
  - s̄'s king ends on F_Z. The only pieces that could attack it are s's pawns and king. s's context pawns do not
    attack F_Z (I2); the rest is the same in π(R′). The kings are not adjacent, as in π(R′).
  - There are no sliders, so there are no pins.
  So guided strategies exist, and a winning strategy of the local game, read in the real game, is one.
- **Step 3: s̄ is never stuck.** A winning move of the local game exists whenever s̄ is to move before its win,
  and by Step 2 it is a legal real move. So s̄ always has a legal real move, and is never mated or stalemated before
  winning.
- **Step 4: s does not win first.** By Step 1 the projection of the play so far is a play of L_T(Q_Z) in which
  s̄ plays winning moves only, and such a play is over by s̄'s T-th move. So s has at most T turns, and the
  turn j at which s might promote has j ≤ T.
  - *A Z-pawn.* By Step 1 this is a promotion by s in a line of L_T(Q_Z) in which s̄ played winning moves only.
    That contradicts rule 1 (a promotion by s is a failure).
  - *A context pawn.* **Claim M:** μ_s ≤ j. Delete from the real play s̄'s moves and s's Z-pawn moves. What is
    left is a sequence of at most j moves of s, each a king move or a context-pawn move, ending with the
    promotion. It is a legal sequence in Q° (the position of (L2)). Indeed, s's king and the context pawns of
    both colours stand on the same squares in the real play and in the sequence, because s̄'s context pawns
    do not move and only s moves them (captures included). A king move is legal in Q°: its destination is not
    occupied by an own context pawn, it is not attacked by an s̄ context pawn (the same attackers), and Q°
    has fewer other pieces (no s̄ king, no Z-pawn), so no condition is added. A context-pawn move is legal
    in Q°: its target squares are on context files, where the real occupants are context pawns and possibly
    s's king (same in Q°); s̄'s king and all Z-pawns are on F_Z (I1, I3); the own king is not attacked
    (I4); and the only e.p. right that can be used is the one of Q (I5), at s's first turn. If it is used, it is
    the first move of the sequence, and Q° keeps exactly that right for its first move. So μ_s ≤ j ≤ T, which
    contradicts (L2). This is where the king's help in removing blockers is counted: it uses moves of s.
  - A context *passer* that exists but has not promoted in the window does nothing: in P only a promotion ends
    the game.
- **Step 5: no other ending.**
  - s cannot mate s̄: s̄ is never mated before winning (Step 3). In particular s's Z-pawns and king, which do
    attack F_Z, cannot take s̄'s last move away, because the prescribed local move is legal in the real
    position (Step 2).
  - s̄ is not stalemated (Step 3). s is not stalemated by (L3). There is no infinite play: the window has at
    most T moves of s̄.
- **Step 6: s̄ wins in time.** The projection is a play of the winning local game, so it ends within s̄'s first T
  moves with a promotion by s̄ or a mate of s. A promotion by s̄ is a legal real move (Step 2) and ends the real
  game in s̄'s favour in P. A mate of s in π(R) is a mate in R: s is in check in R (I4), and every legal real
  move of s is a local move or a pass (Step 1), and no pass exists in check, so s has no legal move in R either.
  Since s moves first after r, s̄'s t-th move comes after s's t-th, and the count is the one used in Step 4. ∎

*Part (b)* is the same proof with Q as the starting point: only (I1)–(I5) at Q were used, that s̄'s king is not
attacked at Q, and that an e.p. right is that of a pawn standing where the right says. These are the hypotheses of
(b) (they hold for a chess-legal Q, and for the Q of (a) because m and r are legal), together with Lemma 2.2.
*Part (a)* is part (b) applied to Q: m and r are Z-moves, so
every pawn is still a Z-pawn on F_Z or a context pawn on a context file and the buffer is empty (Lemma 2.2);
s̄'s king is on F_Z by the Data; no s̄ context pawn attacks s's king, because m was legal and r moves no context
pawn; and the only e.p. right Q can carry is one created by r, with its target on F_Z.

**Remark (an objection, answered).** One may object that (L2) counts promotions only and that a context passer within T ends the game in s's favour. In the D-model a passer is a terminal. Whether it is decisive is (V2), a hypothesis
of Theorem 1.14 (Proposition 2.11, P11), and Theorem 2.7 does not claim it. Theorem 2.7 is a statement about P. In P a
context passer of s is not terminal. Only a promotion ends the game, and (L2) bounds the first promotion of every
context pawn of s, passer or not, by T + 1 moves of s. A passer that stands at the end of the window has not
promoted, and s̄ has. So the objection does not apply to Theorem 2.7: it reads a P-statement as a D-statement.

**What Theorem 2.7 does not give.**
- *No C-win, and no margin of μ_s gives one.* In P a promotion wins at once. In chess the new queen must survive
  and the ending must be won. (L1) asks for a queen that s cannot capture at once, which is not enough: that s̄ wins
  chess after the promotion is the per-position hypothesis (A_Q), checked by kpsolve (§1.2). (L2⁺) is only a margin.
  The examples below are kpsolve results (`--promote QRBN --cap 2`, both bounds equal; the P values come from the `--pmodel` build of Appendix A). They are data, and the claims they support keep the label CONJECTURE. In each, s̄ is Black, and (L1) with the queen clause, (L2) with the e.p. clause and (L3) hold.
  - μ_s = T + 1, window form with Q = the position: cyl:7×6 `Ka4 ka6 Pf4 pb2`, White to move. T = 1 (b1=Q), and the
    White pawn f4 has μ_s = 2. Black wins P. **White wins chess**, and 1.f5 is the only winning move.
  - μ_s = T + 1, form (a): cyl:7×6, Y = `Kc5 ka3 Pe2 pc4`, White to move, m = Kc5–d5, r = c4–c3,
    Q = `Kd5 ka3 Pe2 pc3`, T = 2 (c2, c1=Q), μ_s = 3. Corollary 2.8 applies (d(Kd5, c1) = 4 = D + 2). After m, Black
    wins P and **White wins chess**.
  - μ_s = T + 1, form (a): cyl:7×6, Y = `Kb4 ka1 Pe4 pa2`, White to move, m = Kb4–c5, r = Ka1–b1,
    Q = `Kc5 kb1 Pe4 pa2`, T = 1, μ_s = 2. After m, Black wins P and chess is **drawn**.
  - μ_s = T + 2: flat:6×6 `Ke6 kb1 Pf2 pc2`, White to move. T = 1, μ_s = 3 (f4, f5, f6=Q). Black wins P and chess
    is **drawn**.
  - In a sampled enumeration of one Black Z-pawn and one White context pawn, draws are still present at μ_s ≥ T + 3 on flat:6×6 (4 of 659), and there are none at μ_s ≥ T + 2 on cyl:7×6 (COMPUTED-1, a sample).
  - Hence a chess form of (V3) does not follow from any horizon condition: the statement "a certificate of horizon h implies (V3)", read in chess, is refuted by the second and third example. Theorem 2.7 supports the P-version only.
- *No D-model statement.* For Theorem 1.14 the theorem supplies (V2) for the terminal "a Z-move is punished",
  at one Z-move and only in contexts where LC_T holds. It says nothing about (V2) for the passer terminals,
  nothing about (V3) for the other Z-moves, and nothing about (V1) or (V4).
- *No converse.* LC_T is sufficient only. A Z-move can be punished in P although (L1), (L2) or (L3) fails for
  every reply, for example by a different reply that the certificate does not use.
- *One Z-move at one position.* Theorem 2.4 needs every Z-move of the loser at every loser-to-move node, each with
  its own certificate. (L2) is context-dependent: for T = 1 it holds in every chess-legal non-terminal context
  when H ≥ 5, and for T ≥ 2 it fails in some context (Proposition 2.10).
- *The conditions cannot be dropped.* All examples are in cyl:7×6. The P values are results of the `--pmodel` build of Appendix A. They are data, and the claim that the conditions cannot be dropped keeps the label CONJECTURE; the races can be checked by hand.
  - (L3): `Kb5 kd5 Pb4 Pc5 Pe3 Pf3 Pf4 Pf5`, Black to move, is a draw in P. (L1) holds with T = 1 (c6=Q), Black
    has no pawn, and the White pawns on e3, f3, f4, f5 cover d4, e4, e5, e6, so Black is stalemated. This is
    the position after `Kd5 Kxb5` in `Ka5 kc6 Pb4 Pc5 pb5` with that context. In that start position Kd5 is
    still punished in P, by a different reply, so this is also an example of the missing converse.
  - (L2): `Kd6 kc2 pa3 Pe4 pe5 pf5`, White to move, is a White win in P. Black's local win has T = 2 (a2, a1=Q),
    the context is non-terminal, but μ_s = 2: exf5 and f6=Q (Proposition 2.10(b)). For T = 1 the same happens
    with a passer: `Kb5 kd5 Pb4 Pc5 pe2`, Black to move, is a Black win.
  - (L2), the e.p. clause: `Kd6 kc4 Pe3 pa4 pe4 pf3`, White to move, e.p. right on f4 (Black has just played
    f5–f3). Black (s̄) has a local win with T = 3 (a3, a2, a1=Q), (L3) holds, and without the clause μ_s = 6, so
    (L1), (L2) and (L3) would all hold. Yet White wins in P: exf4 e.p., f5, f6=Q, and its third move promotes
    before Black's third. With the clause μ_s = 3 < T + 1 = 4, as it should. The same position without the right
    is a Black win in P. So (b) is false without the e.p. clause. Part (a) cannot meet this case.
  - (L2), sharpness of μ_s ≥ T + 1: `Kf5 kc6 Pe4 pb3`, White to move, has T = 2 (b2, b1=Q) and μ_s = 2, and White wins
    P (1.e5 b2 2.e6=Q). With the pawn on e3 instead, μ_s = 3 and Black wins P (1.e4 b2 2.e5 b1=Q). The example
    `Kd6 kc2 pa3 Pe4 pe5 pf5` above also has μ_s = T = 2.
  - (L1) is the substance: with no local win there is nothing to transfer.

**Corollary 2.7′ (the contrapositive; the content of P12). PROVED in P.** Let X
have the structure of Definition 2.1 (kings and Z-pawns on F_Z, context on context files), let F be the
`--frozen` model (a king move loses at once for the mover, a promotion wins at once, stalemate and infinite play
are draws), and suppose σ has a winning strategy S in F from X. If at every node of S with σ̄ to move every
legal king move of σ̄ is a P-loss for σ̄, then σ wins P from X. Hence, if σ wins F but not P, then for every
winning strategy S of σ in F some node of S with σ̄ to move has a legal king move m of σ̄ that is not a
P-loss, and for that m, every admissible reply r (Definition 2.6, with s = σ̄ and s̄ = σ: a non-promoting Z-move
of σ that leaves σ's king on F_Z) and every T ≥ 1, (L1), (L2) or (L3) fails. A promoting reply by σ would make m a
P-loss for σ̄, so it does not occur for a move that is not a P-loss; replies that are not admissible are outside
LC_T.
- *Proof.* In P, σ plays S. S uses no king move of σ, since in F a king move is a loss for its maker, so the
  kings stand where they did at X, and the nodes of S keep the structure (a pawn move preserves it by Lemma
  2.2; a promotion ends the game). Every legal pawn move of σ̄ is the same move in F and in P, and S answers
  it. Every king move of σ̄ is a P-loss by hypothesis. Stalemates are draws in both
  models and do not occur in S. Terminals of S are promotions by σ, a P-win, and mates, equal in both. So the
  play is finite and σ wins P. The second statement is the contrapositive. Its last clause is the contrapositive
  of Theorem 2.7(a): a king move m with a reply r and T such that LC_T holds would be punished. ∎
- In chess: if `--frozen` reports a win for σ at X and the chess result at X is not a σ-win, then either P(X) is
  not a σ-win (the statement above) or (A_Q) fails at X. The comparison is one-directional: σ may win real chess
  by king moves that F forbids.

**Lemma 2.7a (transfer from a promotion model to chess). PROVED.** For a
king-and-pawn position X let EPW(X) be chess in which the first promotion by either side ends the game as a White win,
and EPB(X) the same with a Black win. Everything else is as in chess: a mate wins, stalemate and infinite play are
draws. A promotion move is legal in EPW and EPB exactly when it is legal in chess.
- (a) If White has no winning strategy in EPW(X), White has none in C(X).
- (b) If Black has no winning strategy in EPB(X), Black has none in C(X).
- (c) If both hold, C(X) is a draw.
- *Proof.* (a) By contraposition. Let σ be a winning strategy of White in C(X). Every play consistent with σ is
  finite and ends in a mate of Black. Play σ in EPW(X), against any behaviour of Black. Until the first promotion the
  legal moves, the mate test and the stalemate test are the same in the two games, so the play so far is a prefix of
  a chess play consistent with σ. If a promotion (by either side) occurs before σ's mate, the play ends in EPW as a
  White win. If none occurs, the whole play is a chess play consistent with σ and ends in the mate of Black, which
  is a White win in EPW as well. No play is infinite. So σ wins EPW(X). (b) is the same with the colours exchanged.
  (c) EPW, EPB and C are finite-state reachability games, so "neither side can force a win" is exactly the value D.
  ∎
- The lemma is used only in the direction "cannot win". The converse is not claimed (White may win EPW by a
  promotion that chess does not reward). EPW and EPB do not distinguish the piece promoted to, and the proof needs
  no cap on officers.
- *Application (CHECKED-2: two independently written implementations of the models).* With White to move, EPW = D and EPB = D for P7 (`Ke6 Pd7 kd8 pe7`, on
  cyl:8×8 and on flat:8×8) and for P5 (`Kc4 Pb5 kb6 pc5`, on cyl:7×6). By the lemma, White cannot win chess and Black
  cannot win chess there, so the chess value of the w-entry is D. kpsolve exact (lower and upper bound equal) gives D
  as well, and the Lichess tablebase agrees on flat:8×8. The lemma gives a chess draw, not a draw in P and not a hand
  proof of the draw in P. (For P7 w and for P5 w the draw, in P and in chess directly, also has a hand proof that does not use this lemma, so for both the lemma is an agreeing check.) For P6 the values are different (EPW = D and EPB = L with White to move on cyl:8×8): the lemma
  is not used there, the chess value comes from the reduction to KPK (§6, P6).
- *Consistency test, not part of the proof.* On 423 legal positions of cyl:5×6 no position has "White cannot win in EPW" while kpsolve gives a White win in chess, and there is no mirror case: 0 violations (COMPUTED-1).

**Corollary 2.8 (square-rule form of (L1)). PROVED.** Suppose:
- Q_Z consists of the two kings and one s̄-pawn p, and s̄'s king is not on p's path;
- the plan is "push p every move", with D = number of ranks to the promotion square q_D;
- d(k_s, q_D) ≥ D + 2, where k_s is s's king square after m.

Then s̄ wins the local game of (L1) within T ≤ D moves:
- for k = ∞;
- for every finite k, provided s's king always has a legal move in Q_Z. This is the stalemate proviso: a
  king boxed in at a rank edge, with no pass left, would be stalemated.

The finite-k clause is a side remark. The local game of Definition 2.6 has k = ∞
only, and Theorem 2.7 uses nothing else. The first clause gives (L1) of Definition 2.6 for this Q_Z: p promotes
by pushes with s̄'s king never moving, s has no pawn to promote, and s cannot be stalemated because it may pass.

*Proof.*
- **Distances to every path square.** Let q_j be the path square j ranks ahead, with q₀ = p's square. The
  triangle inequality gives d(k_s, q_j) ≥ d(k_s, q_D) − (D − j) ≥ j + 2.
- **Timing.** p reaches q_j at s̄'s move number t_j ≤ j; a double step only makes it earlier. Up to that
  moment s has made t_j moves.
- **The king can neither block nor capture.** To block q_j, s's king must be there within t_j ≤ j moves.
  To capture p on q_j, it must arrive by move t_j + 1 ≤ j + 1. Both are impossible.
- **The pawn cannot be stopped otherwise.** Q_Z holds no s-pawn, and the buffer keeps context pawns away.
- **The queen is safe.** For j = D the same bound keeps the new queen out of reach.
- **Budgets.** A pass changes nothing on the board, so the timing argument covers every pattern of passes.
  The only remaining defence is a stalemate, which the proviso excludes. ∎

The bound is the classical "rule of the square": with the defender to move, d(k_s, q_D) ≥ D + 2 is exactly the classical rule of the square, not a margin on top of it. Corollary 2.8 is rarely enough for trébuchets, because the defending king starts next to
the action. (L1) must then be checked by a small search (Appendix A).

**Lemma 2.9 (blockade). PROVED, under the hypothesis (B1).** In Q_Z, suppose:
- all of s̄'s Z-pawns stand on one file f, and s's king stands on a square of f in front of s̄'s front pawn, so above every s̄ pawn;
- **(B1)** at most one s̄ pawn is *attacked by an s pawn*. An s̄ pawn on (f, x) is attacked iff an s pawn stands on the square
  diagonally in front of it (on file f ± 1, one rank on in s̄'s direction). The relation is symmetric: the two pawns attack each
  other, and the one that is to move may capture. (B1) holds if s has no pawn on f ± 1, whenever s̄ has
  exactly one Z-pawn, and on every 4-rank board (counted from s̄'s side, s̄ pawns stand on rank 2 or higher, so two attacked s̄ pawns
  need an s̄ pawn on rank 3 or higher, attacked by an s pawn on rank 4 = s̄'s last rank, where no s pawn stands; so H ≥ 5 is needed);
- s is to move and may pass (k = ∞). An e.p. right carried by Q_Z was therefore created by s̄.

Then s has a strategy against which no s̄ pawn ever promotes and s is never mated. So s̄ wins L_T(Q_Z) for no T, in the reading
(L1) and in the reading (L1_P).

*Proof.* The strategy of s: if some s̄ pawn is attacked by an s pawn, capture it with an s pawn that attacks it; otherwise pass.
The king of s never moves. Let k be its rank. Write "attacked" for "attacked by an s pawn". Claim (J): at every turn of s̄, (J1) every
s̄ pawn stands on file f, below the king of s; (J2) no s̄ pawn is attacked. At the root, (J1) is the hypothesis. (J2) is not yet true
there, but at s's first turn (B1) leaves at most one attacked pawn, and the strategy captures it, so (J2) holds at s̄'s first turn.
Then the induction:
- *s̄ moves; (J1) and (J2) hold before its move.* A king move changes no pawn of either side except that it may capture an s pawn,
  and removing pawns attacks nothing new. A pawn move on f stays on f and below the king: a push needs an empty target and a double
  step needs two empty squares, and the king's square is occupied; so no s̄ pawn reaches a rank above k − 1, in particular none
  reaches its last rank (k ≤ H), and **no promotion is possible** by a pawn on f. A pawn capture needs an s pawn diagonally in front,
  which is exactly an attack, and by (J2) there is none; an e.p. capture needs an e.p. right created by a double step of s, and s
  never double-steps (it captures or passes), while a right present in Q_Z was created by s̄. So no s̄ pawn leaves f, and (J1) holds
  after the move. Only the moved pawn can be newly attacked, because the attack relation is a pairing of an s̄ pawn's square with an
  s pawn's square, and no other pawn moved. So at s's turn **at most one s̄ pawn is attacked**.
- *s moves.* s is not in check: its king stands on f, and s̄'s pawns stand on f and attack files f ± 1 only (on a cylinder of width
  2 the file f ± 1 is the other file, still not f); a king gives no check. So the pass is legal, and so is a capture (no sliders, no
  pins; the king stands where it was). A capture by s is never a promotion: it lands on the square of an s̄ pawn, and s̄ pawns stand
  on rank 2 or higher from s̄'s side, so that square is not on s's last rank. If an s̄ pawn P is attacked, the capture removes P. The
  capturing pawn Q came from file f ± 1 and lands on f, so it attacks no square of file f; and Q attacked only P among s̄'s pawns (it
  attacks two squares, both on files at distance 1 from Q's file, and at most one of them is on f, apart from the width-2 cylinder
  where both squares coincide). The other pairs are untouched. So after s's move (J2) holds, and (J1) holds, since P was the only pawn
  removed.
By induction, no s̄ pawn promotes, and none ever leaves f; s is never in check at its turns, so it is never mated. s̄ cannot win L_T for
any T. ∎ (The proof does not use that s̄'s king is confined to F_Z, nor the move count.)

**Remark (the hypothesis (B1) is needed, and it is not necessary).**
- *Without (B1) the lemma is FALSE.* The strategy "s passes forever" fails when an s̄ pawn can capture an s pawn. The strategy "pass, but capture any s̄ pawn that attacks an s-pawn" fails too, as soon as two s̄ pawns are
  attacked: s captures one and s̄ captures with the other, and the pawn that has left f is no longer blockaded. Counterexamples, all
  with Black = s to move, in the local game of Definition 2.6 with k = ∞, with and without the queen clause. For each, White (s̄)
  wins within T = 3 moves, against every Black move, the pass included. CHECKED-2 for each: at least two of three independently written solvers agree (a C++ solver, a Python solver, and a third solver written from the definition; see each line).
  - cyl:7×6, F_Z = {a, b, c}: `Ka5 kc6 Pc3 Pc4 pb4 pb5`. s̄ = White has two Z-pawns on c, s has b4, b5 (b4 attacks c3, b5 attacks c4).
    After 1…bxc4 White plays 2.cxb4, and the pawn runs to b6, which Ka5 guards; the black king cannot step to b5 or b6. Every Black move
    loses, the pass included (3 White moves at most). The same position is a White win in P with real kings (`kp_p --pmodel`; COMPUTED-1, one code); each of Black's five legal moves loses.
  - flat:4×5, F_Z = {a, b, c, d}: `Kd4 kb5 Pb2 Pb3 pc3 pc4`: each Black move, the pass included, loses within 3 White moves. After
    a pass, 2.bxc4+ and 3.c5=Q (c4 and c5 are guarded by Kd4); after 1…cxb3 2.bxc3, a black pawn run is too slow because c3–c4 gives
    check to the king on b5. Verified by hand, and CHECKED-2 as above.
  - flat:3×5, F_Z = {a, b, c}, f = a: `Kc4 ka5 Pa2 Pa3 pb3 pb4`. s̄ = White has two Z-pawns on a, s has b3, b4 (b3 attacks a2, b4
    attacks a3), and the black king stands on a5, above both. CHECKED-2 (the Python solver and the third solver); not verified by hand.
  - *Size.* A counterexample needs at least 5 ranks, because (B1) is automatic on 4 ranks (PROVED, in the statement above), and 5
    ranks suffice (the flat:4×5 and flat:3×5 examples). Any violation of (B1) needs two s̄ pawns on f and two s pawns. The width is
    not established as minimal: 3 files is the narrowest board with a counterexample found, and boards with fewer than 3 files were
    not searched.
- *(B1) is sufficient and not necessary.* In a bounded enumeration (the boards and pawn counts of the search), s̄ wins 22,456 of
  the 2,233,320 roots with two or more attacked s̄ pawns (about 1.0%); the positions of the kings decide. COMPUTED-1: one C++ implementation, with a Python solver agreeing on a spot check of 92 sampled roots. Random samples with the third solver (win searched within T ≤ 6 or 7) show the same pattern, no White win with at most one
  attacked pawn and wins only with two or more; they give 5% to 8% lost on flat:4×5 and cyl:7×6, a higher share than 1.0%
  because of the small boards and capped pawn counts, so the 1.0% describes that enumeration and is not a general rate.
- *Computer check of the strategy (not part of the proof).* The strategy was run on small boards: 0 violations in 31,355 sampled roots with at most one attacked pawn, over 14 board and file settings (flat 3×4 to 5×6, cyl:4×6, cyl:5×5, cyl:7×6), and in 4,534 roots on flat:3×5 with the third solver (COMPUTED-1 each).
- The uses in §5.2, P5 and P7 are unaffected. In the starting positions s may have a pawn (7.2 `Pd7`, P5 `Pb5`), but in Q_Z, after
  the reply r, s has no pawn (r captures it: Kxd7, Kxb5), and s̄ has one Z-pawn, so (B1) holds anyway.

**Proposition 2.10 (which punishments are universal). PROVED.**
- **(a)** If T = 1 and **H ≥ 5**, then in every chess-legal non-terminal context (every context without a
  passer) no s context pawn can promote in one move, under both the textbook and the e.p.-aware passed test.
  Hence (L2), which counts context pawns only, holds. *Proof:* an s-pawn that
  can promote in one move stands on its penultimate rank (the seventh on 8 ranks).
  - No enemy pawn can stand ahead of it, since no pawn stands on the last rank.
  - It cannot be taken en passant. Only a pawn that has just made a double step can be. In a chess position
    the last move before Y was s̄'s, and so was the last move before Q (r, or in the window form the move that led
    to Q), so no pawn of s has just double-stepped. In §5.3 the window Q is Y itself.
  - So it is passed under either test, and the context would be terminal. The argument needs chess-legal
    contexts: cylcgt's component model can keep a stale right in a component after its owner has moved
    elsewhere.
  - The king's help does not change this: removing a blocker takes a move of its own.
  - *Z-pawns.* (L2) does not count them. They are covered by (L1), whatever their
    distance from promotion: a promotion by s is a failure for s̄ in the local game, and Step 4 of Theorem 2.7 uses
    exactly that. (If s can promote at its first turn, (L1) fails. If an s Z-pawn stands on its penultimate rank but s
    is in check at Q and cannot promote at once, (L1) may hold, and then the theorem applies.) In the uses in §5.2–5.4, P3, P5 and
    P7 the s Z-pawn is captured by r. In §5.3 and P8 it survives; it is far from promotion.
  - *The e.p. clause of (L2).* In the window form (b), Q may carry an e.p. right with
    its target off F_Z, and Q° then lets s use it at its first move. It does not change the T = 1 argument: the
    capture lands on the target square, which is on the third rank of s̄'s side and so is never s's last rank, and a
    pawn that promotes at once still has to stand on its penultimate rank.

  *A stronger statement needs six ranks.* "In a non-terminal context no pawn of *either* colour is one move
  from promotion" is false on 5 ranks under the e.p.-aware test. In `W a2 / B a3 b2` with White to move just
  after ...b4–b2, White may capture en passant on b3, so nothing is passed; yet b2 is one move from promotion.
  - The pawn belongs to the side *not* to move, so (L2) is unaffected.
  - A search of flat 4-file boards with at most 2 pawns a side finds 156 such (position, e.p. right) pairs on 5
    ranks and none on 6 or 7 ranks (COMPUTED-1). A second program finds 120 when the double-step origin must be empty, and none on 8 ranks (COMPUTED-1; its script was not kept).
  - On H ≥ 6 a double step lands H − 4 ≥ 2 moves from promotion, so the stronger statement holds. The proof of the horizon-1 proposition in the main text argues this stronger form, hence its six ranks; its statement concerns the defender only.

  *Four ranks.* For H = 4, a pawn on its second rank promotes by a double step onto the last rank in one move
  and need not be passed, so (L2) can fail with μ_s = 1.

  So, by Theorem 2.7 (PROVED, in P), a group whose punishments satisfy (L1) with T = 1 is decisively
  punished in P in every chess-legal non-terminal context on boards with H ≥ 5, provided (L3) holds. No Z-pawn
  proviso is needed. For T = 1, (L3) asks only that s is not stalemated at its single turn.
- **(b)** For every T ≥ 2 there is a non-terminal context with μ_s = 2 (this requires board width ≥ |F_Z| + 4).
  - *Example (White):* W (f, H−2); B (f, H−1) and (f+1, H−1). No pawn is passed. White captures to
    (f+1, H−1) and promotes next move.
  - So (L2) fails there, and a punishment with T ≥ 2 is never certified for all contexts. That statement is PROVED
    (the example above). Whether the freeze itself fails in P is a different statement. It is split below into a checked example and a CONJECTURE.
  - *Three implementations.* Every number below is exact, in P with real kings, and every one was produced by three codes: the kpsolve family (`kpsolve --frozen` and the `--pmodel` build `kp_p.c`, which share one source), an independently written solver `pk2.c`, and a third solver `ref3`, written from the rules `kings/SPEC.md` alone. "CHECKED-2 (three implementations agree)" below means that they agree on every position of the
    computation. It is a finite computation, not a proof.
  - *Definition (the zero beside a context, in P).* For a group Z and a context G (Definition 2.1) let Φ(G ⊞ Z) be the
    pair (w, b) of P results, White to move and Black to move, from White's view. Let Ψ(G ⊞ Z) be the same pair in the
    frozen model `--frozen` (a king move loses at once, a promotion wins at once, stalemate draws). Ψ plays the role of
    "the result of G": on the sample below it does not depend on the kings (cyl:7×6, contexts on e–f with at most two
    pawns of each colour on ranks 2–5, 1,770 positions: Z_T replaced by two parked kings `Ka1 ka6` gives the same
    Ψ, 0 differences; CHECKED-2, `ref3` and the kpsolve family). That this holds for every G is not
    shown here (a CONJECTURE; the reason one expects it is that kings on F_Z are never attacked by context pawns and
    never block them, Lemma 2.2). **Z acts as 0 beside G (in P)** if Φ(G ⊞ Z) = Ψ(G ⊞ Z).
  - **CHECKED-2 (three implementations agree; no hand proof is given): the zero of a frozen group depends on the
    context, in P.** Z_T = `Ka4 Pb3 kc3 pb4` on cyl:7×6 (the trébuchet of P4, Pattern A of §5.1 with r = 3), and two
    locked context pairs, each a single file with no passer and no move, so each has the value 0 and Ψ = (L, W):
    - G1 = {Pe3, pe4}: Φ = (L, W) = Ψ(G1). Z_T acts as 0 beside G1.
    - G2 = {Pe2, pe3}: Φ = (L, L) ≠ (L, W) = Ψ(G2). Black to move wins by the sortie 1...Kd2, the only winning move
      (Kc2, Kb2 and Kd4 lose; Kd3 is illegal, the pawn e2 covers it; Kc4 and Kxb3 are illegal as well). Z_T does not act as 0
      beside G2.
    - The mirror (colours swapped, ranks reversed, files reflected about b) is G2′ = {Pf4, pf5}: Φ = (W, W) ≠ (L, W),
      White to move wins by Kg5; and G1′ = {Pf3, pf4} behaves as G1 (Φ = Ψ = (L, W); `ref3` and a second code).
    - Same on the group of §5.1 on cyl:8×8 (`Kh5 Pa4 kb4 pa5`, contexts on d–f, ranks 2–7): {Pe3, pe4} gives (L, W)
      and {Pe2, pe3} gives (L, L); {Pe6, pe7} gives (W, W). `ref3` also finds {Pd2, pd3} and
      {Pd3, pd4} different with Black to move, and {Pf5, pf6} and {Pf6, pf7} different with White to move. The
      mechanism was analysed for Z_T only, not for this group.
    - *Mechanism for Z_T: a timing tie, decided by one tempo.* 1...Kd2 steps onto the buffer file next to the context.
      If White punishes the sortie with 2.Kxb4, the b-pawn is free but its own king stands in front of it: it needs a
      step aside and three pushes, four moves, with White to move after Black's capture. Black replies 2...Kxe2 in G2
      and 2...Kxe3 in G1, which makes the black context pawn a passer. In G2 that pawn needs three more moves (king
      steps off, e2, e1=Q), in G1 four (king steps off, e3, e2, e1=Q). White moves first, so White's fourth move
      is before Black's fourth but after Black's third. The two race positions confirm it: `Kb4 Pb3 ke2 pe3`, White to
      move, is lost for White; `Kb4 Pb3 ke3 pe4`, White to move, is won (three implementations). In P a promotion ends
      the game, so no queen is ever captured. In G2 every other White reply to 1...Kd2 loses as well (by the
      solvers); in G1 White wins after 1...Kd2, so the sortie is punished there.
    - *The numbers of Theorem 2.7 (COMPUTED-1, one implementation).* The local game of
      Definition 2.6 after m = 1...Kd2 and r = 2.Kxb4 (Black may pass, White's king confined to the a–c files) has T = 4,
      both for (L1_P) and for (L1) with the queen clause (T = 3 fails). The breadth-first search for μ_s of (L2) gives
      μ_s = 4 in G2 and μ_s = 5 in G1. So (L2) holds in G1 (μ_s = T + 1) and fails in G2 (μ_s = T) by exactly one tempo.
      (L3) was not checked. The sortie is punished only if no context pawn becomes a passer that is at most as slow as
      the punisher.
    - *Distance.* On cyl:8×6 (Z_T on a–c, buffer d and h, context on e–g) the same pair {Pe2, pe3} fails, and moved one
      file away, {Pf2, pf3} and {Pg2, pg3}, it holds (and so do all rank shifts on f and g, except the mirror image
      {Pg4, pg5} of G2). Over all 4,579 contexts on e–g with at most two pawns of each colour on ranks 2–5, 152 have
      Φ ≠ Ψ (47 with a passer, 105 without), and every one has a pawn on e or g, the files next to the buffer. None of
      the 62 non-empty contexts confined to f differs (63 with the empty context), and neither does any of the 81
      single-file contexts on f with up to four pawns of each colour (CHECKED-2: the kpsolve family and `pk2.c`; the 81 also with `ref3`: 0 differ). So in every failing context of this sample a context pawn stands within a step
      of the buffer file the sortie king enters. Whether that is necessary in general is not shown.
    - *The six P4 contexts do not show it in P.* In P all six rows of P4 equal the convention (CHECKED-2, three
      implementations agree), including H*, H*2 and H0 (H0 is G1). The draws that kpsolve finds there in C are
      therefore chess-only effects, not P effects. Their cause was not examined.
    - *Scope.* Z_T on cyl:7×6, contexts on e–f with at most two pawns of each colour on ranks 2–5 (885 contexts):
      838 have Φ = Ψ and 47 do not (43 of the 47 have no passer; CHECKED-2, three implementations). In the 23
      passer-free contexts with Ψ = (L, W) that differ, the side to move loses in Ψ and not in P in 26 (context, side to
      move) pairs, and in all 26 a king step to the buffer file (Kd2 or Kd3 for Black; Kg3, Kg4 or Kg5 for White) is
      among its moves that do not lose. With at most three pawns of each colour (3,237 contexts, the same files and
      ranks) 99 differ: 4 with a passer and 95 without; 39 of the passer-free ones have frozen (L, W); in 44 (context,
      side to move) pairs the frozen mover loses and does not lose in P; no position was left unresolved. This ≤ 3 count is CHECKED-2 (`pk2.c` and the kpsolve family, and `ref3` with its own generator, on cyl:7×6, with and without `--frozen`). Among these positions are cases of
      Corollary 2.7′: `--frozen` reports a win for σ and σ does not win P (G2 with Black to move: `--frozen` is a
      White win, P is a Black win).
  - **CONJECTURE (what remains): the general statement.** For each frozen group with T ≥ 2 there is a context, with
    the defender in zugzwang there, where the freeze fails in P. **A proof is not available as stated, and the
    obstacle is not technical.** T belongs to a certificate, not to a group. A failure needs three things at once for
    one sortie m: (i) the sortie king can reach a buffer square next to a context pawn it can capture (here Kd2, Kg4,
    Kg5), which depends on where the kings stand in Z; (ii) the counter-passer that results is no slower than the
    punisher's *exact* P-win, not the bound T of (L1); (iii) s has no other loss on the way. A converse of Theorem
    2.7 (μ_s ≤ T implies that m is not punished) is false in general (see "No converse"), because s̄ may win faster
    than T or by another reply. So the statement can be settled only group by group, by solving. What is checked
    (CHECKED-2, not a proof): Z_T on cyl:7×6, cyl:8×6 and the group of §5.1 on cyl:8×8, each by an example of a
    context. What is open: a computation solved the 1,236 bare groups on F_Z (§8 item 6) against contexts of at most two pawns a side on the files at distance ≥ 2 (the whole set of 885 on cyl:7×6; smaller file sets or a screen elsewhere, §8 item 6): 269 of 446
    classes fail, and four classes act as 0 beside all 885 contexts on cyl:7×6 (CHECKED-2) with exact-P punishment T_P ≥ 2 on both sides; two of the four fail beside `Pf2 pf3 pf4 pf5`. The T of Definition 2.6 was not computed for them, so the CONJECTURE stands as stated; the exceptions are at the level of T_P and of contexts of at most two pawns a side. For `Kb3 Pa2 Pc2 kb1 pa3 pc3` and `Kb1 Pa2 Pb3 ka3 pb2 pc5`
    there is no failing context in the samples named in §8 item 6 (CONJECTURE that none exists). Open as well: groups in which no sortie king can reach the buffer in time (not isolated by that computation), and every group outside the enumeration.

**Proposition 2.11 (frozen-king passer certificate). PROVED in P (frozen), as a sufficient condition.** A passed pawn need not stay passed: an ω pawn can capture a β pawn on a neighbouring file (Step 2 below deals with this). The computation that accompanies the proof is CHECKED-2: a second, independently written checker finds 0 violations (see the checks below).

*Setting.* F is the frozen promotion model, `kpsolve --frozen`: a promotion wins at once for the promoter; a legal
king move ends the play at once in favour of the opponent of its maker; a side with no legal move at all (king
moves count as moves) that is not in check draws, and one in check loses; infinite play is a draw. The board is
a cylinder with W files and H ≥ 5 ranks (files mod W). On a flat board the same proof works with the neighbouring
files that exist (not separately written out); runs on flat 5×6, 6×6, 7×6 and 6×7 give 434,429 certified positions with side to move and 0 violations (see the checks).

*Notation.* Fix a legal position y (kings not adjacent, the side not to move not in check) before any promotion, the side s to move, a side β (the beneficiary) and ω, the
other side. For a pawn q of either colour let ρ(q) be its rank counted from β's side: ρ(q) = rank(q) if β is
White, and ρ(q) = H + 1 − rank(q) if β is Black, whatever the colour of q. β's pawns advance towards larger ρ, ω's towards smaller ρ; "ahead of p" means larger ρ.
β's start rank is ρ = 2 and ω's is ρ = H − 1. For a pawn p of β put d = H − ρ(p) − [ρ(p) = 2] (the number of β
moves p needs to promote; this is cylcgt's `promote_distance`), and
- e = d if s = ω (ω makes e moves before β's promoting push),
- e = d − 1 if s = β.

*The ω-only game G_ω(y; p).* Delete p. Only ω moves, one move after another. β's other pawns stay where they are
and can be captured. Both kings stay and block squares; nobody captures a king. ω's pawns move as in chess:
push, double step from the start rank over an empty square, capture, and the e.p. capture that y offers (only
as the first move, and only if s = ω). μ_ω(y; p) is the least number of moves after which some ω pawn stands on
its last rank (the promoting move included), or ∞. It is a minimum over **all** ω pawns, passers or not,
with captures allowed. An ω king move ends F at once, so it never occurs in G_ω.

*Hypotheses.*
- **(H1) clear path.** p is a pawn of β that is passed at y in cylcgt's e.p.-aware sense (`passed` with
  `PASSED_RESPECTS_EP = True`: no ω pawn on files f − 1, f, f + 1 with ρ > ρ(p), and p cannot be taken en passant at
  y), and every square of p's file ahead of p, the promotion square included, is empty. So p is the front pawn
  of its file, and **no pawn and no king of either colour** stands on the path.
- **(H2) no check.** No pawn of either colour stands on a file adjacent to the file of β's king.
- **(H3) no stalemate.** ω's king has a neighbouring square t that is not adjacent to β's king, such that no
  pawn of either colour stands on the file of t or on a file adjacent to it. "Not adjacent" means king distance ≥ 2.
- **(H4) no interference.** Every pawn of β other than p that stands on a file adjacent to p's file has
  ρ ≤ ρ(p) + 1.
- **(H5) timing.** μ_ω(y; p) ≥ e + 1.

**Statement.** Under (H1)–(H5), β wins F from (y, s) by pushing p at every turn (the double step first if
ρ(p) = 2).

*Proof.* Write f for p's file and ρ₀ for ρ(p) at y.

*Step 0, three facts about F.*
- (F1) A pawn changes file only by a capture, and lands on the square of the captured piece (an e.p. capture lands
  on the file of the captured pawn). There are no officers before the first promotion, and a king is never
  captured. So a pawn enters a file only by capturing a pawn that stands on it, and a file without pawns never
  gets one.
- (F2) A king move ends F at once. So in any play in which its maker has not lost, no king moves, and both kings
  stand where they stand at y.
- (F3) A promotion ends F with a win for the promoter.

*Step 1, safety of the kings.*
- By (H2) and (F1), no pawn ever stands on a file adjacent to β's king, so no ω pawn ever attacks it. ω's king
  gives no check. So β is never in check, and no push of p is ruled out by king safety.
- By (H3) and (F1), the three files around t never hold a pawn. So t is never occupied, never attacked by a
  β pawn (p included), and is not adjacent to β's king: a move of ω's king to t is always legal, even if ω is
  in check. So ω always has a legal move: it is never stalemated, and F has no draw by stalemate in the play below.

*Step 2, the invariant.* Consider plays in which β follows the strategy Π (push p) and ω moves arbitrarily. Let
ρ_p be the current value of ρ(p) and call the files f − 1, f, f + 1 the *strip*. We show:
- (J_β) at every node with β to move, every ω pawn in the strip has ρ ≤ ρ_p + 1;
- (J_ω) at every node with ω to move, every ω pawn in the strip has ρ ≤ ρ_p, and p cannot be taken en passant;
- (I1) at every node, every square of file f ahead of p is empty.

At y: (J_β) or (J_ω), according to s, is (H1) (passed, aware), and (I1) is (H1). In the following, β's other pawns
and both kings never move, by Π and (F2).
- *β moves.* p goes from ρ_p to ρ′ ∈ {ρ_p + 1, ρ_p + 2}; the squares are empty by (I1), and the move is legal by
  Step 1. By (J_β), the ω pawns in the strip have ρ ≤ ρ_p + 1 ≤ ρ′. A double step (ρ′ = ρ_p + 2) leaves every ω
  pawn in the strip strictly below ρ′, and an e.p. capturer stands on the rank of p, so none exists. A single step
  gives no e.p. right. So (J_ω) holds, and (I1) still holds.
- *ω moves a pawn.* (a) A push or double step lowers ρ. It cannot enter p's square or a square ahead of p on file
  f, because the pawn stands at ρ ≤ ρ_p. (b) A capture lands on the square of a captured β pawn q (or on an e.p.
  target). It captures p never: (J_ω) leaves no ω pawn at ρ_p + 1 next to p, and p is not e.p.-capturable. So
  q ≠ p. If q is on file f, then q stands behind p (nothing of β stands ahead of p by (H1)), and the landing
  rank is below ρ_p. If q is on file f ± 1, then ρ(q) ≤ ρ₀ + 1 ≤ ρ_p + 1 by (H4), and the landing rank is ρ(q). An
  e.p. capture is possible only with the right offered by y when s = ω (Π double-steps only p, and p is not
  capturable): the victim q′ is a β pawn that just double-stepped, the landing square is the skipped square, one
  rank below q′. If q′ is on f ± 1, then ρ(q′) ≤ ρ₀ + 1 by (H4); if on f, it is behind p. Either way the landing
  rank is at most ρ_p + 1. (c) So every ω pawn in the strip after the move has ρ ≤ ρ_p + 1, which is (J_β),
  and nothing lands on file f ahead of p, which is (I1). Captures that land outside the strip change nothing.
  (The tempting one-line argument "ω pawns move away from p's promotion side, so none can ever stand beside its landing
  square" is false: a capture of a β pawn on a neighbouring file puts an ω pawn there. (H4) is what bounds the landing rank.)

*Step 3, consequences.* At every ω turn no ω pawn stands at ρ_p + 1 next to p, and p cannot be taken e.p., so p is
never captured; nothing stands ahead of p on file f ((I1)), so p is never blocked. At every β turn the push is
legal. So Π can be played to the end.

*Step 4, ω's moves are moves of G_ω.* In a play consistent with Π, each ω pawn move is a move of G_ω(y; p): the
squares and the captured pawns are the same, p never takes part (Step 3), β's other pawns stay (Π), the kings
stay (F2), and the only e.p. capture is the one offered at y. (G_ω has fewer obstacles, since p is deleted; this
only enlarges its move set.) So if ω promotes after k of its moves in the real play, then k ≥ μ_ω(y; p). An ω king
move loses at once (F2).

*Step 5, timing.* Under Π, β promotes with its d-th push. Before that push ω has made exactly e moves. By (H5),
e < μ_ω(y; p), so by Step 4 none of those moves promotes, and by Step 1 ω has a legal move each time, so the
play is not a draw. ω's only other moves are king moves, which lose at once. β's d-th push is legal (Step 3)
and promotes, and by (F3) β wins. ∎

**Corollary 2.11a ((V2) at a passer or race terminal of the D-model).** Let y′ be the node reached by a move of M
(N to move), and let cylcgt credit it to b ∈ {M, N}:
- only M has a passed pawn: b = M;
- only N has a passed pawn: b = N;
- both have one (a race, scored by the count rule): b = N if dp(N) ≤ dp(M), else b = M, where dp is
  `promote_distance`.

Then (V2) holds at y′ if (H1)–(H5) hold at (y′, s = N, β = b) for some pawn p of b. Then e = d if b = M (the
opponent moves first) and e = d − 1 if b = N (the beneficiary moves first). This covers the terminal's beneficiary
in both move orders, and a race won by the side to move. The corollary is the proposition at y′. It is
sufficient only (slack example below).

**Corollary 2.11b (the layout of P11).** On cyl:8×6 with `Ka1 ka6` and every pawn on c–g (the a-, b- and h-files
empty), the pawns stay on c–g (F1). Then for either colour as β: (H2) holds (the neighbours of the a-file are b and h);
(H3) holds with t = a5 for ω = Black and t = a2 for ω = White (king distance d(a5, a1) = d(a2, a6) = 4 ≥ 2); and no king stands
on p's file. So at a terminal of such a position only the passed front pawn, (H4) and (H5) have to be checked. A pawn on the a-file breaks (H3): in `Ka1 ka6 Pa3 Pc2 w -` no neighbour of a6 has three pawn-free files.

**Remark (the count rule is not a (V2) certificate).** In the count rule's test, β wins iff dp(ω) ≥ e + 1. This is
(H5) with μ_ω replaced by ω's fastest **passer** distance dp(ω), and dp(ω) ≥ μ_ω whenever no king stands on the
path of that passer (always so in P11's layout). The two agree only if no non-passer of ω is as fast. Without a passer of ω the count rule credits β whatever ω's pawns do, and it sees neither captures
(H4) nor kings (H1, H2) nor stalemate (H3).

**What the hypotheses do (every example is a `kpsolve --frozen --cap 1` result, re-run on a separate build).** A pair such as (L, L) is kpsolve's printed line `A B` for the side to move given: the two cap
bounds, equal in `--frozen`, from White's point of view. It is not the pair (r_w, r_b) of §1.1. Unless a
board is named, it is cyl:8×6; β is White (p = Pc4 or Pc2) unless said otherwise.
- *(H5), both move orders.* ω to move (e = d = 2): `Ka1 ka6 Pc4 pe3 b -` (μ = 2) gives (L, L), so ω wins the tie;
  `Ka1 ka6 Pc4 pe4 b -` (μ = 3) gives (W, W). β to move (e = d − 1): `Ka1 ka6 Pc4 pe3 w -` (e = 1, μ = 2) gives (W, W);
  `Ka1 ka6 Pc3 pe3 w -` (d = 3, e = 2, μ = 2) gives (L, L). With Black as β: `Ka1 ka6 pc3 Pe4 w -` (ω to move,
  μ = 2) gives (W, W) and `Ka1 ka6 pc3 Pe3 w -` (μ = 3) gives (L, L).
- *(H5), non-passers count.* `Ka1 ka6 Pc2 Pd4 pd3 b -`: p = Pd4 is a passer (d = 2) and the only Black pawn is not
  one, but d3xc2 and c1=Q take ω two moves. (L, L), although cylcgt credits White. This is the position
  after c3xd4 in `Ka1 ka6 Pc2 Pc3 pd3 pd4 w -`, whose D-result is a White win and whose `--frozen` result is (L, L):
  the D-result and `--frozen` differ at this root. Race: `Ka1 ka6 Pc4 Pd2 pe3 pf4 b -` is (L, L); the count rule
  credits White (dp = 2 against dp(Black) = 3 for the passer f4), but Black's non-passer e3 takes d2 and promotes in two.
- *(H5) is not necessary.* cyl:7×6 `Ka1 ka6 Pc2 Pd3 Pf2 pe4 b -` has μ = e = 3 and is (W, W): the proposition says
  nothing there.
- *(H4), and the threshold ρ(p) + 1 is exact.* `Ka1 ka6 Pc2 Pd4 Pe2 pe5 b -` is (L, L): p = c2, Pd4 stands at
  ρ = ρ(p) + 2, and e5xd4 followed by d3, d2, d1 takes ω four moves (μ = 4 ≥ e + 1 = 4, so (H5) holds); the
  pawn on d4 then attacks c3 and the double step is met by dxc3 e.p. `Ka1 ka6 Pc2 Pd3 Pe2 pe5 b -`
  (Pd3 at ρ(p) + 1) is (W, W). The failure arises inside the D-model: `Ka1 ka6 Pc2 Pe2 Pe3 pd4 pe4 pe5 w -` has D-result
  "White wins" (e3xd4 makes c2 a passer, a terminal credited to White) and is (L, L) in F.
  With the bound ρ(p) + 2 in place of ρ(p) + 1, the end-to-end run below refutes 8 certified wins (9,852 roots, cyl:6×6); so does
  dropping (H4) (16 of 80 positions with side to move on cyl:6×6).
- *(H2).* `Ke2 ka6 Pc4 pf4 b -` is (L, L) (f4-f3+ forces a king move or no reply), `Ka1 ka6 Pc4 pf4 b -` is (W, W);
  in both p = c4, d = 2 and μ = 3 = e + 1.
- *(H1), kings.* `Ka1 kc5 Pc4 pf4 b -`, `Kc5 ka6 Pc4 pf4 b -`, `Kc6 ka6 Pc4 pf4 b -` and `Ka1 kc6 Pc4 pf4 b -`
  (a king of either colour on the path, or on the promotion square) are all (L, L).
- *(H1), e.p.* `Ka1 ka6 Pe4 pd4 b e3` (e4 has just been played, e.p. right on e3) is (L, L); the same position
  without the right, `... b -`, is (W, W). The textbook passed test calls e4 passed at once, the aware test does not.
  Another: `Ka1 ka6 Pc3 Pd4 Pf2 pc4 b d3` is (L, L) and `... b -` is (W, W): the right is the only reason that
  μ = 3 ≤ e = 3 (the e.p. capture is the first move of G_ω).
- *(H3).* `Ke1 ka6 Pa4 Pc5 Pg5 pa5 b -` is (D, D): p = c5 (d = 1), (H1), (H2), (H4) and (H5) hold (μ = ∞: a5 is
  blocked and has nothing to capture), but Black has no legal move: a4 covers b5 and h5 across the seam, c5
  covers b6 and g5 covers h6. Without Pg5 the king can step to h6 (and lose), and the position is (W, W). Also
  flat:7×6 `Kb1 ka6 Pa4 Pc2 Pc5 pa5 b -` is (D, D); there the static (H2) fails, but no check can occur.
  (P1a of §5.4, cyl:7×6 `Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5 b -`, is (D, D) too, but it is not an example for (H3):
  the black king stands on c6, the promotion square of c5, so (H1) fails as well.)

**Checks (data, not proof; kpsolve built from `kings/kpsolve.c`).** The first checker decides (H1)–(H5) with its own move generator; only `passed` and `promote_distance` are cylcgt's.
- *Proposition against `--frozen`, kings parked* (`Ka1` and a Black king on the top rank of the a-file, the b-file and the
  last file empty, pawns on files c to W − 2, ≤ 3 per side except where noted; both colours as β, both sides to move; the
  unit is a position with its side to move, certified for one β by some p): cyl:6×6 74,410
  positions, cyl:8×6 (≤ 2 per side) 64,954, cyl:6×7 306,020, cyl:6×5 12,160, cyl:7×6 496,848: **0 violations in
  954,392**. With (H4) dropped: 16 of 80 (6×6), 56 of 456 (6×7), 32 of 368 (7×6) violate.
- *Independent check (a second, separately written program).* An instance is a position, a side to move, a beneficiary β and a pawn p. The checker decides (H1)–(H5) with its own move generator and a search for μ_ω, and agrees with
  cylcgt's `passed` on 2,000 random positions. Certified instances, all of them β wins in `--frozen`: cyl:6×6 parked,
  ≤ 3 a side, 91,074 (74,410 positions with side to move, the same count as above); cyl:7×6 parked, ≤ 2 a side, 29,140,
  and 20,000 random positions with 3 a side, 23,363; cyl:8×6 with random kings, 2,751; cyl:6×6 with an e.p. right, 5,716
  (2,356 of them with another β pawn capturable e.p. and ω to move): **0 violations**. Dropping (H4) gives 80, 24 and
  23 violations on the parked boards; dropping (H2) or (H3) gives 3,277 and 2,086 with random kings.
- *Kings anywhere* (random placements, so that (H2), (H3) and the king clause of (H1) are tested as stated): cyl:7×6,
  cyl:8×6 and cyl:6×7, 20,000 positions with side to move each, ≤ 3 pawns a side: 0 violations in 60,000. With one hypothesis dropped,
  the violations are: (H2) 1,744, 1,853 and 1,394 of 20,000; (H3) 8 of 19,033, 8 of 16,599 and 5 of 20,000; the king
  clause of (H1) 563 of 1,315, 469 of 1,020 and 556 of 1,783; (H4) 0 of 4 and 0 of 9 (too few) and 2 of 11.
- *Chain D → P, end to end* (kings parked; no passer at the root; both sides to move): cyl:6×6 files c–e, ≤ 3 pawns a
  side, 9,852 roots; cyl:7×6 files c–f, ≤ 3 a side, 40,204 roots; cyl:8×6 ≤ 2 a side, 5,384 roots; cyl:6×6 ≤ 2, 1,432
  roots; 56,872 in all. The conservative D-game in which a side's own terminals, and the opponent's moves into
  terminals credited to it, must be certified by Corollary 2.11a gives a win only if `--frozen` agrees: 48,000
  certified wins, 0 violations. When **every** terminal of the D-game is certified (26,014 roots), `--frozen` equals
  the D-result (o(W)): 0 violations. Without (H4) in the certificate: 8 violations (cyl:6×6). `--frozen` differs from
  o(W) at 3,194 of the 56,872 roots, all of them with some uncertified terminal.
- *Further programs (two more checkers, written without reading the code of the first two).* An instance is (position, side to move, β, p).
  - Exhaustive with kings parked on the a-file (all legal a-file king pairs): cyl:5×6 files c–d ≤ 3 a side, cyl:6×6
    c–e ≤ 3, cyl:7×6 c–f ≤ 2, cyl:8×6 c–g ≤ 2, cyl:6×7 c–e ≤ 2. Exhaustive with free kings: cyl:5×6 c–d ≤ 3, cyl:4×6.
    Random scenes built for the tight cases (cyl:5×6 to 8×6, 6×7, 6×5) and uniform random positions (cyl:5×6 to 8×6,
    6×7). On these cylinders, in all,
    5,730,596 certified positions with side to move (6,783,482 instances): **0 violations**, and no position is
    certified for both colours. Flat 5×6, 6×6, 7×6 and 6×7: 434,429 positions (516,823 instances), 0 violations.
  - The tight cases occur among the cylinder instances: (H5) with μ = e + 1 (3,306,911 instances), another β pawn at ρ(p) + 1 on an
    adjacent file (242,044), an ω pawn entering the strip by a capture (307,127), an ω e.p. right against another
    β pawn (333,474), ω in check at y (48,190), races (4,642,279).
  - Controls: on cyl:6×6 parked (all legal a-file king pairs, so a larger sample than the 16 of 80 above), dropping (H4) gives 24 of 940 failures, and the same 24 fail with the bound
    ρ(p) + 2 (`Ka1 ka6 Pe2 pc5 pd3 pe5 w -`); (H5) weakened to μ ≥ e gives 6,891 of 7,855; dropping the e.p. clause
    of (H1) gives 272 of 692. With random kings, dropping (H2) or the king clause of (H1) gives hundreds of failures
    per board, dropping (H3) 1 to 12.
  - Reproduced exactly: every parked count above that was re-run (74,410; 64,954; 306,020; 12,160;
    496,848; the second program's 91,074 and 29,140), the end-to-end figures (48,000 conservative wins, 26,014 fully certified
    roots, 3,194 differences, 8 violations without (H4)), and every example above. On cyl:8×6 with pawns on c–g
    (≤ 2 a side), (H2), (H3) and the king clause of (H1) held in all 371,250 instances (Corollary 2.11b), and
    dp(ω) ≥ μ_ω held in all 378,407 instances with no king on the fastest passer's path (the count-rule remark).

**Remark 2.11 (the certificate is not special to kings; real kings).** The same (V2) question arises for passer
terminals. The certificate of Definition 2.6 (king moves) does not apply to a passer as written (Q_Z deletes the
passer, r is not a king capture, the owner's king may leave F_Z, the component's own pawns are unaddressed).
Proposition 2.11 supplies the missing certificate for passer and race terminals **in the frozen model**, and
Corollary 2.11a states it for the D-model.
- **Proved about real kings: Theorem 2.11K below, a square rule with a no-stalemate clause (PROVED in P).** Every step of Proposition 2.11 uses (F2). The hypotheses (H1)–(H5) are not enough with real kings:
  `Ka1 ka6 Pc2 w -` (cyl:8×6) satisfies (H1)–(H5) with μ = ∞ and is (W, W) in F, but P with real kings (the `--pmodel` build `kp_p`) and chess (kpsolve exact) both give (D, D).
- **Corollary 2.8** is the real-king statement for one pawn: a single-pawn local game with a king beyond reach.
- **Real-king square rule: the first statement is FALSE (CHECKED-2); with a no-stalemate clause it is PROVED in P.**
  - *The statement without a no-stalemate clause is false.* It reads: let β's king be sheltered as in (H2), let the pawn data satisfy (H1), (H4) and (H5) with
    ω's king allowed to move and to capture β's other pawns in G_ω, let q₀, …, q_d be the squares p occupies before its first push and
    after each push, and n_j = j if s = ω, j − 1 if s = β; if d(k_ω, q_j) ≥ n_j + 2 for every j (j = 0 only if s = ω), then β wins P with real kings.
    It drops (H3) of Proposition 2.11, and with real kings ω can be stalemated, or can walk into a stalemate, which is a draw in P (the Remark's own
    caveat). CHECKED-2 (kp_p `--pmodel`, a second, independently written P solver and a pure-Python solver `pyp.py` agree; an independently written certificate checker accepts the named pawn in each case): cyl:6×6 `Ka4 ka6 Pa5 Pd5 b -` (β = White, p = d5, Black has no legal move at y itself), flat:6×6
    `Kc1 ka1 Pc2 pa2 w -` (one pawn each, ω's king is shut in by its own pawn and β's king), `Kc1 ka1 Pc2 pa3 w -` (ω steers into the stalemate: c3 pa2 c4) and
    `Kd2 kf1 Pa2 Pf3 pf2 pd3 w -` (stalemate after the first push) are (D, D) although every hypothesis holds. Samples with the White king on a1 only and ≤ 2 + 2 pawns cannot meet such nets.
    Two implementations of the certificate in one code base agree on 15,000 random positions (COMPUTED-1).
  - *Counts (β = White; the flip of ranks and colours gives β = Black, checked on 175,454 positions, COMPUTED-1).* Exhaustive over all kings, both sides to move, e.p. rights,
    COMPUTED-1 (one program): certified positions and the violating ones (kp_p value not a β win): cyl:6×6 ≤ 4 + 4 pawns 142,434,153 certified, **496 violating**; cyl:6×6 ≤ 3 + 3 19,373,221, 32;
    cyl:7×6 ≤ 3 + 3 117,348,760, 101 (≤ 3 + 2: 26,083,399, 93; ≤ 2 + 2: 3,740,009, 2); cyl:8×6 ≤ 2 + 2 10,378,374, 4; flat:6×6 ≤ 3 + 3 299,322,340, **54,452** (≤ 2 + 2: 11,838,544, 5,490); flat:7×6 ≤ 2 + 2 40,233,315, 9,662.
    The small sweeps were reproduced exactly by a second program with its own enumeration, its own certificate and kp_p (CHECKED-2): flat:6×6 ≤ 1 + 1 156,528 certified, 208 violating (all (D, D)); flat:7×6 ≤ 1 + 1 357,542, 276; flat:6×6 ≤ 2 + 0 171,334, 36;
    cyl:6×6 ≤ 2 + 2 1,072,469, 1 (`Ka4 ka6 Pa5 Pd5 b -`). One pawn in all (1 + 0) never violates (CHECKED-2 on flat:6×6, flat:7×6 and cyl:6×6); 1 + 1 violates on flat boards only (flat:6×6 208, flat:7×6 276 positions, kp_p on every position;
    CHECKED-2), on cylinders from 2 pawns (cyl:6×6 ≤ 2 + 0 has 1; CHECKED-2).
    A strategy simulation (own move generator, checked against `pyp.py`) plays "β pushes p every turn" against all ω lines on every certified instance: its only failures are ω stalemates
    (at y or later) — no capture of p, no block, no earlier ω promotion in any sweep — so a violation can only sit where the simulation shows a stalemate line, and kp_p was run on all of those (COMPUTED-1 for the large sweeps; a second simulation reports a stalemate as the only failure on the small ones, CHECKED-2).
    "ω not stalemated at y" is not enough (22 violating instances of the cyl:6×6 ≤ 4 + 4 sweep and 45,566 of the flat:6×6 ≤ 3 + 3 sweep remain; COMPUTED-1).
    The control without king moves in G_ω (variant KV = 2) fails on 153,582 instances of cyl:6×6 ≤ 3 + 3 (ω promotes first; COMPUTED-1). The simplest mechanism is that the king steps off its own pawn's path
    and its pawn then promotes: cyl:6×6 `Ka1 ke1 Pc2 pe2 w -` passes every hypothesis under KV = 2 (the king is frozen, so the pawn on e2 never moves) and is (L, L) in P, since Black plays Kd1 and e1=Q before c6 can be reached
    (kp_p, and the second certificate checker accepts it under KV = 2; COMPUTED-1). So (H5) must use the king.
  - ***Theorem 2.11K.* PROVED in P.** Notation of Proposition 2.11; Π is "β pushes p at every
    turn (the double step first if ρ(p) = 2)". Assume (H1) (path free of pawns and kings), (H4), (H2) (no pawn of either colour on a file adjacent to β's king's file),
    (H5K) μ^K_ω(y; p) ≥ e + 1, where μ^K_ω is μ_ω in G^K_ω, which is G_ω with ω's king allowed one step per move onto a square that is not an ω pawn, not β's king and not adjacent to it,
    capturing β's other pawns (the variant that also forbids squares attacked by a remaining β pawn is covered too), (SQ) d(k_ω, q_j) ≥ n_j + 2 for j = 0, …, d (j = 0 only if s = ω), and
    (NS) in no play of Π is ω stalemated at one of its turns (a search of depth ≤ e over ω's replies); (NS) follows from (H3K): every square x with d(x, k_ω) ≤ e − 1 has a king-neighbour t with
    d(t, k_β) ≥ 2 and no pawn of either colour on the files of t, t − 1, t + 1. Then β wins P from (y, s) by Π.
    *Proof.* (F1) a pawn changes file only by a capture, landing on the captured pawn's square (e.p.: on the captured pawn's file); a king capture only removes a pawn; so a pawn enters a file only by
    capturing a pawn on it and a file without pawns never gets one. (F2) the first promotion ends P with a win for its maker. (F3) under Π only p moves.
    *Step 1.* By (H2) and (F1) no pawn ever stands on a file adjacent to β's king, so no ω pawn attacks it, and ω's king is never adjacent to it: β is never in check and no push exposes β's king.
    *Step 2.* Exactly Step 2 of Proposition 2.11, proved by induction on the plies of the play (Steps 2 and 3 use each other: Step 2 assumes that p is still on the board, Step 3 shows that ω's king never takes it; the induction runs over the plies, and at each ply both statements hold for the earlier plies):
    (J_β) at β's turns every ω pawn in the strip f − 1, f, f + 1 has ρ ≤ ρ_p + 1; (J_ω) at ω's turns it has ρ ≤ ρ_p and p cannot be taken e.p.; (I1) no pawn stands ahead of p on its file.
    The proof uses only pawn moves, (H1), (H4) and (F1)–(F3); king captures remove β pawns and add none, so every bound on a landing rank can only drop. Hence no ω pawn captures p or lands ahead of it.
    *Step 3.* After β's j-th push p stands on q_j and ω has made n_j moves, its king at distance ≤ n_j from k_ω; to capture p it needs distance ≤ 1, i.e. d(k_ω, q_j) ≤ n_j + 1, against (SQ) (for j = 0, s = ω, no move has been made and d(k_ω, q₀) ≥ 2).
    Before the (j + 1)-th push ω has made n_{j+1} moves, so its king is on q_{j+1} only if d(k_ω, q_{j+1}) ≤ n_{j+1}, against (SQ); the square skipped by the double step is adjacent to q₁ and at distance ≥ n₁ + 1. β's king is not on the path (H1).
    With Step 2 every push of Π is legal.
    *Step 4.* β always has the push; by (NS) ω has a legal move (or is mated, a win for β) at each turn.
    *Step 5.* Every ω move before β's promoting push is a move of G^K_ω from y (pawn moves: the squares empty in the play are empty in G_ω, where p is deleted, captured pawns are β pawns other than p, the only e.p. capture is the one offered at y;
    king moves: a legal king step goes to a square that is not an ω pawn, not β's king, not adjacent to it, and captures a β pawn other than p). Before β's d-th push ω has made exactly e moves, and (H5K) says that none of the e-move plays of G^K_ω puts an ω pawn on its last rank.
    So ω does not promote first, and the d-th push promotes: β wins by (F2).
    *(H3K) ⟹ (NS).* At ω's m-th turn (m ≤ e) its king stands on some x with d(x, k_ω) ≤ m − 1 ≤ e − 1. For the t of (H3K), the three files around t hold no pawn, hence (F1) never do: t is never occupied by or attacked by a pawn, t is not β's king and not adjacent to it, so the step x → t is legal even in check. ∎
    Computational counterpart (COMPUTED-1): on every certified instance of every sweep (H3K) implies (NS) (0 exceptions among 761,023,066 certified instances, that is 609,716,942 certified positions, in the five top sweeps; an instance is a position with a choice of β and p; the nested sweeps are not added), and (NS) leaves 0 violations, kp_p and the simulation agreeing on all instances solved by both.
    These are checks of the proved implication and of the theorem, not part of the proof. A second program's samples agree (COMPUTED-1: 16,500 random positions on six boards, and all 1,072,467 certified positions of cyl:6×6 ≤ 2 + 2 without a stalemate line are (W, W) in kp_p; 0 exceptions).
  - *CONJECTURE′ (evidence only).* Replace (NS) by (H3) of Proposition 2.11 at ω's own king: k_ω has a neighbouring square t, not adjacent to β's king, with no pawn on the files of t, t − 1, t + 1. 0 violations in all sweeps and hunts, but in 565
    cases (172 instances in the exhaustive sweeps, 393 positions in random hunts; COMPUTED-1) ω has a line that stalemates Π and β still wins by another move (kp_p), so Theorem 2.11K does not cover them and a proof needs another strategy for β.
    The 172 are 134 (flat:6×6 ≤ 3 + 3) + 36 (flat:7×6 ≤ 2 + 2) + 2 (cyl:8×6 ≤ 2 + 2); the flat:6×6 ≤ 2 + 2 sweep (8 instances) is nested in the ≤ 3 + 3 one and is not added again.
  - The chess form needs (A_Q) at the resulting position (§1.2) and is not claimed.
- P11 in §6 relies on Proposition 2.11 in the sense given there. P11 is a frozen-model statement (`--frozen`); it does not use Theorem 2.11K, which is about P with real kings, and Theorem 2.11K does not change P11.

---

## 3. Spare tempo moves as loopy games

**Definition 3.1 (pass reservoirs).** Each reservoir is a D-game with a single position ω.
- **on_D:** L(ω) = {ω}, R(ω) = ∅. White can pass forever; Black has no move.
- **off_D:** the mirror image.
- **dud_D:** L(ω) = R(ω) = {ω}.

Their CGT analogues are on = {on | }, off = { | off} and dud = {dud | dud} (KNOWN: [WW] ch. 11 "Games
Infinite and Indefinite"; [S] ch. VI). Also KNOWN [S, ch. VI]:
- on exceeds every number;
- on, off and over are stoppers, while dud is not;
- G + dud is a draw for every G in which only running out of moves decides the game.

**Proposition 3.2 (a shuttling king is a pass). PROVED.** Let Z be a king group and z ↔ z′ two non-capturing
White king moves inside F_Z, with:
- in both z and z′, every Black Z-move a suicide in the D-model;
- the two shuttle moves legal in every context, which Lemma 2.2 guarantees, since they stay on F_Z.

Then, in the D-model and for a short context G, r(G ⊞ Z) ≥ r(G ⊞ on_D), with equality if White has no other
Z-moves. (Two shuttles, one for each king: Proposition 3.2′ below.)

*Proof.*
- The relation {(z, ω), (z′, ω)} is a bisimulation. In each of z and z′, White can move to the other, and
  Black's Z-options are all suicides. So the 2-cycle has the same results as the 1-cycle ω.
- Black's suicides can be deleted (Lemma 1.7). This is valid in chess only under (V1b): Black must always
  have the legal suicide.
- Any further White Z-moves only help White (Lemma 1.6). ∎

**Chess bridge** (PROVED, by the sharp form of Theorem 1.14 with D = G ⊞ on_D; the proof of Theorem 1.14(i) does not apply, since it assumes that σ never moves in Z, which White's shuttle violates).
Here G is the pawn-only D-model of the context, with the e.p. flag as a coordinate. The pass of on_D resets the flag,
as White's shuttle does in chess (a king move ends an e.p. right; Remark on e.p. after Proposition 3.2′). Let X be a
chess position with Z and context G as in Proposition 3.2, and suppose r(G ⊞ on_D) = W at π(X). Let Σ be a rank-lowering White strategy in G ⊞ on_D, with its passes played as the shuttle, and let
N be the set of chess positions before the first promotion that arise when White plays Σ as chess moves and Black
plays any legal D-move, starting from X (so X ∈ N), up to the first closing move (π sends both shuttle
states to ω). Assume, at the nodes of N:
- (V1a) with White to move, the move Σ prescribes is legal; if Σ prescribes a position of G ⊞ on_D (not a ⊕), the
  move does not promote and leads to the matching position (the shuttle is legal by the hypothesis of Proposition 3.2,
  which Lemma 2.2 secures against context pawns). With Black to move,
  every legal Black context move is an option of G, and if that option is a position, the move leads to the matching
  position. The context moves of both sides obey condition (E) for e.p.;
- every Black Z-move is decisively punished in P;
- every decisive event of G that is reached is a P-win for its beneficiary;
- Black is not stalemated.

Then X is a P-win for White. *Proof:* N is White-certified for the sharp form of Theorem 1.14.
- (S1): if Σ prescribes a ⊕, White's move is a decisive event of G and is closing by the third bullet. Otherwise
  it is a D-move by (V1a), and it lowers ρ, a pass included, because Σ chooses an option of smaller rank.
- (S2): before the first promotion every Black move is a context move or a Z-move (Definition 2.1, Lemma 2.2). A
  Black context move is a D-move to a node of N, or an option of G to a terminal. A ⊕ is closing by the third
  bullet. A ⊖ (a Black promotion, for instance) would be a ⊖ option of a Black node of W_White, and there is none.
  Black has no move in on_D, so a Black Z-move is not a D-option; it is closing by the second bullet.
- (S3) is the last bullet. Checkmate of Black is a P-win, so only stalemate has to be excluded.

The sharp form gives a P-win. The mirror statement holds for Black wins.

(V1a) is required along Σ only. The stronger reading "every legal chess move of the side to move is one of the D-options" would exclude the Black Z-moves that the second bullet is about, and it would ask for White moves that Σ never plays. Moves that Σ makes to a ⊕ have no matching position; the shuttle ends an e.p. right, so the pass resets the flag; and the last bullet excludes stalemate only, not checkmate, which is a White win. The bridge needs (V1a): it fails in P2 + H\* if White plays e3–e4, which stalemates Black, so the bridge may only be used along a strategy that avoids that move; kpsolve gives (W, W) for P2 + H\*.

**Theorem 3.3 (BIG fails with a shuttle). PROVED.**
- **(a)** For every short CGT game G, including games with ±B terminals, G + on is in 𝓛.
  *Proof:* Left always has the move on → on, and Right never has a move in on. Right's moves in G are
  finitely many in any play, so Right runs out and loses, whoever starts.
  - In particular on + (−B) is in 𝓛 for every B. (KNOWN as "on exceeds every number", [S] ch. VI.)
- **(b)** In chess semantics, { | ⊖} ⊞ on_D is (L, L): Black plays ⊖ when on move, and White can only pass.
  (With the other reading of ∅, A′ = {∅ | ⊖}, the pair is (W, L) in the D-model: White plays A′ → ∅ and
  leaves Black with no move at all, which the D-model scores as a loss for Black and chess as a stalemate. The
  statement above uses the same A′ = { | ⊖} as Proposition 1.13.)

So once a White shuttle is modelled as on, the BIG convention predicts "White wins" for every position. That
is false whenever Black has a forced decisive event.
- The reason is that BIG encodes "decisive" as "many spare moves". An infinite tempo supply outlasts any
  finite BIG; the tempo-count condition of Proposition 1.13 fails for every B.
- The fix is to make decisive events terminal (game-ending), which the D-model does. This is the setting
  that *affine normal play* formalises (Larsson–Nowakowski–Santos, GONC 6, 2025). Nothing below depends on that paper.

**Theorem 3.4 (outcome rules with passes). PROVED.** Let G be a short D-game under normal play, and write x
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

*Proof.*
- **(a)** States are pairs (x, s); a pass moves (x, s) to (x, s̄). Use the least fixed point of
  Definition 1.2.
  - Suppose Left first wins (x, L) at stage n by passing. Then Left won (x, R) at an earlier stage. But
    Right's pass from (x, R) leads back to (x, L), so (x, L) was won at a stage earlier still, a
    contradiction.
  - So Left's winning moves are always G-moves. Left wins (x, R) iff every Right option, Right's pass
    included, leads to a Left win.
  - That is the recursion above. It is well-founded: Λ_L(x) uses Λ_R only at G-successors of x, and Λ_R(x)
    uses Λ_L at x and at its successors. Compute it in reverse topological order.
  - If G has no terminals, Λ_L fails at the sinks and therefore everywhere.
- **(b)** The only non-G move is White's pass (x, L) → (x, R), and from (x, R) every move is a G-move.
  - Black makes finitely many moves in any play, since G is finite and acyclic, and plays alternate. So every
    play is finite, the game is determined (Zermelo, KNOWN), and there are no draws.
  - Black's wins satisfy the stated recursion: Black needs a winning G-option, since it has no pass, and
    every White option, including the pass, must lead to a Black win.
  - If Black has no option at all, Black loses: the "some" over an empty set fails. ∎

**Corollary 3.5 (monotone chain). PROVED.** For every x and s:

  W in G ⊞ dud_D ⇒ W in G ⊞ off_D ⇒ W in G ⇒ W in G ⊞ on_D,

and the mirror chain holds for L.

*Proof.*
- **First step.** By (a), a winning White strategy in G ⊞ dud_D uses no passes and beats every Black
  behaviour, passes included. So it wins G ⊞ off_D.
- **Second step.** G has fewer Black options (Lemma 1.6). A Black player without moves now simply loses.
- **Third step.** on_D adds White options (Lemma 1.6). ∎

**Sums with loopy components.** Everything here is about D-games in the
sense of Definition 1.1, with loopy components allowed, the sum ⊞ of Definition 1.3 (the first decisive event ends the
whole play, infinite play is a draw) and the loopy CGT translation y^B, which is Definition 1.4 used verbatim for loopy components (Definition 1.4 states it for short
ones; ⊕ ↦ the chain +B, ⊖ ↦ −B; the translated components have no terminals, and Σ y_i^B is the ordinary disjunctive sum under normal play, with draws by
infinite play). First-event dominance (below) is Definition 1.10 restated for loopy components.
- *Labels.* Theorem 3.7, Lemma 3.8a, Theorem 3.8, Corollary 3.8b, Propositions 3.9 and 3.10 and Theorem 3.11 are PROVED. Corollary 3.11a is immediate from Theorem 3.11, and the body of Proposition 3.12 follows from Theorems 3.3 and 3.4 (both PROVED). Random tests of the statements (564 bridge positions, 546 criterion positions, 3,584 sandwich positions, 1,185 reserve implications, 0 failures) are COMPUTED-1. The brute-force results are CHECKED-2 where two independent solvers agree (`dsum.py` and a second solver written from scratch: 20,324 states, 0 disagreements) and COMPUTED-1 otherwise (a count from one generator); the chess P-model counts are COMPUTED-1, because the P-model oracle was run only once.
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

**Theorem 3.7 (loopy bridge). PROVED.** If Y is first-event dominant for B, then for every reachable tuple Y′ and both
movers the D-result of ⊞ y′_i equals the outcome of Σ (y′_i)^B (W, D or L). No shortness or stopper hypothesis.

*Proof.* Let 𝒟 be the D-graph on reachable tuples with a mover and 𝒞 the CGT graph. A D-option to a non-terminal is the same
move in 𝒞; a D-option to σ in coordinate j is the 𝒞-option to the frontier position (σB in coordinate j, the other mover to
move); 𝒞 has no other options, and a node has an option in 𝒟 iff it has one in 𝒞.
(⊆) By induction on the 𝒟-stage, W^𝒟_σ ⊆ W^𝒞_σ: a σ̄-node with no option has none in 𝒞. A σ-node with a σ-terminal option has the 𝒞-option
to a frontier position of sign σ, a σ-win by dominance; one with an option in W^𝒟_{σ,n} has the same option in 𝒞, in W^𝒞_σ by induction.
A σ̄-node of W^𝒟_σ has no σ̄-terminal option, and each other option is a σ-terminal (frontier, dominance) or in W^𝒟_σ (induction).
(⊇) By induction on the 𝒞-stage, for nodes of 𝒟. A σ-node with a winning 𝒞-option: if it is a frontier position, its sign is σ,
because a frontier of sign σ̄ is a σ̄-win by dominance and W_L ∩ W_R = ∅; so 𝒟 has the σ-terminal option. A σ̄-node all of whose 𝒞-options are in W^𝒞_σ has no
frontier option of sign σ̄ (same reason), so each 𝒟-option is σ's terminal or a node in W^𝒞_σ, hence in W^𝒟_σ. ∎

**Lemma 3.8a (subadditivity). PROVED.** If Left wins G_1 + n_1 second and G_2 + n_2 second (any loopy normal-play games), Left wins
G_1 + G_2 + (n_1 + n_2) second; and if Left wins G + n second she wins G + m second for m ≥ n. So the reserve of a sum is at most the
sum of the reserves, for λ and for ρ.

*Proof.* In H_i = G_i + n_i Left follows a stage-lowering strategy of W_L. Let Φ = ρ_1 + ρ_2 at positions with Right to move.
Right moves in one component (not in tokens); Left answers in the same component with a stage-lowering move (a token or a G_i-move).
Φ drops by at least 2 per round, Left always has a reply, and when Φ = 0 Right is to move with no option anywhere and loses.
Extra tokens are never used and never hurt. ∎

**Theorem 3.8 (reserve criterion; the loopy Theorem 1.11(b)). PROVED.** Let Y = (G_1, …, G_k), B ≥ 1. If for every j and every σ for which
some reachable node of G_j has an event of sign σ,

  Σ_{i≠j} Λ_B(G_i) ≤ B − 1 (σ = +),  Σ_{i≠j} P_B(G_i) ≤ B − 1 (σ = −),

then Y is first-event dominant for B, so by Theorem 3.7 the D-result of ⊞ is the CGT outcome of Σ y_i^B at every reachable position.
Moreover:
- (a) *Theorem 1.11(b) is the special case of short, pairwise safe components with B > max(M_L(Y), M_R(Y)).* For a short y with no
  ⊖ reachable, λ_B(y) ≤ M_R(y): y^B has no −B, Right makes at most M_R(y) moves in it (a move into +B counts as one, and the chain has
  no Right option), and Left answers each with a token. Pairwise safety (Definition 1.10) says that if + is a threat in G_j then no node of any
  other component has an option ⊖, so Σ_{i≠j} Λ_B(G_i) ≤ M_R(Y) ≤ B − 1; σ = − is symmetric.
- (b) *It is strictly stronger.* A = `{ ∣ ⊕}` (Right's only option is the suicide ⊕) and C = `{⊖ ∣ }` have threats of opposite sign
  (Definition 1.10 counts the suicides, so they are not pairwise safe), yet all four reserves are 0: Left has no move in A, so Right, moving
  second, wins A − 0 at once; Right has no move in C. The criterion holds for every B ≥ 1 and the D-result (L, W) is the outcome of `{ ∣ B} + {−B ∣ } = 0`.
- (c) *Necessity of the reserve condition for dominance, for one rest component.* If the rest of an event is a single component G with a reserve ∞
  opposite the event (e.g. `off` beside a ⊕ event), dominance fails for every B: it needs Left to win B + G^B second, i.e. λ_B(G) ≤ B. This is necessity for dominance only, not for D = CGT:
  `{⊖∣} ⊞ on` is not dominant (the event ⊖ has the rest `on`, with ρ = ∞), yet D = CGT = (W, W) for B = 2, 5, 9, because Right can never force the −B (Proposition 3.12). In 9,592 random cases with an infinite reserve opposite an event, dominance failed in all (COMPUTED-1).

*Proof.* Let (Y′, j, +) be an event, R = Σ_{i≠j} (y′_i)^B and Λ = Σ_{i≠j} λ_B(y′_i) ≤ B − 1. By Lemma 3.8a Left wins R + Λ second, hence
R + (B − 1) and R + B second. The frontier position is B + R. If Right is to move, it cannot move in the stack B, so this is R + B second, a Left win.
If Left is to move, she plays B → B − 1 and wins R + (B − 1) second. The case σ = − is the mirror image with ρ_B. ∎

*Reading (the "value" of a loopy component). PROVED, from Theorem 3.8.* Under the criterion the D-result of the sum is the outcome of Σ y_i^B, so it is determined by the loopy-CGT class of each y_i^B (its equivalence class under
outcomes in all loopy contexts) and by the reserve data that certify the criterion. If y_i is a stopper, so is y_i^B (the chains are acyclic), and its class is Siegel's simplest form [S, ch. VI] (KNOWN, not re-derived here). For the reservoirs `on`, `off`, `dud`
opposite a threat that the threatening side can force, no B reproduces the D-result on the forced positions (Proposition 3.12); opposite a threat that cannot be forced (a suicide) the translation can
still be right although dominance fails (Theorem 3.8(c)).

**Corollary 3.8b (one loopy component plus short components). PROVED from Theorem 3.8.** Let S be a terminal-free component (stopper or not) with finite reserves at every reachable node, Λ(S) = max λ(y) < ∞ and P(S) = max ρ(y) < ∞
(for terminal-free S the reserves do not depend on B), and let K = (K_1, …, K_m) be short and pairwise safe (Definition 1.10). If B ≥ 1 + max(Λ(S), P(S)) + max(M_L(K), M_R(K)), the criterion holds, so the D-result of S ⊞ K is the outcome of S + Σ K_i^B
at every reachable position. *Proof.* All events are in K. For an event of sign + in K_j the rest is S together with the other K_i, and Λ(S) + Σ_{i≠j} Λ_B(K_i) ≤ Λ(S) + M_R(K) ≤ B − 1 by Theorem 3.8(a); σ = − is symmetric. ∎
It is the finite-reserve half of the "one stopper plus short components" case: S = over and S = under qualify (Proposition 3.9) and so does every stopper whose reserves are finite; `on` and `off` are not covered by the corollary as stated (ρ(on) = λ(off) = ∞) but satisfy Theorem 3.8 directly: S = on when K has no ⊖ event
(only the σ = + condition is needed, and Λ(on) = 0), S = off when it has no ⊕ event (the sign condition of Theorem 3.8 is what pairs the reservoir with the threats of the side it favours), with K pairwise safe and
B ≥ 1 + max(M_L(K), M_R(K)) (argued from the proof of Corollary 3.8b with the one-sided condition; unlike the finite-reserve statement, this extension has not been checked by an independent referee; tested on 1,810 random instances, 0 failures, COMPUTED-1). The other pairings are Theorem 3.4 and Proposition 3.12. Most random stoppers do not qualify: 9,488 of the 12,610 random stopper-plus-safe-short instances had an infinite reserve.

**Proposition 3.9 (reserves of the named games). PROVED.** (λ, ρ): on (0, ∞), off (∞, 0), over (0, 1), under (1, 0), dud (∞, ∞).

*Proof.* on: Right has no move, so Left wins second at once: λ = 0. Whatever Right's tokens, Left passes forever and Right runs out: Right never wins, ρ = ∞.
off is the mirror image. over: Right moves first (a pass or a token); Left plays ω → 0 and Right has no move: λ = 0. With no Right token Left moving first plays ω → 0
and wins; with one token Left's only move is ω → 0 (tokens are Right's), Right plays the token and Left is stuck: ρ = 1. under is the mirror image.
dud: Right can pass forever, so Left never forces a win; likewise Right: λ = ρ = ∞. ∎ (The same table was computed by two independently written solvers, B = 4: CHECKED-2. For over and under these are also Λ and P, the node 0 inside them having reserves (0, 0).)

**Proposition 3.9′ (reserves and Siegel's stops). PROVED from the two standard facts (R1) and (R2) below, which are KNOWN and were not re-derived here.**
Let y be a node of a finite terminal-free stopper. Its stops LS(y), RS(y) ∈ ℝ ∪ {±∞} are Siegel's [S, ch. VI] (KNOWN): if y equals a number x (that is, y − x is a second-player win: both players lose moving first) then LS(y) = RS(y) = x; otherwise LS(y) is the maximum of RS(y^L) over the Left options and RS(y) is the minimum of LS(y^R) over the Right options, with max ∅ = −∞ and min ∅ = +∞.
Write y + C for y with C Left tokens, as in the conventions above (C an integer ≥ 0). Two standard facts compare the right stop with the number −C:
- (R1) (KNOWN) If Left wins y + C moving second, then RS(y) ≥ −C.
- (R2) (KNOWN) If RS(y) > −C, then Left wins y + C moving second.

(R1) and (R2) say that RS(y) is the supremum of the numbers x for which Left wins y − x moving second, read at the integers x = −C: (R1) is the case x = −C, and (R2) is the fact that adding a positive number keeps a Left win second (the proof of Lemma 3.8a works for any two components; a finite number game may be replaced by an equal one inside a sum, which is KNOWN). The imported fact is therefore that the recursion above computes this supremum for a stopper (Siegel). It is not re-derived here. The data below test it.

Let u = −RS(y). Then:
- (a) λ(y) < ∞ iff RS(y) > −∞. If RS(y) = +∞, then λ(y) = 0.
- (b) If u is finite, then max(0, ⌈u⌉) ≤ λ(y) ≤ max(0, ⌊u⌋ + 1). So λ(y) = max(0, ⌈u⌉) unless u is an integer ≥ 0, and then λ(y) ∈ {u, u + 1}.
- (c) (mirror) Let v = LS(y). Then ρ(y) < ∞ iff LS(y) < +∞; if LS(y) = −∞ then ρ(y) = 0; and if v is finite, max(0, ⌈v⌉) ≤ ρ(y) ≤ max(0, ⌊v⌋ + 1).
- (d) The conjectured form "λ = ⌈−RS⌉ or one more" is true only after the clamp at 0 in (b). It fails exactly when RS(y) ≥ 2 is finite, because λ ≥ 0: the integer 2 = {1∣} has RS = 2 and λ = 0.
- (e) At an integer boundary the stops do not decide. For RS = LS = 0 all four pairs (λ, ρ) ∈ {0, 1}² occur: 0 gives (0, 0), over and ↑ give (0, 1), under and ↓ give (1, 0), * gives (1, 1). For u = m an integer ≥ 0, λ(y) = m iff Left wins y + m second.
- (f) For a terminal-free stopper S: all reserves are finite on reach(S) iff RS > −∞ and LS < +∞ at every node of reach(S). Then Λ(S) ≤ max(0, ⌊−m⌋ + 1) with m = min RS over reach(S) (Λ(S) = 0 if m = +∞), and P(S) ≤ max(0, ⌊M⌋ + 1) with M = max LS over reach(S) (P(S) = 0 if M = −∞). So the B of Corollary 3.8b can be read off the stops.

*Proof.* (a), (b). Let λ(y) = C < ∞. Left wins y + C second, so RS(y) ≥ −C by (R1), that is C ≥ u. Hence RS(y) > −∞, and since C is an integer ≥ 0, C ≥ max(0, ⌈u⌉).
Conversely let RS(y) > −∞. If RS(y) = +∞, then RS(y) > 0 and (R2) with C = 0 gives λ(y) = 0. If u is finite, put C = max(0, ⌊u⌋ + 1). Then C > u (if C = 0 then ⌊u⌋ ≤ −1, so u < 0), so RS(y) = −u > −C, and (R2) gives λ(y) ≤ C.
If u is not an integer, then ⌈u⌉ = ⌊u⌋ + 1 and the two bounds agree. If u is an integer < 0, both bounds are 0. If u is an integer ≥ 0, the bounds are u and u + 1.
(c) Swap the Left and Right options of y. The mirror game ȳ is a stopper, λ(ȳ) = ρ(y) because the rules are symmetric, and RS(ȳ) = −LS(y) because the recursion is symmetric and the number x goes to −x. Apply (a) and (b) to ȳ.
(d) If RS(y) ≥ 2 is finite, then ⌈−RS⌉ + 1 ≤ −1 < 0 ≤ λ. If RS(y) < 2 then u > −2: for ⌈u⌉ = −1 the set {−1, 0} contains λ = 0 (u < 0), and for ⌈u⌉ ≥ 0, (b) gives ⌈u⌉ ≤ λ ≤ ⌊u⌋ + 1 ≤ ⌈u⌉ + 1.
(e) The last sentence: the set of C with "Left wins y + C second" is upward closed (Lemma 3.8a), so λ(y) ≤ m iff Left wins y + m second, and λ(y) ≥ m by (b). The four pairs, by hand, with ↑ = {0 ∣ *} and * = {0 ∣ 0}. 0: (0, 0) is trivial. over and under: Proposition 3.9. *: in * + 0 Right moves to 0 and Left has no move, so λ ≥ 1; in * + 1 Right's only move leaves 0 + 1, Left plays the token and Right is stuck, so λ(*) = 1; ρ(*) = 1 by symmetry. ↑: in ↑ + 0 Right's only move is to *, Left answers * → 0 and Right is stuck, so λ(↑) = 0; with Left to move at ↑ she plays to 0 and wins, so ρ(↑) ≥ 1, and in ↑ − 1 her only move is to 0 − 1, after which Right moves and she is stuck, so ρ(↑) = 1. ↓ is the mirror image of ↑. The stops of all six games are 0 (KNOWN for the infinitesimals ↑, ↓, *; for over and under the recursion gives LS = RS(0) = 0 and RS = LS; also computed below).
(f) (a) and (c) at every node, and both bounds are monotone in RS(y) and LS(y); Λ(S) and P(S) are the maxima over reach(S). ∎

*Data.* Two C implementations (A: token DP and a profile against dyadic numbers on a 1/16 grid; B: a generic sum solver, explicit number games on a 1/32 grid, explicit token chains) agree on λ, ρ, LS, RS at every node of every graph tested, and the stops from Siegel's recursion agree with the supremum of the numbers x with Left winning y − x (moving first, second) in every case (0 mismatches). The corrected relation (b), (c) holds in all of them. Every rooted stopper with at most 4 nodes (3, 43, 4,281 and 2,169,427 isomorphism classes on 1 to 4 nodes, 2,173,754 in all): 0 violations; the literal form for λ fails in 1,213 of them (3 on 3 nodes, 1,210 on 4 nodes), exactly those with finite RS ≥ 2, and the mirror form for ρ fails in another 1,213, exactly those with LS ≤ −2 (2,426 classes in all). 105,000 random stoppers of 5 to 8 nodes (620,000 nodes): 0 violations of (b), (c); the literal form fails only for RS ≥ 2 (8,873 nodes for λ, 8,779 for ρ at LS ≤ −2). The named games: on (0, ∞), off (∞, 0), over (0, 1), under (1, 0), 0 (0, 0), * (1, 1), ↑ (0, 1), ↓ (1, 0), 1 (0, 1), 2 (0, 2), −1 (1, 0), 1/2 (0, 1), ±1 (2, 2), {on∣off} (∞, ∞), and the three-node stopper of the tempo-regime counterexample under "What fails" below (∞, ∞); stops are the values. A third C implementation and a Python one, written without reading the first two, reproduce: the class counts 3, 43, 4,281 (own labelled enumeration, root fixed, canonical under permutations of the other nodes) and 2,169,427 (own enumeration of all 2^32 labelled graphs on 4 nodes, 12,958,975 of them rooted stoppers), the 1,210 literal violations on 4 nodes, and all 48 signatures (λ, ρ, LS, RS) with identical counts; 0 violations of (b), (c) and 0 grid mismatches with the supremum characterisation on every node of every 4-node class (8,677,708 nodes); 0 violations on random stoppers of 4 to 8 nodes, with the literal form failing exactly when RS ≥ 2 or LS ≤ −2; a Python solver with a different data layout agreed on all 5,200 nodes of 1,100 random stoppers of 4 to 6 nodes. CHECKED-2. A further C checker and a further Python checker, written from the definitions only without reading the earlier code, reproduce the class counts 3, 43, 4,281 and 2,169,427 (12,958,975 labelled rooted stoppers on 4 nodes), the same 48 signatures with the same counts, the 1,210 literal violations of the λ form on 4 nodes, and 0 violations of (b), (c) at all 8,677,708 nodes of the 4-node classes. A grid of 1/16 with |x| ≤ 9 gives the same result as 1/8 with |x| ≤ 6 on every 4-node class, so the grid is not a cut-off. On 1,100,000 random stoppers of 5 to 8 nodes (7,000,000 nodes) there were 0 violations of (b), (c) and 0 mismatches between Siegel's recursion and the supremum characterisation; the literal form failed exactly when the finite stop was ≥ 2 (ρ: ≤ −2) at every node of every class of at most 4 nodes and in a random run of 100,000 six-node stoppers. The Python program (token DP for λ and ρ, naive fixpoint sweeps, exact fractions) agrees with the C program on every node of 2,100 random stoppers of 2 to 7 nodes (8,850 nodes), and an own Python count gives the class counts 3, 43, 4,281. (R1) and (R2) held at every node tested, the integers x = −C included; they are KNOWN and not proved here. The exhaustive search stops at 4 nodes: 5 nodes were not enumerated (the class counts grow by factors of 14, 100 and 507 from 1 to 4 nodes, so 5 nodes means billions of classes, an extrapolation).

**Proposition 3.10 (no draws beside a stopper). PROVED.** If all components are short except one stopper S, every play of ⊞ is finite and the D-result is W or L.
*Proof.* A move in a short coordinate descends in a finite acyclic graph, so a play contains finitely many of them; after the last, all moves are in S and the movers
alternate, an infinite alternating play of S, which a stopper does not have. ∎ For dud (a non-stopper) `G ⊞ dud` is a draw when G has no terminal, `on ⊞ off` is a draw,
and a random non-stopper beside random short components has a draw in 1,315 of 3,335 instances (stoppers: 0 draws in 7,932 instances, 116,954 states; COMPUTED-1; a second generator: 0 draws in 1,277 stopper instances and a draw in 320 of 1,223 non-stopper instances, so the draw rate depends on the generator).

**Theorem 3.11 (sandwich). PROVED.** Let K be any D-game (loopy allowed) and S a D-game none of whose options is a terminal of its own mover (no Left option ⊕, no Right
option ⊖; suicides are allowed, as for the deleted Z-moves of a frozen group; every terminal-free S qualifies, stopper or not). Then for every k, s and mover:

  (k, mover) ∈ W(K ⊞ off) ⇒ (k, s, mover) ∈ W(K ⊞ S) ⇒ (k, mover) ∈ W(K ⊞ on),
  (k, mover) ∈ L(K ⊞ on) ⇒ (k, s, mover) ∈ L(K ⊞ S) ⇒ (k, mover) ∈ L(K ⊞ off),

and W(K ⊞ off) = W(K ⊞ dud), L(K ⊞ on) = L(K ⊞ dud). Call P_L(K, mover) = "Left wins K ⊞ off" (Left can force a decisive event against a Right who may pass) and
P_R(K, mover) = "Right wins K ⊞ on". For short K these are the predicates Λ and Ρ of Theorem 3.4.

*Proof.* (1) Let σ be a stage-lowering Left strategy at (k, ω, mover) in K ⊞ off. In K ⊞ S Left keeps the virtual position (k, ω) in K ⊞ off. Off has no Left move, so σ prescribes
only K-moves and the terminal ⊕, which she plays for real. A real Right move in K is a virtual Right move; a real Right move in S is treated as the virtual pass ω → ω; a real
Right terminal is a suicide ⊕, or ⊖, which is not an option at a node of W_L. If Right has no real option it loses. The stage drops every round.
(2) Let σ be a stage-lowering Left strategy at (k, s, mover) in K ⊞ S. In K ⊞ on Left keeps a virtual S-position; when σ prescribes an S-move s̃ → s̃′ she passes ω → ω and updates s̃
(σ never prescribes a Left terminal in S, for S has none, nor a suicide). Right's real options are K-moves only, a subset of the virtual ones.
(3) Suppose (k, ω, L) enters W_L(K ⊞ dud) at stage n ≥ 1 through the Left pass to (k, ω, R). Then (k, ω, R) ∈ W_{L,n−1}, so all its options, Right's pass back to (k, ω, L) among them,
lie in W_{L,n−2}, and (k, ω, L) entered earlier: a contradiction. So by induction on the stage the Left pass is never needed, W_L(K ⊞ dud) ⊆ W_L(K ⊞ off), and the reverse inclusion
is clear. The L-statements are the mirror images. ∎

**Corollary 3.11a. PROVED** (immediate from Theorem 3.11). P_L ∩ P_R = ∅. On P_L the D-result of K ⊞ S is W for every such S and every s, on P_R it is L. So whatever Z is, if one side can force a decisive event
against a passing opponent, that side wins; Theorem 3.4 and Corollary 3.5 are the cases S = on, off, dud. For K short and S a stopper (no draws, Proposition 3.10), S can matter only
in the *tempo regime* T = ¬(P_L ∪ P_R): outside T the result does not depend on S. (The inclusions W(K ⊞ S) ⊆ ¬P_R and L(K ⊞ S) ⊆ ¬P_L hold everywhere and are Theorem 3.11 itself; they say nothing inside T.)

**Proposition 3.12 (where the translation is right for the pure reservoirs). PROVED.** Let K be short.
- K^B + on ∈ 𝓛, so the translation says W at both movers and is right at (K, mover) iff (K, mover) ∉ P_R (Theorem 3.4(b)); on P_L, where Left forces, D = W as well.
- K^B + off ∈ 𝓡, so the translation says L and is right iff ∉ P_L.
- K^B + dud is a draw (Left can pass forever, so Right never wins, and conversely), right iff ∉ P_L ∪ P_R (Theorem 3.4(a)).
So the translation is right exactly outside P_R for `on`, outside P_L for `off` and in the tempo regime T for `dud`; it is wrong exactly on the forced positions of the side that the reservoir
does not favour (of both sides for `dud`). Theorem 3.4, not Theorem 1.11, is the sum theorem for them. *Proof.* Theorem 3.3(a) and its mirror for the first two; for dud, Left can pass forever. ∎
(The reading "right in the tempo regime, wrong on the forced positions of the side the reservoir favours" is false for `on` and `off`. A check of 53,838 (K, mover, reservoir) cases with the statement as written: 0 violations, COMPUTED-1.)

**What fails. The named examples are CHECKED-2 at the root (two independently written solvers agree, B = 2, 5, 9 unless stated); the statistics are COMPUTED-1; results are (Left first, Right first).**
- *An infinite reserve opposite a threat that the threatening side can force kills every B.* `{⊕∣} ⊞ off`: D-result (W, W), CGT outcome (L, L) for B = 2, 5, 9. `{⊕∣} ⊞ dud`: D (W, W), CGT (D, D). `{∣⊖} ⊞ on`: D (L, L),
  CGT (W, W). The favourable pairs are right: `{⊕∣} ⊞ on` and `⊞ over` are (W, W) in both; `{∣⊖} ⊞ off`, `⊞ over`, `⊞ under` are (L, L) in both.
- *A threat that cannot be forced does not.* If the only event is a suicide (Left's own ⊖ in `{⊖∣}`, Right's own ⊕ in `{∣⊕}`), the other side never has to allow it and the translation can be right although
  dominance and the criterion of Theorem 3.8 fail: `{⊖∣} ⊞ on` D = CGT = (W, W); `{∣⊕} ⊞ off` D = CGT = (L, L); `{⊖∣} ⊞ dud` and `{∣⊕} ⊞ dud` D = CGT = (D, D) (B = 2, 5, 9). The reserve
  criterion is therefore not necessary for D = CGT (see also the last bullet).
- *Non-stoppers.* Theorem 3.7 holds verbatim, and so does Theorem 3.8 with finite reserves: S = {S, 0 ∣ S} (not a stopper, λ = 0 at both nodes) beside `{⊕∣}` is dominant and D = CGT = (W, W). What is lost is
  Proposition 3.10 (draws) and the compatibility of dud (λ = ρ = ∞) with a threat of either sign.
- *The tempo-regime guess is false for general stoppers (the guess is refuted).* "For K short and S a terminal-free stopper, outside P_L ∪ P_R the translation K^B + S gives the D-result."
  It fails in 60 of the 28,581 sampled tempo-regime states in which the criterion of Theorem 3.8 is violated (S = random stopper 39, short 7, arbitrary loopy 7, under 4, over 3; never for on, off, dud: 8,646 tempo-regime states;
  the failures with a short, over or under S come from a K whose own components violate the criterion), and in none of the 40,380 states (all regimes) in which the criterion holds. Smallest counterexample, 2 + 3 nodes, B = 3, 14, 40 alike: K = `{1 ∣ ⊖, 1}` with node 1 = 0 (Left's only move is to 0; Right may
  play ⊖, a Black win, or move to 0); S has nodes a, b, c with a: Left → c, Right → b, c; b: Right → a, b; c: Left → b, c (c is on-like, b off-like; S is a stopper).
  At (K, a), Left to move, K ⊞ off is lost and K ⊞ on is won for Left, so it is in T. The D-result is **L**: K → 0 lets Right play a → b and Left is stuck; a → c lets Right play ⊖.
  The translation says **W**: after a → c Right's ⊖ becomes −B and Left passes forever in c. (ρ_B(S) = ∞.) CHECKED-2 (two solvers for B = 1, 2, 3, 14, 40, and this hand argument).
  A second, independent counterexample (found by a second random search): K = `{⊕, 0 ∣ 0}` (nodes k and 0; Left may play ⊕ or move to 0, Right may only move to 0), S = `{0 ∣ off}` (nodes s, 0 and off, a stopper). At the
  root with Right to move K ⊞ on is (W, W) and K ⊞ off is (W, L), so Right-first is in T; the D-result is **W**, the translation gives **L**, for B = 1, 2, 5, 14. Hand check: Right's K → 0 loses to Left's S → 0 (Right is stuck);
  Right's S → off lets Left play ⊕ at once, a White win in the D-game; in the translation that ⊕ is the stack +B, Right passes forever in `off` and Left runs out of moves. CHECKED-2.
  Statistics (COMPUTED-1): a second, different generator does not reproduce the 60 of 28,581 exactly, but it reproduces the content: 1 failure in 6,882 tempo-regime states with the criterion violated and 0 in 3,594
  with it true.
- *The criterion is not necessary.* `{∣⊕, 0}` ⊞ `{⊖, 0 ∣ 0}` (each with a self-loop at its only node; the first is off-like with a Right suicide, the second dud-like with a Left suicide) is dominant at B = 5 and D = CGT = (D, D),
  although the criterion fails: λ_5 of the second component is exactly B = 5 (Left stops Right's passes only by her suicide to −B), and the criterion asks for ≤ B − 1 (22 cases of this kind among the 4,693 dominant loopy cases; a second solver confirms D = CGT = (D, D) for B = 3, 5, 7, dominance true, criterion false, λ_5 of the second component exactly 5; CHECKED-2).

**Computations (COMPUTED-1 for the experiments, CHECKED-2 where two independent solvers agree, as marked).** The first set of programs consists of a Python solver `dsum.py` with a test driver and a C solver `sumsolve.c`; a third solver was written separately from the definitions. Random components: short DAGs (≤ 4 or 5 nodes, ≤ 2 or 3 options per side, both signs of terminal options), random loopy components with terminals (≤ 3 nodes), on, off, over, under, dud, random stoppers (≤ 4 or 5 nodes); 2 or 3 components.
- *Solver cross-check:* Python (explicit reachable product, counter-based least fixed point) against `sumsolve.c` (dense product, naive iteration, its own translation) on the root tuple, both movers, D-result and CGT outcome:
  0 disagreements on 6,000 instances, and on 3,000 more with another seed; 1,169 have D ≠ CGT, 1,468 a draw. In a second mode the C program gives the D-result and the CGT outcome at *every* tuple of original nodes, and these are compared with the Python results at every reachable tuple, both movers: 47,896 states in two runs (the second with a richer generator), 0 disagreements. These all-states samples contain no instance with D ≠ CGT and no draw, so they test only the agreeing regime; the differing regime is covered by the root cross-checks (1,169 and 557 instances with D ≠ CGT) and by the third solver. *Third solver:* written from the definitions, it agrees with `dsum.py` on 1,500 random instances (2 or 3 components of up to 4 nodes, loopy or short, with terminals, B in {1, 2, 4, 6}):
  D-result and CGT outcome at every reachable tuple and both movers, 20,324 states, 0 disagreements, and dominance and the reserve criterion on all 1,500 instances: CHECKED-2. The dominance, reserve and regime statistics of the first set use the Python solver only (COMPUTED-1).
- *Theorems 3.7, 3.8:* 26,000 random instances, D = CGT compared at all reachable tuples and both movers. 4,693 non-vacuous loopy cases with dominance
  (4,671 with the criterion): 0 violations; criterion ⇒ dominance ⇒ equality, 0 violations; where dominance fails, D ≠ CGT in 6,898 + 1,115 instances (by accident equal in 2,123 + 667).
- *Theorem 3.8(a):* 5,537 pairwise safe (Definition 1.10) short instances with B = max(M_L(Y), M_R(Y)) + 1, 5,127 of them with events: the criterion, dominance and D = CGT at every reachable tuple hold in all, 0 failures.
- *Corollary 3.8b:* 3,122 instances (2,625 with events) with a random terminal-free stopper S of finite reserves (or over, under) beside 1-2 pairwise safe short components, B as in the corollary: the criterion holds and D = CGT at every reachable position in all, 0 failures (9,488 further instances skipped because S had an infinite reserve).
- *Proposition 3.12* (B = 14): 189,072 (K, mover, reservoir) checks, translation right exactly as stated: 0 violations.
- *Lemma 3.8a:* 5,682 checks, 0 violations.
- *Theorem 3.4 predicates:* 225,312 (position, mover, reservoir) checks, 0 violations. *"White wins G ⊞ over whenever White wins G moving second" (Proposition 4.6 of the source note):* 20,628 checks, 0 violations.
- *Theorem 3.11:* 15,000 instances, 142,798 states (K one or two components, short or loopy with terminals; S named, quiet short, stopper, quiet loopy, loopy with suicide-only terminals, 38,020
  states of the last kind): 0 violations of the four inclusions and of W(off) = W(dud), L(on) = L(dud).
- *Runs of the third solver (own generator; COMPUTED-1, all 0 violations).* Theorem 3.7 (dominance ⇒ D = CGT at every reachable tuple, both movers; criterion ⇒ dominance): 10,000 random instances (1,778 dominant, 1,646 with the criterion), and exhaustively all
  2,080 pairs of one-node components with options in {self-loop, ⊕, ⊖} (268 non-vacuous dominant, 49 dominant without the criterion), 2 × 3,000 one-node × random two-node, 1,200 random triples of one-node components. Theorem 3.8(a): 641 safe instances. Corollary 3.8b: 721 instances
  (591 with events). Lemma 3.8a: 1,600 checks. Theorem 3.11: 6,150 instances. Proposition 3.12: 53,838 checks. Proposition 3.10: 1,277 stopper instances, no draw.
- *Corollary 3.11a and the translation:* 102,883 states with (K, mover) ∈ P_L ∪ P_R, D-result = forced result in all of them; 40,380 states with the criterion true, D = CGT in all.

**Chess instances with a shuttle beside small contexts (COMPUTED-1, P model; the P-model oracle was run once, see the last-but-one bullet).** Z_onT1 = `Ka5 Pb4 Pc5 kc6 pb5` on cyl:7x6 is `on_D` (Proposition 3.2, §5.4); a pawn context on the e and f files is turned
into a D-game (positions = pawn configurations with e.p. as in `cylcgt`, decisive events = a passer, races by the "count" rule, as in `lemmas/common.py`), and the prediction is the solver's D-result of K ⊞ on_D, which is
Theorem 3.4(b) and, for the forced positions, Theorem 3.11. 18 contexts of 1-5 pawns (for each predicted class (W,W), (W,L), (L,L): the four smallest and two mid-size contexts found among 6,000 random placements, plus the P9 context `Pe2 pf3` as a control)
and 6 colour-reversed contexts with Z_offT1 = `Kc1 Pb2 ka2 pb3 pc2` (prediction from the `off_D` model). Oracle: the P-model solver `kp_p` (first promotion wins, real kings; e.p. on, promotion to a queen, cap 0), on all 48 positions.
- **21 of 24 agree**: 6/6 Z_off contexts; for Z_on, 6/6 in (W,W), 5/6 in (L,L), 4/6 in (W,L); P9 `Pe2 pf3` gives (W, L) as in P9.
- The 3 disagreements are (V1a)/(V2) failures on this narrow board (the seam makes the e-file 2-3 king steps from the a-file), not failures of the sum theory:
  (i) `Pe2 pe3 pf4`, predicted (L,L), P-model (W,L): White's king sortie Ka5-g4 (not a shuttle move) wins, so P is better for White than D, as Proposition 3.2 allows (r(G ⊞ Z) ≥ r(G ⊞ on_D));
  (ii) `Pe4 pf5`, predicted (W,L), P-model (W,W): after Black's capture f5xe4 the new Black passer is caught by Ka5-g4 (`Ka5 Pb4 Pc5 kc6 pb5 pe4 w` is a White win in P), so Black's decisive event is not a P-win ((V2));
  (iii) `Pe2 Pe3 pe4 pf3 pf4`, predicted (W,L), P-model (L,L): every White move loses; White's capture e3xf4 creates a passer that the D-model scores as a win, but Black's f3xe2 and e1=Q is a faster counter-promotion (a race, (V2)).
- **80 further random contexts** (1-4 pawns on e, f; same oracle): 64 of 80 agree. Over all 98 Z_on contexts, 79 agree; 13 differ in White's favour (the P-result is at least the prediction, as the inequality
  r(G ⊞ Z) ≥ r(G ⊞ on_D) of Proposition 3.2 allows: White's non-shuttle king moves); 5 are draws where the D-model predicts a decision (the stalemate mechanism, (V1b); `Pe4 pe5` is one: e4 covers d5 and pe5 is blocked, so Black has no legal move;
  the other four were not diagnosed); 1 is worse for White than predicted ((iii) above, a race, (V2)).
- **Status.** The P-model results are COMPUTED-1 (one run); nothing in the chess part is CHECKED-2. A second program recounted the counts above from the result files (24 base contexts, 21 agree; 80 random contexts, 64 agree; 79 of 98 Z_on contexts agree; 13 + 5 + 1 differences as listed), and the prediction side was re-derived by hand for `Pe2 pf3` ((W, L)), `Pe2 pe3` ((W, W)) and `Pe4 pf5` (predicted (W, L), P-model (W, W)); the `Pe4 pe5` stalemate explanation is right.
- **Chess values (kpsolve, cap 1) were not computed for these contexts.** So the new contexts are P-model results (the Z_on claims of §5.4 are "PROVED in P"; the chess claim needs (A_Q) at each position), and the only kpsolve (C) value for a context here is the one already recorded for P9.

**What loopy kings do to the convention.**
- **With a White shuttle (PROVED by Theorem 3.4(b)):** the components' values (numbers, infinitesimals, nimbers)
  are irrelevant except for Black's forcing threats. White cannot be zugzwanged, and Black loses as soon as its
  context tempo runs out.
- **With shuttles on both sides (PROVED in the D-model by Proposition 3.2′):** for a
  component with four combined king states, each side's shuttle an option and every other option a suicide, all tempo
  content disappears. A position in which neither side can force a decisive event against a passing opponent is a
  draw even where the convention predicts a clear winner, and a side wins iff it can (Theorem 3.4(a), through
  Proposition 3.2′). The chess bridge is Theorem 3.2‴. It needs, per group and context, that every non-shuttle Z-move
  is decisively punished; a win needs this only for the loser and only in the two states in which the winner's king
  stands still. The 7.3 group is **not** of this type: f7–f8=Q is a White Z-move that is no suicide (§5.3). A group of this type
  exists in P on the flat 7×6 board: Z_B of §5.7 has every non-shuttle move losing by force at all 8 roots (PROVED in §5.7; CHECKED-2 for the computations),
  and beside every context tested its P-result equals r(G ⊞ dud_D) (COMPUTED-1; 225 of 885 contexts untested; every context of at most 3 pawns on files e–g CHECKED-2, §5.7);
  CONJECTURE that this holds in every context. Z_B is **not** exactly two-shuttle in chess (CHECKED-2: 25 of
  the 26 deviations lose, Kc3–d2 from (c3, b5) draws: §5.7); open: chess contexts of Z_B, chess on the cylinder (Z_B, Z_C), a hand proof on the cylinder, other boards (§8,
  item 2). On the cylinder dud groups exist in P (§5.7, §8 item 2): Z_B and the passer-free
  group Z_C are exactly two-shuttle at their 8 roots on cyl:8×6 (Z_B also on cyl:7×6; CHECKED-2), Z_C is not exact beside every context,
  and G8a, G8b (no pawn move at all) are exactly two-shuttle in P (CHECKED-2) and in chess at cap 2 (COMPUTED-1). Z_A (§5.7) has one White break.

**Proposition 3.2′ (two shuttling kings are a dud). PROVED.** The D-model part is also checked by two brute-force implementations, on short and loopy G (see the checks below).

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
    positive fraction of random instances (COMPUTED-1). At G = 0 each of the eight deletions changes the result at all
    four states (two separately written programs agree, CHECKED-2).

*Proof.* Two lemmas, then the parts.

**Lemma A (p-morphism).** Let A, B be D-games and φ a map from the positions of A to those of B (identity on terminals)
such that, for every position u of A and each player s, (i) φ maps every s-option of u to an s-option of φ(u), and
(ii) every s-option of φ(u) is φ of some s-option of u. Then r_A(u, s) = r_B(φ(u), s) for all u, s. A and B may be loopy.
*Proof.* Let U_n^σ be the stage sets of Definition 1.2 (U_0 = ∅; (u, σ) enters at stage n+1 if some σ-option is a
σ-terminal or a position t with (t, σ̄) in U_n^σ; (u, σ̄) enters if every option is a σ-terminal or a t with (t, σ) in
U_n^σ, a position without options entering at stage 1). By induction on n, (u, s) is in U_n^σ(A) iff (φ(u), s) is in
U_n^σ(B). For s = σ, an option of u that is good at stage n maps by (i) to a good option of φ(u), and a good option
of φ(u) is φ of an option of u by (ii), which is good by induction. For s = σ̄, every option of φ(u) is φ of an option
of u by (ii), and every option t of u maps to an option of φ(u) by (i). The union over n is the least fixed point. ∎

**Lemma B (the winner of G ⊞ dud_D never passes).** Let (x, ω, σ) be in W^σ of G ⊞ dud_D, entering at stage n. Then
some option that makes it enter at stage n is a G-move (a σ-terminal of G or a position (x′, ω) with σ̄ to move and
stage ≤ n − 1). *Proof.* If the only such option were the pass, to (x, ω, σ̄) at stage m ≤ n − 1, then every option of
(x, ω, σ̄), the pass back included, has stage ≤ m − 1, so (x, ω, σ) would enter at stage ≤ m < n. ∎
This is the content of the proof of Theorem 3.4(a), "Left's winning moves are always G-moves".

*(a)* Let A = G ⊞ Z and A⁰ = G ⊞ Z⁰, where Z⁰ keeps only the four shuttle options at the four states.
- The stage sets of A and A⁰ coincide. A deleted option is a Left option ⊖ or a Right option ⊕. For the player to move
  it never makes a position enter (it is a terminal for the opponent). For the opponent it is a terminal that is always
  fine, so a position all of whose remaining options are fine, or that has none, enters at the same stage in A⁰ and A.
  (This is Lemma 1.7; its proof does not use shortness.)
- φ(x′, (a, b)) = (x′, ω) maps A⁰ onto G ⊞ dud_D. The Left options of (x′, (a, b)) are the terminals of G, the
  positions (x′^L, (a, b)) and (x′, (ā, b)); their images are the Left options of (x′, ω): the terminals of G, the
  positions (x′^L, ω) and (x′, ω), the pass. So (i) and (ii) hold for Left, and for Right with (x′, (a, b̄)). By
  Lemma A the results agree. ∎

*(b)* Delete White's further options (they can be added back as unreachable positions of the smaller game): (a) applies,
and by option monotonicity (Lemma 1.6) the larger game is at least as good for White, since Black's options are
unchanged. The second inequality is its mirror.

*(c)* Take σ = White. By induction on n, (x′, ω, s) in U_n^White(G ⊞ dud_D) implies (x′, (z, b), s) in U_n^White(G ⊞ Z)
for both b. For s = White, Lemma B gives a G-move making it enter, and the same move exists in G ⊞ Z. For s = Black,
every option of (x′, ω, Black) is good: a G-option, or the pass. At (x′, (z, b)) Black has the same G-options, the
shuttle to (x′, (z, b̄)) by (T2) (it corresponds to the pass), and otherwise only ⊕ options by (T4). All are good. ∎

*(Remark on e.p.)* The sum of Definition 1.3 leaves G alone under a Z-move,
and in chess an e.p. right expires under a king move. Model the flag as a coordinate of G that every Z-move resets, and
the pass of dud_D likewise. Lemma A goes through unchanged (φ forgets only the Z-state, and both games reset the flag at
corresponding moves). Lemma B needs one more line. The pass from (x, f, ω, σ) leads to (x, none, ω, σ̄), and the pass
back leads to the flag-free state (x, none, ω, σ), which is not (x, f, ω, σ) when the flag f is set. The flag belongs
to the side to move, so (x, f, σ) has all the options of (x, none, σ) and possibly an e.p. capture more. By option
monotonicity (Lemma 1.6) its stage is at most the stage of (x, none, σ). So (x, f, σ) enters at stage ≤ m < n: the same
contradiction. The conclusion of Lemma B also holds on all 4,579 pawn contexts of the checks below (155,400 winning nodes, 0 violations, by the third implementation; COMPUTED-1). The chess statements below use this reading.

**Remark 3.2′a (what it says about the conjecture).** A two-shuttle component realises dud_D, so the "shuttles on both
sides" bullet above is PROVED in the D-model for every component that satisfies (T1)–(T4). Whether a chess king group
does is a separate question, answered by the hypotheses of Theorem 3.2‴ below and, for a concrete group, by a search
(§5.7: Z_B in P).

**Lemma 3.2″ (four-state geometry; PROVED).** Let z ≠ z′ and w ≠ w′ be empty squares of F_Z, z, z′ adjacent and w, w′
adjacent, such that (K1) no Black Z-pawn attacks z or z′ and no White Z-pawn attacks w or w′, and (K2) the king distance
d(a, b) ≥ 2 for all four (a, b) (the kings never touch). Then, in every context (files at distance ≥ 2 from F_Z), with
the Z-pawns unmoved and the kings on {z, z′} and {w, w′}: neither king is in check, both shuttle moves are legal
(whatever the other king's square), and each side has a legal move, so nobody is stalemated.
*Proof.* A king is attacked only by an enemy pawn or the enemy king. By Lemma 2.2 no context pawn attacks a square of
F_Z and no pawn stands on a buffer file; the Z-pawns do not attack the four squares by (K1), and the kings do not attack
each other by (K2). So there is no check, and a shuttle move is legal: its target is empty, not attacked, and not
adjacent to the enemy king. Each side has its shuttle as a legal move. ∎

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

*Proof.* (a) By the sharp form of Theorem 1.14 it is enough to exhibit a White-certified set; take N.
- (S1): at a White node of N, Σ prescribes a G-move or a ⊕. By (V1a-ctx) the move is legal and leads to the prescribed
  D-position; a promotion wins in P by (V2-ctx). The rank is lowered.
- (S2): at a Black node of N every legal move is one of: a context move, a D-move by (V1a-ctx) to a position of N (a
  decisive event of G for White is closing by (V2-ctx); a promotion by Black would be a ⊖ option of a Black node of
  W^White, and there is none); Black's shuttle, a D-move (legal by Lemma 3.2″) whose rank is lower because the pass is
  an option of a Black node of W^White; any other move, closing by (Pun_Black).
- (S3): Black's shuttle is a legal move, so Black is not stalemated (Lemma 3.2″).
The sharp form gives a P-win. ∎(a)

(b) *D-win ⇒ P-win:* by (a) at every regular position, as (Pun) holds everywhere. *P-win ⇒ D-win:* by induction on the
stage of the P-win, a regular position y that is a P-win for σ has π(y) in W^σ. Suppose π(y) = (x, ω) with side s and
(x, ω, s) not in W^σ.
- s = σ: σ has a legal move that promotes or leads to a P-win of smaller stage. A promotion is a σ-terminal option of D
  by (V1a-ctx), which would put (x, ω, σ) in W^σ. A context move or a shuttle is a D-move to a regular y′ of smaller
  stage, and by induction π(y′) is in W^σ, again a contradiction. Any other move is decisively punished (Pun_σ), a P-win
  for σ̄, not for σ.
- s = σ̄: being a P-win, y has every legal move of σ̄ leading to a P-win for σ, and σ̄ is not stalemated. As (x, ω, σ̄)
  is not in W^σ and σ̄ has the pass, some option of it is neither a σ-terminal nor in W^σ. By (V1a-ctx) and Lemma 3.2″ it
  is realised by a legal move of σ̄ (a promotion, or a context or shuttle move to a regular y′ with π(y′) the option).
  By induction that move is not a P-win for σ. Contradiction.
So the P-win sets of both sides are π^{-1}(W^σ). ∎

**Which hypotheses hold.**
- (K1), (K2) are a finite test on Z alone, and by Lemma 3.2″ they give legality of both shuttles, no check and no
  stalemate in **every** context. (V1b) is therefore no hypothesis here: it is automatic, unlike in the one-sided bridge.
- A win needs no hypothesis on the winner's shuttle (Lemma B): only (Pun) for the loser, in the two states in which the
  winner's king stands still. Draws and the exact statement need (Pun) for both sides in all four states.
- (V1a-ctx), (V2-ctx) are per-context facts, as in the one-sided bridge.
- (Pun) is a per-group, per-context fact. It does not follow from the geometry of Z, and it fails when a counter-chance
  is faster than the punishment (Proposition 2.10(b)). It is the only gap of the bridge (the chess statement needs (A_Q)(X) as
  always, and (Pun) is stated for P): no theorem here gives it for a concrete group in all contexts. Theorem 2.7 and Proposition 2.10(a) give it in P for punishments of depth
  T = 1 under their side conditions.

**Checks of Proposition 3.2′ and Theorem 3.2‴ (data, not proofs).**
- *D-model, brute force, first implementation:* 400 random short D-games G (3 to 6
  positions, random options including ⊕, ⊖), each with random components Z of the kinds "exact (T1)–(T4) with extra
  suicides", "(T1), (T2), (T4) plus random further White options", the mirror, and (c)'s half-slice, solved by least fixed
  point on the explicit sum. (a): 44,208 of 44,208 instances agree. (b): 44,208 of 44,208 for each of the two
  inequalities. (c): 4,980 of 4,980. COMPUTED-1: one implementation; the statements are PROVED above.
- *D-model, brute force, a second, independently written implementation* (counter-based retrograde on the explicit sum): 400 random games of 2 to 6 positions, half of them loopy, 0 to 2 extra
  Z-positions. (a): 38,544 of 38,544 short and 37,200 of 37,200 loopy. (b): 75,744 of 75,744 for each inequality. (c):
  6,492 of 6,492 (White version) and 6,060 of 6,060 (Black version). 0 violations. COMPUTED-1 for the data; the
  statements are PROVED above, for loopy G as well.
- *Predictions for pawn-only contexts:* a least-fixed-point solver, the closed recursion of Theorem 3.4(a) (a pass resets the e.p. flag) and a third implementation (own pawn generator and own retrograde) agree on all 4,579 contexts of ≤ 2 + 2 pawns on files e–g
  of the flat 7×6 board: CHECKED-2. All three solve Theorem 3.4(a) on one pawn-game model, so this checks Theorem 3.4(a)
  with e.p. resets, not chess.
- *Chess, concrete groups:* §5.7. Counts are root instances of Theorem 3.2‴ under this convention: (Pun) for the
  loser holds on all regular positions reachable from the root and the D-result is W or L, for (a); both (Pun) hold, for
  (b). Z_A: (a) 208 instances, (b) 48 instances, 0 failures. Z_B: (a) 160 instances, (b) 56 instances, 0 failures.
  COMPUTED-1 in P.

**Literature (KNOWN).**
- Mäser (MGONC 2002) models *promotion* as on/off. That is a different use: there `on` is the new queen's
  inexhaustible tempo.
- Elkies (GONC 1996; arXiv 1999) lists loopy values (tis/tisn, over, on/off, dud) among chess positions.
- Siegel ("Coping with cycles", GONC 3, 2009) gives chess positions of value on and upon.
- Gafni (thesis 2011) computes loopy K+P vs K values on 3×3 and 3×4 boards.

None of these treats loopy kings inside sums with game-ending decisive events.
