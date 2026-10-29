import csv, collections
cfgs = {'cyl7x6_f3':('cyl',7,0,3),'cyl7x6_f4':('cyl',7,0,4),'cyl8x6_f3':('cyl',8,0,3),'cyl8x6_f4':('cyl',8,0,4),'flat7x6_f3_z0':('flat',7,0,3),'flat7x6_f3_z2':('flat',7,2,3),'flat7x6_f4_z0':('flat',7,0,4),'flat8x6_f3_z0':('flat',8,0,3),'flat8x6_f3_z2':('flat',8,2,3),'flat8x6_f4_z0':('flat',8,0,4)}
tot = near = 0; other = []
for r in csv.reader(open('data/table_all.tsv'), delimiter='\t'):
    if r[0] not in cfgs or r[5] != 'FAIL': continue
    kind, W, zs, fz = cfgs[r[0]]
    files = [ 'abcdefgh'.index(t[1]) for t in r[6].split()]
    def dist(f):
        zf = range(zs, zs + fz)
        if kind == 'cyl': return min(min((f - z) % W, (z - f) % W) for z in zf)
        return min(abs(f - z) for z in zf)
    d = min(dist(f) for f in files) if files else None
    tot += 1
    if d == 2: near += 1
    else: other.append((r[0], r[1], r[6], d))
print('main failing classes', tot, 'with a pawn at distance exactly 2:', near, 'others:', other)
