"""K19 claim 5.6: the engine-suite draw 8/8/3p4/5Kp1/6Pk/2P5/8/8 w (flat 8x8), White sortie Ke6, reply Kxg4.
mu_W (L2), T (L1) and the comparison mu >= T + 1."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from k19engine import *
from localgame import Local, mu_search

B = parse_board('flat:8x8')
root = parse_pos(B, 'Kf5 kh4 Pg4 Pc3 pg5 pd6 w -')
res = {}
print('root', fmt_pos(B, root))
mv = legal_moves(B, root)
print('White legal moves:', ' '.join(('K' if m.frm == root[0] else 'P') + B.name(m.to) + ('x' if m.cap else '') for m in mv))
m = [x for x in mv if x.frm == root[0] and x.to == B.sq('e6')][0]
reps = legal_moves(B, m.pos)
print('Black replies after Ke6:', ' '.join(('K' if x.frm == m.pos[1] else 'p') + B.name(x.to) + ('x' if x.cap else '') for x in reps))
r = [x for x in reps if x.frm == m.pos[1] and x.to == B.sq('g4')][0]
Q = r.pos
print('Q =', fmt_pos(B, Q))
# projection onto F_Z = {f,g,h}: delete pawns off F_Z (c3, d6)
FZ = {B.file[B.sq('f1')], B.file[B.sq('g1')], B.file[B.sq('h1')]}
QZ = (Q[0], Q[1], tuple(p for p in Q[2] if B.file[p] in FZ), tuple(p for p in Q[3] if B.file[p] in FZ), -1, Q[5])
print('Q_Z =', fmt_pos(B, QZ))
# (L2): context pawns of both colours stay, s = White, Z-pawns and Black king deleted
ctx_w = [p for p in Q[2] if B.file[p] not in FZ]
ctx_b = [p for p in Q[3] if B.file[p] not in FZ]
res['mu_W'] = mu_search(B, 0, Q[0], ctx_w, ctx_b)
print('mu_W (king e6, context pawns c3 / d6):', res['mu_W'])
res['mu_W_no_enemy_pawn'] = mu_search(B, 0, Q[0], ctx_w, [])
print('mu_W with d6 removed:', res['mu_W_no_enemy_pawn'])
res['mu_W_pawn_only'] = None
# (L1)
for label, kw, conf in [('K7_queen_confined', dict(queen=True, mate_win=True), FZ), ('K7_P_confined', dict(queen=False, mate_win=True), FZ),
                        ('K7_queen_unconfined', dict(queen=True, mate_win=True), None),
                        ('old_nomate_queen_confined', dict(queen=True, mate_win=False), FZ)]:
    L = Local(B, 1, conf=conf, **kw)
    T = {('inf' if k is None else k): L.minT(QZ, k, tmax=10) for k in (0, 1, 2, 3, 4, None)}
    res['T_' + label] = T
    print('T', label, T)
L = Local(B, 1, conf=FZ, queen=True, mate_win=True)
Tq = L.minT(QZ, None)
res['L3_T'] = {T: L.L3_root(QZ, T) for T in range(Tq, Tq + 3)}
print('L3 at T =', res['L3_T'])
# Also the full position's local game with the context pawns kept (not the projection): sanity (A = Black)
Lfull = Local(B, 1, conf=FZ, queen=True, mate_win=True)
res['T_with_context_pawns_kept'] = Lfull.minT(Q, None, tmax=10)
print('T with context pawns kept in the local game (not the definition):', res['T_with_context_pawns_kept'])
# unbounded: does Black win at all?
res['lfp_unbounded_inf_passes'] = Local(B, 1, conf=FZ, queen=True, mate_win=True).lfp(QZ, True)
print('unbounded local game, passes:', res['lfp_unbounded_inf_passes'])
# remark in 5.1: a single free White pawn on rank 2 of an 8-rank board has mu = 5
B8 = parse_board('cyl:8x8')
res['mu_single_pawn_rank2'] = mu_search(B8, 0, B8.sq('h1'), [B8.sq('b2')], [])
print('mu of a single free pawn on rank 2 (8 ranks):', res['mu_single_pawn_rank2'])
res['mu_single_pawn_rank2_black'] = mu_search(B8, 1, B8.sq('h8'), [B8.sq('b7')], [])
json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'claim56.json'), 'w'), indent=1, default=str)
