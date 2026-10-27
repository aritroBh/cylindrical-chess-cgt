"""K19 claim 5.5: Z_on = Ka4 Pb2 / kc4 pb3 (8x6 cylinder). Black's king moves (sorties m), White's reply r = Kxb3,
then the local game with attacker White (king confined to {a,b,c}) against a defender (Black) that may pass:
T for pass budgets k = 0..8 and unlimited; the unbounded least fixed point with no passes and with unlimited passes."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from k19engine import *
from localgame import Local

B = parse_board('cyl:8x6')
root = parse_pos(B, 'Ka4 kc4 Pb2 pb3 b -')
print('root', fmt_pos(B, root))
mv = legal_moves(B, root)
print('Black legal moves:', ' '.join(('k' if m.frm == root[1] else 'p') + B.name(m.to) + ('x' if m.cap else '') for m in mv))
for sq in ['c3']:
    print('Kc3 legal?', any(m.to == B.sq(sq) and m.frm == root[1] for m in mv), '(white pawn b2 attacks c3 and a3)')
conf = {B.file[B.sq('a1')], B.file[B.sq('b1')], B.file[B.sq('c1')]}
rows = []
for m in [x for x in mv if x.frm == root[1]]:
    rec = {'sortie': 'k' + B.name(m.to)}
    reps = legal_moves(B, m.pos)
    rec['white_replies'] = [('K' if x.frm == m.pos[0] else 'P') + B.name(x.to) + ('x' if x.cap else '') for x in reps]
    r = [x for x in reps if x.frm == m.pos[0] and x.to == B.sq('b3')]
    if not r:
        rec['note'] = 'Kxb3 not legal'
        rows.append(rec)
        print(json.dumps(rec))
        continue
    Q = r[0].pos
    rec['Q'] = fmt_pos(B, Q)
    for label, kw in [('K7_queen', dict(queen=True, mate_win=True)), ('K7_P', dict(queen=False, mate_win=True))]:
        L = Local(B, 0, conf=conf, **kw)
        rec['T_' + label] = {('inf' if k is None else k): L.minT(Q, k, tmax=14) for k in (0, 1, 2, 3, 4, 5, 6, 8, None)}
        rec['lfp_' + label] = {'no_passes': L.lfp(Q, False)[0], 'passes': L.lfp(Q, True)[0]}
    Lu = Local(B, 0, conf=None, queen=True, mate_win=True)
    rec['lfp_unconfined_queen'] = {'no_passes': Lu.lfp(Q, False)[0], 'passes': Lu.lfp(Q, True)[0]}
    rows.append(rec)
    print(json.dumps(rec), flush=True)
json.dump(rows, open(os.path.join(os.path.dirname(__file__), '..', 'claim55.json'), 'w'), indent=1)
