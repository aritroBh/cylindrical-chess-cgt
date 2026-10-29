import sys
mine = set(frozenset(l.split()) for l in open(sys.argv[1]) if l.strip())
theirs = set()
for l in open(sys.argv[2]):
    z = l.rsplit(' | ', 1)[0].split(); theirs.add(frozenset(z))
print('mine', len(mine), 'K29', len(theirs), 'only mine', len(mine - theirs), 'only K29', len(theirs - mine))
