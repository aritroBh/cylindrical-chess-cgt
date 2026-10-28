"""step3_rg.py -- re-solve every hit and its colour reversal with (a) the ORIGINAL rg binary
research/ring_family_proof/rg, (b) fresh builds of rg.c (MAXN default and MAXN=64).  Batches <= 40, fresh process per batch, nice 15."""
import os, sys, subprocess, time, resource
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ringtools as rt
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "hits_all.tsv"))]
drive_sig = {r: sg for _, r, sg, _ in rows}
rings = sorted(drive_sig)
items = []     # (label, text)
for r in rings:
    items.append(("hit", r))
    items.append(("colour_reversed", rt.fmt(rt.colour_reverse(rt.parse(r)))))
bins = {"rg_original": os.path.join(HERE, "..", "..", "ring_family_proof", "rg"),
        "rg_fresh": os.path.join(HERE, "rg_fresh"), "rg_fresh_maxn64": os.path.join(HERE, "rg_fresh64")}
res = {}
for name, b in bins.items():
    assert len(items) <= 40
    t0 = time.time()
    p = subprocess.run(["nice", "-n", "15", b, "solve", "3"], input="\n".join(t for _, t in items) + "\n",
                       capture_output=True, text=True, env=dict(os.environ, TBITS="22"))
    out = [l.split() for l in p.stdout.splitlines() if l.strip()]
    assert p.returncode == 0 and len(out) == len(items), (name, p.returncode, len(out), p.stderr[:200])
    res[name] = [(o[0], o[1]) for o in out]
    print(name, "rc", p.returncode, "outputs", len(out), "wall %.1fs" % (time.time() - t0))
with open(os.path.join(HERE, "step3_rg.tsv"), "w") as f:
    f.write("kind\tring\tsig_drive_rg_copy\t" + "\t".join(bins) + "\tnodes_original\n")
    for i, (kind, t) in enumerate(items):
        ds = drive_sig.get(t, "(mirror of a hit; driver sig N/A)")
        f.write("%s\t%s\t%s\t%s\t%s\n" % (kind, t, ds, "\t".join(res[n][i][0] for n in bins), res["rg_original"][i][1]))
bad = 0
for i, (kind, t) in enumerate(items):
    s = {res[n][i][0] for n in bins}
    if s != {"NNPN"}: bad += 1
print("rings", len(items), "not NNPN under some rg build:", bad)
print(open(os.path.join(HERE, "step3_rg.tsv")).read())
