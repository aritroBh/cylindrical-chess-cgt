"""Real-chess (explicit kings) diagnosis of the sides of the 34 rows where the exact real result differs from the
frozen-king result.  One kpsolve process at a time, nice 15, 1 thread, RSS-watchdogged (own PID only).
Usage: python3 -I realking.py CAP   -> realking_capCAP.json"""
import json, sys, subprocess, time, threading, collections
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms")
import pawngame as pg
ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
HERE = ROOT + "/research/v2_mechanisms/"
CAP = sys.argv[1]
THREADS = sys.argv[3] if len(sys.argv) > 3 else "1"
W_ = 7
G = pg.Game(2, 6, True, 3)


def run_kp(lines, tag):
    cmd = ["nice", "-n", "15", f"{ROOT}/kings/kpsolve", "--board", "cyl:7x6", "--ep", "on", "--promote", "Q", "--cap", CAP,
           "--threads", THREADS, "--moves"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    open(HERE + "logs/kpsolve.pid", "a").write(f"{p.pid} {tag} cap{CAP}\n")
    peak, tripped = [0], []

    def wd():
        while p.poll() is None:
            try:
                rss = int(subprocess.run(["ps", "-o", "rss=", "-p", str(p.pid)], capture_output=True, text=True).stdout.strip() or 0)
            except ValueError:
                rss = 0
            peak[0] = max(peak[0], rss)
            if rss > 3800 * 1024:
                tripped.append(rss); p.kill(); return   # our own child only
            time.sleep(2)
    threading.Thread(target=wd, daemon=True).start()
    t0 = time.time()
    out, err = p.communicate("\n".join(lines) + "\n")
    if tripped:
        raise MemoryError(f"{tag}: kpsolve over 3.8 GB")
    res = {}
    for line in out.splitlines():
        parts = [x.strip() for x in line.split("|")]
        a, b = parts[1].split()
        mv = {}
        if len(parts) >= 3:
            if parts[2].startswith("A: ") and len(parts) >= 4:
                pa = dict(t.rsplit(":", 1) for t in parts[2][3:].split()); pb = dict(t.rsplit(":", 1) for t in parts[3][3:].split())
                mv = {m: (pa[m] if pa[m] == pb.get(m) else "?") for m in pa}
            else:
                mv = dict(t.rsplit(":", 1) for t in parts[2].split())
        res[parts[0]] = (a, b, mv)
    return res, err.strip().splitlines()[-1] if err.strip() else "", peak[0] // 1024, round(time.time() - t0, 1)


def sqx(t): return "abcdefg".index(t[0]), int(t[1:])
def nmx(f, r): return "abcdefg"[f % W_] + str(r)


def apply(line, mv):
    toks = line.split()
    pieces, stm, ep = toks[:-2], toks[-2], toks[-1]
    pc, body = mv[0], mv[1:]
    promo = None
    if "=" in body: body, promo = body.split("=")
    frm, to = body[:2], body[2:]
    white = stm == "w"
    letter = pc if white else pc.lower()
    new, newep = [], "-"
    epcap = None
    if pc == "P" and frm[0] != to[0] and not any(t[1:] == to for t in pieces) and ep == to:
        epcap = to[0] + frm[1]    # e.p.: the captured pawn stands on (to file, from rank)
    for t in pieces:
        if t[1:] == to or (epcap and t[1:] == epcap):
            continue
        if t[0] == letter and t[1:] == frm:
            new.append((promo if white else promo.lower()) + to if promo else letter + to)
        else:
            new.append(t)
    if pc == "P" and frm[0] == to[0] and abs(int(to[1]) - int(frm[1])) == 2:
        newep = frm[0] + str((int(to[1]) + int(frm[1])) // 2)
    return " ".join(new) + (" b " if white else " w ") + newep


def kdist(a, b):
    (f1, r1), (f2, r2) = sqx(a), sqx(b)
    df = min((f1 - f2) % W_, (f2 - f1) % W_)
    return max(df, abs(r1 - r2))


def main():
    rows = [json.loads(l) for l in open(HERE + "mechanisms_34.jsonl")]
    roots = []
    for x in rows:
        for key, side in (("wtm", "w"), ("btm", "b")):
            if x["real"][key][0] != x["frozen"][key][0]:
                roots.append((x, key, side))
    base = {"w": "wtm", "b": "btm"}
    lines = []
    for x, key, side in roots:
        pos = G.parse(x["P"])
        lines.append(f"Pa3 pa4 Kg4 kb3 " + " ".join(["P" + pg.nm((f + 3, r)) for f, r in sorted(pos[0])] + ["p" + pg.nm((f + 3, r)) for f, r in sorted(pos[1])]) + f" {side} -")
    out = {"cap": CAP, "roots": []}
    res, log, peak, secs = run_kp(lines, "realking_roots")
    out["kpsolve_roots"] = dict(log=log, peak_rss_mb=peak, seconds=secs)
    print("roots", log, peak, secs, flush=True)
    kids = {}
    info = []
    for (x, key, side), line in zip(roots, lines):
        a, b, mv = res[line]
        pos = G.parse(x["P"])
        sidekey = "W" if side == "w" else "B"
        fz = G.fg_moves(pos, sidekey)   # frozen values of pawn moves
        me = "W" if side == "w" else "L"
        # frozen-winning pawn moves of the frozen winner
        d = dict(P=x["P"], side=side, real=(a, b), frozen=x["frozen"][key], moves=mv)
        d["best_real_moves"] = [m for m, v in mv.items() if v == a]
        d["pawn_moves_frozen"] = {l: v[0] for l, v in fz.items()}
        info.append(d)
        # children of the frozen-best pawn moves (those whose frozen value is the frozen result)
        for m, v in mv.items():
            if m[0] == "P":
                kids[apply(line, m)] = None
    # second layer: all replies after every pawn move of each root (cheap: few lines)
    res2, log2, peak2, secs2 = run_kp(list(kids), "realking_children")
    out["kpsolve_children"] = dict(log=log2, peak_rss_mb=peak2, seconds=secs2)
    print("children", log2, peak2, secs2, flush=True)
    for d, (x, key, side), line in zip(info, roots, lines):
        d["children"] = {}
        for m, v in d["moves"].items():
            if m[0] != "P": continue
            ch = apply(line, m)
            a2, b2, mv2 = res2[ch]
            d["children"][m] = dict(line=ch, value=(a2, b2), replies=mv2)
        out["roots"].append(d)
    json.dump(out, open(HERE + f"realking_cap{CAP}.json", "w"), indent=1)
    # human-readable digest
    for d in out["roots"]:
        print("\n==", d["P"], "mover", d["side"], "real", d["real"], "frozen", d["frozen"])
        print("  root moves:", d["moves"])
        for m, c in d["children"].items():
            print("  after", m, "value", c["value"], "replies", c["replies"])


if __name__ == "__main__":
    main()
