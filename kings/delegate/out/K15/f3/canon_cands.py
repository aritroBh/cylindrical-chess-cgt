#!/usr/bin/env python3
"""usage: canon_cands.py W H CLASS file... : distinct groups (file translation on the cylinder, file mirror, colour flip)
of class CLASS in K15 candidate files.  Prints: canonical form <TAB> number of listed placements <TAB> a representative root."""
import sys, importlib.util
args = sys.argv[1:]
W, H, CLS, files = int(args[0]), int(args[1]), args[2], args[3:]
sys.argv = ['canon', str(W), str(H)]
spec = importlib.util.spec_from_file_location('canon', '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/v2/canon.py')
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
from collections import defaultdict
d = defaultdict(list)
for fn in files:
    for l in open(fn):
        p = l.rstrip('\n').split('\t')
        if p[0] != CLS: continue
        d[c.canon(c.parse(p[1]))].append(p[1])
for k, v in sorted(d.items()): print(k, len(v), v[0], sep='\t')
