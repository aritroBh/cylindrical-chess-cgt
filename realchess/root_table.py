"""Root move tables: real-chess result of every legal move at the embedded
root (White and Black to move) against the cylcgt value of the resulting
component, under whichever cylcgt is imported (run once per convention).
Real results come from results/<tag>_root_children.json, made by the resolve
stage on both roots and all their children (see --print-resolve-command).

    PYTHONPATH=. .venv/bin/python -m realchess.root_table [--component "W: a2 c2 / B: b7 d7"]
"""
import argparse
import json
import os
import shlex

from cylcgt import cgt, pawns
from cylcgt.pawns import Pos

from . import component as C
from . import movegen as mg
from .solve_candidate import Model, RESULTS, tag_of


def root_fens(comp):
    return {stm: mg.normal_fen(C.embed(comp, stm.upper())) for stm in "wb"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", default="W: a2 c2 / B: b7 d7")
    ap.add_argument("--print-resolve-command", action="store_true")
    a = ap.parse_args()
    comp = Pos.parse(a.component)
    tag = tag_of(comp)
    src = os.path.join(RESULTS, f"{tag}_root_children.json")
    if a.print_resolve_command:
        fens = []
        for f in root_fens(comp).values():
            fens.append(f)
            pos = mg.parse_fen(f)
            fens += [mg.normal_fen(mg.make(pos, m)) for m in mg.legal_moves(pos)]
        print("PYTHONPATH=. .venv/bin/python -m realchess.solve_candidate resolve --offline --ext 4 "
              f"--component {shlex.quote(a.component)} --out {os.path.relpath(src)} "
              + " ".join("--fen " + shlex.quote(f) for f in fens))
        return
    real = {p["fen"]: p["result_for_side_to_move"] for p in json.load(open(src))["positions"]}
    conv = "e.p.-aware" if getattr(pawns, "PASSED_RESPECTS_EP", False) else "textbook"
    model = Model()
    out = {"component": a.component, "convention": conv, "cylcgt_file": pawns.__file__, "roots": {}}
    for stm, fen in root_fens(comp).items():
        pos = mg.parse_fen(fen)
        rows = []
        for m in mg.legal_moves(pos):
            ch = mg.make(pos, m)
            f = mg.normal_fen(ch)
            r = real.get(f, "unresolved")
            mover = {"win": "loss", "loss": "win", "draw": "draw"}.get(r, "unresolved")
            row = {"move": m.uci(), "real_result_for_mover": mover}
            if pos.board[m.frm].upper() == "K":
                row["model"] = "king move (outside the pawn model; the model assumes it loses)"
            else:
                p = model.comp(ch)
                if C.is_terminal(model.board, p):
                    row["model"] = "terminal"
                else:
                    vals = {rule: model.value(Pos(p.white, p.black, p.ep), rule) for rule in ("count", "mover", "opponent")}
                    row["model_child_value"] = {k: cgt.show(v) for k, v in vals.items()}
                    # mover wins (in isolation) iff the child is a second-player... i.e. the opponent, to move, loses
                    side = "B" if stm == "w" else "W"
                    row["model_mover_wins_in_isolation"] = {
                        k: (cgt.outcome(v) == "P" or cgt.outcome(v) == ("L" if side == "B" else "R"))
                        for k, v in vals.items()}
            rows.append(row)
        out["roots"][stm] = {"fen": mg.normal_fen(pos), "real_result_for_side_to_move": real.get(mg.normal_fen(pos)),
                             "moves": rows}
    name = f"{tag}_root_table_" + ("epaware" if conv == "e.p.-aware" else "textbook") + ".json"
    with open(os.path.join(RESULTS, name), "w") as fh:
        json.dump(out, fh, indent=1)
    for stm, r in out["roots"].items():
        print(stm, r["real_result_for_side_to_move"])
        for row in r["moves"]:
            print("   ", row["move"], "real:", row["real_result_for_mover"], "| model:",
                  row.get("model_child_value", row.get("model")), row.get("model_mover_wins_in_isolation", ""))


if __name__ == "__main__":
    main()
