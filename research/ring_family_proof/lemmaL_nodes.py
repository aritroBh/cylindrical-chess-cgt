"""Lemma 3 (insertion) on the ACTUAL nodes of the reduced games: for every node p of R_n (n >= n0, one parity), every admissible cut c
(files c-4..c+5 pattern files in all nodes) compare K-children and T-flags of p and of ins_c(p) from the engine's classification.
Usage: python lemmaL_nodes.py <odd|even|Fodd|Feven> nlo nhi"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fam, graph
from lemmaL_test import classify_many, summarize, ins_str
from pump_verify import family, ins_tokens

def main():
    name = sys.argv[1]; nlo, nhi = int(sys.argv[2]), int(sys.argv[3])
    mk, parity, fname = family(name)
    pairs = 0; bad = 0; kept_total = 0
    for n in range(nlo, nhi + 1, 2):
        S = mk(n); g = graph.build(S)
        nodes = [graph.parse_pos(p)[0] for p in g.pos]
        dev = {i for t in nodes for i, (a, b) in enumerate(zip(t, S)) if a != b}
        wall = fam.wall_files(fname, n)
        cuts = [c for c in range(4, n - 5) if all(((c + d) in wall) and ((c + d) not in dev) for d in range(-4, 6))]
        texts = []
        for t in nodes:
            texts.append(" ".join(t))
            for c in cuts: texts.append(" ".join(ins_tokens(t, c)))
        blocks = classify_many(texts)
        k = 0
        for t in nodes:
            b0 = blocks[k]; k += 1
            k1, t1 = summarize(b0)
            for c in cuts:
                b2 = blocks[k]; k += 1
                k2, t2 = summarize(b2)
                pairs += 1; kept_total += sum(len(k1[X]) for X in "WB")
                for X in "WB":
                    if {ins_str(x, c) for x in k1[X]} != k2[X] or t1[X] != t2[X]: bad += 1
        print(f"{name} n={n}: {len(nodes)} nodes x {len(cuts)} cuts (c = {cuts[0]}..{cuts[-1]})  running totals: pairs {pairs}, mismatches {bad}", flush=True)
    print(f"Lemma 3 on actual nodes ({name}, n={nlo}..{nhi}): {pairs} (node, cut) pairs, {kept_total} kept moves compared, mismatches {bad}")
    return bad

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
