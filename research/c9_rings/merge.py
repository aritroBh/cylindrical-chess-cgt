#!/usr/bin/env python3
"""merge.py DIR [--known KNOWN.tok N] -> text summary on stdout.

Reads every DIR/**/*.summary.txt written by drive.py (with its .hist.tsv and .hits.tsv), groups the chunks by split
(N P NW NB from the recorded command), and prints per split: chunks seen, rings, counts per signature, the *2/*3 rows,
every ring with a P at h=2 or h=3, and the failures.  With --known (a file of rg-token rings, scanner hits) it
canonicalises both sides under the dihedral group and says which hits were found and whether a found ring is unknown."""
import sys, os, glob, collections, re

NAMES = {"PNNN": "0", "NPNN": "*1", "NNPN": "*2", "NNNP": "*3", "NNNN": "fuzzy with 0,*1,*2,*3",
         "LLLL": "G>0 (Left wins)", "RRRR": "G<0 (Right wins)"}

def canon(ring):
    t = ring.split()
    n = len(t)
    imgs = []
    for s in range(n):
        imgs.append(tuple(t[(i + s) % n] for i in range(n)))
        imgs.append(tuple(t[(s - i) % n] for i in range(n)))
    return min(imgs)

def read_kv(fn):
    d = {}
    for line in open(fn):
        k, _, v = line.rstrip("\n").partition("\t")
        d[k] = v
    return d

def main():
    a = sys.argv[1:]
    root = a[0]
    known = None
    if "--known" in a:
        known = {}
        for line in open(a[a.index("--known") + 1]):
            if line.strip():
                r = line.split("\t")[0].strip()
                known[canon(r)] = r
    groups = collections.defaultdict(lambda: dict(chunks=set(), K=set(), rings=0, nodes=0, hist=collections.Counter(), hits=[], unresolved=0, wall=0.0))
    for sfn in sorted(glob.glob(os.path.join(root, "**", "*.summary.txt"), recursive=True)):
        kv = read_kv(sfn)
        cmd = kv["cmd"].split()
        N, P, NW, NB = cmd[2:6]
        ci, ck = int(cmd[cmd.index("--chunk") + 1]), int(cmd[cmd.index("--chunk") + 2])
        g = groups[(int(N), int(P), int(NW), int(NB))]
        g["chunks"].add(ci); g["K"].add(ck)
        g["rings"] += int(kv["rings_sent"]); g["nodes"] += int(kv["rg_nodes_total"]); g["unresolved"] += int(kv["unresolved"])
        g["wall"] += float(kv["wall_seconds"])
        base = sfn[:-len(".summary.txt")]
        for line in open(base + ".hist.tsv"):
            s, c = line.split()
            g["hist"][s] += int(c)
        for line in open(base + ".hits.tsv"):
            if line.strip():
                g["hits"].append(line.rstrip("\n").split("\t"))
    for key in sorted(groups):
        N, P, NW, NB = key
        g = groups[key]
        print("== C%d, %d pawns, split %d+%d: chunks %d of K=%s, rings %d, rg nodes %d, unresolved %d, driver wall %.0fs"
              % (N, P, NW, NB, len(g["chunks"]), sorted(g["K"]), g["rings"], g["nodes"], g["unresolved"], g["wall"]))
        for s, c in sorted(g["hist"].items(), key=lambda x: -x[1]):
            print("   %-6s %10d  %s" % (s, c, NAMES.get(s, "")))
        print("   rings with P at h=2 or h=3: %d  (*2: %d, *3: %d, other: %d)" % (
            len(g["hits"]), sum(1 for h in g["hits"] if h[1] == "NNPN"), sum(1 for h in g["hits"] if h[1] == "NNNP"),
            sum(1 for h in g["hits"] if h[1] not in ("NNPN", "NNNP"))))
        for h in g["hits"]:
            print("   HIT\t%s\t%s" % (h[0], h[1]))
        if known is not None:
            found = {}
            unknown = []
            for h in g["hits"]:
                c = canon(h[0])
                if c in known: found[c] = h
                else: unknown.append(h)
            print("   known hits found: %d of %d; hits not in the known list: %d" % (len(found), len(known), len(unknown)))
            for c, h in found.items():
                print("   FOUND\t%s\t%s" % (h[0], h[1]))
            for h in unknown:
                print("   NOT-IN-LIST\t%s\t%s" % (h[0], h[1]))

if __name__ == "__main__":
    main()
