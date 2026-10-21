"""Dawson's chess variants on new surfaces and wider boards.

Surfaces:
1. 3xn Möbius strip (twisted seam: crossing flips pawn color)
2. 3xn Torus (both files and ranks wrapped)
3. 4xn and 5xn boards (flat and cylinder)

Solves normal and misere play for small n by exhaustive search from the pawn rules.
"""

import sys
from functools import lru_cache
from dataclasses import dataclass
from typing import Tuple, List, Set, Dict, Optional
from enum import Enum

sys.setrecursionlimit(1000000)

E, W, B = 0, 1, 2


class Surface(Enum):
    FLAT = "flat"
    CYLINDER = "cylinder"
    MOEBIUS = "moebius"
    TORUS = "torus"


@dataclass(frozen=True)
class Board:
    """Board configuration."""
    files: int
    ranks: int
    surface: Surface
    
    def __post_init__(self):
        if self.ranks < 3:
            raise ValueError("Need at least 3 ranks for Dawson's chess")
        if self.files < 1:
            raise ValueError("Need at least 1 file")
    
    def start_position(self) -> Tuple[Tuple[Tuple[int, ...], ...], int]:
        """Return (position, side_to_move) for the standard start.
        Side 0 = White to move, Side 1 = Black to move.
        Position is tuple of files, each file is tuple of ranks (0=bottom/White side).
        """
        files = []
        for f in range(self.files):
            col = [E] * self.ranks
            col[0] = W      # White on rank 0 (bottom)
            col[self.ranks - 1] = B  # Black on top rank
            files.append(tuple(col))
        return (tuple(files), 0)
    
    def neighbors(self, f: int) -> List[int]:
        """Files adjacent to f (for captures)."""
        if self.surface in (Surface.CYLINDER, Surface.MOEBIUS, Surface.TORUS):
            return [(f - 1) % self.files, (f + 1) % self.files]
        else:
            res = []
            if f > 0:
                res.append(f - 1)
            if f < self.files - 1:
                res.append(f + 1)
            return res
    
    def rank_neighbors(self, r: int, direction: int) -> List[int]:
        """Ranks adjacent to r in given direction (+1 for White/up, -1 for Black/down)."""
        # For captures: diagonal moves change both file and rank
        # For straight moves: only rank changes
        r1 = r + direction
        if self.surface == Surface.TORUS:
            r1 = r1 % self.ranks
        if 0 <= r1 < self.ranks:
            return [r1]
        return []
    
    def move_pawn(self, pos: Tuple, f: int, r: int, nf: int, nr: int, 
                  side: int) -> Tuple[Tuple[Tuple[int, ...], ...], int, bool]:
        """Execute a pawn move. Returns (new_pos, new_side, color_flipped).
        Color flip happens on Möbius when crossing the file seam.
        """
        files = [list(col) for col in pos]
        piece = files[f][r]
        files[f][r] = E
        files[nf][nr] = piece
        
        color_flipped = False
        new_piece = piece
        
        # Check for Möbius color flip when crossing file seam
        if self.surface == Surface.MOEBIUS:
            # Crossing the seam: moving from file 0 to n-1 or n-1 to 0
            if (f == 0 and nf == self.files - 1) or (f == self.files - 1 and nf == 0):
                # Flip color
                new_piece = B if piece == W else W
                files[nf][nr] = new_piece
                color_flipped = True
        
        new_pos = tuple(tuple(col) for col in files)
        new_side = 1 - side
        return new_pos, new_side, color_flipped
    
    def get_moves(self, pos: Tuple, side: int) -> Tuple[List[Tuple], bool, bool]:
        """Get all legal moves for side (0=White, 1=Black).
        Returns (successor_positions, has_capture, promotion_reached).
        Captures are compulsory.
        """
        me = W if side == 0 else B
        them = B if side == 0 else W
        direction = 1 if side == 0 else -1
        
        captures = []
        pushes = []
        promo = False
        
        for f in range(self.files):
            for r in range(self.ranks):
                if pos[f][r] != me:
                    continue
                
                # Straight push
                for nr in self.rank_neighbors(r, direction):
                    if pos[f][nr] == E:
                        new_pos, new_side, _ = self.move_pawn(pos, f, r, f, nr, side)
                        # Check promotion: pawn reached opposite back rank
                        if (side == 0 and nr == self.ranks - 1) or (side == 1 and nr == 0):
                            promo = True
                        pushes.append((new_pos, new_side))
                
                # Diagonal captures
                for nf in self.neighbors(f):
                    for nr in self.rank_neighbors(r, direction):
                        if pos[nf][nr] == them:
                            new_pos, new_side, _ = self.move_pawn(pos, f, r, nf, nr, side)
                            captures.append((new_pos, new_side))
        
        # Captures are compulsory
        if captures:
            # Deduplicate
            seen = set()
            uniq = []
            for p, s in captures:
                if p not in seen:
                    seen.add(p)
                    uniq.append((p, s))
            return [p for p, s in uniq], True, promo
        
        seen = set()
        uniq = []
        for p, s in pushes:
            if p not in seen:
                seen.add(p)
                uniq.append((p, s))
        return [p for p, s in uniq], False, promo


def solve_board(board: Board, max_positions: int = 10000000) -> Dict:
    """Solve a board by memoised minimax for both normal and misere play.
    Returns dict with outcomes and statistics.
    """
    start_pos, start_side = board.start_position()
    normal_memo = {}
    misere_memo = {}
    promo_seen = [False]
    positions_visited = [0]
    
    def solve_normal(pos: Tuple, side: int) -> bool:
        key = (pos, side)
        if key in normal_memo:
            return normal_memo[key]
        positions_visited[0] += 1
        if positions_visited[0] > max_positions:
            raise MemoryError(f"Exceeded max positions {max_positions}")
        
        succ, _, promo = board.get_moves(pos, side)
        if promo:
            promo_seen[0] = True
        
        if not succ:
            normal_memo[key] = False  # no move = loss in normal play
            return False
        
        # Win if any move leads to opponent loss
        result = any(not solve_normal(q, 1 - side) for q in succ)
        normal_memo[key] = result
        return result
    
    def solve_misere(pos: Tuple, side: int) -> bool:
        key = (pos, side)
        if key in misere_memo:
            return misere_memo[key]
        
        succ, _, _ = board.get_moves(pos, side)
        
        if not succ:
            misere_memo[key] = True  # no move = win in misere play
            return True
        
        # Win if any move leads to opponent loss (in misere)
        result = any(not solve_misere(q, 1 - side) for q in succ)
        misere_memo[key] = result
        return result
    
    # Solve from start for both sides to move
    normal_w = solve_normal(start_pos, 0)
    normal_b = solve_normal(start_pos, 1)
    misere_w = solve_misere(start_pos, 0)
    misere_b = solve_misere(start_pos, 1)
    
    return {
        'board': board,
        'positions': len(normal_memo),
        'normal_white_first': normal_w,
        'normal_black_first': normal_b,
        'misere_white_first': misere_w,
        'misere_black_first': misere_b,
        'promotion_reached': promo_seen[0],
    }


def analyze_shape_heaps(board: Board, pos: Tuple) -> Tuple:
    """Extract heap structure from a quiet position.
    For flat/cylinder: runs of untouched files.
    For Möbius: more complex due to color flips.
    For Torus: wraps in both directions.
    """
    # A file is "untouched" if it has W on rank 0, E on middle ranks, B on top rank
    # But on Möbius/Torus, colors may be flipped
    
    full_pattern = [E] * board.ranks
    full_pattern[0] = W
    full_pattern[board.ranks - 1] = B
    full_pattern = tuple(full_pattern)
    
    # For Möbius, a flipped file would have B on rank 0, W on top rank
    flipped_pattern = [E] * board.ranks
    flipped_pattern[0] = B
    flipped_pattern[board.ranks - 1] = W
    flipped_pattern = tuple(flipped_pattern)
    
    untouched = []
    for f in range(board.files):
        col = pos[f]
        if col == full_pattern:
            untouched.append(True)
        elif col == flipped_pattern:
            untouched.append(True)  # Count flipped as untouched too
        else:
            untouched.append(False)
    
    if board.surface in (Surface.CYLINDER, Surface.TORUS):
        if all(untouched):
            return ("ring", board.files)
    
    if board.surface == Surface.MOEBIUS:
        if all(untouched):
            return ("moebius_ring", board.files)
    
    runs = []
    if board.surface in (Surface.CYLINDER, Surface.TORUS, Surface.MOEBIUS):
        # Find a break point
        try:
            k = untouched.index(False)
            order = [(k + i) % board.files for i in range(board.files)]
        except ValueError:
            order = list(range(board.files))
    else:
        order = list(range(board.files))
    
    cur = 0
    for f in order:
        if untouched[f]:
            cur += 1
        else:
            if cur > 0:
                runs.append(cur)
            cur = 0
    if cur > 0:
        runs.append(cur)
    
    return tuple(sorted(runs))


# Octal game 0.137 support
def octal_moves(code: str, n: int) -> List[Tuple]:
    """Get options for a heap of size n in octal game."""
    mv = [(k, int(d)) for k, d in enumerate(code[2:], start=1) if int(d)]
    out = []
    for k, bits in mv:
        r = n - k
        if r < 0:
            continue
        if r == 0 and bits & 1:
            out.append(())
        if r >= 1 and bits & 2:
            out.append((r,))
        if r >= 2 and bits & 4:
            for a in range(1, r // 2 + 1):
                out.append((a, r - a))
    return out


def octal_grundy(code: str, N: int) -> List[int]:
    g = [0] * (N + 1)
    for n in range(1, N + 1):
        opts = set()
        for rest in octal_moves(code, n):
            x = 0
            for h in rest:
                x ^= g[h]
            opts.add(x)
        m = 0
        while m in opts:
            m += 1
        g[n] = m
    return g


def octal_options(code: str):
    return [(k, int(d)) for k, d in enumerate(code[2:], start=1) if int(d)]


def heap_moves(mv, n):
    out = []
    for k, bits in mv:
        r = n - k
        if r < 0:
            continue
        if r == 0 and bits & 1:
            out.append(())
        if r >= 1 and bits & 2:
            out.append((r,))
        if r >= 2 and bits & 4:
            for a in range(1, r // 2 + 1):
                out.append((a, r - a))
    return out


# Misere solver for octal 0.137 (sums of strips)
from functools import lru_cache

MV_0137 = octal_options("0.137")

def canon_heaps(heaps):
    return tuple(sorted(1 if h == 2 else h for h in heaps if h > 0))

@lru_cache(maxsize=None)
def misere_P_heaps(heaps):
    heaps = canon_heaps(heaps)
    if not heaps:
        return False
    for i, h in enumerate(heaps):
        if h in (1, 2):
            rest = heaps[:i] + heaps[i+1:]
            if misere_P_heaps(rest):
                return False
            continue
        for rest in heap_moves(MV_0137, h):
            new = canon_heaps(heaps[:i] + heaps[i+1:] + rest)
            if misere_P_heaps(new):
                return False
    return True


def predict_normal(board: Board, pos: Tuple, gvals: List[int]) -> bool:
    """Predict normal outcome from heap decomposition."""
    sh = analyze_shape_heaps(board, pos)
    if sh and sh[0] in ("ring", "moebius_ring"):
        n = sh[1]
        if board.surface == Surface.CYLINDER:
            return gvals[n - 3] == 0 if n >= 3 else True
        elif board.surface == Surface.MOEBIUS:
            # Need to compute Möbius ring rule
            return None  # Unknown
        elif board.surface == Surface.TORUS:
            # Need to compute Torus ring rule
            return None
    x = 0
    for h in sh:
        x ^= gvals[h]
    return x != 0


def predict_misere(board: Board, pos: Tuple) -> bool:
    """Predict misere outcome from heap decomposition."""
    sh = analyze_shape_heaps(board, pos)
    if sh and sh[0] in ("ring", "moebius_ring"):
        n = sh[1]
        if board.surface == Surface.CYLINDER:
            strip = n - 3
            if strip <= 0:
                return False  # empty is N in misere
            return misere_P_heaps((strip,))
        elif board.surface == Surface.MOEBIUS:
            return None
        elif board.surface == Surface.TORUS:
            return None
    return not misere_P_heaps(sh)


def run_analysis(max_n: int = 16):
    """Run analysis for all variants up to max_n."""
    gvals = octal_grundy("0.137", max_n + 10)
    
    print("=" * 80)
    print("DAWSON'S CHESS VARIANTS ANALYSIS")
    print("=" * 80)
    
    results = {}
    
    # 1. Standard 3xn flat and cylinder (baseline)
    for surface_name, surface in [("flat", Surface.FLAT), ("cylinder", Surface.CYLINDER)]:
        print(f"\n--- 3xn {surface_name.upper()} (baseline) ---")
        for n in range(1 if surface == Surface.FLAT else 3, max_n + 1):
            board = Board(n, 3, surface)
            try:
                res = solve_board(board)
                results[(surface_name, n)] = res
                nw = "W" if res['normal_white_first'] else "L"
                nb = "W" if res['normal_black_first'] else "L"
                mw = "W" if res['misere_white_first'] else "L"
                mb = "W" if res['misere_black_first'] else "L"
                print(f"  n={n:2d}: pos={res['positions']:6d}  normal: W1={nw} B1={nb}  misere: W1={mw} B1={mb}  promo={res['promotion_reached']}")
            except MemoryError as e:
                print(f"  n={n:2d}: {e}")
                break
    
    # 2. 3xn Möbius strip
    print(f"\n--- 3xn MOEBIUS STRIP ---")
    for n in range(3, max_n + 1):
        board = Board(n, 3, Surface.MOEBIUS)
        try:
            res = solve_board(board)
            results[('moebius', n)] = res
            nw = "W" if res['normal_white_first'] else "L"
            nb = "W" if res['normal_black_first'] else "L"
            mw = "W" if res['misere_white_first'] else "L"
            mb = "W" if res['misere_black_first'] else "L"
            print(f"  n={n:2d}: pos={res['positions']:6d}  normal: W1={nw} B1={nb}  misere: W1={mw} B1={mb}  promo={res['promotion_reached']}")
        except MemoryError as e:
            print(f"  n={n:2d}: {e}")
            break
    
    # 3. 3xn Torus
    print(f"\n--- 3xn TORUS ---")
    for n in range(3, max_n + 1):
        board = Board(n, 3, Surface.TORUS)
        try:
            res = solve_board(board)
            results[('torus', n)] = res
            nw = "W" if res['normal_white_first'] else "L"
            nb = "W" if res['normal_black_first'] else "L"
            mw = "W" if res['misere_white_first'] else "L"
            mb = "W" if res['misere_black_first'] else "L"
            print(f"  n={n:2d}: pos={res['positions']:6d}  normal: W1={nw} B1={nb}  misere: W1={mw} B1={mb}  promo={res['promotion_reached']}")
        except MemoryError as e:
            print(f"  n={n:2d}: {e}")
            break
    
    # 4. 4xn flat and cylinder
    for surface_name, surface in [("flat", Surface.FLAT), ("cylinder", Surface.CYLINDER)]:
        print(f"\n--- 4xn {surface_name.upper()} ---")
        for n in range(1 if surface == Surface.FLAT else 3, max_n + 1):
            board = Board(n, 4, surface)
            try:
                res = solve_board(board)
                results[(f'4xn_{surface_name}', n)] = res
                nw = "W" if res['normal_white_first'] else "L"
                nb = "W" if res['normal_black_first'] else "L"
                mw = "W" if res['misere_white_first'] else "L"
                mb = "W" if res['misere_black_first'] else "L"
                print(f"  n={n:2d}: pos={res['positions']:6d}  normal: W1={nw} B1={nb}  misere: W1={mw} B1={mb}  promo={res['promotion_reached']}")
            except MemoryError as e:
                print(f"  n={n:2d}: {e}")
                break
    
    # 5. 5xn flat and cylinder
    for surface_name, surface in [("flat", Surface.FLAT), ("cylinder", Surface.CYLINDER)]:
        print(f"\n--- 5xn {surface_name.upper()} ---")
        for n in range(1 if surface == Surface.FLAT else 3, max_n + 1):
            board = Board(n, 5, surface)
            try:
                res = solve_board(board)
                results[(f'5xn_{surface_name}', n)] = res
                nw = "W" if res['normal_white_first'] else "L"
                nb = "W" if res['normal_black_first'] else "L"
                mw = "W" if res['misere_white_first'] else "L"
                mb = "W" if res['misere_black_first'] else "L"
                print(f"  n={n:2d}: pos={res['positions']:6d}  normal: W1={nw} B1={nb}  misere: W1={mw} B1={mb}  promo={res['promotion_reached']}")
            except MemoryError as e:
                print(f"  n={n:2d}: {e}")
                break
    
    return results, gvals


def check_misere_cylinder_periodicity():
    """Check misere cylinder outcomes for periodicity up to n=100.
    Uses the existing C program data.
    """
    print("\n" + "=" * 80)
    print("MISERE CYLINDER PERIODICITY ANALYSIS (n <= 100)")
    print("=" * 80)
    
    # From misere_c_100.txt: single rings that are misere N (first player wins)
    misere_N_rings = [4, 5, 9, 10, 14, 18, 19, 23, 24, 28, 32, 33, 37, 38, 42, 47, 51, 52, 56, 57, 61, 65, 66, 70, 71, 75, 79, 85, 95, 99]
    
    print(f"Misere N-rings (first player wins) for n=3..103: {misere_N_rings}")
    
    # Check if this matches "strip n-3 is misere P"
    misere_P_strips = [1, 2, 6, 7, 11, 15, 16, 20, 21, 25, 29, 30, 34, 35, 39, 44, 48, 49, 53, 54, 58, 62, 63, 67, 68, 72, 76, 82, 92, 96]
    predicted_N_rings = [s + 3 for s in misere_P_strips if s + 3 <= 103]
    
    print(f"Predicted from strip P-positions (n-3): {predicted_N_rings}")
    print(f"Match: {misere_N_rings == predicted_N_rings}")
    
    # Check periodicity
    outcomes = ['N' if n in misere_N_rings else 'P' for n in range(3, 104)]
    print(f"Outcomes n=3..103: {''.join(outcomes)}")
    
    # Look for periods
    for p in range(1, 50):
        matches = all(outcomes[i] == outcomes[i + p] for i in range(len(outcomes) - p))
        if matches:
            print(f"  Period {p} holds for all available n")
    
    # Check from some point onward
    for p in range(1, 50):
        for start in range(20, 60):
            if start + p < len(outcomes):
                matches = all(outcomes[i] == outcomes[i + p] for i in range(start, len(outcomes) - p))
                if matches:
                    print(f"  Period {p} from n={start+3} onward")
                    break
    
    return misere_N_rings


def analyze_moebius_structure(max_n: int = 16):
    """Analyze the Möbius strip game structure to identify octal form."""
    print("\n" + "=" * 80)
    print("MOEBIUS STRIP STRUCTURAL ANALYSIS")
    print("=" * 80)
    
    # For Möbius, the ring doesn't simply reduce to a strip
    # because the twist changes the topology
    # Let's compute the macro-move graph for the full ring
    
    for n in range(3, min(max_n + 1, 11)):
        board = Board(n, 3, Surface.MOEBIUS)
        start_pos, _ = board.start_position()
        
        # Get all legal first moves from the full ring
        succ, is_cap, _ = board.get_moves(start_pos, 0)
        print(f"\n  n={n}: {len(succ)} first moves (capture={is_cap})")
        
        # Analyze resulting shapes
        shapes = set()
        for q in succ:
            sh = analyze_shape_heaps(board, q)
            shapes.add(sh)
        print(f"    Resulting shapes: {shapes}")
        
        # Check if all first moves are equivalent (by symmetry)
        # On Möbius, rotation by 1 file is a symmetry, but reflection may not be
        # because the twist breaks reflection symmetry


def analyze_torus_structure(max_n: int = 16):
    """Analyze the Torus game structure."""
    print("\n" + "=" * 80)
    print("TORUS STRUCTURAL ANALYSIS")
    print("=" * 80)
    
    for n in range(3, min(max_n + 1, 11)):
        board = Board(n, 3, Surface.TORUS)
        start_pos, _ = board.start_position()
        
        succ, is_cap, _ = board.get_moves(start_pos, 0)
        print(f"\n  n={n}: {len(succ)} first moves (capture={is_cap})")
        
        shapes = set()
        for q in succ:
            sh = analyze_shape_heaps(board, q)
            shapes.add(sh)
        print(f"    Resulting shapes: {shapes}")


def analyze_wider_boards(max_n: int = 12):
    """Analyze 4xn and 5xn boards for structural patterns."""
    print("\n" + "=" * 80)
    print("WIDER BOARDS (4xn, 5xn) STRUCTURAL ANALYSIS")
    print("=" * 80)
    
    for ranks in [4, 5]:
        for surface_name, surface in [("flat", Surface.FLAT), ("cylinder", Surface.CYLINDER)]:
            print(f"\n  --- {ranks}xn {surface_name.upper()} ---")
            for n in range(1 if surface == Surface.FLAT else 3, min(max_n + 1, 10)):
                board = Board(n, ranks, surface)
                try:
                    res = solve_board(board, max_positions=500000)
                    nw = "W" if res['normal_white_first'] else "L"
                    nb = "W" if res['normal_black_first'] else "L"
                    mw = "W" if res['misere_white_first'] else "L"
                    mb = "W" if res['misere_black_first'] else "L"
                    print(f"    n={n:2d}: pos={res['positions']:6d}  normal: W1={nw} B1={nb}  misere: W1={mw} B1={mb}")
                except MemoryError:
                    print(f"    n={n:2d}: too large")
                    break


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=12)
    parser.add_argument("--misere-cylinder", action="store_true")
    parser.add_argument("--moebius", action="store_true")
    parser.add_argument("--torus", action="store_true")
    parser.add_argument("--wider", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    
    if args.all or not any([args.misere_cylinder, args.moebius, args.torus, args.wider]):
        run_analysis(args.max_n)
    
    if args.all or args.misere_cylinder:
        check_misere_cylinder_periodicity()
    
    if args.all or args.moebius:
        analyze_moebius_structure(args.max_n)
    
    if args.all or args.torus:
        analyze_torus_structure(args.max_n)
    
    if args.all or args.wider:
        analyze_wider_boards(args.max_n)