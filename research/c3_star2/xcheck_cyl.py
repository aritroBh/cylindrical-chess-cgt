"""CHECKED-2 for the walk-through: cylcgt versus the independent C solver (research/star2_frontier/frontier.c,
copied as research/c3_star2/cyl_eval.c with cylinder adjacency enabled for --eval).

Random cylinder positions on 3 and 4 files (2-3 pawns per side, ranks 2-7, no passers on both sides at the root).
Compares the 9 settings: race rule x (e.p. off | e.p. on textbook | e.p. on aware).
Output: summary counts; any disagreement printed in full.

Run: PYTHONPATH=. .venv/bin/python research/c3_star2/xcheck_cyl.py
"""
import random
import subprocess
import sys
from cylcgt import pawns, cgt

HERE = "research/c3_star2"
EVAL = f"{HERE}/cyl_eval"
RACES = ["count", "mover", "opponent"]
SETTINGS = []  # (race, ep_on, aware) in the C column order
for r in RACES:
    SETTINGS += [(r, True, False), (r, False, False), (r, True, True)]


def random_position(rng, files):
    sq = [(f, r) for f in range(1, files + 1) for r in range(2, 8)]
    n_w = rng.randint(2, 3)
    n_b = rng.randint(2, 3)
    picks = rng.sample(sq, n_w + n_b)
    w = frozenset((f - 1, r) for f, r in picks[:n_w])
    b = frozenset((f - 1, r) for f, r in picks[n_w:])
    return pawns.Pos(w, b)


def text(pos):
    w = " ".join(sorted(pawns.name(s) for s in pos.white))
    b = " ".join(sorted(pawns.name(s) for s in pos.black))
    return f"W: {w} / B: {b}"


def cgt_class(g, nim_check=True):
    k = -1
    if nim_check:
        for q in range(0, 16):
            if cgt.nimber(q) is g:
                k = q
                break
    return cgt.outcome(g), k


def cylcgt_setting(files, pos, setting):
    race, ep_on, aware = setting
    pawns.RACE_RULE = race
    pawns.PASSED_RESPECTS_EP = aware
    pawns._value.cache_clear()
    board = pawns.Board(files, 8, True, ep_on)
    return pawns.value(board, pos)


def main(n_per_width=25, seed=20261022):
    rng = random.Random(seed)
    cases = []
    for files in (3, 4):
        made = 0
        while made < n_per_width:
            pos = random_position(rng, files)
            wp = pawns.passed(pawns.Board(files, 8, True, True), pos, "W")
            bp = pawns.passed(pawns.Board(files, 8, True, True), pos, "B")
            if wp and bp:
                continue
            cases.append((files, pos))
            made += 1
    # C solver: one run per width
    total = {}
    bad = []
    n_cases = 0
    for files in (3, 4):
        group = [(f, p) for f, p in cases if f == files]
        inp = "\n".join(f"{text(p)}\t{f}" for f, p in group) + "\n"
        path = f"{HERE}/xcheck_in_{files}.tsv"
        open(path, "w").write(inp)
        out = subprocess.run([EVAL, "--eval", path, "--cylinder"], capture_output=True, text=True, check=True).stdout
        rows = [ln.split("\t") for ln in out.strip().split("\n") if not ln.startswith("#")]
        assert len(rows) == len(group), (len(rows), len(group))
        for (f, p), row in zip(group, rows):
            n_cases += 1
            cvals = row[3:]
            for si, setting in enumerate(SETTINGS):
                g = cylcgt_setting(f, p, setting)
                oc, k = cgt_class(g)
                ccls, cnim = cvals[si].split(",")
                key = (f, setting)
                total.setdefault(key, [0, 0])
                total[key][0] += 1
                # the C solver reports outcome of G and the nimber k (or -1); cylcgt nimber from identity check
                agree = (oc == ccls) and (k == int(cnim))
                if agree:
                    total[key][1] += 1
                else:
                    bad.append((f, text(p), setting, cgt.show(g), oc, k, cvals[si]))
    print(f"positions: {n_cases} (3 files and 4 files, seed {seed}); settings checked: {len(SETTINGS)}")
    agree_all = sum(v[1] for v in total.values())
    tot_all = sum(v[0] for v in total.values())
    print(f"agreements (outcome class and nimber): {agree_all} / {tot_all}")
    for key, (t, a) in sorted(total.items(), key=lambda x: (x[0][0], x[0][1])):
        print(f"  {key[0]} files, {key[1][0]}, e.p. {'on' if key[1][1] else 'off'}, {'aware' if key[1][2] else 'textbook'}: {a}/{t}")
    print("disagreements:", len(bad))
    for b in bad[:20]:
        print("  ", b)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 25)
