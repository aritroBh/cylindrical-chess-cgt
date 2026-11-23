# EDITS for kings/theory/LOOPY.md after K51 and K52 (integrator, 2026-11-23)

Apply with `kings/delegate/apply_edits.py`. Every OLD block occurs exactly once in LOOPY.md as of
2026-11-23 (md5 c5a83e4f7c43b521fc36568f862f8b22, 4010 lines). No edit touches Theorem 2.7 or its proof.
Evidence: `findings.txt`, `verify.py` / `verify.out`, `witness_settings.py` / `witness_settings.out`,
`flagfree_probe.py` in this directory.

### EDIT 1 status row T1.11(c)
<<<<<<< OLD
Without (E): OPEN (no counterexample in a small search, COMPUTED-1). The frontier step's inheritance of threats by re-split components is now proved | R2 item 2; T30 audit: a move count corrected; s12a referee |
=======
Without (E): FALSE (revised after K52, 2026-11-23; was OPEN): flat 5×7 after a2–a4, `W a4 b3 e2 / B a5 b4 e4` with Black's right on a3 is passer-free, (HSS) and (B) hold, o(S) = 𝓡 and the D-result pair is 𝓝 (PROVED by hand; COMPUTED-1 under both passed tests and all three race rules); whether (E) can be dropped at roots without a right is OPEN. GAP → PROVED after repair (revised after K52, 2026-11-23): the frontier step charged every later opponent move to the stopped count M as one continuing D-play, which fails after a later freeze in one daughter; it is replaced by the quiet-move argument (proposed by K52, re-derived step by step by the integrator); the false sub-assertions "M(Y) ≤ M(X)" for re-split Y and "a race needs both threats" for the scored τ are withdrawn; (HSS) is stated with the passer-colour τ_P that `hereditarily_safe` checks. Read by Codex (OpenAI, outside the Claude family) in K52, 2026-11-23: true with its hypotheses, census 32,880 S/W comparisons, 0 disagreements (COMPUTED-1) | R2 item 2; T30 audit: a move count corrected; s12a referee; K52 (Codex) |
>>>>>>> NEW

### EDIT 2 status row T1.14(i)
<<<<<<< OLD
| T1.14(i) | PROVED | R2: sound |
=======
| T1.14(i) | PROVED at a root before the first decisive event, or at a credited root with its own certificate (revised after K52, 2026-11-23: FALSE for an unrestricted already-credited root, cyl:8×6 `Ka1 ka6 Pc2 Pd4 pd3 b -`: D credits White, Black wins P). Read by Codex (OpenAI, outside the Claude family) in K52, 2026-11-23 | R2: sound; K52 (Codex) |
>>>>>>> NEW

### EDIT 3 status row T1.14(iii)
<<<<<<< OLD
| T1.14(iii) | PROVED after repair, but a tautology: (A_Q) is now a per-position hypothesis | R2 item 8 |
=======
| T1.14(iii) | PROVED after repair: (A_Q) is now a per-position hypothesis. Not a tautology (revised after K52, 2026-11-23): (A_Q)(X) is the implication "P-win for σ ⇒ C-win for σ", and (i) supplies the P-winner. Read by Codex (OpenAI, outside the Claude family) in K52, 2026-11-23, with (ii) and the later uses of 1.14: sound per starter | R2 item 8; K52 (Codex) |
>>>>>>> NEW

### EDIT 4 status row T3.4
<<<<<<< OLD
| T3.4 | PROVED | R4: sound |
=======
| T3.4 | PROVED. Re-proved blind by K51 (Codex, OpenAI, outside the Claude family, 2026-11-23): the theorem holds; one sentence of the proof of (a), "Left's winning moves are always G-moves", was FALSE (a winning pass exists for X = {x}, L(x) = {⊕}, R(x) = ∅) and is replaced by "whenever Left wins on its turn, some winning G-move exists" (revised after K51, 2026-11-23); 22,522,464 comparisons of two solvers, 0 disagreements (CHECKED-2, K51) | R4: sound; K51 (Codex) |
>>>>>>> NEW

### EDIT 5 "defined on every board height"
<<<<<<< OLD
  +BIG; neither raises). With this convention S, W and D are defined on every board height, and no result of §1
  needs a bound on H.
=======
  +BIG; neither raises). With this convention the promotion recursion of S, W and D is defined at every board
  height from a passer-free root, and no result of §1 needs a bound on H (revised after K52, 2026-11-23: the
  earlier "defined on every board height" was too wide; at a root that already has passers of both colours S sums
  +BIG − BIG = 0 when they are in different components, flat 8×8 `W a2 / B h7`, and `pawns.value` raises
  RaceError when they are in one, flat 8×8 `W a5 / B b4`; COMPUTED-1, `kings/delegate/out/K52/integrate/verify.out`; such an initial race
  needs a separate convention, as at P11).
>>>>>>> NEW

### EDIT 6 (A_Q) settled-by line: --frozen computes F, not P
<<<<<<< OLD
- *Settled by:* kpsolve with `--cap 1` computes C exactly whenever its bounds agree (A = B), and `--frozen`
  computes P; the two runs decide (A_Q)(X) for that X.
=======
- *Settled by:* kpsolve with `--cap 1` computes C exactly whenever its bounds agree (A = B), and a free-king P
  solver (K7's `kp_p --pmodel`, or the solvers of K19 and K24) computes P; the two runs decide (A_Q)(X) for that X.
  (Revised after K52, 2026-11-23: this line said that `--frozen` computes P; it computes the frozen-king model F,
  as Definition 1.5 states.)
>>>>>>> NEW

### EDIT 7 Definition 1.10: the passer-colour threats τ_P
<<<<<<< OLD
  - This is the τ of `notes/lemmas.md` (Definition 2.0) and of `lemmas/common.py: threats`, which count a
    passer created by either side's move. The earlier version of this note counted only Left options to ⊕ and
    Right options to ⊖, and was therefore blind to suicides (revised after review: R1 item 1, R2 item 1).
=======
  - The earlier version of this note counted only Left options to ⊕ and Right options to ⊖, and was therefore
    blind to suicides (revised after review: R1 item 1, R2 item 1).
  - **Pawn threats τ_P (revised after K52, 2026-11-23).** For a pawn position y, τ_P(y) contains + iff some
    position reachable from y in the same any-order sense (y included, not continuing past a position with a
    passer) has a White passer, and − iff some such position has a Black passer; a race puts both signs in. This
    is the τ of `notes/lemmas.md` (Definition 2.0) and of `lemmas/common.py: threats`. On the pawn D-game
    τ(y) ⊆ τ_P(y), because a terminal credited to a side has a passer of that side (PROVED). The inclusion can be
    strict, so the earlier sentence here, that τ is what `threats` computes, was FALSE at races: on flat 8×8
    `W b2 d6 / B c7`, c7×d6 gives both sides a passer, five moves each, scored for White by the count rule, and no
    terminal credited to Black is reachable, so τ = {+} while τ_P = {+, −} (COMPUTED-1, K52 `examples.py` and
    `kings/delegate/out/K52/integrate/verify.out`). τ_P is monotone like τ. (HSS) of Theorem 1.11(c) and (V4) of
    Theorem 1.14 are stated with τ_P, which makes them exactly what `lemmas/common.py: hereditarily_safe` checks.
>>>>>>> NEW

### EDIT 8 Theorem 1.11(c) label
<<<<<<< OLD
**(c) The re-splitting version. PROVED after repair (R2 item 2).** Let X
=======
**(c) The re-splitting version. PROVED after repair (R2 item 2; the frontier step re-proved, revised after K52, 2026-11-23).** Let X
>>>>>>> NEW

### EDIT 9 (HSS) with τ_P
<<<<<<< OLD
- **(HSS)** at every position Y reachable from X before the first decisive event, the components of Y are
  pairwise safe (Definition 1.10, corrected τ: an option to ⊕ or ⊖ counts whoever makes it); and
=======
- **(HSS)** at every position Y reachable from X before the first decisive event, the components of Y are
  pairwise safe for the pawn threats τ_P of Definition 1.10: a passer of either colour counts, whoever creates it,
  and a race counts for both colours (revised after K52, 2026-11-23: this is what `lemmas/common.py:
  hereditarily_safe` checks; the proof uses only the credited sign, so (c) also holds with the scored τ in
  (HSS), a weaker hypothesis, PROVED by the same proof); and
>>>>>>> NEW

### EDIT 10 (E) cannot be dropped
<<<<<<< OLD
  right. (Revised after the s12a referee, 2026-11-23: the step "both models give the child" of the proof uses it.
  Whether (c) holds without (E) is OPEN: no counterexample in a small search, COMPUTED-1.)
=======
  right. (Revised after the s12a referee, 2026-11-23: the step "both models give the child" of the proof uses it.)
  **(E) cannot be dropped (revised after K52, 2026-11-23; this replaces "Whether (c) holds without (E) is OPEN").**
  On flat 5×7, e.p. on, play a2–a4 from the passer-free position `W a2 b3 e2 / B a5 b4 e4`. The result
  X = `W a4 b3 e2 / B a5 b4 e4`, with Black's right on a3, is passer-free and satisfies (HSS) and (B), yet
  o(S(X)) = 𝓡 while the D-result pair is 𝓝. PROVED by hand: the a/b component is locked except for b4×a3 e.p.,
  which leaves a Black passer on a3, so in S it is { | −B} = −B − 1 and keeps its right while the e-file is
  played; the e-file `W e2 / B e4` offers one move to either side, each of which locks it, so it is *; and
  −B − 1 + * is 𝓡 for every B ≥ 1. In D, White moving first plays e2–e3 (its only move), the right lapses, and
  Black has no move; Black moving first takes e.p. and has a passer; so 𝓝. Neither component can split, the
  e-file never has a threat, and every tempo count is at most 2, so (HSS) and (B) hold; (E) fails at X itself,
  which has two components and a usable right. No race occurs, so the race rule plays no part; the
  e.p.-aware and the textbook passed test agree here. Also COMPUTED-1 with BIG = 256, both passed tests and all
  three race rules: `cgt.outcome(pawns.value(Board(5, 7, False, True), X))` = 𝓡 and `common.alt_outcome` = 𝓝,
  with a second minimax in agreement (`kings/delegate/out/K52/integrate/witness_settings.out`, `verify.out`;
  K52 `examples.py`). The entry that differs has White to move just after its own double step, which is not a
  chess turn. On the chess turn the conclusion fails as well: `W a4 b2 b3 e2 e4 / B a5 b4 b6 e6`, same right,
  Black to move: S is 𝓝 (a/b is −1, the e-file is {2 | 1}) and the D-result pair is 𝓛, so Black to move wins
  in S and loses in D (COMPUTED-1, both passed tests, all three race rules). Both witnesses have a right at the
  root. Whether (E) can be dropped for a root without a right, with (E) failing only later, is OPEN: the
  flag-free predecessors of both witnesses agree (COMPUTED-1, `flagfree_probe.py`), and the K52 census found no
  passer-free root with ≤ 2 + 2 pawns that fails (E).
>>>>>>> NEW

### EDIT 11 unfolding of S: general states
<<<<<<< OLD
*Proof.* Unfold S(X) as a game form F whose positions are pairs (Y, N), where Y is a pawn position (the live
components) and N is a finite multiset of frozen integers ±B. A move is either a move in an integer summand or
a pawn move in a live component Z; if that move creates a passer (or a race) in Z, then Z leaves Y and ±B joins
N; otherwise Z is replaced by its new components. This is `cylcgt.pawns.value` unfolded.
=======
*Proof.* Unfold S(X) as a game form F whose positions are pairs (Y, N), where Y is a tuple of live pawn
components, each with its own e.p. right (F keeps a right with its component while play goes on elsewhere), and
N is a finite multiset of integer stacks, each ±B when it is frozen; spending a token reduces the magnitude of a
stack by one (revised after K52, 2026-11-23: "a multiset of frozen integers ±B" missed the spent stacks). A move
is either a move in an integer stack (the move form n = {n − 1 | } for n > 0 and its negative, before canonical
simplification) or a pawn move in a live component Z; if that move creates a passer (or a race) in Z, the passed
test being applied to all of Z before it is re-split (§1.5), then Z leaves Y and ±B joins N; otherwise Z is
replaced by its new components. This is `cylcgt.pawns.value` unfolded.
>>>>>>> NEW

### EDIT 12 frontier step: the quiet-move argument
<<<<<<< OLD
- **Frontier.** Let (Y, {σB}) be a position of F in which no live component has a (−σ)-threat and
  B > M_{−σ}(Y), where M_{−σ} is the tempo count of the opponent of σ (M_L for White, M_R for Black). Then σ
  wins F(Y, {σB}) whoever moves first. Take σ = +; the case σ = − is symmetric. σ's strategy is to move in the
  positive integer summand on every turn, which is possible while it has a move left; the opponent cannot move
  in a positive integer (its canonical form is {B−1 | }), and every integer frozen later is +B, because a −B
  would need a − threat and a race needs both threats. (Re-split components inherit "no − threat": if a live
  component W₀ has no − threat and a move in W₀ does not freeze it, none of its new components has a − threat.
  A double step does not change which files are occupied, so W₀ does not split; a move that splits W₀ is a
  capture, which leaves no e.p. right, so while a − threat of one new component is played out the others stay
  as they are, with no passer and no right; the move followed by that sequence would be a − threat of W₀. This is
  not the monotonicity of Definition 1.10, which is about one fixed D-game; under the e.p.-aware test a sibling
  with a usable right could otherwise turn passed early. Revised after the s12a referee, 2026-11-23.) So every
  opponent move is a pawn move in a live
  component, and the opponent has at most M_{−σ}(Y) moves in all. σ needs at most M_{−σ}(Y) + 1 moves (one
  reply to each opponent move, plus one if σ moves first), and the first stack has B ≥ M_{−σ}(Y) + 1, so σ
  has a move at every turn of its own and the opponent runs out of moves first. The stack can reach
  0 = { | } only with σ's last move: that takes B ≥ M_{−σ}(Y) + 1 turns of σ, so by then the opponent has made
  all M_{−σ}(Y) of its moves. (Revised after the T30 proof audit, `notes/proof_audit2/REPORT.md`,
  2026-10-22.)
=======
- **Frontier (re-proved, revised after K52, 2026-11-23).** Let Y be a non-terminal position reachable from X,
  let a move in its component Z create a passer or a race in Z credited to σ, and let Y″ be the other
  components of Y. Then σ wins F(Y″, {σB}) whoever moves first. Take σ = + (White); the case σ = − is the colour
  reverse. (The earlier proof charged every later opponent move to the stopped count M_{−σ}(Y″) as if all of
  them were moves of one continuing D-play. After a later freeze in one daughter the opponent can go on in a
  sister, past the point where the stopped count of their common parent stops, so that step was a GAP, K52. The
  argument below was proposed by K52 (Codex) and re-derived step by step by the integrator. PROVED.)
  - *What is used, all at Y.* + ∈ τ_P(Z), since White has a passer after the move, so by (HSS) no component C of
    Y″ has − ∈ τ_P(C) (the scored τ would do as well: the move is an option into a terminal credited to White).
    By (B), B > M_R(Y) ≥ Σ_{C ∈ Y″} M_R(C). If Y″ is non-empty, Y has two or more components, so by (E) no right
    in Y is usable. A right that is not usable allows no capture and protects no pawn from the passed test (both
    need an enemy pawn beside the double-stepped pawn), and it stays so while its component is not played.
  - *Strategies.* White plays only in positive integer stacks, never a pawn move. So after the frontier every
    pawn move is Black's, the only new rights come from Black double steps (rights for White, which White never
    uses), and no Black move is an e.p. capture.
  - *Projection.* Fix a component C of Y″ and list Black's later moves in C and in the daughters into which C
    splits. A move is *quiet* if it does not freeze the daughter it is played in, and *freezing* otherwise. Let
    P₀ = C and let P_k be C after the first k quiet moves, with every frozen daughter left where it stood just
    before its freezing move (parked).
    1. Every quiet move is legal from P_{k−1} in the D-game of C alone (one component, one global right): a
       pawn move depends only on its own file and the adjacent ones; a capture lands only on a file that holds an
       enemy pawn, so occupied files never close the empty file between two daughters, and a parked daughter
       shares no such file with a played one; and no move uses a right.
    2. No P_k is terminal. Let P_k be the first that is. The daughter of the k-th quiet move is passer-free,
       because F tests it with the same right as D (that move set or dropped it). Every other daughter was
       passer-free when last tested, and its pawns and the pawns on its adjacent files are unchanged; D can
       differ from F only by dropping a right that F still keeps there, a right made by a Black double step,
       which can only make that Black pawn passed. So P_k has Black passers only, and it is reached from the
       non-terminal P_{k−1} by a Black move: in the D-game of C a terminal credited to Black is reachable, so
       − ∈ τ_P(C), and also − ∈ τ(C) for the scored τ. This contradicts (HSS).
    3. Every freezing move adds +B. The freezing move from P_{k−1} gives a position P′ of the D-game of C whose
       moved daughter is the one F tests, and the other daughters can only add Black passers, by the argument of
       step 2. If F credited Black (a Black-only passer, or a race scored for Black), P′ would have a Black
       passer and be credited to Black under each of the three race rules: an extra Black passer can only
       shorten Black's promotion distance, and under the mover and opponent rules the mover is Black in both.
       So − ∈ τ_P(C) and − ∈ τ(C), contradicting (HSS).
  - *Count.* By steps 1 and 2 the quiet moves from C form a sequence of Black moves in the D-game of C through
    non-terminal positions, so there are at most M_R(C) of them, and the number q of all quiet Black moves
    satisfies q ≤ Σ_{C ∈ Y″} M_R(C) < B. Each freezing move adds a stack +B. When White is to move after q quiet
    and f freezing Black moves, White has made at most q + f moves, so its stacks hold at least
    B + fB − (q + f) = (B − q) + f(B − 1) ≥ 1 tokens, and White has a move. Black cannot move in a positive
    integer. Every Black move advances a pawn, so Black makes finitely many moves, and White's tokens are
    finite; so play is finite, White never runs out of moves, and Black does: White wins, whoever started.
  - *What this needs from Definition 1.10.* τ and M must be read with any-order sequences, since the projected
    play is Black's alone; they may stop at the first terminal, since the projection passes none before its last
    step. So the definitions as stated suffice, with (B) as stated (at Y). The earlier argument that re-split
    daughters inherit "no − threat" (revised after the s12a referee) is sound (K52) but no longer needed.
  - *An alternative under a stronger bound.* Let N(X) be the largest number of moves of one side in any finite
    sequence of legal pawn moves from X, by either side in any order, play continuing past passed pawns. Under
    (E), B > N(X) implies (B): at a reachable Y the longest stopped sequences of the components of Y can be
    played one after another after the moves from X to Y, so Σ M ≤ N(X) (PROVED). The converse fails: a stopped
    count ends at the first passer and N(X) does not, and on boards up to 8×8 N(X) ≤ 8(1 + 2 + … + 6) = 168 < 256.
    Under B > N(X) the count above is immediate: Black's moves after the frontier, freezing ones included,
    played on the whole board after the moves from X to Y, form such a sequence (file locality; White makes
    no pawn move; no older right is usable, by (E)), so there are fewer than B of them; step 3 is still needed
    for the sign of the later stacks (PROVED; this is the route of the paper's appendix, `s12a_core.tex`, A.6).
>>>>>>> NEW

### EDIT 13 induction: withdraw "its moves are moves of D and the tempo count bounds them"
<<<<<<< OLD
    the same options in both models and no passer in the child. For the same reason, after the frontier the
    opponent never captures e.p. with a right left from before it, so its moves are moves of D and the tempo
    count bounds them (revised after the s12a referee, 2026-11-23).
=======
    the same options in both models and no passer in the child (the two children differ at most by rights
    that are not usable, which change no option and no passed test). For the same reason, after the frontier
    the opponent never captures e.p. with a right left from before it (revised after the s12a referee,
    2026-11-23). That alone does not bound the opponent's later moves by a stopped count; the frontier step
    does (revised after K52, 2026-11-23: the clause "so its moves are moves of D and the tempo count bounds
    them" is withdrawn; read as one continuing D-play it is FALSE).
>>>>>>> NEW

### EDIT 14 induction, terminal child: drop M(Y) ≤ M(X) and "a race has both threats"
<<<<<<< OLD
    starts. F gives (Y″, {σB}), where Y″ consists of the other components of Y. Here σ ∈ τ(Z): Z reaches the
    passer in one move, and for a race both signs are in τ(Z). Y is pairwise safe by (HSS), so no other live
    component has a (−σ)-threat, and the frontier step applies because M_{−σ}(Y″) ≤ M_{−σ}(Y) ≤ M_{−σ}(X) < B.
    So σ wins this option too.
=======
    starts. F gives (Y″, {σB}), where Y″ consists of the other components of Y, and σ wins it whoever starts by
    the frontier step, which uses (HSS), (B) and (E) at Y itself. So σ wins this option too. (Revised after
    K52, 2026-11-23. The earlier text bounded M_{−σ}(Y″) ≤ M_{−σ}(Y) ≤ M_{−σ}(X); the second inequality is FALSE
    for re-split positions: flat 5×6, e.p. off, `W a2 a3 c2 d2 d3 e3 / B a4 b3 d4` is one component with stopped
    M_Black = 1, and after c2×b3 each of its two daughters has M_Black = 1, since in either a Black capture
    creates a White passer (COMPUTED-1, `kings/delegate/out/K52/integrate/verify.out`). It is not needed, since
    (B) holds at Y. The text also said that for a race both signs are in τ(Z): true for τ_P, false for the scored
    τ, and only the credited sign is used.)
>>>>>>> NEW

### EDIT 15 necessity of the hypotheses of 1.11(c)
<<<<<<< OLD
Outcomes are determined by the outcomes of the options, so o(F(Y, ∅)) = o(D(Y)). ∎
=======
Outcomes are determined by the outcomes of the options, so o(F(Y, ∅)) = o(D(Y)). ∎

*The hypotheses of (c) are needed in a uniform statement (revised after K52, 2026-11-23).*
- (E): the flat 5×7 example stated with (E) above (PROVED).
- (HSS): flat 5×6, e.p. off, `W a4 d4 / B b5 e5`. In each pair every move ends the component: each side has a
  capture that leaves its own passer, and each push makes a race, so each pair is {B | −B} whatever the races
  score; the
  two equal switches cancel, S = 0 = 𝓟, while in D whoever moves captures and wins, 𝓝. (E), (B) and the
  passer-free root hold (PROVED by hand; COMPUTED-1, `kings/delegate/out/K52/integrate/verify.out`). This is
  Proposition 1.12 in pawns.
- (B): Proposition 1.13 in pawns. W a4 / B b5 as one component and, on a separated file, W d2 / B d3 with a rear
  Black pawn that has n moves left, so that component is −n. For B = 1 and n = 2 (flat 4×7, rear pawn on d6),
  {1 | −1} − 2 is 𝓡, while in D White moving first plays a4×b5 and wins (PROVED by hand). With BIG = 256 the same
  shape on flat 4×263, rear pawn on d261 (n = 257): o(S) = 𝓡, D gives 𝓝, (HSS) holds (COMPUTED-1, same file).
  On boards up to 8×8, (B) holds automatically for B = 256, since every tempo count is at most
  8(1 + 2 + … + 6) = 168 (PROVED).
>>>>>>> NEW

### EDIT 16 (V4) with τ_P
<<<<<<< OLD
    into two), with the king group Z deleted, are pairwise safe: no two different components carry + ∈ τ and
    − ∈ τ, where τ counts options to ⊕ or ⊖ by **either** player (Definition 1.10);
=======
    into two), with the king group Z deleted, are pairwise safe: no two different components carry + ∈ τ_P and
    − ∈ τ_P, where τ_P counts a passer of either colour, whoever creates it, and a race for both colours
    (Definition 1.10; revised after K52, 2026-11-23: τ_P, as in (HSS) and `hereditarily_safe`);
>>>>>>> NEW

### EDIT 17 Theorem 1.14(i): a root before the first decisive event
<<<<<<< OLD
- **(i)** P(X) = D(X) with s to move. There are no draws, and the result is the normal-play result of G₁ ⊞ … ⊞ G_k (Z
  deleted).
=======
- **(i)** P(X) = D(X) with s to move. There are no draws, and the result is the normal-play result of G₁ ⊞ … ⊞ G_k (Z
  deleted). Here X is a position of D(X), that is, before the first decisive event. (Revised after K52,
  2026-11-23: if the convention already credits a terminal at X, no event is reached by a move and (V2) says
  nothing; (i) then needs its own root certificate, that X with s to move is a P-win for the credited side, as in
  P11. Without it (i) is FALSE: cyl:8×6 `Ka1 ka6 Pc2 Pd4 pd3 b -`, where d4 is passed and d3 is blocked by c2, so
  D credits White, but Black plays d3–d2 and d2–d1, and in between White can neither promote nor stop d2. PROVED
  by hand; `--frozen` gives (L, L), §6 P11.)
>>>>>>> NEW

### EDIT 18 Theorem 1.14(iii) statement: not a tautology
<<<<<<< OLD
- **(iii)** Under (A_Q)(X) (the per-position hypothesis of §1.2, checked by kpsolve), C(X) = P(X). This is now
  a tautology: (A_Q)(X) says exactly this (revised after review: R2 item 8).
=======
- **(iii)** Under (A_Q)(X) (the per-position hypothesis of §1.2, checked by kpsolve), C(X) = P(X) with s to move.
  (Revised after K52, 2026-11-23: this used to be called a tautology; (A_Q)(X) is only the implication "P-win for
  σ ⇒ C-win for σ" and says nothing about a P-draw, so (iii) also uses (i).)
>>>>>>> NEW

### EDIT 19 Theorem 1.14(iii) proof
<<<<<<< OLD
- **(iii)** Definition of (A_Q)(X). ∎
=======
- **(iii)** By (i) the starter s has a P-winner σ. By (A_Q)(X) σ wins C from the same root with the same starter,
  so the two entries agree (revised after K52, 2026-11-23). ∎
>>>>>>> NEW

### EDIT 20 summary row T1.14
<<<<<<< OLD
| T1.14 | Validity, per side to move: (V1)–(V3) for that side give P = D (no draws),
=======
| T1.14 | Validity, per side to move: (V1)–(V3) for that side give P = D (no draws) at a root before the first decisive event (revised after K52, 2026-11-23),
>>>>>>> NEW

### EDIT 21 Proposition 1.15(b) search: the conjecture is limited by the counterexample
<<<<<<< OLD
    found, and when (HSS) holds the sum reading and the chess reading agreed on every searched root. CONJECTURE that (E) can be
=======
    found, and when (HSS) holds the sum reading and the chess reading agreed on every searched root. Outside this boundary (E) cannot be dropped from Theorem 1.11(c): a pawn-only position on flat 5×7 satisfies (HSS) and (B) and gives o(S) ≠ D (revised after K52, 2026-11-23; see the statement of Theorem 1.11(c)). CONJECTURE that (E) can be
>>>>>>> NEW

### EDIT 22 (V1a) table row: (E) clause
<<<<<<< OLD
(CONJECTURE that (E) is not needed when (HSS) holds, in the searched boundary only) |
=======
(CONJECTURE that (E) is not needed when (HSS) holds, in the searched boundary only; for pawn sums in general it is needed, Theorem 1.11(c), revised after K52, 2026-11-23) |
>>>>>>> NEW

### EDIT 23 §7 en passant
<<<<<<< OLD
   - Inside components, the sum needs condition (E) (L1.6–1.7 of `notes/lemmas.md`). Theorem 1.14(V1a)
=======
   - Inside components, the sum needs condition (E) (L1.6–1.7 of `notes/lemmas.md`), and Theorem 1.11(c) fails
     without it even under (HSS) and (B) (revised after K52, 2026-11-23). Theorem 1.14(V1a)
>>>>>>> NEW

### EDIT 24 Theorem 3.4(a) proof: the false sentence
<<<<<<< OLD
  - So Left's winning moves are always G-moves. Left wins (x, R) iff every Right option, Right's pass
=======
  - So whenever Left wins on its turn, some winning G-move exists (revised after K51, 2026-11-23: the earlier
    "Left's winning moves are always G-moves" is FALSE. For X = {x}, L(x) = {⊕}, R(x) = ∅, White to move can
    pass, Black's only option is to pass back, and White takes ⊕; so the pass is a winning move. The stage
    argument above shows only that a first-stage win is never established by the pass. PROVED by hand; found by
    K51, Codex). Left wins (x, R) iff every Right option, Right's pass
>>>>>>> NEW

### EDIT 25 Lemma B title and its pointer to Theorem 3.4
<<<<<<< OLD
**Lemma B (the winner of G ⊞ dud_D never passes).**
=======
**Lemma B (the winner of G ⊞ dud_D need never pass; revised after K51, 2026-11-23: "never passes" was too strong, a winning pass can exist, as in the example in the proof of Theorem 3.4(a)).**
>>>>>>> NEW

### EDIT 26 pointer after Lemma B
<<<<<<< OLD
This is the content of the proof of Theorem 3.4(a), "Left's winning moves are always G-moves".
=======
This is the content of the proof of Theorem 3.4(a), "whenever Left wins on its turn, some winning G-move exists"
(revised after K51, 2026-11-23).
>>>>>>> NEW
