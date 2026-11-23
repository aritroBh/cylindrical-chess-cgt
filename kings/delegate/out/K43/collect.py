#!/usr/bin/env python3
"""K43: parse logs/*.out into a list of run records (dict) for the report builders."""
import glob, re, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
def runs():
    out = []
    for f in sorted(glob.glob(os.path.join(HERE, "logs", "*.out"))):
        tag = os.path.basename(f)[:-4]
        if not os.path.exists(os.path.join(HERE, "logs", tag + ".done")): continue
        rec = {"tag": tag, "under": None, "over": None, "hits": 0, "board": None}
        for l in open(f):
            if l.startswith("RESULT "):
                kv = {k: int(v) for k, v in re.findall(r"(\w+)=(-?\d+)", l)}
                m = re.search(r"refstyle|lemma410\(checked=(\d+) noShuttle=(\d+) legalAtOther=(\d+) violations=(\d+)\)", l)
                if m and m.group(1) is not None:
                    kv["lem_checked"], kv["lem_noshuttle"], kv["lem_legal"], kv["lem_viol"] = map(int, m.groups())
                kv["F1"] = int(re.search(r"F1\([^)]*\)=(\d+)", l).group(1)); kv["F2"] = int(re.search(r"F2\(U2\)=(\d+)", l).group(1))
                kv["F3"] = int(re.search(r"F3\(U3 loose\)=(\d+)", l).group(1)); kv["F4"] = int(re.search(r"F4\(exact U4\)=(\d+)", l).group(1))
                if "white(under)" in l: rec["under"] = kv
                else: rec["over"] = kv
            elif l.startswith("HIT "): rec["hits"] += 1
        e = open(os.path.join(HERE, "logs", tag + ".err")).read().split("\n", 1)[0]
        rec["board"] = e
        out.append(rec)
    return out
if __name__ == "__main__":
    for r in runs():
        u = r["under"]; o = r["over"]
        print(r["tag"], "|", r["board"][:110], "|", "under F4=%d over F4=%d hits=%d" % (u["F4"], o["F4"], r["hits"]))
