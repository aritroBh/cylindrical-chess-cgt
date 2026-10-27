"""Check the Q_22 base graph and Lemma 2(b) on its actual reduced nodes."""

from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/ring_n_plus_2_proof/verify_compute"))
import myeng as M


def tokens(n):
    assert n >= 8 and n % 2 == 0
    return (['W4', 'B7'] + ['B4', 'W2'] * ((n - 8) // 2)
            + ['W3B6', 'W3', 'W2B5', 'B5', 'W2', 'B4'])


def classify_one(pos, ep, side, child):
    result = M.verdict(child[0], child[1], side)
    if result == side:
        return 'T'
    other = 1 - side
    if result == other:
        return 'L'
    for reply_pos, reply_ep in M.gen_moves(child[0], child[1], other):
        if M.verdict(reply_pos, reply_ep, other) == other:
            return 'P'
    return 'K'


def main():
    n = 22
    start = tuple(M.parse_file(t) for t in tokens(n))
    graph = M.Graph(start)
    stats = graph.stats()
    expected_zone = [0, 1, 2, 3, *range(15, 20), 21]
    assert stats['nodes'] == 7968, stats
    assert stats['flagged'] == 0, stats
    assert stats['zone'] == expected_zone, stats
    signature = graph.signature(range(5))
    assert signature == 'NNNPN', signature

    pattern = {j: M.parse_file('B4' if j % 2 == 0 else 'W2')
               for j in range(2, n - 6)}
    for pos, ep in graph.order:
        assert ep is None
        assert not M.passed_pawns(pos, ep, M.W)
        assert not M.passed_pawns(pos, ep, M.B)
        assert all(pos[j] == pattern[j] for j in range(4, 15))

    stable = set(range(4, 15))
    windows = {}
    for j in range(5, 14):
        if all(k in stable for k in range(j - 1, j + 4)):
            windows[j] = (j - 1, j + 3)
        else:
            assert all(k in stable for k in range(j - 3, j + 2)), j
            windows[j] = (j - 3, j + 1)
    assert windows[5] == (4, 8) and windows[13] == (10, 14), windows

    positions = Counter()
    moves_a = moves_b = 0
    classes = Counter()
    by_end = Counter()
    for pos, ep in graph.order:
        for side in (M.W, M.B):
            for j, (lo, hi) in windows.items():
                rank_bits = pos[j][side]
                if not rank_bits:
                    continue
                assert pos[j] == pattern[j]
                ranks = list(M.bits(rank_bits))
                assert len(ranks) == 1, (j, ranks)
                positions[j] += 1
                for child in M.gen_moves(pos, ep, side, only=(j, ranks[0])):
                    moves_a += 1
                    assert not M.passed_pawns(child[0], child[1], side), (j, side)
                    kind = classify_one(pos, ep, side, child)
                    moves_b += 1
                    classes[(j, kind)] += 1
                    if kind not in 'LP':
                        raise AssertionError((j, side, kind))
                    if j in (5, 13):
                        by_end[(j, kind)] += 1

    assert moves_a == moves_b
    assert positions[5] == stats['nodes'] and positions[13] == stats['nodes']
    print('Q_22 reduced graph:', stats)
    print(f'reduced-game signature h=0..4: {signature}')
    print('pattern files fixed in every node: 4..14')
    print('applicable windows by q file:', windows)
    print('Lemma 2(b) windows at wall-arc ends: j=5 -> 4..8, j=13 -> 10..14')
    print(f'actual nodes checked: {stats["nodes"]}; q positions={sum(positions.values())}; '
          f'moves={moves_b}; Lemma 2(a) failures=0; Lemma 2(b) T/K failures=0')
    print('moves by j and class:', dict(sorted(classes.items())))
    print('end-window moves by j and class:', dict(sorted(by_end.items())))


if __name__ == '__main__':
    main()
