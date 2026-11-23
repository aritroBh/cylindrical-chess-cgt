"""T84 independent, eight-rank, count-rule whole-board check. No project imports."""
import argparse
import re
from functools import lru_cache


def start(family, n):
    common = "W6B7 W3 B7 B6 W3 W2 B6 W2".split()
    minimum = dict(M=8, O=9, T=10, S=11, W=11)[family]
    if n < minimum or (n-minimum) % 2 or (family == "W" and n != 11):
        raise ValueError(f"bad width for {family}")
    if family == "M":
        files = ["B4", "W2"] * ((n-8)//2) + "B6 W2 W3 B6 B7 W3 B7 W5".split()
    elif family == "O":
        files = ["B4"] + ["B7", "W5"] * ((n-9)//2) + "B7 W3 B7 B6 W3 W2 B6 W2".split()
    elif family == "T":
        files = ["B4", "W2"] * ((n-10)//2) + ["B5", "W2"] + common
    elif family == "S":
        files = ["B4", "B6", "W3"] + ["W2", "B4"] * ((n-11)//2) + common
    else:
        files = "B4 B7 W4 W6B7 W3 B7 B6 W3 W2 B6 W2".split()  # S6 witness, distinct from S11.
    assert len(files) == n
    masks = [0, 0]
    for f, word in enumerate(files):
        for color, rank in re.findall(r"([WB])([1-8])", word):
            masks[color == 'B'] |= 1 << (f + n*(int(rank)-1))
    assert sum(x.bit_count() for x in masks) == n + (family in "TSW")
    return (*masks, 0)


def check(family, n, heap_max, graph=False):
    row = (1 << n) - 1
    left_edge = sum(1 << (r*n) for r in range(8))
    right_edge = left_edge << (n-1)
    root = start(family, n)

    def neighbors(bits):
        return (((bits & ~right_edge) << 1) | ((bits & right_edge) >> (n-1)) |
                ((bits & ~left_edge) >> 1) | ((bits & left_edge) << (n-1)))

    @lru_cache(131072)
    def covered(enemy, white):
        spread = enemy | neighbors(enemy)
        if white:
            spread >>= n
            for k in (1, 2, 4):
                spread |= spread >> (k*n)
        else:
            spread <<= n
            for k in (1, 2, 4):
                spread |= spread << (k*n)
        return spread

    def terminal(w, b, ep, mover):
        wp = w & ~ep & ~covered(b, True)
        bp = b & ~ep & ~covered(w, False)
        if not wp:
            return 1 if bp else None
        if not bp:
            return 0
        wr = (wp.bit_length()-1)//n + 1
        br = ((bp & -bp).bit_length()-1)//n + 1
        dw, db = 8-wr-(wr == 2), br-1-(br == 7)
        return (1-mover) if dw == db else int(db < dw)

    def children(p, side):
        w, b, ep = p
        own, other = (b, w) if side else (w, b)
        forward = (lambda x: x >> n) if side else (lambda x: x << n)
        occupied = w | b
        ep_target = forward(ep & other)
        steps = ((own >> n) if side else (own << n)) & ~occupied
        for push_count in (0, 1, 2):
            if push_count == 0:
                targets = neighbors(forward(own)) & (other | ep_target)
            elif push_count == 1:
                targets = steps
            else:
                intermediate = steps & (row << (n*(5 if side else 2)))
                targets = forward(intermediate) & ~occupied
            while targets:
                dst = targets & -targets
                targets ^= dst
                back = dst << n if side else dst >> n
                flag, victim = 0, 0
                if push_count == 0:
                    sources = neighbors(back) & own
                    victim = ep if dst == ep_target else dst
                elif push_count == 1:
                    sources = back
                else:
                    sources = back << n if side else back >> n
                    flag = dst if neighbors(dst) & other else 0
                while sources:
                    src = sources & -sources
                    sources ^= src
                    moved, rest = own ^ src ^ dst, other & ~victim
                    yield (rest, moved, flag) if side else (moved, rest, flag)

    if graph:
        zone = 0
        nodes, pending = {root: None}, [root]
        edges = wins = flagged = 0
        while pending:
            p = pending.pop()
            assert terminal(*p, 0) is None
            flagged += bool(p[2])
            zone |= (root[0] ^ p[0]) | (root[1] ^ p[1])
            options = []
            for side in (0, 1):
                has_win, kept = False, []
                for q in children(p, side):
                    result = terminal(*q, side)
                    if result is not None:
                        wins += result == side
                        has_win |= result == side
                    elif not any(terminal(*r, 1-side) == 1-side for r in children(q, 1-side)):
                        edges += 1
                        kept.append(q)
                        if q not in nodes:
                            nodes[q] = None
                            pending.append(q)
                options.append((has_win, frozenset(kept)))
            nodes[p] = options
        files = [f for f in range(n) if zone & (left_edge << f)]
        print(f"{family}{n} nodes={len(nodes)} K={edges} T={wins} flags={flagged} zone={files}", flush=True)
        assert not flagged
        covered.cache_clear()
        return nodes
    else:
        for expire in (False, True):
            @lru_cache(200000)
            def win(w, b, ep, side, h):
                # Search every legal alternative until a winning one is found.
                # Move ordering only: try all direct terminal wins first.
                live = []
                for q in children((w, b, ep), side):
                    winner = terminal(*q, side)
                    if winner == side:
                        return True
                    if winner is None:
                        live.append(q)
                if any(not win(*q, 1-side, h) for q in live):
                    return True
                heap_ep = 0 if expire else ep
                winner = terminal(w, b, heap_ep, side) if heap_ep != ep else None
                if winner is not None:
                    return h > 0 and winner == side
                return any(not win(w, b, heap_ep, 1-side, small) for small in range(h))

            assert terminal(*root, 0) is None
            sig = ''.join({(False, False): 'P', (True, True): 'N',
                           (True, False): 'L', (False, True): 'R'}[
                               (win(*root, 0, h), win(*root, 1, h))] for h in range(heap_max+1))
            print(f"{family}{n} {'expire' if expire else 'keep'} {sig}", flush=True)
            goal = 2 if family in "MO" else 3
            minimum = dict(M=10, O=11, T=12, S=13, W=11)[family]
            if n >= minimum:
                assert sig == ''.join('P' if h == goal else 'N' for h in range(heap_max+1))
            elif heap_max >= goal:
                assert sig[goal] != 'P'
            win.cache_clear()
    covered.cache_clear()


def check_insertion(family, n, cut):
    if not 0 <= cut < n-1:
        raise ValueError("cut must have a right neighbour in this indexing")
    old = check(family, n, 0, graph=True)
    new = check(family, n+2, 0, graph=True)
    row = (1 << n)-1
    left = (1 << (cut+1))-1

    def insert(bits):
        out = 0
        for rank in range(8):
            strip = (bits >> (n*rank)) & row
            copies = (((strip >> (cut+1)) & 1) | (((strip >> cut) & 1) << 1)) << (cut+1)
            out |= ((strip & left) | copies | ((strip & ~left) << 2)) << ((n+2)*rank)
        return out

    image = {p: (insert(p[0]), insert(p[1]), 0) for p in old}  # Graph check asserted no live flag.
    assert image[start(family, n)] == start(family, n+2)
    assert len(old) == len(new) and set(image.values()) == new.keys()
    for p, options in old.items():
        for side, (has_win, children) in enumerate(options):
            assert (has_win, {image[q] for q in children}) == new[image[p]][side]
    print(f"{family}{n}->{n+2} cut={cut} root, bijection, per-side K children and T flags agree", flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('members', nargs='+', help='e.g. M10 O11 T12 S13, or W11 for the separate S6 witness')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--graph', action='store_true', help='count K-reachable nodes, K/T moves and changed files')
    mode.add_argument('--cut', type=int, help='compare the complete reduced graph with the next width at this cut')
    parser.add_argument('--heaps', type=int, help='maximum heap, default 3 for M/O and 4 for T/S')
    args = parser.parse_args()
    for member in args.members:
        match = re.fullmatch(r'([MOTSW])([0-9]+)', member)
        if not match or (args.heaps is not None and not 0 <= args.heaps < 256):
            parser.error('invalid member or heap size')
        family, width = match.groups()
        if args.cut is None:
            check(family, int(width), args.heaps if args.heaps is not None else 3+(family in "TSW"), args.graph)
        else:
            check_insertion(family, int(width), args.cut)
