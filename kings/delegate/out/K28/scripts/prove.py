"""prove.py -- K28: build a finite win certificate from solver oracles.

Claim "CLAIMANT wins from ROOT": a certificate is a finite tree.  At a node with the claimant to move, ONE move is listed and it must
lead to a certified node; at a node with the opponent to move, EVERY legal move is listed and each must lead to a certified node.  A leaf
is a position that a solver oracle values exactly in the claimant's favour (claim W: B = W, claim L: A = L, where A >= true >= B,
White's view).  Every leaf is cited with the oracle entries that prove it.  No leaf is ever assumed.

usage: prove.py CLAIM(W|L) ROOT_POSITION  ORACLE_FILE [ORACLE_FILE ...]  [--depth D] [--out cert.txt] [--missing missing.txt]
An ORACLE_FILE is a kpsolve/kq3 output (`pos | A B | A: .. | B: ..`).  Several files give several witnesses for a leaf: with --need K a leaf
needs K different files that all prove it (K = 2 for "two solvers agree").
Positions whose own entry is needed but absent are written to --missing (they are then queried and the prover is run again)."""
import sys, argparse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import kchess

ap = argparse.ArgumentParser()
ap.add_argument('claim'); ap.add_argument('root'); ap.add_argument('oracles', nargs='+')
ap.add_argument('--depth', type=int, default=12); ap.add_argument('--need', type=int, default=1)
ap.add_argument('--out', default=None); ap.add_argument('--missing', default=None)
ap.add_argument('--stats', action='store_true')
a = ap.parse_args()
CL = a.claim  # 'W' or 'L'
RANK = {'L': 0, 'D': 1, 'W': 2}
root = kchess.canon(a.root)
claimant = 0 if CL == 'W' else 1

oracles = []          # list of (name, dict pos -> (A, B, moves))
for f in a.oracles:
    oracles.append((f.rsplit('/', 1)[-1], kchess.parse_kp_output(f)))

def proves(A, B):
    return B == 'W' if CL == 'W' else A == 'L'
def excludes(A, B):   # the oracle shows the claim is false
    return A != 'W' if CL == 'W' else B != 'L'

def entry_proof(pos):
    """names of the oracles that prove the claim at pos"""
    return [n for n, d in oracles if pos in d and proves(d[pos][0], d[pos][1])]
def entry_excl(pos):
    return [n for n, d in oracles if pos in d and excludes(d[pos][0], d[pos][1])]
def child_hint(parent, mvname):
    """(proved_by, excluded_by) for the child reached by mvname, from the parent's move lists."""
    pr, ex = [], []
    for n, d in oracles:
        if parent in d and mvname in d[parent][2]:
            A, B = d[parent][2][mvname]
            if proves(A, B): pr.append(n)
            if excludes(A, B): ex.append(n)
    return pr, ex

missing = set()
memo = {}      # pos -> certificate (list of lines) or None (definitely not provable within limits)
nodes = 0

def prove(pos, depth, path):
    """returns a certificate tuple (kind, data) or None"""
    global nodes
    if pos in memo: return memo[pos]
    if pos in path: return None            # a cycle gives no finite proof; do not memoise (depends on path)
    pr = entry_proof(pos)
    if len(pr) >= a.need:
        memo[pos] = ('leaf', pr); return memo[pos]
    ex = entry_excl(pos)
    if ex:
        memo[pos] = None; return None
    b, s = kchess.parse(pos)
    if depth == 0:
        return None
    mv = kchess.children(pos)
    if not mv:
        memo[pos] = None; return None   # terminal and not proved by an oracle: mate/stalemate are in the oracle, so treat as not proved
    nodes += 1
    path = path | {pos}
    if s == claimant:
        # choose a move: order by hints (child proved first, then undecided, skip excluded)
        cand = []
        for n_, c in mv:
            prh, exh = child_hint(pos, n_)
            if exh: continue
            cand.append((0 if len(prh) >= a.need else 1, n_, c))
        cand.sort()
        incomplete = False
        for _, n_, c in cand:
            r = prove(c, depth - 1, path)
            if r is not None:
                memo[pos] = ('or', n_, c, r); return memo[pos]
        return None
    else:
        kids = []
        for n_, c in mv:
            prh, exh = child_hint(pos, n_)
            if exh: return None             # this reply refutes the claim by an oracle (not memoised: another oracle might be stale)
        for n_, c in mv:
            r = prove(c, depth - 1, path)
            if r is None: return None
            kids.append((n_, c, r))
        memo[pos] = ('and', kids); return memo[pos]

def collect_missing(pos, depth, path, seen):
    """positions that are undecided by their parent's hints but have no own entry (so they cannot be expanded)"""
    if pos in seen or depth == 0 or pos in path: return
    seen.add(pos)
    if any(pos in d for _, d in oracles) is False:
        missing.add(pos); return
    if len(entry_proof(pos)) >= a.need or entry_excl(pos): return
    b, s = kchess.parse(pos)
    for n_, c in kchess.children(pos):
        prh, exh = child_hint(pos, n_)
        if exh and s != claimant: return
        if exh: continue
        if len(prh) >= a.need: continue
        collect_missing(c, depth - 1, path | {pos}, seen)

cert = prove(root, a.depth, frozenset())
lines = []
def show(pos, node, ind):
    pad = '  ' * ind
    if node[0] == 'leaf':
        lines.append(f"{pad}{pos}  LEAF proved by {', '.join(node[1])}")
    elif node[0] == 'or':
        lines.append(f"{pad}{pos}  [{'White' if claimant == 0 else 'Black'} plays {node[1]}]")
        show(node[2], node[3], ind + 1)
    else:
        lines.append(f"{pad}{pos}  [all {len(node[1])} replies]")
        for n_, c, r in node[1]:
            lines.append(f"{pad}  {n_}:")
            show(c, r, ind + 2)
if cert is not None:
    show(root, cert, 0)
    nleaf = sum(1 for l in lines if 'LEAF' in l)
    print(f"PROVED: {CL} from {root}; certificate has {len(lines)} lines, {nleaf} leaves, {nodes} internal nodes expanded")
    if a.out: open(a.out, 'w').write('\n'.join(lines) + '\n')
else:
    seen = set(); collect_missing(root, a.depth, frozenset(), seen)
    print(f"NOT PROVED within depth {a.depth}; {len(missing)} positions have no oracle entry")
    if a.missing: open(a.missing, 'w').write('\n'.join(sorted(missing)) + ('\n' if missing else ''))
