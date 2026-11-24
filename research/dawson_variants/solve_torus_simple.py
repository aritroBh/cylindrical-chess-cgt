"""Simple direct solver for two-row torus and Möbius strip."""

import sys
from functools import lru_cache

sys.path.insert(0, '.')

E, W, B = 0, 1, 2


class TwoRowTorusBoard:
    def __init__(self, n: int):
        self.n = n
        self.files = n
        self.ranks = 2
    
    def neighbours(self, f: int):
        return [(f - 1) % self.n, (f + 1) % self.n]
    
    def start(self):
        return tuple((W, B) for _ in range(self.n))
    
    def moves(self, pos, side):
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
    def _move(pos, f, r, g, r1, me):
        files = [list(x) for x in pos]
        files[f][r] = E
        files[g][r1] = me
        return tuple(tuple(x) for x in files)


class MobiusBoard:
    def __init__(self, n: int):
        self.n = n
        self.files = n
        self.ranks = 3
    
    def neighbours(self, f):
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
    
    def start(self):
        return tuple((W, E, B) for _ in range(self.n))
    
    def moves(self, pos, side):
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
        seen = set()
        unique = []
        for p in res:
            if p not in seen:
                seen.add(p)
                unique.append(p)
        return unique, bool(caps)
    
    @staticmethod
    def _move(pos, f, r, g, r1, me):
        files = [list(x) for x in pos]
        files[f][r] = E
        files[g][r1] = me
        return tuple(tuple(x) for x in files)


def solve_direct(board, max_positions=2_000_000):
    sys.setrecursionlimit(1000000)
    
    normal_memo = {}
    misere_memo = {}
    positions_count = [0]
    
    @lru_cache(maxsize=None)
    def normal_win(pos, side):
        positions_count[0] += 1
        if positions_count[0] > max_positions:
            raise RuntimeError("Limit exceeded")
        succ, _ = board.moves(pos, side)
        if not succ:
            return False
        return any(not normal_win(q, 1 - side) for q in succ)
    
    @lru_cache(maxsize=None)
    def misere_win(pos, side):
        succ, _ = board.moves(pos, side)
        if not succ:
            return True
        return any(not misere_win(q, 1 - side) for q in succ)
    
    start = board.start()
    nw = normal_win(start, 0)
    nb = normal_win(start, 1)
    mw = misere_win(start, 0)
    mb = misere_win(start, 1)
    
    return {
        'normal_white_first': nw,
        'normal_black_first': nb,
        'misere_white_first': mw,
        'misere_black_first': mb,
        'positions_explored': positions_count[0],
    }


def main():
    print("Solving Two-row torus (3xn, 2 ranks) for n=3..12...")
    for n in range(3, 13):
        try:
            board = TwoRowTorusBoard(n)
            r = solve_direct(board, max_positions=1_000_000)
            nw = 'W' if r['normal_white_first'] else 'L'
            nb = 'W' if r['normal_black_first'] else 'L'
            mw = 'W' if r['misere_white_first'] else 'L'
            mb = 'W' if r['misere_black_first'] else 'L'
            print(f"n={n:2d}: normal {nw}/{nb}  misere {mw}/{mb}  (pos: {r['positions_explored']})")
        except RuntimeError as e:
            print(f"n={n:2d}: TIMEOUT - {e}")
    
    print("\nSolving Möbius strip (3xn) for n=3..12 (verification)...")
    for n in range(3, 13):
        try:
            board = MobiusBoard(n)
            r = solve_direct(board, max_positions=1_000_000)
            nw = 'W' if r['normal_white_first'] else 'L'
            nb = 'W' if r['normal_black_first'] else 'L'
            mw = 'W' if r['misere_white_first'] else 'L'
            mb = 'W' if r['misere_black_first'] else 'L'
            print(f"n={n:2d}: normal {nw}/{nb}  misere {mw}/{mb}  (pos: {r['positions_explored']})")
        except RuntimeError as e:
            print(f"n={n:2d}: TIMEOUT - {e}")


if __name__ == "__main__":
    main()