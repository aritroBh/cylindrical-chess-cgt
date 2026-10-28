#!/usr/bin/env python3
"""mktable.py: markdown tables of the exhaustive sim sweeps (logs/EX*_*.jsonl) and of the kp_p sample runs."""
import json, glob, collections, os, re
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/logs'
ex = collections.OrderedDict()
for f in sorted(glob.glob(D + '/EX_*.jsonl')):
    for l in open(f):
        d = json.loads(l); t = d['tag']
        if t == 'EX_c66_33': continue  # exact replicate of EXD_c66_33 (same counts), not added
        T = ex.setdefault(t, collections.Counter()); T['board'] = d['board']; T['shards'] += d.get('nshards', 1); T['of'] = d['of']
        for k, v in d['tally'].items(): T[k] += v
        s = d['summary']
        T['kpp_pos'] += s['positions']; T['viol_pos'] += s['violating_positions']; T['viol_inst'] += s['variants[instances,violations]']['orig'][1]
        T['rss'] = max(T['rss'], d.get('rss', 0))
print("| sweep | board, pawns (W+B, beta = White) | shards | positions enumerated | certified positions | certified instances | Pi wins | stalemate line (at y) | other Pi failure | kp_p on the stalemate positions: violating positions (instances) | H3K instances (with stalemate) | H3 at k_omega (with stalemate line) | with e.p. | tight mu | tight SQ | omega in check at y |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for t, T in ex.items():
    print(f"| {t} | {T['board']} | {T['shards']}/{T['of']} | {T['seen']:,} | {T['cert_positions']:,} | {T['instances']:,} | {T['S1_instances']:,} | {T['stalemate_instances']:,} ({T['stalemate_at_y']:,}) | {T['gap_instances']:,} | {T['viol_pos']:,} ({T['viol_inst']:,}) | {T['S2_instances']:,} ({T['S2_but_stalemate']}) | {T['S3_instances']:,} ({T['S3_but_stalemate']}) | {T['with_ep']:,} | {T['tight_mu']:,} | {T['tight_sq']:,} | {T['omega_in_check']:,} |")
