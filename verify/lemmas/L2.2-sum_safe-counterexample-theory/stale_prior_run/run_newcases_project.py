"""Cross-validate new independent-search counterexamples with project code (pawns.value, lemmas.common W/alt)
and, for count rule on 8 ranks, crosscheck/minimax.py."""
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from crosscheck import minimax as mm
from lemmas.common import S, W, alt_outcome, hereditarily_safe
CASES = [((8, 8, False, False), "W: d2 f4 h5 / B: e5 e7 g7 h6", "count"),
         ((8, 8, False, False), "W: a4 c4 d5 e3 / B: b5 b6 c7 f6", "count"),
         ((8, 8, False, False), "W: c2 d5 f3 g3 / B: c3 c7 e6 f5", "mover"),
         ((8, 8, True, False), "W: e2 e6 g2 h5 / B: d6 f7 g7", "mover"),
         ((8, 8, True, False), "W: c5 e4 f6 g3 / B: d6 d7 f5 f7", "count"),
         ((8, 8, True, True), "W: e3 g3 h4 / B: a5 a6 f4 f6", "count")]
for bk, text, rule in CASES:
    b = Board(*bk); x = Pos.parse(text)
    xc = mm.outcome_class(mm.Board(*bk), mm.Position(x.white, x.black, None)) if rule == "count" else "-"
    print(bk, text, rule, "comps", len(pawns.components(b, x)), "sum_safe", pawns.sum_safe(b, x),
          "HSS", hereditarily_safe(b, x), "o(S)", cgt.outcome(S(b, x, rule)), "o(W)", cgt.outcome(W(b, x, rule)),
          "alt", alt_outcome(b, x, rule), "crosscheck", xc, flush=True)
