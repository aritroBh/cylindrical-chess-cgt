"""Recompute every pawn-only CGT value claimed in prior_work/main.tex.

Run:  .venv/bin/python -m cylcgt.verify_paper
"""
from dataclasses import replace

from . import cgt, pawns
from .pawns import CYL8, Board, Pos, RaceError, components, describe, passed, value

CLAIMS = [
    # label, position, claimed value (as written in the paper)
    ("2.1 zero", "W: e4 / B: e5", "0"),
    ("2.2 zero (wrap)", "W: a2 h1 / B: a3 h4", "0"),
    ("3.1 one", "W: a3 h1 / B: a4 h5", "1"),
    ("3.2 two", "W: a4 h1 / B: a5 h6", "2"),
    ("4.1 star", "W: e4 / B: e6", "*"),
    ("4.2 up (as drawn)", "W: e3 / B: e6", "↑"),
    ("4.2 up (intended? e2/e5)", "W: e2 / B: e5", "↑"),
    ("4.3 tiny", "W: a4 h2 h4 / B: a5 a6 a7 h3", "{0||0|-1} (tiny-1)"),
    ("7.1 puzzle 1 (total)", "W: a4 a5 c2 c3 f3 f4 h2 h3 / B: a7 c5 c6 f7 h6", "1 ± 1 + {{2|1}|0}"),
    ("7.1  c-file", "W: c2 c3 / B: c5 c6", "±1"),
    ("7.1  f-file", "W: f3 f4 / B: f7", "{{2|1}|0}"),
    ("7.1  a/h-files", "W: a4 a5 h2 h3 / B: a7 h6", "1"),
    ("7.2 pawn part (a,b,h files)", "W: a2 b2 h3 / B: a6 b7 h7", "±1"),
    ("7.3 pawns (kings removed)", "W: a1 a5 c1 c3 d3 f7 g1 h1 / B: c2 d4 d5 d6 g3 g7 h4", "2"),
]


def run(board: Board):
    print(f"\n=== board: {board.files}x{board.ranks} {'cylinder' if board.wrap else 'flat'}, "
          f"en passant {'on' if board.ep else 'off'} ===")
    for label, text, claim in CLAIMS:
        pos = Pos.parse(text)
        pawns.race_hits.clear()
        pawns._value.cache_clear()
        try:
            d = describe(board, pos)
        except RaceError as e:
            print(f"{label:30s} claim {claim:22s} -> RACE (both sides have passers) {e}")
            continue
        flags = []
        if any(r == 1 for _, r in pos.white) or any(r == board.ranks for _, r in pos.black):
            flags.append("illegal-in-chess (pawn on own back rank)")
        if passed(board, pos, "W") or passed(board, pos, "B"):
            flags.append("already has a passed pawn")
        if pawns.race_hits:
            alt = {}
            for rule in ("mover", "opponent"):
                pawns.RACE_RULE, saved = rule, pawns.RACE_RULE
                pawns._value.cache_clear()
                alt[rule] = cgt.show(value(board, pos))
                pawns.RACE_RULE = saved
            pawns._value.cache_clear()
            sens = "race-rule SENSITIVE" if len(set(alt.values()) | {d['value']}) > 1 else "race-rule robust"
            flags.append(f"{len(pawns.race_hits)} race lines, {sens} {alt}")
        print(f"{label:30s} claim {claim:22s} -> {d['value']:24s} outcome {d['outcome']}  "
              f"mean {d.get('mean')}  temp {d.get('temperature')}  {'; '.join(flags)}")


if __name__ == "__main__":
    run(CYL8)
    run(replace(CYL8, ep=False))
