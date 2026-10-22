import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "verify_ext", "codex")); sys.path.insert(0, os.path.dirname(__file__))
import solver as cx
from common import *
for text in sys.argv[1:]:
    W, B = parse_pos(text); width = max(f for f, _ in W + B) + 1
    g = pawns.value(pawns.Board(width, 8, False, True), pawns.Pos(frozenset(W), frozenset(B)))
    pg = cx.PawnGame(width, "count", True, "aware"); st = cx.parse_position(text.replace(":", ""), width)
    lm, rm = pg._outcome_masks(*st); lf, rf = bool(lm & 1), bool(rm & 1)
    oc = "N" if lf and rf else "L" if lf else "R" if rf else "P"
    print(text, "| cylcgt", outcome_nim(g), "| codex bitmask", oc, flush=True)
