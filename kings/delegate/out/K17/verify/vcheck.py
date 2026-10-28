"""Referee's own check of (V1a)-(V4) of Theorem 1.14 at every chess-reachable position before the first decisive
event, for a root position of the structured class, P model with real kings (my psolve) -- independent of K17.
usage: vcheck.py <spec> <FZ files e.g. 0,1> <pos> [<pos> ...]      ('pos' = 'Ka2 kb4 ... b -' in quotes)
Decisive events: a move after which a context pawn is passed (my dgame.terminal on the CONTEXT pawns only,
e.p.-aware), beneficiary by the 'count' race rule; or any Z-move (V3: must be a P-loss for the mover).
Checks: V1b (>= 1 legal move), V1a (no check; non-Z legal moves == D-options of the context game, same results),
V2 (decisive event by a non-Z move: P-value for the mover agrees with the beneficiary), V3, V4 (pairwise safety of the
re-split context components, hereditarily -- via dgame/ecl code)."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import psolve
from dgame import *
import ecl


def ctx_pos(pb, bd, pos, FZ):
    wk, bk, wp, bp, side, ep = pos
    cw = frozenset((f, r + 1) for f, r in wp if f not in FZ)
    cb = frozenset((f, r + 1) for f, r in bp if f not in FZ)
    e = None
    if ep is not None:
        (tf, tr), col = ep
        if tf not in FZ:
            if col == 0: e = ((tf, tr + 1), (tf, tr + 2), 'B')
            else: e = ((tf, tr + 1), (tf, tr), 'W')
    return (cw, cb, e)


def main(spec, FZ, texts):
    kind, dims = spec.split(':'); w, h = map(int, dims.split('x'))
    pb = psolve.Board(w, h, kind == 'cyl'); bd = Bd(w, h, kind == 'cyl')
    FZ = set(FZ)
    roots = [psolve.parse(pb, t) for t in texts]
    S = psolve.Solver(pb); S.explore(roots); S.solve()
    print('# P states', len(S.succ))
    for root in roots:
        print('ROOT', psolve.fmt(pb, root), '  P(White view) =', S.white_view(root))
        seen = set(); stack = [root]; res = dict(V1a=True, V1b=True, V2=True, V3=True, V4=True); notes = []
        order = []
        while stack:
            p = stack.pop()
            if p in seen: continue
            seen.add(p); order.append(p)
            side = p[4]; me = 'W' if side == 0 else 'B'; mover_val_of = lambda v: v
            ms = S.succ[p]
            if not ms: res['V1b'] = False; notes.append('no legal move at ' + psolve.fmt(pb, p))
            cp = ctx_pos(pb, bd, p, FZ)
            # V4 at p (pairwise safety of components of the context, hereditary handled by visiting all p)
            if not _safe(bd, cp): res['V4'] = False; notes.append('V4: unsafe components at ' + psolve.fmt(pb, p))
            dopts = {}
            for c in gen(bd, cp, me):
                dopts[(c[0], c[1])] = c
            in_chk = psolve.in_check(pb, p)
            nonZ = {}
            for kind_, q, lab in ms:
                if kind_ == 'P':
                    # promotion by a pawn: which file?  treat as non-Z if the pawn file not in FZ
                    notes.append('promotion available at ' + psolve.fmt(pb, p) + ' ' + lab)
                    res['V2'] = False
                    continue
                isZ = (kind_ == 'K') or (kind_ == 'p' and pawn_file(lab) in FZ)
                v = {'W': 'L', 'L': 'W', 'D': 'D'}[S.val[q]]   # value for the mover
                if isZ:
                    if v != 'L': res['V3'] = False; notes.append('Z-move not a suicide: %s at %s -> %s' % (lab, psolve.fmt(pb, p), v))
                else:
                    cq = ctx_pos(pb, bd, q, FZ)
                    nonZ[(cq[0], cq[1])] = (q, v)
            if in_chk and nonZ: res['V1a'] = False; notes.append('check but non-Z move legal?!')
            if set(nonZ) != set(dopts):
                res['V1a'] = False
                notes.append('V1a: non-Z legal moves differ from D-options at %s (in_check=%s): legal-only %d, D-only %d' % (
                    psolve.fmt(pb, p), in_chk, len(set(nonZ) - set(dopts)), len(set(dopts) - set(nonZ))))
            for k, (q, v) in nonZ.items():
                if k not in dopts: continue
                c = dopts[k]
                t = terminal(bd, c)
                if t is None:
                    if q not in seen: stack.append(q)
                else:
                    ben = ('W' if t == 1 else 'B') if t != 0 else race_winner(bd, c, me)
                    want = 'W' if ben == me else 'L'
                    if v != want: res['V2'] = False; notes.append('V2: event %s at %s: D beneficiary %s, P value for mover %s' % (k, psolve.fmt(pb, p), ben, v))
        print('  chess-reachable positions before first decisive event:', len(order), ' flags:', res)
        for n_ in notes[:8]: print('   note:', n_)
        for p in order: print('   pos', psolve.fmt(pb, p), ' P(white view)', S.white_view(p))


def pawn_file(lab):
    # label 'P(f, r)-(f2, r2)' or 'P(f, r)x(f2, r2)...'
    return int(lab[2:lab.index(',')])


_tau_memo = {}


def _tau(bd, pos):
    k = (bd.w, bd.h, bd.wrap, pos)
    if k in _tau_memo: return _tau_memo[k]
    out = set()
    if passed_set(bd, pos, 'W'): out.add(1)
    if passed_set(bd, pos, 'B'): out.add(-1)
    if not out:
        for side in 'WB':
            for c in gen(bd, pos, side): out |= _tau(bd, c)
    _tau_memo[k] = frozenset(out)
    return _tau_memo[k]


def _safe(bd, pos):
    ts = [_tau(bd, c) for c in ecl.comps_of(bd, pos)]
    return not any(i != j and 1 in a and -1 in b for i, a in enumerate(ts) for j, b in enumerate(ts))


if __name__ == '__main__':
    main(sys.argv[1], [int(x) for x in sys.argv[2].split(',')], sys.argv[3:])
