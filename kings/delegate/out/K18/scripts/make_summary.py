#!/usr/bin/env python3
"""collect the K18 numbers into summary.json (run from the K18 directory)."""
import json, os, re, collections, subprocess, sys
S = {}
def rd(fn):
    try: return open(fn).read()
    except OSError: return None
# searches
srch = {}
for tag in ["c8x6_f3_22", "c7x6_f3_22", "c8x6_f4_22", "c7x6_f4_22", "c8x6_f3_32", "c7x6_f3_32", "flat6x6_f3_22"]:
    e = rd(f"logs/search_{tag}.err")
    if e:
        m = re.search(r"roots=(\d+)\s+candidates\(any\) P=(\d+) Q=(\d+)\s+candidates\(no escape\) P=(\d+) Q=(\d+)", e)
        if m: srch[tag] = dict(zip(["roots", "root_cand_any_P", "root_cand_any_Q", "root_cand_noesc_P", "root_cand_noesc_Q"], map(int, m.groups())))
S["search_roots"] = srch
S["search_distinct"] = rd("logs/search_summary.txt")
S["bare_crosscheck"] = rd("logs/bare_noesc.txt")
S["lg_vs_lg2_random"] = rd("logs/xcheck_result.txt")
# k classes
try:
    rows = json.load(open("logs/sorties_k_all.json"))
    def cls(kv):
        f = [x is not None for x in kv[:7]]
        if all(f): return "finite for every k<=6"
        if f[0] and not any(f[1:]): return "k*=0"
        if all(f[k] == (k % 2 == 0) for k in range(7)): return "even k only"
        return "other finite pattern"
    S["k_classes"] = dict(collections.Counter(cls(r["kvec"]) for r in rows)); S["n_plain_only_king_sorties"] = len(rows)
except OSError: pass
for d, n in (("E1", "E1"), ("E3", "E3"), ("E2", "E2")):
    t = rd(f"logs/{d}/summary.txt")
    if t: S[n] = t
json.dump(S, open("summary.json", "w"), indent=1)
print("wrote summary.json")
