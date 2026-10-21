import json, glob, sys, collections
# scan every .vals file; report nimbers (key "*k") and any value whose key is "*k" or number+nimber containing *k>=2
res = collections.defaultdict(set)
pos_by = collections.defaultdict(list)
for d in sys.argv[1:]:
    for vf in glob.glob(d + "/*.vals"):
        tag = vf.split("/")[-1].rsplit(".jsonl.vals",1)[0]
        parts = tag.split("_")
        setting = parts[2] + "/" + parts[3]
        nimv = {}
        for line in open(vf):
            r = json.loads(line)
            k = r["key"]
            if k.startswith("*"):
                res[setting].add(k); nimv[r["vid"]] = k
            if r["cls"] == "number+nimber":
                res[setting+" n+n"].add(r["detail"])
            if r["cls"] == "ups":
                res[setting+" ups"].add(r["detail"])
        # positions
        for line in open(vf[:-5]):
            p = json.loads(line)
            if p["vid"] in nimv and nimv[p["vid"]] != "*1":
                pos_by[(setting, nimv[p["vid"]])].append((("cyl" if p["wrap"] else "flat")+str(p["n"]), p["pos"], p["ring"], p["ncomp"]))
for s in sorted(res): print(s, sorted(res[s]))
for k in sorted(pos_by):
    v = pos_by[k]
    print(k, len(v))
    for x in sorted(set(v)): print("   ", x)
