"""diff_rules.py -- differential test of the rule transcriptions on random positions.

Compares, position by position and move by move:
  M = myeng.py (this directory)
  T = T50 verifier engine (t50/eng.py, unchanged copy)
  C = cylcgt/pawns.py RULE PREDICATES ONLY (moves, passed, promote_distance; the race decision is rewritten here from
      pawns._child).  No game value (cgt.py) is computed.  C is optional (skipped if cylcgt cannot be imported).
What is compared: the set of (new position, e.p. flag) of every move of each colour; the verdict (W/B/None, with the race
rule) after every move; the T/L/P/K classification of every move (M vs T); the race distances.
Usage (project root):  PYTHONPATH=. python -B research/ring_n_plus_2_proof/verify_compute/diff_rules.py [seed] [walks]
"""
import os, random, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 't50'))
import myeng as M
import eng as T

try:
    from cylcgt import pawns as C
    HAVE_C = True
except Exception as ex:                      # pragma: no cover
    HAVE_C = False
    print('cylcgt.pawns not importable:', ex)

LET = {0: 'W', 1: 'B'}


def to_T(ep):
    return None if ep is None else (ep[0], LET[ep[1]])


def from_T(ep):
    return None if ep is None else (ep[0], 0 if ep[1] == 'W' else 1)


# ---- conversion to / from the pawns.py representation
def to_C(pos, ep):
    white = frozenset((f, r) for f in range(len(pos)) for r in M.bits(pos[f][0]))
    black = frozenset((f, r) for f in range(len(pos)) for r in M.bits(pos[f][1]))
    raw = None
    if ep is not None:
        f, st = ep
        if st == 0:
            raw = ((f, 3), (f, 4), 'B')
        else:
            raw = ((f, 6), (f, 5), 'W')
    return C.Pos(white, black, raw)


def from_C(p, n):
    w = [0] * n
    b = [0] * n
    for f, r in p.white:
        w[f] |= 1 << (r - 1)
    for f, r in p.black:
        b[f] |= 1 << (r - 1)
    pos = tuple(zip(w, b))
    ep = None
    if p.ep is not None:
        (f, _), (f2, r2), capturer = p.ep
        stepper = 0 if capturer == 'B' else 1
        cap_mask_idx = 1 - stepper
        if (pos[(f - 1) % n][cap_mask_idx] | pos[(f + 1) % n][cap_mask_idx]) >> (r2 - 1) & 1:
            ep = (f, stepper)
    return pos, ep


def verdict_C(board, p, mover):
    wp, bp = C.passed(board, p, 'W'), C.passed(board, p, 'B')
    if wp and bp:
        other = 'B' if mover == 'W' else 'W'
        win = other if C.promote_distance(board, p, other) <= C.promote_distance(board, p, mover) else mover
        return 0 if win == 'W' else 1
    if wp:
        return 0
    if bp:
        return 1
    return None


stats = dict(positions=0, move_sets=0, children=0, races=0, ep_flags=0, ep_caps=0, kinds=0, dist=0, v_none=0, v_W=0, v_B=0, mism=0)


def bad(msg):
    stats['mism'] += 1
    if stats['mism'] <= 20:
        print('MISMATCH', msg, flush=True)


def compare_position(pos, ep, board):
    n = len(pos)
    stats['positions'] += 1
    if ep is not None:
        stats['ep_flags'] += 1
    for c in (0, 1):
        sm = set(M.gen_moves(pos, ep, c))
        st = set((p, from_T(e)) for p, e in T.moves(pos, to_T(ep), LET[c]))
        stats['move_sets'] += 1
        if sm != st:
            bad(('moves M!=T', n, pos, ep, c, len(sm), len(st)))
        if HAVE_C:
            cp = to_C(pos, ep)
            sc = set(from_C(q, n) for q in C.moves(board, cp, LET[c]))
            if sm != sc:
                bad(('moves M!=C', n, pos, ep, c, len(sm), len(sc)))
        # e.p. captures exercised: moves available only because of the flag
        if ep is not None and ep[1] != c:
            stats['ep_caps'] += len(sm - set(M.gen_moves(pos, None, c)))
        # verdicts and classification
        cl_M = {(k, p, e) for k, p, e in M.classify(pos, ep, c)}
        cl_T = {(k, p, from_T(e)) for k, p, e in T.classify_moves(pos, to_T(ep), LET[c])}
        stats['kinds'] += 1
        if cl_M != cl_T:
            bad(('classify M!=T', n, pos, ep, c))
        for (np_, ne) in sm:
            stats['children'] += 1
            vm = M.verdict(np_, ne, c)
            stats['v_none' if vm is None else 'v_W' if vm == 0 else 'v_B'] += 1
            vt = T.status(np_, to_T(ne), LET[c])
            vt = None if vt is None else (0 if vt == 'W' else 1)
            if vm != vt:
                bad(('verdict M!=T', n, np_, ne, c, vm, vt))
            if HAVE_C:
                vc = verdict_C(board, to_C(np_, ne), LET[c])
                if vm != vc:
                    bad(('verdict M!=C', n, np_, ne, c, vm, vc))
            wp, bp = M.passed_pawns(np_, ne, 0), M.passed_pawns(np_, ne, 1)
            if wp and bp:
                stats['races'] += 1
                for s in (0, 1):
                    dm = M.promo_dist(np_, ne, s)
                    dt = T.prom_dist(np_, to_T(ne), LET[s])
                    stats['dist'] += 1
                    if dm != dt:
                        bad(('dist M!=T', n, np_, ne, s, dm, dt))
                    if HAVE_C:
                        dc = C.promote_distance(board, to_C(np_, ne), LET[s])
                        if dm != dc:
                            bad(('dist M!=C', n, np_, ne, s, dm, dc))
            # the sets of passed pawns
            twp = sorted(T.passed_ranks(np_, to_T(ne), 'W'))
            tbp = sorted(T.passed_ranks(np_, to_T(ne), 'B'))
            if sorted(wp) != twp or sorted(bp) != tbp:
                bad(('passed M!=T', n, np_, ne))
            if HAVE_C:
                cpp = to_C(np_, ne)
                if bool(wp) != C.passed(board, cpp, 'W') or bool(bp) != C.passed(board, cpp, 'B'):
                    bad(('passed M!=C', n, np_, ne))


def random_dense(rng, n):
    toks = []
    pos = []
    for f in range(n):
        w = b = 0
        for _ in range(rng.choice([0, 1, 1, 1, 2])):
            w |= 1 << (rng.choice([2, 2, 3, 4, 5, 6, 7]) - 1)
        for _ in range(rng.choice([0, 1, 1, 1, 2])):
            r = rng.choice([7, 7, 6, 5, 4, 3, 2])
            if not (w >> (r - 1)) & 1:
                b |= 1 << (r - 1)
        pos.append((w, b))
    return tuple(pos)


def walk(rng, pos, ep, plies, board):
    c = rng.choice([0, 1])
    for _ in range(plies):
        compare_position(pos, ep, board)
        ms = M.gen_moves(pos, ep, c)
        if not ms:
            c = 1 - c
            ms = M.gen_moves(pos, ep, c)
            if not ms:
                return
        pos, ep = rng.choice(ms)
        c = 1 - c


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    walks = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    rng = random.Random(seed)
    t0 = time.time()
    boards = {}
    for _ in range(walks):
        kind = rng.random()
        if kind < 0.4:
            n = rng.choice([8, 10, 12, 14])
            pos = M.P_start(n)
        else:
            n = rng.choice([4, 5, 6, 7, 8, 9])
            pos = random_dense(rng, n)
        if HAVE_C:
            board = boards.setdefault(n, C.Board(n, 8, True, True))
        else:
            board = None
        walk(rng, pos, None, rng.choice([6, 12, 24]), board)
    print('diff_rules seed', seed, 'walks', walks, stats, 'time %.1fs' % (time.time() - t0), 'C-checked' if HAVE_C else 'no-C')
    sys.exit(1 if stats['mism'] else 0)


main()
