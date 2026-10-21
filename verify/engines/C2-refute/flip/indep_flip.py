#!/usr/bin/env python3
"""Adversarial re-computation of claim C2 (side-to-move flip test), independent of engine/ code.

Does NOT import anything from engine/ or realchess/. Uses:
  * engine/suite/results.json only as DATA (FEN, component, stm, tablebase root);
  * crosscheck/minimax.py (Codex's independent whole-position solver) for the CGT outcome class,
    and, for comparison only, cylcgt (the project's model) -- both under race rule "count",
    4-file flat 8-rank board, e.p. on;
  * my own UCI drivers for Stockfish 19 `eval` and Lc0 `go nodes 1`;
  * my own legality check for the twins.

Run from the project root:
    PYTHONPATH=. .venv/bin/python verify/engines/C2-refute/flip/indep_flip.py
Writes verify/engines/C2-refute/flip/indep_rows.json and prints the tables.
"""
import json
import statistics
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from crosscheck import minimax as X  # noqa: E402  (independent solver)
from cylcgt import cgt, pawns  # noqa: E402  (project model, comparison only)

SF = ROOT / "engine/vendor/Stockfish/src/stockfish"
LC0 = "/opt/homebrew/bin/lc0"


# ---------------------------------------------------------------- FEN + legality (own code)
def board_of(fen):
    rows = fen.split()[0].split("/")
    b = {}
    for i, row in enumerate(rows):
        r = 8 - i
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                b[(f, r)] = ch
                f += 1
        assert f == 8, fen
    return b


def attacked_by(b, sq, color):
    """Is square sq attacked by `color` ('w'/'b')? Only kings and pawns exist here."""
    f, r = sq
    for (g, s), p in b.items():
        if color == "w" and p == "P" and s + 1 == r and abs(g - f) == 1:
            return True
        if color == "b" and p == "p" and s - 1 == r and abs(g - f) == 1:
            return True
        if (p == "K" and color == "w") or (p == "k" and color == "b"):
            if max(abs(g - f), abs(s - r)) == 1:
                return True
    return False


def legal_twin(fen):
    b = board_of(fen)
    stm = fen.split()[1]
    if set(b.values()) - set("KkPp"):
        return False, "other pieces"
    if list(b.values()).count("K") != 1 or list(b.values()).count("k") != 1:
        return False, "kings"
    if any(p in "Pp" and r in (1, 8) for (f, r), p in b.items()):
        return False, "pawn on back rank"
    wk = next(s for s, p in b.items() if p == "K")
    bk = next(s for s, p in b.items() if p == "k")
    # side NOT to move must not be in check
    if stm == "w" and attacked_by(b, bk, "w"):
        return False, "black (not to move) in check"
    if stm == "b" and attacked_by(b, wk, "b"):
        return False, "white (not to move) in check"
    return True, ""


def twin_of(fen):
    p = fen.split()
    return f"{p[0]} {'b' if p[1] == 'w' else 'w'} - - 0 1"


# ---------------------------------------------------------------- outcome classes
XB = X.Board(files=4, ranks=8, wrap=False, ep=True)
PB = pawns.Board(4, 8, False, True)


def o_crosscheck(comp):
    return X.outcome_class(XB, X.parse_position(comp))


def o_cylcgt(comp):
    pawns.RACE_RULE = "count"
    return cgt.outcome(pawns.value(PB, pawns.Pos.parse(comp)))


# ---------------------------------------------------------------- engines (own drivers)
def sf_evals(fens):
    cmds = ["uci", "isready"]
    for fen in fens:
        cmds += [f"position fen {fen}", "eval", "isready"]
    cmds.append("quit")
    out = subprocess.run([str(SF)], input="\n".join(cmds) + "\n", capture_output=True, text=True,
                         timeout=900).stdout
    blocks = out.split("readyok")
    # blocks[0] = before first readyok (uci header); blocks[i] (i>=1) = output of i-th eval
    res = []
    for blk in blocks[1:1 + len(fens)]:
        fin = [ln for ln in blk.splitlines() if ln.startswith("Final evaluation")]
        nn = [ln for ln in blk.splitlines() if ln.startswith("NNUE evaluation") and "white side" in ln]
        assert len(fin) == 1 and len(nn) == 1, blk[-400:]
        res.append((float(nn[0].split()[2]), float(fin[0].split()[2])))
    assert len(res) == len(fens)
    return res


def lc0_scores(fens):
    p = subprocess.Popen([LC0], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                         text=True, bufsize=1)

    def send(s):
        p.stdin.write(s + "\n")
        p.stdin.flush()

    def until(prefix):
        lines = []
        while True:
            ln = p.stdout.readline()
            if not ln:
                raise RuntimeError("lc0 died")
            ln = ln.rstrip("\n")
            lines.append(ln)
            if ln.startswith(prefix):
                return lines

    send("uci")
    until("uciok")
    send("isready")
    until("readyok")
    res = []
    for fen in fens:
        send("ucinewgame")
        send("isready")
        until("readyok")
        send(f"position fen {fen}")
        send("go nodes 1")
        lines = until("bestmove")
        score = None
        for ln in lines:
            t = ln.split()
            if t and t[0] == "info" and "score" in t:
                i = t.index("score")
                kind, v = t[i + 1], int(t[i + 2])
                score = v if kind == "cp" else (100000 if v > 0 else -100000)
        best = lines[-1].split()[1]
        white = score if fen.split()[1] == "w" else -score
        res.append((white, best))
    send("quit")
    p.wait(timeout=30)
    return res


def main():
    rows = json.loads((ROOT / "engine/suite/results.json").read_text())
    se = {r["id"]: r for r in json.loads((ROOT / "engine/experiments/results/static_eval.json").read_text())["rows"]}
    lc = {r["id"]: r for r in json.loads((ROOT / "engine/experiments/results/lc0_value_n1.json").read_text())["rows"]}
    out = []
    for r in rows:
        tw = twin_of(r["fen"])
        ok, why = legal_twin(tw)
        out.append({"id": r["id"], "fen": r["fen"], "twin": tw, "stm": r["stm"], "component": r["component"],
                    "treb": r["treb"], "tb_root": r["tb_root"], "twin_legal": ok, "illegal_why": why,
                    "o_x": o_crosscheck(r["component"]), "o_c": o_cylcgt(r["component"]),
                    "o_worker": se[r["id"]]["o"], "value_count": r["value"]["count"]})
    print("twins legal (own check):", sum(o["twin_legal"] for o in out), "of", len(out),
          Counter(o["illegal_why"] for o in out if not o["twin_legal"]))
    print("o: crosscheck vs worker agree", sum(o["o_x"] == o["o_worker"] for o in out),
          "; cylcgt vs worker agree", sum(o["o_c"] == o["o_worker"] for o in out))
    for o in out:
        if o["o_x"] != o["o_worker"]:
            print("   o disagreement", o["id"], o["component"], "crosscheck", o["o_x"], "worker", o["o_worker"])
    fens = []
    for o in out:
        fens += [o["fen"], o["twin"]]
    t0 = time.time()
    sfv = sf_evals(fens)
    print(f"stockfish evals done in {time.time() - t0:.1f}s")
    t0 = time.time()
    lcv = lc0_scores(fens)
    print(f"lc0 nodes-1 done in {time.time() - t0:.1f}s")
    sf_mis = lc_mis = lc_sign_mis = 0
    for i, o in enumerate(out):
        (o["sf_nnue"], o["sf_final"]), (o["sf_twin_nnue"], o["sf_twin_final"]) = sfv[2 * i], sfv[2 * i + 1]
        (o["lc_white"], o["lc_best"]), (o["lc_twin_white"], o["lc_twin_best"]) = lcv[2 * i], lcv[2 * i + 1]
        w = se[o["id"]]
        L = lc[o["id"]]
        sf_mis += (o["sf_final"], o["sf_twin_final"]) != (w["final"], w["twin_final"])
        lc_mis += (o["lc_white"], o["lc_twin_white"]) != (L["lc0_orig_white_cp"], L["lc0_twin_white_cp"])
        lc_sign_mis += ((o["lc_white"] > 0, o["lc_twin_white"] > 0) !=
                        (L["lc0_orig_white_cp"] > 0, L["lc0_twin_white_cp"] > 0))
        # delta = eval(White to move) - eval(Black to move), White POV
        if o["stm"] == "W":
            o["d_sf"] = o["sf_final"] - o["sf_twin_final"]
            o["d_sf_nnue"] = o["sf_nnue"] - o["sf_twin_nnue"]
            o["d_lc"] = o["lc_white"] - o["lc_twin_white"]
            o["d_lc_worker"] = L["lc0_orig_white_cp"] - L["lc0_twin_white_cp"]
            o["d_sf_worker"] = w["final"] - w["twin_final"]
        else:
            o["d_sf"] = o["sf_twin_final"] - o["sf_final"]
            o["d_sf_nnue"] = o["sf_twin_nnue"] - o["sf_nnue"]
            o["d_lc"] = o["lc_twin_white"] - o["lc_white"]
            o["d_lc_worker"] = L["lc0_twin_white_cp"] - L["lc0_orig_white_cp"]
            o["d_sf_worker"] = w["twin_final"] - w["final"]
    print(f"rerun vs worker JSON: SF final mismatching pairs {sf_mis}; Lc0 cp mismatching pairs {lc_mis}; "
          f"Lc0 sign-pattern mismatches {lc_sign_mis}")
    (HERE / "indep_rows.json").write_text(json.dumps(out, indent=0))
    report(out)


def report(out, okey="o_x"):
    print(f"\n## Flip test (class from {okey}); right = delta>0 for N, delta<0 for P (strict); "
          "worker's rule counts delta==0 as right for P")
    for src, key in (("SF final (rerun)", "d_sf"), ("SF final (worker JSON)", "d_sf_worker"),
                     ("SF raw NNUE (rerun)", "d_sf_nnue"),
                     ("Lc0 n1 (rerun)", "d_lc"), ("Lc0 n1 (worker JSON)", "d_lc_worker")):
        line = [src]
        for o_ in "NPLR":
            ds = [o[key] for o in out if o[okey] == o_ and o["twin_legal"]]
            pos = sum(d > 0 for d in ds)
            neg = sum(d < 0 for d in ds)
            zero = len(ds) - pos - neg
            line.append(f"{o_}: n={len(ds)} >0:{pos} <0:{neg} =0:{zero} med={statistics.median(ds):+.2f}")
        print(" | ".join(line))


if __name__ == "__main__":
    main()
