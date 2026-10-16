"""Extra checks with the independent model (indep.py).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/lemmas/L4.2-critical-races-reproduce/extra.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep as I

root = I.parse("W: a2 c2 / B: b7 d7")
mon, moff = I.Model(root, True), I.Model(root, False)
strip = lambda S: {(c[0], c[1], s) for c, s in S}
print("stripped ep-on race set == ep-off race set:", strip(mon.races) == strip(moff.races))
print("ep-on positions stripped == ep-off positions:", {(x[0], x[1]) for x in mon.positions} == {(x[0], x[1]) for x in moff.positions})
# count e.p. captures actually available anywhere in the e.p.-on tree
n_ep_moves = 0
usable_ep_in_race = 0
for x in mon.positions:
    if x[2]:
        owner = x[2][2]
        plain = (x[0], x[1], None)
        with_ep = I.gen(x, owner, True)
        without = I.gen(plain, owner, True)
        if with_ep - without:
            n_ep_moves += len(with_ep - without)
for c, s in mon.races:
    if c[2]:
        owner = c[2][2]
        if I.gen(c, owner, True) - I.gen((c[0], c[1], None), owner, True):
            usable_ep_in_race += 1
print("e.p. captures available at non-terminal nodes of the e.p.-on tree:", n_ep_moves)
print("race children whose ep right is actually usable:", usable_ep_in_race,
      "of", sum(1 for c, s in mon.races if c[2]))
# critical single flips under other baselines
for base_name, base in (("mover", lambda c, s: s), ("opponent", lambda c, s: I.other(s))):
    for m, tag in ((mon, "on"), (moff, "off")):
        bv = m.classify(lambda c, s: base(c, s))
        crit = []
        for c, s in sorted(m.races, key=lambda t: (I.show(t[0]), t[1])):
            def v(cc, ss, c=c, s=s):
                w = base(cc, ss)
                return I.other(w) if (cc, ss) == (c, s) else w
            val = m.classify(v)
            if val != bv:
                crit.append((I.show(c), s, val))
        print(f"baseline {base_name}, e.p. {tag}: base {bv}; single flips changing it: {len(crit)}", crit)
