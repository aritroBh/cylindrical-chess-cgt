# Lemma P (y_b in W_N => y_w in W_N, Black not in check) and Theorem 1 (r(x+n) = r(x+0), n = -3..3) with vk.c
import sys, subprocess
def run(W, H, t):
    d = {}
    for l in subprocess.run(["./vk", str(W), str(H), f"t/{t}.t"], capture_output=True, text=True).stdout.split("\n"):
        if l:
            a = l.split(); d[(a[0], a[1], a[2], a[3])] = a[4]
    return d
for b in sys.argv[1:]:
    W, H = map(int, b.split("x"))
    z = run(W, H, "zero")
    viol = []; nplace = 0
    for (wk, p, bk, s), v in z.items():
        if s != "b": continue
        tw = (wk, p, bk, "w")
        if tw not in z: continue  # Black in check
        nplace += 1
        if v == "W" and z[tw] != "W": viol.append((wk, p, bk, z[tw]))
    msg = f"cyl:{b}: {nplace} placements (Black not in check), Lemma P violations {len(viol)}"
    if viol:
        from collections import Counter
        msg += f" (y_w results {dict(Counter(v[3] for v in viol))}; e.g. {' '.join(viol[0][:3])})"
    if len(sys.argv) and W * H <= 64:
        bad = 0
        for t in ["m1", "m2", "m3", "p1", "p2", "p3"]:
            d = run(W, H, t)
            bad += sum(1 for k in z if d[k] != z[k])
        msg += f"; Theorem 1, n in -3..3: {bad} positions with r(x+n) != r(x+0)"
    print(msg, flush=True)
