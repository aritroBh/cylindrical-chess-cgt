"""Join FAIL lines (root | m | value) with the sortie list to give 'position after m + context' lines."""
import sys
sorties, fails, ctx = sys.argv[1], sys.argv[2], sys.argv[3]
after = {}
for line in open(sorties):
    f = line.rstrip('\n').split(' | ')
    after[(f[0], f[1])] = f[2]
for line in open(fails):
    if not line.startswith('FAIL'):
        continue
    f = line.rstrip('\n').split(' | ')
    pos = after[(f[1], f[2])].split()
    toks, rest = pos[:-2], pos[-2:]
    print(' '.join(toks + ctx.split() + rest), '|', f[3])
