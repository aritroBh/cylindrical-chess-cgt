"""Audit classification differences and LOOPY's stronger-claim counts."""
import argparse
import csv
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent


def differences(w, h, wrap, cap, require_empty_origin):
    # A difference requires that the victim was the sole textbook passer.
    squares = [(f, r) for f in range(w) for r in range(2, h)]
    for f in range(w):
        def near(g, j):
            return abs(g-j) <= 1 or (wrap and abs(g-j) == w-1)

        victim = f, h-3
        excluded = {victim, (f, h-2)}
        if require_empty_origin:
            excluded.add((f, h-1))
        free = [q for q in squares if q not in excluded]
        possible_white = [(g,r) for g,r in free if r >= h-3 or not near(f,g)]
        for i in range(1, cap+1):
            for white in combinations(possible_white, i):
                if not any(r == h-3 and near(f,g) for g,r in white):
                    continue
                # Every other black pawn must have a white pawn ahead.
                extras = [(g,r) for g,r in free if (g,r) not in white
                          and any(y < r and near(x,g) for x,y in white)]
                for j in range(cap):
                    for extra in combinations(extras, j):
                        black = (victim, *extra)
                        if all(any(y > r and near(g,x) for x,y in black) for g,r in white):
                            yield white, black, (f, h-2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--differences', help='new CSV path for individual classification differences')
    args = parser.parse_args()
    with (HERE / 'counts.csv').open() as f:
        rows = list(csv.DictReader(f))
    print('ranks states promotes nonterminal_text nonterminal_aware fail_text fail_aware')
    for heights in [(4,), (5,6,7,8)]:
        print(f'{heights[0]}-{heights[-1]}', *(sum(int(row[key]) for row in rows
              if int(row['ranks']) in heights) for key in list(rows[0])[4:]))
    print('ranks stronger_claim_origin_unchecked stronger_claim_origin_empty')
    for h in range(5,9):
        print(h, *(2*sum(any(r == h-1 for f,r in white) or any(r == 2 for f,r in black)
                         for white, black, target in differences(4, h, False, 2, strict))
                   for strict in (False, True)))
    if args.differences:
        with open(args.differences, 'x', newline='') as f:
            log = csv.writer(f, lineterminator='\n')
            log.writerow('files ranks board side white black ep'.split())
            for row in rows:
                if row['ep'] == 'none' or row['ranks'] == '4':
                    assert row['nonterminal_text'] == row['nonterminal_aware']
                    continue
                w, h = int(row['files']), int(row['ranks'])
                count = 0
                for white, black, target in differences(w,h,row['board']=='cyl',3,True):
                    for reflect in (False, True):
                        def fmt(pieces):
                            return ' '.join(chr(97+g) + str(h+1-r if reflect else r) for g,r in pieces)
                        wp, bp = (black, white) if reflect else (white, black)
                        log.writerow([w,h,row['board'],'B' if reflect else 'W',fmt(wp),fmt(bp),fmt([target])])
                        count += 1
                assert count == int(row['nonterminal_aware']) - int(row['nonterminal_text'])
