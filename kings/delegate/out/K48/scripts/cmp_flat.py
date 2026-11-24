# K48: compare implementation A (p45a) and R (r48) on the flat searches, per file triple; print a table and the hits.
# usage: cmp_flat.py W...   (reads logs/flat/{A,R}_flatWx6_f*.out)
import sys, re, os
tot = {}
for W in sys.argv[1:]:
    for t in open('in/triples_flat%s.txt' % W).read().split():
        tag = 'flat%sx6_f%s' % (W, t.replace(',', '_'))
        fa, fr = 'logs/flat/A_%s.out' % tag, 'logs/flat/R_%s.out' % tag
        a = r = None; hits = []
        if os.path.exists(fa) and os.path.exists(fa.replace('.out', '.done')):
            a = {}
            for l in open(fa):
                m = re.match(r'RESULT flat shuttler=(\S+) placements=(\d+) F1\([^)]*\)=(\d+) noFreeze=\d+ promoFreeze=(\d+) F2\([^)]*\)=(\d+) F3\([^)]*\)=(\d+) F3one=\d+ F4\([^)]*\)=(\d+)', l)
                if m: a[m.group(1)] = tuple(int(x) for x in m.groups()[1:])
                if l.startswith('HIT'): hits.append('A ' + l.strip())
        if os.path.exists(fr) and os.path.exists(fr.replace('.out', '.done')):
            for l in open(fr):
                m = re.match(r'SUMMARY \S+ files \S+ max \S+: layers (\d+) placements (\d+) U1 (\d+) promoFreeze (\d+) U1\+U2 (\d+) loose (\d+) exact (\d+)', l)
                if m: r = tuple(int(x) for x in m.groups()[1:])
                if l.startswith('HIT'): hits.append('R ' + l.strip())
        st = []
        if a: st.append('A under %s over %s %s' % (a.get('white(under)'), a.get('black(over)'), 'over=under' if a.get('white(under)') == a.get('black(over)') else 'OVER!=UNDER'))
        if r: st.append('R %s' % (r,))
        if a and r: st.append('A=R' if a.get('white(under)') == r else 'DIFFER')
        print(W, t, ' | '.join(st) if st else 'not run')
        for h in hits: print('   ', h)
        for k, v in (('A', a.get('white(under)') if a else None), ('R', r)):
            if v: tot.setdefault((W, k), [0] * 6); tot[(W, k)] = [x + y for x, y in zip(tot[(W, k)], v)]
print('TOTALS (placements, O1, promoFreeze, O1+O2, loose, exact; under orientation):')
for k in sorted(tot): print(' ', k, tot[k])
