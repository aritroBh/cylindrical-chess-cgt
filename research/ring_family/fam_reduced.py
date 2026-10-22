import sys, subprocess
sys.path.insert(0, "research/ring_family")
from ringlib import *
from touched import touched
def go(label, pre, per, suf, ks):
    print("==", label)
    for k in ks:
        r = from_cstr(pre) + from_cstr(per) * k + from_cstr(suf)
        n = len(r)
        p = subprocess.run(["nice", "-n", "15", "research/ring_family/ringeval_w", "--width", str(n), "--reduced", "/tmp/fr.tsv", "--max-entries", "4194304", "--rg-cap", "300000"], input=to_text(r) + "\n", capture_output=True, text=True)
        lines = p.stdout.strip().split("\n")
        edges = [l.rstrip("\n").split("\t") for l in open("/tmp/fr.tsv")]
        t, m = touched(edges)
        nodes = lines[-1].split("nodes=")[1].split()[0]
        print(f"  k={k} C{n} {lines[0].split(chr(9))[1]}{lines[0].split(chr(9))[2]} reduced nodes={nodes} untouched files={n-len(t)} touched={''.join(chr(97+i) for i in sorted(t))}")
go("F2: B5 W2B3 | (W5 B7)^k | W3B6 W3 W2B5", "B5 W2B3", "W5 B7", "W3B6 W3 W2B5", range(1, 7))
go("F3: B5 W2B3 | (B4 W2)^k | W3B6 W3 W2B5", "B5 W2B3", "B4 W2", "W3B6 W3 W2B5", range(1, 7))
go("F4: B5 W23 | (W4 B6)^k | B5 W3 W4B7 W3B7", "B5 W23", "W4 B6", "B5 W3 W4B7 W3B7", range(1, 7))
go("F7: B5 W23 B5 W3 | (W2 B4)^k? -> use slot 4", "B5 W23 B5 W3", "W2 B4", "W4B7 W3B7", range(1, 7))
