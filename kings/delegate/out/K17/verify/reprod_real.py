"""Referee reproduction of the 'real kings, check at the root' hit counts with my own generator and my own D,
using my private build of kp_p (P model, real kings).
usage: reprod_real.py gen  <spec> <files> <maxp> <outprefix>   -> writes <outprefix>.in (kp queries) and .meta
       reprod_real.py eval <spec> <outprefix>                   -> reads <outprefix>.out
Layout (as described in the task): Z = locked pair Pa(r)/pa(r+1) on file a, Black king b(r+1) (attacked by Pa(r)),
White king on any square of files a,b not adjacent to the Black king; context pawns on the given files, ranks
2..H-1, 1..maxp pawns per colour, no passer at the root (e.p.-aware).  Hit: P = W (White wins, Black to move)
with at least one legal Black move, and D(Black to move) = Black wins in my own D."""
import sys, itertools, json
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from dgame import *

def nm(s): return chr(97 + s[0]) + str(s[1])

def contexts(bd, files, maxp):
    sqs = [(f, r) for f in files for r in range(2, bd.h)]
    for w in range(1, maxp + 1):
        for ws in itertools.combinations(sqs, w):
            rest = [s for s in sqs if s not in ws]
            for bl in range(1, maxp + 1):
                for bs in itertools.combinations(rest, bl):
                    pos = (frozenset(ws), frozenset(bs), None)
                    if terminal(bd, pos) is not None: continue
                    yield pos

def main_gen(spec, files, maxp, pre):
    kind, dims = spec.split(':'); w, h = map(int, dims.split('x'))
    bd = Bd(w, h, kind == 'cyl'); alt = make_alt(bd)
    ctxs = list(contexts(bd, files, maxp))
    cand = [p for p in ctxs if alt(p, 'B') == 'B']
    print('contexts', len(ctxs), 'D(Black first)=Black wins', len(cand))
    qs = []; meta = []
    for r in range(2, h - 1):
        wz, bz, bk = (0, r), (0, r + 1), (1, r + 1)
        for f in (0, 1):
            for rk in range(1, h + 1):
                wk = (f, rk)
                if wk in (wz, bz, bk): continue
                if abs(wk[0] - bk[0]) <= 1 and abs(wk[1] - bk[1]) <= 1: continue
                for p in cand:
                    toks = ['K' + 'ab'[f] + str(rk), 'k' + nm(bk), 'P' + nm(wz), 'p' + nm(bz)]
                    toks += ['P' + nm(s) for s in sorted(p[0])] + ['p' + nm(s) for s in sorted(p[1])]
                    qs.append(' '.join(toks) + ' b -')
    open(pre + '.in', 'w').write('\n'.join(qs) + '\n')
    print('queries', len(qs))

def main_eval(spec, pre):
    hits = []; tot = 0; mated = 0; illegal = 0
    for ln in open(pre + '.out'):
        if ' | ' not in ln: continue
        pos, rest = ln.split(' | ', 1)
        parts = rest.split(' | ')
        head = parts[0].split(); mv = parts[1].split() if len(parts) > 1 else []
        tot += 1
        if head[0] == 'X': illegal += 1; continue
        if head[0] == 'W':
            if not mv: mated += 1
            else: hits.append(pos)
    print('answered', tot, 'illegal', illegal, 'W with no legal move (mate)', mated, 'HITS', len(hits))
    json.dump(hits, open(pre + '.hits.json', 'w'))

if __name__ == '__main__':
    if sys.argv[1] == 'gen':
        main_gen(sys.argv[2], [int(x) for x in sys.argv[3].split(',')], int(sys.argv[4]), sys.argv[5])
    else:
        main_eval(sys.argv[2], sys.argv[3])
