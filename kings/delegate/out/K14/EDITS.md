# K14 proposed edits to kings/theory/LOOPY.md

Each block replaces its OLD text (which occurs exactly once in the current LOOPY.md) by its NEW text.

### EDIT status row: shuttles on both sides
<<<<<<< OLD
| §3, shuttles on both sides | CONJECTURE: needs a two-sided Proposition 3.2 | R4 item 6 |
=======
| P3.2′ (two shuttling kings are a dud) | D-model: PROVED (new, K14, 2026-10-27): a p-morphism onto dud_D on the four combined king states, for every D-game G; inequalities when one side has further Z-moves; a win needs only the half of the states in which the winner's king stands still; all eight shuttle arrows are needed (counterexamples); brute force on random games, 0 violations. Chess bridge (Theorem 3.2‴): PROVED, conditional on (V1a-ctx), (V2-ctx) and the per-group hypothesis (Pun) that every non-shuttle Z-move is decisively punished; stalemate is excluded automatically. Existence: Z_A (§5.7, flat 7×6) is a two-shuttle group up to one White break (Kxb4 in one state): COMPUTED-1 in P. An exactly frozen group was not found in a search of 6,674 four-state-legal groups (flat 7×6 and 7×7, 7×6 cylinder; ≤ 2 + 2 pawns, partly ≤ 3 + 3): CONJECTURE that none exists in that family | R4 item 6; K14 |
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
- **With shuttles on both sides (PROVED in the D-model by Proposition 3.2′; revised after K14, 2026-10-27):** for a
  component with four combined king states, each side's shuttle an option and every other option a suicide, all tempo
  content disappears. A position in which neither side can force a decisive event against a passing opponent is a
  draw even where the convention predicts a clear winner, and a side wins iff it can (Theorem 3.4(a), through
  Proposition 3.2′). The chess bridge is Theorem 3.2‴. It needs, per group and context, that every non-shuttle Z-move
  is decisively punished; a win needs this only for the loser and only in the two states in which the winner's king
  stands still. The 7.3 group is **not** of this type: f7–f8=Q is a White Z-move that is no suicide (§5.3). Whether an
  exactly frozen two-shuttle chess group exists is open (§8, item 2); the best group found, Z_A (§5.7), has one White
  break.
>>>>>>> NEW

### EDIT section 3: Proposition 3.2prime and its chess bridge
<<<<<<< OLD
**Literature (KNOWN, as summarised in [notes/lit_cgt_chess.md](../../notes/lit_cgt_chess.md)).**
=======
**Proposition 3.2′ (two shuttling kings are a dud). PROVED (new, K14, 2026-10-27; the D-model part is one model's proof,
not yet independently re-derived, plus a brute-force check).**

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
  - Brute force (K14, `scripts/prop_check.py`, 400 random short G with 3 to 6 positions): deleting any one of the
    eight shuttle arrows from an otherwise exact Z changes the result in about 72 % of the (G, state, side) instances.

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

*(Remark on e.p.)* The sum of Definition 1.3 leaves G alone under a Z-move, and in chess an e.p. right expires under a
king move. Model the flag as a coordinate of G that every Z-move resets, and the pass of dud_D likewise. Lemmas A and B and
all of the above go through unchanged (φ forgets only the Z-state, and both games reset the flag at corresponding moves).
The chess statements below use this reading.

**Remark 3.2′a (what it says about the conjecture).** A two-shuttle component realises dud_D, so the "shuttles on both
sides" bullet above is PROVED in the D-model for every component that satisfies (T1)–(T4). Whether a chess king group
does is a separate question, answered by the hypotheses of Theorem 3.2‴ below and, for a concrete group, by a search.

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
  is faster than the punishment (Proposition 2.10(b)). It is the one remaining gap of the bridge: no theorem here gives
  it for a concrete group in all contexts. Theorem 2.7 and Proposition 2.10(a) give it in P for punishments of depth
  T = 1 under their side conditions.

**Checks of Proposition 3.2′ and Theorem 3.2‴ (K14; data, not proofs).**
- *D-model, brute force* (`kings/delegate/out/K14/scripts/prop_check.py 400`): 400 random short D-games G (3 to 6 positions,
  random options including ⊕, ⊖), each with random components Z of the kinds "exact (T1)–(T4) with extra suicides",
  "(T1), (T2), (T4) plus random further White options", the mirror, and (c)'s half-slice, solved by least fixed point on the
  explicit sum. (a): 44,208 of 44,208 instances agree. (b): 44,208 of 44,208 for each of the two inequalities. (c): 4,980 of
  4,980. Deleting any one of the eight arrows changes the result in 72–73 % of the instances (COMPUTED-1: the solver is
  new and one implementation; the statements are PROVED above).
- *Predictions for pawn-only contexts:* the least-fixed-point solver `scripts/dmodel.py` and the closed recursion of
  Theorem 3.4(a) (`scripts/closed_form.py`, a pass resets the e.p. flag) agree on all 4,579 contexts of ≤ 2 + 2 pawns on
  files e–g of the flat 7×6 board (two implementations: CHECKED-2).
- *Chess, a concrete group:* §5.7 (Z_A). Theorem 3.2‴(a), 200 instances with (Pun) at all regular positions and r_D = W
  (resp. L), 0 failures; part (b), 16 instances, 0 failures; COMPUTED-1 in P.

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
- **Without the pawn break (revised after K14, 2026-10-27).** Z₇.₃ itself is not a two-shuttle component: f7–f8=Q is
  a White Z-move that is no suicide, so (T3) of Proposition 3.2′ fails and part (b) gives only r(G ⊞ Z₇.₃) ≥
  r(G ⊞ dud_D), the trivial bound here. The four combined king states are legal (the kings keep distance ≥ 2 in all
  four), so the geometry of Lemma 3.2″ holds. "If f8 were unavailable" does not define a group: (T3) and (T4) would
  also have to hold for g7–g6, g7–g5 and the king moves, which in Z₇.₃ lose only because of f8=Q. The earlier sentence
  "would be dud-type" is withdrawn as unproved. The two-sided proposition it needed is now Proposition 3.2′ (PROVED),
  and a concrete group that is two-shuttle up to one White break is Z_A of §5.7.
  - *Scratch evidence:* no both-sides-shuttle group without a pawn break exists among 3-file groups with
    ≤ 2 + 2 pawns and no passer on the 8×6 cylinder. K14 repeated the search with kpsolve as the filter (§5.7): none
    with every non-shuttle move losing at once, on the 7×6 cylinder or the flat boards 7×6, 7×7 (CONJECTURE).
>>>>>>> NEW

### EDIT section 5.7 (new): a two-shuttle group
<<<<<<< OLD
## 6. Testable predictions
=======
### 5.7 A two-shuttle group (K14, 2026-10-27)

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
  zugzwang), both in 1. Predicted W or L was never contradicted. Example f2 / f3 (blocked, so G has no move): the prediction is (D, D), but Black to move at (a5, c5) must
  shuttle to c6, and Kxb4 then wins; four of the eight roots are W. With the context on files e–g (closer to the sortie
  squares) 5 of 12 representative contexts fail (24 of 96 roots).
- **Chess (C) for Z_A. Mostly not done.** In chess (`kpsolve --board flat:7x6 --ep on --promote QRBN --cap 1`) Z_A alone
  is (D, D) at all 8 roots, exact (COMPUTED-1, 1.4 CPU-s). The chess results with contexts were not computed: a batch of 4
  contexts was still running after one CPU-minute and was stopped, and the shared heavy slots were queued behind other
  jobs. So (A_Q) is not checked for any context, and every context result above is a statement in P.
- **The bridge on Z_A. COMPUTED-1.** `scripts/bridge_check.py` enumerates the regular positions of each context (8 to
  about 330) and classifies every legal move as context move, shuttle or other. (Pun_White) holds at all regular positions
  in 14 of the 68 contexts, (Pun_Black) in 17, both in 2. Theorem 3.2‴(a): at the 200 roots where (Pun) for the loser holds
  everywhere and r_D = W (resp. L) for the winner, P agrees: 0 failures. Theorem 3.2‴(b): 16 roots with both (Pun)'s, 0
  failures. All 15 mismatching contexts have a (Pun) failure: 0 contexts where the hypotheses hold and the conclusion
  fails. (Pun) is sufficient, not necessary: many of the 53 matching contexts have a (Pun) failure at some regular position
  that the winner's play never uses.
- **Search for an exactly frozen two-shuttle group. Negative result, COMPUTED-1.** `scripts/search_groups.py` lists every
  placement of the kings and of pawns on F_Z in which the four combined king states are legal (K1, K2: kings with two
  adjacent safe squares each, never touching) and the number of other legal moves in the four states is at most 18
  (12 for ≤ 3 + 3 pawns on three files). 6,674 groups: flat 7×6 (F_Z of 3 files, ≤ 2 + 2 and ≤ 3 + 3 pawns; F_Z of 2 files,
  ≤ 3 + 3), flat 7×7 (≤ 2 + 2), cylinder 7×6 (≤ 2 + 2). 1,147 of them are (D, D) at all 8 roots with Z alone (P model),
  and **none** has every non-shuttle move losing at once, which is a necessary condition for (T3), (T4) in P. The
  minimum number of non-losing non-shuttle moves (over the 8 roots) is 1: it is attained only by Z_A (flat 7×6), its
  colour-reversed mirror, a variant with an extra immobile White pawn on b2, and the corresponding groups on the 7×7 board. On the
  cylinder 7×6 only 6 groups are drawn at all 8 roots and the minimum is 12. So an exactly frozen two-shuttle group is not
  known: CONJECTURE that none exists in this family (one search, one solver, scored by a cut-off on the other-move count).

## 6. Testable predictions
>>>>>>> NEW

### EDIT section 7: downgraded dud claim
<<<<<<< OLD
- "A dud group exists in small K+P positions": now a CONJECTURE.
=======
- "A dud group exists in small K+P positions": now a CONJECTURE. (After K14: Z_A of §5.7 is dud-type up to one White
  break, COMPUTED-1 in P; an exactly frozen two-shuttle group is still unknown.)
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
   need wider searches. (K14: on the flat boards 7×6 and 7×7 a group exists that is two-shuttle up to one White break,
   Z_A of §5.7; among 6,674 four-state-legal groups none has every non-shuttle move losing at once, and on the 7×6
   cylinder none comes close. Open: an exactly frozen group, on any board.)
>>>>>>> NEW

### EDIT appendix A: no dud group
<<<<<<< OLD
  - no dud and no over group.
=======
  - no dud and no over group. (K14 repeated the dud search on the 7×6 cylinder and the flat 7×6 and 7×7 boards with
    kpsolve as the filter: §5.7.)
>>>>>>> NEW
