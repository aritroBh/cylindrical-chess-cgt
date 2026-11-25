"""K63 question 3: rough mechanism labels for the disagreements, read from the ref3pv lines (one optimal line each;
another optimal line may show another mechanism, so the labels describe the line printed, not every line).
usage: python3 classify_lines.py <tag> <context files, e.g. g,h>   (reads logs/ctx_<tag>_table.txt, logs/lines_<tag>.out)
Labels (first event in the line that touches the context, then who promotes):
  king-raid      a king captures a context pawn
  pawn-contact   a pawn capture between a group pawn and a context pawn (either direction)
  ctx-promotes   the line ends with a context pawn promoting; grp-promotes: a group pawn promotes
  draw           P result D (no line printed)"""
import re
import sys
from collections import Counter

tag, files = sys.argv[1], sys.argv[2].split(',')
lines = {}
for l in open('logs/lines_%s.out' % tag):
    pos, rest = l.rstrip('\n').split(' | ', 1)
    lines[pos] = rest
dis = []
for l in open('logs/ctx_%s_table.txt' % tag):
    m = re.match(r'^(ctx\d+) \[(.*)\] (q?[AB] [bw]): P (\w), prediction (\w)\s+\((.*)\)$', l.rstrip('\n'))
    if m:
        dis.append(m.groups())
tally = Counter(); out = []
for name, ctx, lab, p, pred, pos in dis:
    rest = lines.get(pos, '')
    ctxsq = set(x[1:] for x in ctx.split())
    lab2 = []
    if p == 'D':
        lab2.append('draw')
    mv = rest.split(' | line: ')[1].split() if ' | line: ' in rest else []
    first = None
    for x in mv:
        x = x.lstrip('.')
        if x[0] in 'Kk' and x.endswith('x') and x[3] in files:
            first = 'king-raid'; break
        if x[0] in 'Pp' and len(x) >= 5 and x[1] != x[3] and (x[1] in files) != (x[3] in files):
            first = 'pawn-contact'; break
    if first:
        lab2.append(first)
    if mv and mv[-1].endswith('=promotes'):
        lab2.append('ctx-promotes' if mv[-1].lstrip('.')[1] in files else 'grp-promotes')
    key = ' + '.join(lab2) if lab2 else 'other'
    tally[key] += 1
    out.append('%s [%s] %s: P %s, pred %s  -> %s' % (name, ctx, lab, p, pred, key))
print('\n'.join(out))
print('# tally:', dict(tally.most_common()))
