#!/usr/bin/env python3
"""canonical form of a king group under: file translation (cylinder, mod W), file mirror, colour flip (rank mirror + swap colours).
usage: canon.py W H < lines of 'K.. k.. P.. p.. [w -]'  -> prints canonical group, count, members"""
import sys
from collections import defaultdict
W=int(sys.argv[1]); H=int(sys.argv[2])
def parse(s):
    t=[x for x in s.split() if len(x)>=3 and x[0] in 'KkPp']
    return [(x[0], ord(x[1])-97, int(x[2:])) for x in t]
def fmt(p):
    ks=sorted(p, key=lambda z:('KkPp'.index(z[0]),z[1],z[2]))
    return ' '.join(f"{c}{chr(97+f)}{r}" for c,f,r in ks)
def variants(p):
    out=[]
    for flip in (0,1):
        for mir in (0,1):
            q=[]
            for c,f,r in p:
                if mir: f=(-f)%W
                if flip: c=c.swapcase(); r=H+1-r
                q.append((c,f,r))
            for tr in range(W):
                out.append([(c,(f+tr)%W,r) for c,f,r in q])
    return out
def canon(p):
    return min(fmt(v) for v in variants(p))
if __name__=='__main__':
    d=defaultdict(list)
    for l in sys.stdin:
        l=l.strip()
        if not l: continue
        l=l.split('\t')[0] if l.startswith(('dud','over')) is False else l
        d[canon(parse(l))].append(l)
    for k,v in sorted(d.items()): print(k,len(v),sep='\t')
