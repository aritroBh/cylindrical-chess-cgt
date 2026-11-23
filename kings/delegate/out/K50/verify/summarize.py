"""K50 referee: tally the harness outputs. Usage: python3 summarize.py out1.jsonl [out2.jsonl ...]"""
import json
import sys
from collections import Counter

t = Counter()
viol = []
crash = []
for fn in sys.argv[1:]:
    for l in open(fn):
        r = json.loads(l)
        if r["P"] == ["?", "?"]:  # no solver result (kp_p rejects the board): not compared
            t["skipped (no kp_p result) " + r["board"]] += 1
            continue
        t["positions"] += 1
        t["Y nodes"] += r["nY"]
        for m in ("strict", "ctx"):
            if m not in r:
                continue
            d = r[m]
            t[f"{m} runs"] += 1
            t[f"{m} {d['verdict']}"] += 1
            if d["verdict"] == "CRASH":
                crash.append((r["board"], r["pos"], m, d["err"]))
                t[f"{m} CRASH " + d["err"][:40]] += 1
            if d["verdict"] == "CERTIFIED":
                t[f"{m} CERTIFIED {'full' if d['proves'].startswith('Theorem') else 'sharp'}"] += 1
            for s in ("white", "black"):
                if d.get("V3", {}).get(s) == "CERTIFIED":
                    t[f"{m} V3 {s} CERTIFIED"] += 1
                if d.get("V1b", {}).get(s) == "CERTIFIED":
                    t[f"{m} V1b {s} CERTIFIED"] += 1
            if d.get("V2p") == "CERTIFIED":
                t[f"{m} V2-passer CERTIFIED"] += 1
            if d.get("D") and r.get("refD") and d["D"] != r["refD"]:
                t[f"{m} program D != ref D"] += 1
        if r["P"][0] != r["P"][1]:
            t["kp_p inexact"] += 1
        for v in r["viol"]:
            viol.append((r["board"], r["gid"], v))
for k in sorted(t):
    print(f"{t[k]:8d}  {k}")
print("VIOLATIONS", len(viol))
for v in viol[:50]:
    print("  ", v)
print("CRASHES", len(crash))
for c in crash[:20]:
    print("  ", c)
