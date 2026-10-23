"""Pumping check with the independent engine.

For a family and a range of ring sizes n (one parity class at a time) build the reduced game graph R_n, and check:
  (Z)  every node is e.p.-free and agrees with the start position outside a fixed zone of files (the "window");
  (I)  inserting two wall files at a cut deep inside the wall maps the nodes of R_n onto the nodes of R_{n+2},
       the kept edges onto the kept edges, and the terminal-win flags onto the terminal-win flags (so R_{n+2} = ins(R_n));
  (S)  the outcome string of G + *h (h = 0..7) on R_n.
Usage: python pump_verify.py <odd|even|Fodd|Feven> <nlo> <nhi>
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fam, graph

RHO = int(os.environ.get("RHO", "5"))

def family(name):
    if name == "odd": return fam.odd, 1, "odd"
    if name == "even": return fam.even, 0, "even"
    if name == "Fodd": return fam.F, 1, "F"
    if name == "Feven": return fam.F, 0, "F"
    raise ValueError(name)

def ins_tokens(toks, c):
    return toks[:c + 1] + [toks[c + 1], toks[c]] + toks[c + 1:]

def zone_files(base):
    """files on which some node differs from the start"""
    return None

def analyse(name, n):
    mk, parity, fname = family(name)
    start = mk(n)
    g = graph.build(start)
    nodes = []
    dev = set(); ep = 0
    for p in g.pos:
        t, e = graph.parse_pos(p)
        nodes.append(t)
        if e: ep += 1
        for i, (a, b) in enumerate(zip(t, start)):
            if a != b: dev.add(i)
    return g, nodes, dev, ep, start

def main():
    name = sys.argv[1]; nlo = int(sys.argv[2]); nhi = int(sys.argv[3])
    mk, parity, fname = family(name)
    assert nlo % 2 == parity
    prev = None
    print(f"family {name}: n, pawns, nodes, kept edges, terminal edges, zone(dev files), eps, outcome G+*h h=0..7, [insertion check vs previous n]")
    for n in range(nlo, nhi + 1, 2):
        t0 = time.time()
        g, nodes, dev, ep, start = analyse(name, n)
        nk = sum(1 for es in g.edges for e in es if e[1] != "T"); nt = sum(1 for es in g.edges for e in es if e[1] == "T")
        sig = graph.solve(g, 7)
        line = f"n={n:3d} pawns={fam.ntoks_pawns(start)} nodes={g.n()} kept={nk} T={nt} zone={sorted(dev)} ep={ep} sig={sig}"
        if prev is not None:
            pn, pg, pnodes, pdev, pstart = prev
            # cut: the middle of the pristine files (all files outside both zones, as seen from the start)
            wall = fam.wall_files(fname, pn)
            # choose c so that the 2*RHO files c-RHO+1 .. c+RHO of the smaller ring are wall files that no node ever changes
            cands = [c for c in range(pn - 1) if all((c + d) in range(pn) and (c + d) in wall and (c + d) not in pdev for d in range(-RHO + 1, RHO + 1))]
            if not cands:
                line += f"  [no cut with {2*RHO} unchanged wall files]"
            else:
                c = cands[len(cands) // 2]
                if os.environ.get('FIXC'):
                    c = int(os.environ['FIXC'])
                    assert c in cands, ('FIXC not admissible', c, cands)
                # sanity: ins of the start position is the next start position
                ok_start = ins_tokens(pstart, c) == start
                img = {}
                for i, t in enumerate(pnodes):
                    key = " ".join(ins_tokens(t, c)); img[i] = key
                cur = {" ".join(t): i for i, t in enumerate(nodes)}
                same_nodes = set(img.values()) == set(cur.keys()) and len(set(img.values())) == len(img)
                # edge sets, in terms of node strings
                def eset(graph_, nodes_, f):
                    s = set()
                    for i, es in enumerate(graph_.edges):
                        for side, tgt, mv in es:
                            s.add((f(i), side, "T" if tgt == "T" else f(tgt)))
                    return s
                e_prev = eset(pg, pnodes, lambda i: img[i])
                e_cur = eset(g, nodes, lambda i: " ".join(nodes[i]))
                same_edges = e_prev == e_cur
                line += f"  [cut c={c}: start->start {ok_start}, nodes onto {same_nodes}, kept+T edges equal {same_edges}]"
        print(line, f"({time.time() - t0:.1f}s)", flush=True)
        prev = (n, g, nodes, dev, start)

if __name__ == "__main__":
    main()
