#!/usr/bin/env python3
"""
Independent solver for L12 cold read.
Written from the paper's rules (02_rules.tex §2.1-2.5, 05_sums.tex §5),
NOT from cylcgt/ or any existing solver in the repository.

Checks three claims:
  L4: Positions A and B are *2 in the default setting; not *2 with e.p. off
      or under the opponent rule.
  L5: W a2 b2 b3 / B a5 a6 b6 is 1/8 in all nine settings and for every
      race assignment.
  L6: X = W b2 d4 g3 h5 / B a7 c7 f7 g4 on C8, ep off, count rule:
      S(X) is a Black win; W(X) is a first-player win.
"""

import sys
from functools import lru_cache
from itertools import product

BIG = 256

# ─── Board ───

class Board:
    def __init__(self, files, ranks=8, topology='flat'):
        self.files = files
        self.ranks = ranks
        self.topology = topology  # 'flat' or 'cylinder'

    def on_board(self, r):
        return 1 <= r <= self.ranks

    def beside(self, f, right):
        """Return (neighbor_file, mirrored) or None."""
        if right:
            if f + 1 < self.files:
                return (f + 1, False)
            else:
                if self.topology == 'flat':
                    return None
                elif self.topology == 'cylinder':
                    return (0, False)
        else:
            if f > 0:
                return (f - 1, False)
            else:
                if self.topology == 'flat':
                    return None
                elif self.topology == 'cylinder':
                    return (self.files - 1, False)

    def home_rank(self, up):
        return 2 if up else self.ranks - 1

    def distance(self, pawn):
        """Moves to promote, double step counted as one."""
        f, r, up = pawn
        d = (self.ranks - r) if up else (r - 1)
        if r == self.home_rank(up) and d >= 2:
            d -= 1
        return d


FLAT8 = Board(8, 8, 'flat')
CYL8 = Board(8, 8, 'cylinder')


# ─── Pawn representation ───
# pawn = (file, rank, up)
# position = (white_pawns_tuple, black_pawns_tuple, ep_square_or_None)
# ep_square = (file, rank)  -- the square of the pawn that can be taken

def ahead(up, r):
    return r + 1 if up else r - 1

def is_ahead(up, r, s):
    return r < s if up else s < r

def capture_to(board, pawn, right):
    """Where does pawn land if it captures to the right/left?"""
    f, r, up = pawn
    nb = board.beside(f, right)
    if nb is None:
        return None
    g, flip = nb
    r1 = ahead(up, r)
    if not board.on_board(r1):
        return None
    if flip:
        return (g, board.ranks + 1 - r1, not up)
    return (g, r1, up)

def capture_targets(board, pawn):
    targets = []
    for right in [True, False]:
        t = capture_to(board, pawn, right)
        if t is not None:
            targets.append(t)
    return targets

def sq(pawn):
    return (pawn[0], pawn[1])

def ep_captures(board, pos, color, victim_pawn):
    """Find all (capturer, capturer_after) for ep capture of victim_pawn owned by color."""
    _, _, v_up = victim_pawn
    skipped = (victim_pawn[0], ahead(not v_up, victim_pawn[1]))
    enemy_color = 1 - color
    enemy_pawns = pos[enemy_color]
    results = []
    for q in enemy_pawns:
        for t in capture_targets(board, q):
            if sq(t) == skipped:
                results.append((q, t))
    return results

def normalize(settings, board, pos):
    """Sort pawns, validate ep."""
    wp = tuple(sorted(pos[0]))
    bp = tuple(sorted(pos[1]))
    ep = pos[2]
    base = (wp, bp, None)
    if ep is not None:
        # Find the pawn at ep
        pawn_at_ep = None
        pawn_color = None
        for p in wp:
            if sq(p) == ep:
                pawn_at_ep = p
                pawn_color = 0
                break
        if pawn_at_ep is None:
            for p in bp:
                if sq(p) == ep:
                    pawn_at_ep = p
                    pawn_color = 1
                    break
        if pawn_at_ep is not None and settings['ep'] != 'off':
            f, r, up = pawn_at_ep
            home = board.home_rank(up)
            two_ahead = ahead(up, ahead(up, home))
            one_ahead = ahead(up, home)
            all_sqs = set(sq(p) for p in wp + bp)
            if (r == two_ahead
                and (f, one_ahead) not in all_sqs
                and (f, home) not in all_sqs
                and len(ep_captures(board, base, pawn_color, pawn_at_ep)) > 0):
                return (wp, bp, ep)
    return (wp, bp, None)


# ─── Move generation ───

def all_squares(pos):
    return set(sq(p) for p in pos[0] + pos[1])

def build_pos(color, mine, theirs, ep):
    mine_sorted = tuple(sorted(mine))
    theirs_sorted = tuple(sorted(theirs))
    if color == 0:
        return (mine_sorted, theirs_sorted, ep)
    else:
        return (theirs_sorted, mine_sorted, ep)

def step_moves(board, pos, color, pawn):
    f, r, up = pawn
    r1 = ahead(up, r)
    if board.on_board(r1) and (f, r1) not in all_squares(pos):
        new_pawn = (f, r1, up)
        mine = tuple(new_pawn if p == pawn else p for p in pos[color])
        return [build_pos(color, mine, pos[1-color], None)]
    return []

def double_step_moves(settings, board, pos, color, pawn):
    f, r, up = pawn
    if r != board.home_rank(up):
        return []
    r1 = ahead(up, r)
    r2 = ahead(up, r1)
    occ = all_squares(pos)
    if not board.on_board(r1) or not board.on_board(r2):
        return []
    if (f, r1) in occ or (f, r2) in occ:
        return []
    new_pawn = (f, r2, up)
    mine = tuple(new_pawn if p == pawn else p for p in pos[color])
    after = build_pos(color, mine, pos[1-color], None)
    ep_sq = None
    if settings['ep'] != 'off':
        if len(ep_captures(board, after, color, new_pawn)) > 0:
            ep_sq = sq(new_pawn)
    return [build_pos(color, mine, pos[1-color], ep_sq)]

def capture_moves(board, pos, color, pawn):
    theirs = pos[1-color]
    results = []
    for t in capture_targets(board, pawn):
        for q in theirs:
            if sq(q) == sq(t):
                new_mine = tuple(t if p == pawn else p for p in pos[color])
                new_theirs = tuple(p for p in theirs if p != q)
                results.append(build_pos(color, new_mine, new_theirs, None))
                break
    return results

def ep_moves(settings, board, pos, color, pawn):
    if settings['ep'] == 'off' or pos[2] is None:
        return []
    ep_square = pos[2]
    theirs = pos[1-color]
    victim = None
    for q in theirs:
        if sq(q) == ep_square:
            victim = q
            break
    if victim is None:
        return []
    # The captures available for the opponent color (= 1-color), from victim owned by 1-color
    pairs = ep_captures(board, pos, 1-color, victim)
    results = []
    for capturer, capturer_after in pairs:
        if capturer == pawn:
            new_mine = tuple(capturer_after if p == pawn else p for p in pos[color])
            new_theirs = tuple(p for p in theirs if p != victim)
            results.append(build_pos(color, new_mine, new_theirs, None))
    return results

def moves(settings, board, pos, color):
    """All positions color can reach in one move, deduplicated."""
    result = []
    seen = set()
    for pawn in pos[color]:
        for m in (step_moves(board, pos, color, pawn)
                  + double_step_moves(settings, board, pos, color, pawn)
                  + capture_moves(board, pos, color, pawn)
                  + ep_moves(settings, board, pos, color, pawn)):
            key = m
            if key not in seen:
                seen.add(key)
                result.append(m)
    return result


# ─── Passed pawn test ───

def blocks(board, p, q):
    """Does enemy pawn q block pawn p?"""
    pf, pr, pup = p
    qf, qr, qup = q
    if qf == pf and is_ahead(pup, pr, qr):
        return True
    for right in [True, False]:
        nb = board.beside(pf, right)
        if nb is not None:
            g, flip = nb
            if qf == g:
                qr2 = (board.ranks + 1 - qr) if flip else qr
                if is_ahead(pup, pr, qr2):
                    return True
    return False

def textbook_passed(board, pos, color, pawn):
    enemy = pos[1-color]
    return all(not blocks(board, pawn, q) for q in enemy)

def ep_capturable(board, pos, color, pawn):
    """Can pawn of color be captured ep on the next move?"""
    if pos[2] != sq(pawn):
        return False
    return len(ep_captures(board, pos, color, pawn)) > 0

def passed(settings, board, pos, color, pawn):
    if not textbook_passed(board, pos, color, pawn):
        return False
    if settings['ep'] == 'aware' and ep_capturable(board, pos, color, pawn):
        return False
    return True

def has_passed(settings, board, pos, color):
    return any(passed(settings, board, pos, color, p) for p in pos[color])


# ─── Race winner ───

def is_front(pos, pawn):
    f, r, up = pawn
    for p in pos[0] + pos[1]:
        if p[0] == f and is_ahead(up, r, p[1]):
            return False
    return True

def race_distance(settings, board, pos, color):
    dists = []
    for p in pos[color]:
        if passed(settings, board, pos, color, p) and is_front(pos, p):
            dists.append(board.distance(p))
    return min(dists) if dists else None

def race_winner(settings, board, pos, mover):
    if settings['race'] == 'mover':
        return mover
    if settings['race'] == 'opponent':
        return 1 - mover
    # count
    d_mover = race_distance(settings, board, pos, mover)
    d_other = race_distance(settings, board, pos, 1 - mover)
    # other <= mover (with None = infinity)
    def le_inf(a, b):
        if b is None:
            return True
        if a is None:
            return False
        return a <= b
    if le_inf(d_other, d_mover):
        return 1 - mover
    return mover


# ─── Components ───

def components(board, pos):
    """Split position into components along empty files."""
    all_pawns = pos[0] + pos[1]
    occ = sorted(set(p[0] for p in all_pawns))
    if not occ:
        return []

    # Group into runs of consecutive files
    groups = []
    current = [occ[0]]
    for f in occ[1:]:
        if f == current[-1] + 1:
            current.append(f)
        else:
            groups.append(current)
            current = [f]
    groups.append(current)

    # On cylinder: merge first and last if they wrap
    if board.topology != 'flat' and len(groups) > 1:
        if groups[0][0] == 0 and groups[-1][-1] == board.files - 1:
            merged = groups[-1] + groups[0]
            groups = [merged] + groups[1:-1]

    result = []
    for g in groups:
        gset = set(g)
        wp = tuple(p for p in pos[0] if p[0] in gset)
        bp = tuple(p for p in pos[1] if p[0] in gset)
        ep = pos[2] if (pos[2] is not None and pos[2][0] in gset) else None
        result.append((wp, bp, ep))
    return result


# ─── Game trees ───

class Tree:
    """A finite combinatorial game tree."""
    def __init__(self, left, right):
        self.left = tuple(left)   # Left (White) options
        self.right = tuple(right) # Right (Black) options

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash((self.left, self.right))

    def neg(self):
        return Tree([t.neg() for t in self.right], [t.neg() for t in self.left])

ZERO = Tree([], [])

def star(k):
    if k == 0:
        return ZERO
    opts = [star(i) for i in range(k)]
    return Tree(opts, opts)

def dy(k):
    """Dyadic 1/2^k: dy(0)=1, dy(1)=1/2, dy(2)=1/4, dy(3)=1/8."""
    if k == 0:
        return Tree([ZERO], [])
    return Tree([ZERO], [dy(k-1)])

STAR2 = star(2)
EIGHTH = dy(3)


# ─── Component representation for sums ───
# comp = ('pawns', pos) | ('num', n) | ('tree', tree)

def comp_options(env, color, comp):
    """Options for a component; each option is a list of comps, or None (undefined race)."""
    settings, board = env['settings'], env['board']
    big = env.get('big', BIG)
    race_fn = env.get('race_fn', None)

    kind = comp[0]
    if kind == 'num':
        n = comp[1]
        if color == 0:  # White
            if n > 0:
                return [[('num', n - 1)]]
            return []
        else:
            if n < 0:
                return [[('num', n + 1)]]
            return []
    elif kind == 'tree':
        t = comp[1]
        opts = t.left if color == 0 else t.right
        return [[('tree', o)] for o in opts]
    elif kind == 'pawns':
        pos = comp[1]
        mvs = moves(settings, board, pos, color)
        result = []
        for q in mvs:
            hp_w = has_passed(settings, board, q, 0)
            hp_b = has_passed(settings, board, q, 1)
            if not hp_w and not hp_b:
                comps = components(board, q)
                result.append([('pawns', c) for c in comps])
            elif hp_w and not hp_b:
                result.append([('num', big)])
            elif not hp_w and hp_b:
                result.append([('num', -big)])
            else:
                # Race
                if race_fn is not None:
                    winner = race_fn(q, color)
                else:
                    winner = race_winner(settings, board, q, color)
                if winner is None:
                    result.append(None)  # undefined
                elif winner == 0:
                    result.append([('num', big)])
                else:
                    result.append([('num', -big)])
        return result

def sum_options(env, color, comps):
    """All options in a sum: choose one component and move in it."""
    result = []
    for i, comp in enumerate(comps):
        opts = comp_options(env, color, comp)
        for opt in opts:
            if opt is None:
                result.append(None)
            else:
                result.append(list(comps[:i]) + opt + list(comps[i+1:]))
    return result


# ─── Game outcome (with memoization) ───

def game_wins(env, fuel, comps_tuple, color, memo=None):
    """Does color win the sum of comps? Returns True/False/None."""
    if fuel <= 0:
        return None
    if memo is None:
        memo = {}

    # Normalize: merge integers, drop zeros
    comps = list(comps_tuple)
    num_total = 0
    rest = []
    for c in comps:
        if c[0] == 'num':
            num_total += c[1]
        elif c[0] == 'tree' and c[1] == ZERO:
            pass
        else:
            rest.append(c)
    if num_total != 0:
        rest.append(('num', num_total))
    comps = rest
    comps_key = (tuple(sorted(comps, key=str)), color)

    if comps_key in memo:
        v = memo[comps_key]
        if v is not None:
            return v

    opts = sum_options(env, color, comps)
    result = False  # assume loss unless we find a win
    unknown = False
    for opt in opts:
        if opt is None:
            unknown = True
            continue
        r = game_wins(env, fuel - 1, tuple(opt), 1 - color, memo)
        if r is None:
            unknown = True
        elif r is False:
            # Opponent loses, so we win
            result = True
            break

    if result:
        memo[comps_key] = True
        return True
    elif unknown:
        return None
    else:
        memo[comps_key] = False
        return False


def outcome_fn(env, fuel, pos, tree, color):
    """Does color win pos + tree?"""
    comps = [('pawns', c) for c in components(env['board'], pos)]
    comps.append(('tree', tree))
    memo = {}
    return game_wins(env, fuel, tuple(comps), color, memo)


def is_value(env, fuel, pos, v):
    """X has value v iff both sides lose in X + (-v)."""
    settings, board = env['settings'], env['board']
    if has_passed(settings, board, pos, 0) or has_passed(settings, board, pos, 1):
        return False
    r_w = outcome_fn(env, fuel, pos, v.neg(), 0)
    r_b = outcome_fn(env, fuel, pos, v.neg(), 1)
    return r_w == False and r_b == False


def not_value(env, fuel, pos, v):
    """X does not have value v: some side wins X + (-v)."""
    settings, board = env['settings'], env['board']
    r_w = outcome_fn(env, fuel, pos, v.neg(), 0)
    r_b = outcome_fn(env, fuel, pos, v.neg(), 1)
    return r_w == True or r_b == True


# ─── W(X): whole-board game ───

def W_wins(env, fuel, pos, color, memo=None):
    """Does color win the whole-board game? First passed pawn ends the game."""
    if fuel <= 0:
        return None
    if memo is None:
        memo = {}
    key = (pos, color)
    if key in memo:
        return memo[key]

    settings, board = env['settings'], env['board']
    race_fn = env.get('race_fn', None)
    mvs = moves(settings, board, pos, color)
    if not mvs:
        memo[key] = False
        return False  # no moves = loss

    result = False
    unknown = False
    for q in mvs:
        hp_w = has_passed(settings, board, q, 0)
        hp_b = has_passed(settings, board, q, 1)
        if not hp_w and not hp_b:
            r = W_wins(env, fuel - 1, q, 1 - color, memo)
            if r is None:
                unknown = True
            elif r is False:
                result = True
                break
        elif hp_w and not hp_b:
            if color == 0:
                result = True
                break
            # else this move is bad for black
        elif not hp_w and hp_b:
            if color == 1:
                result = True
                break
            # else bad for white
        else:
            # Race
            if race_fn is not None:
                winner = race_fn(q, color)
            else:
                winner = race_winner(settings, board, q, color)
            if winner is None:
                unknown = True
            elif winner == color:
                result = True
                break

    if result:
        memo[key] = True
        return True
    elif unknown:
        return None
    else:
        memo[key] = False
        return False


# ─── S(X): sum model ───

def S_wins(env, fuel, pos, color):
    """Does color win the sum model of pos?"""
    comps = [('pawns', c) for c in components(env['board'], pos)]
    memo = {}
    return game_wins(env, fuel, tuple(comps), color, memo)


# ─── Position constructors ───

def make_pos(white_squares, black_squares, ep=None):
    """Create a position from lists of (file, rank) squares.
       White pawns move up, black pawns move down."""
    wp = tuple(sorted((f, r, True) for f, r in white_squares))
    bp = tuple(sorted((f, r, False) for f, r in black_squares))
    return (wp, bp, ep)

def sqr(letter, rank):
    return (ord(letter) - ord('a'), rank)


# ─── Define positions ───

# L4: Position A: W a4 b3 d2 d3 / B a7 b7 c5
posA = make_pos([sqr('a',4), sqr('b',3), sqr('d',2), sqr('d',3)],
                [sqr('a',7), sqr('b',7), sqr('c',5)])

# L4: Position B: W b4 c2 d2 / B a6 a7 c6 d5
posB = make_pos([sqr('b',4), sqr('c',2), sqr('d',2)],
                [sqr('a',6), sqr('a',7), sqr('c',6), sqr('d',5)])

# L5: W a2 b2 b3 / B a5 a6 b6
posG = make_pos([sqr('a',2), sqr('b',2), sqr('b',3)],
                [sqr('a',5), sqr('a',6), sqr('b',6)])

# L6: W b2 d4 g3 h5 / B a7 c7 f7 g4 on C8
posX = make_pos([sqr('b',2), sqr('d',4), sqr('g',3), sqr('h',5)],
                [sqr('a',7), sqr('c',7), sqr('f',7), sqr('g',4)])


# ─── Environments ───

def make_env(ep_rule, race_rule, board, big=BIG, race_fn=None):
    return {
        'settings': {'ep': ep_rule, 'race': race_rule},
        'board': board,
        'big': big,
        'race_fn': race_fn,
    }

DEFAULT_ENV = make_env('aware', 'count', FLAT8)
FUEL = 400

ALL_SETTINGS = list(product(['aware', 'textbook', 'off'],
                             ['count', 'mover', 'opponent']))


# ─── Run checks ───

def check_L4():
    print("=" * 60)
    print("L4: Positions A and B, value *2")
    print("=" * 60)

    # Default setting: should be *2
    env = DEFAULT_ENV
    print(f"\nDefault (aware, count):")
    r = is_value(env, FUEL, posA, STAR2)
    print(f"  posA = *2: {r}")
    r = is_value(env, FUEL, posB, STAR2)
    print(f"  posB = *2: {r}")

    # Not *2 with ep off, any race rule
    for race in ['count', 'mover', 'opponent']:
        env = make_env('off', race, FLAT8)
        rA = not_value(env, FUEL, posA, STAR2)
        rB = not_value(env, FUEL, posB, STAR2)
        print(f"  ep off, {race}: posA not *2: {rA}, posB not *2: {rB}")

    # Not *2 under opponent, any ep
    for ep in ['aware', 'textbook', 'off']:
        env = make_env(ep, 'opponent', FLAT8)
        rA = not_value(env, FUEL, posA, STAR2)
        rB = not_value(env, FUEL, posB, STAR2)
        print(f"  {ep}, opponent: posA not *2: {rA}, posB not *2: {rB}")

    # Extra: *2 in (aware,mover), (textbook,count), (textbook,mover)
    for ep, race in [('aware','mover'), ('textbook','count'), ('textbook','mover')]:
        env = make_env(ep, race, FLAT8)
        rA = is_value(env, FUEL, posA, STAR2)
        rB = is_value(env, FUEL, posB, STAR2)
        print(f"  {ep}, {race}: posA = *2: {rA}, posB = *2: {rB}")


def check_L5():
    print("\n" + "=" * 60)
    print("L5: posG = 1/8 in all nine settings")
    print("=" * 60)

    for ep, race in ALL_SETTINGS:
        env = make_env(ep, race, FLAT8)
        r = is_value(env, FUEL, posG, EIGHTH)
        print(f"  ({ep}, {race}): 1/8 = {r}")


def find_race_positions(settings, board, pos, fuel=10000):
    """Find all (race_position, mover_color) reachable from the game tree."""
    races = set()
    seen = set()
    queue = []
    for c in components(board, pos):
        queue.append(c)

    while queue and fuel > 0:
        fuel -= 1
        p = queue.pop(0)
        if p in seen:
            continue
        seen.add(p)
        for color in [0, 1]:
            for q in moves(settings, board, p, color):
                hp_w = has_passed(settings, board, q, 0)
                hp_b = has_passed(settings, board, q, 1)
                if hp_w and hp_b:
                    races.add((q, color))
                elif not hp_w and not hp_b:
                    for c in components(board, q):
                        if c not in seen:
                            queue.append(c)
    return races


def check_L5_all_assignments():
    print("\n  Checking all race assignments...")
    for ep in ['aware', 'textbook', 'off']:
        settings = {'ep': ep, 'race': 'count'}
        races = find_race_positions(settings, FLAT8, posG)
        race_list = sorted(races, key=lambda x: (str(x[0]), x[1]))
        k = len(race_list)
        print(f"  ep={ep}: {k} race positions, checking 2^{k} = {2**k} assignments")

        all_ok = True
        for bits in range(2**k):
            race_table = {}
            for i, (rp, mc) in enumerate(race_list):
                winner = 0 if (bits >> i) & 1 else 1
                race_table[(rp, mc)] = winner

            def race_fn(pos, mover):
                key = (pos, mover)
                return race_table.get(key, None)

            env = make_env(ep, 'count', FLAT8, race_fn=race_fn)
            r = is_value(env, FUEL, posG, EIGHTH)
            if not r:
                all_ok = False
                print(f"    FAILED for bits={bits:0{k}b}")
                break

        print(f"    All assignments: {'PASS' if all_ok else 'FAIL'}")


def check_L6():
    print("\n" + "=" * 60)
    print("L6: posX on C8, ep off, count rule")
    print("=" * 60)

    env = make_env('off', 'count', CYL8)

    # Check it's a single component
    comps = components(CYL8, posX)
    print(f"  Components: {len(comps)}")
    print(f"  Has passed W: {has_passed(env['settings'], CYL8, posX, 0)}")
    print(f"  Has passed B: {has_passed(env['settings'], CYL8, posX, 1)}")

    # W(X): first-player win
    memo_w = {}
    w_white = W_wins(env, FUEL, posX, 0, memo_w)
    memo_b = {}
    w_black = W_wins(env, FUEL, posX, 1, memo_b)
    print(f"  W(X), White to move wins: {w_white}")
    print(f"  W(X), Black to move wins: {w_black}")
    print(f"  W(X) is first-player win: {w_white == True and w_black == True}")

    # S(X): Black wins whoever starts
    s_white = S_wins(env, FUEL, posX, 0)
    s_black = S_wins(env, FUEL, posX, 1)
    print(f"  S(X), White to move wins: {s_white}")
    print(f"  S(X), Black to move wins: {s_black}")
    print(f"  S(X) is Black win: {s_white == False and s_black == True}")


if __name__ == '__main__':
    print("Independent solver for L12 cold read")
    print("Written from the paper's rules, not from cylcgt/ or any repo solver.\n")

    check_L4()
    check_L5()
    check_L5_all_assignments()
    check_L6()

    print("\n" + "=" * 60)
    print("Done.")
