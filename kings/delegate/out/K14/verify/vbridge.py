#!/usr/bin/env python3
"""Referee's own check of Theorem 3.2''' on Z_A.  For every context: enumerate the regular positions (own pawn generator,
own king-state bookkeeping), ask kpp --moves for every legal move and its P-value, and classify each move.
Checks (V1a-ctx) (legal context moves == G's options), (V2-ctx), (Pun_W), (Pun_B), then the conclusions of 3.2'''(a),(b)."""
import json, sys, subprocess, collections
sys.path.insert(0, '.')
from vpawn import W, H, sq, children, closed

def nm(s): return chr(96 + s[0]) + str(s[1])

def ctx_moves(wp, bp, ep, side):
    """like vpawn.children but with descriptors (from,to) ."""
    out = []
    mine, theirs = (wp, bp) if side == 0 else (bp, wp)
    dr = 1 if side == 0 else -1
    start = 2 if side == 0 else H - 1
    last = H if side == 0 else 1
    occ = set(wp) | set(bp)
    def make(nm_, nt_, e):
        return ((tuple(sorted(nm_)), tuple(sorted(nt_))) if side == 0 else (tuple(sorted(nt_)), tuple(sorted(nm_)))) + (e,)
    for (f, r) in mine:
        t = (f, r + dr)
        if t not in occ:
            if t[1] == last: out.append(((nm((f, r)), nm(t)), None))
            else:
                out.append(((nm((f, r)), nm(t)), make([p for p in mine if p != (f, r)] + [t], theirs, None)))
                t2 = (f, r + 2 * dr)
                if r == start and t2 not in occ:
                    out.append(((nm((f, r)), nm(t2)), make([p for p in mine if p != (f, r)] + [t2], theirs, t)))
        for df in (-1, 1):
            c = (f + df, r + dr)
            if not (1 <= c[0] <= W): continue
            if c in theirs:
                if c[1] == last: out.append(((nm((f, r)), nm(c)), None))
                else: out.append(((nm((f, r)), nm(c)), make([p for p in mine if p != (f, r)] + [c], [p for p in theirs if p != c], None)))
            elif ep is not None and c == ep:
                v = (c[0], c[1] - dr)
                if v in theirs: out.append(((nm((f, r)), nm(c)), make([p for p in mine if p != (f, r)] + [c], [p for p in theirs if p != v], None)))
    return out

KW = ['a5', 'a6']; KB = ['c5', 'c6']

def pos_str(x, a, b, side):
    wp, bp, ep = x
    epstr = '-'
    if ep is not None:
        # include only if a capture exists for the side to move
        if any(d[1] == nm(ep) for d, nx in ctx_moves(wp, bp, ep, side) if nx is not None):
            epstr = nm(ep)
    return ' '.join(['K' + KW[a], 'k' + KB[b], 'Pb3', 'pb4', 'pb5'] + ['P' + nm(p) for p in wp] + ['p' + nm(p) for p in bp] + ['w' if side == 0 else 'b', epstr])

def regular(x0, a0, b0, s0):
    seen = set(); stack = [(x0, a0, b0, s0)]
    while stack:
        st = stack.pop()
        if st in seen: continue
        seen.add(st)
        x, a, b, s = st
        wp, bp, ep = x
        for d, nx in ctx_moves(wp, bp, ep, s):
            if nx is not None: stack.append((nx, a, b, 1 - s))
        nx = (wp, bp, None)
        stack.append((nx, 1 - a, b, 1) if s == 0 else (nx, a, 1 - b, 0))
    return seen

def main():
    ctxs = [json.loads(l) for l in open('../logs/small_contexts_fg.jsonl')]
    per_ctx_regs = []
    allpos = {}
    for c in ctxs:
        x0 = (tuple(sorted(sq(n) for n in c['w'])), tuple(sorted(sq(n) for n in c['b'])), None)
        regs = {}
        for a in (0, 1):
            for b in (0, 1):
                for s in (0, 1):
                    regs[(a, b, s)] = regular(x0, a, b, s)
        per_ctx_regs.append((x0, regs))
        for r in regs.values():
            for st in r:
                allpos[pos_str(st[0], st[1], st[2], st[3])] = st
    keys = sorted(allpos)
    print('distinct regular positions', len(keys), file=sys.stderr)
    out = subprocess.run(['./kpp', '--board', 'flat:7x6', '--ep', 'on', '--promote', 'QRBN', '--cap', '1', '--pmodel', '--moves'],
                         input='\n'.join(keys) + '\n', capture_output=True, text=True).stdout.strip().split('\n')
    info = {}
    for line in out:
        parts = line.split(' | ')
        if len(parts) < 2: continue
        A, B = parts[1].split()
        if A == 'X': info[parts[0]] = None; continue
        mv = parts[2].split() if len(parts) > 2 else []
        info[parts[0]] = (A, [m.rsplit(':', 1) for m in mv])
    # per-position classification
    cls = {}
    problems = collections.Counter()
    for k, st in allpos.items():
        x, a, b, s = st
        wp, bp, ep = x
        r = info[k]
        assert r is not None, k
        res, moves = r
        mine = ctx_moves(wp, bp, ep, s)
        mine_set = collections.Counter(d for d, nx in mine)
        kp_ctx = collections.Counter(); other_vals = []; shuttles = 0
        for mname, val in moves:
            base = mname.split('=')[0]
            if base[0] == 'K':
                frm, to = base[1:3], base[3:5]
                shut = (s == 0 and {frm, to} == set(KW)) or (s == 1 and {frm, to} == set(KB))
                if shut: shuttles += 1
                else: other_vals.append(val)
            else:
                frm, to = base[1:3], base[3:5]
                if frm[0] == 'b':  # a Z-pawn move
                    other_vals.append(val)
                else:
                    kp_ctx[(frm, to)] += 1
                    # (V2-ctx): promotion of s is a win for s in P
                    if '=' in mname:
                        want = 'W' if s == 0 else 'L'
                        if val != want: problems['promotion not a win for promoter'] += 1
        # V1a-ctx: same multiset of (from,to) up to promotion suffix duplicates
        if set(kp_ctx) != set(mine_set): problems['V1a-ctx mismatch'] += 1
        if shuttles != 1: problems['shuttle count != 1'] += 1
        loser_val = 'L' if s == 0 else 'W'   # side s moved: punished = win for s-bar
        pun = all(v == loser_val for v in other_vals)
        cls[k] = pun
    print('problems:', dict(problems), file=sys.stderr)
    # P-results per root and conclusions
    stats = collections.Counter(); ctx_pun = []
    mism_with_pun_fail = 0; mism_ctx = 0
    for ci, (x0, regs) in enumerate(per_ctx_regs):
        pred = closed(x0)
        union = set()
        for r in regs.values(): union |= r
        punW = all(cls[pos_str(*st)] for st in union if st[3] == 0)
        punB = all(cls[pos_str(*st)] for st in union if st[3] == 1)
        ctx_pun.append((punW, punB))
        mism = False
        for (a, b, s), reg in regs.items():
            root = (x0, a, b, s)
            P = info[pos_str(x0, a, b, s)][0]
            D = pred[s]
            ppunW = all(cls[pos_str(*st)] for st in reg if st[3] == 0)
            ppunB = all(cls[pos_str(*st)] for st in reg if st[3] == 1)
            if P != D: mism = True
            if D == 'W':
                if ppunB:
                    stats['a_instances'] += 1
                    if P != 'W': stats['a_fail'] += 1
            elif D == 'L':
                if ppunW:
                    stats['a_instances'] += 1
                    if P != 'L': stats['a_fail'] += 1
            if ppunW and ppunB:
                stats['b_instances'] += 1
                if P != D: stats['b_fail'] += 1
            if P != D and ppunW and ppunB: stats['mismatch_with_both_pun'] += 1
        if mism:
            mism_ctx += 1
            if not (punW and punB): mism_with_pun_fail += 1
    print('contexts', len(per_ctx_regs), 'PunW holds in', sum(1 for p in ctx_pun if p[0]), 'PunB in', sum(1 for p in ctx_pun if p[1]), 'both in', sum(1 for p in ctx_pun if p[0] and p[1]))
    print(dict(stats))
    print('mismatching contexts', mism_ctx, 'of which with a (Pun) failure somewhere on the regular positions', mism_with_pun_fail)

main()
