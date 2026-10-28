import sys, json
pre = sys.argv[1]; hits = []; tot = 0; mate = 0; ill = 0
for ln in open(pre + '.out'):
    if ' | ' not in ln: continue
    pos, rest = ln.rstrip('\n').split(' | ', 1); t = rest.split()
    tot += 1
    if t[0] == 'X': ill += 1; continue
    if t[0] == 'W':
        if len(t) == 1: mate += 1
        else: hits.append(pos)
print(pre, 'answered', tot, 'illegal', ill, 'W,no legal move', mate, 'HITS', len(hits))
json.dump(hits, open(pre + '.hits.json', 'w'))
