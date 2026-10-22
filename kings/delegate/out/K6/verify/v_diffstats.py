import json, os, sys, collections
K4 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for size in ['3x4', '4x4', '3x5', '4x5', '5x5']:
    for kind in ('flat', 'cyl'):
        rows = [json.loads(l) for l in open(os.path.join(K4, '%s_%s.jsonl' % (kind, size)))]
        c = collections.Counter(); outc = collections.Counter()
        for r in rows:
            for v, d in r['diff'].items():
                c[(v, d['second_player'])] += 1
                outc[(v, d['white_starts'] + d['black_starts'])] += 1
        nm = sum(1 for r in rows if r['matched'])
        runs = sum(len(r['diff']) for r in rows)
        passed = sum(v for (nv, ok), v in c.items() if ok)
        print(kind, size, 'placements with matched V:', nm, 'diff tests:', runs, 'second-player survivals:', passed, 'fails:', runs - passed,
              dict(((k, v) for k, v in sorted(outc.items()))))
