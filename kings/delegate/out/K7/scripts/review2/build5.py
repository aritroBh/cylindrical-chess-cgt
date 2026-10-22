"""Build final_edits5.txt from final_edits4.txt: substitute in the NEW parts, then append new edits."""
S = "/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k7/"
t = open(S + "w/final_edits4.txt").read()


def rep(old, new):
    global t
    n = t.count(old)
    assert n == 1, (n, old[:80])
    t = t.replace(old, new)


M = "(revised after K7, 2026-10-22)"

# ---- Edit 1: caveat
rep("""right (revised after K7, 2026-10-22). K3 did not see the repair, and no second model and no human has
re-derived it.""",
"""right (revised after K7, 2026-10-22). Three more AI reviewers (logic, chess, consistency) then read the
final text, with the e.p. clause. They found no counterexample and no false step in the proof, only wording and
bookkeeping errors, which were corrected in the same pass (revised after K7, 2026-10-22). The corrected text has
not been read again. K3 did not see the repair, and no human has re-derived it. The scripts behind the checks
of Appendix A are in the K7 scratchpads, not in the project.""")

# ---- Edit 2: T2.7 row + new C2.7' row
rep("""(L3) is stated over the real play of a guided strategy. K3's objection""",
    """(L3) is stated over the real play of a guided strategy, in which s̄ makes Z-moves only. K3's objection""")
rep("""The theorem gives a P-win only. A C-win needs (A_Q) | R1 item 3, R3 items 2 and 3; K3; K7 |""",
    """The theorem gives a P-win only. The bound μ_s ≥ T + 1 is sharp in P, and in chess no margin of μ_s replaces (A_Q) (examples in the text). A second review round found no false step | R1 item 3, R3 items 2 and 3; K3; K7 |
| C2.7′ | PROVED in P (revised after K7, 2026-10-22): the contrapositive of Theorem 2.7(a), the content of P12. If `--frozen` reports a win for σ and every king move of σ̄ at the nodes of σ's winning strategy is a P-loss, then σ wins P. The chess form adds (A_Q) | K7 |""")

# ---- Edit 3: P2.10(a) proviso, status table
rep("""so there is no Z-pawn proviso: an s Z-pawn one move from promotion in Q makes (L1) fail by itself (revised after K7, 2026-10-22).""",
    """so there is no Z-pawn proviso: s's Z-pawns are covered by (L1), whatever their distance from promotion (revised after K7, 2026-10-22).""")

# ---- Edit 6: summary table T2.7 row + C2.7' row
rep("""decisive punishment in P | PROVED after repair (revised after K7, 2026-10-22) |""",
    """decisive punishment in P; μ_s ≥ T + 1 is sharp | PROVED after repair (revised after K7, 2026-10-22) |
| C2.7′ | If `--frozen` reports a win for σ and every king move of σ̄ on the nodes of its winning strategy is a P-loss, σ wins P (content of P12) | PROVED in P (revised after K7, 2026-10-22) |""")

# ---- Edit 7 summary table P2.10 row: ok as is.

# ---- Edit 8: Definition 2.6 and Theorem 2.7
rep("""the buffer empty, no officer, no promotion yet.
- m is a legal Z-move of s that is not a promotion.""",
    """the buffer empty, no officer, no promotion yet. An e.p. right carried by Y is cleared by m. The proof of (a) does not
  use that Y is chess-legal: it uses that m and r are legal moves (see (b)).
- m is a legal Z-move of s that is not a promotion.""")

rep("""    - With context pawns only, Proposition 2.10(a) needs no Z-pawn proviso: an s Z-pawn one move from promotion
      in Q makes (L1) fail.""",
    """    - With context pawns only, Proposition 2.10(a) needs no Z-pawn proviso: s's Z-pawns are covered by (L1),
      whatever their distance from promotion (a promotion by s is a failure for s̄ in the local game).""")

rep("""  - **(L2⁺)**, the recommended margin before invoking (A_Q), is μ_s ≥ T + 2. With μ_s = T + 1, s's pawn reaches
    its seventh rank just as s̄ queens, and queen-against-seventh-rank-pawn endings can be drawn.
- **(L3) no stalemate of s in the window.** A *guided strategy* of s̄ is a strategy in the real game that at each
  of its turns plays a move whose projection is a winning move of L_T(Q_Z) at the projected position, with the
  remaining time.""",
    """  - **μ_s ≥ T + 1 is the exact bound for P.** Step 4 shows that s promotes no earlier than its (T + 1)-th turn, and
    s̄ queens on its T-th move, which follows s's T-th turn. With μ_s = T, s promotes first (example below).
  - **(L2⁺)**, μ_s ≥ T + 2, is only a margin, and it does not give a chess win. With μ_s = T + 1, s promotes at once
    after s̄ queens (queen against queen, not against a pawn on its seventh rank). With μ_s = T + 2, s̄ has one move
    with its new queen, and a draw can still follow. No margin of μ_s replaces (A_Q) at the position (examples in
    "What Theorem 2.7 does not give"). The earlier wording, "queen-against-seventh-rank-pawn endings can be
    drawn", described the T + 1 case wrongly (revised after K7, 2026-10-22).
- **(L3) no stalemate of s in the window.** A *guided strategy* of s̄ is a strategy in the real game that at each
  of its turns plays a Z-move (a king step onto a square of F_Z, a move of a Z-pawn, or a promotion) whose
  projection is a winning move of L_T(Q_Z) at the projected position, with the remaining time. s̄ never moves a
  context pawn.""")

rep("""- **(b) Window form.** The proof does not use how Q arose. Let Q be any legal position with s to move in which
  every pawn is a Z-pawn on F_Z or a context pawn on a context file, the buffer is empty, there is no officer,
  s̄'s king stands on F_Z, and no s̄ context pawn attacks s's king (automatic if s's king is on F_Z). Q may
  carry an e.p. right with its target anywhere: (L2) counts a right whose target is off F_Z, and π keeps a
  right whose target is on F_Z. If (L1),
  (L2) and (L3) hold at Q, s̄ has a forced win in P from Q. This is the form used in §5.3 and P8, with Q = Y.""",
    """- **(b) Window form.** The proof does not use how Q arose. Let Q be a position with s to move which is
  chess-legal, or which arises from a position Y of Definition 2.1 by legal moves m and r as in (a), and in which
  every pawn is a Z-pawn on F_Z or a context pawn on a context file, the buffer is empty, there is no officer,
  s̄'s king stands on F_Z, and no s̄ context pawn attacks s's king (automatic if s's king is on F_Z). Q may
  carry an e.p. right with its target anywhere: (L2) counts a right whose target is off F_Z, and π keeps a
  right whose target is on F_Z. If (L1),
  (L2) and (L3) hold at Q, s̄ has a forced win in P from Q. This is the form used in §5.3 and P8, with Q = Y.
  The window form does not cover a legal position in which s is in check from an s̄ context pawn that has just
  moved (s's king on a context or buffer file): there (I4) fails, and the theorem says nothing.""")

rep("""A right created by
    s is of no use to s̄'s prescribed moves. So the only e.p. capture that an s context pawn can ever make is the
    one of the right carried by Q, if its target is off F_Z, and it can be made at s's first turn only.""",
    """A right created by
    s concerns an s pawn, so it is of no use to an s context pawn. If its target is on F_Z, s̄'s Z-pawns may use it,
    and the local game accounts for this (π keeps such a right). If its target is off F_Z, no s̄ pawn that s̄
    moves can use it, and π drops it. So the only e.p. capture that an s context pawn can ever make is the
    one of the right carried by Q, if its target is off F_Z, and it can be made at s's first turn only.""")

rep("""*Part (b)* is the same proof with Q as the starting point: only (I1)–(I5) at Q were used, and they are the
hypotheses of (b) together with Lemma 2.2. *Part (a)* is part (b) applied to Q: m and r are Z-moves, so""",
    """*Part (b)* is the same proof with Q as the starting point: only (I1)–(I5) at Q were used, that s̄'s king is not
attacked at Q, and that an e.p. right is that of a pawn standing where the right says. These are the hypotheses of
(b) (they hold for a chess-legal Q, and for the Q of (a) because m and r are legal), together with Lemma 2.2.
*Part (a)* is part (b) applied to Q: m and r are Z-moves, so""")

rep("""- *No C-win.* In P a promotion wins at once. In chess the new queen must survive and the ending must be won.
  (L1) asks for a queen that s cannot capture at once, which is not enough: that s̄ wins chess after the
  promotion is the per-position hypothesis (A_Q), checked by kpsolve (§1.2). (L2⁺) is only a margin.""",
    """- *No C-win, and no margin of μ_s gives one.* In P a promotion wins at once. In chess the new queen must survive
  and the ending must be won. (L1) asks for a queen that s cannot capture at once, which is not enough: that s̄ wins
  chess after the promotion is the per-position hypothesis (A_Q), checked by kpsolve (§1.2). (L2⁺) is only a margin.
  The examples below are kpsolve results (`--promote QRBN --cap 2`, both bounds equal; the P values come from the
  private `--pmodel` copy of Appendix A). By the Labels rule they are data and keep the label CONJECTURE. In each,
  s̄ is Black, and (L1) with the queen clause, (L2) with the e.p. clause and (L3) hold (revised after K7, 2026-10-22).
  - μ_s = T + 1, window form with Q = the position: cyl:7×6 `Ka4 ka6 Pf4 pb2`, White to move. T = 1 (b1=Q), and the
    White pawn f4 has μ_s = 2. Black wins P. **White wins chess**, and 1.f5 is the only winning move.
  - μ_s = T + 1, form (a): cyl:7×6, Y = `Kc5 ka3 Pe2 pc4`, White to move, m = Kc5–d5, r = c4–c3,
    Q = `Kd5 ka3 Pe2 pc3`, T = 2 (c2, c1=Q), μ_s = 3. Corollary 2.8 applies (d(Kd5, c1) = 4 = D + 2). After m, Black
    wins P and **White wins chess**.
  - μ_s = T + 1, form (a): cyl:7×6, Y = `Kb4 ka1 Pe4 pa2`, White to move, m = Kb4–c5, r = Ka1–b1,
    Q = `Kc5 kb1 Pe4 pa2`, T = 1, μ_s = 2. After m, Black wins P and chess is **drawn**.
  - μ_s = T + 2: flat:6×6 `Ke6 kb1 Pf2 pc2`, White to move. T = 1, μ_s = 3 (f4, f5, f6=Q). Black wins P and chess
    is **drawn**.
  - In a sampled enumeration of one Black Z-pawn and one White context pawn, a reviewer found draws still present at
    μ_s ≥ T + 3 on flat:6×6 (4 of 659), and none at μ_s ≥ T + 2 on cyl:7×6 (scratch).
  - Hence a chess form of (V3) does not follow from any horizon condition. The paper's Conjecture `conj:cert`
    (`paper/ieee/sections/04_kings.tex`, "a certificate of horizon h implies (V3)") and the matching sentence of
    `kings/REPORT.md` are refuted as worded by the second and third example. Theorem 2.7 supports the P-version only.""")

rep("""- *The conditions cannot be dropped.* All examples are in cyl:7×6 and checked with the P solver.""",
    """- *The conditions cannot be dropped.* All examples are in cyl:7×6. The P values are kpsolve results from the private
  `--pmodel` copy of Appendix A (not saved in the project). By the Labels rule they are data, and the claim that
  the conditions cannot be dropped keeps the label CONJECTURE; the races can be checked by hand.""")

rep("""  - (L1) is the substance: with no local win there is nothing to transfer.""",
    """  - (L2), sharpness of μ_s ≥ T + 1: `Kf5 kc6 Pe4 pb3`, White to move, has T = 2 (b2, b1=Q) and μ_s = 2, and White wins
    P (1.e5 b2 2.e6=Q). With the pawn on e3 instead, μ_s = 3 and Black wins P (1.e4 b2 2.e5 b1=Q). The example
    `Kd6 kc2 pa3 Pe4 pe5 pf5` above also has μ_s = T = 2.
  - (L1) is the substance: with no local win there is nothing to transfer.""")

# ---- Edit 9/10/11: P2.10(a)
rep("""  - *Z-pawns* (revised after K7, 2026-10-22). (L2) no longer counts them. An s Z-pawn that is one move from promotion in Q makes (L1)
    fail, because a promotion by s is a failure for s̄ in the local game. In the uses in §5.2–5.4, P3, P5 and P7
    the s Z-pawn is captured by r. In §5.3 and P8 it survives; it is far from promotion, and (L1) covers it.""",
    """  - *Z-pawns* (revised after K7, 2026-10-22). (L2) no longer counts them. They are covered by (L1), whatever their
    distance from promotion: a promotion by s is a failure for s̄ in the local game, and Step 4 of Theorem 2.7 uses
    exactly that. (If s can promote at its first turn, (L1) fails. If an s Z-pawn stands on its penultimate rank but s
    is in check at Q and cannot promote at once, (L1) may hold, and then the theorem applies.) In the uses in §5.2–5.4, P3, P5 and
    P7 the s Z-pawn is captured by r. In §5.3 and P8 it survives; it is far from promotion.""")

# ---- Edit 15: Appendix A, K7 checks
rep("""  - a solver of the local game of (L1) (passes, confined king, mate of s a win, promotion by s a failure, T ≤ 5),
    a search for μ_s (context pawns only, and the old count with Z-pawns), and a search of the real window game
    for (L3) (s̄ restricted to winning local moves, s free);
  - the exact P value from a private copy of `kings/kpsolve.c` with one added switch (a promotion wins at once
    for the promoter, kings move normally). The project file is unchanged.""",
    """  - a solver of the local game of (L1) (passes, confined king, mate of s a win, promotion by s a failure, T ≤ 5),
    a search for μ_s (context pawns only, and the old count with Z-pawns), and a search of the real window game
    for (L3). In that search s is free, and s̄ plays any move whose projection is a winning local move, except
    king moves off F_Z. It did **not** exclude context moves of s̄, so its strategies are wider than the guided
    strategies of Definition 2.6 as now worded (Z-moves only). The runs are therefore not an exact test of the
    stated (L3); a reviewer's corrected harness (below) restricts s̄ to Z-moves;
  - the exact P value from a private copy of `kings/kpsolve.c` with one added switch, `--pmodel` (a promotion wins at
    once for the promoter, kings move normally). The project file is unchanged. The whole patch is three lines:
    `PMODEL = 0` added to the static flags next to `FROZEN`; the test `if (FROZEN) emit(..., 'P', ...)` at the
    promotion move generator changed to `if (FROZEN || PMODEL) emit(..., 'P', ...)`; and
    `else if (!strcmp(argv[i], "--pmodel")) PMODEL = 1;` in the option parser.
  - All K7 runs of the drafter used F_Z = {a, b, c}.""")
rep("""cyl:7×6 run where half of the positions have it on F_Z (522 positions with LC_T in all). 34000""",
    """cyl:7×6 run where half of the positions have it on F_Z (934 positions with LC_T in that run, 522 of them with the target on F_Z). 34000""")
rep("""    win in P and a Black win in P without the right (private patched copy of `kpsolve.c`).""",
    """    win in P and a Black win in P without the right (private patched copy of `kpsolve.c`).
  - **Independent re-check by a reviewer (2026-10-22; scratch, not saved in the project).** A second implementation,
    written without the drafter's code, using kpsolve only for P values. Numbers as reported by the reviewer, not
    re-run by me, except where stated:
    - its move generator agrees with `kpsolve --moves` on 1600 random positions; it reproduces the (L1) values of
      §5.1 (below); Corollary 2.8 holds on 9566 placements on 4 boards, with the queen clause;
    - window form (b), random Q with 1 to 3 pawns a side, about 45000 pairs satisfying (L1) to (L3) on cyl:7×6
      (F_Z = a–c, b–d, a–b, a–d), cyl:7×5, cyl:6×6, flat:6×6 and flat:7×6 (middle group): no non-win. A structured
      e.p. family (an s pawn blocked by an s̄ pawn beside one that has just double-stepped): 19525 pairs with the
      e.p. clause, no non-win. The same positions without the clause: 53210 pairs, 8387 of them P non-wins. So the
      harness has power, and the clause cures the first draft's error. A stalemate-focused family: 40308 pairs, no
      non-win. When (L1) and (L2) hold and (L3) fails, 109 of 139 are P non-wins, so (L3) is needed;
    - form (a): 117232 triples (random Y, every Z-move m, every admissible r), and in all of them both Y·m and Q are
      P-wins for s̄. The quantitative claim, that a guided strategy of s̄ wins within T moves against every legal real
      play of s, had no failure in about 70000 pairs. With μ_s = T instead of T + 1, about 23 percent of the LC
      positions are non-wins;
    - sharpness examples of the text above: I re-ran them myself with the private builds, and they agree.""")
# ---- Edit 17: 5.1 (L1) evidence
rep("""      reply Kxa4, with a second scratch implementation. (L1) holds with T = 6, 6, 5, 6, 6 for Kg4, Kg5, Kg6, Kh6,
      Ka6, and with T = 6, 6, 6, 7, 7 if the new queen must also be safe. This is still scratch evidence: the label
      stays CONJECTURE (revised after K7, 2026-10-22).""",
    """      reply Kxa4, with a second scratch implementation. (L1_P), which has no queen clause, holds with
      T = 6, 6, 5, 6, 6 for Kg4, Kg5, Kg6, Kh6, Ka6. (L1), with the queen clause, holds with T = 6, 6, 6, 7, 7.
      A reviewer's independent implementation gave the same two lists. So in P the freeze needs μ_s ≥ 7 at the
      zugzwang nodes (Theorem 2.7 holds with (L1_P)), and μ_s ≥ 8 with the queen clause, which is the value used
      above. This is still scratch evidence: the label stays CONJECTURE (revised after K7, 2026-10-22).""")

# ---- Edit 19: status row 5.1
rep("""(T = 5 to 7), same label (revised after K7, 2026-10-22)""",
    """((L1_P): T = 5 to 6; (L1) with the queen clause: T = 6 to 7), same label (revised after K7, 2026-10-22)""")

# ---- Edit 16 (Cor 2.8): fine as is. Edit 18, 12, 13, 14, 4, 5: as is.

# ---- New edits
new = []


def add(label, old, newtext):
    new.append(f"### EDIT {label}\n<<<<<<< OLD\n{old}\n=======\n{newtext}\n>>>>>>> NEW\n")


add("20: status paragraph: caveat sentence",
    """repaired proof was written by a free external model and read once by the integrator. Each was then checked""",
    """repaired proof, except those of T2.7 and P12 (see the K7 caveat below), was written by a free external model and
read once by the integrator. Each was then checked""")

add("21: status table: C2.8 row",
    """| C2.8 | PROVED (wording corrected) | R3 item 7 |""",
    """| C2.8 | PROVED (wording corrected). The finite-k clause was made a side remark after K7 (revised after K7, 2026-10-22). A reviewer found no counterexample in 9566 placements on 4 boards (scratch) | R3 item 7; K7 |""")

add("22: P2.10(a): the e.p. sentence in the proof",
    """  - It cannot be taken en passant. Only a pawn that has just made a double step can be. In a chess position
    the last move before Y was s̄'s, and r, the last move before Q, is not a double step: it is a king capture,
    or the promotion in §5.3.""",
    """  - It cannot be taken en passant. Only a pawn that has just made a double step can be. In a chess position
    the last move before Y was s̄'s, and so was the last move before Q (r, or in the window form the move that led
    to Q), so no pawn of s has just double-stepped. In §5.3 the window Q is Y itself (revised after K7, 2026-10-22).""")

add("23: section 7 item 3: the budget clause",
    """the "every budget" clause in (L1), and the traps""",
    """the unlimited-pass clause in (L1) (the earlier "every budget" phrasing is withdrawn; revised after K7, 2026-10-22), and the traps""")

add("24: section 8 item 1: pre-K7 budgets",
    """satisfied (L1) for every
     budget.""",
    """satisfied (L1) for every
     budget k ≤ 4 and for k = ∞ (the local game before K7; Definition 2.6 now has k = ∞ only; revised after K7,
     2026-10-22).""")

add("25: section 6: P4 row, pre-K7 marker",
    """(L1) holds: scratch, T ≤ 5, all budgets, confined king. (L2) holds at every loser-to-move node: scratch. (L3) not checked""",
    """(L1) holds: scratch, T ≤ 5, all budgets, confined king. (L2) holds at every loser-to-move node: scratch. (L3) not checked. These checks used the local game and the μ before K7: the old μ counted the king and all pawns, and Definition 2.6 now counts the king and context pawns, with the e.p. clause (revised after K7, 2026-10-22)""")

add("26: Appendix A: the old mu",
    """- **μ.** A breadth-first search over the defender's moves alone (king and pawns), with the other side's
  context pawns fixed and its king absent. It covers every context position reachable inside the e-file
  context.""",
    """- **μ.** A breadth-first search over the defender's moves alone (king and pawns), with the other side's
  context pawns fixed and its king absent. It covers every context position reachable inside the e-file
  context. (This is the μ_s before K7. Definition 2.6 now counts the defender's king and the context pawns only,
  with s̄'s king and all Z-pawns deleted and the e.p. clause. The K7 checks below use the new count; revised after
  K7, 2026-10-22.)""")

t = t.rstrip("\n") + "\n\n" + "\n".join(new)
open(S + "r2/final_edits5.txt", "w").write(t)
print("ok", t.count("### EDIT"))
