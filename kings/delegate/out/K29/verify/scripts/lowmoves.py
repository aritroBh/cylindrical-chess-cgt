import csv, subprocess, collections
K = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
cfg = {'cyl7x6_f3':'cyl:7x6','flat7x6_f3_z0':'flat7x6','flat7x6_f3_z2':'flat7x6','flat8x6_f3_z2':'flat8x6'}
rows = [r for r in csv.reader(open(K + 'data/table_all.tsv'), delimiter='\t') if r[0] in cfg and r[5] == 'SURVIVES']
allmoves = collections.Counter(); nsurv = 0; every3 = 0
for c, rb in cfg.items():
    zs = [r[1] for r in rows if r[0] == c]
    # all GROUPS of the surviving classes, not only reps? reps only (the table lists class representatives)
    ins = [z + ' ' + s + ' -' for z in zs for s in 'wb']
    o = subprocess.run([K + 'verify/bin/ref3d', '--board', rb, '--moves'], input='\n'.join(ins) + '\n', capture_output=True, text=True).stdout.splitlines()
    o = [l for l in o if ' | ' in l]
    for i, z in enumerate(zs):
        nsurv += 1; has3 = False; low = []
        for j in (2*i, 2*i+1):
            toks = o[j].rsplit(' | ', 1)[1].split()
            for x in toks[2:]:
                mv, v, d = x.split(':'); tp = (int(d) + 1) // 2
                if tp >= 3: has3 = True
                else: low.append((mv, tp)); allmoves[(mv, tp)] += 1
        every3 += has3
        print(c, z, 'low (T_P<=2) moves:', low)
print('survivor (group,config) pairs', nsurv, 'with a sortie T_P>=3:', every3, ' distinct low moves:', sorted(allmoves.items()))
