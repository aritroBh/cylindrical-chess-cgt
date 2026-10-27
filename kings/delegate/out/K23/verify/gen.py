import sys, itertools
# gen.py ZTOKENS FILES MAXW MAXB LO HI : own generator; prints positions (both stm) and a "# ctx" key per context
z, files, mw, mb, lo, hi = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
sq = [f + str(r) for f in files for r in range(lo, hi + 1)]
n = 0
def subsets(k):
    for c in range(k + 1):
        yield from itertools.combinations(sq, c)
for W_ in subsets(mw):
    for B_ in subsets(mb):
        if set(W_) & set(B_): continue
        toks = [z] + ['P' + s for s in W_] + ['p' + s for s in B_]
        for stm in 'wb': print(' '.join(toks + [stm, '-']))
        n += 1
sys.stderr.write('%d contexts\n' % n)
