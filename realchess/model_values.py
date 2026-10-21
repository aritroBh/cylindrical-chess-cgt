"""Model-level (cylcgt) values of an a-d component under both passed-pawn
conventions, every RACE_RULE, and e.p. on/off (4-file flat board, 8 ranks).

  textbook   : the main checkout's cylcgt (a pawn is passed as soon as no enemy
               pawn can stop it, even if it can still be taken en passant);
  e.p.-aware : the ep-aware-passed worktree's cylcgt, PASSED_RESPECTS_EP = True
               (a pawn that can still be taken e.p. is not passed).

The two cylcgt versions share a module name, so each runs in its own
subprocess. The e.p.-aware worktree is also run with PASSED_RESPECTS_EP = False
as a control: it must reproduce the textbook numbers exactly.

    PYTHONPATH=. .venv/bin/python -m realchess.model_values --component "W: a2 c2 / B: b7 d7"

A component is "benchmark-eligible" only if all 12 values (2 conventions x
3 race rules x e.p. on/off) are the same game.
Set REALCHESS_EPAWARE_PATH to override the worktree location.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EPAWARE_DEFAULT = ("/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/"
                   "57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt")
RULES = ("count", "mover", "opponent")


def _inner(component: str, flag: str | None):
    """Run inside one cylcgt version; print JSON."""
    from cylcgt import cgt, pawns
    from cylcgt.pawns import Board, Pos
    if flag is not None:
        if not hasattr(pawns, "PASSED_RESPECTS_EP"):
            raise SystemExit("this cylcgt has no PASSED_RESPECTS_EP flag")
        pawns.PASSED_RESPECTS_EP = (flag == "1")
    p = Pos.parse(component)
    out = {"cylcgt_file": pawns.__file__,
           "PASSED_RESPECTS_EP": getattr(pawns, "PASSED_RESPECTS_EP", "absent (textbook)"),
           "values": {}}
    for ep in (True, False):
        b = Board(4, 8, False, ep)
        for rule in RULES:
            pawns.RACE_RULE = rule
            pawns._value.cache_clear()
            pawns.race_hits.clear()
            g = pawns.value(b, p)
            key = f"ep={'on' if ep else 'off'},rule={rule}"
            out["values"][key] = {"value": cgt.show(g), "outcome": cgt.outcome(g),
                                  "race_hits": len(pawns.race_hits)}
            try:
                out["values"][key]["mean"] = str(cgt.mean(g))
                t = cgt.temperature(g)
                out["values"][key]["temperature"] = "number" if t is None else str(t)
            except Exception as e:  # pragma: no cover
                out["values"][key]["thermo_error"] = repr(e)
    print(json.dumps(out))


def run(component: str, epaware_path: str | None = None):
    ep_path = epaware_path or os.environ.get("REALCHESS_EPAWARE_PATH", EPAWARE_DEFAULT)
    py = sys.executable

    def sub(cylcgt_root, flag):
        # `python -m` puts the working directory FIRST on sys.path (before
        # PYTHONPATH), so the subprocess runs inside the tree whose cylcgt it
        # must import, and the loaded file is checked afterwards.
        env = dict(os.environ, PYTHONPATH=cylcgt_root + os.pathsep + ROOT)
        cmd = [py, "-m", "realchess.model_values", "--inner", "--component", component]
        if flag is not None:
            cmd += ["--flag", flag]
        r = subprocess.run(cmd, env=env, cwd=cylcgt_root, capture_output=True, text=True, check=True)
        out = json.loads(r.stdout.strip().splitlines()[-1])
        want = os.path.realpath(os.path.join(cylcgt_root, "cylcgt"))
        if not os.path.realpath(out["cylcgt_file"]).startswith(want):
            raise RuntimeError(f"loaded {out['cylcgt_file']}, expected cylcgt under {want}")
        return out

    res = {"component": component, "board": "4 files (a-d), 8 ranks, flat",
           "textbook": sub(ROOT, None)}
    if os.path.isdir(os.path.join(ep_path, "cylcgt")):
        res["ep_aware"] = sub(ep_path, "1")
        res["control_epaware_worktree_flag_off"] = sub(ep_path, "0")
        res["control_matches_textbook"] = (res["control_epaware_worktree_flag_off"]["values"]
                                           == res["textbook"]["values"])
    else:
        res["ep_aware"] = None
        res["note"] = f"e.p.-aware worktree not found at {ep_path}"
    vals = set()
    for conv in ("textbook", "ep_aware"):
        if res.get(conv):
            vals |= {v["value"] for v in res[conv]["values"].values()}
    res["distinct_values"] = sorted(vals)
    res["benchmark_eligible"] = bool(res.get("ep_aware")) and len(vals) == 1
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", default="W: a2 c2 / B: b7 d7")
    ap.add_argument("--inner", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--flag", default=None, help=argparse.SUPPRESS)
    ap.add_argument("--epaware-path", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.inner:
        _inner(a.component, a.flag)
        return
    res = run(a.component, a.epaware_path)
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
