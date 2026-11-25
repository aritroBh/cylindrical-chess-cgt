"""K63 question 3: compare the P results of F2 + X (ref3m, kp_p --pmodel) with the D-sum predictions of gen_ctx63.py.
usage: python3 cmp_ctx63.py <tag>   (reads in/ctx_<tag>.pos, in/ctx_<tag>.pred, logs/ctx_<tag>_ref3m.out, logs/ctx_<tag>_kpp.out)
Prediction: roots r(over_D (+) X, s) (Corollary 4.17: = r(F2 (+) X, s) in the D-sum); q's r(X, s) (= r(q (+) X, s)).
Positions per context: A b, A w, B b, B w, qA b, qA w, qB b, qB w (A: kc4, B: kc5; qA after b2-b4, qB after b2-b3).
X (illegal position) is skipped.  Prints one line per context, the disagreements, and tallies."""
import sys
from collections import Counter

tag = sys.argv[1]
LAB = ['A b', 'A w', 'B b', 'B w', 'qA b', 'qA w', 'qB b', 'qB w']
pos = [l.rstrip('\n') for l in open('in/ctx_%s.pos' % tag)]


def load(fn, kpp):
    out = {}
    try:
        f = open(fn)
    except FileNotFoundError:
        return None
    for l in f:
        if ' | ' not in l:
            continue
        p, r = l.rstrip('\n').split(' | ', 1)
        t = r.split()
        out[p] = (t[0] if t[0] == t[1] else 'U') if kpp else t[0]
    return out


ref = load('logs/ctx_%s_ref3m.out' % tag, False)
kpp = load('logs/ctx_%s_kpp.out' % tag, True)
preds = []
for l in open('in/ctx_%s.pred' % tag):
    name, rest = l.split(' [', 1)
    ctx, rest = rest.split('] ', 1)
    t = rest.split()
    preds.append((name, ctx, {'ow': t[2], 'ob': t[4], 'zw': t[7], 'zb': t[9]}, t[11] == '1'))
tally = Counter(); bypos = Counter(); solver_diff = 0; rows = []; diffs = []
for k, (name, ctx, pr, ep) in enumerate(preds):
    ps = pos[8 * k: 8 * k + 8]
    want = [pr['ob'], pr['ow'], pr['ob'], pr['ow'], pr['zb'], pr['zw'], pr['zb'], pr['zw']]
    r = [ref.get(p, '?') if ref else '?' for p in ps]
    q = [kpp.get(p, '?') if kpp else '?' for p in ps]
    if ref and kpp:
        solver_diff += sum(1 for a, b in zip(r, q) if a != b)
    bad = [i for i in range(8) if r[i] not in ('X', '?') and r[i] != want[i]]
    nx = sum(1 for v in r if v == 'X')
    for i in range(8):
        if r[i] == 'X':
            bypos['%s X' % LAB[i]] += 1
        elif r[i] == want[i]:
            bypos['%s same' % LAB[i]] += 1
        else:
            bypos['%s differ' % LAB[i]] += 1
    tally['agree' if not bad else 'differ'] += 1
    if nx:
        tally['with an illegal (X) position'] += 1
    rows.append('%-6s %-14s P %s  kp_p %s  pred %s%s' % (name, ctx, ' '.join(r), ' '.join(q), ' '.join(want),
                                                      '' if not bad else '  DIFFER at ' + ', '.join(LAB[i] for i in bad)))
    for i in bad:
        diffs.append('%s [%s] %s: P %s, prediction %s   (%s)' % (name, ctx, LAB[i], r[i], want[i], ps[i]))
print('# context | P results (ref3m) and kp_p at: ' + ', '.join(LAB) + ' (White\'s view) | prediction | verdict')
print('\n'.join(rows))
print('# disagreements (%d):' % len(diffs))
print('\n'.join(diffs))
print('# contexts %d: %s' % (len(preds), dict(tally)))
print('# per position:', dict(sorted(bypos.items())))
print('# ref3m vs kp_p differences: %s' % (solver_diff if ref and kpp else 'not both run'))
