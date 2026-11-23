"""K50 referee harness. Compares every CERTIFIED verdict and every CERTIFIED clause of kings/embed_check.py
(strict and --ctx) with kp_p --pmodel --moves (P with real kings), using an independent pawn-game reference (ref.py).
Run from the project root:
  python3 kings/delegate/out/K50/verify/harness.py <shard> <nshards> <n_ctx_per_job> <seed> [outfile]
Checks (C1..C5 in VERIFY.md):
  C1 verdict CERTIFIED at X: kp_p exact and equal to the predicted winner (the D-winner); program D == ref D.
  C2 full form (Theorem 1.14(i)) at X: P(Y) = refD(Y) at sampled chess-reachable Y (context moves only).
  C3 V3 certified for side s: at X and the Y with s to move, every Z-move of s is a P-loss for s (kp_p --moves).
  C4 V2 passer/race clause certified: at X and every Y, every context move reaching a terminal leads to a P-win
     of the terminal's beneficiary (whole-board credit).
  C5 V1b certified for side s: at X and the Y with s to move, s has a legal move.
"""
import json
import os
import random
import subprocess
import sys
import time

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ref  # noqa: E402
from kings.embed_check import Board, Checker  # noqa: E402

KP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kp_p")

K29 = {"K29c1": "Kb3 Pa2 Pc2 kb1 pa3 pc3", "K29c2": "Kb1 Pa2 Pb3 ka3 pb2 pc5",
       "K29c3": "Kb3 Pa2 Pa4 ka5 pa3 pb4", "K29c4": "Kb3 Pc2 Pa4 ka5 pc3 pb4"}
JOBS = []  # (board, fz, group-id, group, context files)
for bd, cf in (("cyl:6x6", "e"), ("cyl:7x6", "ef"), ("cyl:8x6", "efg"), ("flat:7x6", "efg"), ("flat:8x6", "efgh")):
    JOBS.append((bd, None, "ZT", "Ka4 Pb3 kc3 pb4", cf))
    for k, g in K29.items():
        JOBS.append((bd, "a,b,c", k, g, cf))
for bd, cf in (("cyl:7x6", "efg"), ("cyl:8x6", "efgh"), ("flat:7x6", "efg"), ("flat:8x6", "efgh")):
    JOBS.append((bd, None, "Z72", "Kc4 Pb5 kb6 pc5", cf))
JOBS += [("cyl:7x6", None, "FigA", "Kg4 Pa3 kb3 pa4", "de"), ("cyl:8x6", None, "FigA", "Kh4 Pa3 kb3 pa4", "def"),
         ("flat:8x6", None, "FigB", "Kf4 Pg3 kh3 pg4", "abcd"), ("flat:7x6", None, "FigB", "Ke4 Pf3 kg3 pf4", "abc"),
         ("flat:8x6", None, "FigBm", "Kc4 Pb3 ka3 pb4", "efgh")]


def geo(bd):
    k, s = bd.split(":")
    W, H = map(int, s.split("x"))
    return W, H, k == "cyl"


def gen_contexts(G, cf, n, rnd, stm):
    """Contexts as (w, b, ep) with ep usable by stm, no passer at the root (reference test)."""
    H = G.H
    files = [ref.FILES.index(c) for c in cf]
    out, seen, tries = [], set(), 0
    while len(out) < n and tries < 200 * n:
        tries += 1
        kind = rnd.random()
        w, b, ep = set(), set(), None
        if kind < 0.3 and len(files) >= 2:  # e.p. right at the root for stm
            f = rnd.choice(files)
            g = ref.Geo(G.W, H, G.wrap).nb(f, rnd.choice((-1, 1)))
            if g is None or g not in files:
                continue
            if stm == "w":  # black just played f(H-1)-f(H-3)
                b.add((f, H - 3)); w.add((g, H - 3)); ep = ((f, H - 2), (f, H - 3))
            else:
                w.add((f, 4)); b.add((g, 4)); ep = ((f, 3), (f, 4))
        nx = rnd.randint(0, 4 if kind < 0.3 else 5)
        sqs = [(f, r) for f in files for r in range(2, H)]
        for _ in range(nx):
            s = rnd.choice(sqs)
            if rnd.random() < 0.35:  # bias to start ranks
                s = (s[0], 2 if rnd.random() < 0.5 else H - 1)
            if s in w or s in b:
                continue
            if ep and s in (ep[0], (ep[0][0], H - 1 if stm == "w" else 2)):
                continue
            (w if rnd.random() < 0.5 else b).add(s)
        if not w and not b:
            continue
        if len(w) > 3 or len(b) > 3:
            continue
        w, b = frozenset(w), frozenset(b)
        if any(ref.is_passed(G, w, b, ep, "W", p) for p in w) or any(ref.is_passed(G, w, b, ep, "B", p) for p in b):
            continue
        key = (w, b, ep)
        if key in seen:
            continue
        seen.add(key)
        out.append(key)
    return out


def postext(group, w, b, stm, ep):
    toks = [group] + ["P" + ref.name(p) for p in sorted(w)] + ["p" + ref.name(p) for p in sorted(b)]
    return " ".join(toks) + f" {stm} " + (ref.name(ep[0]) if ep else "-")


def in_check_any(G, group, w, b):
    """True if either king is attacked by a pawn (reference test, used to skip illegal / in-check roots)."""
    pcs = {ref.sq(t[1:]): t[0] for t in group.split()}
    wk = [s for s, c in pcs.items() if c == "K"][0]
    bk = [s for s, c in pcs.items() if c == "k"][0]
    wp = {s for s, c in pcs.items() if c == "P"} | set(w)
    bp = {s for s, c in pcs.items() if c == "p"} | set(b)
    a = any((G.nb(wk[0], d), wk[1] + 1) in bp for d in (-1, 1) if G.nb(wk[0], d) is not None)
    c = any((G.nb(bk[0], d), bk[1] - 1) in wp for d in (-1, 1) if G.nb(bk[0], d) is not None)
    return a or c


def reach(G, w, b, ep, stm, nmax, rnd, depth=4):
    """Chess-reachable Y (context moves only) before the first decisive event, depth <= 4 plies; sampled."""
    out = []
    front = [(w, b, ep, stm)]
    seen = {(w, b, ep, stm)}
    for _ in range(depth):
        nxt = []
        for (cw, cb, cep, s) in front:
            for nw, nb_, nep in ref.children(G, cw, cb, cep, "W" if s == "w" else "B"):
                if ref.credit(G, nw, nb_, nep, "W" if s == "w" else "B") is not None:
                    continue
                k = (nw, nb_, nep, "b" if s == "w" else "w")
                if k not in seen:
                    seen.add(k)
                    nxt.append(k)
        front = nxt
        out += nxt
    rnd.shuffle(out)
    return out[:nmax]


def kp_batch(board, lines):
    p = subprocess.run([KP, "--board", board, "--pmodel", "--moves"], input="\n".join(lines) + "\n",
                       capture_output=True, text=True, timeout=7200)
    res = {}
    for l in p.stdout.splitlines():
        parts = l.split("|")
        if len(parts) >= 2:
            mv = {}
            if len(parts) >= 3:
                for t in parts[2].split():
                    m, v = t.rsplit(":", 1)
                    mv[m] = v
            res[parts[0].strip()] = (parts[1].split(), mv)
    return res


def parse_mv(m, H):
    pc = m[0]
    i = 1
    a = m[i]; i += 1
    j = i
    while m[j].isdigit():
        j += 1
    fr = (ref.FILES.index(a), int(m[i:j]))
    a2 = m[j]; k = j + 1
    l = k
    while l < len(m) and m[l].isdigit():
        l += 1
    to = (ref.FILES.index(a2), int(m[k:l]))
    return pc, fr, to


def apply_ctx(G, w, b, ep, side, fr, to):
    mine, theirs = (set(w), set(b)) if side == "W" else (set(b), set(w))
    mine.discard(fr); mine.add(to)
    nep = None
    if to in theirs:
        theirs.discard(to)
    elif ep and to == ep[0] and fr[0] != to[0]:
        theirs.discard(ep[1])
    if abs(to[1] - fr[1]) == 2:
        nep = ((fr[0], (fr[1] + to[1]) // 2), to)
    if side == "W":
        return frozenset(mine), frozenset(theirs), nep
    return frozenset(theirs), frozenset(mine), nep


def main():
    shard, nsh, nctx, seed = map(int, sys.argv[1:5])
    ctxfrac = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
    outf = open(sys.argv[5], "w")
    rnd = random.Random(seed * 1000 + shard)
    alljobs = json.load(open(sys.argv[7])) if len(sys.argv) > 7 else JOBS
    jobs = [j for i, j in enumerate(alljobs) if i % nsh == shard]
    for bd, fz, gid, group, cf in jobs:
        W, H, wrap = geo(bd)
        G = ref.Geo(W, H, wrap)
        B = Board(W, H, wrap)
        FZ = None
        X = []
        for stm in "wb":
            for (w, b, ep) in gen_contexts(G, cf, nctx, rnd, stm):
                if in_check_any(G, group, w, b):
                    continue
                X.append((w, b, ep, stm))
        t0 = time.process_time()
        recs = []
        CH = {m: Checker(B, 8, 300000, m == "ctx", 30) for m in ("strict", "ctx")}
        for (w, b, ep, stm) in X:
            txt = postext(group, w, b, stm, ep)
            rec = {"board": bd, "gid": gid, "pos": txt}
            runctx = rnd.random() < ctxfrac
            for mode in (("strict", "ctx") if runctx else ("strict",)):
                try:
                    r = CH[mode].run(txt, fz)
                except Exception as e:  # noqa: BLE001  (a crash of the program is recorded, not a verdict)
                    rec[mode] = {"verdict": "CRASH", "err": repr(e)}
                    continue
                if FZ is None and r["separation"].get("F_Z"):
                    FZ = {ref.FILES.index(c) for c in r["separation"]["F_Z"]}
                d = {"verdict": r["verdict"], "proves": r.get("proves", "")[:30],
                     "D": r.get("D_result", {}).get("winner")}
                if r["separation"]["verdict"] == "PASS" and isinstance(r["V1"], dict) and "V1b" in r["V1"]:
                    d["V1b"] = {s: r["V1"]["V1b"][s]["verdict"] for s in ("white", "black")}
                    d["V3"] = {s: r["V3"][s]["verdict"] for s in ("white", "black")}
                    d["V2p"] = r["V2"]["passer_and_race_terminals"]["verdict"]
                    d["E"] = r["V1"]["E"]["verdict"]
                rec[mode] = d
            recs.append((rec, w, b, ep, stm))
        # reference D and reachable Y
        q = set()
        for rec, w, b, ep, stm in recs:
            q.add(rec["pos"])
            try:
                rec["refD"] = "White" if ref.dgame(G, w, b, ep, "W" if stm == "w" else "B") == (stm == "w") else "Black"
            except RuntimeError:
                rec["refD"] = None
            need = any(m in rec and rec[m].get("verdict") == "CERTIFIED" or "CERTIFIED" in json.dumps(rec[m].get("V3", {}))
                       or rec[m].get("V2p") == "CERTIFIED" for m in ("strict", "ctx") if m in rec)
            rec["Y"] = []
            if need:
                for (yw, yb, yep, ys) in reach(G, w, b, ep, stm, 25, rnd):
                    t = postext(group, yw, yb, ys, yep)
                    rec["Y"].append((t, yw, yb, yep, ys))
                    q.add(t)
        kp = kp_batch(bd, sorted(q))
        for rec, w, b, ep, stm in recs:
            row = {k: v for k, v in rec.items() if k != "Y"}
            row["P"] = kp.get(rec["pos"], (["?", "?"], {}))[0]
            viol = []
            nodes = [(rec["pos"], w, b, ep, stm, True)] + [(t, yw, yb, yep, ys, False) for t, yw, yb, yep, ys in rec["Y"]]
            for mode in ("strict", "ctx"):
                if mode not in rec:
                    continue
                d = rec[mode]
                pr = d.get("D")
                if d["verdict"] == "CERTIFIED":
                    P = row["P"]
                    want = "W" if pr == "White" else "L"
                    if not (P[0] == P[1] == want):
                        viol.append(f"C1 {mode}: predicted {pr}, P {P}")
                    if rec.get("refD") and rec["refD"] != pr:
                        viol.append(f"C1 {mode}: program D {pr} != ref D {rec['refD']}")
                    if d["proves"].startswith("Theorem"):
                        for t, yw, yb, yep, ys, isroot in nodes[1:]:
                            P = kp.get(t, (["?", "?"], {}))[0]
                            rd = ref.dgame(G, yw, yb, yep, "W" if ys == "w" else "B") == (ys == "w")
                            want = "W" if rd else "L"
                            if not (P[0] == P[1] == want):
                                viol.append(f"C2 {mode}: Y {t}: refD {want} P {P}")
                if "V3" not in d:
                    continue
                for t, yw, yb, yep, ys, isroot in nodes:
                    res, mv = kp.get(t, (["?", "?"], {}))
                    side = "white" if ys == "w" else "black"
                    loss = "L" if ys == "w" else "W"
                    win = "W" if ys == "w" else "L"
                    if d["V1b"][side] == "CERTIFIED" and not mv:
                        viol.append(f"C5 {mode}: {t}: no legal move")
                    for m, v in mv.items():
                        pc, fr, to = parse_mv(m, H)
                        zmove = pc in "Kk" or fr[0] in FZ
                        if zmove and d["V3"][side] == "CERTIFIED" and v != loss:
                            viol.append(f"C3 {mode}: {t}: Z-move {m} -> {v}")
                        if not zmove and d["V2p"] == "CERTIFIED":
                            nw, nb_, nep = apply_ctx(G, yw, yb, yep, "W" if ys == "w" else "B", fr, to)
                            c = ref.credit(G, nw, nb_, nep, "W" if ys == "w" else "B")
                            if c is not None:
                                want = "W" if c == "W" else "L"
                                if v != want:
                                    viol.append(f"C4 {mode}: {t}: {m} terminal credited {c} -> P {v}")
            row["nY"] = len(rec["Y"])
            row["viol"] = viol
            outf.write(json.dumps(row) + "\n")
        outf.flush()
        print(bd, gid, len(recs), "positions", round(time.process_time() - t0, 1), "cpu-s", flush=True)


if __name__ == "__main__":
    main()
