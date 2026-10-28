"""step3b: each hit and each colour reversal in its OWN fresh process of the original rg (no shared memo), H=3 and H=6."""
import os, sys, subprocess
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
RG = os.path.join(HERE, "..", "..", "ring_family_proof", "rg")
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "step3_rg.tsv"))][1:]
out = []
for kind, ring, *_ in rows:
    r = []
    for H in (3, 6):
        p = subprocess.run(["nice", "-n", "15", RG, "solve", str(H)], input=ring + "\n", capture_output=True, text=True, env=dict(os.environ, TBITS="22"))
        assert p.returncode == 0, p.stderr
        r.append(p.stdout.split()[0])
    out.append((kind, ring, r[0], r[1]))
    print("%-16s %-34s H=3: %s   H=6: %s" % (kind, ring, r[0], r[1]), flush=True)
open(os.path.join(HERE, "step3b_rg_single.tsv"), "w").write("kind\tring\tsig_h0_3\tsig_h0_6\n" + "".join("\t".join(o) + "\n" for o in out))
