#!/usr/bin/env python
"""verify_hits.py HITS.tsv [HITS2.tsv ...]

Recompute, with cylcgt, the value of every position listed in a frontier_split
hits file and compare it with the scanner's nimber.

A hits file is a TSV whose header names the settings, e.g.

    #position  width  npawns  count/epon  count/epoff  count/epon/aware  ...

Column 4.. are "outcome,nimber" (nimber -1 = "not a nimber").

The scanner's settings map onto cylcgt as follows:

    setting name          RACE_RULE      PASSED_RESPECTS_EP   board.ep
    count/epon            count          False                True
    count/epoff           count          False                False
    count/epon/aware      count          True                 True
    mover/epon            mover          False                True
    mover/epoff           mover          False                False
    mover/epon/aware      mover          True                 True
    opponent/epon         opponent       False                True
    opponent/epoff        opponent       False                False
    opponent/epon/aware   opponent       True                 True

Exit status 0 if every position agrees.
"""
import sys

sys.path.insert(0, ".")
from cylcgt import cgt, pawns  # noqa: E402

RACE = {"count": "count", "mover": "mover", "opponent": "opponent"}


def setting_params(name):
    race, _, rest = name.partition("/")
    ep = rest.startswith("epon")
    aware = rest.endswith("aware")
    return RACE[race], aware, ep


def clear_caches():
    for fn in (pawns._value.cache_clear,):
        fn()


def main(paths):
    total = ok = 0
    bad = []
    for path in paths:
        with open(path) as fh:
            header = fh.readline().rstrip("\n").split("\t")
            names = header[3:]
            cols = {n: 4 + i for i, n in enumerate(names)}
            for line in fh:
                f = line.rstrip("\n").split("\t")
                if len(f) < 4:
                    continue
                pos_text, width = f[0], int(f[1])
                pos = pawns.Pos.parse(pos_text)
                for name in names:
                    race, aware, ep = setting_params(name)
                    pawns.RACE_RULE = race
                    pawns.PASSED_RESPECTS_EP = aware
                    clear_caches()
                    board = pawns.Board(width, 8, True, ep)
                    g = pawns.value(board, pos)
                    nim = g.nim if g.nim is not None else -1
                    got = f[cols[name] - 1].split(",")[1]
                    total += 1
                    if int(got) == nim:
                        ok += 1
                    else:
                        bad.append((path, pos_text, width, name, got, nim,
                                    cgt.show(g)))
    print(f"checked {total} (position, setting) pairs; {ok} agree, {len(bad)} disagree")
    for b in bad:
        print("  MISMATCH", b)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
