#!/usr/bin/env python3
"""mksummary.py: write summary.json from the logs (exhaustive sweeps, kp_p samples, small exhaustive sets)."""
import json, glob, collections, re
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16'
out = {"task": "K16 real-king square rule (LOOPY Remark 2.11)", "exhaustive_sweeps": {}, "kpp_samples": {}, "small_exhaustive": []}
for f in sorted(glob.glob(D + '/logs/EX_*.jsonl')):
    for l in open(f):
        d = json.loads(l); t = d['tag']
        if t == 'EX_c66_33': continue  # replicate of EXD_c66_33
        T = out["exhaustive_sweeps"].setdefault(t, collections.Counter())
        T['board'] = d['board']; T['shards_done'] += d.get('nshards', 1); T['shards_total'] = d['of']
        for k, v in d['tally'].items(): T[k] += v
        s = d['summary']; T['kpp_positions'] += s['positions']; T['violating_positions'] += s['violating_positions']
        T['violating_instances'] += s['variants[instances,violations]']['orig'][1]
        for v in ('S0', 'S1', 'S2', 'S3'): T['viol_' + v] += s['variants[instances,violations]'][v][1]
for f in sorted(glob.glob(D + '/logs/*.jsonl')):
    if '/EX_' in f: continue
    for l in open(f):
        d = json.loads(l); t = d['tag']; s = d['summary']
        T = out["kpp_samples"].setdefault(t, collections.Counter()); T['board'] = d['board']; T['chunks'] += 1
        T['positions'] += s['positions']; T['violating_positions'] += s.get('violating_positions', s.get('violations', 0)); T['gap'] += s.get('gap', 0)
        if 'variants[instances,violations]' in s:
            for k, v in s['variants[instances,violations]'].items():
                T['inst_' + k] += v[0]; T['viol_' + k] += v[1]
        else:
            T['inst_orig'] += s['instances']; T['viol_orig'] += s['violations']
for l in open(D + '/logs/small_exhaustive.txt'):
    m = re.match(r'(\S+) (\d\+\d) n=\s*(\d+) (\{.*\})', l)
    if m:
        d = json.loads(m.group(4))
        out["small_exhaustive"].append({"board": m.group(1), "pawns": m.group(2), "positions": int(m.group(3)), "violating_positions": d["violating_positions"],
                                        "variants": d["variants[instances,violations]"]})
out["checks"] = {"pycert": open(D + '/logs/pycert.txt').read().strip().split('\n'), "xsim": open(D + '/logs/xsim.txt').read().strip().split('\n')}
json.dump(out, open(D + '/summary.json', 'w'), indent=1, default=dict)
print("summary.json written", len(out["exhaustive_sweeps"]), "sweeps")
