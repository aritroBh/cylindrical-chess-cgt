"""K76 referee of K75: own group table, contexts, positions and prediction (written without reading K75's gen.py,
pred75.py or groups.py beyond their usage lines).

Groups are read from the sources, not from K75's in/groups48.txt: K65's findings list (38 groups, roots and shuttle
square) and K67's in/groups_new.txt (10 groups; its C125_15 line is a rerun of a K65 group and is skipped).  Freezes
are not read anywhere: they are found by p74 (-m at the White-to-move roots; logs/alone76.out), see "freezes".

Usage (repository root; run with python3 -I):
  mk76.py alone                 -> the 96 roots alone (both sides to move), input for p74 -m (stdout)
  mk76.py freezes ALONE.out     -> table of groups with freezes, Definition 4.8 check by p74, F_Z, files, distances
  mk76.py qcheck                -> the 192 q positions alone (both sides to move), for p74 -m
  mk76.py pos G F N [K]         -> positions (8 per context) for group G, context file F, at most N + N pawns
                                   (N = 1, 2, 3; N = 6: all 729 placements); K = w=WORD,WORD,... keeps the contexts
                                   whose colour word (from rank 2 up, W/B; E = empty) is listed (a part of a split run);
                                   K = a|b: no White pawn above a Black pawn (a) or the rest (b) (not used in the end)
  mk76.py names G F N [K]       -> the context names in the same order
  mk76.py plan N LIMIT          -> a split of the N + N contexts into parts by colour word, each part reaching at most
                                   LIMIT contexts (greedy, words in lexicographic order)
  mk76.py pred N                -> prediction per context pattern (file-free), 8 values each
Positions per context: A b, A w, B b, B w, qA b, qA w, qB b, qB w.
"""
import itertools, re, sys

K65 = "kings/delegate/out/K65/findings.txt"
K67 = "kings/delegate/out/K67/in/groups_new.txt"
FREEZE = "kings/delegate/out/K75/verify/logs/freezes76.txt"
FILES = "abcdefgh"


def groups():
    G = {}
    for l in open(K65):
        m = re.match(r"^(C1\d\d_\d\d)\s+(K\w\d) (k\w\d) (.*?) /(\w\d)\s+Def 4.8", l)
        if m:
            pcs = m.group(4).split()
            G[m.group(1)] = (m.group(2)[1:], m.group(3)[1:], m.group(5),
                             sorted(p[1:] for p in pcs if p[0] == "P"), sorted(p[1:] for p in pcs if p[0] == "p"), "K65")
    for l in open(K67):
        n, pcs, a, b = l.strip().split("|")
        if n in G: continue
        pcs = pcs.split()
        G[n] = (pcs[0][1:], a, b, sorted(p[1:] for p in pcs[2:] if p[0] == "P"),
                sorted(p[1:] for p in pcs[2:] if p[0] == "p"), "K67")
    return G


def board(K, k, wp, bp, ctx, stm, ep="-"):
    return " ".join([f"K{K}", f"k{k}"] + [f"P{s}" for s in wp] + [f"p{s}" for s in bp] + ctx) + f" {stm} {ep}"


def load_freezes():
    F = {}
    for l in open(FREEZE):
        if l.startswith("#"): continue
        r = l.strip().split("|")
        F[r[0]] = (r[8], r[9])          # freeze at A, at B as "c2c4"
    return F


def qpawns(wp, fz):
    return sorted([fz[2:]] + [s for s in wp if s != fz[:2]])


def epq(fz, bp):
    """e.p. square after a double-step freeze if a Black pawn stands beside the arrival square"""
    if int(fz[3]) - int(fz[1]) != 2: return "-"
    for d in (-1, 1):
        f = FILES.find(fz[2]) + d
        if 0 <= f < 8 and FILES[f] + fz[3] in bp: return fz[2] + str(int(fz[1]) + 1)
    return "-"


def contexts(n, half=None):
    out = []
    mx = 6 if n == 6 else n
    for nw in range(mx + 1):
        for ws in itertools.combinations(range(2, 8), nw):
            for nb in range(mx + 1):
                for bs in itertools.combinations([r for r in range(2, 8) if r not in ws], nb):
                    out.append((ws, bs))
    if half and half.startswith("w="):
        keep = set(half[2:].split(","))
        out = [c for c in out if word(*c) in keep]
    elif half:
        above = lambda ws, bs: bool(ws) and bool(bs) and max(ws) > min(bs)
        out = [c for c in out if above(*c) == (half == "b")]
    return out


def word(ws, bs):
    """colour word of a context from rank 2 up, e.g. Ph2 ph3 -> WB; empty context -> E"""
    return "".join("W" if r in ws else "B" for r in sorted(ws + bs)) or "E"


def closure(cl):
    """contexts reachable from the list cl by pushes (single, double from the home rank) and removals (king captures);
    an over-estimate of what p74 enumerates (removal is allowed from every square)"""
    seen = set((frozenset(w), frozenset(b)) for w, b in cl)
    todo = list(seen)
    while todo:
        W, B = todo.pop(); occ = W | B; nxt = []
        for p in W:
            nxt.append((W - {p}, B))
            if p + 1 <= 7 and p + 1 not in occ: nxt.append((W - {p} | {p + 1}, B))
            if p == 2 and 3 not in occ and 4 not in occ: nxt.append((W - {p} | {4}, B))
        for p in B:
            nxt.append((W, B - {p}))
            if p - 1 >= 2 and p - 1 not in occ: nxt.append((W, B - {p} | {p - 1}))
            if p == 7 and 6 not in occ and 5 not in occ: nxt.append((W, B - {p} | {5}))
        for c in nxt:
            if c not in seen: seen.add(c); todo.append(c)
    return len(seen)


def plan(n, limit):
    """greedy partition of the contexts of size n into parts by colour word, each part's closure <= limit contexts"""
    cl = contexts(n)
    byw = {}
    for c in cl: byw.setdefault(word(*c), []).append(c)
    words = sorted(byw)                  # lexicographic order of the colour words keeps related words together
    parts, cur = [], []
    for w in words:
        trial = cur + [w]
        if cur and closure([c for x in trial for c in byw[x]]) > limit:
            parts.append(cur); cur = [w]
        else:
            cur = trial
    parts.append(cur)
    return [(p, closure([c for x in p for c in byw[x]]), sum(len(byw[x]) for x in p)) for p in parts]


def cname(f, ws, bs):
    return " ".join([f"P{f}{r}" for r in ws] + [f"p{f}{r}" for r in bs]) or "empty"


def positions(G, F, g, f, ws, bs):
    K, a, b, wp, bp, _ = G[g]
    ctx = [f"P{f}{r}" for r in ws] + [f"p{f}{r}" for r in bs]
    out = [board(K, a, wp, bp, ctx, "b"), board(K, a, wp, bp, ctx, "w"),
           board(K, b, wp, bp, ctx, "b"), board(K, b, wp, bp, ctx, "w")]
    for k, fz in ((a, F[g][0]), (b, F[g][1])):
        q = qpawns(wp, fz)
        out += [board(K, k, q, bp, ctx, "b", epq(fz, bp)), board(K, k, q, bp, ctx, "w")]
    return out


# ---- prediction.  X: pawns on one file as a D-game (Definition 1.3): a move is a push of one step, or two from the
# home rank (2 for White, 7 for Black) over an empty square; reaching rank 8 (White) / 1 (Black) is a terminal win;
# a side with no move loses.  Over (omega): Black may pass and stay in omega; White may move omega -> 0 once.
memo = {}
def val(W, B, om, side):
    """1 if White wins, 0 if Black wins; W, B frozensets of ranks; side 'w' or 'b' to move"""
    key = (W, B, om, side)
    if key in memo: return memo[key]
    occ = W | B
    res = None
    if side == "w":
        kids = [(W, B, False, "b")] if om else []
        for p in W:
            if p + 1 in occ: continue
            if p + 1 == 8: res = 1; break
            kids.append((W - {p} | {p + 1}, B, om, "b"))
            if p == 2 and 4 not in occ: kids.append((W - {p} | {4}, B, om, "b"))
        if res is None: res = int(any(val(*c) == 1 for c in kids))
    else:
        kids = [(W, B, om, "w")] if om else []
        for p in B:
            if p - 1 in occ: continue
            if p - 1 == 1: res = 0; break
            kids.append((W, B - {p} | {p - 1}, om, "w"))
            if p == 7 and 5 not in occ: kids.append((W, B - {p} | {5}, om, "w"))
        if res is None: res = int(not any(val(*c) == 0 for c in kids))
    memo[key] = res
    return res


def pred(ws, bs):
    W, B = frozenset(ws), frozenset(bs)
    c = lambda om, s: "W" if val(W, B, om, s) else "L"
    root = [c(True, "b"), c(True, "w")]
    q = [c(False, "b"), c(False, "w")]
    return root * 2 + q * 2


def fdist(f1, f2):
    return abs(FILES.find(f1) - FILES.find(f2))


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    G = groups()
    cmd = sys.argv[1]
    if cmd == "alone":
        # roots both sides; every White pawn move at a White-to-move root gives a q-candidate
        for g in sorted(G):
            K, a, b, wp, bp, _ = G[g]
            print(f"# {g}")
            for k in (a, b):
                print(board(K, k, wp, bp, [], "b")); print(board(K, k, wp, bp, [], "w"))
    elif cmd == "freezes":
        txt = open(sys.argv[2]).read().split("\n")
        # parse p74 -m output: position line, then move lines
        cur, mv = None, {}
        for l in txt:
            if not l.strip(): continue
            if not l.startswith("   "):
                cur = l.split("  P=")[0].strip(); mv[cur] = (l.split("P=")[1].strip(), [])
            else:
                nm, v = l.split(); mv[cur][1].append((nm, v))
        print("# name|men|src|WK|kA|kB|wp|bp|freeze A|freeze B|alone check|F_Z|context files|dW,dA,dB per file")
        for g in sorted(G):
            K, a, b, wp, bp, src = G[g]
            fr, ok = [], True
            for k in (a, b):
                rb, rw = mv[board(K, k, wp, bp, [], "b")], mv[board(K, k, wp, bp, [], "w")]
                # Black to move at the root: every move but the shuttle loses at once (value W after it)
                other = b if k == a else a
                bad = [n for n, v in rb[1] if v != "W" and n != f"K{k}-{other}"]
                good = [n for n, v in rw[1] if v != "L"]
                if bad or len(good) != 1 or good[0][0] == "K": ok = False
                fr.append(good[0].replace("-", "") if good else "?")
            F = {"x": tuple(fr)}
            fz = set()
            for s in [K, a, b] + wp + bp + [fr[0][2:], fr[1][2:]]: fz.add(s[0])
            ctx = [f for f in FILES if all(fdist(f, x) >= 2 for x in fz)]
            dist = ";".join(f"{f}:{fdist(f, K[0])},{fdist(f, a[0])},{fdist(f, b[0])}" for f in ctx)
            print("|".join([g, str(2 + len(wp) + len(bp)), src, K, a, b, ",".join(wp), ",".join(bp), fr[0], fr[1],
                            "ok" if ok else "CHECK", "".join(sorted(fz)), "".join(ctx), dist]))
    elif cmd == "qcheck":
        # q's alone, both sides to move, for p74 -m (Definition 4.8: every move loses at once)
        F = load_freezes()
        for g in sorted(G):
            for p in positions(G, F, g, "a", (), ())[4:]: print(p)
    elif cmd in ("pos", "names"):
        F = load_freezes()
        g, f, n = sys.argv[2], sys.argv[3], int(sys.argv[4])
        half = sys.argv[5] if len(sys.argv) > 5 else None
        for ws, bs in contexts(n, half):
            if cmd == "pos": print("\n".join(positions(G, F, g, f, ws, bs)))
            else: print(cname(f, ws, bs))
    elif cmd == "plan":
        for p, c, k in plan(int(sys.argv[2]), int(sys.argv[3])):
            print("w=" + ",".join(p), c, k)
    elif cmd == "pred":
        for ws, bs in contexts(int(sys.argv[2])):
            print(f"{cname('h', ws, bs):24s} " + " ".join(pred(ws, bs)))
