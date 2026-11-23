"""K50 referee: the positions on which embed_check crashed (min() of an empty list, cert_terminal), re-run with
the patched program (verify/patched/kings/embed_check.py) and compared with the kp_p result from the harness.
Run from the project root: python3 .../crash_recheck.py out1.jsonl ..."""
import importlib.util
import json
import os
import sys
from collections import Counter

spec = importlib.util.spec_from_file_location("pe", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                 "patched", "kings", "embed_check.py"))
Pm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Pm)
t = Counter()
bad = []
for fn in sys.argv[1:]:
    for l in open(fn):
        r = json.loads(l)
        if r["P"] == ["?", "?"]:
            continue
        for m in ("strict", "ctx"):
            if r.get(m, {}).get("verdict") != "CRASH":
                continue
            W, H = map(int, r["board"].split(":")[1].split("x"))
            fz = None if r["gid"] in ("ZT", "Z72", "FigA", "FigB", "FigBm") else "a,b,c"
            o = Pm.Checker(Pm.Board(W, H, r["board"].startswith("cyl")), 8, 300000, m == "ctx", 30).run(r["pos"], fz)
            t[(m, o["verdict"])] += 1
            if o["verdict"] == "CERTIFIED":
                want = "W" if o["D_result"]["winner"] == "White" else "L"
                ok = r["P"][0] == r["P"][1] == want
                t[(m, "CERTIFIED agrees with kp_p" if ok else "CERTIFIED DISAGREES")] += 1
                if not ok:
                    bad.append((r["board"], r["pos"], m, want, r["P"]))
print(dict(t))
print("disagreements", bad)
