"""K49: test Theorem G and the converse on random terminal-free test games T.
For each board, writes random T's (disjoint, <=64 nodes per file), runs kn (normal play), and for every (x,s) with
x in DEC/ON/DUD compares r(x (+) T) with r(on (+) T) computed here.  Usage: python randT.py W H SEED NFILES"""
import random, subprocess, sys, os, collections
W, H, seed, nf = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
here = os.path.dirname(os.path.abspath(__file__)); tmp = here + '/../tmp'
rng = random.Random(seed)

def on_sum(nodes):
    """r(on (+) T) at (t, mover) for every t: Left can always pass; Right loses iff stuck. W or D (Left never loses)."""
    n = len(nodes); win = set()   # (t, 'L'/'R') Left-win
    ch = True
    while ch:
        ch = False
        for t in range(n):
            L, R = nodes[t]
            if (t, 'L') not in win and ((t, 'R') in win or any((u, 'R') in win for u in L)):
                win.add((t, 'L')); ch = True
            if (t, 'R') not in win and all((u, 'L') in win for u in R):
                win.add((t, 'R')); ch = True
    return win

stats = collections.Counter(); bad = []; typ = collections.defaultdict(lambda: [True, True])
import load
cls = load.load(W, H) if (W, H) in [(a, b) for a in (3,4,5,6,7,8) for b in (6, 8)] else None
if cls is None:
    o = subprocess.run([f'{tmp}/kn', str(W), str(H), f'{here}/std.t'], capture_output=True, text=True).stdout.splitlines()
    cols = o[0].split()[1:]; cls = {}
    for ln in o[1:]:
        a, b = ln.split('|'); cls[' '.join(a.split())] = load.tag(dict(zip(cols, b.split())))
for it in range(nf):
    nodes, roots = [], []
    while len(nodes) < 56:
        k = rng.randint(1, 4); base = len(nodes)
        comp = [([], []) for _ in range(k)]
        for i in range(k):
            for side in (0, 1):
                for _ in range(rng.choice([0, 0, 1, 1, 2])):
                    comp[i][side].append(base + rng.randrange(k))
        nodes += [(sorted(set(a)), sorted(set(b))) for a, b in comp]
        roots.append(base)
    fn = f'{tmp}/r{W}x{H}_{seed}_{it}.t'
    with open(fn, 'w') as f:
        print(len(nodes), file=f)
        for L, R in nodes: print('L:', *L, '; R:', *R, file=f)
        for r in roots: print(f'T{r}', r, file=f)
    win = on_sum(nodes)
    S = set(range(len(nodes)))
    ch = True
    while ch:
        ch = False
        for u in list(S):
            L, R = nodes[u]
            if not any(v in S for v in R) or any(v not in S for v in L): S.discard(u); ch = True
    out = subprocess.run([f'{tmp}/kn', str(W), str(H), fn], capture_output=True, text=True).stdout.splitlines()
    os.remove(fn)
    names = out[0].split()[1:]
    for ln in out[1:]:
        a, b = ln.split('|'); a = a.split(); res = b.split()
        s = a[3]
        for nm, r in zip(names, res):
            t = int(nm[1:]); mv = 'L' if s == 'w' else 'R'
            pos = ' '.join(a); c = cls[pos]
            cb = cls.get(' '.join(a[:3]) + ' b', 'X'); onL = (t, 'L') in win; onR = (t, 'R') in win
            if t in S:
                stats[('reserve', c, r)] += 1
                if c != 'DEC' and r == 'W': bad.append(('U', pos, nm))
            wk_, bk_, p_ = (load.sq(x) for x in a[:3])
            if H - p_[1] == 1 and c == 'ON':
                Pi = [((p_[0] + i) % W, p_[1] - 1) for i in (-1, 0, 1)]
                if s == 'w': exp = onL if cb == 'ON' else onR
                elif bk_ == (p_[0], p_[1] + 1): exp = onR
                else: exp = onL
                stats[('d1', s, 'ok' if (r == 'W') == exp else 'BAD')] += 1
                if (r == 'W') != exp: bad.append(('d1', pos, nm))
            cb = cls.get(' '.join(a[:3]) + ' b', 'X')
            onL = (t, 'L') in win; onR = (t, 'R') in win
            if c == 'ON':
                ty = typ[pos]; ty[0] &= ((r == 'W') == onL); ty[1] &= ((r == 'W') == onR)
                if s == 'b': pred = 'W' if onR else None
                else: pred = 'W' if (onR or (onL and cb in ('ON', 'DEC'))) else None
                cw = cls.get(' '.join(a[:3]) + ' w', 'X(check)')
                key = (s, c, 'pair' + cb if s == 'w' else 'twin_w=' + cw, 'G=W' if pred else 'G=?', 'on' + ('W' if (onL if s == 'w' else onR) else 'D'), r)
                stats[key] += 1
                if pred == 'W' and r != 'W': bad.append((pos, nm))
                if s == 'b' and not onR and r == 'W':
                    (pf, pr) = load.sq(a[2]); (bf, br) = load.sq(a[1])
                    chk = br == pr + 1 and ((bf - pf) % W in (1, W - 1))
                    stats[('b-exception', 'check' if chk else 'nocheck')] += 1
                    pass
            else:
                stats[(s, c, r)] += 1
    stats['files'] += 1
tc = collections.Counter()
for pos, (l, rr) in typ.items():
    c2 = cls.get(pos[:-1] + ('b' if pos.endswith('w') else 'w'), 'X')
    tc[(pos[-1], 'twin=' + c2, {(True, True): 'L=R', (True, False): 'like (on,L)', (False, True): 'like (on,R)', (False, False): 'NEITHER'}[(l, rr)])] += 1
for k in sorted(tc): print(f'cyl:{W}x{H} ON-position type', k, tc[k])
for k in sorted(stats, key=str): print(f'cyl:{W}x{H}', k, stats[k])
print(f'cyl:{W}x{H} violations (G, U, d1)', len(bad), bad[:5])
