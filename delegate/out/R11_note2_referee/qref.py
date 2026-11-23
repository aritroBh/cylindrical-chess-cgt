"""Independent referee engine for the Q family (Note 2 of Section S15).

Written from the rules in sections/02_rules.tex and the Model paragraph of
supp/s13.tex only; imports nothing from the repository.

Board: tuple of n strings of length 8 (index r-1 = rank r), chars '.', 'W', 'B'.
Flag: (file, rank) of a pawn that just made a double step and stands beside an
enemy pawn (so it can be taken e.p.), else None.
Race rule "count", e.p.-aware passed test, normal play, G + *h.

usage:
  python3 qref.py full N [N ...]      whole-board search, h=0..4, both heap/e.p. readings
  python3 qref.py reduced N [N ...]   reduced graph (Lemma 1 classes), zone, flags, signature
  python3 qref.py pump N0 N1          check ins_9(R_n) = R_{n+2} for n = N0, N0+2, ..., N1-2
"""
import sys
sys.setrecursionlimit(100000)

W, B = 'W', 'B'
OTHER = {W: B, B: W}


def q_start(n):
    assert n % 2 == 0 and n >= 8
    files = ['W4', 'B7'] + ['B4', 'W2'] * ((n - 8) // 2) + ['W3B6', 'W3', 'W2B5', 'B5', 'W2', 'B4']
    assert len(files) == n
    board = []
    for spec in files:
        s = ['.'] * 8
        i = 0
        while i < len(spec):
            s[int(spec[i + 1]) - 1] = spec[i]
            i += 2
        board.append(''.join(s))
    return tuple(board)


def setsq(board, f, r, ch):
    s = board[f]
    s = s[:r - 1] + ch + s[r:]
    return board[:f] + (s,) + board[f + 1:]


def passed(board, flag, f, r, col):
    n = len(board)
    if flag == (f, r):
        return False  # can be captured e.p. on the opponent's next move
    for g in ((f - 1) % n, f, (f + 1) % n):
        s = board[g]
        if col == W:
            if B in s[r:]:
                return False
        else:
            if W in s[:r - 1]:
                return False
    return True


def dist(col, r):
    if col == W:
        return 8 - r - (1 if r == 2 else 0)
    return r - 1 - (1 if r == 7 else 0)


def best_passer(board, flag, col):
    """min promotion distance over passed pawns of col, or None."""
    best = None
    for f, s in enumerate(board):
        for i, ch in enumerate(s):
            if ch == col and passed(board, flag, f, i + 1, col):
                d = dist(col, i + 1)
                if best is None or d < best:
                    best = d
    return best


def terminal(board, flag, mover):
    """None if neither side has a passed pawn, else the winner."""
    dw = best_passer(board, flag, W)
    db = best_passer(board, flag, B)
    if dw is None and db is None:
        return None
    if db is None:
        return W
    if dw is None:
        return B
    if dw < db:
        return W
    if db < dw:
        return B
    return OTHER[mover]  # tie: side that did not just move


def moves(board, flag, col):
    """list of (child_board, child_flag, touched_files)."""
    n = len(board)
    out = []
    enemy = OTHER[col]
    step = 1 if col == W else -1
    for f, s in enumerate(board):
        for i, ch in enumerate(s):
            if ch != col:
                continue
            r = i + 1
            r1 = r + step
            if not (1 <= r1 <= 8):
                continue
            b0 = setsq(board, f, r, '.')
            # single step
            if s[r1 - 1] == '.':
                out.append((setsq(b0, f, r1, col), None, (f,)))
                # double step
                start = 2 if col == W else 7
                r2 = r + 2 * step
                if r == start and s[r2 - 1] == '.':
                    nb = setsq(b0, f, r2, col)
                    fl = None
                    for g in ((f - 1) % n, (f + 1) % n):
                        if nb[g][r2 - 1] == enemy:
                            fl = (f, r2)
                    out.append((nb, fl, (f,)))
            # captures
            for g in ((f - 1) % n, (f + 1) % n):
                if board[g][r1 - 1] == enemy:
                    nb = setsq(setsq(b0, g, r1, '.'), g, r1, col)
                    out.append((nb, None, (f, g)))
            # en passant: flagged enemy pawn on (g, r) beside us, we land on (g, r1)
            if flag is not None:
                g, fr = flag
                if fr == r and g in ((f - 1) % n, (f + 1) % n) and board[g][fr - 1] == enemy \
                        and board[g][r1 - 1] == '.':
                    nb = setsq(setsq(b0, g, fr, '.'), g, r1, col)
                    out.append((nb, None, (f, g)))
    return out


# ---------------- whole-board search of G + *h ----------------

def solve_full(n, hmax=4, mode='keep'):
    memo = {}

    def win(board, flag, h, side):
        key = (board, flag, h, side)
        v = memo.get(key)
        if v is not None:
            return v
        res = False
        other = OTHER[side]
        for nb, nf, _ in moves(board, flag, side):
            t = terminal(nb, nf, side)
            if t == side:
                res = True
                break
            if t is None and not win(nb, nf, h, other):
                res = True
                break
        if not res:
            for h2 in range(h):
                if mode == 'keep':
                    if not win(board, flag, h2, other):
                        res = True
                        break
                else:  # expire: a heap move clears the flag
                    t = terminal(board, None, side) if flag is not None else None
                    if t == side:
                        res = True
                        break
                    if t is None and not win(board, None, h2, other):
                        res = True
                        break
        memo[key] = res
        return res

    root = q_start(n)
    assert terminal(root, None, B) is None
    sig = ''.join('N' if win(root, None, h, W) and win(root, None, h, B) else
                  ('P' if not win(root, None, h, W) and not win(root, None, h, B) else
                   ('L' if win(root, None, h, W) else 'R')) for h in range(hmax + 1))
    return sig, len(memo)


# ---------------- reduced graph (Lemma 1 classes) ----------------

def classify(board, flag, side):
    """returns (T count, list of K children, counts dict)."""
    other = OTHER[side]
    T = 0
    K = []
    cnt = {'T': 0, 'L': 0, 'P': 0, 'K': 0}
    for nb, nf, _ in moves(board, flag, side):
        t = terminal(nb, nf, side)
        if t == side:
            cnt['T'] += 1
            continue
        if t == other:
            cnt['L'] += 1
            continue
        poisoned = False
        for nb2, nf2, _ in moves(nb, nf, other):
            if terminal(nb2, nf2, other) == other:
                poisoned = True
                break
        if poisoned:
            cnt['P'] += 1
        else:
            cnt['K'] += 1
            K.append((nb, nf))
    return cnt, K


def reduced(n=None, root=None):
    if root is None:
        root = (q_start(n), None)
    nodes = {root: None}
    order = [root]
    i = 0
    info = {}
    while i < len(order):
        p = order[i]
        i += 1
        rec = {}
        for side in (W, B):
            cnt, K = classify(p[0], p[1], side)
            rec[side] = (cnt['T'], K, cnt)
            for c in K:
                if c not in nodes:
                    nodes[c] = None
                    order.append(c)
        info[p] = rec
    return root, order, info


def solve_reduced(root, info, hmax=4):
    memo = {}

    def win(p, h, side):
        key = (p, h, side)
        v = memo.get(key)
        if v is not None:
            return v
        T, K, _ = info[p][side]
        res = T > 0
        if not res:
            for c in K:
                if not win(c, h, OTHER[side]):
                    res = True
                    break
        if not res:
            for h2 in range(h):
                if not win(p, h2, OTHER[side]):
                    res = True
                    break
        memo[key] = res
        return res

    out = ''
    for h in range(hmax + 1):
        a, b = win(root, h, W), win(root, h, B)
        out += 'N' if a and b else 'P' if not a and not b else 'L' if a else 'R'
    return out


def summary(n):
    root, order, info = reduced(n)
    rb = root[0]
    zone = sorted({f for p in order for f in range(n) if p[0][f] != rb[f]})
    flagged = sum(1 for p in order if p[1] is not None)
    passers = sum(1 for p in order if terminal(p[0], p[1], W) is not None or terminal(p[0], p[1], B) is not None)
    Kedges = sum(len(info[p][s][1]) for p in order for s in (W, B))
    Tedges = sum(info[p][s][0] for p in order for s in (W, B))
    sig = solve_reduced(root, info)
    return dict(n=n, nodes=len(order), K=Kedges, T=Tedges, flagged=flagged,
                with_passer=passers, zone=zone, sig=sig), (root, order, info)


def ins(board, c):
    return board[:c + 1] + (board[c + 1], board[c]) + board[c + 1:]


def pump(n0, n1, c=9):
    prev = summary(n0)[1]
    for n in range(n0, n1, 2):
        nxt = summary(n + 2)[1]
        r0, o0, i0 = prev
        r1, o1, i1 = nxt
        ok_root = (ins(r0[0], c), r0[1]) == r1
        img = {p: (ins(p[0], c), None if p[1] is None else (p[1][0] + (2 if p[1][0] > c else 0), p[1][1])) for p in o0}
        ok_nodes = set(img.values()) == set(o1) and len(img) == len(o1)
        ok_edges = True
        for p in o0:
            q = img[p]
            for s in (W, B):
                if i0[p][s][0] != i1[q][s][0]:
                    ok_edges = False
                if sorted(img[c_] for c_ in i0[p][s][1]) != sorted(i1[q][s][1]):
                    ok_edges = False
        print(f'ins_{c}: R_{n} -> R_{n+2}: root {ok_root}, nodes {ok_nodes}, K-edges and T-counts {ok_edges}', flush=True)
        prev = nxt


if __name__ == '__main__':
    import time
    cmd = sys.argv[1]
    if cmd == 'full':
        for a in sys.argv[2:]:
            n = int(a)
            for mode in ('keep', 'expire'):
                t = time.time()
                sig, states = solve_full(n, 4, mode)
                print(f'Q_{n} full mode={mode} sig h=0..4 {sig} states={states} {time.time()-t:.1f}s', flush=True)
    elif cmd == 'reduced':
        for a in sys.argv[2:]:
            t = time.time()
            s, _ = summary(int(a))
            print(s, f'{time.time()-t:.1f}s', flush=True)
    elif cmd == 'pump':
        pump(int(sys.argv[2]), int(sys.argv[3]))
