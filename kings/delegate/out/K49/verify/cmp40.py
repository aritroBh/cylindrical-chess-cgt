# compare vk.c with K40's (N) sum tables (CHECKED-2) on a board, for the tests vk shares
import sys, subprocess, lzma
W, H = int(sys.argv[1]), int(sys.argv[2])
tests = {"0": "zero", "1": "p1", "2": "p2", "3": "p3", "-1": "m1", "-2": "m2", "-3": "m3", "on": "on", "off": "off",
         "dud": "dud", "over": "over", "under": "under", "*": "star", "up": "up", "down": "down", "+-1": "pm1"}
def run(t, extra=()):
    out = subprocess.run(["./vk", str(W), str(H), f"t/{t}.t", *extra], capture_output=True, text=True).stdout.split("\n")
    d = {}
    for l in out:
        if not l: continue
        a = l.split()
        d[(a[0][1:], a[2][1:], a[1][1:], a[3])] = a[4]
    return d
mine = {k: run(v) for k, v in tests.items()}
rows = lzma.open(f"../../K40/data/sums_normal_cyl_{W}x{H}.tsv.xz", "rt").read().split("\n")
hdr = rows[0].split("\t")
diff = n = 0
seen = set()
for r in rows[1:]:
    if not r: continue
    c = r.split("\t"); wk, bk, p, s = c[0].split()
    key = (wk, bk, p, s); seen.add(key)
    for k in tests:
        n += 1
        if mine[k].get(key) != c[hdr.index(k)]:
            diff += 1
            if diff < 5: print("DIFF", key, k, mine[k].get(key), c[hdr.index(k)])
extra = set(mine["0"]) - seen
print(f"cyl:{W}x{H}: {len(seen)} K40 rows, {n} results compared, {diff} differences, {len(extra)} positions only in vk")
