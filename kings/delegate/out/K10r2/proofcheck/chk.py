#!/usr/bin/env python3
"""Referee's own checker of Proposition 2.11 (written without opening K10/K10v outputs).
Usage: chk.py gen SEED N W H MAXP MODE > positions   (writes position lines + metadata as comments)
       chk.py verify instances.json results.txt
"""
import sys, random, json, itertools
from collections import deque

import os
DROP = int(os.environ.get("DROP", "0"))
SLACK = int(os.environ.get("SLACK", "0"))
FILES = "abcdefgh"

def sqname(s): return f"{FILES[s[0]]}{s[1]}"

def cdist(a, b, W):
    df = abs(a[0]-b[0]); df = min(df, W-df)
    return max(df, abs(a[1]-b[1]))

class Ctx:
    def __init__(s, W, H): s.W, s.H = W, H

def rho(q, beta, H):
    return q[1] if beta == 'W' else H+1-q[1]

def strip(f, W): return {(f-1) % W, f, (f+1) % W}

def ep_info(pos):
    # pos: dict(wk,bk,wp,bp,stm,ep) ep = target square or None
    return pos['ep']

def ep_victim(pos, H):
    e = pos['ep']
    if e is None: return None, None
    # stm captures; victim is of colour opposite stm
    if pos['stm'] == 'W':   # black just double-stepped; victim black pawn at (f, e.r-1)
        return 'B', (e[0], e[1]-1)
    else:
        return 'W', (e[0], e[1]+1)

def capturers_adjacent(pos, W):
    """are there stm pawns on the victim's rank adjacent to victim?"""
    col, v = ep_victim(pos, 0)
    if v is None: return False
    mine = pos['wp'] if pos['stm'] == 'W' else pos['bp']
    return any(((v[0]+d) % W, v[1]) in mine for d in (-1, 1))

def mu_omega(pos, p, beta, W, H, first_ep):
    """min number of omega moves until an omega pawn reaches its last rank; p deleted."""
    om = 'B' if beta == 'W' else 'W'
    wp = set(pos['wp']); bp = set(pos['bp'])
    if beta == 'W': wp.discard(p)
    else: bp.discard(p)
    opaw = frozenset(bp if om == 'B' else wp)
    bpaw = frozenset(wp if om == 'B' else bp)
    kings = {pos['wk'], pos['bk']}
    d = -1 if om == 'B' else 1
    start = H-1 if om == 'B' else 2
    last = 1 if om == 'B' else H
    # e.p. at first move
    ep0 = None
    if first_ep and pos['ep'] is not None and pos['stm'] == om:
        col, v = ep_victim(pos, H)
        if col == beta and v != p:
            ep0 = (pos['ep'], v)
    seen = {}
    start_state = (opaw, bpaw, ep0)
    dq = deque([(start_state, 0)])
    seen[start_state] = 0
    while dq:
        (op, bpw, ep), k = dq.popleft()
        occ = set(op) | set(bpw) | kings
        for q in op:
            f, r = q
            rest = op - {q}
            r1 = r + d
            if (f, r1) not in occ:
                if r1 == last: return k+1
                ns = (rest | {(f, r1)}, bpw, None)
                if ns not in seen: seen[ns] = k+1; dq.append((ns, k+1))
                r2 = r + 2*d
                if r == start and (f, r2) not in occ:
                    if r2 == last: return k+1
                    ns = (rest | {(f, r2)}, bpw, None)
                    if ns not in seen: seen[ns] = k+1; dq.append((ns, k+1))
            for dfl in (-1, 1):
                t = ((f+dfl) % W, r1)
                if t in bpw:
                    if r1 == last: return k+1
                    ns = (rest | {t}, bpw - {t}, None)
                    if ns not in seen: seen[ns] = k+1; dq.append((ns, k+1))
                elif ep is not None and ep[0] == t:
                    ns = (rest | {t}, bpw - {ep[1]}, None)
                    if ns not in seen: seen[ns] = k+1; dq.append((ns, k+1))
    return 10**6

def certify(pos, beta, p, W, H, do_h=(1, 2, 3, 4, 5)):
    """returns dict of hypotheses flags for pawn p of beta."""
    om = 'B' if beta == 'W' else 'W'
    bpaws = pos['wp'] if beta == 'W' else pos['bp']
    opaws = pos['bp'] if beta == 'W' else pos['wp']
    f = p[0]; rp = rho(p, beta, H)
    res = {}
    # H1
    ok = True
    st = strip(f, W)
    for q in opaws:
        if q[0] in st and rho(q, beta, H) > rp: ok = False
    # e.p.: p capturable
    col, v = ep_victim(pos, H)
    if v == p and col == beta and capturers_adjacent(pos, W): ok = False
    # path
    allp = set(pos['wp']) | set(pos['bp']) | {pos['wk'], pos['bk']}
    for s in range(1, H):
        # squares ahead
        pass
    if beta == 'W':
        path = [(f, r) for r in range(p[1]+1, H+1)]
    else:
        path = [(f, r) for r in range(1, p[1])]
    if any(s in allp for s in path): ok = False
    res[1] = ok
    # H2
    bk = pos['bk'] if beta == 'B' else pos['wk']
    ok2 = True
    adj = {(bk[0]-1) % W, (bk[0]+1) % W}
    for q in set(pos['wp']) | set(pos['bp']):
        if q[0] in adj: ok2 = False
    res[2] = ok2
    # H3
    ok_ = pos['wk'] if beta == 'B' else pos['bk']  # omega king
    okk = ok_
    ok3 = False
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0: continue
            t = ((okk[0]+df) % W, okk[1]+dr)
            if not (1 <= t[1] <= H): continue
            if cdist(t, bk, W) < 2: continue
            ts = strip(t[0], W)
            if any(q[0] in ts for q in set(pos['wp']) | set(pos['bp'])): continue
            ok3 = True
    res[3] = ok3
    # H4
    ok4 = True
    for q in bpaws:
        if q != p and q[0] in {(f-1) % W, (f+1) % W} and rho(q, beta, H) > rp+1+SLACK: ok4 = False
    res[4] = ok4
    # H5
    d = H - rp - (1 if rp == 2 else 0)
    e = d if pos['stm'] == om else d-1
    mu = mu_omega(pos, p, beta, W, H, True)
    res[5] = mu >= e+1
    res['d'] = d; res['e'] = e; res['mu'] = mu
    return res

def posline(pos, W, H):
    toks = [f"K{sqname(pos['wk'])}", f"k{sqname(pos['bk'])}"]
    toks += [f"P{sqname(s)}" for s in sorted(pos['wp'])]
    toks += [f"p{sqname(s)}" for s in sorted(pos['bp'])]
    ep = '-' if pos['ep'] is None else sqname(pos['ep'])
    return " ".join(toks) + f" {pos['stm'].lower()} {ep}"

def gen_pos(rng, W, H, maxp, mode):
    # mode: 'park' kings on a1/a H, pawns on c..W-2 ; 'rand' random kings, pawns on files in window
    for _ in range(1000):
        if mode.startswith('park'):
            wk = (0, 1); bk = (0, H)
            files = list(range(2, W-1))
        else:
            wk = (rng.randrange(W), rng.randrange(1, H+1))
            bk = (rng.randrange(W), rng.randrange(1, H+1))
            if cdist(wk, bk, W) < 2: continue
            files = list(range(W))
        if mode.endswith('win'):
            k = rng.choice([3, 4, 5])
            if len(files) < k: k = len(files)
            s0 = rng.randrange(len(files)-k+1)
            files = files[s0:s0+k]
        nw = rng.randint(1, maxp); nb = rng.randint(1, maxp)
        wp = set(); bp = set()
        occ = {wk, bk}
        def place(n, col, S):
            tries = 0
            while len(S) < n and tries < 50:
                tries += 1
                f = rng.choice(files); r = rng.randint(2, H-1)
                if (f, r) in occ: continue
                S.add((f, r)); occ.add((f, r))
        place(nw, 'W', wp); place(nb, 'B', bp)
        stm = rng.choice('WB')
        ep = None
        # e.p. right sometimes
        if rng.random() < 0.3:
            if stm == 'W':   # black pawn just double-stepped to rank H-2 (skipped H-1... start H-1 -> H-3)
                cands = [q for q in bp if q[1] == H-3 and (q[0], H-2) not in occ and (q[0], H-1) not in occ]
                # target square (f, H-2), origin (f,H-1) empty
                cands = [q for q in cands if any(((q[0]+d) % W, q[1]) in wp for d in (-1, 1))]
                if cands:
                    q = rng.choice(cands); ep = (q[0], q[1]+1)
            else:
                cands = [q for q in wp if q[1] == 4 and (q[0], 3) not in occ and (q[0], 2) not in occ]
                cands = [q for q in cands if any(((q[0]+d) % W, q[1]) in bp for d in (-1, 1))]
                if cands:
                    q = rng.choice(cands); ep = (q[0], q[1]-1)
        return dict(wk=wk, bk=bk, wp=frozenset(wp), bp=frozenset(bp), stm=stm, ep=ep)
    return None

def main():
    cmd = sys.argv[1]
    if cmd == 'gen':
        seed, N, W, H, maxp, mode = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
        out = sys.argv[8]
        rng = random.Random(seed)
        inst = []; lines = []
        seen = set()
        tries = 0
        while len(inst) < N and tries < N*400:
            tries += 1
            pos = gen_pos(rng, W, H, maxp, mode)
            if pos is None: continue
            L = posline(pos, W, H)
            if L in seen: continue
            for beta in 'WB':
                pawns = pos['wp'] if beta == 'W' else pos['bp']
                for p in pawns:
                    c = certify(pos, beta, p, W, H)
                    if all(c[i] for i in (1, 2, 3, 4, 5) if i != DROP):
                        seen.add(L)
                        inst.append(dict(line=L, beta=beta, p=sqname(p), d=c['d'], e=c['e'], mu=c['mu'], W=W, H=H))
                        lines.append(L)
        with open(out + '.json', 'w') as fh: json.dump(inst, fh)
        with open(out + '.pos', 'w') as fh:
            for L in sorted(set(lines)): fh.write(L + "\n")
        print(len(inst), "certified instances", len(set(lines)), "positions", tries, "tries", file=sys.stderr)
    elif cmd == 'verify':
        inst = json.load(open(sys.argv[2]))
        res = {}
        for ln in open(sys.argv[3]):
            if ' | ' not in ln: continue
            a, b = ln.rstrip().split(' | ')
            res[a] = b.split()
        bad = 0; skipped = 0; ok = 0
        for i in inst:
            r = res.get(i['line'])
            if r is None or r[0] != r[1]: print("NOEXACT", i); continue
            if r[0] == 'X': skipped += 1; continue
            want = 'W' if i['beta'] == 'W' else 'L'
            if r[0] != want:
                bad += 1; print("VIOLATION", i, r)
            else: ok += 1
        print("ok", ok, "violations", bad, "illegal", skipped)

main()
