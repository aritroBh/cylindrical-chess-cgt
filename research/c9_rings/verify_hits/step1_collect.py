"""step1_collect.py -- collect every NNPN/NNNP hit from ALL final chunk outputs under work/c9p10 (not the partial merge),
check completeness of the chunk set, reduce to classes under rotation, reflection and colour reversal, test legality
with ringtools.legality (own code), write hits_all.tsv, classes.tsv, legality.tsv."""
import os, glob, collections, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ringtools as rt

WORK = os.path.join(HERE, "..", "work", "c9p10")
chunks = sorted(glob.glob(os.path.join(WORK, "s*_c*of*.summary.txt")))
print("summary files:", len(chunks))
byK = collections.defaultdict(set)
tot_rings = collections.Counter()
unres = 0
sig_hist = collections.Counter()
hit_rows = []          # (file, ring, sig, nodes)
missing_done = []
for s in chunks:
    base = s[:-len(".summary.txt")]
    nm = os.path.basename(base)           # s5_5_c012of400
    split, rest = nm.split("_c")
    ci, ck = rest.split("of")
    byK[(split, int(ck))].add(int(ci))
    if not os.path.exists(base + ".done"):
        missing_done.append(nm)
    kv = dict(l.rstrip("\n").split("\t", 1) for l in open(s) if "\t" in l)
    tot_rings[split] += int(kv["rings_sent"])
    unres += int(kv["unresolved"])
    if int(kv["rings_sent"]) != int(kv["rings_solved"]) + int(kv["unresolved"]):
        print("MISMATCH rings", nm)
    for l in open(base + ".hist.tsv"):
        sg, c = l.split()
        sig_hist[(split, sg)] += int(c)
    for l in open(base + ".hits.tsv"):
        if l.strip():
            r, sg, nd = l.rstrip("\n").split("\t")
            hit_rows.append((nm, r, sg, int(nd)))
    # err files must be empty (or only benign)
    if os.path.getsize(base + ".err") > 0:
        print("non-empty .err:", nm, open(base + ".err").read()[:200].replace("\n", " | "))

for (split, K), got in sorted(byK.items()):
    print("split %s: K=%d, chunks present %d, complete=%s" % (split, K, len(got), got == set(range(K))))
print("chunks without .done:", missing_done)
print("total unresolved:", unres)
print("rings per split:", dict(tot_rings), "total", sum(tot_rings.values()))

# cross-check: signatures with P at h=2 or h=3 in the histograms vs hit lines
ph = collections.Counter()
for (split, sg), c in sig_hist.items():
    if len(sg) == 4 and (sg[2] == "P" or sg[3] == "P"):
        ph[(split, sg)] += c
print("histogram signatures with P at h=2/h=3:", dict(ph))
print("hit lines:", len(hit_rows))
assert sum(ph.values()) == len(hit_rows), "hist count != hits lines"

# colour reversal: the split k+m <-> m+k histograms should be mirror images (L<->R)
sw = {"L": "R", "R": "L", "N": "N", "P": "P"}
mism = 0
for (split, sg), c in sig_hist.items():
    a, b = split.split("_")[0][1:], split.split("_")[1]
    other = "s%s_%s" % (b, a)
    osg = "".join(sw[x] for x in sg)
    if sig_hist.get((other, osg), 0) != c:
        mism += 1
print("histogram mirror mismatches between split k+m and m+k:", mism)

with open(os.path.join(HERE, "hits_all.tsv"), "w") as f:
    for nm, r, sg, nd in hit_rows:
        f.write("%s\t%s\t%s\t%d\n" % (nm, r, sg, nd))

classes = collections.defaultdict(list)
for nm, r, sg, nd in hit_rows:
    classes[rt.canon_full(rt.parse(r))].append((r, sg, nm))
print("distinct hit rings (as printed):", len(set(r for _, r, _, _ in hit_rows)))
print("classes under rotation+reflection+colour reversal:", len(classes))
with open(os.path.join(HERE, "classes.tsv"), "w") as cf, open(os.path.join(HERE, "legality.tsv"), "w") as lf:
    cf.write("class_id\tcanonical\tmembers_in_hits\tsplit\n")
    lf.write("ring\tkind\tsplit\tlegal\tviolations\n")
    for i, (c, mem) in enumerate(sorted(classes.items())):
        cid = "H%d" % (i + 1)
        cf.write("%s\t%s\t%d\t%s\n" % (cid, rt.fmt(c), len(mem), rt.split_of(c)))
        print(cid, rt.fmt(c), "| hit members:", [(m[0], m[1]) for m in mem])
        # all hit rings and colour reversals
        for r, sg, nm in mem:
            for kind, ring in (("hit", rt.parse(r)), ("colour_reversed", rt.colour_reverse(rt.parse(r)))):
                errs = rt.legality(ring, 9, 10)
                lf.write("%s\t%s\t%s\t%s\t%s\n" % (rt.fmt(ring), kind, rt.split_of(ring), "legal" if not errs else "ILLEGAL", "; ".join(errs)))
# which hit rings are colour reversals of other hit rings
hs = {}
for nm, r, sg, nd in hit_rows:
    hs[r] = rt.parse(r)
canon_d = {r: rt.canon_dihedral(p) for r, p in hs.items()}
cd_set = set(canon_d.values())
print("hit rings whose colour reversal is also a hit (up to dihedral):",
      sum(1 for r, p in hs.items() if rt.canon_dihedral(rt.colour_reverse(p)) in cd_set), "of", len(hs))
print("dihedral classes among hits:", len(cd_set))
