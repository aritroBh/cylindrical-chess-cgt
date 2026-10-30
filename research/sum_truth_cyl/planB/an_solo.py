import json, glob, collections
PRED = {"L": ("W", "W"), "R": ("L", "L"), "N": ("W", "L"), "P": ("L", "W")}
info = json.load(open('small_comps.json')); real = {}; kpm = {}
for f in glob.glob('solo_cap1/*.json'):
    r = json.load(open(f))
    assert not r['killed_over_limit'], f
    for s in r['stdout']:
        a, b = s.split('|'); real[a.strip()] = tuple(b.split())
for d in info:
    w, bt = real[d['wtm']], real[d['btm']]
    d['real'] = [w, bt]; d['exact'] = w[0] == w[1] and bt[0] == bt[1]
    for key in ('textbook', 'ep-aware'):
        o = d[key]['outcome']
        d[key + '_verdict'] = 'race' if o == 'race' else ('undet' if not d['exact'] else ('match' if (w[0], bt[0]) == PRED[o] else 'MISMATCH'))
json.dump(info, open('small_comps_real.json', 'w'), indent=1)
print(collections.Counter((d['textbook_verdict'], d['ep-aware_verdict']) for d in info))
print(collections.Counter((d['npawn'], d['textbook_verdict']) for d in info))
