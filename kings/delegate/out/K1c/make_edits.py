"""Generate kings/delegate/out/K1c/EDITS.md (K1c part: LOOPY.md sections 3-6 and Appendix A).

The OLD blocks are copied verbatim from kings/theory/LOOPY.md by line range, so they are
byte-exact. The script refuses to write the file if an OLD block is not unique in the note.
"""
import sys

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
SRC = ROOT + "/kings/theory/LOOPY.md"
OUT = ROOT + "/kings/delegate/out/K1c/EDITS.md"

text = open(SRC, encoding="utf-8").read()
lines = text.split("\n")


def old(a, b):
    """Lines a..b inclusive, 1-based, copied verbatim from the note."""
    return "\n".join(lines[a - 1:b])


EDITS = []


def E(label, a, b, new):
    EDITS.append((label, old(a, b), new))


# ---------------------------------------------------------------- section 3
E("R4 item 7", 617, 623, r"""**Chess bridge** (PROVED after repair, by the proof of Theorem 1.14 with (V1a) added).
Suppose r(G ⊞ on_D) = W, White plays that strategy (shuttling for its passes), and along it:
- (V1a) every legal chess move of the side to move is one of the D-options of the D-model, and leads to the
  matching position;
- every Black Z-move is decisively punished in P;
- every decisive event of G that is reached is a P-win for its beneficiary;
- Black always has a legal move.

Then White wins in P. *Proof:* the proof of Theorem 1.14(i), with (V1a) among the hypotheses — (V1a) makes
the D-play a chess play, the shuttling strategy supplies White's passes, and the last two bullets make every
deviation decisive for Black. The mirror statement holds for Black wins.
(Revised after review: R4 item 7: the bridge needs (V1a). It fails in P2 + H\* if White plays e3–e4, which
stalemates Black, so the bridge may only be used along a strategy that avoids that move; kpsolve gives (W, W)
for P2 + H\*.)""")

E("R4 item 6", 692, 698, r"""**What loopy kings do to the convention.**
- **With a White shuttle (PROVED by Theorem 3.4(b)):** the components' values (numbers, infinitesimals, nimbers)
  are irrelevant except for Black's forcing threats. White cannot be zugzwanged, and Black loses as soon as its
  context tempo runs out.
- **With shuttles on both sides (CONJECTURE):** all tempo content should disappear. Positions without threats
  should be draws, even where the convention predicts a clear winner. The 7.3 group would be of this type if
  its pawn could not promote (§5.3). *To settle:* a two-sided Proposition 3.2 — a bisimulation on the four
  combined king states, in each of which each side's shuttle is legal and each side is frozen — followed by
  Theorem 3.4(a). (Revised after review: R4 item 6: Theorem 3.4 is stated for one reservoir, so this bullet
  was not proved by it.)""")

# ---------------------------------------------------------------- section 4
E("R4 item 3", 719, 723, r"""**Theorem 4.2 (finite versus loopy tempo). PROVED after repair** (each part is proved
below).
- **(a)** Let G be short, and let R_n^W have no Black options (Black's suicides are deleted first; see (b)).
  Then G ⊞ R_n^W behaves as "White has n one-shot passes", and its BIG translation G^B + n gives the right
  outcome when G ⊞ R_n^W is first-event dominant. A sufficient condition is pairwise safety in G ⊞ R_n^W
  together with B > n + max(M_L(G), M_R(G)), with the threats counted by the corrected τ of Definition 1.10
  (revised: τ counts moves into ⊕ or ⊖ by *either* player).
  *Proof:* Theorem 1.11(a) and (b), with the corrected τ. R_n has no Black options, so it carries no threat at
  all, τ(R_n) = ∅, and pairwise safety in G ⊞ R_n^W follows from pairwise safety in G. Its n Left moves
  enter M_L, so max(M_L(G ⊞ R_n^W), M_R(G ⊞ R_n^W)) ≤ max(M_L(G), M_R(G)) + n < B, which is the bound (b)
  needs, and Theorem 1.11(b) then gives first-event dominance. (Revised after review: R4 item 3: Definition
  4.1 allowed Black suicides inside R_n, and then the stated hypothesis does *not* give first-event
  dominance — take a context whose only option is Black's move to ⊖, whose translation is −B−1, with n = 1 and
  a Black suicide at ρ₁: the frontier is B + (−B−1) = −1 ∈ 𝓡, so dominance fails for every B. The corrected
  τ counts that suicide, so the hypothesis correctly fails there; with no Black options the proof above is
  complete.)""")

E("R4 item 4", 724, 728, r"""- **(b)** If White's safe Z-moves form an acyclic graph and all Black Z-moves are suicides, then
  Z, with Black's suicides deleted, is equivalent in the D-model to R_ℓ^W, where ℓ is the length of the
  longest path of safe White moves; and in CGT, for B > ℓ, its BIG translation is the integer ℓ.
  *Proof:* induction on the number of White options, using {m₁, …, m_k | } = max m_i + 1: the value of a
  White-only option set is 1 plus the maximum of the values of its options, and dominated options can be
  deleted (KNOWN, [WW] ch. 2, [S] ch. II). In the D-model the deletion of Black's suicides is Lemma 1.7, a
  statement about results; the CGT statement needs the extra hypothesis B > ℓ, because {i−1 | B} = i holds
  only for B > i. (Revised after review: R4 item 4: Lemma 1.7 alone does not give the CGT equality, and the
  D-model equivalence to R_ℓ was not proved; both are now proved, and the CGT form carries B > ℓ.)""")

E("R4 item 5", 729, 735, r"""- **(c)** A reservoir with a White 2-cycle is on_D and equals no integer. *Proof:* take G = R_{n+1}^B, n + 1
  Black tempi with no threats.
  - G ⊞ R_n^W with White to move is L: the tempi run out on White first.
  - G ⊞ on_D with White to move is W: Black runs out.
  - on_D is not a number at all, so it differs from every integer, negative ones included.
  - The identification needs the hypotheses of Proposition 3.2 — the cycle must be reachable, and in each of
    its two states every Black Z-move must be a suicide — not merely the existence of a cycle.
  (Revised after review: R4 item 5: separating on_D from the integers has to cover the negative integers as
  well, and "is on_D" needs Proposition 3.2's hypotheses.)

So a group's tempo is *finite* (a stopper equal to an integer) exactly when its safe spare moves form an
**acyclic** graph, and *unbounded* (on or off) when they contain a cycle. The word is "acyclic", not
"non-reversible": a 3-cycle has no immediately reversible move and is still unbounded.
(Revised after review: R4 item 5: the old sentence conflated acyclicity with the absence of a 2-cycle.)""")

E("R4 items 1 and 2", 737, 740, r"""**Proposition 4.3 (no finite king tempo in isolated K+P groups). FALSE as originally stated →
repaired.** Let Z be a king group in a position without officers, with a buffer. Suppose side s plays a
non-capturing king move u → v inside F_Z, and the opponent replies outside Z. **As stated this is false:** the
step back fails if s was in check on u, or if the reply promotes. The repaired statement adds two hypotheses:
- (H1) s is not in check on u;
- (H2) the reply is not a promotion, and does not attack u.

Then v → u is legal at s's next turn and restores Z exactly.""")

E("R4 item 2, R1 item 11", 741, 743, r"""**Consequences, with the scope narrowed (revised after review: R4 item 2, R1 item 11).** Call a king step
u → v inside F_Z *safe* if (H1) and (H2) hold and the opponent is frozen — all its Z-moves are suicides — at
both u and v. Then one safe step gives s an unlimited supply of passes: s returns to u on its next turn, the
Z-state is exactly as before, and the step can be repeated. So, among king steps *inside* F_Z, the tempo of a
pure reservoir is 0 (the opponent is frozen and s has no safe step) or ∞ (s has a safe step); it is never a
finite n ≥ 1. Three caveats, which the original wording hid:
- the dichotomy covers king steps inside F_Z only. A step onto a buffer file can be taken away later by a
  context pawn (Lemma 2.2 lets context pawns attack buffer squares), so such a supply depends on the context
  and is neither 0 nor ∞;
- a king move can be neither a suicide nor a pass: it can unfreeze the opponent without losing (§5.5 shows
  this), so the dichotomy is about pure reservoirs only;
- "safe" is not "any legal step": the opponent must be frozen at the new state v as well as at u.""")

E("R4 items 1 and 2", 745, 750, r"""*Proof.*
- u is empty, since s's king just left it and the opponent did not move in Z.
- u is not adjacent to the opponent's king: by (H1) the opponent's king was not adjacent to u when s's king
  stood there (kings may never be adjacent), and by (H2) the reply did not move it next to u.
- u is not attacked by an opponent Z-pawn, since none has moved (by (H2) the reply is not a promotion), and by
  (H1) none attacked u before. It is not attacked by a context pawn either: context pawns attack only context
  and buffer squares (Lemma 2.2), and u ∈ F_Z.
- With no sliders, the move exposes nothing. ∎

*Counterexample to the original statement (revised after review: R4 item 1).* `Kb2 Pc2 kc4 pc3`, White to
move, on flat:4x4: White is in check from pc3 and plays Kb2–a1; when Black then moves outside Z, Kb2 is
illegal, because pc3 still attacks it. The position is hand-checkable; kpsolve confirms the move lists:
only Ka1a2 and Ka1b1 are legal for `Ka1 Pc2 kc4 pc3 w -`. The step back fails because u was attacked, not
because the opponent moved.
  - Reproduce: `printf 'Kb2 Pc2 kc4 pc3 w -\nKa1 Pc2 kc4 pc3 w -\n'
    | kings/kpsolve --board flat:4x4 --ep on --promote QRBN --cap 1 --moves`.""")

E("R4 item 2, R1 item 11", 752, 754, r"""**What this means for the "n safe spare moves" picture.** In king-and-pawn chess, a king with exactly n safe
spare moves cannot occur in an isolated group *for steps inside F_Z*: one safe step and the step back already
give infinitely many (Proposition 4.3, repaired). Steps out of F_Z are the exception, and their supply depends
on the context. (Revised after review: R4 item 2, R1 item 11: the original sentence claimed more than
Proposition 4.3 proves.)""")

E("R1 item 11", 760, 761, r"""**Definition 4.4 (over).** over = {0 | over} (KNOWN, [WW] ch. 11, [S] ch. VI). Right can pass forever
(over → over), and Left has one move, to 0, that ends Right's passing. (Revised after review: R1 item 11: the
note had no item 4.4, so the numbering jumped from 4.3 to 4.5; this paragraph is now Definition 4.4.)""")

E("R4 item 8", 784, 786, r"""**Chess reading of over.**
- Black has a safe king shuttle (endless passes), and White has exactly one move that takes away a shuttle
  square and leaves a mutual zugzwang. That move is typically a pawn move, but not by Proposition 4.3:
  Proposition 4.3 assumes a frozen opponent that replies outside Z, and in an over-group the opponent
  shuttles inside Z. (Revised after review: R4 item 8.)""")

E("R1 item 10, R4 item 8", 789, 791, r"""- **CONJECTURE 4.7:** no over-type group with ≤ 2 + 2 pawns fits on 3 files of the 8×6 cylinder, but over
  is realisable on the cylinder with wider groups. *Scratch evidence:* the first half; a geometric search over
  placements of ≤ 2 + 2 pawns on 3 (or 4) files found none (Appendix A). *To settle:* a wider search, then
  kpsolve. (Revised after review: R1 item 10, R4 item 8: the search described in Appendix A covered ≤ 2 + 2
  pawns, not the ≤ 3 + 2 claimed here; the conjecture is restated for what was actually searched.)""")

# ---------------------------------------------------------------- section 5
E("R1 item 11, R4 item 9", 809, 809, r"""- **Frozen in the convention. PROVED by enumeration** (revised after review: R1 item 11, R4 item 9: the
  proof is written out here, instead of being left to the diagram audit). The group is WK h5, WP a4, BK b4,
  BP a5 on the 8-file cylinder. WK's five legal moves are Kg4, Kg5, Kg6, Kh6 and Ka6; each of them abandons
  WP a4, which Black's king then captures on a4, giving Black a passer. BK's five legal moves are Ka3, Kc3,
  Kc4, Kc5 and Kb5; the first four abandon BP a5, which White's king then captures on a5, giving White a
  passer, and the fifth (Kb5) puts Black's king on the square that guards both a4 and a5, so that White is in
  zugzwang with only pawn-blocked moves left. So every king move in the group is decisively punished, and the
  group is frozen. The enumeration agrees with `notes/diagram_audit.md` §C.3.""")

E("R4 item 9, R1 item 11", 836, 841, r"""- **White's sorties: the certificate fails. PROVED by Lemma 2.9.** (The heading "White's sorties are not
  punished" stated as fact what is proved only as the failure of the certificate.)
  - Ke5 already stands on the e-pawn's path. Kd5 and Kf5 reach e5 next move: after ...Kxd7, e5 is not
    adjacent to d7 and not attacked by e7.
  - By Lemma 2.9, (L1) fails for these three sorties. PROVED.
  - That the three sorties are *not punished* in P (no forced promotion for Black) rests on scratch evidence
    only, and is a CONJECTURE (revised after review: R4 item 9, R1 item 11): even without passes, Black cannot
    force promotion after Kd5, Ke5 or Kf5. Only Kf7 loses, in 10 moves. In chess, kpsolve gives (D, W) for the
    6-rank analogue Z_72 bare, so White to move draws (P5).""")

E("R4 item 6", 869, 872, r"""- **Without the pawn break. CONJECTURE** (revised after review: R4 item 6): if f8 were unavailable, the
  group would be a both-sides shuttle (dud-type), and Theorem 3.4(a) would make every threat-free sum a draw —
  but that needs a two-sided Proposition 3.2, which is not proved: the bisimulation must hold on the four
  combined king states, in each of which each side's shuttle is legal and each side is frozen.
  - *Scratch evidence:* no both-sides-shuttle group without a pawn break exists among 3-file groups with
    ≤ 2 + 2 pawns and no passer on the 8×6 cylinder. dud may not occur in small K+P groups (CONJECTURE).""")

E("R1 item 11", 893, 895, r"""- **So Z_onT1 realises `on`. PROVED in P** (revised after review: R1 item 11: the claim carried no label).
  By Proposition 3.2, its chess bridge and Proposition 2.10(a), Theorem 3.4(b) applies in every non-terminal
  context that leaves d5 legal and leaves Black a legal move after Kxb5. Black loses unless it has a forced
  decisive event against a passing White. Predictions P2 and P10; in chess the conclusion needs (A_Q), which
  is checked position by position (kpsolve: (W, W) for all ten P2 and P10 positions).""")

E("R1 items 10 and 11, R4 item 9", 914, 917, r"""- **It passes the convention's test. PROVED by enumeration.** Every Black king move drops b3, after which
  White has a passer and Black none, and White's king shuttles a3 ↔ a4.
- **But Black has an escape. CONJECTURE (scratch evidence; kpsolve agrees).** After the sortie Kc5 and Kxb3,
  White cannot force promotion even without passes; after Kd4 and Kd5, White wins only if Black has no spare
  move. Black's legal moves in the group are Kc5, Kd4, Kd5 and Kd3 (revised after review: R1 item 10 — Kd3
  was missing from the original list; Kc3 is illegal because White's pawn b2 attacks c3), and kpsolve confirms
  that the escape is exactly Kc5: `Ka4 Pb2 kc5 pb3 w -` is (D, D) — a draw, with or without the passes — while
  `Ka4 Pb2 kd3 pb3 w -`, `Ka4 Pb2 kd4 pb3 w -` and `Ka4 Pb2 kd5 pb3 w -` are (W, W).
  - Reproduce: `printf 'Ka4 Pb2 kc5 pb3 w -\nKa4 Pb2 kd3 pb3 w -\nKa4 Pb2 kd4 pb3 w -\nKa4 Pb2 kd5 pb3 w -\n'
    | kings/kpsolve --board cyl:8x6 --ep on --promote QRBN --cap 1 --moves`.""")

E("R1 item 11", 928, 930, r"""  - Our count gives μ_W = 5: the c-pawn walks c4–c8 while Black is busy. **PROVED by count** (revised after
    review: R1 item 11: this chain carried no labels).
  - Black's local win after Ke6 Kxg4 takes T = 5 (scratch). **CONJECTURE** (scratch evidence).
  - So μ = T, and (L2) fails by one tempo. **CONJECTURE** (scratch evidence; Review 4 re-derived both
    numbers independently: μ = 5 = T, so (L2) does fail by one tempo — R4 item 10).""")

# ---------------------------------------------------------------- section 6
E("R1 item 5, PREDICTIONS.md", 940, 944, r"""kpsolve options: `--ep on --promote QRBN --cap 1`, and `--cap 2` for the three P4 rows whose cap-1 bounds
differed. Positions use the format of `kings/SPEC.md`; append ` w -` or ` b -`. Each row gives:
- the predicted result pair (w, b), W/D/L from White's view;
- the Z = 0 convention pair (king group read as 0, H valued by `cylcgt` on its strip);
- the pair kpsolve computes in chess (C), from `kings/results/PREDICTIONS.md`;
- the theorem behind the prediction, and its label.

Reproduce the kpsolve column with `kings/kpsolve --board cyl:7x6 --ep on --promote QRBN --cap 1` on the
positions of the rows (and `--board cyl:8x6` for P10, `--cap 2` for the three P4 rows); the raw runs are in
`kings/results/theory_predictions_raw.txt` and `kings/results/theory_P4_cap2.txt`.""")

# rows are lines 958..970; column 5 (Naive convention) is followed by the new kpsolve column


def rebuild(lineno, kpsolve, family=None, basis=None, label=None):
    """Rebuild one table row with the kpsolve column inserted after the 'Z = 0 convention' column."""
    parts = [p.strip() for p in lines[lineno - 1].split("|")]
    assert len(parts) == 9, (lineno, parts)
    parts = parts[:6] + [kpsolve] + parts[6:]
    if family is not None:
        parts[3] = family
    if basis is not None:
        parts[7] = basis
    if label is not None:
        parts[8] = label
    return "| " + " | ".join(parts[1:-1]) + " |"


E("PREDICTIONS.md (kpsolve column)", 956, 957,
  r"""| # | Board | Position family | Predicted (w, b) | Z = 0 convention | kpsolve (C) | Basis | Label |
|---|---|---|---|---|---|---|---|""")

E("PREDICTIONS.md (kpsolve column)", 958, 962, "\n".join([
    rebuild(958, "(D, D)", label="PROVED; kpsolve agrees"),
    rebuild(959, "(D, D)", label="PROVED; kpsolve agrees"),
    rebuild(960, "(W, W) in all five",
            label="PROVED in P; C modulo (A_Q); kpsolve agrees on all ten"),
    rebuild(961, "(L, L) in all five",
            label="PROVED in P; C modulo (A_Q); kpsolve agrees on all ten"),
    rebuild(962, "(L,W), (L,L), (W,W), (D,L), (D,L), (L,D)",
            label="CONJECTURE → **refuted** by kpsolve in 3 of 6 contexts (H\\*, H\\*2, H0)"),
]))

E("PREDICTIONS.md (kpsolve column)", 963, 966, "\n".join([
    rebuild(963, "bare (D, W); + Hp1 (W, W)",
            label="all entries PROVED in P except the bare w-entry, which is a CONJECTURE (scratch: no "
                  "forced promotion); kpsolve agrees on all four entries"),
    rebuild(964, "not run", label="CONJECTURE (not run on 8×8)"),
    rebuild(965, "not run", label="b PROVED in P; w CONJECTURE (not run on 8×8)"),
    rebuild(966, "6-rank analogue (W, W); 8×8 not run", label="PROVED in P"),
]))

E("PREDICTIONS.md (kpsolve column)", 967, 970, "\n".join([
    rebuild(967, "(W, L)", label="PROVED in P; kpsolve agrees"),
    rebuild(968, "(W, W) for k = 0, 1, 2", label="PROVED in P; kpsolve agrees for k = 0, 1, 2"),
    rebuild(969, "— (a harness check, not one position)",
            family="Kings parked on the a-file (`Ka1 ka6`, b- and h-files empty); pawn components on c–g; "
                   "every passer and race node speed-certified (Remark 2.11 with frozen kings); condition (E). "
                   "Here W(X) is the D-game of X with its own winning side, and \"hereditarily sum-safe\" "
                   "(HSS) means that every component of X is itself sum-safe in the sense of Theorem 1.14(ii)"),
    rebuild(970, "— (a harness check, not one position)",
            label="PROVED (implication), restricted to the nodes where `--frozen` reports a win"),
]))

E("R4 item 7", 973, 977, r"""- **What P2, P3 and P10 prove.** The derivations use only enumerated move lists (§5.4) and Theorem 3.4(b).
  The one-move punishment holds in every context listed, except where a context pawn covers the king's escape
  square d5 (respectively d2) — and that happens only after the *winning* side has moved its own pawn there:
  - In H\*, White's single step e3–e4 covers d5 and **stalemates Black**: kpsolve scores it a draw, so White
    must avoid it and play the shuttle (Ka6). (Revised after review: R4 item 7: the old sentence "none of them
    puts a pawn on e4 … that would cover d5" was wrong for H\*, where the pawn moves there during the window.)
  - In H\*2, White's double step e2–e4 *would* stalemate Black. In P3's H\*2, Black's double step e5–e3 would
    stalemate White. The winner simply never plays it.""")

E("R1 item 6", 978, 979, r"""- **Scratch confirmation in P.** A scratch P-model solver (no e.p.; queen safety required — a stricter P
  than Definition 1.5's, which counts any promotion as a win) reproduced every P-level entry of P1, P2, P3,
  P5, P9 and P10 that it finished:""")

E("R1 item 5, PREDICTIONS.md", 989, 992, r"""- **What separates the theory from the conventions (revised after review: R1 item 5).** The old headline — "P2,
  P3 and P10 are the decisive tests of the loopy theory" — did not say which baseline it used. Against the
  note's own "Z = 0" reading (king group = 0, the context valued by cylcgt on its strip) it is right: that
  reading gets 17 of the 26 P2/P3/P10 entries wrong, and at least one of the two results in every one of the
  13 positions. Against the *literal* convention it is not: on the actual pawn sets, `cylcgt.pawns.value`
  returns +BIG for every P2 and P10 position and −BIG for every P3 position, so literal cylcgt gets all 26
  entries right and does **not** separate the theory from cylcgt. The positions that do separate them are P1
  (the stalemate trap: both readings say (W, W) and (L, L), the truth is (D, D)), P5 and P7 (the literal
  reading has no answer — it scores a race at move 0 on the 6-rank analogue — while kpsolve settles P5 bare as
  (D, W)), P9 (both readings predict (W, W), the truth is (W, L)) and P4 (below). Over the 25 exactly
  determined predictions of `kings/results/PREDICTIONS.md`, the theory holds in 22 and literal cylcgt in 16;
  the three positions literal cylcgt scores as a race (P5 bare, P5 + Hp1, P8 6-rank) have no answer from it
  at all.
- **What P4 tests, and how it failed.** P4 was the positive control: the theory predicts that the convention
  is *right* there. kpsolve refutes it in 3 of the 6 contexts.
  - H\* and H\*2 with White to move are draws, not (W, L). In H\* every White king move loses (Ka5, Kb5, Kg3,
    Kg4, Kg5) and White's only drawing move is e3–e4; in H\*2 the position is a draw as well.
  - H0 with Black to move is a draw, not (L, W): Black's king draws by Kd3 or Kd2.
  - The mechanism: the defending king walks to the locked context pawns and attacks the stuck pawn there
    (…Kd3, …Kd2, …Kd4). In H0 after …Kd3 the white king is confined to the a- and b-files: Kg4, Kg5 and Kg3
    all lose, while Ka5, Kb4 and Kb5 draw. This is what Proposition 2.10(b) predicts — the zero of the group is
    context-dependent, a CONJECTURE after Proposition 2.10(b), now supported in C by P4 — and the (L2) margin
    the theory assumed does not survive the context.
  - The same three contexts are exactly the ones in which the Z = 0 convention and literal cylcgt are wrong
    too, so the refutation is a fact about the positions, not about the convention.""")

# ---------------------------------------------------------------- appendix A
E("R1 item 10, R4 item 8", 1089, 1091, r"""- **Group search.** On the 8×6 and 7×6 cylinders: all placements of the kings and of ≤ 2 + 2 pawns on 3 (or 4)
  files, with no passer at the root. Each placement was classified as frozen, on, off, dud or over by one-ply
  tests. It found: (revised after review: R1 item 10, R4 item 8: the search covered ≤ 2 + 2 pawns, so every
  claim that depends on it is stated for ≤ 2 + 2 — Conjecture 4.7's "≤ 3 + 2" was wrong. The "no passer at the
  root" test is the note's own, not cylcgt's: cylcgt's passed test calls Z_onT1's c5 passed, so the search
  would have rejected Z_onT1.)""")

# ---------------------------------------------------------------- status rows
STATUS = r"""
## STATUS ROWS

| result | final label | one-line note with review item |
|---|---|---|
| T4.2(a) | PROVED after repair (through the corrected T1.11(b)) | R4 item 3: Black suicides inside R_n break the hypothesis; R_n must have no Black options |
| T4.2(b) | PROVED after repair (needs B > ℓ; the D-model equivalence is now proved) | R4 item 4: Lemma 1.7 is a D-result, not a CGT equality |
| T4.2(c) | PROVED after repair (negative integers; reachable cycle; "acyclic", not "non-reversible") | R4 item 5 |
| P4.3 | FALSE as originally stated (a king in check) → s not in check on u, reply not a promotion: PROVED after repair. The dichotomy "0 or ∞" is narrowed to steps inside F_Z with the opponent frozen at both ends | R4 items 1 and 2, R1 item 11 |
| D4.4 (over) | the numbering gap is filled | R1 item 11 |
| P4.5, P4.6 | PROVED | R4: sound |
| C4.7 | CONJECTURE, restated for ≤ 2 + 2 pawns (what was searched) | R1 item 10, R4 item 8 |
| §3, shuttles on both sides | CONJECTURE: needs a two-sided Proposition 3.2 | R4 item 6 |
| §3, Prop 3.2 chess bridge | PROVED after repair (adds (V1a)) | R4 item 7 |
| §4, "over" chess reading | the "typically a pawn move by Proposition 4.3" is withdrawn | R4 item 8 |
| §5.1, frozen | PROVED by enumeration, now written out | R1 item 11, R4 item 9 |
| §5.2, White's sorties | the certificate fails: PROVED (L2.9). "Not punished": CONJECTURE (scratch); in C, kpsolve confirms the 6-rank analogue (P5) | R4 item 9 |
| §5.4, Z_onT1 realises `on` | PROVED in P (label added) | R1 item 11 |
| §5.5 | CONJECTURE (scratch; kpsolve agrees): the escape is exactly Kc5 — (D, D) after …Kc5, (W, W) after …Kd3, …Kd4 and …Kd5. Kd3 added to the move list | R1 items 10 and 11, R4 item 9 |
| §5.6 | μ_W = 5: PROVED by count. T = 5 and "(L2) fails by one tempo": CONJECTURE (scratch; R4 re-derived both) | R1 item 11 |
| P1a, P1b (§6) | PROVED; kpsolve (D, D) | PREDICTIONS.md, as for every P-row |
| P2, P3 | PROVED in P; kpsolve agrees in C on all 10 positions; literal cylcgt also gets them right | R1 item 5 |
| P4 | CONJECTURE → **refuted** by kpsolve in 3 of 6 contexts (H*, H*2, H0) | PREDICTIONS.md, theory_P4_cap2_moves.txt |
| P5 | PROVED in P (b entries, + Hp1); bare w-entry CONJECTURE; kpsolve agrees on all four entries | — |
| P6, P7 | CONJECTURE, and partly PROVED in P; not run | — |
| P8 | PROVED in P; kpsolve (W, W) on the 6-rank analogue; 8×8 not run | — |
| P9 | PROVED in P; kpsolve (W, L) | — |
| P10 | PROVED in P; kpsolve (W, W) for k = 0, 1, 2 | R1; PREDICTIONS.md lists all three rows (the draft row said "not run") |
| P11 | PROVED (implication) after repair: W(X) and HSS defined; (V1b) checked from the layout | R1 item 11 |
| P12 | PROVED (implication) after repair: restricted to nodes where `--frozen` reports a win | knock-on of R2 item 4 |
"""

# ---------------------------------------------------------------- checks and write
bad = False
for label, o, n in EDITS:
    cnt = text.count(o)
    if cnt != 1:
        print(f"NOT UNIQUE ({cnt}): {label}")
        bad = True
# no overlapping OLD blocks
spans = []
for label, o, n in EDITS:
    i = text.index(o)
    spans.append((i, i + len(o), label))
spans.sort()
for (a1, b1, l1), (a2, b2, l2) in zip(spans, spans[1:]):
    if b1 > a2:
        print(f"OVERLAP: {l1} / {l2}")
        bad = True
if bad:
    sys.exit("aborted: the OLD blocks are not usable")

with open(OUT, "w", encoding="utf-8") as f:
    for k, (label, o, n) in enumerate(EDITS, 1):
        f.write(f"### EDIT {k}: {label}\n<<<<<<< OLD\n{o}\n=======\n{n}\n>>>>>>> NEW\n\n")
    f.write(STATUS.strip() + "\n")
print(f"wrote {OUT}: {len(EDITS)} edits")
