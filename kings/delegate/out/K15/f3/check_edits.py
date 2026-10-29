#!/usr/bin/env python3
"""check that every EDIT block of ../EDITS.md has an OLD text occurring exactly once in the CURRENT LOOPY.md"""
import re, sys
L = open('/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md').read()
E = open(sys.argv[1] if len(sys.argv) > 1 else '../EDITS.md').read()
blocks = re.findall(r'### EDIT ([^\n]*)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW', E, re.S)
bad = 0
for lab, old, new in blocks:
    n = L.count(old)
    print(f"{lab!r}: OLD occurs {n} time(s)", 'OK' if n == 1 else 'PROBLEM')
    bad += n != 1
print('blocks', len(blocks), 'problems', bad)
