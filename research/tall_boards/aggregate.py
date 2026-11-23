#!/usr/bin/env python3
"""Aggregate results/levels.tsv + hits.tsv into results/table.tsv and results/table.md (board x R)."""
import json, os, collections
T = os.path.dirname(os.path.abspath(__file__))
rows = collections.defaultdict(dict)   # (F,w,R) -> p -> merged level dict
for line in open(T+"/results/levels.tsv"):
    F,w,R,p,tot,proc,comp,cpu,cnt,ps = line.rstrip("\n").split("\t")
    key = (int(F),int(w),int(R)); p = int(p)
    d = rows[key].get(p)
    new = {"roots":int(tot),"proc":int(proc),"complete":int(comp),"cpu":float(cpu),"cnt":json.loads(cnt)}
    # a later pass re-runs an incomplete level from scratch: keep the one with more processed roots
    if d is None or new["proc"] >= d["proc"]:
        if d: new["cpu"] += d["cpu"]
        rows[key][p] = new
    else: d["cpu"] += new["cpu"]
def name(F,w): return f"{'cyl' if w else 'flat'} {F}"
out = []; md = []
for key in sorted(rows, key=lambda k:(k[1]*0+k[0]*0+0,k[0],k[1],k[2])):
    F,w,R = key; lv = rows[key]; ps = sorted(lv)
    cpu = sum(lv[p]["cpu"] for p in ps)
    # largest complete prefix
    cp = None; N = 0
    for p in ps:
        if lv[p]["complete"]: cp = p; N += lv[p]["roots"]
        else: break
    def least(q):
        for p in ps:
            c = lv[p]["cnt"].get(f"*{q}",0)
            if c:
                exact = all(lv[x]["complete"] for x in ps if x < p)
                return f"{'' if exact else '<='}{p}"
        return None
    tot = collections.Counter()
    for p in ps:
        for k,v in lv[p]["cnt"].items(): tot[k]+=v
    hi = {k:v for k,v in tot.items() if k!="other" and int(k[1:])>=4}
    exhausted = bool(ps) and all(lv[x]["complete"] for x in ps) and (ps[-1]==F*(R-2) or (len(ps)>1 and lv[ps[-1]]["roots"]==0 and lv[ps[-2]]["roots"]==0))
    last_complete = cp
    def desc(q):
        l = least(q)
        if l: return l
        if exhausted: return f"none (space exhausted; all {sum(lv[p]['roots'] for p in ps)} roots)"
        return f"none up to {cp} pawns ({N} roots)"
    out.append((F,w,R,desc(2),desc(3),dict(tot),hi,cp,N,round(cpu),exhausted))
with open(T+"/results/table.tsv","w") as f:
    f.write("board\tR\tleast_*2\tleast_*3\tcounts_by_nimber_over_all_levels\tgeq4\tcomplete_through_p\tN_roots_complete\tcpu_s\texhausted\n")
    for F,w,R,a,b,tot,hi,cp,N,cpu,ex in out:
        f.write(f"{name(F,w)}\t{R}\t{a}\t{b}\t{json.dumps({k:v for k,v in sorted(tot.items()) if k!='other'})}\t{json.dumps(hi)}\t{cp}\t{N}\t{cpu}\t{int(ex)}\n")
print(open(T+"/results/table.tsv").read())

# markdown table
with open(T+"/results/table.md","w") as f:
    f.write("| board | R | least p for *2 | least p for *3 | roots found by nimber (all levels run) | exhaustive through p (roots) |\n|---|---|---|---|---|---|\n")
    for F,w,R,a,b,tot,hi,cp,N,cpu,ex in sorted(out, key=lambda x:(x[1],x[0],x[2])):
        cnt = ", ".join(f"{k}:{v}" for k,v in sorted(tot.items()) if k!="other")
        f.write(f"| {name(F,w)} | {R} | {a} | {b} | {cnt}{'; >=*4: '+str(hi) if hi else ''} | {'all p (' + str(N) + ')' if ex else str(cp) + ' (' + str(N) + ')'} |\n")
