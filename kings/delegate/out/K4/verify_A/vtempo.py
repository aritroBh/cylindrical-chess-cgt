"""Verifier A, extra: tempo scan.  For each quiet placement, profile(n) = (r(x+n, W starts), r(x+n, B starts))
for integers n in -R..R; a jump is a change of profile between n and n+1.  usage: vtempo.py board [R]."""
import json
import os
import sys
import vgraph
import vproduct as pr

HERE = os.path.dirname(os.path.abspath(__file__))
K4 = os.path.dirname(HERE)


def integer(n):
    """The integer n as an explicit chain game, root = node 0."""
    if n == 0:
        return [[]], [[]]
    k = abs(n)
    if n > 0:
        lo = [[i + 1] for i in range(k)] + [[]]
        ro = [[] for _ in range(k + 1)]
    else:
        lo = [[] for _ in range(k + 1)]
        ro = [[i + 1] for i in range(k)] + [[]]
    return lo, ro


def main():
    board = sys.argv[1]
    R = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    G = vgraph.build(board)
    nodes = [(G.index[(0, wk, bk, (), 1 << p, 0, -1)], G.index[(1, wk, bk, (), 1 << p, 0, -1)]) for _, wk, p, bk in G.places]
    prof = {}
    for n in range(-R, R + 1):
        g = integer(n)
        ng = len(g[0])
        res = pr.solve(G, g)
        prof[n] = [(res[a * ng], res[b * ng]) for a, b in nodes]
    num, where = {}, {}
    beyond, examples = 0, []
    for i in range(len(nodes)):
        jumps = [n for n in range(-R, R) if prof[n][i] != prof[n + 1][i]]
        num[len(jumps)] = num.get(len(jumps), 0) + 1
        for n in jumps:
            where[n] = where.get(n, 0) + 1
        if any(n < -2 or n > 1 for n in jumps):
            beyond += 1
            if len(examples) < 3:
                examples.append(G.places[i][0])
    const_tail = all(prof[n][i] == prof[2][i] for n in range(2, R + 1) for i in range(len(nodes))) and \
        all(prof[n][i] == prof[-2][i] for n in range(-R, -1) for i in range(len(nodes)))
    mine = {'board': board, 'placements': len(nodes), 'number_of_jumps': {str(k): v for k, v in sorted(num.items())},
            'jump_between_n_and_n_plus_1': {str(k): v for k, v in sorted(where.items())},
            'placements_with_a_jump_beyond_pm2': beyond, 'examples_beyond_pm2': examples,
            'all_profiles_constant_for_n_ge_2_and_n_le_minus_2': const_tail}
    builder = None
    for ln in open(os.path.join(K4, 'tempo_scan.jsonl')):
        d = json.loads(ln)
        if d['board'] == board:
            builder = d
    same = builder is not None and all(builder[k] == mine[k] for k in mine)
    print(json.dumps(mine))
    print('builder:', json.dumps(builder))
    print('TEMPO-SCAN SAME AS BUILDER:', same)


if __name__ == '__main__':
    main()
