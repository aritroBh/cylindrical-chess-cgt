"""K19: the Black side of 5.1 (claimed self-dual): Black's legal king moves at the root, the reply Kxa5 by White,
local game with attacker White (king confined to {h,a,b}); T for budgets and (L3); plus the enumeration of both
sides' king moves of the bare group."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from k19engine import *
from localgame import Local

B = parse_board('cyl:8x8')
conf = {7, 0, 1}
broot = parse_pos(B, 'Kh5 kb4 Pa4 pa5 b -')
bm = legal_moves(B, broot)
print('Black legal moves at the root (Black to move):', ['k' + B.name(m.to) + ('x' if m.cap else '') for m in bm])
print('Is Kb5 legal?', any(m.to == B.sq('b5') for m in bm), '; Kb3 legal?', any(m.to == B.sq('b3') for m in bm))
print('White pawn a4 attacks', [B.name(s) for s in B.pcap[0][B.sq('a4')]], '; Black pawn a5 attacks', [B.name(s) for s in B.pcap[1][B.sq('a5')]])
rows = []
for m in bm:
    rec = {'sortie': 'k' + B.name(m.to)}
    reps = legal_moves(B, m.pos)
    r = [x for x in reps if x.frm == m.pos[0] and x.to == B.sq('a5')]
    rec['white_replies'] = [('K' if x.frm == m.pos[0] else 'P') + B.name(x.to) + ('x' if x.cap else '') for x in reps]
    if not r:
        rec['note'] = 'Kxa5 not legal'
        rows.append(rec); print(json.dumps(rec)); continue
    Q = r[0].pos
    rec['Q'] = fmt_pos(B, Q)
    for label, kw in [('K7_queen', dict(queen=True, mate_win=True)), ('K7_P', dict(queen=False, mate_win=True))]:
        L = Local(B, 0, conf=conf, **kw)
        rec['T_' + label] = {('inf' if k is None else k): L.minT(Q, k, tmax=12) for k in (0, 1, 2, 3, 4, 5, 6, None)}
    L = Local(B, 0, conf=conf, queen=True, mate_win=True)
    Tq = rec['T_K7_queen']['inf']
    rec['L3_queen'] = {T: L.L3_root(Q, T) for T in range(Tq, Tq + 3)}
    rows.append(rec)
    print(json.dumps(rec), flush=True)
# the position after Kb3?? and the non-capturing Black moves: is White in zugzwang after the 'fifth' move?
json.dump(rows, open(os.path.join(os.path.dirname(__file__), '..', 'claim51b.json'), 'w'), indent=1)
