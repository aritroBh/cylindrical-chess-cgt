"""ChessSums generator: sums of certified pawn components with exact CGT truth.

    cd /Users/aritro/Downloads/Research/Chessendgames
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.generate --seed 20261015

Deterministic for a given --seed (and given sizes). Writes bench/data/:
    components.jsonl                the certified component library
    {split}.jsonl                   train / val / test / test_heldout
    {split}_8file.jsonl             the rows of {split} that sit on an 8-file board
    manifest.json                   sizes, filter statistics, distributions, sha256

Ground truth per instance (all from cylcgt):
    value      canonical form of the sum of the component values
    outcome    L / R / N / P of that value
    winning_moves[side]   a move wins iff the position after it has outcome in
                          {L,P} (White moved) or {R,P} (Black moved)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from collections import Counter, defaultdict
from pathlib import Path

from cylcgt import cgt

from . import board as bd
from . import cgtfmt
from .components import BIG, build, public

DATA = Path(__file__).resolve().parent / "data"
MAX_FILES = 26          # file letters a..z
OUTCOMES = ("L", "R", "N", "P")

SPLITS = [
    # name, size, {k: share}, pool, require_heldout
    ("train", 20000, {1: 0.15, 2: 0.35, 3: 0.50}, "train", False),
    ("val", 2000, {1: 0.15, 2: 0.35, 3: 0.50}, "train", False),
    ("test", 2000, {4: 1 / 3, 5: 1 / 3, 6: 1 / 3}, "train", False),
    ("test_heldout", 2000, {1: 0.2, 2: 0.4, 3: 0.4}, "heldout", True),
]
FIT8_SHARE_TEST_K4 = 0.5  # half of the k=4 test rows are drawn so that they fit 8 files


def needed_width(widths, wrap):
    k = len(widths)
    return sum(widths) + (k if wrap else k - 1)


class Sampler:
    """Pick a value class with probability ~ sqrt(class size), then a component."""

    def __init__(self, comps):
        by_val = defaultdict(list)
        for c in comps:
            by_val[c["value"]].append(c)
        self.vals = sorted(by_val)
        self.by_val = by_val
        self.w = [math.sqrt(len(by_val[v])) for v in self.vals]

    def draw(self, rng, max_width=4):
        for _ in range(1000):
            v = rng.choices(self.vals, weights=self.w)[0]
            cs = [c for c in self.by_val[v] if c["width"] <= max_width]
            if cs:
                return rng.choice(cs)
        raise RuntimeError("no component fits")


def layout(rng, comps, wrap, fit8):
    """Place components on a board. Returns (W, [(comp, start_file)]) or None."""
    widths = [c["width"] for c in comps]
    need = needed_width(widths, wrap)
    if need <= 8:
        W = 8
    else:
        if fit8:
            return None
        W = need + rng.randint(0, 2)
    if W > MAX_FILES:
        return None
    order = list(comps)
    rng.shuffle(order)
    k = len(order)
    extra = W - need
    if wrap:
        gaps = [1] * k
        for _ in range(extra):
            gaps[rng.randrange(k)] += 1
        start = rng.randrange(W)
        placed, f = [], start
        for c, g in zip(order, gaps):
            placed.append((c, f % W))
            f += c["width"] + g
    else:
        slots = [0] + [1] * (k - 1) + [0]
        for _ in range(extra):
            slots[rng.randrange(k + 1)] += 1
        placed, f = [], slots[0]
        for i, c in enumerate(order):
            placed.append((c, f))
            f += c["width"] + slots[i + 1]
        assert f + 0 <= W
    return W, placed


def shift_sq(s, start, W):
    return ((s[0] + start) % W, s[1])


def shift_move(name, start, W):
    sep = "x" if "x" in name else "-"
    a, b = name.split(sep)
    fa, fb = bd.parse_sq(a), bd.parse_sq(b)
    return f"{bd.sqname(shift_sq(fa, start, W))}{sep}{bd.sqname(shift_sq(fb, start, W))}"


def instance(placed, W, wrap):
    """Compute the full ground-truth record for components placed on a board."""
    games = [c["_game"] for c, _ in placed]
    G = cgt.total(games)
    k = len(games)
    # others[i] = sum of all components except i
    pre = [cgt.ZERO]
    for g in games:
        pre.append(cgt.add(pre[-1], g))
    suf = [cgt.ZERO]
    for g in reversed(games):
        suf.append(cgt.add(suf[-1], g))
    suf = suf[::-1]
    others = [cgt.add(pre[i], suf[i + 1]) for i in range(k)]

    white, black, comps_out = set(), set(), []
    legal = {"W": [], "B": []}
    winning = {"W": [], "B": []}
    for i, (c, start) in enumerate(placed):
        p = c["_pos"]
        cw = {shift_sq(s, start, W) for s in p.white}
        cb = {shift_sq(s, start, W) for s in p.black}
        white |= cw
        black |= cb
        files = [bd.FILES[(start + j) % W] for j in range(c["width"])]
        comps_out.append({"comp_id": c["comp_id"], "files": "".join(files),
                          "position": bd.pos_text(cw, cb), "value": c["value"]})
        for m in c["moves"]:
            side, child = m["side"], m["_game"]
            name = shift_move(m["move"], start, W)
            legal[side].append(name)
            if child.num is not None and abs(child.num) >= BIG // 2:
                wins = (child.num > 0) == (side == "W")
            else:
                h = cgt.add(child, others[i])
                wins = cgt.le(cgt.ZERO, h) if side == "W" else cgt.le(h, cgt.ZERO)
            if wins:
                winning[side].append(name)
    white, black = frozenset(white), frozenset(black)
    geo = bd.Geometry(W, wrap)
    # the whole-board move generator must agree with the per-component move lists
    for side in "WB":
        whole = sorted(n for n, *_ in bd.gen_moves(geo, white, black, side))
        assert whole == sorted(legal[side]), (bd.pos_text(white, black), side)
        legal[side] = whole
        winning[side] = sorted(winning[side])
    comps_out.sort(key=lambda d: bd.FILES.index(d["files"][0]))
    t = cgt.temperature(G)
    return {
        "k": k,
        "board": {"files": W, "ranks": 8, "cylinder": wrap},
        "position": bd.pos_text(white, black),
        "placement": bd.placement(geo, white, black),
        "white": sorted(map(bd.sqname, white)),
        "black": sorted(map(bd.sqname, black)),
        "components": comps_out,
        "value": cgtfmt.fmt(G),
        "value_ascii": cgtfmt.fmt(G, ascii=True),
        "kind": cgtfmt.kind(G),
        "outcome": cgt.outcome(G),
        "mean": cgtfmt.fnum(cgt.mean(G)),
        "temperature": None if t is None else cgtfmt.fnum(t),
        "legal_moves": legal,
        "winning_moves": winning,
        "fits8": W == 8,
    }, G


def gen_split(name, size, kshare, pool_kind, need_held, comps, rng, seen, log):
    train_pool = [c for c in comps if c["heldout"] is None]
    held_pool = [c for c in comps if c["heldout"] is not None]
    s_train = Sampler(train_pool)
    s_held = Sampler(held_pool) if held_pool else None
    ks = sorted(kshare)
    counts = {k: round(size * kshare[k]) for k in ks}
    counts[ks[-1]] += size - sum(counts.values())
    rows = []
    shortfall = Counter()
    for k in ks:
        n_k = counts[k]
        quota = {o: n_k // 4 + (1 if j < n_k % 4 else 0) for j, o in enumerate(OUTCOMES)}
        got = Counter()
        fit8_target = round(n_k * FIT8_SHARE_TEST_K4) if (name == "test" and k == 4) else 0
        fit8_got = 0
        attempts, max_attempts = 0, 400 * n_k
        while sum(got.values()) < n_k:
            attempts += 1
            relax = attempts > max_attempts
            want_fit8 = fit8_got < fit8_target
            maxw = 2 if want_fit8 else 4
            if need_held:
                held_slots = [rng.random() < 0.5 for _ in range(k)]
                if not any(held_slots):
                    held_slots[rng.randrange(k)] = True
                cs = [s_held.draw(rng, maxw) if h else s_train.draw(rng, maxw) for h in held_slots]
            else:
                cs = [s_train.draw(rng, maxw) for _ in range(k)]
            wrap = rng.random() < 0.5
            lay = layout(rng, cs, wrap, fit8=want_fit8)
            if lay is None:
                continue
            W, placed = lay
            G = cgt.total(c["_game"] for c in cs)
            o = cgt.outcome(G)
            if got[o] >= quota[o] and not relax:
                continue
            rec, _ = instance(placed, W, wrap)
            key = (W, wrap, rec["position"])
            if key in seen:
                continue
            seen.add(key)
            got[o] += 1
            if rec["fits8"] and want_fit8:
                fit8_got += 1
            held = sorted({c["heldout"] for c in cs if c["heldout"]})
            rec["heldout"] = held
            rows.append(rec)
        for o in OUTCOMES:
            if got[o] < quota[o]:
                shortfall[f"k={k} {o}"] += quota[o] - got[o]
        log(f"  {name} k={k}: {n_k} rows, outcomes {dict(sorted(got.items()))}, attempts {attempts}")
    rng.shuffle(rows)
    for i, r in enumerate(rows):
        r["id"] = f"{name}-{i:05d}"
        r["split"] = name
    return rows, shortfall


ORDER = ["id", "split", "k", "board", "position", "placement", "white", "black", "components",
         "value", "value_ascii", "kind", "outcome", "mean", "temperature", "legal_moves",
         "winning_moves", "fits8", "heldout"]


def dump(path: Path, rows):
    with path.open("w") as f:
        for r in rows:
            f.write(json.dumps({k: r[k] for k in ORDER}, ensure_ascii=False) + "\n")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=20261015)
    ap.add_argument("--scale", type=float, default=1.0, help="multiply every split size (e.g. 0.05 for a smoke test)")
    ap.add_argument("--out", type=Path, default=DATA)
    a = ap.parse_args(argv)
    t0 = time.time()
    a.out.mkdir(parents=True, exist_ok=True)
    print("building component library ...", flush=True)
    comps, cstats = build(verbose=True)
    with (a.out / "components.jsonl").open("w") as f:
        for c in comps:
            f.write(json.dumps(public(c), ensure_ascii=False) + "\n")
    seen = set()
    manifest = {"seed": a.seed, "scale": a.scale,
                "component_filter": {k: v for k, v in cstats.items() if k != "seconds"}, "splits": {}}
    for si, (name, size, kshare, pool, need_held) in enumerate(SPLITS):
        rng = random.Random(a.seed * 1000 + si)
        size = max(4, round(size * a.scale))
        rows, short = gen_split(name, size, kshare, pool, need_held, comps, rng, seen, print)
        p = a.out / f"{name}.jsonl"
        dump(p, rows)
        rows8 = [r for r in rows if r["fits8"]]
        p8 = a.out / f"{name}_8file.jsonl"
        dump(p8, rows8)
        manifest["splits"][name] = {
            "rows": len(rows), "rows_8file": len(rows8),
            "k": dict(sorted(Counter(r["k"] for r in rows).items())),
            "outcome": dict(sorted(Counter(r["outcome"] for r in rows).items())),
            "kind": dict(sorted(Counter(r["kind"] for r in rows).items())),
            "cylinder": sum(r["board"]["cylinder"] for r in rows),
            "board_files": dict(sorted(Counter(r["board"]["files"] for r in rows).items())),
            "rows_with_winning_move": {s: sum(1 for r in rows if r["winning_moves"][s]) for s in "WB"},
            "max_value_len": max(len(r["value"]) for r in rows),
            "outcome_quota_shortfall": dict(short),
            "sha256": sha(p), "sha256_8file": sha(p8),
        }
        print(f"{name}: {len(rows)} rows ({len(rows8)} on 8 files)  [{time.time() - t0:.0f}s]", flush=True)
    manifest["components_sha256"] = sha(a.out / "components.jsonl")
    (a.out / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    print(f"done in {time.time() - t0:.0f}s; manifest at {a.out / 'manifest.json'}")


if __name__ == "__main__":
    main()
