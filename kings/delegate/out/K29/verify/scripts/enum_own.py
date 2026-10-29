#!/usr/bin/env python3
# own enumerator (referee K29, pass 2), independent of grp.c and of the earlier referee's ref3enum.cpp.
# enum_own.py BOARD(ref spelling) NAME ZS FZ OUT : all groups with kings on F_Z, W in 0..2 white and B in 0..2 black pawns on F_Z, ranks 2-5,
# at least one pawn, no e.p.; query ref3 (P model) for both sides to move; keep groups with (White to move: L, Black to move: W).
import sys, itertools, subprocess
board, name, zs, fz, out = sys.argv[1:6]; zs = int(zs); fz = int(fz)
Wd = int(''.join(c for c in board.split('x')[0] if c.isdigit()))
cyl = board.startswith('cyl')
files = [(zs + i) % Wd for i in range(fz)]
L = lambda f: 'abcdefgh'[f]
pawnsq = [L(f) + str(r) for f in files for r in range(2, 6)]
kingsq = [L(f) + str(r) for f in files for r in range(1, 7)]
def subs(k):
    for c in range(k + 1): yield from itertools.combinations(pawnsq, c)
B = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify/bin/ref3'
p = subprocess.Popen([B, '--board', board], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1 << 20)
import threading
meta = []
def feed():
    for Wp in subs(2):
        for Bp in subs(2):
            if not Wp and not Bp: continue
            if set(Wp) & set(Bp): continue
            pt = ['P' + s for s in Wp] + ['p' + s for s in Bp]
            for wk in kingsq:
                for bk in kingsq:
                    if wk == bk: continue
                    for stm in 'wb':
                        p.stdin.write(' '.join(['K' + wk, 'k' + bk] + pt + [stm, '-']) + '\n')
    p.stdin.close()
t = threading.Thread(target=feed); t.start()
res = {}
n = 0
for l in p.stdout:
    pos, r = l.rstrip('\n').rsplit(' | ', 1)
    toks = pos.split(); stm = toks[-2]; key = tuple(sorted(toks[:-2]))
    res.setdefault(key, {})[stm] = r; n += 1
t.join()
cands = [k for k, v in res.items() if v.get('w') == 'L' and v.get('b') == 'W']
with open(out, 'w') as f:
    for k in sorted(cands): f.write(' '.join(k) + '\n')
print(name, 'positions solved', n, 'distinct groups', len(res), 'candidates (L,W)', len(cands))
