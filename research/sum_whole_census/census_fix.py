"""Census worker: S (sum model, fast outcome minimax) vs W (whole board) for passer-free positions.
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
_ck = lambda p: (tuple(sorted(p.white)), tuple(sorted(p.black)), p.ep or ())

sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/research/sum_whole_census')
from s_exact import make_S

def clear_all(sclear):
    sclear(); C.alt_winner.cache_clear(); pawns._value.cache_clear(); C._T_memo.clear()


def main():
    src, dst = sys.argv[1], sys.argv[2]
    w = int(src.split('raw_w')[1][0])
    board = Board(w, 8, False, True)
    Sout, sclear = make_S(board)
    lines = [l.rstrip('\n').split('\t') for l in open(src)]
    out = open(dst, 'w'); t0 = time.time(); BLOCK = 1500
    for b0 in range(0, len(lines), BLOCK):
        rows = lines[b0:b0+BLOCK]
        poss = [Pos.parse(r[1]) for r in rows]
        for test, base in ((0, 3), (1, 7)):
            pawns.PASSED_RESPECTS_EP = bool(test)
            for ri, rule in enumerate(RULES):
                pawns.RACE_RULE = rule
                clear_all(sclear)
                for r, p in zip(rows, poss):
                    e = r[base+1+ri]
                    r[base+1+ri] = Sout(p, rule) + e[1:]
        for r in rows: out.write('\t'.join(r) + '\n')
        out.flush()
        print(f"{b0+len(rows)}/{len(lines)} t={time.time()-t0:.0f}s", flush=True)
main()
