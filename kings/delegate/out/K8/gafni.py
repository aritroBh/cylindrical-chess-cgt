"""K4 driver: signatures of K+P vs K quiet placements against 16 test games, flat and cylinder.

    PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K4/gafni.py flat:3x4 cyl:3x4 ...

Per board it (1) builds the chess graph, (2) runs check 1 against kpsolve (stops if any difference),
(3) solves x (+) T for the 16 test games T and, for every candidate V that some placement matches,
x (+) (-V), (4) writes <flat|cyl>_<W>x<H>.jsonl (one line per quiet placement) and meta_<board>.json.
Check 2 (pure CGT facts) is run once, first, by checks.py and must pass.
"""

import json
import os
import sys
import time

import checks
import check1
import graph
import testgames as tg
from product import solve_product, pure

HERE = os.path.dirname(os.path.abspath(__file__))
DIFF_W_OK = ('D', 'L')      # White starts: second-player survival means White does not win
DIFF_B_OK = ('D', 'W')      # Black starts: Black does not win


def candidate_signatures():
    """{name: 32-char signature} of V (+) T for the 26 candidates V and 16 test games T."""
    out = {}
    for name, V in tg.candidates():
        sig = ''
        for t in tg.TESTS:
            a, b = pure(tg.plus(V, tg.GAMES[t]))
            sig += a + b
        out[name] = sig
    return out


def signatures(cg):
    """{(white-to-move node, black-to-move node): 32-char signature} over the quiet KPK placements."""
    sigs = {pair: [] for pair in cg.quiet_kpk}
    for t in tg.TESTS:
        T = tg.GAMES[t]
        res = solve_product(cg, T)
        for cw, cb in cg.quiet_kpk:
            sigs[(cw, cb)].append('DWL'[res[cw * T.n + T.start]] + 'DWL'[res[cb * T.n + T.start]])
    return {k: ''.join(v) for k, v in sigs.items()}


def process(board, cand_sigs, workdir):
    t0 = time.time()
    cg = graph.ChessGraph(board)
    c1 = check1.check1(cg, os.path.join(workdir, 'check1'))
    if c1['diffs']:
        print('CHECK 1 FAILED on', board, c1['diffs'][:10])
        json.dump(c1, open(os.path.join(workdir, 'FAILED_check1_%s.json' % board.replace(':', '_')), 'w'), indent=1)
        sys.exit(2)
    sigs = signatures(cg)
    chess = solve_product(cg, tg.GAMES['0'], stalemate_draw=True)
    by_sig = {}
    for name, s in cand_sigs.items():
        by_sig.setdefault(s, []).append(name)
    matched = {pair: by_sig.get(s, []) for pair, s in sigs.items()}
    # difference tests: x (+) (-V) for every V that some placement matches
    used = sorted({v for m in matched.values() for v in m}, key=list(cand_sigs).index)
    cands = dict(tg.candidates())
    diff = {}
    for v in used:
        nv = tg.neg(cands[v])
        res = solve_product(cg, nv)
        diff[v] = {pair: ('DWL'[res[pair[0] * nv.n + nv.start]], 'DWL'[res[pair[1] * nv.n + nv.start]])
                   for pair in cg.quiet_kpk}
    path = os.path.join(workdir, board.replace(':', '_') + '.jsonl')
    n_all_w = n_all_l = n_unm = 0
    with open(path, 'w') as f:
        for pair in sorted(cg.quiet_kpk, key=lambda p: cg.placement(p[0])):
            cw, cb = pair
            sig = sigs[pair]
            dec = 'W' if set(sig) == {'W'} else 'L' if set(sig) == {'L'} else None
            m = matched[pair]
            cls = ('WHITE-WINS-ALL' if dec == 'W' else 'BLACK-WINS-ALL' if dec == 'L'
                   else '/'.join(m) if m else 'unmatched')
            n_all_w += dec == 'W'
            n_all_l += dec == 'L'
            n_unm += (not m and dec is None)
            stm, wk, bk, offs, wp, bp, ep = cg.pos[cw]
            line = dict(board=board, placement=cg.placement(cw),
                        wk=cg.sqname(wk), p=cg.sqname(wp.bit_length() - 1), bk=cg.sqname(bk),
                        sig=sig, decisive=dec, matched=m, cls=cls,
                        chess=['DWL'[chess[cw]], 'DWL'[chess[cb]]],
                        diff={v: dict(white_starts=diff[v][pair][0], black_starts=diff[v][pair][1],
                                      second_player=(diff[v][pair][0] in DIFF_W_OK and diff[v][pair][1] in DIFF_B_OK))
                              for v in m})
            f.write(json.dumps(line, ensure_ascii=False) + '\n')
    c1meta = {k: v for k, v in c1.items() if k not in ('diffs', 'mutual_placements', 'kpk_outcomes')}
    c1meta['mutual_zugzwangs'] = c1['mutual_zugzwangs']
    c1meta['mutual_examples'] = c1['mutual_placements'][:5]
    meta = dict(board=board, nodes=cg.n, edges=len(cg.succ), kpk_positions=len(cg.kpk),
                quiet_placements=len(cg.quiet_kpk), check1=c1meta,
                check1_differences=len(c1['diffs']), decisive_white=n_all_w, decisive_black=n_all_l,
                unmatched=n_unm, seconds=round(time.time() - t0, 1), jsonl=os.path.basename(path))
    json.dump(meta, open(os.path.join(workdir, 'meta_%s.json' % board.replace(':', '_')), 'w'), indent=1)
    print(board, meta, flush=True)
    return meta


def main(argv):
    c2 = checks.check2()
    for desc, exp, got, reading, ok in c2:
        print('check2 %-4s %-22s %s' % ('PASS' if ok else 'FAIL', desc, got))
    if not all(r[4] for r in c2):
        sys.exit('check 2 failed')
    cand = candidate_signatures()
    json.dump(dict(tests=tg.TESTS, order='for each test game: White-starts char, Black-starts char',
                   candidates=cand), open(os.path.join(HERE, 'candidates.json'), 'w'), indent=1)
    for board in argv:
        process(board, cand, HERE)


if __name__ == '__main__':
    main(sys.argv[1:])
