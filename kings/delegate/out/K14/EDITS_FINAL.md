# K14 final edits to kings/theory/LOOPY.md (fix round, 2026-10-27)

Rebased onto the current LOOPY.md (which contains the K19 and K23 edits of 2026-10-27, commit fb7d4a4). Each block replaces its OLD text (which occurs exactly once in the current LOOPY.md) by its NEW text. Apply all 14 blocks.

## Notes for the integrator

- LOOPY.md now contains the K19 and K23 edits of 2026-10-27 (commit fb7d4a4). All 14 OLD texts were re-checked against it: each occurs exactly once. Blocks 1, 7, 8, 9, 10, 11, 13 and 14 changed in substance after the referee (VERIFY.md section 7); blocks 2, 3, 4, 5, 6 and 12 are K14's text unchanged (the referee found them accurate). No new block was needed: the referee found no further stale text.
- **Z_B is CHECKED-2 in P.** The integrator confirmed Z_B's 8 root values (all D in P) and every move list at the 8 roots with the K23 referee's independent solver ref3 (`kings/delegate/out/K23/verify/ref3.cpp`; for flat boards pass `--board flat7x6`, a parsing quirk), which shares no code with kpsolve or kp_p. So "Z_B alone is (D, D) at all 8 roots in P and every non-shuttle move loses at once" is CHECKED-2 (kp_p and ref3). The contexts, the bridge counts and the search are COMPUTED-1 (the referee's kpp run, one implementation).
- Section 8 numbers used (VERIFY.md): Z_A beside all 885 contexts with <= 2 + 2 pawns on f, g (7,080 roots): 58 contexts (156 roots) differ from r(G + dud_D), all with prediction D and a decisive result, no predicted W or L contradicted. Z_B beside the first 660 of those 885 contexts (5,280 roots): 0 differ, 225 contexts untested.
- Referee points, all applied: (1) the negative search result is replaced by Z_B (blocks 1, 7, 10, 11, 13); the K14 search is kept only as a record, with its cut-off (18), which excluded Z_B (blocks 10, 13, 14); its 7x7 and cylinder statements are marked not repeated and not claimed. (2) The e.p. remark: Lemma A unchanged, Lemma B gets the extra line (block 8). (3) The "72 %" figure is dropped; "a positive fraction, and at G = 0 all four states" replaces it (block 8). (4) Header wording: "re-checked by one referee (same model family) and by two brute-force implementations, short and loopy G" (blocks 1, 8). (5) Bridge counts: 208 and 48 under the referee's convention, 0 failures; K14's 200 and 16 mentioned as its own convention (block 10). (6) Pun is the only gap of the bridge, and chess needs (A_Q) (block 8). (7) The e2/g4 qualifier for "never contradicted" (block 10). (8) The unchecked 7.3 sentence "which in Z7.3 lose only because of f8=Q" is deleted, and the false last sentence of block 9 is replaced; the Kf8 remark (f8=Q exists in two of four states) is added (block 9). (9) In chess with cap 1 the bounds for Z_B are (W, L), undecided; open: chess (cap 2), the cylinder, other boards.
- No referee point was judged wrong. One small deviation: the referee says Z_B has 27 non-shuttle moves over the 8 roots; the move lists in VERIFY.md section 5.2 add up to 26, so the count is not quoted.
- The label "CONJECTURE that Z_B is exactly two-shuttle in every context" is kept as a CONJECTURE: (Pun) is a per-context fact and 225 of 885 contexts are untested. No label is stronger than the evidence: Theorem 3.2‴ stays conditional, and solver results are never called PROVED.

### EDIT status row: shuttles on both sides
<<<<<<< OLD
| §3, shuttles on both sides | CONJECTURE: needs a two-sided Proposition 3.2 | R4 item 6 |
=======
| P3.2′ (two shuttling kings are a dud) | D-model: PROVED (new, K14; revised after the K14 referee, 2026-10-27): a p-morphism onto dud_D on the four combined king states, for every D-game G; inequalities when one side has further Z-moves; a win needs only the half of the states in which the winner's king stands still; all eight shuttle arrows are needed (counterexamples). The proof was re-checked by one referee (same model family) and the statements by two brute-force implementations, on short and loopy G, 0 violations (COMPUTED-1 for the data). Chess bridge (Theorem 3.2‴): PROVED in P, conditional on (V1a-ctx), (V2-ctx) and the per-group hypothesis (Pun) that every non-shuttle Z-move is decisively punished; stalemate is excluded automatically. (Pun) is the only gap of the bridge; the chess statement also needs (A_Q). Existence (revised after the K14 referee, 2026-10-27): Z_B (§5.7; flat 7×6; White king b2/c3, Black king a4/b5, pawns Pa3 Pb4 pb3 pc4) has every non-shuttle move losing at once, and Z_B alone is (D, D) at all 8 roots in P: CHECKED-2 (kp_p and the independent solver ref3). Beside every context tested the P-result of G ⊞ Z_B equals r(G ⊞ dud_D): COMPUTED-1 (68 contexts, 12 contexts on files e–g, and the first 660 of 885 contexts of ≤ 2 + 2 pawns on f, g; 225 contexts untested). In chess with cap 1 the bounds at the 8 roots are (W, L): undecided. Open: chess (cap 2), the cylinder, other boards. Z_A (§5.7) is a second group, with one White break (Kxb4). K14's first search found no frozen group only because of a move-count cut-off (18) that excluded Z_B | R4 item 6; K14 and its referee |
>>>>>>> NEW

### EDIT results table: new row P3.2prime
<<<<<<< OLD
| C3.5 | Monotone chain: White wins with dud ⇒ with off ⇒ with nothing ⇒ with on | PROVED |
=======
| C3.5 | Monotone chain: White wins with dud ⇒ with off ⇒ with nothing ⇒ with on | PROVED |
| P3.2′ | Two shuttling kings are a dud: a component with four combined shuttle states, each side's shuttle an option and every other option a suicide, has r(G ⊞ Z) = r(G ⊞ dud_D) for every G; inequalities with further Z-moves; the chess bridge has no stalemate hypothesis | D-model PROVED; chess bridge PROVED, conditional on (Pun) (new, K14, 2026-10-27) |
>>>>>>> NEW

### EDIT summary: both sides can pass
<<<<<<< OLD
  - **if both sides can pass,** a side wins iff it can force a decisive event against a passing opponent;
    otherwise the game is drawn.
=======
  - **if both sides can pass,** a side wins iff it can force a decisive event against a passing opponent;
    otherwise the game is drawn. For a king group with two frozen shuttles this is Proposition 3.2′ together with
    Theorem 3.4(a) (revised after K14, 2026-10-27).
>>>>>>> NEW

### EDIT sharp form: D for the two-sided bridge
<<<<<<< OLD
  For the chess bridge after Proposition 3.2, D = G ⊞ on_D and π sends both shuttle states to ω.
=======
  For the chess bridge after Proposition 3.2, D = G ⊞ on_D and π sends both shuttle states to ω. For the two-sided
  bridge (Theorem 3.2‴), D = G ⊞ dud_D and π sends all four combined king states to ω.
>>>>>>> NEW

### EDIT sharp form: reading (b), a loser that owns a shuttle
<<<<<<< OLD
  those played, because σ̄ chooses. In reading (b) an unpunished Z-move of σ̄ (a loser that owns a shuttle) is a
  D-move and needs no punishment. A decisive event that σ̄ makes for σ is a closing move, which is (V2).
=======
  those played, because σ̄ chooses. In reading (b) an unpunished Z-move of σ̄ (a loser that owns a shuttle) is a
  D-move and needs no punishment: this is the loser's shuttle in Theorem 3.2‴, and with it the loser's stalemate
  (S3) cannot occur. A decisive event that σ̄ makes for σ is a closing move, which is (V2).
>>>>>>> NEW

### EDIT P3.2: pointer to the two-sided version
<<<<<<< OLD
Then, in the D-model and for a short context G, r(G ⊞ Z) ≥ r(G ⊞ on_D), with equality if White has no other
Z-moves.
=======
Then, in the D-model and for a short context G, r(G ⊞ Z) ≥ r(G ⊞ on_D), with equality if White has no other
Z-moves. (Two shuttles, one for each king: Proposition 3.2′ below.)
>>>>>>> NEW

### EDIT section 3: shuttles on both sides
<<<<<<< OLD
- **With shuttles on both sides (CONJECTURE):** all tempo content should disappear. Positions without threats
  should be draws, even where the convention predicts a clear winner. The 7.3 group would be of this type if
  its pawn could not promote (§5.3). *To settle:* a two-sided Proposition 3.2 — a bisimulation on the four
  combined king states, in each of which each side's shuttle is legal and each side is frozen — followed by
  Theorem 3.4(a). (Revised after review: R4 item 6: Theorem 3.4 is stated for one reservoir, so this bullet
  was not proved by it.)
=======
- **With shuttles on both sides (PROVED in the D-model by Proposition 3.2′; revised after K14 and its referee, 2026-10-27):** for a
  component with four combined king states, each side's shuttle an option and every other option a suicide, all tempo
  content disappears. A position in which neither side can force a decisive event against a passing opponent is a
  draw even where the convention predicts a clear winner, and a side wins iff it can (Theorem 3.4(a), through
  Proposition 3.2′). The chess bridge is Theorem 3.2‴. It needs, per group and context, that every non-shuttle Z-move
  is decisively punished; a win needs this only for the loser and only in the two states in which the winner's king
  stands still. The 7.3 group is **not** of this type: f7–f8=Q is a White Z-move that is no suicide (§5.3). A group of this type
  exists in P on the flat 7×6 board: Z_B of §5.7 has every non-shuttle move losing at once at all 8 roots (CHECKED-2),
  and beside every context tested its P-result equals r(G ⊞ dud_D) (COMPUTED-1; 225 of 885 contexts untested);
  CONJECTURE that this holds in every context. Whether Z_B is exactly two-shuttle in chess is undecided (cap 1 gives
  the bounds (W, L)); open: chess (cap 2), the cylinder, other boards (§8, item 2). Z_A (§5.7) has one White break.
>>>>>>> NEW

### EDIT section 3: Proposition 3.2prime and its chess bridge
<<<<<<< OLD
**Literature (KNOWN, as summarised in [notes/lit_cgt_chess.md](../../notes/lit_cgt_chess.md)).**
=======
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

*(Remark on e.p.; revised after the K14 referee, 2026-10-27.)* The sum of Definition 1.3 leaves G alone under a Z-move,
and in chess an e.p. right expires under a king move. Model the flag as a coordinate of G that every Z-move resets, and
the pass of dud_D likewise. Lemma A goes through unchanged (φ forgets only the Z-state, and both games reset the flag at
corresponding moves). Lemma B needs one more line. The pass from (x, f, ω, σ) leads to (x, none, ω, σ̄), and the pass
back leads to the flag-free state (x, none, ω, σ), which is not (x, f, ω, σ) when the flag f is set. The flag belongs
to the side to move, so (x, f, σ) has all the options of (x, none, σ) and possibly an e.p. capture more. By option
monotonicity (Lemma 1.6) its stage is at most the stage of (x, none, σ). So (x, f, σ) enters at stage ≤ m < n: the same
contradiction. The conclusion of Lemma B also holds on all 4,579 pawn contexts of the checks below (155,400 winning
nodes, 0 violations; the referee's `vpawn.py`; COMPUTED-1). The chess statements below use this reading.

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

**Which hypotheses hold (revised after K14).**
- (K1), (K2) are a finite test on Z alone, and by Lemma 3.2″ they give legality of both shuttles, no check and no
  stalemate in **every** context. (V1b) is therefore no hypothesis here: it is automatic, unlike in the one-sided bridge.
- A win needs no hypothesis on the winner's shuttle (Lemma B): only (Pun) for the loser, in the two states in which the
  winner's king stands still. Draws and the exact statement need (Pun) for both sides in all four states.
- (V1a-ctx), (V2-ctx) are per-context facts, as in the one-sided bridge.
- (Pun) is a per-group, per-context fact. It does not follow from the geometry of Z, and it fails when a counter-chance
  is faster than the punishment (Proposition 2.10(b)). It is the only gap of the bridge (the chess statement needs (A_Q)(X) as
  always, and (Pun) is stated for P): no theorem here gives it for a concrete group in all contexts. Theorem 2.7 and Proposition 2.10(a) give it in P for punishments of depth
  T = 1 under their side conditions.

**Checks of Proposition 3.2′ and Theorem 3.2‴ (K14 and its referee; data, not proofs; revised after the K14 referee,
2026-10-27).**
- *D-model, brute force, K14* (`kings/delegate/out/K14/scripts/prop_check.py 400`): 400 random short D-games G (3 to 6
  positions, random options including ⊕, ⊖), each with random components Z of the kinds "exact (T1)–(T4) with extra
  suicides", "(T1), (T2), (T4) plus random further White options", the mirror, and (c)'s half-slice, solved by least fixed
  point on the explicit sum. (a): 44,208 of 44,208 instances agree. (b): 44,208 of 44,208 for each of the two
  inequalities. (c): 4,980 of 4,980. COMPUTED-1: the solver is new and one implementation; the statements are PROVED
  above.
- *D-model, brute force, the referee's own implementation* (`kings/delegate/out/K14/verify/vdmodel.py 400 777`,
  counter-based retrograde on the explicit sum): 400 random games of 2 to 6 positions, half of them loopy, 0 to 2 extra
  Z-positions. (a): 38,544 of 38,544 short and 37,200 of 37,200 loopy. (b): 75,744 of 75,744 for each inequality. (c):
  6,492 of 6,492 (White version) and 6,060 of 6,060 (Black version). 0 violations. COMPUTED-1 for the data; the
  statements are PROVED above, for loopy G as well.
- *Predictions for pawn-only contexts:* the least-fixed-point solver `scripts/dmodel.py`, the closed recursion of
  Theorem 3.4(a) (`scripts/closed_form.py`, a pass resets the e.p. flag) and the referee's third implementation
  (`verify/vpawn.py`, own pawn generator and own retrograde) agree on all 4,579 contexts of ≤ 2 + 2 pawns on files e–g
  of the flat 7×6 board: CHECKED-2. All three solve Theorem 3.4(a) on one pawn-game model, so this checks Theorem 3.4(a)
  with e.p. resets, not chess.
- *Chess, concrete groups:* §5.7. Counts are root instances of Theorem 3.2‴ under the referee's convention: (Pun) for the
  loser holds on all regular positions reachable from the root and the D-result is W or L, for (a); both (Pun) hold, for
  (b). Z_A: (a) 208 instances, (b) 48 instances, 0 failures. Z_B: (a) 160 instances, (b) 56 instances, 0 failures.
  COMPUTED-1 in P.

**Literature (KNOWN, as summarised in [notes/lit_cgt_chess.md](../../notes/lit_cgt_chess.md)).**
>>>>>>> NEW

### EDIT 5.3: without the pawn break
<<<<<<< OLD
- **Without the pawn break. CONJECTURE** (revised after review: R4 item 6): if f8 were unavailable, the
  group would be a both-sides shuttle (dud-type), and Theorem 3.4(a) would make every threat-free sum a draw —
  but that needs a two-sided Proposition 3.2, which is not proved: the bisimulation must hold on the four
  combined king states, in each of which each side's shuttle is legal and each side is frozen.
  - *Scratch evidence:* no both-sides-shuttle group without a pawn break exists among 3-file groups with
    ≤ 2 + 2 pawns and no passer on the 8×6 cylinder. dud may not occur in small K+P groups (CONJECTURE).
=======
- **Without the pawn break (revised after K14 and its referee, 2026-10-27).** Z₇.₃ itself is not a two-shuttle
  component: f7–f8=Q is a White Z-move that is no suicide, so (T3) of Proposition 3.2′ fails and part (b) gives only
  r(G ⊞ Z₇.₃) ≥ r(G ⊞ dud_D), the trivial bound here. (At the two states with Kf8 the pawn f7 is blocked, so f8=Q exists
  in only two of the four states; (T3) fails all the same.) The four combined king states are legal (the kings keep
  distance ≥ 2 in all four; K1 holds: Black's g7 attacks f6 and h6, White's f7 attacks e8 and g8, so neither pawn attacks
  a shuttle square of the other king), so the geometry of Lemma 3.2″ holds. "If f8 were unavailable" does not define a group. The earlier sentence "would be dud-type" is
  withdrawn as unproved. The two-sided proposition it needed is now Proposition 3.2′ (PROVED in the D-model). A group of
  this type exists elsewhere on the flat 7×6 board: Z_B of §5.7 (every non-shuttle move loses at once in P, CHECKED-2),
  and Z_A of §5.7 is two-shuttle up to one White break.
  - *Scratch evidence:* no both-sides-shuttle group without a pawn break exists among 3-file groups with
    ≤ 2 + 2 pawns and no passer on the 8×6 cylinder. This is the earlier scratch search on the cylinders only, with
    one-ply tests, not re-run; it says nothing about flat boards, where Z_B exists (§5.7). "dud may not occur in small
    K+P groups" remains a CONJECTURE for chess and for the cylinder.
>>>>>>> NEW

### EDIT section 5.7 (new): a two-shuttle group
<<<<<<< OLD
## 6. Testable predictions
=======
### 5.7 Two-shuttle groups (K14, 2026-10-27; revised after the K14 referee, 2026-10-27)

Two groups on the flat 7×6 board (F_Z = {a, b, c}, buffer d, context on e–g): Z_A, found first, has one White break,
and Z_B (below, after Z_A) has none. Everything below is a statement in the P model unless chess is named.

**Z_A = Ka5, Ka6 (shuttle) / kc5, kc6 (shuttle) / Pb3 pb4 pb5**, on the flat 7×6 board (F_Z = {a, b, c}, buffer d, context
on e–g). Kings at (a, c) ∈ {a5, a6} × {c5, c6}.
- **Geometry. PROVED by enumeration.** The four states satisfy (K1) and (K2): pb4 and pb5 attack a3, c3, a4, c4, and Pb3
  attacks a4, c4, none of the four shuttle squares; d(a, c) = 2 in all four. The Z-pawns are blocked (b3–b4–b5) and cannot
  move. White's legal moves other than the shuttle: **Kxb4 at (a5, c6) only** (b4 is then undefended); at every other
  state White has no other move (a4 is attacked by b5, b5 is guarded by the Black king, b6 is next to the Black king).
  Black's legal moves other than the shuttle are the sorties c5–d4, d5, d6 and c6–d5, d6 (c4 is attacked by b3, b6 is next
  to the White king).
- **Z alone is (D, D) at all 8 roots** (4 states × 2 sides to move; kpsolve P model, real kings, exact: COMPUTED-1). Every
  Black sortie loses at once (the position after it is a White win). White's Kxb4 draws: it is a non-suicidal further White
  Z-move, so (T3) fails at (a5, c6) and Z_A is a two-shuttle component *up to one White break*. Reproduce: the 8 roots
  (e.g. `Ka5 kc6 Pb3 pb4 pb5 w -`) piped into `kpp --board flat:7x6 --ep on --promote QRBN --cap 1 --pmodel --moves`,
  where `kpp` is a private build of `kings/delegate/out/K7/scripts/draft/kp_p.c`.
- **What Proposition 3.2′ gives for Z_A.** (T1), (T2), (T4) hold at all four states (T4 in the Z-alone sense above), so part
  (b) gives r(G ⊞ Z_A) ≥ r(G ⊞ dud_D) in the D-model, part (c) transfers a White win from any state, and a Black win from
  the two states with the Black king on c5 (there White has no move but the shuttle).
- **Contexts. COMPUTED-1 (P model), prediction CHECKED-2.** 68 pawn-only contexts of ≤ 3 pawns on the files f and g (all six
  outcome pairs of G ⊞ dud_D occur: (D,D), (D,L), (L,L), (W,D), (W,L), (W,W)), each with the four king states and both
  sides to move (544 roots). In **53 contexts** the exact P-result of G ⊞ Z_A equals the prediction r(G ⊞ dud_D) at all 8
  roots. Examples (White's, Black's pawns; prediction): none; f3 / f4 (D,D) blocked; f2 / — (W,W); — / f3 (L,L); f3 / g4
  (W,L); f2 f4 / g5 (W,D); f2 / f5 g3 (D,L). In the **15 other contexts** (40 roots) the result differs, in every case at
  a context in which (Pun) fails somewhere on the regular positions. In all 40 mismatching roots the prediction is D and the result is decisive: Black
  wins in 10 contexts (a sortie beats the context race), White in 4 (White's break Kxb4 turns Black's shuttle into a
  zugzwang), both in 1. Predicted W or L was never contradicted in this f/g sample. Example f2 / f3 (blocked, so G has no move): the prediction is (D, D), but Black to move at (a5, c5) must
  shuttle to c6, and Kxb4 then wins; four of the eight roots are W. With the context on files e–g (closer to the sortie
  squares) 5 of 12 representative contexts fail (24 of 96 roots), and with White e2, Black g4 (prediction (W, L)) the
  result is (L, L) at all 8 roots: a predicted White win is contradicted there, so "never contradicted" holds only in
  the f/g sample. In the larger sample of all 885 contexts with ≤ 2 + 2 pawns on files f, g (7,080 roots), 58 contexts
  (156 roots) differ from r(G ⊞ dud_D), all with prediction D and a decisive result, and again no predicted W or L is
  contradicted (the referee's kpp run, COMPUTED-1; the rates 58 of 885 and 15 of 68 are not comparable, the samples
  differ).
- **Chess (C) for Z_A. Mostly not done.** In chess (`kpsolve --board flat:7x6 --ep on --promote QRBN --cap 1`) Z_A alone
  is (D, D) at all 8 roots, exact (COMPUTED-1, 1.4 CPU-s). The chess results with contexts were not computed: a batch of 4
  contexts was still running after one CPU-minute and was stopped, and the shared heavy slots were queued behind other
  jobs. So (A_Q) is not checked for any context, and every context result above is a statement in P.
- **The bridge on Z_A. COMPUTED-1.** `scripts/bridge_check.py` enumerates the regular positions of each context (8 to
  about 330) and classifies every legal move as context move, shuttle or other. (Pun_White) holds at all regular positions
  in 14 of the 68 contexts, (Pun_Black) in 17, both in 2 (the referee's own generator of the 2,304 regular positions
  agrees, and finds exactly one shuttle for the side to move at each). Theorem 3.2‴(a): at the 208 roots where (Pun) for
  the loser holds on the regular positions reachable from the root and r_D = W (resp. L) for the winner, P agrees: 0
  failures. Theorem 3.2‴(b): 48 roots with both (Pun)'s, 0 failures. (Counts under the referee's convention; K14's own
  convention gave 200 and 16, also with 0 failures.) All 15 mismatching contexts have a (Pun) failure: 0 contexts where the hypotheses hold and the conclusion
  fails. (Pun) is sufficient, not necessary: many of the 53 matching contexts have a (Pun) failure at some regular position
  that the winner's play never uses.
- **An exactly frozen two-shuttle group: Z_B (revised after the K14 referee, 2026-10-27). Z_B alone: CHECKED-2 in P; the
  search and the contexts: COMPUTED-1.** K14's first search (next bullet) found none, because it cut the candidates by an
  approximate count of other moves (at most 18, and 12 for 3 + 3 pawns). The referee searched flat 7×6 with F_Z = {a, b, c}
  and at most 2 White and 2 Black pawns on ranks 2 to 5, **with no cut-off**: 817,270 placements in which the four
  combined king states are legal (K1, K2). At the two roots (z, w), White and Black to move, 535 placements have no
  non-shuttle move that fails to lose at once. At all 8 roots **2 placements have none (mirror images of each other)**
  and 12 have exactly one (Z_A type).
  - **Z_B:** White king b2, c3 (shuttle), Black king a4, b5 (shuttle), pawns Pa3 Pb4 pb3 pc4. Its mirror (a ↔ c) is
    Ka3, Kb2 / kb5, kc4 / Pb4 Pc3 pa4 pb3. Roots are written like `Kb2 ka4 Pa3 Pb4 pb3 pc4 w -`.
  - *Geometry. PROVED by enumeration.* (K1): pb3 attacks a2, c2; pc4 attacks b3, d3; Pa3 attacks b4; Pb4 attacks a5, c5;
    none of b2, c3, a4, b5. (K2): d(b2, a4) = 2, d(b2, b5) = 3, d(c3, a4) = 2, d(c3, b5) = 2.
  - *Move lists at the 8 roots (P model).* The value is that of the position after the move, from White's point of view
    (L = White has lost, W = White has won, D = draw). White to move | Black to move:
    - (b2, a4): Kb1 L, Kc1 L, Ka1 L, b4–b5 L, shuttle D | shuttle D, c4–c3 W
    - (b2, b5): Kb1 L, Kc1 L, Ka1 L, a3–a4 L, shuttle D | Kb6 W, Kc6 W, Ka6 W, c4–c3 W, shuttle D
    - (c3, a4): Kc4 L, Kd4 L, Kd2 L, b4–b5 L, shuttle D | Kxa3 W, b3–b2 W, shuttle D
    - (c3, b5): Kd4 L, Kd2 L, a3–a4 L, shuttle D | Kb6 W, Kc6 W, Ka6 W, b3–b2 W, shuttle D
  - **Z_B alone is (D, D) at all 8 roots in P, and every non-shuttle move loses at once** (every non-shuttle move is a loss for the
    mover; the shuttle draws). So (Pun) holds for Z_B alone at all 8 roots, in both colours. **CHECKED-2:**
    the referee's build of kp_p (the K7 P-model solver) and the K23 referee's solver ref3
    (`kings/delegate/out/K23/verify/ref3.cpp`, which shares no code with kpsolve or kp_p; for flat boards pass
    `--board flat7x6`, a parsing quirk) give the same 8 root values and the same move lists, as re-run by the integrator.
  - *Contexts. COMPUTED-1 (the referee's kpp run), prediction CHECKED-2.* The P-result of G ⊞ Z_B equals the prediction
    r(G ⊞ dud_D) at every root, all outcome pairs included, in: the 68 contexts with ≤ 3 pawns on files f, g (544 roots),
    the 12 representative contexts on files e–g (96 roots), and the first 660 of the 885 contexts with ≤ 2 + 2 pawns on
    files f, g (5,280 roots): 0 contexts and 0 roots differ. 225 of the 885 contexts are untested. Z_A on the same 885
    contexts differs in 58.
  - *The bridge on Z_B. COMPUTED-1* (the referee's `vbridge2.py`, 68 f/g contexts). (Pun_White) holds at all regular
    positions in 19 contexts, (Pun_Black) in 15, both in 7; no context has a mismatch. Theorem 3.2‴(a): 160 instances, (b):
    56 instances, 0 failures.
  - *Chess. Undecided.* In chess with cap 1 the bounds at the 8 roots of Z_B alone are (W, L): the capped promotions are
    met and cap 1 does not decide. Whether Z_B is exactly two-shuttle in chess is open (cap 2 not run, memory), and so is
    every chess result beside contexts.
  - *CONJECTURE* that Z_B is exactly two-shuttle in P in every context. Not proved: (Pun) is a per-context fact, and 225
    of the 885 contexts are untested. It is open on the cylinder and on other boards.
- **K14's first search (superseded by Z_B). COMPUTED-1 as a record of what the script did, not as a negative result.**
  `scripts/search_groups.py` lists every placement of the kings and of pawns on F_Z in which the four combined king states
  are legal (K1, K2: kings with two adjacent safe squares each, never touching) and the number of other legal moves in the
  four states is at most 18 (12 for ≤ 3 + 3 pawns on three files). It listed 6,674 groups (flat 7×6, flat 7×7, cylinder
  7×6), 1,147 of them (D, D) at all 8 roots with Z alone, and found none with every non-shuttle move losing at once. **The
  cut-off excluded Z_B:** with the cut-off raised to 40 the script lists Z_B, which has score 26. The statement "no exactly
  frozen group in this family" is therefore false for flat 7×6. The script's statements for the 7×7 board and the 7×6
  cylinder (including "the minimum is 12" and "none comes close") depend on the same cut-off, were not repeated without
  it, and are not claimed.

## 6. Testable predictions
>>>>>>> NEW

### EDIT section 7: downgraded dud claim
<<<<<<< OLD
- "A dud group exists in small K+P positions": now a CONJECTURE.
=======
- "A dud group exists in small K+P positions": now a CONJECTURE. (After K14 and its referee, 2026-10-27: Z_B of §5.7
  has every non-shuttle move losing at once in P, CHECKED-2, and equals dud_D beside every context tested, COMPUTED-1;
  Z_A is dud-type up to one White break. Chess (cap 2), the cylinder and other boards are open.)
>>>>>>> NEW

### EDIT section 7 item 8: the 2-cycle bisimulation
<<<<<<< OLD
   - The bisimulation in Proposition 3.2 needs *both* shuttle states to have identical properties.
=======
   - The bisimulation in Proposition 3.2 needs *both* shuttle states to have identical properties. For two shuttles
     (Proposition 3.2′) it needs all four combined states, with both shuttles legal in each; deleting any one of the
     eight arrows changes the result (Proposition 3.2′(d)), and the kings' opposition, a missing diagonal state, gives
     (W, L) instead of (D, D).
>>>>>>> NEW

### EDIT section 8 item 2: dud groups
<<<<<<< OLD
2. Do both-sides-shuttle (dud) groups exist without a pawn break on the cylinder? Do over-groups exist? Both
   need wider searches.
=======
2. Do both-sides-shuttle (dud) groups exist without a pawn break on the cylinder? Do over-groups exist? Both
   need wider searches. (After K14 and its referee, 2026-10-27: on the flat 7×6 board Z_B of §5.7 has every non-shuttle
   move losing at once in P, CHECKED-2; a search of flat 7×6 (F_Z = {a, b, c}, ≤ 2 + 2 pawns, no cut-off) found exactly
   two such placements, mirror images, among 817,270, COMPUTED-1. Beside every context tested its P-result equals that of
   dud_D (COMPUTED-1; 225 of 885 contexts untested). K14's own search had a move-count cut-off (18), which excluded Z_B,
   so its negative statements are withdrawn. Open: chess (cap 2; cap 1 gives bounds (W, L)), the cylinder, other
   boards.)
>>>>>>> NEW

### EDIT appendix A: no dud group
<<<<<<< OLD
  - no dud and no over group.
=======
  - no dud and no over group. (This scratch search covered the cylinders only. K14 repeated the dud search on the 7×6
    cylinder and the flat 7×6 and 7×7 boards with kpsolve as the filter, with a move-count cut-off (18), which excluded
    Z_B (§5.7); its negative result is withdrawn. A search of flat 7×6 without the cut-off found Z_B.)
>>>>>>> NEW
