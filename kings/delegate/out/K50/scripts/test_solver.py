"""K50 test (b): embed_check verdicts against kp_p --pmodel (P, real kings) and kpsolve --frozen on 6-rank boards.
A CERTIFIED verdict predicts the P result (the D-game winner); it must agree with kp_p. Run from the project root:
  python3 kings/delegate/out/K50/scripts/test_solver.py <group-id> <n_contexts> [--ctx] [--locked]
Needs kings/delegate/out/K50/kp_p and kpsolve (built from K7's kp_p.c and kings/kpsolve.c)."""
import json
import os
import random
import subprocess
import sys
import time
from collections import Counter

sys.path.insert(0, os.getcwd())
from kings.embed_check import Board, Checker, FILES, has_passer  # noqa: E402

GROUPS = {  # id: (board, group, F_Z or None, context files)
    "ZT": ("cyl:7x6", "Ka4 Pb3 kc3 pb4", None, "ef"),
    "K29a": ("cyl:7x6", "Kb3 Pa2 Pc2 kb1 pa3 pc3", "a,b,c", "ef"),
    "Z72": ("cyl:7x6", "Kc4 Pb5 kb6 pc5", None, "efg"),
    "T6": ("flat:8x6", "Kf4 Pg3 kh3 pg4", None, "abcd"),
    "K29c2": ("cyl:7x6", "Kb1 Pa2 Pb3 ka3 pb2 pc5", "a,b,c", "ef"),
}
OUT = "kings/delegate/out/K50/"


def locked(B, cfiles, H, n, seed):
    """n contexts built from 1 or 2 locked pairs (white pawn directly below a black pawn), plus at most one
    loose pawn, with no passer at the root."""
    rnd = random.Random(seed)
    seen, out = set(), []
    for _ in range(50 * n):
        if len(out) >= n:
            break
        w, b = [], []
        for _ in range(rnd.randint(1, 2)):
            f, r = rnd.choice(cfiles), rnd.randint(2, H - 2)
            w.append((f, r))
            b.append((f, r + 1))
        if rnd.random() < 0.5:
            (w if rnd.random() < 0.5 else b).append((rnd.choice(cfiles), rnd.randint(2, H - 1)))
        if len(set(w + b)) < len(w + b):
            continue
        key = (frozenset(w), frozenset(b))
        st = (frozenset((FILES.index(f), r) for f, r in w), frozenset((FILES.index(f), r) for f, r in b), None)
        if key in seen or has_passer(B, st, "W") or has_passer(B, st, "B"):
            continue
        seen.add(key)
        out.append(" ".join([f"P{f}{r}" for f, r in w] + [f"p{f}{r}" for f, r in b]))
    return out


def contexts(B, cfiles, H, n, seed):
    """n random contexts (1 to 4 pawns, at most 2 a side, ranks 2..H-1) with no passer at the root."""
    rnd = random.Random(seed)
    sqs = [(f, r) for f in cfiles for r in range(2, H)]
    seen, out = set(), []
    while len(out) < n:
        nw, nb = rnd.randint(0, 2), rnd.randint(0, 2)
        if nw + nb == 0:
            continue
        pick = rnd.sample(sqs, nw + nb)
        key = (frozenset(pick[:nw]), frozenset(pick[nw:]))
        if key in seen:
            continue
        seen.add(key)
        st = (frozenset((FILES.index(f), r) for f, r in key[0]), frozenset((FILES.index(f), r) for f, r in key[1]), None)
        if has_passer(B, st, "W") or has_passer(B, st, "B"):
            continue
        out.append(" ".join([f"P{f}{r}" for f, r in pick[:nw]] + [f"p{f}{r}" for f, r in pick[nw:]]))
    return out


def solve(binary, flags, board, lines):
    p = subprocess.run([OUT + binary, "--board", board] + flags, input="\n".join(lines) + "\n",
                       capture_output=True, text=True, timeout=600)
    res = {}
    for l in p.stdout.splitlines():
        if "|" in l:
            a, b = l.split("|")
            res[a.strip()] = b.split()
    return res


def main():
    gid, n = sys.argv[1], int(sys.argv[2])
    ctx = "--ctx" in sys.argv
    board, grp, fz, cf = GROUPS[gid]
    W, H = map(int, board.split(":")[1].split("x"))
    B = Board(W, H, board.startswith("cyl"))
    gen = locked if "--locked" in sys.argv else contexts
    poss = [f"{grp} {c} {s} -" for c in gen(B, cf, H, n, 50) for s in "wb"]
    pres = solve("kp_p", ["--pmodel"], board, poss)
    fres = solve("kpsolve", ["--frozen"], board, poss)
    chk = Checker(B, 8, 300000, ctx, 30)
    tally = Counter()
    bad = []
    t0 = time.process_time()
    for p in poss:
        r = chk.run(p, fz)
        stm = p.split()[-2]
        pv = pres.get(p, ["?", "?"])
        fv = fres.get(p, ["?", "?"])
        pred = None
        if "winner" in r.get("D_result", {}):
            pred = "W" if r["D_result"]["winner"] == "White" else "L"
        route = "full" if r.get("proves", "").startswith("Theorem") else ("sharp" if r["verdict"] == "CERTIFIED" else "-")
        exact = pv[0] == pv[1]
        agree = exact and pred == pv[0]
        tally[(r["verdict"], route, "P=D" if agree else "P!=D")] += 1
        if r["verdict"] == "CERTIFIED" and not agree:
            bad.append((p, pred, pv))
        for k in ("V1", "V2", "V3"):
            tally[(k, r[k]["verdict"])] += 1
        print(json.dumps({"pos": p, "verdict": r["verdict"], "route": route, "D": pred, "P": pv, "F": fv,
                          "V1": r["V1"]["verdict"], "V2": r["V2"]["verdict"], "V3": r["V3"]["verdict"]}))
    print("SUMMARY", gid, board, "ctx" if ctx else "strict", gen.__name__, "positions", len(poss),
          "checker cpu", round(time.process_time() - t0, 1))
    for k, v in sorted(tally.items()):
        print(" ", v, *k)
    print("CERTIFIED disagreeing with kp_p:", len(bad), bad[:5])


if __name__ == "__main__":
    main()
