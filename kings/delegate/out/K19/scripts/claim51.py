"""K19 claim 5.1: the frozen trebuchet Kh5 Pa4 / kb4 pa5 on the 8x8 cylinder.
For each legal White move m (the sorties) and the reply r = Kxa4: the local game (L1) with attacker Black
(king confined to {h,a,b}), defender White passing; T for budgets k = 0..8 and unlimited, for the K7 rules and
the pre-K7 rules; (L1_P) without the queen clause; (L3) in the real window. Output: JSON lines + a table."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from k19engine import *
from localgame import Local

B = parse_board('cyl:8x8')
root = parse_pos(B, 'Kh5 kb4 Pa4 pa5 w -')
conf = {B.file[B.sq('h1')], B.file[B.sq('a1')], B.file[B.sq('b1')]}
out = {}
print('root', fmt_pos(B, root))
moves = legal_moves(B, root)
print('White legal moves:', ' '.join(B.name(m.frm) + B.name(m.to) for m in moves))
sorties = [m for m in moves if m.frm == root[0]]
print('sorties (king moves):', ' '.join('K' + B.name(m.to) for m in sorties))
rows = []
for m in sorties:
    # Black's replies: all legal moves; the standard reply r = king captures a4
    reps = legal_moves(B, m.pos)
    names = [('K' if x.frm == m.pos[1] else 'p') + B.name(x.to) + ('x' if x.cap else '') for x in reps]
    r = [x for x in reps if x.frm == m.pos[1] and x.to == B.sq('a4')]
    rec = {'sortie': 'K' + B.name(m.to), 'black_replies': names}
    if not r:
        rec['note'] = 'Kxa4 not legal'
        rows.append(rec)
        continue
    Q = r[0].pos
    rec['Q'] = fmt_pos(B, Q)
    for label, kw in [('K7_queen', dict(queen=True, mate_win=True)), ('K7_P', dict(queen=False, mate_win=True)),
                      ('old_queen_nomate', dict(queen=True, mate_win=False)), ('old_P_nomate', dict(queen=False, mate_win=False))]:
        L = Local(B, 1, conf=conf, **kw)
        Ts = {}
        for k in [0, 1, 2, 3, 4, 5, 6, 7, 8, None]:
            Ts['inf' if k is None else k] = L.minT(Q, k, tmax=12)
        rec[label] = Ts
    # unconfined version (K7 queen rules, unlimited passes)
    L = Local(B, 1, conf=None, queen=True, mate_win=True)
    rec['unconfined_K7_queen_inf'] = L.minT(Q, None, tmax=12)
    # (L3)
    L = Local(B, 1, conf=conf, queen=True, mate_win=True)
    Tq = rec['K7_queen']['inf']
    rec['L3_queen'] = {T: L.L3_root(Q, T) for T in range(Tq, Tq + 3)}
    Lp = Local(B, 1, conf=conf, queen=False, mate_win=True)
    Tp = rec['K7_P']['inf']
    rec['L3_P'] = {T: Lp.L3_root(Q, T) for T in range(Tp, Tp + 3)}
    rows.append(rec)
    print(json.dumps(rec), flush=True)
json.dump(rows, open(os.path.join(os.path.dirname(__file__), '..', 'claim51.json'), 'w'), indent=1)
