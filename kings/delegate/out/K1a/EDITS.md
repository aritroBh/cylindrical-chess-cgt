### EDIT 1: R1 item 6, R2 item 8: the (A_Q) mention in the summary
<<<<<<< OLD
**The answer, in one paragraph.** The convention gives the chess result when four conditions hold, together
with the axiom (A_Q) that a won promotion race is a won game (Theorem 1.14):
=======
**The answer, in one paragraph.** The convention gives the chess result when four conditions hold, together
with the per-position hypothesis (A_Q)(X) that a won promotion race is a won game (Theorem 1.14; (A_Q) is
false as a general statement, so it is checked position by position by kpsolve; revised after review: R1 item
6, R2 item 8):
>>>>>>> NEW

### EDIT 2: R1 item 1, R2 items 1 and 2: the (V4) bullet in the summary
<<<<<<< OLD
- (V4) no two components carry threats of opposite sign, and BIG exceeds every tempo count.
=======
- (V4) no two components carry threats of opposite sign, and BIG exceeds every tempo count. The check is
  hereditary, on the components of every reachable position, and a threat is a move into a terminal by either
  player (revised after review: R1 item 1, R2 items 1 and 2).
>>>>>>> NEW

### EDIT 3: R1 item 1, R2 item 1: summary row T1.11
<<<<<<< OLD
| T1.11 | Sums: o(S) = decisive-event outcome under first-event dominance; sufficient: no opposite-sign threats in different components, and B > every tempo count | PROVED |
=======
| T1.11 | Sums: o(S) = decisive-event outcome under first-event dominance; sufficient: no opposite-sign threats in different components (a threat is a move into a terminal by either player), and B > every tempo count. (c) is the re-splitting version | PROVED (a); (b) and (c) PROVED after repair |
>>>>>>> NEW

### EDIT 4: R1 item 2, R2 item 3: summary row P1.13
<<<<<<< OLD
| P1.13 | B must exceed every tempo count: with n tempi against a threat, the BIG outcome is right iff n ≤ B | PROVED |
=======
| P1.13 | B must exceed every tempo count: with n tempi against the threat { \| ⊖}, the BIG outcome is right iff n ≤ B | PROVED after repair |
>>>>>>> NEW

### EDIT 5: R2 item 8: summary row T1.14
<<<<<<< OLD
| T1.14 | Validity: (V1)–(V3) give P = D (no draws), (V4) gives o(S) = P, and (A_Q) gives C = P | PROVED (C part modulo A_Q) |
=======
| T1.14 | Validity: (V1)–(V3) give P = D (no draws), (V4) gives o(S) = P, and (A_Q)(X) gives C = P | PROVED (the C part is the per-position hypothesis (A_Q)(X)) |
>>>>>>> NEW

### EDIT 6: R2 item 4: summary row T2.4
<<<<<<< OLD
| T2.4 | Freeze theorem: if Z-moves are punished at every position where the mover is losing, then G + Z has the result of G | PROVED |
=======
| T2.4 | Freeze theorem: if Z-moves are punished at every position where the mover is losing, then G + Z has the result of G, for a G scored under normal play (no draws) | PROVED after repair |
>>>>>>> NEW

### EDIT 7: R2 items 2 and 10: Definition 1.5, the D-terminal and the identification of S(X)
<<<<<<< OLD
- **D(X), the decisive-event model.** A D-game. Its positions are the positions before the first decisive
  event. Its terminals are the decisive events:
  - a passer appears (as in `cylcgt`), with races scored by a race rule;
  - a punished move in the king group (§2).
- **S(X), the BIG convention.** The CGT game D(X)^B, with B = BIG and the components summed. This is
  `cylcgt.pawns.value`.
=======
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
>>>>>>> NEW

### EDIT 8: R2 item 2: the bridge diagram after Definition 1.5
<<<<<<< OLD
S  --Thm 1.11 (V4)-->  D  --Thm 1.14 (V1-V3)-->  P  --(A_Q)-->  C
=======
S  --Thm 1.11(c) (V4)-->  D  --Thm 1.14 (V1-V3)-->  P  --(A_Q)(X)-->  C
>>>>>>> NEW

### EDIT 9: R1 item 11: the notation used in section 6 (o, W(X), S(X), HSS)
<<<<<<< OLD
The models are connected by bridges, each with its own hypotheses:
=======
The models are connected by bridges, each with its own hypotheses:

*Notation.* o(G) is the outcome class of a CGT game G (𝓛, 𝓡, 𝓝, 𝓟); W(X) is the whole-board convention game
of a pawn position X, in which the first passer ends the game (`notes/lemmas.md`); S(X) is the BIG value of
§1.5; and HSS, hereditary sum-safety, is the hypothesis (HSS) of Theorem 1.11(c). (Revised after review:
R1 item 11: §6 used o(W(X)) and "hereditarily sum-safe" without defining them.)
>>>>>>> NEW

### EDIT 10: R1 item 6, R2 item 8: the axiom (A_Q) is false as a general statement
<<<<<<< OLD
**Axiom (A_Q) (CONJECTURE, checked per position).** If X is a P-win for σ, then X is a C-win for σ.
- *Evidence for:* the cylinder KQK tables agree in two independent solvers ([RESULTS.md](../../RESULTS.md) §2:
  KQK is 100% won on the 8×8 cylinder).
- *Evidence against, in general:* L4.4 of `notes/lemmas.md` is a promotion race lost to a promotion with check.
- *Settled by:* kpsolve with `--cap 1` computes C exactly whenever its bounds agree (A = B).
=======
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
>>>>>>> NEW

### EDIT 11: R2 item 2: the remark after Theorem 1.9
<<<<<<< OLD
In one component the convention cannot go wrong: after the first ±B nothing else happens. Trouble needs at
least two components (compare L2.3 of `notes/lemmas.md`).
=======
In one component of the D-model the convention cannot go wrong: after the first ±B nothing else happens.
Trouble needs at least two components (compare L2.3 of `notes/lemmas.md`). That is *not* true of the
re-splitting model S of §1.5 (revised after review: R2 item 2): there a single component can still fail, because
a passer in one sub-part does not end its sibling, so trouble needs a later split, not two components. Example:
flat 7×6, e.p. on, count rule, `W: b2 d3 f2 / B: c4 c5 e5 g5` is one component at the root, yet o(S) = 𝓝 while
the decisive-event result is 𝓡 (COMPUTED-1, `lemmas/common.py`).
>>>>>>> NEW

### EDIT 12: R2 item 9: Definition 1.10, the tempo counts of a sum
<<<<<<< OLD
**Definition 1.10 (tempo counts, threats, dominance).** Let Y = (y₁, …, y_k) be a position of a sum of short
D-games.
- **Tempo counts.** M_L(y) is the largest number of Left moves in any sequence of moves from y (moves by
  both sides, in any order, not necessarily alternating), counting a final move into a terminal. M_R(y) is
  defined the same way for Right. Both are monotone: M(y′) ≤ M(y) whenever y′ is reachable from y.
=======
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
>>>>>>> NEW

### EDIT 13: R1 item 1, R2 items 1 and 9: Definition 1.10, the threat set τ
<<<<<<< OLD
  - In the pawn game every White move advances a White pawn by at least one rank, so
    M_W ≤ Σ_white pawns (H − rank) ≤ (H − 2)p for p legal White pawns. That is ≤ 6p ≤ 48 on 8 ranks.
- **Threats.** τ(y) ⊆ {+, −} contains + iff some position reachable from y without passing a terminal has a
  Left option ⊕. It contains − likewise for ⊖. Like M, τ is monotone.
=======
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
>>>>>>> NEW

### EDIT 14: R1 item 1, R2 item 1: Theorem 1.11, statement of (b)
<<<<<<< OLD
**Theorem 1.11 (sums). PROVED.**
- **(a)** If Y is first-event dominant for B, then the outcome class of Σ y_i^B equals the D-result pair of
  ⊞ y_i.
- **(b)** Y is first-event dominant for B if both of the following hold:
  - *pairwise safety:* no reachable Y′ has two different coordinates with + ∈ τ(y′_i) and − ∈ τ(y′_j);
  - *the bound:* B > max(M_L(Y), M_R(Y)).
=======
**Theorem 1.11 (sums). PROVED for (a); (b) PROVED after repair (revised after review: R1 item 1, R2 item
1); (c) PROVED after repair (R2 item 2).**
- **(a)** If Y is first-event dominant for B, then the outcome class of Σ y_i^B equals the D-result pair of
  ⊞ y_i.
- **(b)** Y is first-event dominant for B if both of the following hold:
  - *pairwise safety:* no reachable Y′ has two different coordinates with + ∈ τ(y′_i) and − ∈ τ(y′_j), with
    the τ of Definition 1.10 (an option to ⊕ or ⊖ counts whoever makes it);
  - *the bound:* B > max(M_L(Y), M_R(Y)).
>>>>>>> NEW

### EDIT 15: R1 item 1, R2 item 1: Theorem 1.11, repaired proof of (b)
<<<<<<< OLD
- **(b)** Take σ = ⊕; the case σ = ⊖ is symmetric.
  - In the frontier position B + Σ_{i≠j} (y′_i)^B, coordinate j had a + threat. By pairwise safety and
    monotonicity of τ, no other coordinate can ever reach ⊖.
  - Left's strategy is to move in a positive integer summand every turn: B, or any +B frozen later.
  - Right cannot move in a positive integer. Its moves are all moves in the rest, at most M_R(rest) ≤ M_R(Y)
    of them, and a Right move into a terminal can only create another +B.
  - Left needs at most M_R(Y) + 1 moves and has at least B ≥ M_R(Y) + 1 available. So Right runs out of
    moves first and loses, whoever started. ∎
=======
- **(b)** Take σ = ⊕; the case σ = ⊖ is symmetric.
  - Let Y′ be reachable from Y without passing a terminal, and let y′_j → ⊕ be the option, made by either
    player. Since the option exists, + ∈ τ(y′_j) (Definition 1.10, corrected: an option counts whoever makes
    it). By pairwise safety no other coordinate has − ∈ τ(y′_i); by monotonicity of τ no other coordinate can
    ever reach ⊖, so no option of the sum Σ_{i≠j}(y′_i)^B is −B. This is the step that failed for the earlier
    τ, which was blind to a ⊕ entered by Right (revised after review: R1 item 1, R2 item 1).
  - The frontier position is B + Σ_{i≠j}(y′_i)^B, and the positive integer B has canonical form {B−1 | } (a
    Left-only stack of B moves, [WW] ch. 2), so Right has no move in it.
  - Left's strategy: on every turn, play in a positive integer summand (the B created by the event, or a +B
    created later), and never in a component.
  - Right's moves are all moves in the components, and there are at most M_R(Y) of them: the moves in one
    coordinate form a sequence of moves in that coordinate, so the total is at most Σ_{i≠j} M_R(y′_i) ≤ M_R(Y)
    (M is monotone, and for a sum M is the sum over the coordinates). A Right move into a terminal can only
    create another +B, because −B is unreachable.
  - Left needs at most M_R(Y) moves (one for each Right move, and none after Right has run out) and the first
    stack has B ≥ M_R(Y) + 1 > M_R(Y) moves, so Left always has a move while Right still has one; the stack
    also never reaches 0, whose canonical form {−1 | 1} would give Right a move. Right runs out of moves
    first and loses, whoever started. ∎
>>>>>>> NEW

### EDIT 16: R2 item 2: the remark after Theorem 1.11, and the new Theorem 1.11(c)
<<<<<<< OLD
This is L2.1 of `notes/lemmas.md`, restated for abstract D-games. The test "hereditarily sum-safe" there is
pairwise safety.
=======
**(c) The re-splitting version. PROVED after repair (R2 item 2).** Let X be a pawn position, let S(X) be its
BIG value computed with re-splitting (§1.5), and let D(X) be the decisive-event game of X, in which the
position is split into its components at every node, a move is a move in one component, and the first decisive
event ends the play. Suppose:
- **(HSS)** at every position Y reachable from X before the first decisive event, the components of Y are
  pairwise safe (Definition 1.10, corrected τ: an option to ⊕ or ⊖ counts whoever makes it); and
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
  component, and the opponent has at most M_{−σ}(Y) moves in all; σ needs at most M_{−σ}(Y) moves and the
  first stack has B ≥ M_{−σ}(Y) + 1 > that many, so the opponent runs out of moves first (the stack never
  reaches 0, whose canonical form {−1 | 1} would let the opponent move).
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

The remark that followed Theorem 1.11 is corrected here (revised after review: R1 item 1, R2 items 1 and 2).
Theorem 1.11(b) is the fixed-sum version of L2.1: its coordinates are the components of the root and never
split. The re-splitting version is (c) above, and the test "hereditarily sum-safe" of `notes/lemmas.md` is
(HSS), not pairwise safety at the root: it re-checks the re-split components at every reachable position, and it
uses the either-player τ.
>>>>>>> NEW

### EDIT 17: R1 item 2, R2 item 3: Proposition 1.13, statement
<<<<<<< OLD
**Proposition 1.13 (BIG must exceed every tempo count; sharp). PROVED.** Let A′ = {∅ | ⊖} be a Black threat
and R_n be n consecutive one-shot White moves with no terminals (the integer n).
- **In chess semantics,** A′ ⊞ R_n is 𝓡 for every n: White can only spend tempi, and Black plays ⊖ when on
  move.
- **In the BIG translation,** {0 | −B} + n has three regimes:
  - 𝓡 if n ≤ B;
  - 𝓟 if n = B + 1;
  - 𝓛 if n ≥ B + 2.
=======
**Proposition 1.13 (BIG must exceed every tempo count; sharp). PROVED after repair (R1 item 2, R2 item 3).**
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
  (COMPUTED-1, `cylcgt.cgt`, B = 4: N, N, N, N, N, L, L, L for n = 0..7). The earlier version of this
  proposition mixed the two readings, and with them the claim was false as stated (revised after review: R1
  item 2, R2 item 3).
>>>>>>> NEW

### EDIT 18: R1 item 2, R2 item 3: Proposition 1.13, proof
<<<<<<< OLD
*Proof of the BIG part.*
- Right moving first goes to n − B. Left, to move, wins iff n − B ≥ 1.
- Left moving first goes to n − 1 + {0 | −B}. Right answers n − 1 − B. Left, to move, wins iff
  n − 1 − B ≥ 1. ∎
=======
*Proof of the BIG part.* { | −B} + n is the integer n − B − 1, and the outcome class of an integer m is 𝓛 if
m ≥ 1, 𝓟 if m = 0 and 𝓡 if m ≤ −1.
- Right moving first goes to n − B. Left, to move, wins iff n − B ≥ 1.
- Left moving first goes to n − 1 + { | −B}. Right answers n − 1 − B. Left, to move, wins iff
  n − 1 − B ≥ 1. ∎
>>>>>>> NEW

### EDIT 19: R1 item 2: Theorem 3.3(b)
<<<<<<< OLD
- **(b)** In chess semantics, {∅ | ⊖} ⊞ on_D is (L, L): Black plays ⊖ when on move, and White can only pass.
=======
- **(b)** In chess semantics, { | ⊖} ⊞ on_D is (L, L): Black plays ⊖ when on move, and White can only pass.
  (With the other reading of ∅, A′ = {∅ | ⊖}, the pair is (W, L) in the D-model: White plays A′ → ∅ and
  leaves Black with no move at all, which the D-model scores as a loss for Black and chess as a stalemate. The
  statement above uses the same A′ = { | ⊖} as Proposition 1.13; revised after review: R1 item 2.)
>>>>>>> NEW

### EDIT 20: R2 items 2 and 5: Theorem 1.14, the hypothesis (V4)
<<<<<<< OLD
- **(V3) frozen Z.** Every legal move inside Z, by either side, is a decisive event for the opponent: a
  suicide.
=======
- **(V3) frozen Z.** Every legal move inside Z, by either side, is a decisive event for the opponent: a
  suicide.
- **(V4) hereditary sum-safety.** At every position Y reachable from X before the first decisive event:
  - the pawn components of Y, re-split as the files split (an empty file stays empty, so a component may split
    into two), with the king group Z deleted, are pairwise safe: no two different components carry + ∈ τ and
    − ∈ τ, where τ counts options to ⊕ or ⊖ by **either** player (Definition 1.10);
  - BIG exceeds every tempo count of Y.
>>>>>>> NEW

### EDIT 21: R2 items 2, 5 and 8: Theorem 1.14, conclusions (ii) and (iii)
<<<<<<< OLD
- **(ii)** If (V4) X is first-event dominant for BIG (sufficient: pairwise safety and BIG > every tempo
  count), then the outcome class of S(X) equals P(X).
- **(iii)** Under (A_Q), C(X) = P(X).
=======
- **(ii)** If (V4) holds, the outcome class of S(X) — the BIG value of the pawn components, with the king
  group Z deleted — equals the outcome class of the D-result pair of P(X).
- **(iii)** Under (A_Q)(X) (the per-position hypothesis of §1.2, checked by kpsolve), C(X) = P(X). This is now
  a tautology: (A_Q)(X) says exactly this (revised after review: R2 item 8).
>>>>>>> NEW

### EDIT 22: R2 items 2 and 5: Theorem 1.14, proof of (ii) and (iii)
<<<<<<< OLD
- **(ii)** Theorem 1.11(a).
- **(iii)** Definition of (A_Q). ∎
=======
- **(ii)** By (i), the D-result pair of X is the D-result pair of D(X), and re-splitting does not change
  that pair (it re-groups the same positions and options). By Theorem 1.11(c), with (V4) supplying (HSS) and
  the bound, the outcome class of S(X) is the outcome class of that D-result pair.
- **(iii)** Definition of (A_Q)(X). ∎
>>>>>>> NEW

### EDIT 23: R2 item 6: Theorem 1.14, sharp form
<<<<<<< OLD
**Sharp form (PROVED by the same proof).**
- (V2) and (V3) are needed only for terminals reached under *one* D-winning strategy of the D-winner.
- (V1a) splits into two halves:
  - the winner's prescribed D-moves must be legal chess moves;
  - every legal chess move of the loser must be a D-option.

  The winner may have extra legal moves (Lemma 1.6).
=======
**Sharp form (PROVED after repair: R2 item 6).**
- (V2) is needed only for the terminals reached under *one* D-winning strategy of the D-winner.
- (V3) is needed in the stronger form: at every loser-to-move node of that strategy, **every** legal Z-move of
  the loser is a P-loss for the loser. The earlier wording ("needed only for terminals") was false as stated: a
  loser's Z-move that is not punished is not a terminal, and then the Lemma 1.7 reduction and the shortness of
  D both fail.
- (V1a) splits into two halves:
  - the winner's prescribed D-moves must be legal chess moves;
  - every legal chess move of the loser must be a D-option.

  The winner may have extra legal moves (Lemma 1.6).
- The conclusion of the sharp form is the result of the strategy itself, not a normal-play result: the D-winner
  σ wins P(X) by that strategy. The claim "the result is the normal-play result of G₁ ⊞ … ⊞ G_k (Z deleted)"
  belongs to (i), not to the sharp form.
>>>>>>> NEW

### EDIT 24: R2 item 9: the tempo bound quoted after Proposition 1.13
<<<<<<< OLD
- Left moving first goes to −B. Right, to move, moves to −(B − 1), and Left then has no move in a
  non-positive integer and loses.
- Right moving first loses by symmetry.
=======
So "BIG dominates" means exactly that BIG exceeds the largest tempo count either side can bring against a
threat. With BIG = 256 and pawns only this holds as long as p ≤ 42, since M ≤ 6p (and M ≤ 48 on 8 ranks when
p ≤ 8). With a shuttling king the tempo count is infinite, and no BIG works (§3) (revised after review: R2
item 9).
>>>>>>> NEW

### EDIT 25: R2 items 2, 5 and 8: the label of Theorem 1.14
<<<<<<< OLD
**Theorem 1.14 (validity of the convention). PROVED.** Assume:
=======
**Theorem 1.14 (validity of the convention). PROVED for (i); (ii) and (iii) PROVED after repair (revised
after review: R2 items 2, 5 and 8).** Assume:
>>>>>>> NEW

### EDIT 26: R1 item 4, R2 item 7: the sentence above the table 'each hypothesis is needed'
<<<<<<< OLD
**Why "exact" does not mean "iff".** (V1)–(V4) are sufficient, and none can be dropped (table below). But no
condition on local data can be *necessary*: the convention is sometimes right by accident.
=======
**Why "exact" does not mean "iff".** (V1)–(V4) are sufficient, and none can be dropped, except that for
(V1a) this is a CONJECTURE (table below). But no condition on local data can be *necessary*: the convention is
sometimes right by accident.
>>>>>>> NEW

### EDIT 27: R1 item 4, R2 item 7: the table 'each hypothesis is needed', rows (V1b) and (V1a)
<<<<<<< OLD
**Each hypothesis is needed.** Each can fail and change the result.

| Hypothesis | Counterexample (where in this note or the project) |
|---|---|
| (V1b) no stalemate | §5.4: the only suicide square is covered, and the position is a draw instead of a win (PROVED) |
| (V1a) non-interaction | King sorties that reach the component: 41 of 449 tablebase king moves draw and 7 win (`engine/suite/`, RESULTS §1) |
=======
**Each hypothesis is needed — except that for (V1a) this is a CONJECTURE (revised after review: R1 item 4,
R2 item 7).** Each can fail and change the result.

| Hypothesis | Counterexample (where in this note or the project) |
|---|---|
| (V1b) no stalemate | §5.4: the only suicide square is covered, and the position is a draw instead of a win (PROVED). The isolated failure needs (V3) to hold, so use the frozen model, where (V3) holds by fiat: `--frozen` gives `Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5` as (D, D), with every king move L, while the convention reads Z as 0 and the context as +1, i.e. (W, W) (COMPUTED-1, `kings/kpsolve --frozen`). With real kings the same position also violates (V3): Ka6 and Kg4–g6 are legal Z-moves that are not suicides |
| (V1a) non-interaction | No isolated counterexample is known: the king sorties that reach the component (41 of 449 tablebase king moves draw and 7 win, `engine/suite/`, RESULTS §1) are *unpunished Z-moves*, i.e. (V2)/(V3) failures, not (V1a) failures. That (V1a) is needed at all is therefore a **CONJECTURE** (revised after review: R1 item 4, R2 item 7) |
>>>>>>> NEW

### EDIT 28: R2 item 4: Theorem 2.4, statement
<<<<<<< OLD
**Theorem 2.4 (freeze theorem). PROVED.** Let G be a short game, either a D-game or the P-game of the
context, and let Z be a king group, possibly loopy. Assume Z's state changes only through Z-moves.
- **(a)** Suppose every Z-move, at every state and in every reachable context, leads to a position won by the
  opponent of the mover. Then r(G ⊞ Z) = r(G) at every reachable (Y, s).
- **(b)** It is enough that this holds at the positions (Y, s) reached under some winning strategy of the
  G-winner σ at which the loser σ̄ is to move.

In chess, assume also (V1b): the side to move always has a legal move.
=======
**Theorem 2.4 (freeze theorem). PROVED after repair (R2 item 4).** Let G be a short game scored under normal
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

*The P-game of the context is **not** covered, and the earlier version of this theorem was false for it
(revised after review: R2 item 4).* The P-model keeps stalemate as a draw, so "G has no draws" fails there and
the step "since G has no draws the results agree" was unjustified. Counterexample: cyl:7×6,
`Ka4 Pb3 Pe3 kc3 pb4 pe4` (Z_T + H0). The context G = {Pe3, pe4} has no move for either side, so it is (D, D)
under P; `kpsolve --frozen` gives (L, W), and there the hypothesis of (a) holds by fiat (king moves lose and
the Z-pawns have no moves); with real kings, White to move is L (exact) (COMPUTED-1, `kings/kpsolve`).
>>>>>>> NEW

### EDIT 29: R2 item 4: the proof of Theorem 2.4(c)
<<<<<<< OLD
- So the G-winner wins G ⊞ Z, and since G has no draws the results agree. (a) is a special case. ∎
=======
- So the G-winner wins G ⊞ Z, and since G has no draws the results agree. (a) is a special case. ∎

*Proof of (c).* σ plays its strategy of G, read in the sum, and never moves in Z, so Z stays in its initial
state. Whenever σ̄ moves in G, σ answers as in G. Whenever σ̄ moves in Z, σ wins by the hypothesis, since that
Z-move is decisively punished. The G-play is finite, since G is short. If σ̄ never moves in Z, the play is a
line of G under σ's strategy: it ends in a σ-win, or in a draw of G, so σ does not lose. If σ̄ does move in Z, σ
wins. ∎
>>>>>>> NEW

## STATUS ROWS

| result | final label | one-line note with review item |
|---|---|---|
| Def 1.5, S(X) | FALSE as originally stated → S(X) is the re-splitting BIG value (`cylcgt.pawns.value`), not D(X)^B; corrected | R2 item 2: cylcgt re-splits at every node, so one component can still fail |
| Def 1.5, the Z-terminal | PROVED (wording corrected): under (V3) every move inside Z is the Z-terminal, so Z is deleted by Lemma 1.7 | R2 item 10 |
| (A_Q), §1.2 | FALSE as a general statement → per-position hypothesis (A_Q)(X), checked by kpsolve; no longer a conjecture | R1 item 6, R2 item 8: `Ke2 Pb5 ka5 w` (cyl:7x6) and `Kd1 Pb3 ka3 w` (flat:4x4) are P-wins and chess draws |
| T1.9 | PROVED; the remark after it is corrected | R2 item 2: the remark was false for cylcgt, which re-splits components |
| Def 1.10, τ | PROVED after repair: τ counts options to ⊕/⊖ by **either** player (the suicide-blind τ was the fatal gap) | R1 item 1, R2 item 1 |
| Def 1.10, tempo counts | PROVED (minor wording repaired: M of a sum is the sum over the coordinates; the bound is ≤ 6p, so BIG needs p ≤ 42, and a final Z-move adds 1) | R2 item 9 |
| T1.11(a) | PROVED | R2: sound |
| T1.11(b) | FALSE as originally stated → PROVED after repair: with the corrected τ, pairwise safety and B > every tempo count give first-event dominance | R1 item 1, R2 item 1 |
| T1.11(c) | PROVED after repair (new): the hereditary, re-splitting version, with the full proof (L2.1 of `notes/lemmas.md` in D-game language) | R2 item 2 |
| P1.12 | PROVED | R2: sound under either reading of ∅ (the BIG part {B \| 0} + {0 \| −B} = 0 checked) |
| P1.13 | FALSE as originally stated → A′ = { \| ⊖}, translation −B−1, regimes 𝓡 / 𝓟 / 𝓛; the {∅ \| ⊖} variant is given too | R1 item 2, R2 item 3 |
| T1.14(i) | PROVED | R2: sound |
| T1.14(ii) | PROVED after repair: (V4) is hereditary, on the re-split components, Z deleted, with the corrected τ; (ii) then follows from (i) and T1.11(c) | R2 items 2 and 5 |
| T1.14(iii) | PROVED, but a tautology: (A_Q) is now the per-position hypothesis (A_Q)(X) | R2 item 8 |
| T1.14, sharp form | FALSE as originally stated → PROVED after repair: every legal Z-move of the loser at its turns must be a P-loss; the conclusion is the strategy's result, not a normal-play result | R2 item 6 |
| §1.5 "each hypothesis is needed", (V1b) row | PROVED (corrected): the isolated witness is the frozen model; with real kings P1a also violates (V3) | R2 item 7 |
| §1.5 "each hypothesis is needed", (V1a) row | CONJECTURE: the king sorties are (V2)/(V3) failures, so no (V1a) counterexample is given and "needed" is unproved for (V1a) | R1 item 4, R2 item 7 |
| T2.4 | FALSE as originally stated (the "P-game of the context" option) → PROVED after repair: G under normal play (no draws), plus the strategy-transfer form (c) for games with draws | R2 item 4: `Ka4 Pb3 Pe3 kc3 pb4 pe4` is (D, D) in P and L in chess |
| T3.3(b) | PROVED after repair: { \| ⊖} ⊞ on_D is (L, L); with {∅ \| ⊖} the pair is (W, L) in the D-model | R1 item 2 |
