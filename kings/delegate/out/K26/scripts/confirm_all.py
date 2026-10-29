#!/usr/bin/env python3
"""K26 final: re-verify EVERY exact group of logs/exact_groups_all.json (dud and on_strong, all boards, all pawn limits) with the independent solver ref3m (--moves; own move
generator, shares no code with kpsolve/kpp), directly from the definition of the class:
  dud:       at all 8 roots (king states x side to move) the mover's only move that does not lose at once is its shuttle (a King move between its two shuttle squares), the shuttle exists exactly once
             and is legal, and every root value is D;
  on_strong: White-to-move roots: only the shuttle does not lose at once; Black-to-move roots: Black has >= 1 legal move and every Black move is lost for Black (value W for White).
Loses at once = the value of the position after the move is L for a White move, W for a Black move (P model, first promotion wins).  A promotion is a move that does not lose at once for the mover.
Usage: confirm_all.py [out.json]   (set K26_BIN for a private build; ref3m is run in batches of 200 positions per board)"""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k26lib import run_solver, safe_nice, OUT
safe_nice()
LOG = os.path.join(OUT, 'logs')
groups = json.load(open(os.path.join(LOG, 'exact_groups_all.json')))
if os.environ.get('K26_GROUPS'):      # alternative group list (same format), e.g. the four-file groups
    groups = json.load(open(os.environ['K26_GROUPS']))
ofile = sys.argv[1] if len(sys.argv) > 1 else os.path.join(LOG, 'confirm_all.json')


def roots(g):
    L = []
    for wk in g['wk']:
        for bk in g['bk']:
            for s in 'wb':
                L.append((wk, bk, s, ' '.join(['K' + wk, 'k' + bk] + ['P' + x for x in g['wp']] + ['p' + x for x in g['bp']] + [s, '-'])))
    return L


def parse(line):
    parts = line.split(' | ')
    toks = parts[1].split()
    mv = []
    for t in toks[1:]:
        nm, v = t.rsplit(':', 1)
        mv.append((nm, v))
    return toks[0], mv


def check(g, line, wk, bk, s):
    val, mv = parse(line)
    if val == 'X':
        return 'illegal root'
    if s == 'w':
        shuttle = set(g['wk'])
        nsh = [m for m in mv if m[0][0] == 'K' and len(m[0]) == 5 and {m[0][1:3], m[0][3:5]} == shuttle]
        leaks = [m for m in mv if m not in nsh and m[1] != 'L']
        if len(nsh) != 1 or leaks:
            return 'white: shuttle %d leaks %s' % (len(nsh), leaks[:3])
        if g['class'] == 'dud' and val != 'D':
            return 'root value %s' % val
    else:
        if g['class'] == 'dud':
            shuttle = set(g['bk'])
            nsh = [m for m in mv if m[0][0] == 'K' and len(m[0]) == 5 and {m[0][1:3], m[0][3:5]} == shuttle]
            leaks = [m for m in mv if m not in nsh and m[1] != 'W']
            if len(nsh) != 1 or leaks:
                return 'black: shuttle %d leaks %s' % (len(nsh), leaks[:3])
            if val != 'D':
                return 'root value %s' % val
        else:
            if not mv or any(m[1] != 'W' for m in mv):
                return 'black not frozen: %s' % mv[:4]
    return None


by_board = collections.defaultdict(list)
for g in groups:
    by_board[g['board']].append(g)
fails = []
nroots = 0
perclass = collections.Counter()
for board, gs in by_board.items():
    L, meta = [], []
    for g in gs:
        for (wk, bk, s, line) in roots(g):
            L.append(line)
            meta.append((g, wk, bk, s))
    res = []
    for lo in range(0, len(L), 200):
        r, _ = run_solver(L[lo:lo + 200], board, 'ref3m', moves=True)
        res += r
    for (g, wk, bk, s), line in zip(meta, res):
        nroots += 1
        why = check(g, line, wk, bk, s)
        if why:
            fails.append({'id': g['id'], 'board': board, 'root': line.split(' | ')[0], 'why': why})
    for g in gs:
        perclass[(g['class'], board)] += 1
    print(board, len(gs), 'groups', len(L), 'roots', 'failures so far', len(fails), file=sys.stderr, flush=True)
out = {'groups': len(groups), 'roots': nroots, 'failures': fails, 'per_class_board': {'%s %s' % k: v for k, v in perclass.items()}}
json.dump(out, open(ofile, 'w'), indent=1)
print(json.dumps({k: out[k] for k in ('groups', 'roots')}), 'failures', len(fails))
