"""Independent re-derivation of claim C2 from the RAW Lichess cache files.

Uses only: engine/suite/selection*.json (positions), engine/suite/candidates.json
(CGT values, only for the tame / race-sensitive grouping), engine/suite/tbcache/*/*.json
(raw Lichess bodies). Does NOT use results.json, tb.MOVER_RESULT or realchess.movegen.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      .venv/bin/python verify/engines/C2-reproduce/indep_c2.py
"""
import collections
import glob
import json
import os

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
S = os.path.join(ROOT, "engine/suite")

# ---- raw cache, keyed by the FEN stored inside each file
cache = {}
for p in glob.glob(os.path.join(S, "tbcache/*/*.json")):
    rec = json.load(open(p))
    cache[rec["fen"]] = rec
print("raw cache files:", len(cache))

sel = json.load(open(os.path.join(S, "selection.json"))) + json.load(open(os.path.join(S, "selection_ext.json")))
print("selected positions:", len(sel), "distinct FENs:", len({c["fen"] for c in sel}))
cands = {(r["pos"], r["stm"]): r for r in json.load(open(os.path.join(S, "candidates.json")))}

FLIP = {"win": "loss", "loss": "win", "draw": "draw", "cursed-win": "blessed-loss",
        "blessed-loss": "cursed-win"}


def parse(fen):
    board, stm = fen.split()[0], fen.split()[1]
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
    return sq, stm


def name(s):
    return "abcdefgh"[s[0]] + str(s[1])


def my_king_moves(sq, stm):
    """Legal king moves in a K+P-only position (no other piece types present)."""
    me_k, op_k, me_p, op_p = ("K", "k", "P", "p") if stm == "w" else ("k", "K", "p", "P")
    ks = next(s for s, c in sq.items() if c == me_k)
    oks = next(s for s, c in sq.items() if c == op_k)
    pdir = -1 if stm == "w" else 1  # direction the OPPONENT pawns capture towards (from their view)
    out = []
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == dr == 0:
                continue
            t = (ks[0] + df, ks[1] + dr)
            if not (0 <= t[0] < 8 and 1 <= t[1] <= 8):
                continue
            if sq.get(t) in (me_k, me_p):
                continue
            if max(abs(t[0] - oks[0]), abs(t[1] - oks[1])) <= 1:
                continue
            # attacked by an opponent pawn? opponent pawn at (t.f+-1, t.r - pdir) ... compute:
            # white pawn at (f,r) attacks (f+-1, r+1); black pawn at (f,r) attacks (f+-1, r-1)
            att = False
            for g in (-1, 1):
                if stm == "w":  # black pawns attack downward: pawn at (t.f+g, t.r+1)
                    src = (t[0] + g, t[1] + 1)
                else:
                    src = (t[0] + g, t[1] - 1)
                if sq.get(src) == op_p:
                    att = True
            if att:
                continue
            # a captured pawn defended by the opponent king was handled above (king adjacency);
            # defended by another opponent pawn is handled by the pawn-attack test above.
            out.append(name(ks) + name(t))
    return ks, set(out)


def tame(v):
    return "W" not in v


def race_sensitive(rec):
    sets = {r: tuple(sorted(m[0] for m in rec["rules"][r]["moves"] if m[4])) for r in ("count", "mover", "opponent")}
    return len(set(sets.values())) > 1


groups = collections.defaultdict(list)
mism = 0
rows = []
for c in sel:
    rec = cache.get(c["fen"])
    assert rec and rec["status"] == 200, c["fen"]
    sq, stm = parse(c["fen"])
    ks, mykm = my_king_moves(sq, stm)
    moves = rec["data"]["moves"]
    lkm = {m["uci"]: FLIP[m["category"]] for m in moves if m["uci"][:2] == name(ks)}
    sanK = {m["uci"] for m in moves if m["san"].startswith("K")}
    if set(lkm) != mykm or sanK != set(lkm):
        mism += 1
        print("KING-MOVE SET MISMATCH", c["id"], c["fen"], sorted(lkm), sorted(mykm), sorted(sanK))
    cr = cands[(c["component"], c["stm"])]
    t, rs = tame(cr["rules"]["count"]["value"]), race_sensitive(cr)
    grp = ("tame" if t else "big") + ("-rs" if rs else "") + "-" + c["treb"][0]
    groups[grp].append((c, lkm, rec))
print("king-move set mismatches vs my generator / SAN:", mism)

for g in sorted(groups):
    km = collections.Counter(v for _, lkm, _ in groups[g] for v in lkm.values())
    print(f"{g:12s} n={len(groups[g]):3d} king-move results (for mover): {dict(km)} total={sum(km.values())}")

# ---- details for the two C2 groups
for g in ("tame-A", "tame-B"):
    print(f"\n== {g}: non-losing king moves")
    stm_c = collections.Counter(c["stm"] for c, _, _ in groups[g])
    tiers = collections.Counter(c["tier"].split("-")[0] for c, _, _ in groups[g])
    trebs = collections.Counter(c["treb"] for c, _, _ in groups[g])
    print("  stm:", dict(stm_c), "tiers:", dict(tiers), "trebs:", dict(sorted(trebs.items())))
    nonlose_pos = 0
    for c, lkm, rec in groups[g]:
        bad = {u: v for u, v in lkm.items() if v != "loss"}
        if bad:
            nonlose_pos += 1
            print(f"  {c['id']} {c['tier'][:2]} {c['treb']} {c['stm']} {c['component']:24s} root={rec['data']['category']:5s} {bad}")
    print("  positions with a non-losing king move:", nonlose_pos, "/", len(groups[g]))
