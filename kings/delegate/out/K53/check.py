"""Print exhaustive counts as CSV. Optional witness file, created exclusively."""
import argparse
import csv
import sys
from itertools import combinations
from math import comb


def subsets(squares):
    return [p for k in range(4) for p in combinations(squares, k)]


def union(masks):
    result = 0
    for mask in masks:
        result |= mask
    return result


def check(w, h, wrap, writer, witnesses):
    # White to move. Reflection in rank plus colour exchange gives each black turn.
    squares = [(f, r) for r in range(2, h) for f in range(w)]
    layouts = subsets(squares)
    full = (1 << len(layouts)) - 1
    member = {q: 0 for q in squares}
    for i, layout in enumerate(layouts):
        for q in layout:
            member[q] |= 1 << i  # bit i = this black layout contains q

    def adjacent(f, g):
        return abs(f - g) == 1 or (wrap and abs(f - g) == w - 1)

    white_pass = {q: full ^ union(member[g, t] for g, t in squares
                                  if t > q[1] and (g == q[0] or adjacent(g, q[0])))
                  for q in squares}

    # Counters for no target and a fresh target, including inert targets.
    counts = [[0] * 6 for _ in range(2)]
    for white in layouts:
        disjoint = full ^ union(member[q] for q in white)
        white_passed = union(white_pass[q] for q in white)
        unblocked = {q for q in squares
                     if not any(r < q[1] and (f == q[0] or adjacent(f, q[0])) for f, r in white)}
        black_passed = union(member[q] for q in unblocked)
        textbook = full ^ (white_passed | black_passed)

        def promotions(target):
            choices = 0
            for f, r in white:
                if r + 1 == h:
                    # Back rank empty in a pawn context, so the push is available.
                    choices |= full
                    for g in range(w):
                        if adjacent(f, g):
                            choices |= member.get((g, h), 0)  # ordinary capture
                            if (g, h) == target:
                                choices |= full  # e.p. lands on the target
                if r == 2 and r + 2 == h and (f, r + 1) not in white:
                    choices |= full ^ member[f, r + 1]
            return choices

        def record(valid, target, aware):
            promoting = promotions(target)
            t = valid & textbook
            a = valid & aware
            ft, fa = t & promoting, a & promoting
            masks = (valid, valid & promoting, t, a, ft, fa)
            row = counts[target is not None]
            for col, mask in enumerate(masks):
                row[col] += 2 * mask.bit_count()
            if witnesses is None:
                return
            failures = ft | fa
            while failures:
                bit = failures & -failures
                black = layouts[bit.bit_length() - 1]
                for reflect in (False, True):
                    def fmt(pieces):
                        return ' '.join(chr(97 + f) + str(h + 1 - r if reflect else r)
                                        for f, r in pieces) or '-'
                    wp, bp = (black, white) if reflect else (white, black)
                    witnesses.writerow([w, h, 'cyl' if wrap else 'flat', 'B' if reflect else 'W',
                                        fmt(wp), fmt(bp), fmt([target] if target else []),
                                        int(bool(ft & bit)), int(bool(fa & bit))])
                failures ^= bit

        record(disjoint, None, textbook)
        for f in range(w):
            start, target, victim = (f, h - 1), (f, h - 2), (f, h - 3)
            if victim not in member or start in white or target in white:
                continue
            valid = disjoint & member[victim] & ~(member[start] | member[target])
            if not valid:
                continue
            aware = textbook
            if victim in unblocked and any(r == victim[1] and adjacent(g, f) for g, r in white):
                aware = full ^ (white_passed | union(member[q] for q in unblocked if q != victim))
            record(valid, target, aware)

    n = len(squares)
    assert counts[0][0] == 2 * sum(comb(n, i) * comb(n-i, j)
                                    for i in range(4) for j in range(4))
    ep_total = 0 if h == 4 else 2*w*sum(comb(n-3, i) * comb(n-3-i, j)
                                        for i in range(4) for j in range(3))
    assert counts[1][0] == ep_total
    for ep, row in enumerate(counts):
        writer.writerow([w, h, 'cyl' if wrap else 'flat', 'target' if ep else 'none', *row])
    return counts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--witnesses', help='new CSV path for every failed implication')
    args = parser.parse_args()
    sink = open(args.witnesses, 'x', newline='') if args.witnesses else None
    try:
        out = csv.writer(sys.stdout, lineterminator='\n')
        log = csv.writer(sink, lineterminator='\n') if sink else None
        if log:
            log.writerow('files ranks board side white black ep textbook_failure aware_failure'.split())
        out.writerow('files ranks board ep states promotes nonterminal_text nonterminal_aware fail_text fail_aware'.split())
        for height in range(4, 9):
            for width in range(3, 6):
                for cylinder in (False, True):
                    rows = check(width, height, cylinder, out, log)
                    if height == 4:
                        assert rows[0][4] == rows[0][5] > 0
                    else:
                        assert all(row[4:] == [0, 0] for row in rows)
    finally:
        if sink:
            sink.close()
