"""gen_report.py -- writes hits_star3.tsv, aborts.tsv, best.tsv and prints the numbers REPORT.md quotes."""
import sys, os, collections, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from growlib import *
from grow import load_cache, kind

cache = load_cache()
rows = list(cache.values())
tot = collections.Counter(kind(f[1]) for f in rows)
byr = collections.defaultdict(collections.Counter)
for f in rows:
    byr[int(f[4])][kind(f[1])] += 1

s3 = [f for f in rows if f[1] == 'NNNPNNNN']
with open('hits_star3.tsv', 'w') as o:
    o.write('ring\tfiles\tpawns\tall_files_occupied\tround\tmove_class\tparent_seed\n')
    for f in sorted(s3, key=lambda f: (int(f[4]), len(f[0].split()), f[0])):
        r = parse(f[0])
        o.write('\t'.join([f[0], str(len(r)), str(npawns(r)), 'yes' if is_ring(r) else 'no', f[4], f[5], f[6]]) + '\n')
with open('aborts.tsv', 'w') as o:
    o.write('ring\tnodes_at_abort\tround\tmove_class\tparent_seed\n')
    for f in rows:
        if f[1] == 'ABORT':
            o.write('\t'.join([f[0], f[2], f[4], f[5], f[6]]) + '\n')

# "best": there is no *4, so list the most informative *3 rings: smallest pawn count, smallest/largest n,
# largest pawn count, hardest search, and one first-found ring per move class
new3 = [f for f in s3 if f[5] != 'seed' and is_ring(parse(f[0]))]
pick = []
def add(f, why):
    if all(f[0] != p[0][0] for p in pick):
        pick.append((f, why))
key_p = lambda f: npawns(parse(f[0]))
add(min(new3, key=lambda f: (key_p(f), len(f[0].split()))), 'fewest pawns among new *3 rings')
add(max(new3, key=lambda f: (key_p(f), -int(f[2]))), 'most pawns among new *3 rings')
add(min(new3, key=lambda f: (len(f[0].split()), key_p(f))), 'fewest files among new *3 rings')
add(max(new3, key=lambda f: (len(f[0].split()), -key_p(f))), 'most files among new *3 rings')
add(max(new3, key=lambda f: int(f[2])), 'largest search among new *3 rings (nodes)')
for cls in ('pair_adj2', 'pair_same2', 'ins2_single', 'ins1_wb', 'add1', 'remove1', 'ins1_single', 'pair_same3'):
    c = [f for f in new3 if f[5] == cls]
    if c and len(pick) < 10:
        add(min(c, key=lambda f: (key_p(f), len(f[0].split()), f[0])), 'smallest new *3 reached by move class ' + cls)
with open('best.tsv', 'w') as o:
    for f, why in pick[:10]:
        o.write('%s\t%s\tfiles=%d\tpawns=%d\tround=%s\t%s\n' % (f[0], f[1], len(f[0].split()), key_p(f), f[4], why))

print(json.dumps({
    'evaluated_total': len(rows),
    'by_round': {r: dict(c) for r, c in sorted(byr.items())},
    'tot': dict(tot),
    'new_star3': len(s3) - 14,
    'star3_rings_all_files': sum(1 for f in s3 if is_ring(parse(f[0]))),
    'star3_nonring': sum(1 for f in s3 if not is_ring(parse(f[0]))),
}, indent=1))
print(open('best.tsv').read())
