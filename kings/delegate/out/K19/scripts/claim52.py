"""K19 claim 5.2 (pattern B, 7.2): Ke6 Pd7 / kd8 pe7 on the 8x8 cylinder, and its 6-rank analogue
Z_72 = Kc4 Pb5 / kb6 pc5 on the 7x6 cylinder.
(1) White's king moves (sorties) and the reply r = Kxd7 (Kxb5): local game with attacker Black (king confined
    to F_Z or not), defender White with no pass / unlimited passes: unbounded least fixed point, and T.
(2) Black's only move Kc7 (Kb7... in the analogue) and White's punishment T = 1.
(3) Own full-board P solver on the position after each sortie (Black to move), and bare, both sides to move."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from k19engine import *
from localgame import Local
from fullp import solve_p, white_pov


def run(spec, wpos, fz_files, name):
    B = parse_board(spec)
    root = parse_pos(B, wpos)
    out = {'board': spec, 'root': fmt_pos(B, root)}
    mv = legal_moves(B, root)
    out['white_moves'] = [('K' if m.frm == root[0] else 'P') + B.name(m.to) + ('x' if m.cap else '') for m in mv]
    broot = root[:5] + (1,)
    bm = legal_moves(B, broot)
    out['black_moves_bare'] = [('k' if m.frm == root[1] else 'p') + B.name(m.to) + ('x' if m.cap else '') for m in bm]
    conf = {ord(c) - 97 for c in fz_files}
    # the pawn that Black's king captures as the standard reply: White's pawn
    wpawn = root[2][0]
    sorties = {}
    for m in [x for x in mv if x.frm == root[0]]:
        rec = {}
        reps = legal_moves(B, m.pos)
        rec['black_replies'] = [('k' if x.frm == m.pos[1] else 'p') + B.name(x.to) + ('x' if x.cap else '') for x in reps]
        r = [x for x in reps if x.frm == m.pos[1] and x.to == wpawn]
        if not r:
            rec['note'] = 'king capture of the Z-pawn not legal'
            sorties['K' + B.name(m.to)] = rec
            continue
        Q = r[0].pos
        rec['Q'] = fmt_pos(B, Q)
        for label, kw, cf in [('K7_queen_conf', dict(queen=True, mate_win=True), conf), ('K7_P_conf', dict(queen=False, mate_win=True), conf),
                              ('K7_P_unconf', dict(queen=False, mate_win=True), None)]:
            L = Local(B, 1, conf=cf, **kw)
            rec['lfp_' + label] = {'no_passes': L.lfp(Q, False)[0], 'passes': L.lfp(Q, True)[0]}
            rec['T_' + label] = {('inf' if k is None else k): L.minT(Q, k, tmax=16) for k in (0, None)}
        sorties['K' + B.name(m.to)] = rec
        # full-board P value after the sortie, Black to move (my solver)
    out['sorties'] = sorties
    return out


res = {}
res['cyl8x8'] = run('cyl:8x8', 'Ke6 kd8 Pd7 pe7 w -', 'def', '7.2')
res['cyl7x6'] = run('cyl:7x6', 'Kc4 kb6 Pb5 pc5 w -', 'abc', 'Z72')
for key in res:
    r = res[key]
    print(key, r['root'])
    print('  White moves:', r['white_moves'], ' Black moves (bare):', r['black_moves_bare'])
    for s, rec in r['sorties'].items():
        print('  sortie', s, json.dumps(rec))
# (2) Black's only move and White's punishment (8x8)
B = parse_board('cyl:8x8')
broot = parse_pos(B, 'Ke6 kd8 Pd7 pe7 b -')
bm = legal_moves(B, broot)
print('Black moves in 7.2:', [B.name(m.to) for m in bm if m.frm == broot[1]])
m = [x for x in bm if x.frm == broot[1]][0]
reps = legal_moves(B, m.pos)
r = [x for x in reps if x.to == B.sq('e7')][0]
Q = r.pos
print('Q after Kc7 Kxe7:', fmt_pos(B, Q))
conf = {3, 4, 5}
L = Local(B, 0, conf=conf, queen=True, mate_win=True)
t1 = L.minT(Q, None, tmax=6)
print('T (attacker White) =', t1, '; (L3) at T:', L.L3_root(Q, t1))
res['black_kc7'] = {'T': t1, 'L3': L.L3_root(Q, t1), 'black_moves_after': [B.name(x.to) for x in legal_moves(B, Q)]}
json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'claim52.json'), 'w'), indent=1)
