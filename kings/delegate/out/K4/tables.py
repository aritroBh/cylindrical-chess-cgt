"""Markdown tables for REPORT.md, computed from the <board>.jsonl files.

    PYTHONPATH=. .venv/bin/python kings/delegate/out/K4/tables.py 3x4 4x4 3x5 4x5 5x5   (prints markdown)

extras.py and reptables.py have the other tables; claims.py recomputes the numbers a report quotes and asserts the
structural claims; mkreport.py prints all of it to stdout.
"""

import collections
import json
import os
import sys

import testgames as tg

HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = tg.TESTS
DECISIVE = ('WHITE-WINS-ALL', 'BLACK-WINS-ALL')


def load(kind, size):
    path = os.path.join(HERE, '%s_%s.jsonl' % (kind, size))
    return {r['placement']: r for r in map(json.loads, open(path))}


def pn(label):
    """pretty class label (code-quoted so that * and | survive markdown)"""
    if label.startswith('unmatched'):
        return label
    if label in DECISIVE:
        return '`' + label + '`'
    return '`' + '/'.join(tg.pretty(x) for x in label.split('/')) + '`'


def sig_kind(sig):
    """'ab' if the signature is T-independent (the same pair for every T), else None."""
    pairs = {sig[i:i + 2] for i in range(0, len(sig), 2)}
    return pairs.pop() if len(pairs) == 1 else None


def refined(r):
    """class, with the unmatched ones split into T-independent pairs and 'T-dependent'."""
    if r['cls'] != 'unmatched':
        return r['cls']
    k = sig_kind(r['sig'])
    return 'unmatched, T-independent (White first: %s, Black first: %s)' % (k[0], k[1]) if k else 'unmatched, T-dependent'


def order_key(label):
    base = ['WHITE-WINS-ALL', 'BLACK-WINS-ALL']
    cand = [n for n, _ in tg.candidates()]
    if label in base:
        return (0, base.index(label))
    if label.startswith('unmatched'):
        return (2, label)
    return (1, cand.index(label.split('/')[0]))


def share(n, tot):
    return '%d (%.1f%%)' % (n, 100.0 * n / tot) if n else '0'


def class_table(flat, cyl, key=lambda r: r['cls']):
    cf = collections.Counter(key(r) for r in flat.values())
    cc = collections.Counter(key(r) for r in cyl.values())
    ex = lambda rows, c: next((p for p, r in sorted(rows.items()) if key(r) == c), '')
    out = ['| class | flat count (share) | flat example | cyl count (share) | cyl example |', '|---|---:|---|---:|---|']
    for c in sorted(set(cf) | set(cc) | set(DECISIVE), key=order_key):     # both extremes are always listed
        out.append('| %s | %s | %s | %s | %s |' % (pn(c),
                   share(cf.get(c, 0), len(flat)), ex(flat, c) or '-', share(cc.get(c, 0), len(cyl)), ex(cyl, c) or '-'))
    out.append('| **total quiet placements** | **%d** | | **%d** | |' % (len(flat), len(cyl)))
    return '\n'.join(out), cf, cc


def one_board(flat, cyl, cf, cc, key=lambda r: r['cls'], size=None):
    common = sorted(set(flat) & set(cyl))
    def reasons(a, b, c, other_name):
        from extras import why_not_quiet
        return why_not_quiet([p for p in a if key(a[p]) == c], other_name, size)

    lines = ['Placements quiet on both boards: %d; of these %d change class when the edges go.' % (
        len(common), sum(key(flat[p]) != key(cyl[p]) for p in common))]
    for name, mine, other, a, b in (('flat', cf, cc, flat, cyl), ('cyl', cc, cf, cyl, flat)):
        other_name = 'cyl' if name == 'flat' else 'flat'
        only = sorted((c for c in mine if c not in other), key=order_key)
        if not only:
            lines.append('- Classes only on the %s board: none.' % name)
            continue
        for c in only:
            ex = [p for p in common if key(a[p]) == c][:2]
            if ex:
                s = '; '.join('`%s`: %s -> %s' % (p, pn(key(flat[p])), pn(key(cyl[p]))) for p in ex)
            else:
                s = 'none exists: no placement of this class is quiet on both boards (%s)' % reasons(a, b, c, other_name)
            lines.append('- Only on %s: **%s** (%d placements). Same placement, other board (flat -> cyl): %s' % (
                name, pn(c), mine[c], s))
    return '\n'.join(lines)


def transitions(flat, cyl, key=lambda r: r['cls'], top=8):
    """The most common changes of class for one and the same placement (quiet on both boards)."""
    common = sorted(set(flat) & set(cyl))
    t = collections.Counter((key(flat[p]), key(cyl[p])) for p in common if key(flat[p]) != key(cyl[p]))
    out = ['%d kinds of change; the %d most common (same placement, flat board -> cylinder):' % (len(t), min(top, len(t))),
           '', '| flat class | cyl class | placements | example placement |', '|---|---|---:|---|']
    for (a, b), n in t.most_common(top):
        ex = next(p for p in common if (key(flat[p]), key(cyl[p])) == (a, b))
        out.append('| %s | %s | %d | `%s` |' % (pn(a), pn(b), n, ex))
    return '\n'.join(out)


def chess_table(rows):
    """class -> chess result pairs (White to move, Black to move)"""
    t = collections.defaultdict(collections.Counter)
    for r in rows.values():
        t[r['cls']][''.join(r['chess'])] += 1
    return {c: dict(v) for c, v in t.items()}


if __name__ == '__main__':
    sizes = sys.argv[1:]
    for size in sizes:
        flat, cyl = load('flat', size), load('cyl', size)
        print('\n#### %s\n' % size)
        tab, cf, cc = class_table(flat, cyl, refined)
        print(tab)
        print()
        print(one_board(flat, cyl, cf, cc, refined, size))
        print()
        print(transitions(flat, cyl, refined))
