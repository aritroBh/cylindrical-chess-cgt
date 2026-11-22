"""(library part of census.py) Census worker: S (sum model, fast outcome minimax) vs W (whole board) for passer-free positions.
usage: census.py W N SHARD NSHARDS   (reads positions from ./enum W N)
S_fast: outcome of the disjunctive sum of components, +-BIG banked as integers (cancel), pass moves for the
side owning a bank.  Validated against cylcgt (canonical forms) and sumtest/sumsolver in crosscheck.py."""
import sys, os, subprocess, time, resource
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
sys.setrecursionlimit(1_000_000)
from functools import lru_cache
from lemmas import common as C
from cylcgt import pawns, cgt
from cylcgt.pawns import Pos, Board

cgt.integer = lru_cache(maxsize=None)(cgt.integer)   # memoise (pure function; avoids rebuilding the 256-chain)
RULES = ("count", "mover", "opponent")
BIGC = 64   # integer value of a frozen passer component; passes spend 1 unit of the bank, as in cylcgt/sumsolver
_ck = lambda p: (tuple(sorted(p.white)), tuple(sorted(p.black)), p.ep or ())

def make_S(board):
    @lru_cache(maxsize=None)
    def children(comp, white, rule):
        """list of ('B', +-1) | ('C', tuple_of_new_comps)"""
        side = "W" if white else "B"
        lpos, rpos = C.split_ep(comp)
        src = lpos if white else rpos
        out = set()
        for c in pawns.moves(board, src, side):
            t = C.terminal(board, c)
            if t == 0:
                out.add(('B', 1 if C.race_winner(board, c, side, rule) == "W" else -1))
            elif t is not None:
                out.add(('B', t))
            else:
                subs = []
                for s in pawns.components(board, c):
                    subs.append(s)
                out.add(('C', tuple(sorted(subs, key=_ck))))
        return tuple(out)

    @lru_cache(maxsize=None)
    def live(comp):
        return bool(pawns.moves(board, comp, "W") or pawns.moves(board, comp, "B"))

    def norm(comps):
        return tuple(sorted((c for c in comps if live(c)), key=_ck))

    @lru_cache(maxsize=None)
    def win(comps, k, white, rule):
        """does the side to move win?"""
        if not comps:
            if k > 0: return white
            if k < 0: return not white
            return False
        for kind, x in _opts(comps, k, white, rule):
            if not win(x[0], x[1], not white, rule):
                return True
        return False

    def _opts(comps, k, white, rule):
        res = []
        seen = set()
        for i, c in enumerate(comps):
            if c in seen: continue
            seen.add(c)
            rest = comps[:i] + comps[i+1:]
            for kind, x in children(c, white, rule):
                if kind == 'B':
                    res.append((0, (norm(rest), k + x * BIGC)))
                else:
                    res.append((0, (norm(rest + x), k)))
        if white and k > 0:
            res.append((0, (comps, k - 1)))
        if (not white) and k < 0:
            res.append((0, (comps, k + 1)))
        return res

    def outcome(root, rule):
        comps = norm(pawns.components(board, root))
        lf, rf = win(comps, 0, True, rule), win(comps, 0, False, rule)
        return {(1,0):"L",(0,1):"R",(1,1):"N",(0,0):"P"}[(int(lf), int(rf))]
    def clear():
        children.cache_clear(); live.cache_clear(); win.cache_clear()
    return outcome, clear

def clear_all(sclear):
    sclear(); C.alt_winner.cache_clear(); pawns._value.cache_clear(); C._T_memo.clear()


_cache = {}
def S_for(board):
    if board not in _cache:
        _cache[board] = make_S(board)
    return _cache[board][0]
def clear():
    for o, c in _cache.values(): c()
