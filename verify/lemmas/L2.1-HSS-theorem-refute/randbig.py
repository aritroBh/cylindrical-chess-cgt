"""Random falsification of Theorem 2.1 on larger boards (up to 8x8), focusing on
NON-TRIVIAL HSS positions (some reachable non-terminal node has >= 2 live
components and some component has a threat). Uses only indep.py.

Roots: random pawn placements on ranks 2..m-1, plus (e.p. on) a random legal
double step played first so that the root may carry a live right.

usage: python -I randbig.py SEED N_PER_BOARD MAXSEC [PER_POS_SEC]
"""
import sys, time, random, signal
from collections import Counter
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import indep as I

seed, nper, maxsec = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
perpos = int(sys.argv[4]) if len(sys.argv) > 4 else 20
rng = random.Random(seed)
RULES = ("count", "mover", "opponent")
BOARDS = [(8, 8, 1, 1), (8, 8, 1, 0), (8, 8, 0, 1), (8, 8, 0, 0), (7, 8, 1, 1), (6, 8, 0, 1),
          (8, 7, 1, 0), (8, 6, 0, 1), (7, 7, 1, 1), (6, 6, 1, 0)]


class TO(Exception):
    pass


def _alarm(*a):
    raise TO()


signal.signal(signal.SIGALRM, _alarm)


def clear_all():
    I.clear_caches()
    I._tau_cache.clear()


def props_factory(bd):
    tau = I.tau_of(bd)
    memo = {}

    def live(z):
        return bool(I.gen_moves(bd, z, "W") or I.gen_moves(bd, z, "B"))

    def props(y):
        r = memo.get(y)
        if r is not None:
            return r
        comps = I.components(bd, y)
        h, e_ok, nt = True, True, False
        if len(comps) >= 2:
            ts = [tau(c) for c in comps]
            if any(1 in a and -1 in b for i, a in enumerate(ts) for j, b in enumerate(ts) if i != j):
                h = False
            if I.ep_usable(bd, y):
                e_ok = False
            if sum(1 for c in comps if live(c)) >= 2 and any(ts):
                nt = True
        for side in ("W", "B"):
            for c in I.gen_moves(bd, y, side):
                wp, bp = I.status(bd, c)
                if not (wp or bp):
                    ch, ce, cn = props(c)
                    h &= ch; e_ok &= ce; nt |= cn
        r = (h, e_ok, nt)
        memo[y] = r
        return r
    return props


stats = Counter()
cex = []
t0 = time.time()
for (n, m, wrap, ep) in BOARDS:
    clear_all()
    bd = I.Board(n, m, bool(wrap), bool(ep))
    props = props_factory(bd)
    got = 0
    tries = 0
    while got < nper and time.time() - t0 < maxsec and tries < 50 * nper:
        tries += 1
        nw, nb = rng.randint(2, 5), rng.randint(2, 5)
        sqs = [(f, r) for f in range(n) for r in range(2, m)]
        pick = rng.sample(sqs, nw + nb)
        x = I.mkpos(pick[:nw], pick[nw:])
        if ep and rng.random() < 0.5:
            side = rng.choice("WB")
            ds = [c for c in I.gen_moves(bd, x, side) if c[2] is not None]
            if ds:
                x = rng.choice(ds)
        wp, bp = I.status(bd, x)
        if wp or bp:
            continue
        signal.alarm(perpos)
        try:
            h, e_ok, nt = props(x)
            if not (h and nt):
                signal.alarm(0)
                stats[("skip", "HSS" if h else "notHSS", "nontriv" if nt else "triv")] += 1
                continue
            mw, mbb = I.move_bound(bd, x)
            bt = max(mw, mbb) + 1
            res = []
            for rule in RULES:
                try:
                    ow = I.oW(bd, x, rule)
                except I.RaceRoot:
                    continue
                o1 = I.oS(bd, x, rule, BIG=bt)
                o2 = I.oS(bd, x, rule, BIG=256)
                res.append((rule, ow, o1, o2))
            signal.alarm(0)
        except TO:
            stats["timeout"] += 1
            clear_all()
            props = props_factory(bd)
            continue
        got += 1
        for rule, ow, o1, o2 in res:
            k = ("E" if e_ok else "notE", "agree" if (o1 == ow and o2 == ow) else "DISAGREE")
            stats[k] += 1
            if e_ok and (o1 != ow or o2 != ow):
                cex.append((str(bd), I.show(x), rule, ow, o1, o2))
            if not e_ok and (o1 != ow or o2 != ow):
                cex.append(("notE", str(bd), I.show(x), rule, ow, o1, o2))
        stats["rootep" if x[2] else "rootplain"] += 1
    stats[f"nontrivHSS[{bd}]"] = got
print(f"seed={seed} time={time.time()-t0:.0f}s")
for k in sorted(stats, key=str):
    print("   ", k, stats[k])
print("COUNTEREXAMPLES:", len([c for c in cex if c[0] != "notE"]))
for c in cex[:30]:
    print("   ", c)
