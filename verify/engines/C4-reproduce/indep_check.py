"""Independent re-check of claim C4 (engine suite), written by the verifier.

Uses NO code from engine/ or cylcgt/: own EPD parsing, own raw-cache indexing,
own pawn move generator and own minimax of the model (kings frozen, a side with
no pawn move loses, exactly-one-side-passed = win for that side, both passed =
"count" race rule as documented in cylcgt/pawns.py).

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      .venv/bin/python verify/engines/C4-reproduce/indep_check.py
"""
import collections
import functools
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SUITE = os.path.join(ROOT, "engine", "suite")
FILES = "abcdefgh"

# ---------------------------------------------------------------- raw tablebase cache
cache = {}
for p in glob.glob(os.path.join(SUITE, "tbcache", "*", "*.json")):
    r = json.load(open(p))
    cache[" ".join(r["fen"].split()[:4])] = r
print("raw cache records:", len(cache))

# perspective sanity over every cached record: root category must be consistent with move categories
bad_persp = 0
cats_seen = collections.Counter()
for k, r in cache.items():
    d = r.get("data") or {}
    mv = d.get("moves", [])
    for m in mv:
        cats_seen[m["category"]] += 1
    cats = {m["category"] for m in mv}
    root = d.get("category")
    if root == "unknown":
        continue
    exp = ("win" if cats & {"loss"} else "cursed-win" if cats & {"blessed-loss"} else
           "draw" if cats & {"draw"} else "blessed-loss" if cats & {"cursed-win"} else "loss")
    if mv and exp != root:
        bad_persp += 1
        print("PERSPECTIVE MISMATCH", k, root, cats)
print("perspective-inconsistent records:", bad_persp, "; move categories seen:", dict(cats_seen))


def tb_lookup(fen4):
    if fen4 in cache:
        return cache[fen4]
    f = fen4.split()
    f[3] = "-"
    return cache.get(" ".join(f))


# ---------------------------------------------------------------- EPD parsing
def parse(path):
    out = []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        fen4 = " ".join(line.split()[:4])
        ops = dict(re.findall(r'(\w+) ("[^"]*"|[^;]*);', line[len(fen4):]))
        ops = {k.strip(): v.strip().strip('"') for k, v in ops.items()}
        out.append((fen4, ops))
    return out


# ---------------------------------------------------------------- own model minimax
def board_of(fen4):
    rows = fen4.split()[0].split("/")
    b = {}
    for i, row in enumerate(rows):
        rank = 8 - i
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                b[(f, rank)] = ch
                f += 1
    return b


def passed(W, B, side):
    mine, th = (W, B) if side == "W" else (B, W)
    for f, r in mine:
        ahead = [(g, s) for g, s in th if abs(g - f) <= 1 and ((s > r) if side == "W" else (s < r))]
        if not ahead:
            return True
    return False


def dist(W, B, side):
    best = 10 ** 6
    mine = W if side == "W" else B
    for f, r in mine:
        # front passed pawn of its file
        one = (frozenset([(f, r)]), B) if side == "W" else (W, frozenset([(f, r)]))
        if not passed(one[0], one[1], side):
            continue
        occ = W | B
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, 9)):
                continue
            d = 8 - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            d = r - 1 - (1 if r == 7 else 0)
        best = min(best, d)
    return best


def gen(W, B, side, ep):
    """pawn moves on files a-d (0..3), flat; ep = target square usable by `side` or None."""
    mine, th = (W, B) if side == "W" else (B, W)
    occ = W | B
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else 7
    out = []
    for (f, r) in mine:
        r1 = r + d
        rest = mine - {(f, r)}
        if not 1 <= r1 <= 8:
            continue
        frm = f"{FILES[f]}{r}"
        promo = "q" if r1 in (1, 8) else ""
        if (f, r1) not in occ:
            out.append((frm + f"{FILES[f]}{r1}" + promo, "push", rest | {(f, r1)}, th, None))
            if r == start and (f, r + 2 * d) not in occ:
                out.append((frm + f"{FILES[f]}{r+2*d}", "double", rest | {(f, r + 2 * d)}, th, (f, r1)))
        for g in (f - 1, f + 1):
            if not 0 <= g <= 3:
                continue
            t = (g, r1)
            if t in th:
                out.append((frm + f"{FILES[g]}{r1}" + promo, "capture", rest | {t}, th - {t}, None))
            elif ep == t:
                out.append((frm + f"{FILES[g]}{r1}", "ep", rest | {t}, th - {(g, r)}, None))
    res = []
    for u, kind, nm, nt, newep in out:
        nW, nB = (frozenset(nm), frozenset(nt)) if side == "W" else (frozenset(nt), frozenset(nm))
        res.append((u, kind, nW, nB, newep))
    return res


def move_result(W, B, mover):
    """'win'/'loss' for the mover if terminal after the move, else None."""
    other = "B" if mover == "W" else "W"
    pw, pb = passed(W, B, "W"), passed(W, B, "B")
    if pw and pb:
        return "win" if dist(W, B, other) > dist(W, B, mover) else "loss"
    if pw or pb:
        return "win" if (pw if mover == "W" else pb) else "loss"
    return None


@functools.lru_cache(maxsize=None)
def stm_wins(W, B, side, ep):
    other = "B" if side == "W" else "W"
    for u, kind, nW, nB, newep in gen(W, B, side, ep):
        res = move_result(nW, nB, side)
        if res == "win":
            return True
        if res is None and not stm_wins(nW, nB, other, newep):
            return True
    return False


def predict(fen4):
    b = board_of(fen4)
    W = frozenset(s for s, p in b.items() if p == "P" and s[0] < 4)
    B = frozenset(s for s, p in b.items() if p == "p" and s[0] < 4)
    side = "W" if fen4.split()[1] == "w" else "B"
    other = "B" if side == "W" else "W"
    eps = fen4.split()[3]
    ep = None if eps == "-" else (FILES.index(eps[0]), int(eps[1]))
    wins, kinds = set(), {}
    for u, kind, nW, nB, newep in gen(W, B, side, ep):
        kinds[u] = kind
        res = move_result(nW, nB, side)
        if res == "win" or (res is None and not stm_wins(nW, nB, other, newep)):
            wins.add(u)
    return wins, kinds, b


# ---------------------------------------------------------------- checks
ver = parse(os.path.join(SUITE, "cgt_verified.epd"))
dis = parse(os.path.join(SUITE, "cgt_disagree.epd"))
print("verified lines:", len(ver), " disagree lines:", len(dis))
fens_v = [f for f, _ in ver]
fens_d = [f for f, _ in dis]
print("distinct FENs verified:", len(set(fens_v)), " disagree:", len(set(fens_d)),
      " overlap:", len(set(fens_v) & set(fens_d)))
print("side to move in verified:", collections.Counter(f.split()[1] for f in fens_v))
men = collections.Counter(sum(1 for c in f.split()[0] if c.isalpha()) for f in fens_v)
print("men count in verified:", dict(men))

problems = 0
nsol = collections.Counter()
slow = 0
slow_broad = 0
root_cats = collections.Counter()
for fen4, ops in ver:
    c2 = set(ops["c2"].split())
    r = tb_lookup(fen4)
    if r is None or r["status"] != 200:
        print("NO TB RECORD", fen4)
        problems += 1
        continue
    d = r["data"]
    root_cats[d["category"]] += 1
    tbwin = {m["uci"] for m in d["moves"] if m["category"] in ("loss", "blessed-loss")}
    odd = {m["uci"]: m["category"] for m in d["moves"] if m["category"] not in ("win", "loss", "draw")}
    if odd:
        print("non-plain categories", fen4, odd)
    pred, kinds, b = predict(fen4)
    tbsan = {m["uci"]: m["san"] for m in d["moves"]}
    bm = set(ops["bm"].split())
    pawn_ucis = set(kinds)
    tb_pawn = {u for u in tbsan if b.get((FILES.index(u[0]), int(u[1]))) in ("P", "p")}
    if pawn_ucis != tb_pawn:
        print("PAWN-MOVE SET MISMATCH", fen4, pawn_ucis ^ tb_pawn)
        problems += 1
    if not (d["category"] == "win" and tbwin == c2 and pred == c2 and {tbsan[u] for u in c2} == bm):
        print("MISMATCH", fen4, d["category"], sorted(tbwin), sorted(pred), sorted(c2), bm)
        problems += 1
    nsol[len(c2)] += 1
    if all(kinds.get(u) == "push" for u in c2) and any(k in ("double", "capture") for k in kinds.values()):
        slow += 1
    if all(kinds.get(u) == "push" for u in c2) and any(k in ("double", "capture", "ep") for k in kinds.values()):
        slow_broad += 1
print("verified problems:", problems)
print("verified TB root categories:", dict(root_cats))
print("verified #solutions:", dict(sorted(nsol.items())), " unique:", nsol[1])
print("slow (push-only wins, a double/capture exists):", slow, "; counting e.p. as capture too:", slow_broad)

# disagree file: bm/c2 must be the TB winning moves, or drawing moves when the root is a draw
dprob = 0
droot = collections.Counter()
for fen4, ops in dis:
    r = tb_lookup(fen4)
    d = r["data"]
    droot[d["category"]] += 1
    tbwin = {m["uci"] for m in d["moves"] if m["category"] in ("loss", "blessed-loss")}
    tbdraw = {m["uci"] for m in d["moves"] if m["category"] == "draw"}
    want = tbwin if tbwin else tbdraw
    pred, kinds, b = predict(fen4)
    c2 = set(ops["c2"].split())
    root_res = d["category"]
    cgt_root = "win" if pred else "loss"
    really_disagree = (pred != tbwin) or (cgt_root != root_res)
    if c2 != want or not really_disagree:
        print("DISAGREE-FILE PROBLEM", fen4, sorted(c2), sorted(want), really_disagree)
        dprob += 1
print("disagree problems:", dprob, " TB roots in disagree file:", dict(droot))

# every probed position: is any CGT/TB disagreement missing from both files?
sel = json.load(open(os.path.join(SUITE, "selection.json"))) + json.load(open(os.path.join(SUITE, "selection_ext.json")))
inv = set(fens_v) | set(fens_d)
missing = collections.Counter()
examples = []
for c in sel:
    fen4 = " ".join(c["fen"].split()[:4])
    r = tb_lookup(fen4)
    d = r["data"]
    tbwin = {m["uci"] for m in d["moves"] if m["category"] in ("loss", "blessed-loss")}
    pred, kinds, b = predict(fen4)
    agree = (pred == tbwin) and (("win" if pred else "loss") == d["category"])
    if fen4 not in inv:
        missing["agree" if agree else "DISAGREE"] += 1
        if not agree:
            examples.append((c["id"], c["tier"], fen4, d["category"], sorted(pred)))
print("probed positions:", len(sel), "; in neither file:", dict(missing))
for e in examples:
    print("   omitted disagreement:", e)

# ---------------------------------------------------------------- cross-check own minimax vs cylcgt outcomes
res = json.load(open(os.path.join(SUITE, "results.json")))
bad = 0
for r in res:
    fen4 = " ".join(r["fen"].split()[:4])
    pred, kinds, b = predict(fen4)
    if pred != set(r["rules"]["count"]["pred_win"]):
        bad += 1
        print("results.json count pred differs from own minimax", r["id"], fen4)
print("results.json rows:", len(res), "; own-minimax vs cylcgt(count) winning-set mismatches:", bad)

cands = json.load(open(os.path.join(SUITE, "candidates.json")))
bad = 0
for rec in cands:
    W = frozenset((FILES.index(s[0]), int(s[1])) for s in rec["white"])
    B = frozenset((FILES.index(s[0]), int(s[1])) for s in rec["black"])
    ep = (FILES.index(rec["ep"][0]), int(rec["ep"][1])) if rec["ep"] else None
    side = rec["stm"]
    other = "B" if side == "W" else "W"
    mine = set()
    allm = set()
    for u, kind, nW, nB, newep in gen(W, B, side, ep):
        allm.add(u)
        res_ = move_result(nW, nB, side)
        if res_ == "win" or (res_ is None and not stm_wins(nW, nB, other, newep)):
            mine.add(u)
    theirs = {m[0] for m in rec["rules"]["count"]["moves"] if m[4]}
    if mine != theirs or allm != {m[0] for m in rec["rules"]["count"]["moves"]} \
            or bool(mine) != rec["rules"]["count"]["stm_wins"]:
        bad += 1
        if bad < 5:
            print("candidate mismatch", rec["pos"], rec["stm"], rec["ep"], sorted(mine), sorted(theirs))
print("candidates:", len(cands), "; own-minimax vs cylcgt(count) mismatches:", bad)

# value classes of the verified set, with the actual value strings
vc = collections.defaultdict(collections.Counter)
byfen = {" ".join(r["fen"].split()[:4]): r for r in res}
for fen4, ops in ver:
    r = byfen[fen4]
    vc[r["features"]["class"]][r["value"]["count"]] += 1
for k, cnt in sorted(vc.items()):
    print(f"class {k}: n={sum(cnt.values())}  values={dict(cnt)}")
