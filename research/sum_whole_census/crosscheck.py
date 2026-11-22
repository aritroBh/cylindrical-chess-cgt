"""Cross-check: census fast solver (A) vs cylcgt canonical forms (B) vs sumtest/sumsolver (C), both modes.
usage: crosscheck.py NPER TEST(0|1) SEED OUT   -- NPER positions sampled uniformly from all census positions
(widths 3,4,5; n=2..6); for each rule compare
  S: fastS == cylcgt outcome(pawns.value) == sumsolver comp-mode G outcome
  W: alt_outcome == cylcgt outcome(lemmas W canonical form) == sumsolver whole-mode G outcome"""
import sys, random, subprocess, time
R0 = '/Users/aritro/Downloads/Research/Chessendgames'
sys.path.insert(0, R0); sys.path.insert(0, R0 + '/sumtest'); sys.setrecursionlimit(1_000_000)
from functools import lru_cache
from lemmas import common as C
from cylcgt import pawns, cgt
from cylcgt.pawns import Pos, Board
import sumsolver as SS
cgt.integer = lru_cache(maxsize=None)(cgt.integer)
sys.argv_ = sys.argv
import importlib.util
spec = importlib.util.spec_from_file_location('census_mod', R0 + '/research/sum_whole_census/s_exact.py'); cl = importlib.util.module_from_spec(spec); spec.loader.exec_module(cl)

nper, test, seed, outf = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
stratum = sys.argv[5] if len(sys.argv) > 5 else 'uniform'
random.seed(seed)
pool = []
for w in (3, 4, 5):
    for n in range(2, 7):
        for l in subprocess.run([R0 + '/research/sum_whole_census/enum', str(w), str(n)], capture_output=True, text=True).stdout.splitlines():
            pool.append((w, l.split(' ', 1)[1]))
if stratum == 'multi':      # extra stratum: at least 2 components at the root and >=4 pawns
    def ncomp(w, t): return len(pawns.components(Board(w, 8, False, True), Pos.parse(t)))
    pool = [x for x in pool if x[0] >= 4 and ncomp(*x) >= 2 and len(x[1].replace('/', ' ').replace('W:', ' ').replace('B:', ' ').split()) >= 5]
if stratum == 'dis':        # positions where the census found S != W in at least one rule (this test)
    import glob, re
    pool = []
    cols = (8, 9, 10) if test else (4, 5, 6)
    for f in sorted(glob.glob(R0 + '/research/sum_whole_census/data/raw_w*.tsv')):
        w = int(re.search(r'raw_w(\d)_', f).group(1))
        for l in open(f):
            r = l.rstrip('\n').split('\t')
            if any(r[c][0] != r[c][1] for c in cols): pool.append((w, r[1]))
sample = random.sample(pool, min(nper, len(pool)))
pawns.PASSED_RESPECTS_EP = bool(test)
def ss_outcome(w, text, rule, mode):
    geo = SS.Geometry(w, False)
    rules = SS.Rules(geo, ep=True, ep_aware=bool(test), race_rule=rule, race_double=True)
    T = SS.Trees(); z = T.node()
    sol = SS.SumSolver(rules, T, mode=mode, ep_scope='component')
    W, B = geo.parse(text)
    return sol.outcomes(W, B, [z])[0]
out = open(outf, 'w'); agree = {}; tot = {}
t0 = time.time()
for rule in ("count", "mover", "opponent"):
    pawns.RACE_RULE = rule
    for i, (w, text) in enumerate(sample):
        board = Board(w, 8, False, True); p = Pos.parse(text)
        if i % 200 == 0:
            pawns._value.cache_clear(); C._W_memo.clear(); C.alt_winner.cache_clear(); cl.clear()
        a_S = cl.S_for(board)(p, rule); a_W = C.alt_outcome(board, p, rule)
        b_S = cgt.outcome(pawns.value(board, p)); b_W = cgt.outcome(C.W(board, p, rule))
        c_S = ss_outcome(w, text, rule, 'comp'); c_W = ss_outcome(w, text, rule, 'whole')
        for name, vals in (('S', (a_S, b_S, c_S)), ('W', (a_W, b_W, c_W))):
            k = (rule, name); tot[k] = tot.get(k, 0) + 1
            ok = len(set(vals)) == 1
            agree[k] = agree.get(k, 0) + ok
            if not ok: out.write(f"MISMATCH\t{w}\t{text}\t{rule}\t{name}\tfast={vals[0]}\tcylcgt={vals[1]}\tsumsolver={vals[2]}\n")
        if i % 100 == 99: print(rule, i + 1, time.time() - t0, flush=True)
for k in sorted(tot): out.write(f"AGREE\t{stratum}\ttest={test}\t{k[0]}\t{k[1]}\t{agree[k]}/{tot[k]}\n")
out.close()
print({k: f"{agree[k]}/{tot[k]}" for k in sorted(tot)})
