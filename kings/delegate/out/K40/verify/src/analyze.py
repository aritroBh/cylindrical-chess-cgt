import sys, json, collections
SP = sys.argv[1]
INT = list(range(-12, 13)); IX = {n: n + 12 for n in INT}
ON, OFF, DUD, OVER, UNDER, STAR, UP, DOWN, PM, ONS = range(25, 35)
def load(fn):
    d = {}
    for ln in open(fn):
        if ln.startswith('#'): continue
        p, r = ln.rstrip('\n').split('\t'); d[p] = r
    return d
def onsig(r):  # W everywhere except D at off and dud
    return all(r[i] == 'W' for i in range(35) if i not in (OFF, DUD)) and r[OFF] == 'D' and r[DUD] == 'D'
def cls(r):
    if set(r) == {'W'}: return 'DEC'
    if set(r) == {'D'}: return 'DUD'
    if onsig(r): return 'ON'
    return 'OTHER'
def intpat(r): return ''.join(r[IX[n]] for n in INT)
def kind(r):
    """for a non DEC/DUD/ON row: monotone threshold over integers or parity etc."""
    s = intpat(r)
    if 'L' in s: return 'hasL'
    w = [n for n in INT if r[IX[n]] == 'W']
    if not w: return 'noW'
    th = min(w)
    if all(r[IX[n]] == 'W' for n in INT if n >= th): return 'thr%d' % th
    return 'nonmono'
out = {}
boards = [(w, h) for h in (6, 7, 8) for w in range(3, 9)]
for w, h in boards:
    b = f'{w}x{h}'
    N = load(f'{SP}/N_{b}.txt'); C = load(f'{SP}/C_{b}.txt'); NK = load(f'{SP}/NK_{b}.txt'); A = load(f'{SP}/A_{b}.txt')
    rec = {}
    for s in 'wb':
        ps = [p for p in N if p.endswith(' ' + s)]
        cN = collections.Counter(cls(N[p]) for p in ps)
        # under C
        cC = collections.Counter()
        kinds = collections.Counter()
        decsame = all((cls(N[p]) == 'DEC') == (cls(C[p]) == 'DEC') for p in ps)
        dudsame = all((cls(N[p]) == 'DUD') == (cls(C[p]) == 'DUD') for p in ps)
        for p in ps:
            c = cls(C[p]); cC[c] += 1
            if c == 'OTHER': kinds[kind(C[p])] += 1
        onN = [p for p in ps if cls(N[p]) == 'ON']
        onN_Pw = sum(1 for p in onN if C[p][IX[0]] == 'W')
        # class fixed by two bits under N
        twobits = all(cls(N[p]) == {('W', 'W'): 'DEC', ('W', 'D'): 'ON', ('D', 'D'): 'DUD'}.get((N[p][IX[0]], N[p][DUD]), '?') for p in ps)
        # N black wins
        nL = sum(1 for p in ps if 'L' in N[p]); cL = sum(1 for p in ps if 'L' in C[p])
        # DEC == P_L (W vs dud)
        decPL = all((cls(N[p]) == 'DEC') == (N[p][DUD] == 'W') for p in ps)
        dudC_eq_dudN_dud = all(N[p][DUD] == C[p][DUD] for p in ps)
        # Kxp test: x (+) on with Kxp = Black win, under N
        kx = collections.Counter((cls(N[p]), NK[p][ON]) for p in ps)
        fort = [p for p in ps if cls(N[p]) == 'DUD' and NK[p][ON] != 'L']
        # atlas
        ad = sum(1 for p in ps if A[p] != C[p][IX[0]]); adtype = collections.Counter((C[p][IX[0]], A[p]) for p in ps if A[p] != C[p][IX[0]])
        PW = sum(1 for p in ps if C[p][IX[0]] == 'W'); AW = sum(1 for p in ps if A[p] == 'W')
        # Prop 5 parity family pattern
        pat5 = ''.join('W' if (n < 0 and n % 2) else 'D' for n in INT)
        fam = sorted(p for p in ps if cls(C[p]) == 'OTHER' and intpat(C[p]) == pat5)
        # 4-file thresholds under N
        kN = collections.Counter(kind(N[p]) for p in ps if cls(N[p]) == 'OTHER')
        rec[s] = dict(n=len(ps), N=dict(cN), C=dict(cC), Ckinds=dict(kinds), decsame=decsame, dudsame=dudsame,
                      onN=len(onN), onN_Pwin=onN_Pw, twobits=twobits, N_blackwins=nL, C_blackwins=cL, decPL=decPL,
                      dud_same_both=dudC_eq_dudN_dud, kxp=str(dict(kx)), fortress=len(fort), fort_ex=fort[:3],
                      atlas_diff=ad, atlas_types=str(dict(adtype)), PW=PW, AW=AW, fam5=len(fam), fam5_ex=fam[:2],
                      Nkinds=dict(kN))
    out[b] = rec
    print(b, json.dumps(rec))
json.dump(out, open(sys.argv[2], 'w'), indent=1)
