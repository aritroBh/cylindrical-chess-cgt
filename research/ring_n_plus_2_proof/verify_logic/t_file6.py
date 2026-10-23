import collections
from engine import *
n = 18
start = parse(P_toks(n))
order, edges = build(start)
cnt = collections.Counter(); ex = {}
for nd in order:
    pos = nd[0]
    for side in 'WB':
        for c, npos, nep, src, kind, pr in classify(pos, nd[1], side):
            if c == 'K' and src == 6:
                key = (side, kind, fmt_file(pos[6]), '->', fmt_file(npos[6]), '| f5', fmt_file(pos[5]), fmt_file(npos[5]), '| f7', fmt_file(pos[7]), fmt_file(npos[7]))
                cnt[key] += 1
for k, v in sorted(cnt.items(), key=lambda x: -x[1])[:20]:
    print(v, k)
print('distinct file-6 contents in nodes', sorted({fmt_file(nd[0][6]) for nd in order}))
print('distinct file-5 contents in nodes', sorted({fmt_file(nd[0][5]) for nd in order}))
print('distinct file-0 contents', sorted({fmt_file(nd[0][0]) for nd in order}))
