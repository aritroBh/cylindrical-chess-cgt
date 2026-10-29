#!/usr/bin/env python3
# K31 task 2: structure of the +1/-1 roots of a single pair on cyl:WxH (lk dump), tests the 'antipodal file' rule.
import subprocess, re, sys, json, os
BIN = os.path.dirname(os.path.abspath(__file__)) + '/../bin'
def dump(board, r, cl):
    o = subprocess.run(['nice','-n','15',BIN+'/lk','classify',board,'a%d'%r,'free','dump='+cl],capture_output=True,text=True).stdout
    return [l.split(' :: ')[1] for l in o.splitlines() if l.startswith('DUMP '+cl+' ::')]
def parse(p):
    d = {}
    for tok in p.split():
        d[tok[0]] = (ord(tok[1]) - 97, int(tok[2:]))
    return d
Ws = range(int(sys.argv[1]), int(sys.argv[2])+1); Hs = range(int(sys.argv[3]), int(sys.argv[4])+1)
out = open(sys.argv[5], 'w'); bad = 0; tot = 0
for H in Hs:
  for W in Ws:
    for r in range(2, H-1):
      for cl in ('+1','-1'):
        ps = dump('cyl:%dx%d'%(W,H), r, cl)
        for p in ps:
            d = parse(p); tot += 1
            ok = (W % 2 == 0 and d['K'][0] == W//2 and d['k'][0] == W//2)
            if not ok: bad += 1
            out.write(json.dumps({'W':W,'H':H,'r':r,'cl':cl,'wk':d['K'],'bk':d['k'],'anti':ok})+'\n')
print('roots', tot, 'not both kings on antipodal file', bad)
