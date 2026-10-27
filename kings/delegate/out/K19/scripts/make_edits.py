"""K19: build EDITS.md for kings/theory/LOOPY.md (read only). Every OLD text is taken from the current LOOPY.md
(or typed and asserted) and must occur exactly once; the script fails otherwise. Usage: make_edits.py <xcheck_local numbers>"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOOPY = '/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md'
text = open(LOOPY).read()
lines = text.split('\n')

edits = []


def add(label, old, new):
    n = text.count(old)
    assert n == 1, (label, n)
    # the edits are applied one after the other: OLD texts must not overlap
    edits.append((label, old, new))


def block(a, b):
    """lines a..b (1-based, inclusive) of LOOPY.md as one string"""
    return '\n'.join(lines[a - 1:b])


XL = open(os.path.join(HERE, '..', 'logs', 'xcheck_local.log')).read().strip().splitlines()[-1] if os.path.exists(os.path.join(HERE, '..', 'logs', 'xcheck_local.log')) else ''
m = re.search(r'positions (\d+) .*?A wins P in (\d+).*?mismatches (\d+).*?mismatches (\d+)', XL)
assert m, XL
XL_N, XL_AW, XL_B1, XL_B2 = m.groups()
assert XL_B1 == '0' and XL_B2 == '0', XL

# 1. labels
add('labels-checked2',
    "- **KNOWN**: from the literature, with a citation.\n",
    "- **KNOWN**: from the literature, with a citation.\n"
    "- **COMPUTED-1** and **CHECKED-2** (revised after K19, 2026-10-27): labels for a finite computation, never for a\n"
    "  theorem. COMPUTED-1: one implementation produced the numbers. CHECKED-2: two independently written\n"
    "  implementations agree on the exact numbers (for example the scratch run and a second program, or two solvers).\n"
    "  Neither label is a proof, and neither replaces PROVED for a statement over all contexts.\n")

# 2. status rows
add('status-5.1-L1',
    "| §5.1, (L1) | CONJECTURE (scratch, k ≤ 4 and k = ∞ only; (L3) not checked). The k = ∞ case was re-run in K7 against the local game of Definition 2.6 ((L1_P): T = 5 to 6; (L1) with the queen clause: T = 6 to 7), same label (revised after K7, 2026-10-22) | R1 items 3 and 10, R4 item 9; K7 |",
    "| §5.1, (L1) | CHECKED-2 (revised after K19, 2026-10-27). K19 wrote the local game again from Definition 2.6 and agrees with the K7 numbers: after the reply Kxa4, with k = ∞ and the king confined to {h, a, b}, T = 6, 6, 6, 7, 7 with the queen clause and T = 6, 6, 5, 6, 6 for (L1_P) (Kg4, Kg5, Kg6, Kh6, Ka6). With the pre-K7 rules and every budget k = 0, …, 8 and ∞ the least T is 5 to 7, as the scratch run said. The budgets k = 5, 6 (not checked before) equal k = ∞, and so does every k ≥ 7, because the window holds at most T ≤ 7 moves of s. The five Black sorties give the mirrored numbers. (L3): COMPUTED-1 (K19 only): in the bare group it holds for the five sorties at T and at T + 1, T + 2, with and without the queen clause | R1 items 3 and 10, R4 item 9; K7; K19 |")
add('status-5.2',
    "\"Not punished\": CONJECTURE (scratch); in C, kpsolve confirms the 6-rank analogue (P5) | R4 item 9 |",
    "\"Not punished\": CHECKED-2 (revised after K19, 2026-10-27): after Kd5, Ke5 or Kf5 Black has no forced promotion, in the local game after ...Kxd7 (with or without passes, confined or not) and in the exact P-model after the sortie with every Black reply (result D, two solvers). Only Kf7 loses, with T = 10. In C, kpsolve agrees on both boards and on the 6-rank analogue (P5) | R4 item 9; K19 |")
add('status-5.5',
    "| §5.5 | CONJECTURE (scratch); Kd3 added | R1 items 10 and 11, R4 item 9 |",
    "| §5.5 | CHECKED-2 (revised after K19, 2026-10-27), with one correction. Confirmed: Black's moves are exactly Kc5, Kd3, Kd4, Kd5; after Kc5 Kxb3 White has no win with any number of passes; after Kd3 White wins with T = 5 for every budget, unlimited passes included. Corrected: after Kd4 and Kd5 White wins the local game against every finite budget of passes (T = 6 + k) and not against unlimited passes, so \"only if Black has no spare move\" holds for an unlimited supply only. kpsolve and the P-model agree on all four sorties | R1 items 10 and 11, R4 item 9; K19 |")
add('status-5.6',
    "μ_W = 5: PROVED by count. T = 5 and \"(L2) fails by one tempo\": CONJECTURE (scratch; R4 re-derived both) | R1 item 11 |",
    "μ_W = 5: PROVED by count (K19's breadth-first search agrees). T = 5 and \"(L2) fails by one tempo\": CHECKED-2 (revised after K19, 2026-10-27: T = 5 for every budget, with or without the queen clause and the confinement; μ_W = 5 < T + 1 = 6; the scratch run, R4 and K19 agree) | R1 item 11; K19 |")
add('status-P5',
    "bare w-entry CONJECTURE; kpsolve agrees on all four entries | — |",
    "bare w-entry CHECKED-2 (revised after K19, 2026-10-27: the P-value D from two independent solvers, and D in C from kpsolve); kpsolve agrees on all four entries | K19 |")
add('status-P6P7',
    "| P6, P7 | CONJECTURE, and partly PROVED in P. kpsolve (exact, 8×8):",
    "| P6, P7 | CHECKED-2 (revised after K19, 2026-10-27: P6 = (L, W) and P7 = (D, W) in P from two independent solvers, on the cylinder and on the flat board; P7's w-entry is the draw that was a CONJECTURE), and partly PROVED in P. kpsolve (exact, 8×8):")

# 3. section 5.1
old = block(1659, 1664)
assert old.startswith("  BP a5 on the 8-file cylinder."), old[:40]
add('5.1-black-moves',
    "BK's five legal moves are Ka3, Kc3,\n  Kc4, Kc5 and Kb5; the first four abandon BP a5, which White's king then captures on a5, giving White a\n  passer, and the fifth (Kb5) puts Black's king on the square that guards both a4 and a5, so that White is in\n  zugzwang with only pawn-blocked moves left. So every king move in the group is decisively punished, and the\n  group is frozen. The enumeration agrees with `notes/diagram_audit.md` §C.3.",
    "BK's five legal moves are Ka3, Kb3,\n  Kc3, Kc4 and Kc5 (Kb5 is illegal: the pawn a4 attacks b5); each of them abandons BP a5, which White's king\n  then captures on a5, giving White a passer. (They are the mirror images of the White list: g4 ↔ c5, g5 ↔ c4,\n  g6 ↔ c3, h6 ↔ b3, a6 ↔ a3.) So every king move in the group is decisively punished, and the group is frozen.\n  (Corrected after K19, 2026-10-27: the earlier list had Kb5 for Kb3 and a zugzwang argument for a move that is\n  not legal. The conclusion stands. K19's move generator, checked against `kpsolve --moves`, gives the list above.\n  The agreement with `notes/diagram_audit.md` §C.3 claimed earlier refers to the earlier list; K19 did not re-read\n  the audit.)")
add('5.1-L1-bullet',
    block(1668, 1671),
    "  - (L1) holds for all five White sorties with T ≤ 7 (5 to 7, depending on the sortie and the budget), for\n"
    "    every pass budget **k = 0, 1, …, 8 and k = ∞**, with the punisher's king confined to {h, a, b}: **CHECKED-2**\n"
    "    (revised after K19, 2026-10-27: the scratch run and K19's code agree. The budgets k = 5, 6, 7, 8 equal k = ∞,\n"
    "    and every k ≥ 7 equals k = ∞, because the window contains at most T ≤ 7 moves of s, so no budget is used up.)\n"
    "    (L3) holds in the bare group for the five sorties: **COMPUTED-1** (K19 only; Appendix A).")
add('5.1-K7-sub',
    "This is still scratch evidence: the label stays CONJECTURE (revised after K7, 2026-10-22).",
    "K19's code reproduces both lists, so this is now CHECKED-2 (revised after K19, 2026-10-27).")
add('5.1-prediction',
    block(1683, 1685),
    "- **Prediction.** The bare 5.1 is a real mutual zugzwang, (L, W) (P6 in §6). **CHECKED-2** (revised after K19,\n"
    "  2026-10-27): K19's own P-model solver and the P-model build of kpsolve both give (L, W) in P, and kpsolve gives\n"
    "  (L, W) in C. After each of the five White sorties (Black to move) White is lost in P, and after each of the five\n"
    "  Black sorties (White to move) Black is lost, in P and in C.")

# 4. section 5.2
add('5.2-not-punished',
    block(1704, 1707),
    "  - That the three sorties are *not punished* in P (no forced promotion for Black) is **CHECKED-2** (revised after\n"
    "    K19, 2026-10-27): even without passes, Black cannot force promotion after Kd5, Ke5 or Kf5. K19: in the local\n"
    "    game after ...Kxd7 Black has no win at any T, with or without passes, with the king confined to {d, e, f} or\n"
    "    not; in the exact P-model after the sortie, against every Black reply, the result is a draw (own solver and the\n"
    "    P build of kpsolve), and kpsolve gives a draw in C on the cylinder and on the flat board. Only Kf7 loses, in 10\n"
    "    moves (T = 10 in the local game without the queen clause, with or without passes; with the queen clause T = 10\n"
    "    without passes and 11 with unlimited passes). In chess, kpsolve gives (D, W) for the 6-rank analogue Z_72 bare,\n"
    "    so White to move draws (P5). In the analogue Kb3, Kc3 and Kd3 are not punished and Kd5 loses (T = 6).")

# 5. section 5.5
add('5.5-escape',
    "- **But Black has an escape. CONJECTURE (scratch evidence; kpsolve agrees).** After the sortie Kc5 and Kxb3,\n  White cannot force promotion even without passes; after Kd4 and Kd5, White wins only if Black has no spare\n  move. Black's legal moves",
    "- **But Black has an escape. CHECKED-2 (revised after K19, 2026-10-27; kpsolve agrees).** After the sortie Kc5\n"
    "  and Kxb3, White cannot force promotion even without passes, and not with unlimited passes either (no win at any\n"
    "  T, confined or not). After Kd4 and Kd5, White wins the local game against every finite budget of Black's passes\n"
    "  (T = 6 + k with the queen clause, k = 0, …, 8) and does not win against unlimited passes: \"wins only if Black\n"
    "  has no spare move\" is right for an unlimited supply of passes and was too strong as written for a finite one.\n"
    "  After Kd3 White wins with T = 5 for every budget, unlimited passes included. So (L1) holds for Kd3 and fails\n"
    "  at k = ∞ for Kd4 and Kd5, which are nevertheless punished in P and in C, because the real supply is finite.\n"
    "  Black's legal moves")

# 6. section 5.6
add('5.6-T-mu',
    block(1806, 1808),
    "  - Black's local win after Ke6 Kxg4 takes T = 5. **CHECKED-2** (revised after K19, 2026-10-27: the scratch run and\n"
    "    K19's code agree. T = 5 for every pass budget 0, …, 4 and ∞, with or without the queen clause and the\n"
    "    confinement to {f, g, h}. Here Q_Z = `Ke6 kg4 pg5`: the context pawns c3 and d6 are deleted.)\n"
    "  - So μ = T, and (L2) fails by one tempo. **CHECKED-2** (Review 4 re-derived both numbers, and K19's breadth-first\n"
    "    search gives μ_W = 5 with the same Q°, so μ_W = 5 < T + 1 = 6). The sortie nevertheless loses in P: the P build\n"
    "    of kpsolve gives Black the win after Ke6 (`Ke6 Pg4 Pc3 kh4 pg5 pd6 b -` is L from White's side;\n"
    "    COMPUTED-1, K19), so the documented draw is an (A_Q) failure, not a failure in P.")

# 7. section 6 rows
add('6-P5',
    "all entries PROVED in P except the bare w-entry, which is a CONJECTURE (scratch: no forced promotion); kpsolve agrees on all four entries |",
    "all entries PROVED in P except the bare w-entry, which is CHECKED-2 (K19, 2026-10-27: the P-value D from an own solver and from the P build of kpsolve, and D in C from kpsolve); kpsolve agrees on all four entries |")
add('6-P6',
    "| Thm 2.4 + Thm 2.7 ((L1) scratch, T ≤ 7) + self-duality | CONJECTURE; kpsolve agrees |",
    "| Thm 2.4 + Thm 2.7 ((L1): CHECKED-2, T ≤ 7; (L2) is vacuous in the bare group; (L3): COMPUTED-1) + self-duality (also checked numerically by K19) | CHECKED-2 (K19, 2026-10-27: (L, W) in P from two solvers); kpsolve agrees |")
add('6-P7',
    "| Prop 2.10(a) for Black; Lemma 2.9 for White | b PROVED in P; w CONJECTURE; kpsolve and Lichess agree |",
    "| Prop 2.10(a) for Black; Lemma 2.9 for White | b PROVED in P; w CHECKED-2 (K19, 2026-10-27: D in P from two solvers, on both boards); kpsolve and Lichess agree |")

# 8. appendix A
add('appendix-K19',
    "    - sharpness examples of the text above: I re-ran them myself with the private builds, and they agree.",
    "    - sharpness examples of the text above: I re-ran them myself with the private builds, and they agree.\n"
    "- **K19 re-computation (2026-10-27; scripts, logs and `summary.json` in `kings/delegate/out/K19/`).** One new\n"
    "  implementation, written from Definition 2.6 and `kings/SPEC.md` without reading `kings/ref/` or the K7 scripts:\n"
    "  - a move generator (kings, pawns, e.p., promotion), which agrees with `kpsolve --moves` on 980 random\n"
    "    positions (4802 moves, 6 boards, with e.p. rights);\n"
    "  - the local game of Definition 2.6: bounded recursion with a pass budget k (0, …, 8, ∞), the queen clause and the\n"
    "    mate rule as switches, so that the pre-K7 and the K7 versions both run; the unbounded least fixed point; (L3) as\n"
    "    a search over guided strategies against a real s without passes; and μ_s as a breadth-first search;\n"
    "  - a full-board solver of the model P, which agrees with the P-model build of kpsolve on 350 random positions;\n"
    "  - the local game with no passes, no confinement and no queen clause is exactly P, and agrees with the P build of\n"
    "    kpsolve on %s random positions (%s of them won by the attacker; bounded recursion and fixed point agree).\n"
    "  Results: §5.1 (L1) and (L3) (five White and five Black sorties), §5.2 (not punished), §5.5, §5.6, P5, P6, P7 as\n"
    "  recorded in the status table and in those sections. Every kpsolve run used a private build\n"
    "  (`cc -O2 -o kp kings/kpsolve.c -lpthread`; the P build is K7's `kp_p.c`)." % (XL_N, XL_AW))

# overlap check
for i, (la, oa, na) in enumerate(edits):
    for lb, ob, nb in edits[i + 1:]:
        assert oa not in ob and ob not in oa, (la, lb)
with open(os.path.join(HERE, '..', 'EDITS.md'), 'w') as f:
    f.write("# K19 edits to kings/theory/LOOPY.md\n\n"
            "Labels changed: CONJECTURE to CHECKED-2 where K19's independent code and the original scratch result agree; "
            "(L3) is COMPUTED-1 (never checked before, one implementation); two statements are corrected "
            "(Black's king moves in 5.1, and \"only if Black has no spare move\" in 5.5). Apply in order; "
            "OLD occurs exactly once in the current LOOPY.md (the script `scripts/make_edits.py` asserts it).\n\n")
    for label, old, new in edits:
        f.write("### EDIT %s\n<<<<<<< OLD\n%s\n=======\n%s\n>>>>>>> NEW\n\n" % (label, old.rstrip('\n') if label != 'labels-checked2' else old.rstrip('\n'), new.rstrip('\n')))
print(len(edits), 'edits written')
