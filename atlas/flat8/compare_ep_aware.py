"""Compare the flat8 atlas before (textbook passed test) and after (e.p.-aware) the convention change."""
import json
import sys
from collections import Counter

old_path, new_path = sys.argv[1], sys.argv[2]


def load(p):
    out = {}
    with open(p) as fh:
        for line in fh:
            r = json.loads(line)
            out[r["position"]] = r
    return out


old, new = load(old_path), load(new_path)
assert set(old) == set(new), (len(old), len(new))
changed = [k for k in old if old[k]["value"] != new[k]["value"]]
oc_changed = [k for k in changed if old[k]["outcome"] != new[k]["outcome"]]
print(f"records {len(old)}; value changed {len(changed)}; outcome changed {len(oc_changed)}")
print("changed by width:", dict(Counter(old[k]["width"] for k in changed)))
print("changed by #pawns:", dict(Counter(old[k]["nw"] + old[k]["nb"] for k in changed)))
print("changed, legal8x8:", sum(1 for k in changed if old[k].get("legal8x8")))
for tag, db in (("old", old), ("new", new)):
    nims = Counter(r["nim"] for r in db.values() if r["nim"] is not None)
    print(f"{tag} nimber census: {dict(sorted(nims.items()))}")
    for k, r in db.items():
        if r["nim"] is not None and r["nim"] >= 2:
            print(f"   {tag} *{r['nim']}: {k} (width {r['width']}, legal8x8 {r.get('legal8x8')}, comps {r['n_components']})")
# value classes that appear or disappear
ov, nv = Counter(r["value"] for r in old.values()), Counter(r["value"] for r in new.values())
gone = [v for v in ov if v not in nv]
born = [v for v in nv if v not in ov]
print(f"distinct values old {len(ov)}, new {len(nv)}; vanished {len(gone)}, new {len(born)}")
short = lambda vs: sorted(vs, key=len)[:25]
print("vanished (shortest):", short(gone))
print("new (shortest):", short(born))
# targets the A2 report highlighted
for k in ["W: a2 c2 / B: b7 d7", "W: a2 b2 d2 / B: a5 c4 d7", "W: a3 c5 d4 / B: a7 b7 d7",
          "W: a2 b2 b6 / B: a6 b7 c5", "W: a2 a3 b2 / B: a6 b5 b6"]:
    if k in old:
        print(f"{k}: old {old[k]['value']}  ->  new {new[k]['value']}")
    else:
        print(f"{k}: not stored under this orientation")

# Elkies targets: exact counts and which positions keep them
TARGETS = ["1/8", "-1/8", "1/16", "-1/16", "1/32", "-1/32", "{0 | ↓*}", "{↑* | 0}", "{0, * | ↓}", "{↑ | 0, *}", "tiny(1)", "miny(1)", "*2"]
for t in TARGETS:
    o = [k for k, r in old.items() if r["value"] == t]
    n = [k for k, r in new.items() if r["value"] == t]
    kept = [k for k in o if new[k]["value"] == t]
    print(f"target {t:12s} old {len(o):3d}  new {len(n):3d}  kept {len(kept):3d}  "
          f"new-only {[k for k in n if k not in o][:4]}  kept-legal8x8 {[k for k in kept if old[k].get('legal8x8')][:4]}")
