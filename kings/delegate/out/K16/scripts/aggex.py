#!/usr/bin/env python3
"""aggex.py : sum the exhaustive sweeps (logs/EX_*.jsonl): tally from chk (--onlystale) + kp_p verdicts on stalemate instances."""
import json, glob, collections, os
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/logs'
tot = collections.OrderedDict()
for f in sorted(glob.glob(D + '/EX_*.jsonl')):
    for l in open(f):
        d = json.loads(l); t = d['tag']
        T = tot.setdefault(t, collections.Counter())
        T['shards'] += d.get('nshards', 1); T['of'] = d['of']
        for k, v in d['tally'].items(): T[k] += v
        s = d['summary']
        T['stale_positions_to_kpp'] += s['positions']
        T['viol_positions'] += s['violating_positions']
        T['viol_instances'] += s['variants[instances,violations]']['orig'][1]
        T['gap_kpp'] += s.get('gap', 0)
        T['rss'] = max(T['rss'], d.get('rss', 0))
for t, T in tot.items():
    done = os.path.exists(f'{D}/{t}.done'.replace('logs/', 'logs/')) or os.path.exists(f'{D}/{t}.done')
    print(f"{t}: shards {T['shards']}/{T['of']}  positions seen {T['seen']:,}  certified positions {T['cert_positions']:,}  instances {T['instances']:,}")
    print(f"    Pi wins (no stalemate line) {T['S1_instances']:,}   stalemate-in-some-line {T['stalemate_instances']:,} (at y: {T['stalemate_at_y']:,})   "
          f"non-stalemate strategy failures {T['gap_instances']:,} (promo {T['gap_promo']}, p captured {T['gap_capt']}, blocked {T['gap_block']})")
    print(f"    stalemate instances sent to kp_p: positions {T['stale_positions_to_kpp']:,} -> violating positions {T['viol_positions']:,}, violating instances {T['viol_instances']:,}")
    print(f"    H3 at k_omega (S3) instances {T['S3_instances']:,} (of which stalemate-line: {T['S3_but_stalemate']})")
    print(f"    H3K instances {T['S2_instances']:,} (of which stalemate: {T['S2_but_stalemate']})   ep {T['with_ep']:,}  tight mu {T['tight_mu']:,}  tight SQ {T['tight_sq']:,}  omega in check {T['omega_in_check']:,}  both colours {T['both_colours']}")
