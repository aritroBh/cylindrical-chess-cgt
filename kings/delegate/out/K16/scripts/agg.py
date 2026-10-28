#!/usr/bin/env python3
"""agg.py [logs/*.jsonl] : sum the per-chunk summaries by tag."""
import sys, json, glob, collections
files = sys.argv[1:] or sorted(glob.glob('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/logs/*.jsonl'))
tot = collections.OrderedDict()
for f in files:
    for l in open(f):
        d = json.loads(l); t = d['tag']; s = d['summary']
        T = tot.setdefault(t, {"board": d['board'], "chunks": 0, "positions": 0, "viol_pos": 0, "rss_max": 0, "gap": 0, "s2bad": 0,
                               "var": {k: [0, 0] for k in ["orig", "S0", "S1", "S2", "S1S2", "S3"]}})
        T["chunks"] += 1; T["positions"] += s["positions"]; T["viol_pos"] += s.get("violating_positions", s.get("violations", 0)); T["gap"] += s.get("gap", 0); T["s2bad"] += s.get("S2_but_stalemate", 0)
        T["rss_max"] = max(T["rss_max"], d.get("rss", 0))
        for k, v in (s["variants[instances,violations]"] if "variants[instances,violations]" in s else {"orig": [s["instances"], s["violations"]]}).items():
            T["var"][k][0] += v[0]; T["var"][k][1] += v[1]
for t, T in tot.items():
    v = T["var"]
    print(f'{t:14s} {T["board"]:9s} chunks={T["chunks"]:3d} positions={T["positions"]:8d} violating_positions={T["viol_pos"]:5d} gap={T["gap"]} s2bad={T["s2bad"]} rssMB={T["rss_max"]/1e6:.0f}  ' +
          ' '.join(f'{k}={v[k][0]}/{v[k][1]}' for k in v))
