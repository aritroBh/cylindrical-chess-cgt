"""C4 verifier: root options of G = W a2 c2 / B b7 d7 under both passer tests (independent impl)."""
import sys
sys.argv = [sys.argv[0], sys.argv[1] if len(sys.argv) > 1 else "count", sys.argv[2] if len(sys.argv) > 2 else "aware"]
import importlib.util, os
spec = importlib.util.spec_from_file_location("ia", os.path.join(os.path.dirname(__file__), "indep_aware.py"))
ia = importlib.util.module_from_spec(spec); spec.loader.exec_module(ia)
from cylcgt import pawns, cgt
G = pawns.Pos.parse("W: a2 c2 / B: b7 d7")
for side in "WB":
    for c in pawns.moves(ia.B, G, side):
        print("  root", ia.RULE, "aware" if ia.AWARE else "plain", side, "->", c, ":", cgt.show(ia.after(c, side)))
