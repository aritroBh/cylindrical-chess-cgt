import glob, math, sys, collections, subprocess, io
D = '/Users/aritro/Downloads/Research/Chessendgames/research/sum_whole_census/data/'
RULES = ("count", "mover", "opponent"); TESTS = ("textbook", "e.p.-aware")
WIDTH = None
def PFX():
    if WIDTH in (None, 'all'): return 'raw_w*'
    return 'raw_' + (WIDTH if WIDTH.startswith('cyl') else 'w' + WIDTH)
def rows():
    for f in sorted(glob.glob(D + PFX() + '_*.tsv')):
        for l in open(f):
            yield l.rstrip('\n').split('\t')
    for f in sorted(glob.glob(D + PFX() + '_*.tsv.zst')):
        p = subprocess.run(['zstd', '-dc', f], capture_output=True, text=True)
        for l in p.stdout.splitlines():
            yield l.split('\t')
def wilson(k, n, z=1.96):
    if n == 0: return (0, 0)
    p = k / n; d = 1 + z*z/n; c = p + z*z/(2*n); h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return (max(0.0,(c-h)/d), min(1.0,(c+h)/d))
def fmt(k, n):
    lo, hi = wilson(k, n); return f"{k}/{n} = {100*k/max(n,1):.3f}% [{100*lo:.3f}, {100*hi:.3f}]"
def parse(r):
    orb = int(r[0]); pos = r[1]; nc = int(r[2])
    npawn = pos.count(' ') - pos.count('/') - pos.count(':') + 0  # recomputed below
    toks = [t for t in pos.replace('/', ' ').replace('W:', ' ').replace('B:', ' ').split()]
    npawn = len(toks)
    out = []
    for ti, base in ((0, 3), (1, 7)):
        hss = r[base] == '1'
        for ri in range(3):
            e = r[base+1+ri]
            out.append((TESTS[ti], RULES[ri], hss, e[0], e[1], e[2] == '1'))
    return orb, pos, nc, npawn, out
def main(filt=None):
    T = collections.defaultdict(lambda: collections.Counter())
    small = collections.defaultdict(list)   # (kind,test,rule) -> list of (npawn,pos)
    thm = collections.defaultdict(list)
    ntot = collections.Counter()
    for r in rows():
        orb, pos, nc, npawn, out = parse(r)
        w = int(pos and 0) + 0
        wid = max(ord(c[0]) for c in pos.replace('/', ' ').replace('W:', ' ').replace('B:', ' ').split()) - 96  # not width; informative only
        for test, rule, hss, s, wv, ss in out:
            K = (test, rule); c = T[K]
            dis = s != wv
            ncb = min(nc, 3)
            for key in (('all',), ('nc', ncb), ('hss', hss), ('ss', ss), ('hss+ss', hss, ss), ('n', npawn)):
                c[key + ('N',)] += 1; c[key + ('W',)] += orb
                if dis: c[key + ('D',)] += 1; c[key + ('DW',)] += orb
            if dis:
                small[('dis',) + K].append((npawn, pos, s, wv, hss, ss, nc))
                if hss: thm[K].append((npawn, pos, s, wv))
                if ss: small[('fp',) + K].append((npawn, pos, s, wv, hss, ss, nc))
            c[('conf', s, wv)] += 1
    return T, small, thm
if __name__ == '__main__':
    WIDTH = sys.argv[1] if len(sys.argv) > 1 else None
    T, small, thm = main()
    o = []
    o.append("## Headline (orbit representatives; N = positions, D = outcome(S) != outcome(W))\n")
    o.append("| test | rule | N | D | rate [Wilson 95%] |\n|---|---|---|---|---|")
    for test in TESTS:
        for rule in RULES:
            c = T[(test, rule)]; o.append(f"| {test} | {rule} | {c[('all','N')]} | {c[('all','D')]} | {fmt(c[('all','D')], c[('all','N')])} |")
    o.append("\n## Weighted by orbit size (all legal positions, not only representatives)\n")
    o.append("| test | rule | N_w | D_w | rate [Wilson 95%] |\n|---|---|---|---|---|")
    for test in TESTS:
        for rule in RULES:
            c = T[(test, rule)]; o.append(f"| {test} | {rule} | {c[('all','W')]} | {c[('all','DW')]} | {fmt(c[('all','DW')], c[('all','W')])} |")
    for title, keys in (("by number of components at the root", [('nc', 1), ('nc', 2), ('nc', 3)]),
                        ("by hereditarily_safe", [('hss', True), ('hss', False)]),
                        ("by sum_safe()", [('ss', True), ('ss', False)]),
                        ("hereditarily_safe x sum_safe()", [('hss+ss', True, True), ('hss+ss', False, True), ('hss+ss', False, False), ('hss+ss', True, False)])):
        o.append(f"\n## {title}\n")
        o.append("| test | rule | " + " | ".join(str(k[1:]) for k in keys) + " |\n|---|---|" + "---|" * len(keys))
        for test in TESTS:
            for rule in RULES:
                c = T[(test, rule)]
                o.append(f"| {test} | {rule} | " + " | ".join(fmt(c[k+('D',)], c[k+('N',)]) for k in keys) + " |")
    o.append("\n## by total pawns\n")
    ns = sorted({k[1] for c in T.values() for k in c if k[0] == 'n'})
    o.append("| test | rule | " + " | ".join(f"n={n}" for n in ns) + " |\n|---|---|" + "---|"*len(ns))
    for test in TESTS:
        for rule in RULES:
            c = T[(test, rule)]
            o.append(f"| {test} | {rule} | " + " | ".join(fmt(c[('n', n, 'D')], c[('n', n, 'N')]) for n in ns) + " |")
    o.append("\n## Theorem check: hereditarily_safe True and S != W\n")
    for test in TESTS:
        for rule in RULES:
            o.append(f"- {test}/{rule}: {len(thm[(test, rule)])} violations" + (f", e.g. {sorted(thm[(test, rule)])[0]}" if thm[(test, rule)] else ""))
    o.append("\n## sum_safe() True but S != W (false positives of the heuristic); smallest by pawns then text\n")
    for test in TESTS:
        for rule in RULES:
            L = sorted(small[('fp', test, rule)])
            o.append(f"- {test}/{rule}: {len(L)} positions; smallest: " + (f"{L[0][1]} (S={L[0][2]}, W={L[0][3]}, hss={L[0][4]}, ncomp={L[0][6]}, {L[0][0]} pawns)" if L else "none"))
    o.append("\n## S != W confusion (S outcome, W outcome) : count\n")
    for test in TESTS:
        for rule in RULES:
            c = T[(test, rule)]
            o.append(f"- {test}/{rule}: " + ", ".join(f"S={k[1]},W={k[2]}:{v}" for k, v in sorted(c.items()) if k[0] == 'conf' and k[1] != k[2]))
    o.append("\n## 5 smallest S != W positions per (test, rule)\n")
    for test in TESTS:
        for rule in RULES:
            L = sorted(small[('dis', test, rule)])[:5]
            o.append(f"- {test}/{rule}:")
            for x in L: o.append(f"    - `{x[1]}` S={x[2]} W={x[3]} hss={x[4]} sum_safe={x[5]} ncomp={x[6]} pawns={x[0]}")
    open(D + f'../analysis_w{WIDTH or "all"}.md', 'w').write("\n".join(o) + "\n")
    print("\n".join(o))
