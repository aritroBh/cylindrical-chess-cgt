"""oS / oW of the 9 listed positions under all three race rules (indep.py only),
plus: are all 83 frontier states of the headline non-pairwise-safe?"""
import indep as I
from indep import Bd, parse, oS, oW, clear
for (n, m, wrap, ep, text, rule, cs, cw) in I.CASES:
    B = Bd(n, m, wrap, ep)
    w, k = parse(text)
    row = []
    for r in ("count", "mover", "opponent"):
        s, ww = oS(B, w, k, r), oW(B, w, k, r)
        clear()
        row.append(f"{r}: S={s} W={ww}{' DIFF' if s != ww else ''}")
    print(f"{n}x{m} {'cyl' if wrap else 'flat'} ep={'on' if ep else 'off'} {text} (listed rule {rule}) | " + " | ".join(row))
