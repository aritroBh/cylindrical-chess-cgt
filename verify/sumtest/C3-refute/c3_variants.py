"""C3 refute lens: is the non-*2 verdict robust to how e.p.-pending races are scored?

Imports only the verifier's own c3_canon.py (same directory).
Variants of the passer test after a double step that leaves an e.p. capture pending:
  aware   : the claim's convention: the e.p.-capturable pawn is not passed; resolve the rest now.
  defer   : no resolution at all while an e.p. capture is pending; the next move in G decides.
  defer_v : defer only when the e.p.-capturable pawn is textbook-passed; otherwise textbook.
  plain   : textbook test (cylcgt's convention).
Run:  .venv/bin/python -I verify/sumtest/C3-refute/c3_variants.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c3_canon as C

POS = "W: a2 c2 / B: b7 d7"


class V(C.Pawns):
    def __init__(self, *a, variant="aware", **k):
        super().__init__(*a, **k)
        self.variant = variant
        self.overlap = set()

    def resolve(self, st, mover_white):
        ep = st[2]
        if ep:
            cap_white = ep[2] == "W"
            vic_plain = self.is_passed(ep[1], not cap_white, st[0] if cap_white else st[1])
            cap_pass = bool(self.passers(st, cap_white, aware=False))
            if vic_plain and cap_pass:
                self.overlap.add(st)
            if self.variant == "defer" or (self.variant == "defer_v" and vic_plain):
                return st
        return super().resolve(st, mover_white)


for files, wrap in ((4, False), (8, True)):
    for race in ("count", "mover", "opponent"):
        for variant in ("plain", "aware", "defer", "defer_v"):
            m = V(files, wrap, ep=True, aware=(variant == "aware"), race=race, variant=variant)
            g = m.parse(POS)
            val, memo = m.value(g)
            vec = "".join(C.outcome(C.add(val, x)) for _, x in C.REF)
            print(f"{files}{'cyl' if wrap else 'flat'} {race:8s} {variant:8s} value={C.show(val):22s} "
                  f"G+*2={C.outcome(C.add(val, C.STAR2))} vec={vec} "
                  f"overlap(victim plain-passed & capturer has passer)={len(m.overlap)}")
# list the overlap states for 4flat count aware
m = V(4, False, ep=True, aware=True, race="count", variant="aware")
m.value(m.parse(POS))
print("\noverlap states (4flat, aware):")
for st in sorted(m.overlap, key=C.fmt):
    print("  ", C.fmt(st))
