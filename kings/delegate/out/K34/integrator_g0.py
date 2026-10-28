"""Integrator check of Proposition 3.2' (d), G = 0: delete each of the eight shuttle arrows of the exact four-state
two-shuttle Z (every other option a suicide) and print the D-results at all four states, White then Black to move.
Run: python3 kings/delegate/out/K34/integrator_g0.py   (written from Definition 1.2; independent of K14 and K34 code)"""
S = [(a, b) for a in (0, 1) for b in (0, 1)]
def solve(delW=None, delB=None):
    def opts(s, m):
        if m == 'W': return [] if s == delW else [((1 - s[0], s[1]), 'B')]
        return [] if s == delB else [((s[0], 1 - s[1]), 'W')]
    res = {}
    for side in 'WB':
        win, ch = set(), True
        while ch:
            ch = False
            for s in S:
                for m in 'WB':
                    n = (s, m)
                    if n in win: continue
                    o = opts(s, m)   # the mover's suicide never helps the mover; the opponent's suicide wins for side
                    if (any(x in win for x in o) if m == side else all(x in win for x in o)):
                        win.add(n); ch = True
        res[side] = win
    return {s: ''.join('W' if (s, m) in res['W'] else 'L' if (s, m) in res['B'] else 'D' for m in 'WB') for s in S}
base = solve()
print('exact Z:', base)
for s in S:
    for k in 'WB':
        r = solve(delW=s) if k == 'W' else solve(delB=s)
        print(f'delete the {k} shuttle at {s}: {sum(r[t] != base[t] for t in S)}/4 states change', r)
