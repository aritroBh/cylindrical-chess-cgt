import sys
SRC = "/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md"
L = open(SRC).read().split("\n")
TXT = "\n".join(L)

def lines(a, b):  # 1-based inclusive
    return "\n".join(L[a - 1:b])

edits = []
def E(title, old, new):
    assert TXT.count(old) == 1, (title, TXT.count(old), old[:80])
    assert "\n=======\n" not in old and "\n=======\n" not in new
    edits.append((title, old, new))

TAG = "(revised after K7, 2026-10-22)"

# ---- 1 status paragraph
E("status paragraph: T2.7 and P12 repaired after K3",
  "17 are SOUND, and 4 are downgraded to GAP (the sharp form of 1.14, Theorem 2.7, P11, P12). No repaired proof\nwas found false.",
  """17 are SOUND, and 4 are downgraded to GAP (the sharp form of 1.14, Theorem 2.7, P11, P12). No repaired proof
was found false. Theorem 2.7 and P12 were repaired afterwards (task K7, 2026-10-22): they are PROVED after
repair in P, and K3's objection to Theorem 2.7 conflated the model P with the D-model (revised after K7,
2026-10-22).""")

# ---- 2 status row T2.7
E("status table: T2.7 row", L[47],
  """| T2.7 | GAP → PROVED after repair, in P (revised after K7, 2026-10-22). K7 made the local game of (L1) explicit (the first promotion ends it, a promotion by s is a failure for s̄, s̄'s king stays on F_Z, no pass in check, a mate of s is a win for s̄, a stalemate of s̄ is a failure; s cannot be stalemated in the local game because it may pass). K7 also fixed the choice that K3 and the T30 recheck left open: (L2) counts s's king and **context** pawns only, and s's Z-pawns are covered by (L1); (L3) is stated over the real play of a guided strategy. K3's objection (a context passer within the window ends the game in s's favour) is right in the D-model and wrong in P: in P only a promotion is terminal, and (L2) bounds it. The theorem gives a P-win only. A C-win needs (A_Q), and the D-model use in Theorem 1.14 needs (V2) | R1 item 3, R3 items 2 and 3; K3; K7 |""")

# ---- 3 status row P2.10(a)
E("status table: P2.10(a) Z-pawn proviso",
  "for chess-legal contexts and s's context pawns; s's Z-pawns are a separate check.",
  "for chess-legal contexts and s's context pawns. (L2) counts context pawns only, so there is no Z-pawn proviso: an s Z-pawn one move from promotion in Q makes (L1) fail by itself (revised after K7, 2026-10-22).")

# ---- 4 status row P12
E("status table: P12 row", L[80],
  """| P12 | GAP → PROVED after repair in P (Corollary 2.7′, from the repaired Theorem 2.7), restricted to nodes where `--frozen` reports a win. The chess form adds (A_Q) at the root; the earlier alternative "(V2) failure" is not needed (revised after K7, 2026-10-22) | knock-on of R2 item 4; K3; K7 |""")

# ---- 5 summary bullet
E("summary: Theorem 2.7 bullet", lines(125, 130),
  """- For a king move, (V2)+(V3) reduce to a local certificate: the punisher promotes within T moves against a
  defender who may pass, and the defender cannot promote within T moves elsewhere (Theorem 2.7: PROVED after
  repair, in P; it gives a P-win, not a C-win; revised after K7, 2026-10-22). The counter-promotion half
  counts the defender's king and context pawns only: its Z-pawns are covered by the local game. That half holds
  in every chess-legal non-terminal context when T = 1, on boards with at least 5 ranks (Proposition 2.10(a)).
  For T ≥ 2 it fails in some context on boards at least |F_Z| + 4 files wide (Proposition 2.10(b)),""")
# check the following line is unchanged text
assert L[130].startswith("  so a slower punishment's zero"), L[129]

# ---- 6 results table
E("summary table: T2.7 row", L[153],
  "| T2.7 | Local certificate LC_T (local forced promotion against a passing defender, no faster counter-promotion by a context pawn, no stalemate of s) ⇒ decisive punishment in P | PROVED after repair (revised after K7, 2026-10-22) |")
E("summary table: P2.10 row", L[156],
  "| P2.10 | For one-move punishments (T = 1) the counter-promotion condition holds in every chess-legal non-terminal context, on boards with at least 5 ranks (the defender's Z-pawns are covered by (L1), not by (L2)); for T ≥ 2 it fails in some (width ≥ \\|F_Z\\| + 4) | (a) PROVED after repair; (b) PROVED |")

# ---- 8 Definition 2.6 and Theorem 2.7
NEW8 = open("/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k7/new8.txt").read().rstrip("\n")
E("Definition 2.6 and Theorem 2.7 (and new Corollary 2.7')", lines(648, 704), NEW8)

# ---- 10 Proposition 2.10(a)
E("P2.10(a): drop the Z-pawn proviso in the statement",
  "Hence (L2) holds whenever, in addition, no s Z-pawn is one move from promotion in Q. *Proof:*",
  "Hence (L2), which counts context pawns only, holds " + TAG + ". *Proof:*")
E("P2.10(a): Z-pawn bullet", lines(762, 764),
  """  - *Z-pawns* """ + TAG + """. (L2) no longer counts them. An s Z-pawn that is one move from promotion in Q makes (L1)
    fail, because a promotion by s is a failure for s̄ in the local game. In the uses in §5.2–5.4, P3, P5 and P7
    the s Z-pawn is captured by r. In §5.3 and P8 it survives; it is far from promotion, and (L1) covers it.""")
E("P2.10(a): closing paragraph", lines(780, 782),
  """  So, by Theorem 2.7 (PROVED after repair, in P), a group whose punishments satisfy (L1) with T = 1 is decisively
  punished in P in every chess-legal non-terminal context on boards with H ≥ 5, provided (L3) holds. No Z-pawn
  proviso is needed. For T = 1, (L3) asks only that s is not stalemated at its single turn """ + TAG + ".")

# ---- 12 section 5.3
E("5.3: window form", L[1154],
  "  - Proposition 2.10(a) gives (L2), because Black cannot promote in one move from a non-terminal context; for Black to move this is Theorem 2.7(b), the window form, with Q = the position itself, and (L3) is the one-turn check that Black is not stalemated: its Z-pawn g7 has the moves g6 and g5 in every context " + TAG + ";")

# ---- 13 section 5.6
E("5.6: quantifier of the contrapositive", lines(1234, 1235),
  """- PROVED: by Theorem 2.7 (contrapositive), for every reply r and every T, every king move that does not lose in P
  violates (L1), (L2) or (L3) """ + TAG + """. A move that loses in P but not in C is an (A_Q) failure.""")

# ---- 14 section 6 P12
E("section 6: P12 row", L[1277],
  """| P12 | cyl:7x6 | Z_T + any context on e–f | If `--frozen` reports a win for σ at X, then either σ wins in P, or, for every `--frozen` winning strategy of σ, some node of it with σ̄ to move has a king move of σ̄ that is not a P-loss. For that move, and for every reply r and every T, (L1), (L2) or (L3) fails. In chess, add (A_Q) at X | — | — (a harness check, not one position) | Thm 2.7 (contrapositive) + the transfer argument of Corollary 2.7′ | PROVED after repair, in P, for the nodes where `--frozen` reports a win; the chess form needs (A_Q) (revised after K7, 2026-10-22) |""")

# ---- 15 appendix
E("Appendix A: K7 checks", L[1440],
  L[1440] + "\n" + open("/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k7/new15.txt").read().rstrip("\n"))

out = []
for i, (t, o, n) in enumerate(edits, 1):
    out.append(f"### EDIT {i}: {t}\n<<<<<<< OLD\n{o}\n=======\n{n}\n>>>>>>> NEW\n")
open("/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k7/edits_K7.txt", "w").write("\n".join(out))
print(len(edits), "edits")
