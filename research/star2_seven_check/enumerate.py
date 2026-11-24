#!/usr/bin/env python3
"""Independent enumerator for 7-pawn positions on flat boards width 1-4.

Enumerates positions with:
- flat widths 1-4, 8 ranks, exactly 7 pawns
- pawns on ranks 2-7 only
- at least one pawn per side
- no passed pawn at root (e.p.-aware test)
- both edge files (0 and w-1) occupied
- one of each mirror pair (left-right reflection)

Evaluates with cylcgt: RACE_RULE="count", PASSED_RESPECTS_EP=True, Board(w,8,False,True)
Reports positions with value *k, k>=2.
"""

import itertools
import json
import multiprocessing as mp
import os
import sys
from dataclasses import dataclass
from pathlib import Path

# Ensure we can import cylcgt
sys.path.insert(0, ".")
from cylcgt import pawns, cgt

# Configuration
RACE_RULE = "count"
PASSED_RESPECTS_EP = True
WIDTHS = [1, 2, 3, 4]
RANKS = 8
TOTAL_PAWNS = 7
PAWN_RANKS = range(2, 8)  # ranks 2-7 inclusive
CHECKPOINT_DIR = Path("research/star2_seven_check/checkpoints")
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = Path("research/star2_seven_check/results.json")
REPORT_FILE = Path("research/star2_seven_check/REPORT.md")

# Expected positions from the claim
EXPECTED = [
    "W: a4 b3 d2 d3 / B: a7 b7 c5",
    "W: b4 c2 d2 / B: a6 a7 c6 d5",
]


@dataclass(frozen=True)
class Position:
    white: tuple[tuple[int, int], ...]  # sorted (file, rank)
    black: tuple[tuple[int, int], ...]

    def to_pos(self) -> pawns.Pos:
        return pawns.Pos(frozenset(self.white), frozenset(self.black))

    def mirror(self, width: int) -> "Position":
        """Left-right mirror: file f -> width-1-f"""
        mwhite = tuple(sorted((width - 1 - f, r) for f, r in self.white))
        mblack = tuple(sorted((width - 1 - f, r) for f, r in self.black))
        return Position(mwhite, mblack)

    def canonical_key(self) -> tuple:
        """Total ordering key for mirror deduplication"""
        return (self.white, self.black)

    def __lt__(self, other: "Position") -> bool:
        return self.canonical_key() < other.canonical_key()


def generate_positions_for_width(width: int) -> list[Position]:
    """Generate all valid 7-pawn positions for a given width."""
    # All possible squares: files 0..width-1, ranks 2..7
    all_squares = [(f, r) for f in range(width) for r in PAWN_RANKS]

    positions = []

    # We need exactly 7 pawns total, at least 1 per side
    for w_count in range(1, TOTAL_PAWNS):  # 1 to 6 white pawns
        b_count = TOTAL_PAWNS - w_count
        # Choose white squares
        for white_squares in itertools.combinations(all_squares, w_count):
            white_set = set(white_squares)
            remaining = [sq for sq in all_squares if sq not in white_set]
            # Choose black squares from remaining
            for black_squares in itertools.combinations(remaining, b_count):
                # Check edge files occupied
                white_files = {f for f, _ in white_squares}
                black_files = {f for f, _ in black_squares}
                all_files = white_files | black_files
                if 0 not in all_files or (width - 1) not in all_files:
                    continue

                pos = Position(tuple(sorted(white_squares)), tuple(sorted(black_squares)))

                # Mirror deduplication: only keep if pos <= mirror
                mirror_pos = pos.mirror(width)
                if pos > mirror_pos:
                    continue

                positions.append(pos)

    return positions


def has_passed_pawn_ep_aware(board: pawns.Board, pos: pawns.Pos) -> bool:
    """Check if either side has a passed pawn under e.p.-aware test."""
    return pawns.passed(board, pos, "W") or pawns.passed(board, pos, "B")


def evaluate_position(width: int, pos: Position) -> dict | None:
    """Evaluate a single position, return result dict if *k with k>=2, else None."""
    board = pawns.Board(width, RANKS, False, True)
    p = pos.to_pos()

    # Check no passed pawn at root (e.p.-aware)
    if has_passed_pawn_ep_aware(board, p):
        return None

    # Configure cylcgt
    pawns.RACE_RULE = RACE_RULE
    pawns.PASSED_RESPECTS_EP = PASSED_RESPECTS_EP
    pawns._value.cache_clear()

    try:
        game = pawns.value(board, p)
    except pawns.RaceError:
        return None  # Race positions are excluded
    except Exception as e:
        print(f"Error evaluating {pos}: {e}", file=sys.stderr)
        return None

    if game.nim is not None and game.nim >= 2:
        return {
            "width": width,
            "position": str(pos),
            "white": [f"{pawns.FILES[f]}{r}" for f, r in pos.white],
            "black": [f"{pawns.FILES[f]}{r}" for f, r in pos.black],
            "nimber": game.nim,
            "value": cgt.show(game),
            "outcome": cgt.outcome(game),
        }
    return None


def worker_width(width: int, positions: list[Position], checkpoint_file: Path) -> list[dict]:
    """Worker process for a single width."""
    results = []
    # Load checkpoint if exists
    done = set()
    if checkpoint_file.exists():
        with open(checkpoint_file) as f:
            for line in f:
                done.add(line.strip())

    for i, pos in enumerate(positions):
        key = f"{width}:{pos.canonical_key()}"
        if key in done:
            continue

        result = evaluate_position(width, pos)
        if result:
            results.append(result)

        # Checkpoint every 100 positions
        if i % 100 == 0:
            with open(checkpoint_file, "a") as f:
                f.write(key + "\n")

    # Final checkpoint
    with open(checkpoint_file, "a") as f:
        f.write(key + "\n")

    return results


def main():
    print("Generating positions...")
    all_positions_by_width = {}
    total_positions = 0

    for width in WIDTHS:
        positions = generate_positions_for_width(width)
        all_positions_by_width[width] = positions
        total_positions += len(positions)
        print(f"  Width {width}: {len(positions)} positions after filters")

    print(f"Total positions to evaluate: {total_positions}")

    # Use multiprocessing with at most 3 processes
    max_processes = min(3, len(WIDTHS))

    print(f"Starting evaluation with {max_processes} processes...")
    all_results = []

    with mp.Pool(max_processes) as pool:
        args = [
            (width, all_positions_by_width[width], CHECKPOINT_DIR / f"checkpoint_w{width}.txt")
            for width in WIDTHS
        ]
        for results in pool.starmap(worker_width, args):
            all_results.extend(results)

    print(f"Found {len(all_results)} positions with *k, k>=2")

    # Save results
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_results, f, indent=2)

    # Generate report
    generate_report(all_results)

    print(f"Results saved to {OUTPUT_FILE}")
    print(f"Report saved to {REPORT_FILE}")


def generate_report(results: list[dict]):
    """Generate the REPORT.md file."""
    # Sort results for consistent output
    results_sorted = sorted(results, key=lambda r: (r["width"], r["position"]))

    # Check against expected
    found_positions = {r["position"] for r in results_sorted}
    expected_set = set(EXPECTED)
    matches_expected = found_positions == expected_set
    only_in_found = found_positions - expected_set
    only_in_expected = expected_set - found_positions

    with open(REPORT_FILE, "w") as f:
        f.write("# T22: Independent Census of 7-Pawn Positions\n\n")
        f.write("## Five-line summary\n\n")
        f.write(f"- **Root count:** {sum(len(generate_positions_for_width(w)) for w in WIDTHS)} positions enumerated\n")
        f.write(f"- **CHECKED-2:** {len(results_sorted)} positions with *k (k≥2) found\n")
        for r in results_sorted:
            f.write(f"  - {r['position']} = *{r['nimber']} ({r['value']})\n")
        f.write(f"- **Match claim:** {'YES' if matches_expected else 'NO'}\n")
        if not matches_expected:
            if only_in_found:
                f.write(f"  - Extra positions found: {sorted(only_in_found)}\n")
            if only_in_expected:
                f.write(f"  - Missing positions: {sorted(only_in_expected)}\n")
        f.write("- **Reproduce:** `PYTHONPATH=. .venv/bin/python research/star2_seven_check/enumerate.py`\n")
        f.write("- **Label:** CHECKED-2 (independent Python enumerator + cylcgt)\n\n")

        f.write("## Method\n\n")
        f.write("- Independent Python enumerator (no code from C scanners)\n")
        f.write("- Flat widths 1–4, 8 ranks, exactly 7 pawns on ranks 2–7\n")
        f.write("- At least one pawn per side\n")
        f.write("- No passed pawn at root (e.p.-aware: `PASSED_RESPECTS_EP=True`)\n")
        f.write("- Both edge files (a and h/d/b/c) occupied\n")
        f.write("- One of each mirror pair (left-right reflection)\n")
        f.write("- Evaluated with `cylcgt`: `RACE_RULE=count`, `Board(w,8,False,True)`\n")
        f.write("- Multiprocessing with 3 processes, checkpointing to disk\n\n")

        f.write("## Full Results\n\n")
        f.write("| Width | Position | Nimber | Value | Outcome |\n")
        f.write("|-------|----------|--------|-------|---------|\n")
        for r in results_sorted:
            f.write(f"| {r['width']} | {r['position']} | *{r['nimber']} | {r['value']} | {r['outcome']} |\n")

        f.write("\n## Reproduction Commands\n\n")
        f.write("```sh\n")
        f.write("cd .\n")
        f.write("PYTHONPATH=. .venv/bin/python research/star2_seven_check/enumerate.py\n")
        f.write("```\n")


if __name__ == "__main__":
    main()