import sys, subprocess
sys.path.insert(0, "research/ring_family")
from ringlib import *
def fam(prefix, period, k, suffix):
    return from_cstr(prefix) + from_cstr(period) * k + from_cstr(suffix)
def counts(ring):
    n = len(ring)
    inp = to_text(ring) + "\n"
    out = subprocess.run(["research/ring_family/ringeval_w", "--width", str(n), "--reduced", "-"], input=inp, capture_output=True, text=True).stdout
    lines = out.strip().split("\n")
    return lines[0].split("\t")[1:3], lines[1].strip()
for name, (pre, per, suf, k0, k1) in {"odd": ("B5 W2B5", "W3 B5", "W23B4", 1, 9), "even": ("B4 W2", "B4 W2", "B5 W2B5 W35B6 W2", 0, 8)}.items():
    print("==", name)
    for k in range(k0, k1 + 1):
        r = fam(pre, per, k, suf)
        v, c = counts(r)
        print(f"k={k} C{len(r)} {v} {c}")
