"""Independent re-check of claim C1 (static eval sign vs tablebase root, by CGT class).

Written from scratch by the C1-refute verifier. Does NOT import any engine/ code.
* FENs: only the "fen" and "id" fields of engine/suite/results.json are used (the material).
* Tablebase root: read directly from raw Lichess JSON files on disk (realchess/cache and
  engine/suite/tbcache), matched on the first four FEN fields. No network.
* Component: extracted here from the FEN (pawns on files a-d); the trebuchet on f-h is checked.
* CGT value: cylcgt (the project's read-only library, not worker code), flat 4x8 board, ep on,
  under all three race rules; classes by canonical-form tests (number: G == mean(G);
  nimber: G == *k), not by string parsing.
* Stockfish: own UCI driver, `eval` command, own parser. Lc0: own driver, `go nodes 1`.

  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python \
     verify/engines/C1-refute/static_eval_c1/indep_eval.py [--lc0]
"""
import glob, json, os, subprocess, sys, time
from fractions import Fraction
from collections import defaultdict, Counter

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
OUT = os.path.join(ROOT, "verify/engines/C1-refute/static_eval_c1")
SF = os.path.join(ROOT, "engine/vendor/Stockfish/src/stockfish")
LC0 = "/opt/homebrew/bin/lc0"
sys.path.insert(0, ROOT)
from cylcgt import cgt, pawns  # noqa: E402

rows = json.load(open(os.path.join(ROOT, "engine/suite/results.json")))

# ---------- raw tablebase cache ----------
tb = {}
for d in ("realchess/cache", "engine/suite/tbcache"):
    for p in glob.glob(os.path.join(ROOT, d, "*", "*.json")):
        try:
            rec = json.load(open(p))
        except Exception:
            continue
        if rec.get("status") != 200 or not rec.get("data"):
            continue
        k = " ".join(rec["fen"].split()[:4])
        cat = rec["data"].get("category")
        if k in tb and tb[k] != cat:
            print("CACHE CONFLICT", k, tb[k], cat)
        tb[k] = cat

# ---------- FEN parsing ----------
def board_of(fen):
    b = {}
    for i, row in enumerate(fen.split()[0].split("/")):
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                b["abcdefgh"[f] + str(8 - i)] = ch
                f += 1
    return b

def component_of(fen):
    b = board_of(fen)
    w = sorted(s for s, c in b.items() if s[0] in "abcd" and c == "P")
    bl = sorted(s for s, c in b.items() if s[0] in "abcd" and c == "p")
    other = [(s, c) for s, c in b.items() if s[0] in "abcde" and c not in "Pp"]
    e_file = [(s, c) for s, c in b.items() if s[0] == "e"]
    return f"W: {' '.join(w)} / B: {' '.join(bl)}", other, e_file

BOARD = pawns.Board(4, 8, False, True)

def eq(a, b):
    return cgt.le(a, b) and cgt.le(b, a)

def cgt_info(comp):
    vals = {}
    for rule in ("count", "mover", "opponent"):
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        vals[rule] = pawns.value(BOARD, pawns.Pos.parse(comp))
    pawns.RACE_RULE = "count"
    pawns._value.cache_clear()
    g = vals["count"]
    o = cgt.outcome(g)
    m = cgt.mean(g)
    is_num = eq(g, cgt.number(Fraction(m)))
    nim = next((k for k in range(1, 8) if eq(g, cgt.nimber(k))), None)
    big = is_num and abs(Fraction(m)) >= pawns.BIG
    rs_value = not (eq(vals["count"], vals["mover"]) and eq(vals["count"], vals["opponent"]))
    rs_outcome = len({cgt.outcome(v) for v in vals.values()}) > 1
    return dict(o=o, is_num=is_num and not big, big=big, nim=nim, show=cgt.show(g),
                rs_value=rs_value, rs_outcome=rs_outcome)

# ---------- Stockfish eval ----------
def sf_evals(fens):
    p = subprocess.Popen([SF], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    p.stdin.write("uci\nisready\n"); p.stdin.flush()
    for line in p.stdout:
        if line.strip() == "readyok":
            break
    res = []
    for fen in fens:
        p.stdin.write(f"position fen {fen}\neval\nisready\n"); p.stdin.flush()
        nn = fin = None
        for line in p.stdout:
            s = line.strip()
            if s == "readyok":
                break
            if s.startswith("NNUE evaluation") and "(white side)" in s:
                nn = float(s.split()[2])
            if s.startswith("Final evaluation"):
                t = s.split()[2]
                fin = None if t.startswith("none") else float(t)
        res.append((nn, fin))
    p.stdin.write("quit\n"); p.stdin.flush(); p.wait()
    return res

# ---------- Lc0 one node ----------
def lc0_evals(fens):
    p = subprocess.Popen([LC0], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                         text=True, bufsize=1)
    p.stdin.write("uci\nisready\n"); p.stdin.flush()
    for line in p.stdout:
        if line.strip() == "readyok":
            break
    res = []
    for fen in fens:
        p.stdin.write(f"ucinewgame\nposition fen {fen}\ngo nodes 1\n"); p.stdin.flush()
        cp = nodes = best = None
        for line in p.stdout:
            t = line.split()
            if t and t[0] == "info" and "score" in t:
                i = t.index("score")
                cp = int(t[i + 2]) if t[i + 1] == "cp" else (100000 if int(t[i + 2]) > 0 else -100000)
                if "nodes" in t:
                    nodes = int(t[t.index("nodes") + 1])
            if t and t[0] == "bestmove":
                best = t[1]
                break
        res.append((cp, nodes, best))  # cp is side-to-move POV (UCI)
    p.stdin.write("quit\n"); p.stdin.flush(); p.wait()
    return res

def main():
    data = []
    for r in rows:
        fen = r["fen"]
        k = " ".join(fen.split()[:4])
        comp, other, efile = component_of(fen)
        info = cgt_info(comp)
        data.append(dict(id=r["id"], fen=fen, stm=fen.split()[1], comp=comp, comp_worker=r["component"],
                         other_ad=other, efile=efile, tb=tb.get(k), **info))
    print("missing TB:", sum(d["tb"] is None for d in data),
          "| component mismatches vs worker field:", sum(d["comp"] != d["comp_worker"] for d in data),
          "| non-pawn men on a-e:", sum(bool(d["other_ad"]) for d in data),
          "| men on e-file:", sum(bool(d["efile"]) for d in data))
    sfr = sf_evals([d["fen"] for d in data])
    for d, (nn, fin) in zip(data, sfr):
        d["sf_nnue_white"], d["sf_final_white"] = nn, fin
    if "--lc0" in sys.argv:
        lcr = lc0_evals([d["fen"] for d in data])
        for d, (cp, nodes, best) in zip(data, lcr):
            d["lc0_cp_stm"], d["lc0_nodes"], d["lc0_best"] = cp, nodes, best
    json.dump(data, open(os.path.join(OUT, "indep_eval.json"), "w"), indent=0)
    report(data)

def report(data):
    has_lc0 = "lc0_cp_stm" in data[0]
    def sf_stm(d, key="sf_final_white"):
        v = d[key]
        return v if d["stm"] == "w" else -v
    print("TB root categories:", Counter(d["tb"] for d in data))
    print("SF final == 0.00:", sum(d["sf_final_white"] == 0 for d in data),
          "| SF final None:", sum(d["sf_final_white"] is None for d in data))
    if has_lc0:
        print("Lc0 nodes reported:", Counter(d["lc0_nodes"] for d in data), "| cp == 0:",
              sum(d["lc0_cp_stm"] == 0 for d in data))
    wl = [d for d in data if d["tb"] in ("win", "loss")]
    groups = {
        "all win/loss": wl,
        "N (count rule)": [d for d in wl if d["o"] == "N"],
        "nimber (any)": [d for d in wl if d["nim"]],
        "nimber, race-insensitive value": [d for d in wl if d["nim"] and not d["rs_value"]],
        "number (non-BIG), any": [d for d in wl if d["is_num"]],
        "number, race-insensitive value": [d for d in wl if d["is_num"] and not d["rs_value"]],
        "N non-nimber": [d for d in wl if d["o"] == "N" and not d["nim"]],
    }
    print("| group | n | distinct comps | TB win | SF final right | SF raw NNUE right |" + (" Lc0 right |" if has_lc0 else ""))
    for g, ds in groups.items():
        ok = sum((sf_stm(d) > 0) == (d["tb"] == "win") for d in ds)
        okn = sum((sf_stm(d, "sf_nnue_white") > 0) == (d["tb"] == "win") for d in ds)
        line = f"| {g} | {len(ds)} | {len({d['comp'] for d in ds})} | {sum(d['tb']=='win' for d in ds)} | {ok} | {okn} |"
        if has_lc0:
            okl = sum((d["lc0_cp_stm"] > 0) == (d["tb"] == "win") for d in ds)
            line += f" {okl} |"
        print(line)
    print("nimber values:", Counter(d["nim"] for d in wl if d["nim"]))
    print("number values:", Counter(d["show"] for d in wl if d["is_num"]))

if __name__ == "__main__":
    if "--report" in sys.argv:
        report(json.load(open(os.path.join(OUT, "indep_eval.json"))))
    else:
        main()
