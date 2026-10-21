import json, glob, sys
for d in sys.argv[1:]:
    for vf in sorted(glob.glob(d + "/*.vals")):
        tag = vf.split("/")[-1].rsplit(".jsonl.vals",1)[0]
        want = {}
        for line in open(vf):
            r = json.loads(line)
            if r["cls"] == "ups" and r["detail"] and ("*2" in r["detail"] or "*3" in r["detail"] or "*4" in r["detail"]):
                want[r["vid"]] = r["detail"]
        if not want: continue
        for line in open(vf[:-5]):
            p = json.loads(line)
            if p["vid"] in want:
                print(tag, p["pos"], want[p["vid"]], "ring=%d ncomp=%d" % (p["ring"], p["ncomp"]))
