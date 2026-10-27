#!/usr/bin/env python3
"""Build EDITS.md for LOOPY.md from the current LOOPY.md (read only) and summary.json. Run after summarize.py."""
import json, sys
LOOPY = '/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md'
S = json.load(open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22/summary.json'))
T = S['totals']
text = open(LOOPY).read()
lines = text.split('\n')
def find(prefix):
    c = [l for l in lines if l.startswith(prefix)]
    assert len(c) == 1, (prefix, len(c))
    return c[0]
old_status = find('| L2.9 | GAP → PROVED after repair')
old_sum = find('| L2.9 | Blockade:')
i0 = next(i for i, l in enumerate(lines) if l.startswith('**Lemma 2.9 (blockade).'))
i1 = next(i for i, l in enumerate(lines) if l.startswith('after review: R1 item 9, R3 item 4).') or l.startswith('letting an s̄ pawn leave f).'))
# the block ends with the line "after review: R1 item 9, R3 item 4)."
i1 = next(i for i, l in enumerate(lines) if i > i0 and l == 'after review: R1 item 9, R3 item 4).')
old_lemma = '\n'.join(lines[i0:i1 + 1])
for o in (old_status, old_sum, old_lemma):
    assert text.count(o) == 1

roots = T['roots']; r2 = T['roots2']; w = T['wins']
new_status = ("| L2.9 | GAP → PROVED after repair, now under the weaker hypothesis (B1): at most one s̄ pawn is attacked by an s pawn "
 "(it holds if s has no pawn on f ± 1, if s̄ has a single Z-pawn, and automatically on 4-rank boards). **The conjecture for the statement without any hypothesis is "
 "REFUTED**: with two attacked s̄ pawns s can lose, for example cyl:7×6 `Ka5 kc6 Pc3 Pc4 pb4 pb5` with Black (s) to move, F_Z = {a, b, c} (a forced promotion in 3 moves "
 "against a defender who may pass; also a P-win with real kings; CHECKED-2 and a P-model run; hand-verified for the 4×5 version `Kd4 kb5 Pb2 Pb3 pc3 pc4`). "
 "Exhaustive search (K22, up to 3 + 3 pawns, and 4 + 4 on small boards): no exception to (B1) in %s roots (COMPUTED-1, a sample re-checked by an independent Python solver) | R1 item 9, R3 item 4; K22 |" % format(roots, ','))
new_sum = ("| L2.9 | Blockade: a defender who may pass and whose king stands in front of the pawn is never beaten, provided at most one s̄ pawn is attacked by an s pawn (B1) | "
 "PROVED after repair under (B1) (it covers “s has no pawn on f ± 1” and “s̄ has one Z-pawn”). Without (B1) it is FALSE (K22: counterexamples with two attacked s̄ pawns) |")
new_lemma = '''**Lemma 2.9 (blockade). PROVED after repair, under the hypothesis (B1) (revised after K22, 2026-10-27).** In Q_Z, suppose:
- all of s̄'s Z-pawns stand on one file f, and s's king stands on a square of f in front of s̄'s front pawn, so above every s̄ pawn;
- **(B1)** at most one s̄ pawn is *attacked by an s pawn*. An s̄ pawn on (f, x) is attacked iff an s pawn stands on the square
  diagonally in front of it (on file f ± 1, one rank on in s̄'s direction). The relation is symmetric: the two pawns attack each
  other, and the one that is to move may capture. (B1) holds if s has no pawn on f ± 1 (the earlier hypothesis), whenever s̄ has
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
  pins; the king stands where it was). If an s̄ pawn P is attacked, the capture removes P. The capturing pawn Q came from file
  f ± 1 and lands on f, so it attacks no square of file f; and Q attacked only P among s̄'s pawns (it attacks two squares, both on
  files at distance 1 from Q's file, and at most one of them is on f, apart from the width-2 cylinder where both squares coincide).
  The other pairs are untouched. So after s's move (J2) holds, and (J1) holds, since P was the only pawn removed.
By induction, no s̄ pawn promotes, and none ever leaves f; s is never in check at its turns, so it is never mated. s̄ cannot win L_T for
any T. ∎ (The proof does not use that s̄'s king is confined to F_Z, nor the move count.)

**Remark (K22: the hypothesis (B1) is needed, and it is not necessary).**
- *Without (B1) the lemma is FALSE.* The earlier proof ("s passes forever") fails when an s̄ pawn can capture an s pawn. The repair
  suggested in review R3 item 4 ("pass, but capture any s̄ pawn that attacks an s pawn") fails too, as soon as two s̄ pawns are
  attacked: s captures one and s̄ captures with the other, and the pawn that has left f is no longer blockaded. (Counterexamples,
  all with Black = s to move, the local game of Definition 2.6 with k = ∞ and no queen clause or with it.)
  - cyl:7×6, F_Z = {a, b, c}: `Ka5 kc6 Pc3 Pc4 pb4 pb5`. s̄ = White has two Z-pawns on c, s has b4, b5 (b4 attacks c3, b5 attacks c4).
    After 1…bxc4 White plays 2.cxb4, and the pawn runs to b6, which Ka5 guards; the black king cannot step to b5 or b6. Every Black move
    loses, the pass included (3 White moves at most). The same position is a White win in P with real kings (`kp_p --pmodel`); each of
    Black's five legal moves loses.
  - flat:4×5, F_Z = {a, b, c, d}: `Kd4 kb5 Pb2 Pb3 pc3 pc4`: each Black move, the pass included, loses within 3 White moves. After
    a pass, 2.bxc4+ and 3.c5=Q (c4 and c5 are guarded by Kd4); after 1…cxb3 2.bxc3, a black pawn run is too slow because c3–c4 gives
    check to the king on b5. Hand-verified.
  - The smallest board is 5 ranks, because (B1) is automatic on 4 ranks; the counterexamples need two s̄ pawns on f and two s pawns.
- *(B1) is sufficient and not necessary.* Two attacked s̄ pawns lose only in some positions: among the %s roots of the search with
  two or more attacked s̄ pawns, s̄ wins %s (about %s%%); the king positions decide.
- The uses in §5.2, P5 and P7 are unaffected: there s has no pawn at all (and s̄ has one Z-pawn).
''' % (format(r2, ','), format(T['wins2'], ','), ('%.1f' % (100.0 * T['wins2'] / r2)))
edits = []
def block(label, old, new):
    return '### EDIT %s\n<<<<<<< OLD\n%s\n=======\n%s\n>>>>>>> NEW\n' % (label, old, new)
out = block('L2.9 status row', old_status, new_status) + '\n' + block('L2.9 summary row', old_sum, new_sum) + '\n' + block('Lemma 2.9 statement and proof', old_lemma, new_lemma.rstrip('\n'))
open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22/EDITS.md', 'w').write(out)
print('EDITS.md written;', len(out), 'bytes')
