import sys
from r2_lib import *
for kind in ('cyl', 'flat'):
    B = Board(kind)
    corners = {0, 7, 56, 63} if kind == 'flat' else set()
    mx = 0; mxc = 0; fails = 0; nfail_nc = 0; n = 0
    for s in range(64):
        for t in range(64):
            if t == s or B.adj[s][t]: continue
            common = [x for x in B.nb[s] if B.adj[x][t]]
            if s in corners: mxc = max(mxc, len(common))
            else: mx = max(mx, len(common))
            for p in (-1, sqn('d7'), sqn('e7')):
                if p in (s, t): continue
                n += 1
                free = [x for x in B.nb[s] if not B.adj[x][t] and x != t and x != p]
                if not free: fails += 1
                if s not in corners and not [x for x in free if x not in corners]: nfail_nc += 1
    print(kind, 'max |N(s)&N(t)| non-corner s:', mx, ' corner s:', mxc, '; cases', n, '; no free move:', fails, '; no free non-corner move (s not a corner):', nfail_nc)
