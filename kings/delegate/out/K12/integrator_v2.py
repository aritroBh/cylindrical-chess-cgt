"""Integrator check of K12 (no e.p. rights): roots of the P11 layout with a passer.
credit: cylcgt value (single) or the count-rule extension (race); result: kpsolve --frozen;
certification: K10r2 search reviewer's chk.py (independent of K12).
Usage: integrator_v2.py W H maxp [chunk]: as integrator_v.py, but kpsolve runs in chunks through heavy.sh."""
import sys, itertools, subprocess, collections, json
R = '/Users/aritro/Downloads/Research/Chessendgames'
sys.path.insert(0, R); sys.path.insert(0, R + '/kings/delegate/out/K10r2/search')
from cylcgt import pawns as P
import chk
W, H, maxp = map(int, sys.argv[1:4])
FN = 'abcdefghij'
cb = P.Board(W, H, True, True)
B = chk.Bd(W, H, True)
sqs = [(f, r) for f in range(2, W - 1) for r in range(2, H)]
roots = []
for nw in range(0, maxp + 1):
    for ws in itertools.combinations(sqs, nw):
        rest = [s for s in sqs if s not in ws]
        for nb in range(0, maxp + 1):
            for bs in itertools.combinations(rest, nb):
                if nw + nb == 0: continue
                txt = 'W: ' + ' '.join(FN[f] + str(r) for f, r in ws) + ' / B: ' + ' '.join(FN[f] + str(r) for f, r in bs)
                pos = P.Pos.parse(txt)
                wp, bp = P.passed(cb, pos, 'W'), P.passed(cb, pos, 'B')
                if not (wp or bp): continue
                for stm in 'wb':
                    if wp and bp:
                        N = 'W' if stm == 'w' else 'B'; M = 'B' if N == 'W' else 'W'
                        cred = N if P.promote_distance(cb, pos, N) <= P.promote_distance(cb, pos, M) else M
                        kind = 'race'
                    else:
                        cred = 'W' if wp else 'B'; kind = 'single'
                        v = P.value(cb, pos); assert v.num == (P.BIG if wp else -P.BIG)
                    y = chk.Pos((0, 1), (0, H), set(ws), set(bs), stm, None)
                    beta = cred.lower()
                    cert = any(chk.certified(chk.hyps(B, y, beta, p)) for p in (y.wp if beta == 'w' else y.bp))
                    roots.append((y.text(B), kind, cred, cert))
lines = [r[0] for r in roots]
# chunked: each batch takes a heavy.sh slot and releases it, so other kings/ jobs can interleave
CH = int(sys.argv[4]) if len(sys.argv) > 4 else 20000
res = {}
for i in range(0, len(lines), CH):
    pr = subprocess.run([R + '/kings/delegate/heavy.sh', R + '/kings/kpsolve', '--board', f'cyl:{W}x{H}', '--frozen', '--cap', '1', '--threads', '2'],
                        input='\n'.join(lines[i:i + CH]) + '\n', capture_output=True, text=True)
    for ln in pr.stdout.splitlines():
        if ' | ' in ln:
            a, b = ln.rsplit(' | ', 1); res[a] = b.split()
    print(f'chunk {i // CH + 1}/{(len(lines) + CH - 1) // CH} done, {len(res)} results', file=sys.stderr, flush=True)
C = collections.Counter(); ex = collections.defaultdict(list)
for t, kind, cred, cert in roots:
    a, b = res[t]; want = 'W' if cred == 'W' else 'L'
    agree = (a == want and b == want)
    k = (kind, 'cert' if cert else 'uncert', 'agree' if agree else 'disagree')
    C[k] += 1
    if len(ex[k]) < 3: ex[k].append(t + ' -> ' + a + b)
print(json.dumps({'board': f'{W}x{H}', 'maxp': maxp, 'roots': len(roots), 'classes': {'/'.join(k): v for k, v in sorted(C.items())}, 'examples': {'/'.join(k): v for k, v in ex.items()}}, indent=1))
