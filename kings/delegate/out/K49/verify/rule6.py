# Proposition 6 (pawn on rank H-1): rule vs computed class and type, vk.c
import sys, subprocess
TESTS = ["zero", "on", "off", "dud", "over", "under", "star", "up", "down", "pm1", "onstar", "m1", "m2", "m3", "p1", "p2", "zoff", "zdud"]
def run(W, H, t):
    d = {}
    for l in subprocess.run(["./vk", str(W), str(H), f"t/{t}.t"], capture_output=True, text=True).stdout.split("\n"):
        if l:
            a = l.split(); d[(a[0][1:], a[1][1:], a[2][1:], a[3])] = a[4]
    return d
def sqp(s): return ord(s[0]) - 97, int(s[1:]) - 1
def classify(W, H, R):
    out = {}
    base = [t for t in TESTS if t not in ("zoff", "zdud")]
    for k in R["zero"]:
        sig = {t: R[t][k] for t in base}
        if all(v == "W" for v in sig.values()): c = "DEC"
        elif all(v == "D" for v in sig.values()): c = "DUD"
        elif all(sig[t] == ("D" if t in ("off", "dud") else "W") for t in base): c = "ON"
        else: c = "OTHER"
        typ = ""
        if c == "ON":
            z = (R["zoff"][k], R["zdud"][k])
            typ = {("W", "W"): "L", ("D", "D"): "R"}.get(z, "?")
        out[k] = (c, typ)
    return out
def rule(W, H, wk, p, bk, s):
    fdist = lambda a, b: min(abs(a - b), W - abs(a - b))
    kd = lambda a, b: max(fdist(a[0], b[0]), abs(a[1] - b[1]))
    f = p[0]; q = (f, H - 1); Pi = [((f + d) % W, H - 3) for d in (-1, 0, 1)]
    dPi = min(kd(wk, x) for x in Pi)
    def wtm(wk, bk):
        if bk != q: return ("DEC", "")
        if dPi_of(wk) == 0: return ("ON", "L")
        if dPi_of(wk) == 1: return ("ON", "R")
        return ("DUD", "")
    dPi_of = lambda w: min(kd(w, x) for x in Pi)
    if s == "w": return wtm(wk, bk)
    if kd(bk, p) == 1 and kd(wk, p) > 1: return ("DUD", "")       # B1
    if bk == q: return ("ON", "R")                                   # B2
    if kd(bk, q) == 1 and kd(wk, q) > 1 and wk != q: return wtm(wk, q)  # B3
    return ("DEC", "")                                               # B4
tot = 0
for b in sys.argv[1:]:
    W, H = map(int, b.split("x"))
    R = {t: run(W, H, t) for t in TESTS}
    C = classify(W, H, R)
    n = bad = 0; b3 = {}
    from collections import Counter
    cnt = Counter()
    for k, (c, typ) in C.items():
        wk, p, bk, s = sqp(k[0]), sqp(k[1]), sqp(k[2]), k[3]
        if p[1] != H - 2: continue
        n += 1
        r = rule(W, H, wk, p, bk, s)
        cnt[(s,) + r] += 1
        if r != (c, typ):
            bad += 1
            if bad < 4: print("EXC", b, k, "rule", r, "computed", (c, typ))
    other = sum(1 for v in C.values() if v[0] == "OTHER")
    tot += n
    print(f"cyl:{b}: {n} positions with pawn on rank H-1, {bad} exceptions (class and type); OTHER signatures on whole board: {other}; {dict(sorted(cnt.items()))}", flush=True)
print("total", tot)
