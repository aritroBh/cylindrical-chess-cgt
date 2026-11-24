"""K56: results of over_D (+) T and of T alone (= 0_D (+) T) for test games T in the K47/K55 line format.
over_D has positions w (omega) and z (0_D): L(w) = {z}, R(w) = {w}, z has no options (LOOPY Proposition 4.6).
Rules of the D-sum (Definition 1.3): a move to a terminal W or B ends the play with that colour winning; a side with
no move loses; infinite play is a draw (least fixed point).  Output per game: name | over_w over_b | T_w T_b."""
import sys
def parse(line):
    name, n, rest = [x.strip() for x in line.split('|', 2)]
    n = int(n); L = [[] for _ in range(n)]; R = [[] for _ in range(n)]
    for item in rest.split(';'):
        item = item.strip()
        if not item: continue
        i, opts = item.split(':', 1); i = int(i)
        for part in opts.split():
            tag, val = part.split('=', 1)
            lst = L[i] if tag == 'L' else R[i]
            for v in val.split(','):
                if v == '': continue
                lst.append(v if v in ('W', 'B') else int(v))
    return name, n, L, R
def solve(states, opts):
    """states: list of (key, side); opts(key, side) -> list of ('T', 'W'|'B') or ('S', key'). Returns dict -> W/L/D."""
    res = {}
    for Y, mine in ((0, 'W'), (1, 'B')):
        win = set(); changed = True
        while changed:
            changed = False
            for st in states:
                if st in win: continue
                k, s = st; os_ = opts(k, s)
                def good(o):
                    return (o[1] == mine) if o[0] == 'T' else ((o[1], 1 - s) in win)
                if s == Y: ok = any(good(o) for o in os_)
                else: ok = all(good(o) for o in os_)
                if ok: win.add(st); changed = True
        for st in states:
            if st in win: res[st] = res.get(st, '') + mine
    return {st: ('W' if res.get(st) == 'W' else 'L' if res.get(st) == 'B' else 'D' if st not in res else '?') for st in states}
def results(line):
    name, n, L, R = parse(line)
    def topts(t, s):
        return [('T', o) if o in ('W', 'B') else ('S', o) for o in (L[t] if s == 0 else R[t])]
    # T alone
    st = [(t, s) for t in range(n) for s in (0, 1)]
    rt = solve(st, topts)
    # over (+) T
    st2 = [((o, t), s) for o in 'wz' for t in range(n) for s in (0, 1)]
    def oopts(k, s):
        o, t = k; out = []
        for x in topts(t, s): out.append(x if x[0] == 'T' else ('S', (o, x[1])))
        if o == 'w': out.append(('S', ('z', t)) if s == 0 else ('S', ('w', t)))
        return out
    ro = solve(st2, oopts)
    return name, ro[(('w', 0), 0)], ro[(('w', 0), 1)], rt[(0, 0)], rt[(0, 1)]
if __name__ == '__main__':
    for line in open(sys.argv[1]):
        if '|' not in line: continue
        print('%s | %s %s | %s %s' % results(line))
