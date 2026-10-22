"""Window-form test of Theorem 2.7(b): random window positions Q, compute (L1),(L2),(L3) and the exact P value."""
import random, subprocess, sys, json, time
from kpgen import Board
from lc import Cert

seed = int(sys.argv[1]); nQ = int(sys.argv[2]); W = int(sys.argv[3]); H = int(sys.argv[4]); wrap = sys.argv[5] == 'cyl'
tag = sys.argv[6]; Tmax = int(sys.argv[7]) if len(sys.argv) > 7 else 4
random.seed(seed)
B = Board(W, H, wrap)
FZ = [0, 1, 2]
C = Cert(B, FZ)
ctxfiles = list(range(4, W - 1)) if wrap else list(range(4, W))
zsq = [r * W + f for r in range(1, H - 1) for f in FZ]
csq = [r * W + f for r in range(1, H - 1) for f in ctxfiles]
fzk = [r * W + f for r in range(H) for f in FZ]
allk = list(range(B.N))

def rand_Q():
    while True:
        s = random.randint(0, 1)
        sk = random.choice(allk if random.random() < 0.6 else fzk)
        bk_ = random.choice(fzk)               # s-bar king on F_Z
        nz = (random.choice([0, 1, 2]), random.choice([0, 1, 2]))
        nc = (random.choice([0, 1, 2]), random.choice([0, 1, 2]))
        if nz[0] + nc[0] > 3 or nz[1] + nc[1] > 3:
            continue
        pool = zsq[:]; random.shuffle(pool)
        wz = pool[:nz[0]]; bz = pool[nz[0]:nz[0] + nz[1]]
        cp = csq[:]; random.shuffle(cp)
        wc = cp[:nc[0]]; bc = cp[nc[0]:nc[0] + nc[1]]
        wp = frozenset(wz + wc); bp = frozenset(bz + bc)
        wk, bk = (sk, bk_) if s == 0 else (bk_, sk)
        pos = (wk, bk, wp, bp, s, -1)
        if not B.legal_pos(pos):
            continue
        # s's king must not be attacked by an s-bar context pawn
        sbar_ctx = [p for p in (bp if s == 0 else wp) if not C.sq_in_FZ(p)]
        att = B.pawn_attacked(sbar_ctx, 1 - s)
        if sk in att:
            continue
        return pos

rows = []
t0 = time.time()
for i in range(nQ):
    Q = rand_Q()
    TP = C.L1(Q, qsafe=False, Tmax=Tmax)
    if TP is None:
        rows.append(dict(Q=B.to_text(Q), TP=None))
        continue
    muB = C.mu(Q, False); muA = C.mu(Q, True)
    TQ = C.L1(Q, qsafe=True, Tmax=Tmax)
    L3 = {}
    for T in range(TP, Tmax + 1):
        if muB >= T + 1:
            e, a, bad = C.L3(Q, T, False)
            L3[T] = (e, a)
    rows.append(dict(Q=B.to_text(Q), TP=TP, TQ=TQ, muB=muB, muA=muA, L3=L3))
    if i % 500 == 0:
        print(i, len(rows), round(time.time() - t0), file=sys.stderr, flush=True)

qs = [r['Q'] for r in rows]
out = subprocess.run(["./kp", "--board", ("cyl" if wrap else "flat") + f":{W}x{H}", "--ep", "on", "--promote", "Q", "--pmodel", "--threads", "2"],
                     input="\n".join(qs) + "\n", capture_output=True, text=True).stdout.splitlines()
assert len(out) == len(rows), (len(out), len(rows))
for row, line in zip(rows, out):
    parts = line.split("|")[1].split()
    row['P'] = parts[0]
    stm = 0 if row['Q'].split()[-2] == 'w' else 1
    row['sbar_wins'] = (parts[0] == parts[1]) and (parts[0] == ('L' if stm == 0 else 'W'))
    row['Y'] = row['Q']; row['m'] = ''; row['r'] = ''
json.dump(rows, open(f"rows_{tag}.json", "w"))
print("rows", len(rows), "L1 holds", sum(1 for r in rows if r['TP'] is not None))
