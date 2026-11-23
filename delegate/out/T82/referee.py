"""T82. Four bitsets (W up/down, B up/down), plus the capturable stepper's square."""
import argparse
import random
import signal
from functools import cache, lru_cache

WHITE, BLACK = 0, 1
LIVE, TIE = -1, 2
CLEAR = -1


def squares(bits):
    while bits:
        bit = bits & -bits
        yield bit.bit_length() - 1
        bits ^= bit


@cache
def geometry(n, square, down):
    f, r = divmod(square, 8)
    step = -1 if down else 1
    ahead = range(r + step, -1 if down else 8, step)
    straight = sum(1 << (8*f + y) for y in ahead)
    view = straight
    diagonals = []
    for g in (f-1, f+1):
        twist = g < 0 or g >= n
        base = 8*(g % n)
        for y in ahead:
            target = base + (7-y if twist else y)
            view |= 1 << target
            if y == r + step:
                diagonals.append((target, int(twist)))
    return straight, view, tuple(diagonals)


def parse(files):
    masks = [0]*4
    for f, tokens in enumerate(files):
        for side, rank in tokens:
            group = {"W": 0, "w": 1, "B": 3, "b": 2}[side]
            masks[group] |= 1 << (8*f + int(rank)-1)
    return (*masks, CLEAR)


def family(k, m):
    core = "B6 W2 W3 B6 B7 W3".split()
    if k == 3:
        files = core + ["B7", "W5"]*m + ["W6B7"]
    else:
        files = ["B4", "W2"]*m + core + ["B7", "W5"] + ["B7"]*(k == 2)
    return len(files), parse([list(zip(t[::2], t[1::2])) for t in files])


@lru_cache(maxsize=65536)
def terminal(n, p):
    occ = p[0] | p[1] | p[2] | p[3]
    # 10 = absent, 9 = passer but no free promotion lane.
    best = [10, 10]
    for group in range(4):
        side, down = divmod(group, 2)
        enemy = p[2*(1-side)] | p[2*(1-side)+1]
        for s in squares(p[group]):
            straight, view, _ = geometry(n, s, down)
            if s != p[4] and not view & enemy:
                r = s % 8
                gap = r if down else 7-r
                dist = 9 if straight & occ else gap - (gap == 6)
                best[side] = min(best[side], dist)
    if best == [10, 10]:
        return LIVE
    if best[0] == best[1]:
        return TIE
    return int(best[1] < best[0])


def moves(n, p, side):
    """Yield (source, landing, victim or -1, child). Also for a retained heap flag."""
    occ = p[0] | p[1] | p[2] | p[3]
    enemy = 2*(1-side)
    ep = p[4]
    skip = CLEAR
    if ep >= 0:
        for g in (enemy, enemy+1):
            if (1 << ep) & p[g]:
                skip = ep + (1 if g % 2 else -1)
    for group in (2*side, 2*side+1):
        down = group % 2
        step = -1 if down else 1
        for s in squares(p[group]):
            r = s % 8
            if not 0 <= r+step < 8:
                continue
            src = 1 << s
            straight = s + step
            without = list(p[:4])
            without[group] ^= src
            if not occ & (1 << straight):
                child = without.copy()
                child[group] |= 1 << straight
                yield s, straight, CLEAR, (*child, CLEAR)
                if r == (6 if down else 1):
                    dest = s+2*step
                    if not occ & (1 << dest):
                        flag = CLEAR
                        # Reverse each diagonal into the skipped square. A twist
                        # reverses the attacker's direction in the target chart.
                        for back_down in (0, 1):
                            for a, twist in geometry(n, straight, back_down)[2]:
                                attacker = enemy + (1 ^ back_down ^ twist)
                                if p[attacker] & (1 << a):
                                    flag = dest
                        child = without.copy()
                        child[group] |= 1 << dest
                        yield s, dest, CLEAR, (*child, flag)
            for dest, twist in geometry(n, s, down)[2]:
                victim = ep if dest == skip else dest
                bit = 1 << victim
                for g in (enemy, enemy+1):
                    if bit & p[g]:
                        child = without.copy()
                        child[g] ^= bit
                        child[group ^ twist] |= 1 << dest
                        yield s, dest, victim, (*child, CLEAR)


def win_at_end(verdict, mover):
    return verdict == mover   # a tied race goes to the opponent of the mover


def classify(n, p, side):
    kept, wins = [], 0
    for _, _, _, q in moves(n, p, side):
        t = terminal(n, q)
        if t != LIVE:
            wins += win_at_end(t, side)
        elif not any(win_at_end(terminal(n, r), 1-side)
                     for _, _, _, r in moves(n, q, 1-side)):
            kept.append(q)
    return kept, wins


def signature(win, hmax):
    return "".join("PLRN"[int(win(WHITE, h)) + 2*int(win(BLACK, h))] for h in range(hmax+1))


def reduced(k, m):
    n, root = family(k, m)
    todo, graph, zone = [root], {}, set()
    edges = threats = flagged = passed = 0
    while todo:
        p = todo.pop()
        if p in graph:
            continue
        flagged += p[4] >= 0
        passed += terminal(n, p) != LIVE
        for i in range(4):
            zone.update(s // 8 for s in squares(p[i] ^ root[i]))
        pair = tuple(classify(n, p, side) for side in (WHITE, BLACK))
        graph[p] = pair
        for children, wins in pair:
            edges += len(children)
            threats += wins
            todo.extend(children)

    @cache
    def win(p, side, h):
        children, wins = graph[p][side]
        return bool(wins or any(not win(q, 1-side, h) for q in children)
                    or any(not win(p, 1-side, j) for j in range(h)))

    sig = signature(lambda s, h: win(root, s, h), 4)
    win.cache_clear()
    return (len(graph), edges, threats, flagged, passed, sorted(zone), sig)


def full(k, m):
    n, root = family(k, m)
    assert terminal(n, root) == LIVE

    @lru_cache(maxsize=65536)
    def options(p, side):
        live = []
        for _, _, _, q in moves(n, p, side):
            t = terminal(n, q)
            if win_at_end(t, side):
                return True, ()
            if t == LIVE:
                live.append(q)
        return False, tuple(live)

    @lru_cache(maxsize=65536)
    def win(p, side, h):
        immediate, live = options(p, side)
        return (immediate or any(not win(p, 1-side, j) for j in range(h))
                or any(not win(q, 1-side, h) for q in live))

    sig = signature(lambda s, h: win(root, s, h), 3)
    win.cache_clear()
    options.cache_clear()
    return sig


def insert(p, c):
    boundary = 8*(c+1)
    low = (1 << boundary)-1
    def grow(bits):
        left = bits & low
        right = bits & ~low
        copies = ((bits >> boundary) & 255) | (((bits >> (boundary-8)) & 255) << 8)
        return left | (copies << boundary) | (right << 16)
    ep = p[4]
    return (*map(grow, p[:4]), ep + 16 if ep >= boundary else ep)


def tokens(n, p):
    out = []
    for f in range(n):
        pieces = (letter+str(s%8+1) for g, letter in enumerate("WwbB")
                  for s in squares(p[g] & (255 << (8*f))))
        out.append("".join(pieces) or "-")
    return " ".join(out)


def attack(width, count, seed, unrestricted_cut):
    rng = random.Random(seed)
    accepted = set()
    seam_boards = set()
    seam = touching = bad = 0
    # Each accepted board is distinct (including its cut).
    span = width if unrestricted_cut else 10
    while len(accepted) < count:
        n = rng.randrange(max(10, span), span+8)
        chart = rng.choice((0, n-span, rng.randrange(n-span+1)))
        start = chart + (span-width)//2
        c = start + width//2-1
        wall = rng.choice((("W2","B4"), ("B4","W2"), ("B7","W5"), ("W5","B7")))
        files = []
        for f in range(n):
            if start <= f < start+width:
                files.append([wall[(f-start)%2]])
            else:
                ranks = rng.sample(range(2,8), rng.choice((0,1,1,2,2,3)))
                files.append([(rng.choice("WwbB"), r) for r in ranks])
        p = parse(files)
        if (n,c,p) in accepted or terminal(n, p) != LIVE:
            continue
        accepted.add((n,c,p))
        touching += chart == 0 or chart+span == n
        if any(abs(s//8 - t//8) == n-1 for side in (0,1)
               for s,t,_,_ in moves(n,p,side)):
            seam += 1
            seam_boards.add((n,p))
        q = insert(p, c)
        problems = []
        for side in (0,1):
            old, ot = classify(n, p, side)
            new, nt = classify(n+2, q, side)
            expected = {insert(child,c) for child in old}
            got = set(new)
            if expected != got or bool(ot) != bool(nt):
                missing = expected - got
                lost_moves = [(s//8, s%8+1, t//8, t%8+1)
                              for s,t,_,child in moves(n,p,side)
                              if child in old and insert(child,c) in missing]
                problems.append((side,len(missing),len(got-expected),bool(ot),bool(nt),lost_moves))
        if problems:
            bad += 1
            print("failure", width, len(accepted), n, c, tokens(n,p), problems, flush=True)
    board_count = len({(n,p) for n,_,p in accepted})
    return width, count, seam, touching, bad, board_count, len(seam_boards)


def selfcheck():
    # A reversed black pawn double-steps up. White sees the skipped square
    # as rank 6 and captures across the seam, arriving on rank 3 facing down.
    n = 5
    p = parse([["b2"], [], [], [], ["W5"]])
    child = next(q for s,t,_,q in moves(n,p,BLACK) if (s,t)==(1,3))
    assert child[4] == 3
    cap = next(q for s,t,v,q in moves(n,child,WHITE) if (s,t,v)==(36,2,3))
    assert cap == parse([["w3"], [], [], [], []])
    assert all(v != 3 for _,_,v,_ in moves(n,child,BLACK))
    assert terminal(n,parse([["W3"],[],[],["B6"],[]])) == TIE
    assert not win_at_end(TIE,WHITE) and not win_at_end(TIE,BLACK)
    # Two separate E walls that meet out of phase are insufficient for V.
    split = parse([["B4"], ["W2"], ["W2"], ["B4"]])
    assert terminal(4, split) == LIVE and terminal(6, insert(split, 1)) == WHITE


if __name__ == "__main__":
    signal.alarm(44*60)
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest="mode", required=True)
    for name in ("reduced", "full"):
        sub = subs.add_parser(name)
        sub.add_argument("first",type=int)
        sub.add_argument("last",type=int)
    sub = subs.add_parser("attack")
    sub.add_argument("width", type=int, choices=(4,6,10))
    sub.add_argument("count", type=int)
    sub.add_argument("seed", type=int)
    sub.add_argument("--unrestricted-cut", action="store_true")
    subs.add_parser("selfcheck")
    args = parser.parse_args()
    selfcheck()
    if args.mode == "attack":
        print("width samples seam_possible touching failures distinct_boards seam_boards", *attack(args.width,args.count,args.seed,args.unrestricted_cut))
    elif args.mode != "selfcheck":
        run = reduced if args.mode == "reduced" else full
        for m in range(args.first,args.last+1):
            for k in range(1,4):
                print(f"F{k} m={m}", run(k,m), flush=True)
