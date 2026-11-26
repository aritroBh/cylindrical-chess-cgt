# Print the cached Syzygy answers (K65 cache, unpacked copy) for the K68 roots and q's. usage: python3 tb_k68.py <tbcache dir>
import json, os, sys
want = ["8/1p6/1Pp5/2P5/1k1K4/8/2P5/8 w", "8/1p6/1Pp5/2P5/1k1K4/8/2P5/8 b", "8/1p6/1Pp5/1kP5/3K4/8/2P5/8 w",
        "8/1p6/1Pp5/1kP5/3K4/8/2P5/8 b", "8/1p6/1Pp5/2P5/1kPK4/8/8/8 w", "8/1p6/1Pp5/2P5/1kPK4/8/8/8 b",
        "8/1p6/1Pp5/1kP5/3K4/2P5/8/8 w", "8/1p6/1Pp5/1kP5/3K4/2P5/8/8 b"]
idx = {}
for d, _, fs in os.walk(sys.argv[1]):
    for f in fs:
        if not f.endswith('.json'): continue
        j = json.load(open(os.path.join(d, f)))
        idx[' '.join(j['fen'].split()[:2])] = j
for w in want:
    j = idx.get(w)
    if not j: print(w, 'NOT CACHED'); continue
    dd = j['data']
    side = w.split()[1]
    print(w, 'to move:', dd['category'], 'dtz', dd['dtz'])
    print('   ', ' '.join('%s:%s' % (m['san'], m['category']) for m in dd['moves']))
