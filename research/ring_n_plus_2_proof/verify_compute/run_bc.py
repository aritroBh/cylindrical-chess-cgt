"""run_bc.py -- (b) reduced graphs of P_n and (c) the insertion isomorphism ins_c : R_n -> R_{n+2}, by two engines.

Engines:  T = T50 verifier engine (t50/red.py + t50/eng.py, unchanged);  M = myeng.py (this directory).
Both graphs are normalised to the same form (nodes (pos, ep) with ep None / (file, 'W'|'B'); per node and side:
(set of T-children, set of K-children, number of L+P moves)) and every check is run on both and across the two.

(b) per even n in LO..HI: node count, K-edges, T-moves, flagged nodes, zone (files that differ from the start in some node),
    passed pawns in any node, signature of G + *h (h = 0..7) from the graph, T-vs-M graph identity.
(c) per even n in 18..HI-2: ins_12(R_n) == R_{n+2} (start maps to start; nodes onto; per node and side: K-children map
    onto K-children, T-flag equal, T-count equal, T-children map onto T-children), for the cut c = 12 and for every cut c in
    the admissible range 11..n-6 (and a few cuts outside it, as negative controls: expected differences are reported, not
    hidden); then Lemma 3 checked directly on every node of R_n for every cut whose arc c-4..c+5 consists of pattern files.
Usage:  python -B run_bc.py LO HI
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 't50'))
import myeng as M
import eng as T
import red as TR

HS = tuple(range(8))
LET = 'WB'
ZONE = [0, 2, 3, 4, 5, 6]
TAG = '_%s_%s' % (sys.argv[1], sys.argv[2])
out_b = open(os.path.join(HERE, 'logs', 'b_reduced' + TAG + '.txt'), 'w')
out_c = open(os.path.join(HERE, 'logs', 'c_insertion' + TAG + '.txt'), 'w')


def pb(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    out_b.write(s + '\n'); out_b.flush()


def pc(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    out_c.write(s + '\n'); out_c.flush()


# --------------------------------------------------------------------------------------------- normalised graphs
class NG:
    """normalised reduced graph: self.info[node][side letter] = (frozenset T, frozenset K, nLP)."""

    def __init__(self, name, start, info, sig, secs):
        self.name, self.start, self.info, self.sig, self.secs = name, start, info, sig, secs
        self.nodes = set(info)

    def stats(self):
        n = len(self.start[0])
        nK = sum(len(self.info[nd][s][1]) for nd in self.info for s in LET)
        nT = sum(len(self.info[nd][s][0]) for nd in self.info for s in LET)
        flagged = sum(1 for nd in self.info if nd[1] is not None)
        p0 = self.start[0]
        zone = sorted({f for (p, _) in self.info for f in range(n) if p[f] != p0[f]})
        return nK, nT, flagged, zone


def build_T(pos0):
    t0 = time.time()
    ids, order, info = TR.build(pos0)
    sig = TR.solve_graph(ids, order, info, HS)
    norm = {nd: {s: (frozenset(info[nd][s][0]), frozenset(info[nd][s][1]), info[nd][s][2]) for s in LET} for nd in order}
    return NG('T50', order[0], norm, sig, time.time() - t0)


def build_M(pos0):
    t0 = time.time()
    G = M.Graph(pos0)
    sig = G.signature(HS)

    def cv(nd):
        return (nd[0], M.ep_letters(nd[1]))

    norm = {}
    for nd, rec in G.info.items():
        norm[cv(nd)] = {LET[c]: (frozenset(cv(x) for x in rec[c][0]), frozenset(cv(x) for x in rec[c][1]), rec[c][2] + rec[c][3])
                        for c in (0, 1)}
    return NG('mine', cv(G.start), norm, sig, time.time() - t0)


def passed_anywhere(ng):
    """number of nodes in which some side has a passed pawn (by BOTH engines' predicates)."""
    bad = 0
    for pos, ep in ng.info:
        epm = None if ep is None else (ep[0], 0 if ep[1] == 'W' else 1)
        if M.passed_pawns(pos, epm, 0) or M.passed_pawns(pos, epm, 1) or T.passed_ranks(pos, ep, 'W') or T.passed_ranks(pos, ep, 'B'):
            bad += 1
    return bad


# ---------------------------------------------------------------------------------------------------- iso checks
def insn(nd, c):
    p, e = nd
    return (M.ins(p, c), None if e is None else ((e[0] if e[0] <= c else e[0] + 2), e[1]))


def iso_check(g0, g1, c):
    """ins_c : g0 -> g1.  Returns dict of counts of violations."""
    res = dict(start=0, onto=0, size=0, K=0, Tflag=0, Tcount=0, Tchild=0, nodes=len(g0.info), dLP=set())
    res['start'] = int(insn(g0.start, c) != g1.start)
    img = {insn(nd, c) for nd in g0.info}
    res['onto'] = int(img != g1.nodes)
    res['size'] = int(len(g0.info) != len(g1.info))
    for nd, rec in g0.info.items():
        nd1 = insn(nd, c)
        if nd1 not in g1.info:
            continue
        for s in LET:
            T0, K0, lp0 = rec[s]
            T1, K1, lp1 = g1.info[nd1][s]
            if bool(T0) != bool(T1): res['Tflag'] += 1
            if len(T0) != len(T1): res['Tcount'] += 1
            if {insn(x, c) for x in K0} != K1: res['K'] += 1
            if {insn(x, c) for x in T0} != T1: res['Tchild'] += 1
            res['dLP'].add((s, lp1 - lp0))
    return res


def iso_ok(r):
    return not (r['start'] or r['onto'] or r['size'] or r['K'] or r['Tflag'] or r['Tcount'] or r['Tchild'])


def expected_wall(j):
    """content of wall file j >= 6 in P_n: W2 on even files, B4 on odd files."""
    return M.parse_file('W2') if j % 2 == 0 else M.parse_file('B4')


def lemma3_direct(ng, c):
    """Lemma 3 on the nodes of ng: for every node p (no flag, no passed pawn) whose files c-4..c+5 are pattern files,
    classify the moves of p and of ins_c(p) afresh (with the engine's own classifier) and compare.
    Returns (nodes tested, node-side checks, mismatches)."""
    n = len(ng.start[0])
    tested = checks = bad = 0
    for pos, ep in ng.info:
        if ep is not None:
            continue
        if not all(pos[j] == expected_wall(j) for j in range(c - 4, c + 6)):
            continue
        tested += 1
        ph = M.ins(pos, c)
        for s in (0, 1):
            a = M.classify(pos, None, s)
            b = M.classify(ph, None, s)
            checks += 1
            ta = any(k == 'T' for k, _, _ in a)
            tb = any(k == 'T' for k, _, _ in b)
            Ka = {(M.ins(p, c), e) for k, p, e in a if k == 'K'}
            Kb = {(p, e) for k, p, e in b if k == 'K'}
            if ta != tb or Ka != Kb:
                bad += 1
    return tested, checks, bad


def main():
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    G = {}
    for n in range(lo, hi + 1, 2):
        if n < 8:
            continue
        pt = T.parse(M.P_tokens(n))
        pm = M.P_start(n)
        assert pt == pm
        gT = build_T(pt)
        gM = build_M(pm)
        G[n] = (gT, gM)
        same = (gT.info == gM.info) and (gT.start == gM.start)
        nK, nT, fl, zone = gT.stats()
        stM = gM.stats()
        pa = passed_anywhere(gT)
        st_ok = ((nK, nT, fl, zone) == stM)
        flag_ok = (T.npawns(pt) == n + 2 and not T.passed_ranks(pt, None, 'W') and not T.passed_ranks(pt, None, 'B')
                   and not M.passed_pawns(pm, None, 0) and not M.passed_pawns(pm, None, 1))
        pb('n=%2d pawns=%2d nodes=%d K=%d T=%d flagged=%d zone=%s passed-nodes=%d sig(h<8) T50=%s mine=%s | graphs identical (nodes, T-sets, K-sets, L+P counts): %s | stats equal: %s | start ok: %s | %.1fs+%.1fs' % (
            n, T.npawns(pt), len(gT.info), nK, nT, fl, zone, pa, gT.sig, gM.sig, same, st_ok, flag_ok, gT.secs, gM.secs))
    pb('(b) summary: n with 813 nodes:', [n for n in G if len(G[n][0].info) == 813],
       '| any difference between engines:', any(G[n][0].info != G[n][1].info for n in G))

    # ------------------------------------------------------------------ (c)
    for n in sorted(G):
        if n + 2 not in G or n < 18:
            continue
        for eng_i, nm in ((0, 'T50'), (1, 'mine')):
            g0, g1 = G[n][eng_i], G[n + 2][eng_i]
            r = iso_check(g0, g1, 12)
            pc('%-4s n=%2d -> %2d cut c=12: ok=%s  violations start=%d onto=%d size=%d K=%d Tflag=%d Tcount=%d Tchild=%d  nodes=%d  (L+P delta per side: %s)' % (
                nm, n, n + 2, iso_ok(r), r['start'], r['onto'], r['size'], r['K'], r['Tflag'], r['Tcount'], r['Tchild'], r['nodes'], sorted(r['dLP'])))
    # all admissible cuts, and controls
    for n in (18, 20, 22, 24, 26, 28):
        if n + 2 not in G:
            continue
        for eng_i, nm in ((0, 'T50'), (1, 'mine')):
            g0, g1 = G[n][eng_i], G[n + 2][eng_i]
            adm = list(range(11, n - 5))
            okadm = [c for c in adm if iso_ok(iso_check(g0, g1, c))]
            allc = list(range(6, n - 1))
            okall = [c for c in allc if iso_ok(iso_check(g0, g1, c))]
            pc('%-4s n=%2d -> %2d all cuts c=6..%d: admissible cuts 11..%d iso ok for %s of %s; ok cuts overall %s; failing cuts %s' % (
                nm, n, n + 2, n - 2, n - 6, okadm == adm and 'all' or okadm, adm, okall, [c for c in allc if c not in okall]))
    # Lemma 3 directly, on every node, every cut
    for n in (18, 20, 22, 26):
        if n not in G:
            continue
        tot = [0, 0, 0]
        percut = []
        for c in range(4, n - 5):
            t, k, b = lemma3_direct(G[n][1], c)
            tot[0] += t; tot[1] += k; tot[2] += b
            percut.append((c, t, b))
        pc('mine n=%2d Lemma 3 direct (nodes x cuts with pattern arc): node-cut pairs=%d, node-side checks=%d, mismatches=%d; per cut (c, nodes, bad): %s' % (
            n, tot[0], tot[1], tot[2], percut))
    # negative control for the direct Lemma-3 test: cuts whose arc touches the zone must be able to fail (arc check dropped)
    n = 18
    pos_nodes = [p for (p, e) in G[n][1].info if e is None]
    for c in (5, 6, 7, 8, 9, 10):
        bad = chk = 0
        for pos in pos_nodes:
            ph = M.ins(pos, c)
            for s in (0, 1):
                a = M.classify(pos, None, s); b = M.classify(ph, None, s)
                chk += 1
                if (any(k == 'T' for k, _, _ in a) != any(k == 'T' for k, _, _ in b) or
                        {(M.ins(p, c), e) for k, p, e in a if k == 'K'} != {(p, e) for k, p, e in b if k == 'K'}):
                    bad += 1
        pc('control (arc NOT required to be pattern files): n=18 cut c=%d node-side checks=%d mismatches=%d' % (c, chk, bad))


main()
