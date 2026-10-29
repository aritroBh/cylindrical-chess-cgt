import sys; sys.path.insert(0, 'scripts')
from lk_py import *
lk = LK(6, 6, False, [(0, 2), (2, 4)])
opts, S_, win = solve(lk, 2)
x = parse(lk, 'Kc3 ka4 Pa2 pa3 Pc4 pc5')
def res(st):
    w = win[0].get(st); b = win[1].get(st)
    return ('W%d' % w) if w is not None else (('L%d' % b) if b is not None else 'D')
for c in (-2, -1, 0, 1, 2):
    print('c=%+d' % c, 'White to move', res((x, c, 0)), ' Black to move', res((x, c, 1)))

def show(st):
    x, c, s = st
    S, wk, bk = x
    return 'K%s k%s %s to move, reserve %+d' % (name(wk), name(bk), 'White' if s == 0 else 'Black', c)
def outcome(st):
    w = win[0].get(st); b = win[1].get(st)
    return ('W', w) if w is not None else (('L', b) if b is not None else ('D', None))
def pv(st, maxply=40):
    """principal variation: the winner minimises, the loser maximises the distance; prints moves."""
    o = outcome(st)
    if o[0] == 'D': return
    player = 0 if o[0] == 'W' else 1
    dist = win[player]
    line = []
    for _ in range(maxply):
        x, c, s = st
        succ = S_[st]
        # terminals
        winT = 1 if player == 0 else -1
        cands = []
        for k, v in succ:
            if k == 'T':
                if v == winT and s == player: cands.append((1, None, 'event'))
            else:
                if v in dist: cands.append((dist[v], v, None))
        if not cands: break
        if s == player:
            best = min(cands, key=lambda t: t[0])
        else:
            best = max(cands, key=lambda t: t[0])
        if best[1] is None:
            line.append('(' + ('White' if s == 0 else 'Black') + ' captures: event, ' + ('+ White' if player == 0 else '- Black') + ' wins)'); break
        nxt = best[1]
        # describe move
        (S1, w1, b1), c1, s1 = nxt
        if (S1, w1, b1) == x:
            mv = 'pass(reserve)'
        else:
            mv = ('K' + name(w1)) if s == 0 else ('k' + name(b1))
        line.append(mv)
        st = nxt
    return line
if __name__ == '__main__':
    for c, s in [(0, 1), (0, 0), (-1, 0), (-1, 1), (1, 0), (1, 1)]:
        st = (x, c, s); print(show(st), outcome(st), pv(st))
