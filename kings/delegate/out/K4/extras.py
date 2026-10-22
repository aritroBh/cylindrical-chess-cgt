"""More tables for REPORT.md (see tables.py): candidate occurrence, chess result against class,
difference tests, signatures present on one board only, check-1 totals, integer tempo scan."""

import collections
import json
import os

import testgames as tg
from tables import HERE, load, pn, refined, order_key, sig_kind


def why_not_quiet(places, kind, size):
    """For placements of one board, say why each is not a quiet placement on the other board."""
    from kings.ref.solve import make_solver
    sv = make_solver(board='%s:%s' % (kind, size), ep='on', promote='QRBN', cap=1)
    g = sv.g
    out = collections.Counter()
    for pl in places:
        wk, wp, bk = [sv.g.parse_square(t[1:]) for t in pl.split()]
        if wk == bk or g.king_mask[wk] >> bk & 1:
            out['kings adjacent'] += 1
        elif sv.in_check((0, wk, bk, (), 1 << wp, 0, -1), 1):
            out['Black king attacked by the pawn'] += 1
        else:
            out['quiet'] += 1
    return ', '.join('%d: %s' % (n, k) for k, n in out.items()) + ' on the ' + kind + ' board'


def candidate_matrix(sizes):
    """candidate -> {board: number of placements whose signature equals the candidate's}"""
    cands = [n for n, _ in tg.candidates()]
    cols = []
    for size in sizes:
        for kind in ('flat', 'cyl'):
            rows = load(kind, size)
            c = collections.Counter(v for r in rows.values() for v in r['matched'])
            cols.append(('%s %s' % (kind, size), c))
    out = ['| candidate V | ' + ' | '.join(n for n, _ in cols) + ' |', '|---|' + '---:|' * len(cols)]
    for v in cands:
        out.append('| `%s` | ' % tg.pretty(v) + ' | '.join(str(c.get(v, 0)) for _, c in cols) + ' |')
    return '\n'.join(out)


def chess_vs_class(sizes):
    """Class (grouped) against the chess result pair (White to move, Black to move), per board."""
    out = ['| board | class | chess (W-to-move, B-to-move): count |', '|---|---|---|']
    for size in sizes:
        for kind in ('flat', 'cyl'):
            t = collections.defaultdict(collections.Counter)
            for r in load(kind, size).values():
                t[refined(r)][''.join(r['chess'])] += 1
            for c in sorted(t, key=order_key):
                out.append('| %s %s | %s | %s |' % (kind, size, pn(c) if not c.startswith('unmatched') else c,
                           ', '.join('%s: %d' % (k, n) for k, n in sorted(t[c].items()))))
    return '\n'.join(out)


def diff_summary(sizes):
    """Difference test x (+) (-V) per board: placements tested / passed (second-player survival)."""
    out = ['| board | placements with a matched V | difference tests run | second-player survivals |', '|---|---:|---:|---:|']
    for size in sizes:
        for kind in ('flat', 'cyl'):
            rows = load(kind, size)
            n = sum(1 for r in rows.values() if r['matched'])
            run = sum(len(r['diff']) for r in rows.values())
            ok = sum(d['second_player'] for r in rows.values() for d in r['diff'].values())
            out.append('| %s %s | %d | %d | %d |' % (kind, size, n, run, ok))
    return '\n'.join(out)


def unmatched_sigs(size, kind, top=12):
    c = collections.Counter(r['sig'] for r in load(kind, size).values() if r['cls'] == 'unmatched' and not sig_kind(r['sig']))
    return c.most_common(top), len(c)



def decode(sig):
    """32-char signature as 16 pairs (White starts, Black starts), in the order of testgames.TESTS."""
    return ' '.join(sig[i:i + 2] for i in range(0, len(sig), 2))


def check1_table(sizes):
    out = ['| board | positions compared (K+P vs K) | other positions compared (K+officer vs K, K vs K) | differences | KPK positions whose value changes if stalemate is a loss |',
           '|---|---:|---:|---:|---:|']
    tot = [0, 0, 0]
    for size in sizes:
        for kind in ('flat', 'cyl'):
            m = json.load(open(os.path.join(HERE, 'meta_%s_%s.json' % (kind, size))))
            c = m['check1']
            out.append('| %s %s | %d | %d | %d | %d |' % (kind, size, c['kpk'], c['other'], m['check1_differences'],
                                                          c['stale_loss_kpk']))
            tot[0] += c['kpk']
            tot[1] += c['other']
            tot[2] += m['check1_differences']
    out.append('| **all 10 boards** | **%d** | **%d** | **%d** | |' % tuple(tot))
    return '\n'.join(out)


def sig_only(size, top=6):
    """Signatures that occur on one board of a size only: count, and an example placement that is
    quiet on both boards with its class on the other board."""
    flat, cyl = load('flat', size), load('cyl', size)
    out = ['| signature (pairs W-first/B-first for ' + ' '.join(tg.pretty(t) for t in tg.TESTS) + ') | board | count | same placement on the other board |',
           '|---|---|---:|---|']
    for name, a, b, other in (('flat', flat, cyl, 'cyl'), ('cyl', cyl, flat, 'flat')):
        sb = {r['sig'] for r in b.values()}
        cnt = collections.Counter(r['sig'] for r in a.values() if r['sig'] not in sb)
        for sg, n in cnt.most_common(top):
            ex = next((p for p, r in sorted(a.items()) if r['sig'] == sg and p in b), None)
            what = ('`%s` -> %s (%s)' % (ex, pn(refined(b[ex])) if not refined(b[ex]).startswith('unmatched') else refined(b[ex]),
                                          decode(b[ex]['sig']))) if ex else 'no such placement is quiet on both boards'
            out.append('| `%s` | %s | %d | %s |' % (decode(sg), name, n, what))
        if not cnt:
            out.append('| none | %s | 0 | |' % name)
    return '\n'.join(out)


def tempo_table():
    out = ['| board | quiet placements | placements whose results never change with n | with 1 change | with 2 changes | changes between n and n+1 at n = ... (count of placements) | any change at n >= 1 or n <= -3 |',
           '|---|---:|---:|---:|---:|---|---|']
    for line in open(os.path.join(HERE, 'tempo_scan.jsonl')):
        d = json.loads(line)
        nj = d['number_of_jumps']
        out.append('| %s | %d | %d | %d | %d | %s | %s |' % (
            d['board'], d['placements'], nj.get('0', 0), nj.get('1', 0), nj.get('2', 0),
            ', '.join('%s: %d' % kv for kv in d['jump_between_n_and_n_plus_1'].items()) or 'none',
            'no' if d['all_profiles_constant_for_n_ge_2_and_n_le_minus_2'] else 'YES'))
    return '\n'.join(out)


def finite_insensitive(sizes):
    """Placements whose results are the same for all 11 finite tests (0, 1, 2, -1, -2, *, up, down,
    1/2, -1/2, +-1), i.e. no finite test game changes the outcome."""
    out = ['| board | quiet placements | same result for all 11 finite tests |', '|---|---:|---:|']
    for size in sizes:
        for kind in ('flat', 'cyl'):
            rows = load(kind, size)
            n = sum(1 for r in rows.values() if len({r['sig'][i:i + 2] for i in range(0, 22, 2)}) == 1)
            out.append('| %s %s | %d | %d |' % (kind, size, len(rows), n))
    return '\n'.join(out)


if __name__ == '__main__':
    import sys
    sizes = sys.argv[1:]
    print('#### check 1 totals\n'); print(check1_table(sizes))
    print('\n#### candidate occurrence matrix\n'); print(candidate_matrix(sizes))
    print('\n#### class against chess result\n'); print(chess_vs_class(sizes))
    print('\n#### difference tests\n'); print(diff_summary(sizes))
    print('\n#### placements insensitive to every finite test game\n'); print(finite_insensitive(sizes))
    print('\n#### integer scan\n'); print(tempo_table())
    for size in sizes:
        print('\n#### %s signatures on one board only\n' % size); print(sig_only(size))
        for kind in ('flat', 'cyl'):
            top, n = unmatched_sigs(size, kind)
            print('\n%s %s: %d distinct T-dependent unmatched signatures; most common:' % (kind, size, n))
            for sg, k in top:
                print('  %4d  %s' % (k, decode(sg)))
