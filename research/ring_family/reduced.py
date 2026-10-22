"""Reduced game: delete every move after which the opponent has an immediate terminal win (a passed pawn that
decides the game).  Uses cylcgt only for move generation / passed tests / canonical forms."""
import sys
sys.path.insert(0, "research/ring_family")
from ringlib import *
from cylcgt import pawns, cgt
from cylcgt.pawns import Board, Pos, name
pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True

BIG = pawns.BIG
def other(s): return "B" if s == "W" else "W"

class Reducer:
    def __init__(self, n):
        self.board = Board(n, 8, True, True)
        self.memo = {}
        self.pmemo = {}
        self.nodes = 0
        self.poisoned_count = 0
        self.moved = set()      # (file, origin square, colour) of pawns that moved in reduced tree
    def terminal_for(self, pos, mover):
        """value of position after `mover` moved, if terminal (as cgt integer), else None"""
        v = pawns._child(self.board, pos, mover)
        return v if v.num is not None and abs(v.num) >= BIG // 2 else None
    def poisoned(self, child, mover):
        """True if after mover's move to `child`, the opponent has a move to a terminal win for the opponent"""
        key = (child, mover)
        r = self.pmemo.get(key)
        if r is not None: return r
        opp = other(mover)
        plain = Pos(child.white, child.black, None)
        lpos = plain if (child.ep and child.ep[2] != opp) else child
        res = False
        for c2 in pawns.moves(self.board, lpos, opp):
            v = pawns._child(self.board, c2, opp)
            if v.num is not None and ((v.num >= BIG // 2) if opp == "W" else (v.num <= -BIG // 2)):
                res = True; break
        self.pmemo[key] = res
        return res
    def options(self, pos, side):
        plain = Pos(pos.white, pos.black, None)
        lpos = plain if (pos.ep and pos.ep[2] != side) else pos
        out = []
        for ch in pawns.moves(self.board, lpos, side):
            tv = self.terminal_for(ch, side)
            if tv is not None:
                # terminal result of this very move
                good = (tv.num > 0) == (side == "W")
                if good: out.append((ch, tv, False))      # winning move: keep (value +-BIG)
                else: self.poisoned_count += 1             # immediately losing move: delete
                continue
            if self.poisoned(ch, side):
                self.poisoned_count += 1
                continue
            out.append((ch, None, True))
        return out
    def value(self, pos):
        wp, bp = pawns.passed(self.board, pos, "W"), pawns.passed(self.board, pos, "B")
        if wp != bp: return cgt.integer(BIG if wp else -BIG)
        r = self.memo.get(pos)
        if r is not None: return r
        self.nodes += 1
        plain = Pos(pos.white, pos.black, None)
        L = []; R = []
        for side, lst in (("W", L), ("B", R)):
            for ch, tv, rec in self.options(pos, side):
                lst.append(tv if tv is not None else self.value(ch))
        g = cgt.make(L, R)
        self.memo[pos] = g
        return g

if __name__ == "__main__":
    ring = from_cstr(sys.argv[1]); n = len(ring)
    red = Reducer(n)
    pos = Pos.parse(to_text(ring))
    g = red.value(pos)
    print("reduced value:", cgt.show(g), "| reduced nodes:", red.nodes, "| deleted moves seen:", red.poisoned_count)

def moved_files(red, ring):
    """for every node in reduced memo, list files whose pawn set changes along kept (reduced) moves"""
    from collections import Counter
    cnt = Counter()
    for pos in list(red.memo.keys()):
        for side in ("W", "B"):
            for ch, tv, rec in red.options(pos, side):
                mine = pos.white if side == "W" else pos.black
                chm = ch.white if side == "W" else ch.black
                src = next(iter(mine - chm), None)
                dst = next(iter(chm - mine), None)
                if src: cnt[(side, src[0], 'from')] += 1
    return cnt
