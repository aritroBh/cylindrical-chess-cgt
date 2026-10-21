"""Sanity checks of wb + our parser on small positions with values known from the paper / report."""
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from driver import G, parse_value, job_line
HERE = os.path.dirname(os.path.abspath(__file__))

def run(files, wrap, white, black, gold, rule="count", aware=1, ep=1):
    gm = G()
    H = gm.export(gm.neg(parse_value(gm, gold))) if gold is not None else []
    row = {"white": white, "black": black, "board": {"files": files, "cylinder": wrap}}
    line = job_line(0, row, rule, aware, ep, 50_000_000, 0, H)
    out = subprocess.run([os.path.join(HERE, "wb")], input=line + "\n", capture_output=True, text=True).stdout
    res = [l.split() for l in out.splitlines()]
    wins = {s: any(x[0] in "MH" and x[1] == s and x[-1] == "1" for x in res) for s in "WB"}
    E = [x for x in res if x[0] == "E"][0]
    return ("P" if not wins["W"] and not wins["B"] else "N" if wins["W"] and wins["B"] else "L" if wins["W"] else "R"), E[1:]

cases = [
    (1, False, ["a2"], ["a4"], "*", "P"), (1, False, ["a2"], ["a4"], None, "N"),
    (1, False, ["a2"], ["a5"], "^", "P"), (1, False, ["a2"], ["a5"], None, "L"),
    (1, False, ["a2"], ["a5"], "0", "L"), (1, False, ["a2"], ["a5"], "*", "L"),
    (1, False, ["a2"], ["a6"], "^^*", "P"),
    (1, False, ["a2"], ["a3"], "0", "P"),
]
for files, wrap, w, b, gold, want in cases:
    got, E = run(files, wrap, w, b, gold)
    print(f"{'ok ' if got == want else 'BAD'} W {w} B {b} files={files} H=-({gold}) -> {got} want {want}  E={E}")
kf = (4, False, ["a2", "c2"], ["b7", "d7"])
for aware in (0, 1):
    for ep in (0, 1):
        for rule in ("count", "mover", "opponent"):
            r = {g: run(*kf, g, rule, aware, ep)[0] for g in ("*2", "0", "{2+-1 | -2+-1}")}
            print("KEY-FACT aware", aware, "ep", ep, rule, "P-test vs:", r, "alone:", run(*kf, None, rule, aware, ep))
