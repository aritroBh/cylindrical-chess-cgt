"""Verifier A, check 1 on the FULL legal KPK set (not only positions reachable from quiet placements)."""
import sys
import vgraph, vchess
tot = {'nodes': 0, 'kpk': 0, 'diff_all': 0, 'diff_kpk': 0}
for b in sys.argv[1:]:
    G = vgraph.build(b, allkpk=True)
    cv = vchess.chess_variant(G)
    lines = [vchess.pos_line(G, p) for p in G.pos]
    out = vchess.run_kpsolve(G, 'kings/delegate/out/K4/verify_A/kpv', lines)
    assert len(out) == len(lines)
    da = dk = nk = 0
    for x, (left, a, bb) in enumerate(out):
        assert left == lines[x]
        pk = bool(G.pos[x][4]); nk += pk
        if not (a == bb == cv[x]):
            da += 1; dk += pk
    print(b, 'nodes', G.n, 'KPK', nk, 'differences all/KPK', da, dk, flush=True)
    tot['nodes'] += G.n; tot['kpk'] += nk; tot['diff_all'] += da; tot['diff_kpk'] += dk
print('TOTAL', tot)
