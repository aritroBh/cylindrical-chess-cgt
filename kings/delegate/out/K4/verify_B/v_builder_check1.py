import os, sys
sys.dont_write_bytecode = True
K4 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, K4)
import graph, check1
for b in sys.argv[1:]:
    cg = graph.ChessGraph(b)
    r = check1.check1(cg, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'builder_check1'))
    print(b, 'KPK', r['kpk'], 'other', r['other'], 'x', r['x'], 'differences', len(r['diffs']), 'cmd:', r['cmd'])
