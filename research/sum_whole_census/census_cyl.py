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
    w, n, shard, nsh = map(int, sys.argv[1:5])
    lines = subprocess.run(['/Users/aritro/Downloads/Research/Chessendgames/research/sum_whole_census/enum_cyl', str(w), str(n)],
                           capture_output=True, text=True).stdout.splitlines()
    lines = lines[shard::nsh]
    board = Board(w, 8, True, True)
    Sout, sclear = make_S(board)
    out = open(f'/Users/aritro/Downloads/Research/Chessendgames/research/sum_whole_census/data/raw_cyl{w}_n{n}_s{shard}of{nsh}.tsv', 'w')
    BLOCK = 1500
    t0 = time.time()
    for b0 in range(0, len(lines), BLOCK):
        blk = lines[b0:b0+BLOCK]
        poss = [Pos.parse(l.split(' ', 1)[1]) for l in blk]
        rows = [[l.split(' ',1)[0], l.split(' ',1)[1], str(len(pawns.components(board, p)))] for l, p in zip(blk, poss)]
        for test in (0, 1):                       # 0 textbook, 1 e.p.-aware
            pawns.PASSED_RESPECTS_EP = bool(test)
            clear_all(sclear)
            hss = [C.hereditarily_safe(board, p) for p in poss]
            for r, h in zip(rows, hss): r.append('1' if h else '0')
            for rule in RULES:
                pawns.RACE_RULE = rule
                clear_all(sclear)
                for r, p in zip(rows, poss):
                    s = Sout(p, rule); wv = C.alt_outcome(board, p, rule)
                    ss = pawns.sum_safe(board, p) if len(pawns.components(board, p)) > 1 else True
                    r.append(f"{s}{wv}{'1' if ss else '0'}")
        for r in rows: out.write('\t'.join(r) + '\n')
        out.flush()
        print(f"{b0+len(blk)}/{len(lines)} t={time.time()-t0:.0f}s rss={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6:.2f}GB", flush=True)
main()
