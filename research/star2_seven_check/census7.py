#!/usr/bin/env python3
"""Chunked census of 7-pawn flat positions whose cylcgt value is *k with k >= 2.

This is a fresh, restartable enumerator for the census that T22 lost.  Scope,
conventions and the evaluation are T22's (see `enumerate_fast.py`), only the
bookkeeping is new: the work is split into numbered chunks, each chunk writes
its hits to disk as it goes, and each chunk is independently re-runnable.

Scope (identical to T22):
  * flat widths 1..4, 8 ranks, exactly 7 pawns, all on ranks 2..7;
  * at least one pawn per side;
  * both edge files occupied;
  * no passed pawn at the root under the e.p.-aware test;
  * exactly one of each mirror pair (left-right reflection);
  * cylcgt with RACE_RULE="count", PASSED_RESPECTS_EP=True, Board(w, 8, False, True).

Chunk rule (deterministic, and a partition of the scope):
  The white combinations are enumerated in canonical order and numbered 0, 1,
  2, ...  Chunk k keeps the white combinations whose index is congruent to k
  modulo K, and processes ALL their valid black combinations.  Every position
  of the scope therefore belongs to exactly one chunk, and each chunk gets
  approximately 1/K of the work.

Usage:
    census7.py --width W --chunk k --of K     # run one chunk
    census7.py --sanity                       # the two sanity checks
    census7.py --count --width W              # count the scope of one width

Outputs (in ./census7/):
    w{W}_c{k}.hits.tsv   one line per hit: position <TAB> k <TAB> value
    w{W}_c{k}.done       counts of the chunk, written when the chunk finishes
"""

from __future__ import annotations

import argparse
import itertools
import math
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cylcgt import cgt, pawns  # noqa: E402

HERE = Path(__file__).resolve().parent
OUTDIR = HERE / "census7"
OUTDIR.mkdir(parents=True, exist_ok=True)

RANKS = 8
PAWN_RANKS = tuple(range(2, 8))          # ranks 2..7 inclusive
TOTAL_PAWNS = 7
RACE_RULE = "count"
PASSED_RESPECTS_EP = True
RSS_LIMIT_MB = 4000                      # clear the cylcgt caches above this
CLEAR_CACHE_EVERY = 50_000               # clear caches every N positions regardless of RSS
PROGRESS_EVERY = 20_000                  # generated positions between progress lines
CHECK_RSS_EVERY = 10_000                 # generated positions between RSS checks

EXPECTED = (
    "W: a4 b3 d2 d3 / B: a7 b7 c5",
    "W: b4 c2 d2 / B: a6 a7 c6 d5",
)

# Recommended chunk counts per width (chosen so each chunk < 30 min)
DEFAULT_K = {1: 1, 2: 3, 3: 10, 4: 30}


# --------------------------------------------------------------------------
# geometry
# --------------------------------------------------------------------------
class Geom:
    """Square layout for one width.

    Square index i = f * 6 + k encodes file f and rank 2 + k, so index order
    equals (file, rank) order and `combinations(range(n), k)` already yields
    squares sorted in the canonical (file, rank) order.
    """

    def __init__(self, width: int):
        self.width = width
        self.n = len(PAWN_RANKS) * width
        self.sq = [(i // 6, PAWN_RANKS[i % 6]) for i in range(self.n)]
        self.file_mask = []
        for f in range(width):
            m = 0
            for k in range(len(PAWN_RANKS)):
                m |= 1 << (f * len(PAWN_RANKS) + k)
            self.file_mask.append(m)
        self.edge0 = self.file_mask[0]
        self.edge_last = self.file_mask[width - 1]

    def mirror(self, squares):
        """The left-right reflection of a square tuple, canonically sorted."""
        w = self.width
        return tuple(sorted((w - 1 - f, r) for (f, r) in squares))


def mask_of(indices) -> int:
    m = 0
    for i in indices:
        m |= 1 << i
    return m


# --------------------------------------------------------------------------
# the scope generator
# --------------------------------------------------------------------------
def scope(geom: Geom, chunk: int, nchunks: int):
    """Yield (white_squares, black_squares) for the positions of one chunk.

    Chunking: white combinations are numbered 0, 1, 2, ... in the canonical
    order (wc=1..6, then lexicographic within each wc).  Chunk `chunk` keeps
    the white combinations whose index is congruent to `chunk` modulo `nchunks`,
    and for each such white combination, it yields ALL valid black combinations
    (those that satisfy the edge-files and mirror filters).

    This chunking keeps all black combinations of a white combination together,
    which dramatically improves cache locality because White's moves (and thus
    the subpositions after White moves) are shared across all black combinations
    of the same white combination.
    """
    w = geom.width
    n = geom.n
    sq = geom.sq
    edge0, edge_last = geom.edge0, geom.edge_last

    white_idx = 0
    for wc in range(1, TOTAL_PAWNS):
        bc = TOTAL_PAWNS - wc
        for white_idx_tuple in itertools.combinations(range(n), wc):
            if white_idx % nchunks != chunk:
                white_idx += 1
                continue

            white_squares = tuple(sq[i] for i in white_idx_tuple)
            wmask = mask_of(white_idx_tuple)
            wfiles = {sq[i][0] for i in white_idx_tuple}
            fmin = min(wfiles)
            fmax = max(wfiles)
            m2 = w - 1 - fmax

            remaining = [i for i in range(n) if not (wmask >> i) & 1]

            for black_idx_tuple in itertools.combinations(remaining, bc):
                bmask = mask_of(black_idx_tuple)
                occ = wmask | bmask
                if not occ & edge0 or not occ & edge_last:
                    continue
                black_squares = tuple(sq[i] for i in black_idx_tuple)
                if fmin != m2:
                    if fmin > m2:
                        continue
                else:
                    wm = geom.mirror(white_squares)
                    if white_squares > wm:
                        continue
                    if white_squares == wm:
                        bm = geom.mirror(black_squares)
                        if black_squares > bm:
                            continue
                yield white_squares, black_squares

            white_idx += 1


def scope_count(geom: Geom) -> int:
    """Number of positions in scope for this width (no evaluation)."""
    return sum(1 for _ in scope(geom, 0, 1))


# --------------------------------------------------------------------------
# evaluation helpers
# --------------------------------------------------------------------------
def make_pos(white, black):
    return pawns.Pos(frozenset(white), frozenset(black))


def pos_str(white, black) -> str:
    def s(sqs):
        return " ".join(f"{chr(ord('a') + f)}{r}" for f, r in sorted(sqs))
    return f"W: {s(white)} / B: {s(black)}"


def rss_mb() -> float:
    """Current resident set size of this process, in MB."""
    try:
        out = subprocess.run(
            ["ps", "-o", "rss=", "-p", str(os.getpid())],
            capture_output=True, text=True, timeout=15,
        ).stdout
        return int(out.strip()) / 1024.0
    except Exception:
        return 0.0


def clear_caches() -> None:
    """Drop the memoisation caches.

    `pawns._value.cache_clear()` is the one the brief asks for.  The cgt
    memo tables are pure function caches and are dropped as well, because
    they dominate the memory.  `cgt._table` is NOT touched: it is the
    hash-consing table, and dropping it would create two distinct objects
    for the same canonical game and break Game identity.
    """
    pawns._value.cache_clear()
    cgt._le_memo.clear()
    cgt._add_memo.clear()
    cgt._neg_memo.clear()


def setup(width: int):
    pawns.RACE_RULE = RACE_RULE
    pawns.PASSED_RESPECTS_EP = PASSED_RESPECTS_EP
    pawns._value.cache_clear()          # the globals just changed
    return pawns.Board(width, RANKS, False, True)


# --------------------------------------------------------------------------
# chunk runner
# --------------------------------------------------------------------------
def run_chunk(width: int, chunk: int, nchunks: int, max_positions: int = 0) -> int:
    hits_path = OUTDIR / f"w{width}_c{chunk}.hits.tsv"
    done_path = OUTDIR / f"w{width}_c{chunk}.done"
    if done_path.exists() and done_path.read_text().startswith("# census7 done"):
        print(f"w{width} c{chunk}/{nchunks}: already done, skipping", flush=True)
        return 0

    board = setup(width)
    geom = Geom(width)

    n_generated = 0
    n_skipped = 0
    n_evaluated = 0
    n_race = 0
    n_other = 0
    tracebacks: list[str] = []
    t0 = time.time()

    hits_f = open(hits_path, "a", buffering=1)

    try:
        for white, black in scope(geom, chunk, nchunks):
            n_generated += 1
            p = make_pos(white, black)
            if pawns.passed(board, p, "W") or pawns.passed(board, p, "B"):
                n_skipped += 1
            else:
                try:
                    g = pawns.value(board, p)
                except pawns.RaceError:
                    n_race += 1
                except Exception:
                    n_other += 1
                    if len(tracebacks) < 3:
                        tracebacks.append(traceback.format_exc())
                else:
                    n_evaluated += 1
                    if g.nim is not None and g.nim >= 2:
                        hits_f.write(f"{pos_str(white, black)}\t{g.nim}\t{cgt.show(g)}\n")
                        hits_f.flush()
                        print(f"  HIT w{width} c{chunk}: {pos_str(white, black)} = {cgt.show(g)}",
                              flush=True)
            if n_generated % CHECK_RSS_EVERY == 0:
                mb = rss_mb()
                if mb > RSS_LIMIT_MB:
                    print(f"  rss {mb:.0f} MB > {RSS_LIMIT_MB} MB, clearing caches", flush=True)
                    clear_caches()
            if n_generated % CLEAR_CACHE_EVERY == 0:
                print(f"  periodic cache clear at {n_generated} positions", flush=True)
                clear_caches()
            if n_generated % PROGRESS_EVERY == 0:
                dt = time.time() - t0
                print(f"  w{width} c{chunk}/{nchunks}: gen={n_generated} skip={n_skipped} "
                      f"eval={n_evaluated} race={n_race} other={n_other} "
                      f"{n_generated / dt:.0f} pos/s rss={rss_mb():.0f}MB", flush=True)
            if max_positions and n_generated >= max_positions:
                print(f"  stopping early at {n_generated} (--max-positions)", flush=True)
                break
    finally:
        hits_f.close()

    dt = time.time() - t0
    if max_positions:
        print(f"w{width} c{chunk}: partial run, no .done written", flush=True)
        return 0

    lines = [
        "# census7 done",
        f"width {width}",
        f"chunk {chunk}",
        f"of {nchunks}",
        f"generated {n_generated}",
        f"skipped_passed {n_skipped}",
        f"evaluated {n_evaluated}",
        f"race_errors {n_race}",
        f"other_errors {n_other}",
        f"seconds {dt:.1f}",
        f"race_rule {RACE_RULE}",
        f"passed_respects_ep {PASSED_RESPECTS_EP}",
        f"chunk_rule white_combination_index mod {nchunks}",
    ]
    if tracebacks:
        lines.append(f"tracebacks {len(tracebacks)}")
        for i, tb in enumerate(tracebacks):
            lines.append(f"--- traceback {i + 1} ---")
            lines.extend(tb.rstrip("\n").splitlines())
    else:
        lines.append("tracebacks 0")
    done_path.write_text("\n".join(lines) + "\n")
    print(f"w{width} c{chunk}/{nchunks}: DONE gen={n_generated} skip={n_skipped} "
          f"eval={n_evaluated} race={n_race} other={n_other} {dt:.0f}s", flush=True)
    return 0


# --------------------------------------------------------------------------
# sanity checks
# --------------------------------------------------------------------------
def do_sanity() -> int:
    ok = True
    board = setup(4)
    print("== check 1: the two reference positions evaluate to *2 ==", flush=True)
    for text in EXPECTED:
        p = pawns.Pos.parse(text)
        g = pawns.value(board, p)
        s = cgt.show(g)
        good = (s == "*2" and g.nim == 2)
        ok &= good
        print(f"  {text} -> {s} (nim={g.nim}) {'OK' if good else 'FAIL'}", flush=True)

    print("== check 2: the generator yields them (or their mirror) ==", flush=True)
    geom = Geom(4)
    wanted = {}
    for text in EXPECTED:
        p = pawns.Pos.parse(text)
        white = tuple(sorted(p.white))
        black = tuple(sorted(p.black))
        wanted[white] = text
        wanted[geom.mirror(white)] = text + "  [mirror]"
    found = set()
    n = 0
    for white, black in scope(geom, 0, 1):
        n += 1
        if white in wanted:
            found.add(wanted[white])
    for text in EXPECTED:
        hit = any(text in f for f in found)
        ok &= hit
        print(f"  {text}: {'FOUND' if hit else 'NOT FOUND'}", flush=True)
    print(f"  (scope of width 4 has {n} positions)", flush=True)

    print("== sanity " + ("PASSED" if ok else "FAILED") + " ==", flush=True)
    return 0 if ok else 1


# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--width", type=int)
    ap.add_argument("--chunk", type=int)
    ap.add_argument("--of", type=int, dest="nchunks")
    ap.add_argument("--sanity", action="store_true")
    ap.add_argument("--count", action="store_true",
                    help="count the scope of one width and exit")
    ap.add_argument("--max-positions", type=int, default=0,
                    help="stop after N generated positions (testing only; no .done)")
    args = ap.parse_args()

    if args.sanity:
        return do_sanity()
    if args.count:
        geom = Geom(args.width)
        print(scope_count(geom))
        return 0
    if args.width is None or args.chunk is None or args.nchunks is None:
        ap.error("--width, --chunk and --of are required")
    if not (0 <= args.chunk < args.nchunks):
        ap.error("--chunk must satisfy 0 <= chunk < --of")
    return run_chunk(args.width, args.chunk, args.nchunks, args.max_positions)


if __name__ == "__main__":
    sys.exit(main())