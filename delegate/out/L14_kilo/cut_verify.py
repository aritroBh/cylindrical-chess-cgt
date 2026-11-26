#!/usr/bin/env python3
"""
Independent verification of the Cut Lemma one-step instances (Part D).
Recomputes from the paper's rules without using any existing solver code.
"""

from functools import lru_cache
from itertools import product
import sys

# ============================================================
# Pawn rules from the paper (cylcgt/pawns.py conventions)
# ============================================================

WHITE = 0
BLACK = 1

class Settings:
    def __init__(self, ep=2, race=0):
        self.ep = ep
        self.race = race
    
    def __eq__(self, other):
        return self.ep == other.ep and self.race == other.race
    
    def __hash__(self):
        return hash((self.ep, self.race))
    
    def __repr__(self):
        ep_names = ['off', 'textbook', 'aware']
        race_names = ['count', 'mover', 'opponent']
        return f"Settings(ep={ep_names[self.ep]}, race={race_names[self.race]})"

all_settings = [
    Settings(0, 0), Settings(0, 1), Settings(0, 2),
    Settings(1, 0), Settings(1, 1), Settings(1, 2),
    Settings(2, 0), Settings(2, 1), Settings(2, 2),
]

class Board:
    def __init__(self, files, ranks, topology='cylinder'):
        self.files = files
        self.ranks = ranks
        self.topology = topology
        self.wrap = (topology == 'cylinder')
    
    def __eq__(self, other):
        return (self.files == other.files and 
                self.ranks == other.ranks and 
                self.topology == other.topology)
    
    def __hash__(self):
        return hash((self.files, self.ranks, self.topology))
    
    def __repr__(self):
        return f"Board({self.files}, {self.ranks}, {self.topology})"

def sort_pawns(pawns):
    return tuple(sorted(pawns, key=lambda p: (p[0], p[1])))

class Position:
    def __init__(self, white, black, ep=None):
        self.white = sort_pawns(white)
        self.black = sort_pawns(black)
        self.ep = ep
    
    def __eq__(self, other):
        return (self.white == other.white and 
                self.black == other.black and 
                self.ep == other.ep)
    
    def __hash__(self):
        return hash((self.white, self.black, self.ep))
    
    def __repr__(self):
        return f"Position(W={self.white}, B={self.black}, ep={self.ep})"
    
    def pawns(self, color):
        return self.white if color == WHITE else self.black
    
    def all_pawns(self):
        return self.white + self.black

def neighbors(board, f):
    if board.wrap:
        return [(f + 1) % board.files, (f - 1) % board.files]
    else:
        res = []
        if f + 1 < board.files:
            res.append(f + 1)
        if f - 1 >= 0:
            res.append(f - 1)
        return res

def fwd_rank(board, side, r):
    if side == WHITE:
        return r + 1 if r + 1 <= board.ranks else None
    else:
        return r - 1 if r - 1 >= 1 else None

def has_pawn(pos, f, r, side):
    if side == WHITE:
        return (f, r, True) in pos.white
    else:
        return (f, r, False) in pos.black

def remove_pawn(pos, f, r, side):
    if side == WHITE:
        new_white = tuple(p for p in pos.white if p != (f, r, True))
        return Position(new_white, pos.black, pos.ep)
    else:
        new_black = tuple(p for p in pos.black if p != (f, r, False))
        return Position(pos.white, new_black, pos.ep)

def add_pawn(pos, f, r, side):
    if side == WHITE:
        new_white = pos.white + ((f, r, True),)
        return Position(new_white, pos.black, pos.ep)
    else:
        new_black = pos.black + ((f, r, False),)
        return Position(pos.white, new_black, pos.ep)

def move_pawn(pos, f1, r1, f2, r2, side):
    pos = remove_pawn(pos, f1, r1, side)
    pos = add_pawn(pos, f2, r2, side)
    return pos

def ep_capturable(board, pos, side, pawn):
    if pos.ep is None:
        return False
    (ep_f, ep_r), ep_color = pos.ep
    if ep_color != side:
        return False
    f, r, _ = pawn
    if board.wrap:
        diff = (f - ep_f) % board.files
        if diff != 1 and diff != board.files - 1:
            return False
    else:
        if abs(f - ep_f) != 1:
            return False
    if side == WHITE:
        return r == ep_r + 1
    else:
        return r == ep_r - 1

def gen_captures(board, pos, side):
    res = []
    pawns = pos.pawns(side)
    enemy = BLACK if side == WHITE else WHITE
    for f, r, _ in pawns:
        r2 = fwd_rank(board, side, r)
        if r2 is None:
            continue
        for g in neighbors(board, f):
            # Regular capture: enemy pawn on (g, r2)
            if has_pawn(pos, g, r2, enemy):
                new_pos = move_pawn(pos, f, r, g, r2, side)
                new_pos = remove_pawn(new_pos, g, r2, enemy)
                new_pos = Position(new_pos.white, new_pos.black, None)
                res.append(new_pos)
            # En passant capture
            if pos.ep is not None:
                (ep_f, ep_r), ep_color = pos.ep
                if ep_color == side and ep_f == g and ep_r == r2:
                    new_pos = move_pawn(pos, f, r, g, r2, side)
                    new_pos = remove_pawn(new_pos, g, r, enemy)
                    new_pos = Position(new_pos.white, new_pos.black, None)
                    res.append(new_pos)
    return res

def gen_pushes(board, pos, side):
    res = []
    pawns = pos.pawns(side)
    for f, r, _ in pawns:
        r2 = fwd_rank(board, side, r)
        if r2 is None:
            continue
        if not has_pawn(pos, f, r2, WHITE) and not has_pawn(pos, f, r2, BLACK):
            new_pos = move_pawn(pos, f, r, f, r2, side)
            ep = None
            if side == WHITE and r == 2 and r2 == 4:
                ep = ((f, 3), BLACK)
            elif side == BLACK and r == 7 and r2 == 5:
                ep = ((f, 6), WHITE)
            new_pos = Position(new_pos.white, new_pos.black, ep)
            res.append(new_pos)
    return res

def gen_moves(board, pos, side):
    caps = gen_captures(board, pos, side)
    if caps:
        return caps
    return gen_pushes(board, pos, side)

def textbook_passed(board, pos, side, pawn):
    f, r, _ = pawn
    if side == WHITE:
        for rf in range(r + 1, board.ranks + 1):
            if has_pawn(pos, f, rf, BLACK):
                return False
            for g in neighbors(board, f):
                if has_pawn(pos, g, rf, BLACK):
                    return False
    else:
        for rf in range(1, r):
            if has_pawn(pos, f, rf, WHITE):
                return False
            for g in neighbors(board, f):
                if has_pawn(pos, g, rf, WHITE):
                    return False
    return True

def passed_pawn(settings, board, pos, side, pawn):
    if settings.ep == 0:
        return textbook_passed(board, pos, side, pawn)
    if settings.ep == 1:
        return textbook_passed(board, pos, side, pawn)
    if not textbook_passed(board, pos, side, pawn):
        return False
    if ep_capturable(board, pos, side, pawn):
        return False
    return True

def has_passed(settings, board, pos, side):
    for pawn in pos.pawns(side):
        if passed_pawn(settings, board, pos, side, pawn):
            return True
    return False

BIG = 256

def classify(settings, board, pos, side):
    w_passed = has_passed(settings, board, pos, WHITE)
    b_passed = has_passed(settings, board, pos, BLACK)
    
    if w_passed and not b_passed:
        return BIG
    if b_passed and not w_passed:
        return -BIG
    if w_passed and b_passed:
        return 0
    return 0

# ============================================================
# Components: split by empty files
# ============================================================

def components_flat(board, pos):
    if board.wrap:
        raise ValueError("Use components_cyl for cylinder")
    
    occupied = set()
    for f, r, c in pos.all_pawns():
        occupied.add(f)
    
    if not occupied:
        return []
    
    comps = []
    current_white = []
    current_black = []
    for f in range(board.files):
        file_white = [p for p in pos.white if p[0] == f]
        file_black = [p for p in pos.black if p[0] == f]
        if file_white or file_black:
            current_white.extend(file_white)
            current_black.extend(file_black)
        else:
            if current_white or current_black:
                comps.append(Position(current_white, current_black, None))
                current_white = []
                current_black = []
    if current_white or current_black:
        comps.append(Position(current_white, current_black, None))
    return comps

def components_cyl(board, pos):
    if not board.wrap:
        raise ValueError("Use components_flat for flat board")
    
    occupied = set()
    for f, r, c in pos.all_pawns():
        occupied.add(f)
    
    if not occupied:
        return []
    
    empty_files = [f for f in range(board.files) if f not in occupied]
    
    if not empty_files:
        return [pos]
    
    comps = []
    for i in range(len(empty_files)):
        e1 = empty_files[i]
        e2 = empty_files[(i + 1) % len(empty_files)]
        
        arc_files = []
        f = (e1 + 1) % board.files
        while f != e2:
            arc_files.append(f)
            f = (f + 1) % board.files
        
        if arc_files:
            comp_white = [p for p in pos.white if p[0] in arc_files]
            comp_black = [p for p in pos.black if p[0] in arc_files]
            if comp_white or comp_black:
                comps.append(Position(comp_white, comp_black, None))
    
    return comps

def components(board, pos):
    if board.wrap:
        return components_cyl(board, pos)
    else:
        return components_flat(board, pos)

# ============================================================
# Cut operation
# ============================================================

def cut_file(n, e, f):
    return (f + n - e - 1) % n

def cut_pawn(n, e, pawn):
    f, r, c = pawn
    return (cut_file(n, e, f), r, c)

def cut_ep(n, e, ep):
    if ep is None:
        return None
    (f, r), color = ep
    return ((cut_file(n, e, f), r), color)

def cut_position(n, e, pos):
    new_white = sort_pawns([cut_pawn(n, e, p) for p in pos.white])
    new_black = sort_pawns([cut_pawn(n, e, p) for p in pos.black])
    new_ep = cut_ep(n, e, pos.ep)
    return Position(new_white, new_black, new_ep)

def normalize(settings, board, pos):
    return Position(pos.white, pos.black, pos.ep)

# ============================================================
# Family generation (FIXED ep position generation)
# ============================================================

def fill_squares(squares, r, k, white_pawns, black_pawns):
    if not squares:
        return [(white_pawns, black_pawns)]
    f, rk = squares[0]
    rest = squares[1:]
    results = fill_squares(rest, r, k, white_pawns, black_pawns)
    if k > 0 and 2 <= rk:
        results += fill_squares(rest, r, k - 1, white_pawns + [(f, rk, True)], black_pawns)
    if k > 0 and rk < r:
        results += fill_squares(rest, r, k - 1, white_pawns, black_pawns + [(f, rk, False)])
    return results

def base_positions(n, r, k, e):
    squares = []
    for f in range(n):
        if f == e:
            continue
        for rk in range(1, r + 1):
            squares.append((f, rk))
    pairs = fill_squares(squares, r, k, [], [])
    return [Position(w, b, None) for w, b in pairs]

def can_have_real_ep(board, pos, pawn):
    """Check if this pawn could have just double-stepped, creating a real ep right"""
    f, r, color = pawn
    if color:  # white
        # White double-steps from rank 2 to 4
        # Pawn must be on rank 4, rank 3 empty, rank 2 had the pawn
        return r == 4 and not has_pawn(pos, f, 3, WHITE) and not has_pawn(pos, f, 3, BLACK)
    else:  # black
        # Black double-steps from rank 7 to 5
        # Pawn must be on rank 5, rank 6 empty, rank 7 had the pawn
        return r == board.ranks - 2 and not has_pawn(pos, f, board.ranks - 1, WHITE) and not has_pawn(pos, f, board.ranks - 1, BLACK)

def family(settings, n, r, k, e):
    bd = Board(n, r, 'cylinder')
    base = base_positions(n, r, k, e)
    result = []
    for P in base:
        result.append(P)
        if settings.ep != 0:
            for pawn in P.all_pawns():
                if can_have_real_ep(bd, P, pawn):
                    f, r_pawn, color = pawn
                    if color:  # white
                        ep = ((f, 3), BLACK)
                    else:  # black
                        ep = ((f, r - 1), WHITE)
                    Q = normalize(settings, bd, Position(P.white, P.black, ep))
                    if Q.ep is not None:
                        result.append(Q)
    return result

# ============================================================
# The step check
# ============================================================

def same_set(a, b):
    return all(x in b for x in a) and all(x in a for x in b)

def step_check(settings, n, r, e, family_set, P):
    cb = Board(n, r, 'cylinder')
    fb = Board(n - 1, r, 'flat')
    cP = cut_position(n, e, P)
    
    # emptyFile e P
    if any(p[0] == e for p in P.all_pawns()):
        return False, "emptyFile failed"
    
    # Position.valid cb P
    for f, rk, c in P.all_pawns():
        if not (0 <= f < n and 1 <= rk <= r):
            return False, "valid cb failed"
    
    # Position.valid fb cP
    for f, rk, c in cP.all_pawns():
        if not (0 <= f < n - 1 and 1 <= rk <= r):
            return False, "valid fb failed"
    
    # normalize s cb P == P
    if normalize(settings, cb, P) != P:
        return False, "normalize cb failed"
    
    # normalize s fb cP == cP
    if normalize(settings, fb, cP) != cP:
        return False, "normalize fb failed"
    
    # components length match
    comps_cb = components(cb, P)
    comps_fb = components(fb, cP)
    if len(comps_cb) != len(comps_fb):
        return False, f"components length mismatch: {len(comps_cb)} vs {len(comps_fb)}"
    
    # cut of components = components of cut
    cut_comps_cb = [cut_position(n, e, c) for c in comps_cb]
    if not same_set(cut_comps_cb, comps_fb):
        print(f"  DEBUG: comps_cb={comps_cb}")
        print(f"  DEBUG: comps_fb={comps_fb}")
        print(f"  DEBUG: cut_comps_cb={cut_comps_cb}")
        return False, "components cut mismatch"
    
    for color in [WHITE, BLACK]:
        # hasPassed agrees
        if has_passed(settings, cb, P, color) != has_passed(settings, fb, cP, color):
            return False, f"hasPassed mismatch for {color}"
        
        # classify agrees
        if classify(settings, cb, P, color) != classify(settings, fb, cP, color):
            return False, f"classify mismatch for {color}"
        
        # epCapturable agrees for every pawn
        for pawn in P.pawns(color):
            cp = cut_pawn(n, e, pawn)
            if ep_capturable(cb, P, color, pawn) != ep_capturable(fb, cP, color, cp):
                return False, f"epCapturable mismatch for {pawn}"
        
        # moves stay in family
        moves_cb = gen_moves(cb, P, color)
        for m in moves_cb:
            if m not in family_set:
                return False, f"move not in family: {m}"
        
        # cut of moves = moves of cut
        moves_fb = gen_moves(fb, cP, color)
        cut_moves_cb = [cut_position(n, e, m) for m in moves_cb]
        if not same_set(cut_moves_cb, moves_fb):
            print(f"  DEBUG moves_cb={moves_cb}")
            print(f"  DEBUG moves_fb={moves_fb}")
            print(f"  DEBUG cut_moves_cb={cut_moves_cb}")
            return False, f"moves cut mismatch for {color}"
    
    return True, "OK"

def fam_check(settings, n, r, k, e):
    F = family(settings, n, r, k, e)
    family_set = set(F)
    for P in F:
        ok, msg = step_check(settings, n, r, e, family_set, P)
        if not ok:
            return False, f"Failed on {P}: {msg}"
    return True, "OK"

def all_check(n, r, k):
    for e in range(n):
        for s in all_settings:
            ok, msg = fam_check(s, n, r, k, e)
            if not ok:
                return False, f"Failed for e={e}, s={s}: {msg}"
    return True, "OK"

# ============================================================
# Run one of the instances
# ============================================================

print("Testing cut_step_3_5_6 (n=3, r=5, k=6)...")
ok, msg = all_check(3, 5, 6)
print(f"Result: {ok}, {msg}")

if ok:
    print("\nTesting cut_step_3_8_4 (n=3, r=8, k=4)...")
    ok, msg = all_check(3, 8, 4)
    print(f"Result: {ok}, {msg}")

print("\nDone.")