#!/usr/bin/env python3
"""K15 fin2: principal variation (shortest forced win for the punisher, longest defence) after a deviation.  Own generator oneply.py; model P.
usage: pv.py W H flat 'root' MOVE   (MOVE like Kb2b1, Pb4b5, Kc4d5)"""
import sys, functools
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2/scripts')
import oneply as O
W, H, flat = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3] == '1'
g = O.G(W, H, flat)
def opp(s): return 'B' if s == 'W' else 'W'
@functools.lru_cache(maxsize=None)
def wins(pos, stm, who, d):
    if d <= 0: return False
    mv = g.moves(pos, stm)
    if stm == who:
        return any(npos is None or wins(npos, opp(stm), who, d - 1) for m, npos in mv)
    if not mv: return O.in_check(g, pos, stm)
    return all(npos is not None and wins(npos, opp(stm), who, d - 1) for m, npos in mv)
def nm(m):
    return ('' if m[0] == 'K' else '') + O.nm(m[1]) + ('x' if m[3] is True else '-') + O.nm(m[2]) + ('=Q' if m[3] == 'promo' else '')
root = sys.argv[4]; mv = sys.argv[5]
pos = O.parse(root); side = root.split()[-2].upper(); o = opp(side)
for m, npos in g.moves(pos, side):
    if ('K' if m[0] == 'K' else 'P') + O.nm(m[1]) + O.nm(m[2]) == mv:
        d = next(d for d in range(1, 40) if wins(npos, o, o, d))
        line = [nm(m)]; cur = npos; stm = o; left = d
        while left > 0:
            mvs = g.moves(cur, stm)
            if stm == o:  # punisher: a move that wins within left-1
                for mm, nn in mvs:
                    if nn is None: line.append(nm(mm)); left = 0; break
                    if wins(nn, opp(stm), o, left - 1): line.append(nm(mm)); cur = nn; break
            else:         # defender: the reply that holds out longest
                best = None
                for mm, nn in mvs:
                    if nn is None: continue
                    dd = next((x for x in range(1, left) if wins(nn, opp(stm), o, x)), 99)
                    if best is None or dd > best[0]: best = (dd, mm, nn)
                if best is None: line.append('#'); break
                line.append(nm(best[1])); cur = best[2]
            stm = opp(stm); left -= 1
        print('%s %s: %s   (%d plies after the move)' % (root, mv, ' '.join(line), d))
