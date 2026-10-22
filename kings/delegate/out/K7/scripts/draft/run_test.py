import random, subprocess, sys, json, time
from kpgen import Board
from lc import Cert

seed = int(sys.argv[1]); nY = int(sys.argv[2]); W = int(sys.argv[3]); H = int(sys.argv[4]); wrap = sys.argv[5] == 'cyl'
tag = sys.argv[6]
Tmax = int(sys.argv[7]) if len(sys.argv)>7 else 5
random.seed(seed)
B = Board(W, H, wrap)
FZ = [0, 1, 2]
C = Cert(B, FZ)
ctxfiles = [4, 5] if W == 7 else [4, 5, 6]
if W == 8: ctxfiles = [4, 5, 6]
zsq = [r * W + f for r in range(1, H - 1) for f in FZ]
csq = [r * W + f for r in range(1, H - 1) for f in ctxfiles]

def rand_Y():
    while True:
        wk = random.choice([r * W + f for r in range(H) for f in FZ]); bk = random.choice([r * W + f for r in range(H) for f in FZ])
        nz = (random.choice([0, 1, 2]), random.choice([0, 1, 2]))
        nc = (random.choice([0, 1, 2, 3]), random.choice([0, 1, 2, 3]))
        pool = zsq[:]
        random.shuffle(pool)
        wz = pool[:nz[0]]; bz = pool[nz[0]:nz[0] + nz[1]]
        cp = csq[:]; random.shuffle(cp)
        wc = cp[:nc[0]]; bc = cp[nc[0]:nc[0] + nc[1]]
        wp = frozenset(wz + wc); bp = frozenset(bz + bc)
        s = random.randint(0, 1)
        pos = (wk, bk, wp, bp, s, -1)
        if B.legal_pos(pos):
            return pos

rows = []
t0 = time.time()
for iy in range(nY):
    Y = rand_Y()
    s = Y[4]
    for m in B.moves(Y):
        if m['promo']:
            continue
        if m['kind'] == 'P' and not C.sq_in_FZ(m['frm']):
            continue
        Ym = m['pos']
        for r in B.moves(Ym):
            if r['promo']:
                continue
            if r['kind'] == 'K' and not C.sq_in_FZ(r['to']):
                continue
            if r['kind'] == 'P' and not C.sq_in_FZ(r['frm']):
                continue
            Q = r['pos']
            TP = C.L1(Q, qsafe=False, Tmax=Tmax)
            if TP is None:
                rows.append(dict(Y=B.to_text(Y), m=(m['kind'], B.fname(m['frm']), B.fname(m['to'])), r=(r['kind'], B.fname(r['frm']), B.fname(r['to'])),
                                 Q=B.to_text(Q), TP=None))
                continue
            muB = C.mu(Q, False); muA = C.mu(Q, True)
            TQ = C.L1(Q, qsafe=True, Tmax=Tmax)
            L3 = {}
            for T in range(TP, Tmax + 1):
                e, a, bad = C.L3(Q, T, False)
                L3[T] = (e, a)
            rows.append(dict(Y=B.to_text(Y), m=(m['kind'], B.fname(m['frm']), B.fname(m['to'])), r=(r['kind'], B.fname(r['frm']), B.fname(r['to'])),
                             Q=B.to_text(Q), TP=TP, TQ=TQ, muB=muB, muA=muA, L3=L3))
    if iy % 200 == 0:
        print(iy, len(rows), time.time() - t0, file=sys.stderr, flush=True)

# P values for all Q
qs = [r['Q'] for r in rows]
inp = "\n".join(qs) + "\n"
out = subprocess.run(["./kp", "--board", ("cyl" if wrap else "flat") + f":{W}x{H}", "--ep", "on", "--promote", "Q", "--pmodel", "--threads", "2"],
                     input=inp, capture_output=True, text=True).stdout.splitlines()
assert len(out) == len(rows), (len(out), len(rows))
for row, line in zip(rows, out):
    parts = line.split("|")[1].split()
    row['P'] = parts[0]; row['P2'] = parts[1]
    stm = 0 if row['Q'].split()[-2] == 'w' else 1
    row['sbar_wins'] = (row['P'] == ('L' if stm == 0 else 'W')) and parts[0] == parts[1]
json.dump(rows, open(f"rows_{tag}.json", "w"))
print("rows", len(rows))
