"""Scratch: does the frozen certificate + a king-race condition give a P-win with REAL kings?  (beta = White)."""
import sys, itertools, subprocess, collections
sys.path.insert(0, '.')
from cert import *
from direct import enum_positions
KPP = '/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k10/fin/kpp'
W, H = int(sys.argv[1]), int(sys.argv[2]); maxw, maxb = int(sys.argv[3]), int(sys.argv[4])
bd = Board(W, H, True, True)
wk = (0, 1)
files = list(range(2, W-1)); ranks = range(2, H)
FL = "abcdefgh"
def nm(s): return f"{FL[s[0]]}{s[1]}"

def kingnbrs(k):
    for df in (-1,0,1):
        for dr in (-1,0,1):
            if df==0 and dr==0: continue
            r = k[1]+dr
            if 1 <= r <= H: yield ((k[0]+df) % W, r)

def mu_real(om, bo, ok, e):
    """ω-only game incl. king (conservative: king may step anywhere not own pawn / adjacent to wk); True if ω can promote within e moves"""
    start = (frozenset(om), frozenset(bo), ok)
    seen = {start}; fr = [start]
    for k in range(1, e+1):
        nx = []
        for om_, bo_, k_ in fr:
            occ = om_ | bo_ | {wk}
            for (f, r) in om_:
                rest = om_ - {(f, r)}; r1 = r-1
                if (f, r1) not in occ:
                    if r1 == 1: return True
                    for s in [(rest|{(f,r1)}, bo_, k_)] + ([(rest|{(f,r-2)}, bo_, k_)] if r == H-1 and (f,r-2) not in occ else []):
                        if s not in seen: seen.add(s); nx.append(s)
                for df in (-1,1):
                    t = ((f+df) % W, r1)
                    if t in bo_:
                        if r1 == 1: return True
                        s = (rest|{t}, bo_-{t}, k_)
                        if s not in seen: seen.add(s); nx.append(s)
            for t in kingnbrs(k_):
                if t in om_ or kdist(bd, t, wk) < 2: continue
                s = (om_, bo_ - {t}, t)
                if s not in seen: seen.add(s); nx.append(s)
        fr = nx
    return False

def kr_ok(p, ok, stm):
    f, r = p
    d = dist_to_promote(bd, 'W', p)
    sched = []
    cur = r
    if r == 2: cur = 4; sched.append((f, 4))
    else: cur = r+1; sched.append((f, cur))
    while len(sched) < d + 0 and cur < H:
        cur += 1; sched.append((f, cur))
    # sched[j-1] = square after j-th push
    if stm == 'B' and kdist(bd, ok, p) < 2: return False
    for j, sq in enumerate(sched, start=1):
        nj = j if stm == 'B' else j-1
        if kdist(bd, ok, sq) < nj + 2: return False
        if j < len(sched):
            nj1 = nj + 1
            if kdist(bd, ok, sched[j]) < nj1 + 1 - 0: return False
    return True

cases = []
for w, b in enum_positions(bd, files, maxw, ranks):
    pass
sqs = [(f, r) for f in files for r in ranks]
def subs(k):
    for n in range(0, k+1): yield from itertools.combinations(sqs, n)
for w in subs(maxw):
    if not w: continue
    for b in subs(maxb):
        if set(w) & set(b): continue
        pos = Pos(frozenset(w), frozenset(b))
        for stm in 'WB':
            for okf in range(W):
                for okr in range(1, H+1):
                    ok = (okf, okr)
                    if kdist(bd, ok, wk) < 3: continue
                    if ok in pos.white | pos.black: continue
                    # static frozen-style hypotheses with this king (kings fixed: ω king as obstacle only for kpath)
                    c, info = check(bd, pos, wk, ok, stm, 'W', use=('P1','front','kpath','N'))
                    if not c: continue
                    p = info['p']
                    d, e = info['d'], info['e']
                    if mu_real(pos.black, pos.white - {p}, ok, e): continue
                    if not kr_ok(p, ok, stm): continue
                    cases.append((" ".join(["Ka1", "k"+nm(ok)] + ["P"+nm(s) for s in sorted(w)] + ["p"+nm(s) for s in sorted(b)]) + (" w -" if stm == 'W' else " b -")))
cases = sorted(set(cases))
print("cases", len(cases), flush=True)
viol = []; illegal = 0
for i in range(0, len(cases), 30000):
    chunk = cases[i:i+30000]
    r = subprocess.run(["nice","-n","10",KPP,"--board",f"cyl:{W}x{H}","--cap","1","--threads","2","--pmodel"],input="\n".join(chunk)+"\n",capture_output=True,text=True)
    res = {l.split(" | ")[0]: l.split(" | ")[1].split() for l in r.stdout.splitlines() if " | " in l}
    for c in chunk:
        v = res.get(c)
        if v == ['X','X']: illegal += 1; continue
        if v != ['W','W']: viol.append((c, v))
print("illegal-input skipped", illegal, "violations", len(viol)); print(viol[:25])
