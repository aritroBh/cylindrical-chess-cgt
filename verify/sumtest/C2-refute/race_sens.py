"""Which race resolutions does G = *2 depend on?  (uses only indep.py)

For count / e.p. off and count / e.p. on textbook (global scope):
  * list every distinct race state reached (W, B, ep, last mover) with its
    count-rule winner and the mover-rule winner;
  * flip each race state's winner on its own and re-test G + *2 = P.
Also: tie-goes-to-mover variant of count.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep
from indep import Cfg, make_solver, outcome, parse, refs, LET

R = refs()
W0, B0 = parse("W: a2 c2 / B: b7 d7")
orig_resolve = indep.resolve

def fmt(W, B):
    s = lambda S: " ".join(sorted(f"{LET[f]}{r}" for f, r in S))
    return f"W: {s(W)} / B: {s(B)}"

def run(cfg, override=None):
    def res(cfg_, W, B, ep, lm):
        r = orig_resolve(cfg_, W, B, ep, lm)
        if override is not None and (W, B, ep, lm) in override:
            return override[(W, B, ep, lm)]
        return r
    indep.resolve = res
    try:
        win, _ = make_solver(cfg)
        return {n: outcome(win, W0, B0, R[n]) for n in ("0", "*", "*2", "*3")}
    finally:
        indep.resolve = orig_resolve

for ep in (False, True):
    cfg = Cfg(ep=ep, race="count")
    indep.RACES.clear()
    base = run(cfg)
    races = sorted(indep.RACES, key=str)
    print(f"\n=== count, ep={ep}: base {base}; {len(races)} distinct race states")
    agree = 0
    crit = []
    for key in races:
        W, B, e, lm = key
        cw = orig_resolve(cfg, W, B, e, lm)
        if cw == lm:
            agree += 1
        flipped = "B" if cw == "W" else "W"
        o = run(cfg, {key: flipped})
        if o["*2"] != "P":
            crit.append((key, cw, o))
    print(f"count winner == mover in {agree}/{len(races)} race states")
    print(f"race states whose single flip destroys G+*2=P: {len(crit)}")
    for (W, B, e, lm), cw, o in crit:
        print(f"   {fmt(W, B)} ep={e} last_mover={lm} count_winner={cw} -> after flip {o}")
    # tie -> mover variant
    def tie_mover(cfg_, W, B, e, lm):
        wl, bl = indep.passers(cfg_, W, B, e)
        r = orig_resolve(cfg_, W, B, e, lm)
        if wl and bl:
            dw, db = indep.dist(cfg_, "W", wl, W, B), indep.dist(cfg_, "B", bl, W, B)
            if dw == db:
                return lm
        return r
    indep.resolve = tie_mover
    win, _ = make_solver(cfg)
    print("count with ties to the MOVER:", {n: outcome(win, W0, B0, R[n]) for n in ("0", "*", "*2", "*3")})
    indep.resolve = orig_resolve
