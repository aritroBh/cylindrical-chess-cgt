"""compare my graph with the builder's graph (graph.ChessGraph, built on kings/ref/solve.py)"""
import sys, os, time
sys.dont_write_bytecode = True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import v_gen
import graph as bg

def ref_to_mine(p, G):
    stm, wk, bk, offs, wp, bp, ep = p
    assert bp == 0 and ep == -1 and len(offs) <= 1
    wps = wp.bit_length() - 1 if wp else -1
    return (stm, wk, bk, wps, offs[0] if offs else None)

for board in sys.argv[1:]:
    t0 = time.time()
    M = v_gen.build(board)
    B = bg.ChessGraph(board)
    G = M['G']
    mine = {n: i for i, n in enumerate(M['nodes'])}
    theirs = {ref_to_mine(p, G): i for i, p in enumerate(B.pos)}
    ok_nodes = set(mine) == set(theirs)
    bad_succ = bad_chk = bad_flip = bad_stm = 0
    if ok_nodes:
        for n, i in mine.items():
            j = theirs[n]
            ms = sorted(M['nodes'][s] for s in M['succ'][i])
            ts = sorted(ref_to_mine(B.pos[s], G) for s in B.succ[B.succ_off[j]:B.succ_off[j + 1]])
            bad_succ += ms != ts
            bad_chk += bool(M['incheck'][i]) != bool(B.incheck[j])
            f1 = M['nodes'][M['flip'][i]] if M['flip'][i] >= 0 else None
            f2 = ref_to_mine(B.pos[B.flip[j]], G) if B.flip[j] >= 0 else None
            bad_flip += f1 != f2
    print(board, 'nodes mine/theirs', len(mine), len(theirs), 'same node set', ok_nodes,
          'succ-mismatch', bad_succ, 'incheck-mismatch', bad_chk, 'flip-mismatch', bad_flip,
          'edges mine', sum(len(s) for s in M['succ']), 'theirs', len(B.succ), '%.1fs' % (time.time() - t0), flush=True)
