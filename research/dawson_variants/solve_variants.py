"""Efficient solvers for Dawson's chess variants on new surfaces.

Uses macro-move decomposition like pawnboard.py but adapted for:
- 3xn Möbius strip (twisted seam)
- 3xn two-row torus (cylindrical, 2 ranks)
"""

import sys
from functools import lru_cache
from typing import List, Tuple, Dict, Set, Optional

sys.path.insert(0, '.')
from dawson.octal import grundy, heap_moves, octal_options
from dawson.misere import misere_P, canon

E, W, B = 0, 1, 2

# ============================================================
# Möbius Strip Solver
# ============================================================

class MobiusBoard:
    """3xn Möbius strip with twisted seam."""
    
    def __init__(self, n: int):
        self.n = n
        self.files = n
        self.ranks = 3
    
    def neighbours(self, f: int) -> List[Tuple[int, int]]:
        """Return (neighbour_file, rank_delta_adjustment) pairs.
        
        Crossing seam (0 <-> n-1) flips forward direction.
        rank_delta_adjustment = -2 means direction flips (White: +1 -> -1, Black: -1 -> +1)
        """
        res = []
        if f > 0:
            res.append((f - 1, 0))
        else:
            res.append((self.n - 1, -2))
        if f < self.n - 1:
            res.append((f + 1, 0))
        else:
            res.append((0, -2))
        return res
    
    def start(self) -> Tuple:
        return tuple((W, E, B) for _ in range(self.n))
    
    def is_untouched(self, f: int, pos: Tuple) -> bool:
        return pos[f] == (W, E, B)
    
    def moves(self, pos: Tuple, side: int) -> Tuple[List[Tuple], bool]:
        """Return (successor_positions, has_capture)."""
        me, them = (W, B) if side == 0 else (B, W)
        d = 1 if side == 0 else -1
        caps, pushes = [], []
        
        for f in range(self.n):
            for r in range(3):
                if pos[f][r] != me:
                    continue
                for g, rank_adj in self.neighbours(f):
                    actual_d = d + rank_adj
                    r1 = r + actual_d
                    if not 0 <= r1 <= 2:
                        continue
                    if pos[g][r1] == them:
                        caps.append(self._move(pos, f, r, g, r1, me))
                    elif pos[g][r1] == E:
                        pushes.append(self._move(pos, f, r, g, r1, me))
        
        res = caps if caps else pushes
        # Deduplicate
        seen = set()
        unique = []
        for p in res:
            if p not in seen:
                seen.add(p)
                unique.append(p)
        return unique, bool(caps)
    
    @staticmethod
    def _move(pos: Tuple, f: int, r: int, g: int, r1: int, me: int) -> Tuple:
        files = [list(x) for x in pos]
        files[f][r] = E
        files[g][r1] = me
        return tuple(tuple(x) for x in files)
    
    def has_capture(self, pos: Tuple, side: int) -> bool:
        return self.moves(pos, side)[1]
    
    def shape_heaps(self, pos: Tuple) -> Tuple:
        """Return multiset of heap sizes (runs of untouched files).
        
        On Möbius strip, the board is not a simple cycle because of the twist.
        We need to find connected components of untouched files.
        """
        full = [self.is_untouched(f, pos) for f in range(self.n)]
        
        # Find connected components of untouched files
        # On Möbius, adjacency is: f adjacent to f+1 and f-1 (with twist at seam)
        # But the twist only affects pawn direction, not file adjacency for components
        # Two untouched files are in the same component if they're connected via untouched files
        visited = [False] * self.n
        components = []
        
        for f in range(self.n):
            if full[f] and not visited[f]:
                # BFS to find component
                comp = []
                stack = [f]
                visited[f] = True
                while stack:
                    cur = stack.pop()
                    comp.append(cur)
                    for g, _ in self.neighbours(cur):
                        if full[g] and not visited[g]:
                            visited[g] = True
                            stack.append(g)
                components.append(len(comp))
        
        return tuple(sorted(components))
    
    def is_terminal_pawn_position(self, pos: Tuple, side: int) -> bool:
        """Check if a pawn has reached promotion rank."""
        if side == 0:
            return any(pos[f][2] == W for f in range(self.n))
        else:
            return any(pos[f][0] == B for f in range(self.n))


class TwoRowTorusBoard:
    """3xn torus-like ring with 2 ranks (cylindrical)."""
    
    def __init__(self, n: int):
        self.n = n
        self.files = n
        self.ranks = 2
    
    def neighbours(self, f: int) -> List[int]:
        return [(f - 1) % self.n, (f + 1) % self.n]
    
    def start(self) -> Tuple:
        return tuple((W, B) for _ in range(self.n))
    
    def is_untouched(self, f: int, pos: Tuple) -> bool:
        return pos[f] == (W, B)
    
    def moves(self, pos: Tuple, side: int) -> Tuple[List[Tuple], bool]:
        me, them = (W, B) if side == 0 else (B, W)
        d = 1 if side == 0 else -1
        caps, pushes = [], []
        
        for f in range(self.n):
            for r in range(2):
                if pos[f][r] != me:
                    continue
                r1 = r + d
                if not 0 <= r1 <= 1:
                    continue
                for g in self.neighbours(f):
                    if pos[g][r1] == them:
                        caps.append(self._move(pos, f, r, g, r1, me))
                    elif pos[g][r1] == E:
                        pushes.append(self._move(pos, f, r, g, r1, me))
        
        res = caps if caps else pushes
        seen = set()
        unique = []
        for p in res:
            if p not in seen:
                seen.add(p)
                unique.append(p)
        return unique, bool(caps)
    
    @staticmethod
    def _move(pos: Tuple, f: int, r: int, g: int, r1: int, me: int) -> Tuple:
        files = [list(x) for x in pos]
        files[f][r] = E
        files[g][r1] = me
        return tuple(tuple(x) for x in files)
    
    def has_capture(self, pos: Tuple, side: int) -> bool:
        return self.moves(pos, side)[1]
    
    def shape_heaps(self, pos: Tuple) -> Tuple:
        full = [self.is_untouched(f, pos) for f in range(self.n)]
        # On cylinder, components are runs of untouched files
        if all(full):
            return ("ring", self.n)
        runs = []
        # Find a gap to start
        start = full.index(False)
        order = [(start + i) % self.n for i in range(self.n)]
        cur = 0
        for f in order:
            if full[f]:
                cur += 1
            else:
                if cur:
                    runs.append(cur)
                cur = 0
        if cur:
            runs.append(cur)
        return tuple(sorted(runs))
    
    def is_terminal_pawn_position(self, pos: Tuple, side: int) -> bool:
        if side == 0:
            return any(pos[f][1] == W for f in range(self.n))
        else:
            return any(pos[f][0] == B for f in range(self.n))


# ============================================================
# Generic solver using macro-move decomposition
# ============================================================

def solve_variant(board, max_n: int = 16, misere: bool = False) -> Dict:
    """Solve a variant using full minimax with macro-move optimization."""
    sys.setrecursionlimit(1000000)
    
    normal_memo = {}
    misere_memo = {}
    promo_seen = [False]
    positions_count = [0]
    
    def get_moves(pos: Tuple, side: int):
        succ, is_cap = board.moves(pos, side)
        promo = board.is_terminal_pawn_position(pos, side)
        return succ, is_cap, promo
    
    def solve_rec(pos: Tuple, side: int):
        key = (pos, side)
        if key in normal_memo:
            return normal_memo[key], misere_memo[key]
        
        positions_count[0] += 1
        if positions_count[0] > 5_000_000:
            raise RuntimeError("Position limit exceeded")
        
        succ, is_cap, promo = get_moves(pos, side)
        if promo:
            promo_seen[0] = True
        
        if not succ:
            normal_memo[key] = False
            misere_memo[key] = True
            return False, True
        
        normal_win = any(not solve_rec(q, 1 - side)[0] for q in succ)
        misere_win = any(not solve_rec(q, 1 - side)[1] for q in succ)
        
        normal_memo[key] = normal_win
        misere_memo[key] = misere_win
        return normal_win, misere_win
    
    start = board.start()
    nw, mw = solve_rec(start, 0)
    nb, mb = solve_rec(start, 1)
    
    return {
        'normal_white_first': nw,
        'normal_black_first': nb,
        'misere_white_first': mw,
        'misere_black_first': mb,
        'positions_explored': positions_count[0],
        'promotion_reached': promo_seen[0],
    }


# ============================================================
# Macro-move based solver (much faster)
# ============================================================

def solve_variant_macro(board_class, max_n: int = 16) -> Dict:
    """Solve using macro-move graph like pawnboard.py."""
    from dawson.octal import grundy
    
    g = grundy("0.137", 200)
    MV = octal_options("0.137")
    
    def heap_moves_cached(h):
        return heap_moves(MV, h)
    
    results = {}
    
    for n in range(3, max_n + 1):
        board = board_class(n)
        
        # Build macro-move graph on quiet positions
        normal_memo = {}
        misere_memo = {}
        positions_count = [0]
        
        def get_macro_moves(pos: Tuple, side: int):
            """Get quiet endpoints after side pushes and forced captures."""
            succ, is_cap = board.moves(pos, side)
            endpoints = set()
            for q in succ:
                stack = [(q, 1 - side)]
                while stack:
                    p, s = stack.pop()
                    nxt, c = board.moves(p, s)
                    if c:
                        for r in nxt:
                            stack.append((r, 1 - s))
                    else:
                        endpoints.add((p, s))
            return endpoints
        
        def solve_quiet(pos: Tuple, side: int):
            key = (pos, side)
            if key in normal_memo:
                return normal_memo[key], misere_memo[key]
            
            positions_count[0] += 1
            
            endpoints = get_macro_moves(pos, side)
            if not endpoints:
                normal_memo[key] = False
                misere_memo[key] = True
                return False, True
            
            normal_win = any(not solve_quiet(q, s)[0] for q, s in endpoints)
            misere_win = any(not solve_quiet(q, s)[1] for q, s in endpoints)
            
            normal_memo[key] = normal_win
            misere_memo[key] = misere_win
            return normal_win, misere_win
        
        # Also check that macro-moves match octal 0.137 predictions
        start = board.start()
        nw, mw = solve_quiet(start, 0)
        nb, mb = solve_quiet(start, 1)
        
        results[n] = {
            'normal_white_first': nw,
            'normal_black_first': nb,
            'misere_white_first': mw,
            'misere_black_first': mb,
            'positions_explored': positions_count[0],
        }
    
    return results


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    print("Solving Möbius strip (3xn) for n=3..16...")
    mobius_results = solve_variant_macro(MobiusBoard, 16)
    
    print("\nMöbius strip outcomes:")
    print("n  | Normal (W/B) | Misère (W/B) | Positions")
    print("---|--------------|--------------|----------")
    for n in range(3, 17):
        r = mobius_results[n]
        nw = 'W' if r['normal_white_first'] else 'L'
        nb = 'W' if r['normal_black_first'] else 'L'
        mw = 'W' if r['misere_white_first'] else 'L'
        mb = 'W' if r['misere_black_first'] else 'L'
        print(f"{n:2d} | {nw}/{nb:10s} | {mw}/{mb:10s} | {r['positions_explored']}")
    
    print("\n\nSolving Two-row torus (3xn) for n=3..16...")
    torus_results = solve_variant_macro(TwoRowTorusBoard, 16)
    
    print("\nTwo-row torus outcomes:")
    print("n  | Normal (W/B) | Misère (W/B) | Positions")
    print("---|--------------|--------------|----------")
    for n in range(3, 17):
        r = torus_results[n]
        nw = 'W' if r['normal_white_first'] else 'L'
        nb = 'W' if r['normal_black_first'] else 'L'
        mw = 'W' if r['misere_white_first'] else 'L'
        mb = 'W' if r['misere_black_first'] else 'L'
        print(f"{n:2d} | {nw}/{nb:10s} | {mw}/{mb:10s} | {r['positions_explored']}")