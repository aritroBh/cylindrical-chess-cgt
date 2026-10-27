"""run_b.py -- (b) the reduced games (nodes reachable by K-moves) of R_n and Qo_n for odd n = LO..HI, by three engines.

  python run_b.py LO HI [FAMS] [CMAX]
Engines: mine = oddeng.py (this directory; canonical e.p. flags AND raw flags), E = verify_compute/myeng.py (Graph),
         C = check3/red.py + eng.py (T50 verifier's engine; only for n <= CMAX, default 21, it is the slowest).
Per (family, n): nodes, K-moves, T-moves, (node, side) pairs with a T-move, flagged nodes, zone (files that differ from the start
in some node), signature of G + *h from the graph (h = 0..7), passed pawns in any node (either colour, with and without e.p.),
files 2..n-8 exactly the pattern (W2 on even, B4 on odd files) in every node, agreement with the start outside the expected zone
{n-7..n-3, n-1} (+ {0,1} for Qo); graphs of the three engines identical (nodes, T-sets, K-sets); raw-flag graph equivalent to
the canonical one; comparison with the numbers in logs/pump_R_11_59.txt / pump_Qo_11_59.txt written by the note's author.
"""
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'verify_compute'))
sys.path.insert(0, os.path.join(HERE, '..', 'check3'))
import oddeng as O          # noqa: E402
import myeng as E           # noqa: E402
import eng as Ceng          # noqa: E402
import red as Cred          # noqa: E402

HS = tuple(range(8))
LOGS = os.path.join(HERE, '..', 'logs')


def norm_E(G):
    def cv(nd):
        return (nd[0], None if nd[1] is None else (nd[1][0], 'WB'[nd[1][1]]))
    out = {}
    for nd, rec in G.info.items():
        out[cv(nd)] = {'WB'[c]: (frozenset(cv(x) for x in rec[c][0]), frozenset(cv(x) for x in rec[c][1])) for c in (0, 1)}
    return cv(G.start), out


def norm_C(pos0):
    ids, order, info = Cred.build(pos0)
    out = {}
    for nd in order:
        out[nd] = {s: (frozenset(info[nd][s][0]), frozenset(info[nd][s][1])) for s in 'WB'}
    return order[0], out, Cred.solve_graph(ids, order, info, HS)


def known(fam):
    """numbers from the note's author (pump_*_11_59.txt): n -> (nodes, kept, T, zone string, sig)."""
    path = os.path.join(LOGS, 'pump_%s_11_59.txt' % fam)
    res = {}
    for line in open(path):
        m = re.match(r'n=\s*(\d+) pawns=(\d+) nodes=(\d+) kept=(\d+) T=(\d+) zone=(\[[^\]]*\]) ep=(\d+) sig=(\w+)', line)
        if m:
            res[int(m.group(1))] = (int(m.group(3)), int(m.group(4)), int(m.group(5)), m.group(6), int(m.group(7)), m.group(8))
    return res


def to_canon_flag(nd):
    """drop an inert flag from a raw node."""
    pos, flag = nd
    if flag is None:
        return nd
    f, c = flag
    n = len(pos)
    r2 = 4 if c == 0 else 5
    se = 8 * (1 - c)
    live = ((pos[f - 1] | pos[(f + 1) % n]) >> (se + r2 - 1)) & 1
    return nd if live else (pos, None)


def main():
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    fams = sys.argv[3].split(',') if len(sys.argv) > 3 else ['R', 'Qo']
    cmax = int(sys.argv[4]) if len(sys.argv) > 4 else 21
    for fam in fams:
        kn = known(fam)
        for n in range(lo, hi + 1, 2):
            t0 = time.time()
            toks = O.tokens_R(n) if fam == 'R' else O.tokens_Qo(n)
            pos0 = O.start(fam, n)
            exp_zone = ([0, 1] if fam == 'Qo' else []) + list(range(n - 7, n - 2)) + [n - 1]
            # ---------------- mine, canonical flags
            G = O.Graph(pos0)
            st = G.stats()
            sig = G.signature(HS)
            nopass = all(not O.passed(p, f, 0) and not O.passed(p, f, 1) and not O.passed(p, None, 0) and not O.passed(p, None, 1)
                         for p, f in G.order)
            pat = [(O.tok_to_file('W2') if j % 2 == 0 else O.tok_to_file('B4')) for j in range(n)]
            pat_ok = all(p[j] == pat[j] for p, _ in G.order for j in range(2, n - 7))
            out_zone_ok = all(p[j] == pos0[j] for p, _ in G.order for j in range(n) if j not in exp_zone)
            start_wall_ok = all(pos0[j] == pat[j] for j in range(2, n - 6))
            # ---------------- mine, raw flags
            Gr = O.Graph(pos0, raw=True)
            sr = Gr.stats()
            inert = sum(1 for nd in Gr.order if nd[1] is not None)
            canon_nodes = {to_canon_flag(nd) for nd in Gr.order}
            raw_equiv = (canon_nodes == set(G.order))
            if raw_equiv:
                for nd in Gr.order:
                    cn = to_canon_flag(nd)
                    for c in (0, 1):
                        T, K, _, _ = Gr.info[nd][c]
                        T0, K0, _, _ = G.info[cn][c]
                        if {to_canon_flag(x) for x in T} != set(T0) or {to_canon_flag(x) for x in K} != set(K0):
                            raw_equiv = False
            # ---------------- E
            tE = time.time()
            GE = E.Graph(O.to_pairs(pos0))
            sE = GE.signature(HS)
            nE = norm_E(GE)
            same_E = (nE == G.canonical())
            tE = time.time() - tE
            # ---------------- C
            if n <= cmax:
                tC = time.time()
                sC0, nC, sC = norm_C(Ceng.parse(toks))
                same_C = (nC == G.canonical()[1] and sC0 == G.canonical()[0])
                sigC = sC
                tC = time.time() - tC
            else:
                same_C, sigC, tC = None, None, 0.0
            # ---------------- the author's numbers
            k = kn.get(n)
            if k:
                author = (k[0] == st['nodes'] and k[1] == st['K'] and k[2] == st['T'] and k[3] == str(st['zone']) and k[4] == st['flagged']
                          and k[5] == sig)
            else:
                author = None
            ok_sig = sig == ('NNPNNNNN' if fam == 'R' else 'NNNPNNNN')
            print(f'{fam}_{n} pawns={O.npawns(pos0)} nodes={st["nodes"]} K={st["K"]} T={st["T"]} Tpairs={st["Tpairs"]} flagged={st["flagged"]} '
                  f'zone={st["zone"]} (expected zone {"OK" if st["zone"] == exp_zone else "DIFFERENT!"}) sig(h<8)={sig} '
                  f'[{"as claimed" if ok_sig else "NOT as claimed"}] no-passed-pawn-in-any-node={nopass} files2..{n - 8}-exact-pattern-in-every-node={pat_ok} '
                  f'start-wall-2..{n - 7}-is-pattern={start_wall_ok} agrees-with-start-outside-zone={out_zone_ok}\n'
                  f'      raw-flag graph: nodes={sr["nodes"]} nodes-with-an-inert-flag={inert} equivalent-to-canonical={raw_equiv} | '
                  f'E: sig={sE} graph-identical={same_E} ({tE:.0f}s) | '
                  f'C: sig={sigC} graph-identical={same_C} ({tC:.0f}s) | author-log-matches={author} | mine {time.time() - t0:.0f}s total', flush=True)


if __name__ == '__main__':
    main()
