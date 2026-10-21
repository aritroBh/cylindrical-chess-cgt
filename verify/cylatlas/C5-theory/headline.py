"""C5-theory: recompute the C5 headline values under all 6 race/e.p. settings, report which
passed-pawn test the imported cylcgt uses, check BIG-invariance of the *2, and check the
translations of the 4-file *2 onto wider flat strips and cylinders (cut lemma).

  textbook passed test (main checkout):
    cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/cylatlas/C5-theory/headline.py
  e.p.-aware passed test (adopted convention; ep-aware-passed copy in the session scratchpad):
    PYTHONPATH=<scratchpad>/ep-wt:. .venv/bin/python verify/cylatlas/C5-theory/headline.py
"""
from cylcgt import cgt, pawns

print("cylcgt.pawns:", pawns.__file__)
print("PASSED_RESPECTS_EP =", getattr(pawns, "PASSED_RESPECTS_EP", "absent -> textbook test"))

POS = [
    ("flat", 4, "W: a2 c2 / B: b7 d7"),
    ("cyl", 4, "W: a2 c2 / B: b7 d7"),
    ("cyl", 3, "W: a2 b3 / B: a5 c5"),
    ("flat", 3, "W: a2 b3 / B: a5 c5"),
]


def val(kind, n, text, rule, ep):
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    pawns.race_hits.clear()
    g = pawns.value(pawns.Board(n, 8, kind == "cyl", ep), pawns.Pos.parse(text))
    return g, len(pawns.race_hits)


for kind, n, text in POS:
    print(f"\n{kind} {n} {text}")
    for ep in (True, False):
        for rule in ("count", "mover", "opponent"):
            g, races = val(kind, n, text, rule, ep)
            print(f"   {rule:8s} ep={'on ' if ep else 'off'}  {cgt.show(g):40s} outcome={cgt.outcome(g)} races={races}")

# translations of the 4-file component (files a-d), other files empty
print("\nTranslations of W a2 c2 / B b7 d7 (count, e.p. on):")
for kind in ("flat", "cyl"):
    for n in range(4, 10):
        g, _ = val(kind, n, "W: a2 c2 / B: b7 d7", "count", True)
        print(f"   {kind} {n}: {cgt.show(g)}")
for n, text in [(8, "W: e2 g2 / B: f7 h7"), (8, "W: d2 f2 / B: e7 g7"), (8, "W: b7 d7 / B: a2 c2")]:
    pass
# flat 8 with the group shifted (and colour-swapped/mirrored variant = negative)
for text in ("W: e2 g2 / B: f7 h7", "W: c2 e2 / B: d7 f7", "W: b2 d2 / B: a7 c7"):
    g, _ = val("flat", 8, text, "count", True)
    print(f"   flat 8 {text}: {cgt.show(g)}")

# BIG invariance of the flat *2 (and of the cylinder value)
print("\nBIG invariance (count, e.p. on):")
orig = pawns.BIG
for big in (32, 64, 256, 1024, 4096):
    pawns.BIG = big
    cgt.BIG_DISPLAY = big // 2
    out = []
    for kind, n, text in POS[:3]:
        g, _ = val(kind, n, text, "count", True)
        out.append(f"{kind}{n}: {cgt.show(g)}")
    gO, _ = val("cyl", 3, "W: a2 b3 / B: a5 c5", "opponent", True)
    out.append(f"cyl3/opponent: {cgt.show(gO)}")
    print(f"   BIG={big}: " + " ; ".join(out))
pawns.BIG = orig
cgt.BIG_DISPLAY = orig // 2
