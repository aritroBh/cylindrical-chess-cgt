#!/usr/bin/env python3
"""T21: re-check every *k (k >= 2) hit of the flat width-5 / 8-pawn scope with cylcgt.

The C solver (`frontier_split`) decides G = *k by testing whether G + *k is a
second-player win.  cylcgt computes the canonical form of G directly.  This
script recomputes each hit with cylcgt at the setting the C solver reported it
at, and in particular at the brief's headline setting (count race rule,
e.p. on, e.p.-aware passed test).

Modes (each can be split into chunks so that no single job is too long):

  --mode headline   every hit, at count / e.p.-on / e.p.-aware
  --mode own        every hit, at each setting the C solver reported it at

Usage:
  PYTHONPATH=. .venv/bin/python research/star2_width5/verify_hits.py \
      --mode headline --chunk 0 --nchunks 8
"""
import argparse
import csv
import gzip
import os
import sys
import time

from cylcgt import cgt, pawns

HERE = os.path.dirname(os.path.abspath(__file__))

# column order of the frontier TSV: race x (ep on textbook | ep off | ep on aware)
SETTINGS = (
    ("count", True, False),
    ("count", False, False),
    ("count", True, True),
    ("mover", True, False),
    ("mover", False, False),
    ("mover", True, True),
    ("opponent", True, False),
    ("opponent", False, False),
    ("opponent", True, True),
)
NAMES = ("C/T", "C/off", "C/aware", "M/T", "M/off", "M/aware", "O/T", "O/off", "O/aware")
HEADLINE = 2  # count / e.p.-aware


def read_rows(path):
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt", newline="") as stream:
        for row in csv.reader(stream, delimiter="\t"):
            if row and not row[0].startswith("#"):
                yield row


def collect_hits():
    hits = {}          # (k, position) -> set of setting indices
    total = 0
    for name in sorted(os.listdir(HERE)):
        if not (name.startswith("split_") and (name.endswith(".tsv") or name.endswith(".tsv.gz"))):
            continue
        for row in read_rows(os.path.join(HERE, name)):
            total += 1
            for setting, field in enumerate(row[3:12]):
                k = int(field.split(",", 1)[1])
                if k >= 2:
                    hits.setdefault((k, row[0]), set()).add(setting)
    return hits, total


def cylcgt_value(text, race, ep_on, aware):
    """Value of `text` under one setting.  The globals must already be set and
    the cache cleared by the caller, so that one cache serves a whole chunk."""
    board = pawns.Board(5, 8, False, ep_on)
    pos = pawns.Pos.parse(text)
    game = pawns.value(board, pos)
    return game, board, pos


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("headline", "own"), required=True)
    parser.add_argument("--chunk", type=int, default=0)
    parser.add_argument("--nchunks", type=int, default=1)
    args = parser.parse_args()

    hits, total = collect_hits()
    sys.stderr.write(f"roots scanned: {total}; distinct *k>=2 hits: {len(hits)}\n")

    # work items: (k, position, setting index), grouped by setting so that one
    # cylcgt cache serves a whole block of positions.
    items = []
    for (k, position), settings in sorted(hits.items()):
        if args.mode == "headline":
            items.append((k, position, HEADLINE))
        else:
            for s in sorted(settings):
                items.append((k, position, s))
    items.sort(key=lambda it: (it[2], it[0], it[1]))
    start = len(items) * args.chunk // args.nchunks
    end = len(items) * (args.chunk + 1) // args.nchunks
    mine = items[start:end]
    sys.stderr.write(f"mode={args.mode} chunk {args.chunk}/{args.nchunks}: {len(mine)} of {len(items)} work items\n")

    out_path = os.path.join(HERE, f"verify_{args.mode}_chunk{args.chunk}.tsv")
    with open(out_path, "w") as out:
        out.write("mode\tc_k\tc_setting\tcylcgt_value\tcylcgt_nim\tcomponents\tagrees\tposition\n")
        current = None
        t0 = time.time()
        for n, (k, position, setting) in enumerate(mine):
            race, ep_on, aware = SETTINGS[setting]
            if current != (race, ep_on, aware):
                pawns.RACE_RULE = race
                pawns.PASSED_RESPECTS_EP = aware
                pawns._value.cache_clear()
                current = (race, ep_on, aware)
            game, board, pos = cylcgt_value(position, race, ep_on, aware)
            nim = game.nim
            agrees = (nim == k)
            out.write(f"{args.mode}\t{k}\t{NAMES[setting]}\t{cgt.show(game)}\t{nim}\t"
                      f"{len(pawns.components(board, pos))}\t{int(agrees)}\t{position}\n")
            out.flush()
            if (n + 1) % 10 == 0:
                sys.stderr.write(f"  {n+1}/{len(mine)} done, {time.time()-t0:.1f}s\n")
    sys.stderr.write(f"wrote {out_path}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
