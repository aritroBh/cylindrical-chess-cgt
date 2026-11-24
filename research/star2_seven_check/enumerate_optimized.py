#!/usr/bin/env python3
"""Optimized independent enumerator for 7-pawn positions.

Generates positions on-the-fly in workers to avoid memory issues.
Uses efficient bitboard representation and batches evaluations.
"""

import itertools
import json
import multiprocessing as mp
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, ".")
from cylcgt import pawns, cgt

RACE_RULE = "count"
PASSED_RESPECTS_EP = True
WIDTHS = [1, 2, 3, 4]
RANKS = 8
TOTAL_PAWNS = 7
PAWN_RANKS = range(2, 8)
CHECKPOINT_DIR = Path("research/star2_seven_check/checkpoints")
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = Path("research/star2_seven_check/results.json")
REPORT_FILE = Path("research/star2_seven_check/REPORT.md")

EXPECTED = [
    "W: a4 b3 d2 d3 / B: a7 b7 c5",
    "W: b4 c2 d2 / B: a6 a7 c6 d5",
]

FILES = "abcdefghijklmnopqrstuvwxyz"


def sq_name(f: int, r: int) -> str:
    return f"{FILES[f]}{r}"


def pos_to_str(white: tuple, black: tuple) -> str:
    w = " ".join(sorted(sq_name(f, r) for f, r in white))
    b = " ".join(sorted(sq_name(f, r) for f, r in black))
    return f"W: {w} / B: {b}"


def generate_canonical_positions(width: int):
    """Generator yielding canonical positions for a width.

    Yields (white_tuple, black_tuple) where white <= mirror(white) lexicographically.
    """
    all_squares = [(f, r) for f in range(width) for r in PAWN_RANKS]
    n_squares = len(all_squares)

    # Precompute mirror mapping
    mirror_map = {i: (width - 1 - f, r) for i, (f, r) in enumerate(all_squares)}

    for w_count in range(1, TOTAL_PAWNS):
        b_count = TOTAL_PAWNS - w_count

        # Iterate over combinations of indices for white
        for white_idx in itertools.combinations(range(n_squares), w_count):
            white_set = set(white_idx)
            remaining = [i for i in range(n_squares) if i not in white_set]

            for black_idx in itertools.combinations(remaining, b_count):
                # Check edge files occupied
                all_files = set()
                for i in white_idx:
                    all_files.add(all_squares[i][0])
                for i in black_idx:
                    all_files.add(all_squares[i][0])
                if 0 not in all_files or (width - 1) not in all_files:
                    continue

                # Build position tuples
                white_pos = tuple(sorted(all_squares[i] for i in white_idx))
                black_pos = tuple(sorted(all_squares[i] for i in black_idx))

                # Mirror deduplication
                white_mirror = tuple(sorted(mirror_map[i] for i in white_idx))
                black_mirror = tuple(sorted(mirror_map[i] for i in black_idx))

                if (white_pos, black_pos) > (white_mirror, black_mirror):
                    continue

                yield white_pos, black_pos


def evaluate_batch(width: int, batch: list[tuple]) -> list[dict]:
    """Evaluate a batch of positions."""
    board = pawns.Board(width, RANKS, False, True)
    pawns.RACE_RULE = RACE_RULE
    pawns.PASSED_RESPECTS_EP = PASSED_RESPECTS_EP
    pawns._value.cache_clear()

    results = []
    for white_pos, black_pos in batch:
        p = pawns.Pos(frozenset(white_pos), frozenset(black_pos))

        if pawns.passed(board, p, "W") or pawns.passed(board, p, "B"):
            continue

        try:
            game = pawns.value(board, p)
        except pawns.RaceError:
            continue
        except Exception:
            continue

        if game.nim is not None and game.nim >= 2:
            results.append({
                "width": width,
                "position": pos_to_str(white_pos, black_pos),
                "white": [sq_name(f, r) for f, r in white_pos],
                "black": [sq_name(f, r) for f, r in black_pos],
                "nimber": game.nim,
                "value": cgt.show(game),
                "outcome": cgt.outcome(game),
            })
    return results


def worker_width(width: int, checkpoint_file: Path, batch_size: int = 1000) -> list[dict]:
    """Worker for a single width, with checkpointing."""
    results = []
    done = set()

    if checkpoint_file.exists():
        with open(checkpoint_file) as f:
            for line in f:
                done.add(line.strip())

    batch = []
    count = 0
    last_checkpoint = time.time()

    for white_pos, black_pos in generate_canonical_positions(width):
        key = f"{white_pos}|{black_pos}"
        if key in done:
            continue

        batch.append((white_pos, black_pos))
        count += 1

        if len(batch) >= batch_size:
            batch_results = evaluate_batch(width, batch)
            results.extend(batch_results)

            # Checkpoint
            with open(checkpoint_file, "a") as f:
                for wp, bp in batch:
                    f.write(f"{wp}|{bp}\n")
            batch = []

            # Progress report every 30 seconds
            if time.time() - last_checkpoint > 30:
                print(f"  Width {width}: processed {count}, found {len(results)} *k>=2", flush=True)
                last_checkpoint = time.time()

    # Process remaining batch
    if batch:
        batch_results = evaluate_batch(width, batch)
        results.extend(batch_results)
        with open(checkpoint_file, "a") as f:
            for wp, bp in batch:
                f.write(f"{wp}|{bp}\n")

    print(f"  Width {width} done: {count} positions, {len(results)} *k>=2 found", flush=True)
    return results


def main():
    print("Starting optimized enumeration...", flush=True)

    # Use multiprocessing with at most 3 processes
    max_processes = min(3, len(WIDTHS))

    print(f"Using {max_processes} processes", flush=True)

    with mp.Pool(max_processes) as pool:
        args = [(w, CHECKPOINT_DIR / f"checkpoint_w{w}.txt") for w in WIDTHS]
        all_results = []
        for results in pool.starmap(worker_width, args):
            all_results.extend(results)

    print(f"Total *k>=2 found: {len(all_results)}", flush=True)

    # Save results
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_results, f, indent=2)

    generate_report(all_results)
    print(f"Results saved to {OUTPUT_FILE}", flush=True)
    print(f"Report saved to {REPORT_FILE}", flush=True)


def generate_report(results: list[dict]):
    results_sorted = sorted(results, key=lambda r: (r["width"], r["position"]))
    found_positions = {r["position"] for r in results_sorted}
    expected_set = set(EXPECTED)
    matches_expected = found_positions == expected_set
    only_in_found = found_positions - expected_set
    only_in_expected = expected_set - found_positions

    with open(REPORT_FILE, "w") as f:
        f.write("# T22: Independent Census of 7-Pawn Positions\n\n")
        f.write("## Five-line summary\n\n")
        f.write(f"- **CHECKED-2:** {len(results_sorted)} positions with *k (k≥2) found\n")
        for r in results_sorted:
            f.write(f"  - {r['position']} = *{r['nimber']} ({r['value']})\n")
        f.write(f"- **Match claim:** {'YES' if matches_expected else 'NO'}\n")
        if not matches_expected:
            if only_in_found:
                f.write(f"  - Extra positions found: {sorted(only_in_found)}\n")
            if only_in_expected:
                f.write(f"  - Missing positions: {sorted(only_in_expected)}\n")
        f.write("- **Reproduce:** `PYTHONPATH=. .venv/bin/python research/star2_seven_check/enumerate_optimized.py`\n")
        f.write("- **Label:** CHECKED-2 (independent Python enumerator + cylcgt)\n\n")

        f.write("## Method\n\n")
        f.write("- Independent Python enumerator (no code from C scanners)\n")
        f.write("- Flat widths 1–4, 8 ranks, exactly 7 pawns on ranks 2–7\n")
        f.write("- At least one pawn per side\n")
        f.write("- No passed pawn at root (e.p.-aware: `PASSED_RESPECTS_EP=True`)\n")
        f.write("- Both edge files occupied\n")
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
        f.write("PYTHONPATH=. .venv/bin/python research/star2_seven_check/enumerate_optimized.py\n")
        f.write("```\n")


if __name__ == "__main__":
    main()