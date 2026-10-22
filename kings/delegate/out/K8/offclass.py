"""K8: count the White-stalemated placements directly, to compare with the off / off+* class of the signatures.

    PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K8/offclass.py cyl:5x4 flat:4x6 ...

For every quiet K+P vs K placement (neither king in check) it asks the move generator of kings/ref/solve.py whether the side to
move has a legal move.  `white_stalemated` = White to move, not in check, no legal move; `black_stalemated` likewise for Black.
The off / off+* class is read from <board>.jsonl (written by gafni.py) when that file exists, and compared.  Writes
offclass_<board>.json.  Nothing here uses the product solver or the test games.
"""
import json
import os
import sys

from kings.ref.solve import make_solver

HERE = os.path.dirname(os.path.abspath(__file__))
WHITE, BLACK = 0, 1


def count(board):
    S = make_solver(board=board, ep='on', promote='QRBN', cap=1)
    g = S.g
    quiet = wst = bst = 0
    wex, bex = [], []
    for wk in range(g.N):
        for bk in range(g.N):
            if wk == bk or g.king_mask[wk] >> bk & 1:
                continue
            for wp in range(g.N):
                if wp in (wk, bk) or g.rank[wp] in (0, g.H - 1):
                    continue
                pw = (WHITE, wk, bk, (), 1 << wp, 0, -1)
                pb = (BLACK, wk, bk, (), 1 << wp, 0, -1)
                if S.in_check(pw, WHITE) or S.in_check(pw, BLACK):
                    continue                                    # not a quiet placement
                quiet += 1
                nq, qs, ex = S.moves(pw, full=True)
                if nq == 0 and not ex:
                    wst += 1
                    wex.append('K%s P%s k%s' % (g.sqname(wk), g.sqname(wp), g.sqname(bk)))
                nq, qs, ex = S.moves(pb, full=True)
                if nq == 0 and not ex:
                    bst += 1
                    bex.append('K%s P%s k%s' % (g.sqname(wk), g.sqname(wp), g.sqname(bk)))
    return quiet, wex, bex


def main(boards):
    for board in boards:
        tag = board.replace(':', '_')
        quiet, wex, bex = count(board)
        rec = dict(label='COMPUTED-1', board=board, quiet=quiet, white_stalemated=len(wex), black_stalemated=len(bex),
                   white_stalemated_placements=wex[:40], black_stalemated_examples=bex[:8])
        path = os.path.join(HERE, tag + '.jsonl')
        if os.path.exists(path):
            off = {json.loads(x)['placement'] for x in open(path) if 'off' in json.loads(x)['matched']}
            rec['off_class_from_signatures'] = len(off)
            rec['off_class_equals_white_stalemated'] = off == set(wex)
        json.dump(rec, open(os.path.join(HERE, 'offclass_%s.json' % tag), 'w'), indent=1)
        print(json.dumps({k: v for k, v in rec.items() if k not in ('white_stalemated_placements', 'black_stalemated_examples')}),
              flush=True)


if __name__ == '__main__':
    main(sys.argv[1:])
