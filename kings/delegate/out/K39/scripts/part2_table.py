#!/usr/bin/env python3
"""K39 part 2 table. usage: part2_table.py ID...  (reads logs/r/c<ID>_*.out and in/ctx/c<ID>.pred.tsv)
Per context and root: chess A, B from own39p and from kp39p (refine), the P value (kpp, ref3m), the D-model prediction
r(H + dud_D), and the parked chess value of H (Ka1 ka6; A B from kp39p, own39p). Prints a line per root and a summary."""
import sys, os
R = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39/logs/r/'
I = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39/in/ctx/'
def first(path, col=1):
    d = {}
    if not os.path.exists(path): return None
    for l in open(path):
        p = l.rstrip('\n').split(' | ')
        if len(p) < 2: continue
        d[p[0]] = p[1].split()
    return d
tot = {}
for cid in sys.argv[1:]:
    oa, ob = first(R + f'c{cid}_own_b0.out'), first(R + f'c{cid}_own_b1.out')
    ka, kb = first(R + f'c{cid}_kp_A.out'), first(R + f'c{cid}_kp_B.out')
    pp, pr = first(R + f'c{cid}_kpp.out'), first(R + f'c{cid}_ref3m.out')
    pk, po0, po1 = first(R + f'c{cid}_park_kp.out'), first(R + f'c{cid}_park_own_b0.out'), first(R + f'c{cid}_park_own_b1.out')
    pred = open(I + f'c{cid}.pred.tsv').read().split()
    pw, pb = pred[1], pred[2]
    roots = [l.strip() for l in open(I + f'c{cid}.zh.in')]
    parks = [l.strip() for l in open(I + f'c{cid}.park.in')]
    def park(stm):
        p = parks[0 if stm == 'w' else 1]
        if not pk: return '??'
        a, b = pk[p][0], pk[p][1]
        o = (po0[p][0] if po0 else '?') + (po1[p][0] if po1 else '?')
        return a + b + ('' if a + b == o else '!' + o)
    for r in roots:
        stm = r.split()[-2]
        A = oa[r][0] if oa and r in oa else '?'; B = ob[r][0] if ob and r in ob else '?'
        KA = ka[r][0] if ka and r in ka else '?'; KB = kb[r][0] if kb and r in kb else '?'
        P1 = pp[r][0] if pp else '?'; P2 = pr[r][0] if pr else '?'
        pd = pw if stm == 'w' else pb
        agree2 = (A, B) == (KA, KB) if '?' not in (KA, KB) else None
        exact = A == B and A != '?'
        chess = A if exact else f'[{A}{B}]'
        status = ('exact' if exact else 'bounds') + ('' if agree2 is None else (' 2sol' if agree2 else ' SOLVERS-DIFFER'))
        cmpD = 'na' if not exact else ('=D' if A == pd else '!=D')
        cmpP = 'na' if not exact else ('=P' if A == P1 else '!=P')
        print(f"c{cid}\t{r}\tchess {chess}\t{status}\tP {P1}{'' if P1 == P2 else '!' + P2}\tpred {pd}\tpark {park(stm)}\t{cmpD} {cmpP}")
        k = (status, cmpD, cmpP); tot[k] = tot.get(k, 0) + 1
print("SUMMARY")
for k, v in sorted(tot.items()): print(" ", k, v)
# --- deviations of Z beside H (own39p move lists, both bounds): Z-moves other than the shuttle that do not lose exactly
SH = ({'b2', 'c3'}, {'a4', 'b5'}); ZF = set('abc')
def moves(path):
    d = {}
    if not os.path.exists(path): return d
    for l in open(path):
        p = l.rstrip('\n').split(' | ')
        if len(p) > 2: d[p[0]] = dict(x.split(':') for x in p[2].split())
    return d
print("NON-LOSING Z DEVIATIONS (exact chess values; '?' = bounds differ)")
for cid in sys.argv[1:]:
    ma, mb = moves(R + f'c{cid}_own_b0.out'), moves(R + f'c{cid}_own_b1.out')
    for r in ma:
        stm = r.split()[-2]
        for m, va in ma[r].items():
            vb = mb[r][m] if r in mb else "?"
            frm, to = m[1:3], m[3:5]
            if frm[0] not in ZF: continue           # a context move
            if m[0] == 'K' and {frm, to} <= SH[0 if stm == 'w' else 1]: continue  # the shuttle
            loses = (va == vb == 'L') if stm == 'w' else (va == vb == 'W')
            if not loses: print(f"  c{cid} {r}: {m} -> {va if va == vb else '?' + va + vb}")
