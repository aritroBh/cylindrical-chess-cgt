import sys, json
def nm(s, W=7): return chr(97 + s % W) + str(s // W + 1)
rows = [json.loads(l) for f in sys.argv[1:] for l in open(f)]
rows.sort(key=lambda r: r['score'])
for r in rows[:int(40)]:
    print(r['score'], r['board'], 'K', [nm(s) for s in r['K']], 'k', [nm(s) for s in r['k']], 'P', [nm(s) for s in r['P']], 'p', [nm(s) for s in r['p']])
