"""Independent re-check of claim C3 (depth-1 promotion-race nodes vs Lichess tablebase).

Does NOT import cylcgt, cgtpos, build_suite, tb or realchess. Reads only:
  engine/suite/selection.json, engine/suite/selection_ext.json   (which FENs were probed)
  engine/suite/tbcache/**.json, realchess/cache/**.json           (cached Lichess replies)
Everything else (FEN parsing, pawn move generation, passed-pawn test, promotion
distance, Lichess category -> mover result) is re-implemented here.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      .venv/bin/python -I verify/engines/C3-reproduce/indep_race.py
"""
import collections
import glob
import json
import os

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
OUT = os.path.join(ROOT, "verify/engines/C3-reproduce")
F = "abcdefgh"

sel = json.load(open(os.path.join(ROOT, "engine/suite/selection.json")))
sel += json.load(open(os.path.join(ROOT, "engine/suite/selection_ext.json")))

cache = {}
for d in ("engine/suite/tbcache", "realchess/cache"):
    for p in glob.glob(os.path.join(ROOT, d, "*", "*.json")):
        try:
            rec = json.load(open(p))
        except Exception:
            continue
        cache[" ".join(rec["fen"].split()[:4])] = rec


def parse(fen):
    board, stm, _c, ep = fen.split()[:4]
    sq = {}
    for i, row in enumerate(board.split("/")):
        r = 8 - i
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                sq[(f, r)] = ch
                f += 1
        assert f == 8
    return sq, stm, ep


def passed(sq, white):
    me, them = ("P", "p") if white else ("p", "P")
    for (f, r), p in sq.items():
        if p != me:
            continue
        ahead = (lambda s: s > r) if white else (lambda s: s < r)
        if not any(q == them and abs(g - f) <= 1 and ahead(s) for (g, s), q in sq.items()):
            return True
    return False


def dist(sq, white):
    me, them = ("P", "p") if white else ("p", "P")
    best = None
    for (f, r), p in sq.items():
        if p != me:
            continue
        ahead = (lambda s: s > r) if white else (lambda s: s < r)
        if any(q == them and abs(g - f) <= 1 and ahead(s) for (g, s), q in sq.items()):
            continue  # not passed
        if any((f, s) in sq for s in range(1, 9) if ahead(s)):
            continue  # file blocked by any piece
        d = (8 - r - (r == 2)) if white else (r - 1 - (r == 7))
        best = d if best is None else min(best, d)
    return best


def pawn_moves(sq, stm, ep):
    white = stm == "w"
    me, them = ("P", "p") if white else ("p", "P")
    dr = 1 if white else -1
    out = []
    for (f, r), p in list(sq.items()):
        if p != me:
            continue
        r1 = r + dr
        promo = "q" if r1 in (1, 8) else ""
        if (f, r1) not in sq:
            n = dict(sq); del n[(f, r)]; n[(f, r1)] = me
            out.append((f"{F[f]}{r}{F[f]}{r1}{promo}", n))
            r2 = r + 2 * dr
            if r == (2 if white else 7) and (f, r2) not in sq:
                n = dict(sq); del n[(f, r)]; n[(f, r2)] = me
                out.append((f"{F[f]}{r}{F[f]}{r2}", n))
        for g in (f - 1, f + 1):
            if not 0 <= g < 8:
                continue
            t = (g, r1)
            if sq.get(t) == them:
                n = dict(sq); del n[(f, r)]; n[t] = me
                out.append((f"{F[f]}{r}{F[g]}{r1}{promo}", n))
            elif ep != "-" and t == (F.index(ep[0]), int(ep[1])):
                n = dict(sq); del n[(f, r)]; n[t] = me; del n[(g, r)]
                out.append((f"{F[f]}{r}{F[g]}{r1}", n))
    return out


# Lichess: a move's category is for the side to move AFTER the move.
MOVER = {"loss": "win", "blessed-loss": "win", "win": "loss", "cursed-win": "loss", "draw": "draw"}

rows = []
missing = 0
persp_bad = 0
for c in sel:
    k = " ".join(c["fen"].split()[:4])
    rec = cache.get(k)
    if rec is None and k.split()[3] != "-":
        rec = cache.get(" ".join(k.split()[:3] + ["-"]))
    if rec is None or rec.get("status") != 200:
        missing += 1
        continue
    data = rec["data"]
    mv = {m["uci"]: m["category"] for m in data["moves"]}
    # perspective self-check: root win <=> some move whose category (for the opponent) is a loss
    root = data["category"]
    some_win = any(v in ("loss", "blessed-loss") for v in mv.values())
    all_lose = all(v in ("win", "cursed-win") for v in mv.values())
    if (root in ("win", "cursed-win")) != some_win or (root in ("loss", "blessed-loss")) != all_lose:
        persp_bad += 1
    sq, stm, ep = parse(c["fen"])
    assert not passed(sq, True) or not passed(sq, False)
    for uci, child in pawn_moves(sq, stm, ep):
        assert uci in mv, (c["fen"], uci)
        if not (passed(child, True) and passed(child, False)):
            continue
        white = stm == "w"
        dm, do = dist(child, white), dist(child, not white)
        truth = MOVER[mv[uci]]
        pred = {"mover": "win", "opponent": "loss", "count": "loss" if do <= dm else "win"}
        npawn = sum(1 for (f, r), p in sq.items() if p in "Pp" and f <= 3)
        rows.append(dict(fen=c["fen"], treb=c["treb"], tier=c["tier"], comp=c["component"], uci=uci,
                         dm=dm, do=do, tb=truth, cat=mv[uci], pred=pred, npawn=npawn))

print(f"selected {len(sel)}, missing/non-200 {missing}, root/move perspective inconsistencies {persp_bad}")
print(f"{len(rows)} depth-1 race nodes; distinct (fen,uci): {len({(r['fen'], r['uci']) for r in rows})}")
print("tb result for mover:", dict(collections.Counter(r["tb"] for r in rows)))
for rule in ("count", "opponent", "mover"):
    print(f"  {rule:9s} {sum(r['pred'][rule] == r['tb'] for r in rows)}/{len(rows)}")
print("by trebuchet:", dict(collections.Counter(r["treb"] for r in rows)))
print("by tier:", dict(collections.Counter(r["tier"] for r in rows)))
print("parent component pawn counts:", dict(collections.Counter(r["npawn"] for r in rows)))
print("distinct parent components:", len({r["comp"] for r in rows}),
      "; distinct (component, move):", len({(r["comp"], r["uci"]) for r in rows}))
print("by d_mover-d_opp:")
by = collections.defaultdict(collections.Counter)
for r in rows:
    by[r["dm"] - r["do"]][r["tb"]] += 1
for k in sorted(by):
    print(f"  {k:+d}: {dict(by[k])}")
print("count misses:")
for r in rows:
    if r["pred"]["count"] != r["tb"]:
        print(f"  {r['fen']} {r['uci']} comp={r['comp']} dm={r['dm']} do={r['do']} tb={r['tb']} ({r['cat']})")
json.dump(rows, open(os.path.join(OUT, "indep_race_rows.json"), "w"), indent=1)
