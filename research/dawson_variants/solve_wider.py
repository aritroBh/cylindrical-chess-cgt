"""Solver for wider boards (4xn, 5xn) flat and cylinder."""

import sys
from functools import lru_cache

sys.path.insert(0, '.')

E, W, B = 0, 1, 2


class WiderBoard:
    """Flat or cylindrical board with extra ranks."""
    
    def __init__(self, n: int, ranks: int, wrap: bool):
        self.n = n
        self.ranks = ranks
        self.wrap = wrap
        self.files = n
    
    def neighbours(self, f: int):
        if self.wrap:
            return [(f - 1) % self.n, (f + 1) % self.n]
        else:
            res = []
            if f > 0:
                res.append(f - 1)
            if f < self.n - 1:
                res.append(f + 1)
            return res
    
    def start(self):
        pos = []
        for _ in range(self.n):
            file_ranks = [E] * self.ranks
            file_ranks[0] = W
            file_ranks[self.ranks - 1] = B
            pos.append(tuple(file_ranks))
        return tuple(pos)
    
    def moves(self, pos, side):
        me, them = (W, B) if side == 0 else (B, W)
        d = 1 if side == 0 else -1
        caps, pushes = [], []
        
        for f in range(self.n):
            for r in range(self.ranks):
                if pos[f][r] != me:
                    continue
                r1 = r + d
                if not 0 <= r1 < self.ranks:
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
    print("Solving wider boards (4xn, 5xn) flat and cylinder for n=3..10...")
    
    for ranks in [4, 5]:
        for wrap in [False, True]:
            label = f"{'cyl' if wrap else 'flat'}{ranks}xn"
            print(f"\n--- {label} ---")
            for n in range(3, 11):
                try:
                    board = WiderBoard(n, ranks, wrap)
                    r = solve_direct(board, max_positions=2_000_000)
                    nw = 'W' if r['normal_white_first'] else 'L'
                    nb = 'W' if r['normal_black_first'] else 'L'
                    mw = 'W' if r['misere_white_first'] else 'L'
                    mb = 'W' if r['misere_black_first'] else 'L'
                    print(f"  n={n:2d}: normal {nw}/{nb}  misere {mw}/{mb}  (pos: {r['positions_explored']})")
                except RuntimeError as e:
                    print(f"  n={n:2d}: TIMEOUT - {e}")
                except Exception as e:
                    print(f"  n={n:2d}: ERROR - {e}")


if __name__ == "__main__":
    main()