#!/usr/bin/env python3
"""make_edits.py: writes EDITS.md. Every OLD block is cut from the current LOOPY.md by line range (so it is exact) and the
script asserts that it occurs exactly once."""
import sys
L = open('/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md').read()
lines = L.split('\n')
def cut(a, b):  # 1-based inclusive line range
    return '\n'.join(lines[a - 1:b])
edits = []
def add(label, old, new):
    assert L.count(old) == 1, (label, L.count(old))
    edits.append((label, old, new))

# E1: Proposition 2.10(b), last bullet
add('P2.10(b): split the conjecture; the example', cut(1129, 1133), """  - So (L2) fails there, and a punishment with T ≥ 2 is never certified for all contexts. That statement is PROVED.
    Whether the freeze itself fails is a different statement. It is split below (K23, 2026-10-27; all values are
    exact, in P with real kings, from the private `--pmodel` build of `kpsolve.c` and an independent solver
    `kings/delegate/out/K23/scripts/pk2.c`).
  - *Definition (the zero beside a context, in P).* For a group Z and a context G (Definition 2.1) let Φ(G ⊞ Z) be the
    pair (w, b) of P results, White to move and Black to move, from White's view. Let Ψ(G) be the same pair in the
    frozen model `kpsolve --frozen` (a king move loses at once, a promotion wins at once, stalemate draws). Ψ(G) is
    "the result of G": it does not depend on the kings (K23: 1,770 positions of cyl:7×6, Z_T against parked kings
    `Ka1 ka6`, 0 differences; CHECKED-2). **Z acts as 0 beside G (in P)** if Φ(G ⊞ Z) = Ψ(G).
  - **PROVED by example, in P (CHECKED-2: two independent implementations agree on every number): the zero of a
    frozen group depends on the context.** Z_T = `Ka4 Pb3 kc3 pb4` on cyl:7×6 (the trébuchet of P4, Pattern A of §5.1 with r = 3), and two
    locked context pairs, each a single file with no passer and no move, so each has the value 0 and Ψ = (L, W):
    - G1 = {Pe3, pe4}: Φ = (L, W) = Ψ(G1). Z_T acts as 0 beside G1.
    - G2 = {Pe2, pe3}: Φ = (L, L) ≠ (L, W) = Ψ(G2). Black to move wins by the sortie 1...Kd2, the only winning move
      (Kc2, Kb2, Kd4 lose; Kd3 is illegal, the pawn e2 covers it). Z_T does not act as 0 beside G2.
    - The mirror (colours swapped, ranks reversed, files reflected about b) is G2′ = {Pf4, pf5}: Φ = (W, W) ≠ (L, W),
      White to move wins by Kg5; and G1′ = {Pf3, pf4} behaves as G1.
    - Same on the group of §5.1 on cyl:8×8 (`Kh5 Pa4 kb4 pa5`, contexts on d–f, ranks 2–7): {Pe3, pe4} gives (L, W) and
      {Pe2, pe3} gives (L, L); {Pe6, pe7} gives (W, W).
    - *Mechanism: a timing tie, decided by one tempo.* 1...Kd2 steps onto the buffer file next to the context. If White
      punishes the sortie with 2.Kxb4, the b-pawn is free but its own king stands in front of it: it needs a step aside
      and three pushes, four moves, with White to move after Black's capture. Black replies 2...Kxe2 in G2 and
      2...Kxe3 in G1, which makes the black context pawn a passer (every other White reply loses as well, by the solver). In G2 that pawn needs three more moves (king
      steps off, e2, e1=Q), in G1 four (king steps off, e3, e2, e1=Q). White moves first, so White's fourth move is
      before Black's fourth but after Black's third. The two race positions confirm it: `Kb4 Pb3 ke2 pe3`, White to
      move, is lost for White; `Kb4 Pb3 ke3 pe4`, White to move, is won. In P a promotion ends the game, so no queen is
      ever captured. In the terms of Theorem 2.7: with the king's help μ_s = 4 in G2 and 5 in G1, against a punisher
      that needs 4 moves, so (L2) holds in G1 (μ_s = T + 1) and fails in G2 (μ_s = T) by exactly one tempo. This
      counts the race by hand; the local game of Definition 2.6 was not run, so (L1) with T = 4 is not certified.
      The sortie is punished only if no context pawn becomes a passer that is at most as slow as the punisher.
    - *Distance.* On cyl:8×6 (Z_T on a–c, buffer d and h, context on e–g) the same pair {Pe2, pe3} fails, and moved one
      file away, {Pf2, pf3} and {Pg2, pg3}, it holds (and so do all rank shifts on f and g, except the mirror image
      {Pg4, pg5} of G2). Over all 4,579 contexts on e–g with at most two pawns of each colour
      on ranks 2–5, 152 have Φ ≠ Ψ, and every one has a pawn on e or g, the files next to the buffer; none of the 62
      contexts confined to f differs, and neither does any of the 81 single-file contexts on f with up to four pawns of
      each colour (CHECKED-2). So the failure needs a context pawn within a step of the buffer file the sortie king
      enters.
    - *The six P4 contexts do not show it in P.* In P all six rows of P4 equal the convention (CHECKED-2), including
      H*, H*2 and H0, so the draws that kpsolve finds there in C are facts about chess (A_Q fails), not about P.
    - *Scope.* Z_T on cyl:7×6, contexts on e–f with at most two pawns of each colour on ranks 2–5 (885 contexts):
      838 have Φ = Ψ and 47 do not (43 of the 47 have no passer; with at most three pawns of each colour, 3,237
      contexts, 99 differ). In the 23 passer-free contexts with Ψ = (L, W)
      that differ, the side to move loses in Ψ and not in P in 26 (context, side to move) pairs, and in all 26 a
      king step to the buffer file (Kd2 or Kd3 for Black; Kg3, Kg4 or Kg5 for White) is among its moves that do not
      lose. Among these positions are cases of Corollary 2.7′: `--frozen` reports a win for σ and σ does not win P
      (G2 with Black to move: `--frozen` is a White win, P is a Black win).
  - **CONJECTURE (what remains): the general statement.** For each frozen group with T ≥ 2 there is a context, with
    the defender in zugzwang there, where the freeze fails in P. **A proof is not available as stated, and the
    obstacle is not technical.** T belongs to a certificate, not to a group. A failure needs three things at once for
    one sortie m: (i) the sortie king can reach a buffer square next to a context pawn it can capture (here Kd2, Kg4,
    Kg5), which depends on where the kings stand in Z; (ii) the counter-passer that results is no slower than the
    punisher's *exact* P-win, not the bound T of (L1); (iii) s has no other loss on the way. A converse of Theorem
    2.7 (μ_s ≤ T implies that m is not punished) is false in general (see "No converse"), because s̄ may win faster
    than T or by another reply. So the statement can be settled only group by group, by solving. What is settled: Z_T
    on cyl:7×6, cyl:8×6 and the group of §5.1 on cyl:8×8. What is open: groups in which no sortie king can reach the
    buffer in time (they might be universal zeros even with T ≥ 2), and every group other than these two.""")

# E2: status table row
add('status table: P2.10(b) row', cut(75, 75),
    '| P2.10(b) | PROVED (the example; it needs width ≥ \\|F_Z\\| + 4). "The zero is context-dependent": PROVED by example in P (CHECKED-2, K23: Z_T beside {Pe3, pe4} and {Pe2, pe3} on cyl:7×6, also the group of §5.1 on cyl:8×8); the general statement for every frozen group with T ≥ 2 is a CONJECTURE. P4 supports it in C only; in P its six rows equal the convention | R3 item 5; K23 |')

# E3: status table P4 row
add('status table: P4 row', cut(97, 97),
    '| P4 | CONJECTURE → **refuted** by kpsolve in 3 of 6 contexts (H\\*, H\\*2, H0), in C. In P all six rows equal the convention (CHECKED-2, K23), so the refutation is a fact about chess (A_Q), not about P | PREDICTIONS.md, theory_P4_cap2_moves.txt; K23 |')

# E4: summary
add('section 0: the conjecture sentence', cut(154, 155),
    """  so a slower punishment's zero is not certified in every context. That it is context-dependent is PROVED by example
  in P (Z_T beside {Pe3, pe4} and {Pe2, pe3}, CHECKED-2, K23); for every frozen group with T ≥ 2 it is a CONJECTURE.""")

# E5: S2 paragraph
add('section 7, (S2): P4 with H0', cut(627, 630),
    """  and White's Ka6 is not a P-loss; reading (b) is the one that applies (Proposition 3.2). P4 with H0, Black to
  move: in C Black's king sorties Kd3 and Kd2 are legal Z-moves of the loser that do not lose (a king-context
  interaction; kpsolve with cap 2 gives a draw instead of the predicted (L, W); COMPUTED-1 in C). In P both sorties
  lose and the position is (L, W), as predicted (CHECKED-2, K23), so this (S2) case is a fact about chess.""")

# E6: P6 row
old = [l for l in lines if l.startswith('| P6 | cyl:8x8 |')]
assert len(old) == 1
add('section 6: P6 row', old[0], old[0].replace('| CONJECTURE; kpsolve agrees |', '| CONJECTURE; kpsolve agrees. The P value (L, W) is exact and CHECKED-2 (K23) |'))

# E7: new row P13 before the notes
add('section 6: new row P13',
    "the chess form needs (A_Q) (revised after K7, 2026-10-22) |\n\n**Notes on the table.**",
    "the chess form needs (A_Q) (revised after K7, 2026-10-22) |\n"
    "| P13 | cyl:7x6; cyl:8x8 | Z_T `Ka4 Pb3 kc3 pb4` beside G1 = `Pe3 pe4` and G2 = `Pe2 pe3`; on cyl:8x8 the group of §5.1 `Kh5 Pa4 kb4 pa5` beside the same pairs | G1 (L, W); for G2 the theory only says that (L2) can fail (Proposition 2.10(b)), it does not predict the value | G1 and G2 both (L, W) | P (exact): G1 (L, W), G2 (L, L) on both boards; C not run (cap 2 is too large on cyl:7×6) | Prop 2.10(b) + Thm 2.7 with μ_s = T in G2 (hand race count, §2 after Proposition 2.10(b)) | the numbers are CHECKED-2 (K23); the failure of the zero in P is PROVED by example |\n\n**Notes on the table.**")

# E8: notes on P4
add('section 6 notes: what P4 tests', cut(1889, 1890),
    """- **What P4 tests, and how it failed.** P4 was the positive control: the theory predicts that the convention
  is *right* there. kpsolve refutes it in 3 of the 6 contexts, in C. In P all six rows equal the convention
  (CHECKED-2, K23: `kings/delegate/out/K23/logs/key_digest.txt`), so the three refutations are facts about chess
  (A_Q fails after the promotion), and P4 does not show a context-dependent zero in P; P13 does.""")
add('section 6 notes: P4 mechanism sentence', cut(1895, 1898),
    cut(1895, 1895) + """
    all lose, while Ka5, Kb4 and Kb5 draw. This is a chess mechanism: in P the same sorties lose, and the zero of Z_T
    is context-dependent in P for a different reason (P13: a timing tie of one tempo, Proposition 2.10(b)). The
    (L2) margin the theory assumed does not survive the context, in P in G2 and in C in H*, H*2 and H0.""")

# E9: open questions
add('section 8: open question 6', cut(1987, 1988),
    cut(1987, 1988) + """
6. **Universal zeros** (CONJECTURE, after Proposition 2.10(b)). The zero of Z_T is context-dependent in P (P13). Is
   there a frozen group with T ≥ 2 that acts as 0 beside every context, for instance one whose sortie king cannot reach
   the buffer before the punisher wins? Solving candidates exhaustively on contexts of at most two pawns a side, as
   K23 did for Z_T (`kings/delegate/out/K23/scripts/`), is cheap in P.""")

with open('EDITS.md', 'w') as f:
    for label, old, new in edits:
        f.write(f"### EDIT {label}\n<<<<<<< OLD\n{old}\n=======\n{new}\n>>>>>>> NEW\n\n")
print(len(edits), 'edits written')
