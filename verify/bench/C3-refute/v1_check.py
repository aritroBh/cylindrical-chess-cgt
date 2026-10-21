"""Own exhaustive check on library v1 (518): which components have a position judged differently?"""
import json, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import comp_enum as ce
v1 = [json.loads(l) for l in open(sys.argv[1])]
v2 = {json.loads(l)["position"] for l in open(ce.DATA / "components.jsonl")}
flag = []
for c in v1:
    W, B = ce.parse(c["position"]); n = c["width"]
    s0, a0, t0 = ce.enumerate_comp(W, B, n, False, False)
    s1, a1, t1 = ce.enumerate_comp(W, B, n, False, True)
    if s0["dbl_beside_passed"] or not (a0 == a1 and t0 == t1):
        flag.append(c["position"])
print("v1", len(v1), "flagged", len(flag), "v1 minus flagged == v2:", {c["position"] for c in v1} - set(flag) == v2,
      "flagged & v2:", len(set(flag) & v2))
