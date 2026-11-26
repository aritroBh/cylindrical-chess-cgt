"""K65: print the six counters of a p45a (over) or r48 run: placements, (O1), promotion freeze, (O1)+(O2), loose, exact.
usage: summ.py <out file> ...   (p45a: RESULT line with shuttler=black(over); r48: SUMMARY line)"""
import lzma, re, sys
def rd(p): return (lzma.open(p, 'rt') if p.endswith('.xz') else open(p)).read()
for p in sys.argv[1:]:
    t = rd(p)
    m = re.search(r'RESULT \S+ shuttler=black\(over\) placements=(\d+) F1\(U1 at both shuttler roots\)=(\d+) noFreeze=\d+ promoFreeze=(\d+) F2\(U2\)=(\d+) F3\(U3 loose\)=(\d+) F3one=\d+ F4\(exact U4\)=(\d+)', t)
    if m: print(p, 'A', tuple(int(x) for x in m.groups())); continue
    m = re.search(r'SUMMARY .*placements (\d+) U1 (\d+) promoFreeze (\d+) U1\+U2 (\d+) loose (\d+) exact (\d+)', t)
    if m: print(p, 'R', tuple(int(x) for x in m.groups())); continue
    print(p, 'no summary')
