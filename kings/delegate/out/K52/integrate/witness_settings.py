"""No-(E) witness under each passed test and race rule. Exact calls:
  pawns.RACE_RULE = rule; pawns.PASSED_RESPECTS_EP = ep_aware; pawns._value.cache_clear()
  cgt.outcome(pawns.value(Board(5, 7, False, True), X))      -> o(S)
  common.alt_outcome(Board(5, 7, False, True), X, rule)       -> o(W)
with X = Pos(W a4 b3 e2 / B a5 b4 e4, ep=((0,3),(0,4),'B')): Black may take a4 e.p. on a3."""
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas import common
b = Board(5, 7, False, True)
for text, tm in (("W: a4 b3 e2 / B: a5 b4 e4", "both"), ("W: a4 b2 b3 e2 e4 / B: a5 b4 b6 e6", "B")):
    p = Pos.parse(text); X = Pos(p.white, p.black, ((0, 3), (0, 4), "B"))
    for ep_aware in (True, False):
        for rule in ("count", "mover", "opponent"):
            pawns.RACE_RULE = rule; pawns.PASSED_RESPECTS_EP = ep_aware
            pawns._value.cache_clear(); common.alt_winner.cache_clear(); common._T_memo.clear()
            hits0 = len(pawns.race_hits)
            S = cgt.outcome(pawns.value(b, X)); Wo = common.alt_outcome(b, X, rule)
            print(f"{text} (ep a3) BIG={pawns.BIG} ep-aware={ep_aware} rule={rule}: o(S)={S} o(W)={Wo} "
                  f"HSS={common.hereditarily_safe(b, X)} races_in_S={len(pawns.race_hits) - hits0}")
