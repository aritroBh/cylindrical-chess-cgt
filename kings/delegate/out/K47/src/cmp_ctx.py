"""K47 item 3: compare the P results of Z_O beside each context (ref3m, kp_p) with r(over + C) (gen_ctx.py's .pred).
usage: python3 cmp_ctx.py <tag>  (reads ctx_<tag>.pos, ctx_<tag>.pred, logs/ctx_<tag>.ref3m, logs/ctx_<tag>.kpp)
Prints a table (one line per context: the four roots d4/b d4/w d5/b d5/w for each solver, and over's w/b) and a tally."""
import sys
from collections import Counter

tag = sys.argv[1]
pos = [l.rstrip('\n') for l in open('ctx_%s.pos' % tag)]


def load(fn, kpp):
    out = {}
    for l in open(fn):
        if ' | ' not in l: continue
        p, r = l.rstrip('\n').split(' | ', 1)
        t = r.split()
        if kpp:
            out[p] = t[0] if t[0] == t[1] else 'U'  # bounds A, B; equal = exact in P (no officers, cap irrelevant in P)
        else:
            out[p] = t[0]
    return out


ref = load('logs/ctx_%s.ref3m' % tag, False)
try:
    kpp = load('logs/ctx_%s.kpp' % tag, True)
except FileNotFoundError:
    kpp = {}
pred = []
for l in open('ctx_%s.pred' % tag):
    name, rest = l.rstrip('\n').split('] ', 1)
    t = rest.split()
    pred.append((name + ']', t[1], t[3]))
tally = Counter(); solver_diff = 0; rows = []
for k, (name, pw, pb) in enumerate(pred):
    ps = pos[4 * k: 4 * k + 4]  # order: d4 b, d4 w, d5 b, d5 w
    r = [ref.get(p, '?') for p in ps]
    q = [kpp.get(p, '?') for p in ps]
    if kpp:
        solver_diff += sum(1 for a, b in zip(r, q) if a != b)
    want = [pb, pw, pb, pw]
    agree = all(a == b for a, b in zip(r, want) if a != 'X')
    tally['agree' if agree else 'differ'] += 1
    rows.append("%-28s ref3m %s  kp_p %s  over+C: w %s b %s  %s" % (name, " ".join(r), " ".join(q), pw, pb, 'same' if agree else 'DIFFERENT'))
print("# context | P results at (d4,b) (d4,w) (d5,b) (d5,w), White's view | r(over + C) White/Black to move | same or not (X ignored)")
print("\n".join(rows))
print("# contexts %d, %s; ref3m vs kp_p differences: %s" % (len(pred), dict(tally), solver_diff if kpp else 'kp_p not run'))
