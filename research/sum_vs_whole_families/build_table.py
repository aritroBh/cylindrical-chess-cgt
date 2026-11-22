import sys, re, glob, os
ROOT="/Users/aritro/Downloads/Research/Chessendgames"; os.chdir(ROOT)
sys.path.insert(0,"research/ring_n_plus_2_proof"); sys.path.insert(0,"research/ring_family")
import fam
from ringlib import from_cstr, to_ring, cstr, nparts
def canon(ring):
    n=len(ring); best=None
    def cr(r): return tuple(((tuple(sorted(9-x for x in b))), tuple(sorted(9-x for x in w))) for (w,b) in r)
    for r0 in (tuple(ring), tuple(reversed(ring)), cr(ring), cr(tuple(reversed(ring)))):
        for s in range(n):
            c=r0[s:]+r0[:s]
            if best is None or c<best: best=c
    return best
MINN={"odd":5,"even":6,"F":7,"P":8,"Q":8,"R":9,"Qo":9,"N1":9,"M":10,"O":11,"S3":13,"T3":12}
index={}
for k,f in fam.FAMILIES.items():
    for n in range(MINN[k],40):
        try: t=f(n)
        except AssertionError: continue
        index[canon(from_cstr(" ".join(t)))]=(k,n)
rows={}  # (ring canon) -> dict
def add(ring, mode, val, time, rss, src, status="ok"):
    c=canon(ring); d=rows.setdefault(c,{"ring":cstr(ring),"n":len(ring),"pawns":nparts(ring),"sum":None,"whole":None})
    key=mode
    if d[key] and d[key][4]=="ok" and status!="ok": return
    d[key]=(val,time,rss,src,status)
# 1. old logs
for p in ["research/sum_model_rings/sum_values.txt","research/sum_model_rings/npawn_values.txt","research/sum_model_rings/odd_values.txt","research/c9_rings/verify_hits/cyl_results.tsv"]+glob.glob("research/ring_family/logs/cyl_*.log"):
    L=open(p).read().splitlines()
    for i,l in enumerate(L):
        m=re.match(r"C(\d+) pawns=(\d+) whole=(True|False): (.*)",l)
        if m and i+1<len(L) and L[i+1].startswith("value = "):
            v=L[i+1][8:]; mm=re.search(r"\s+time ([\d.]+)s\s+maxrss (\d+) MB",v)
            val=v[:mm.start()] if mm else v
            if len(val)>40: val="COMPLEX(not *2): "+val[:30]+"..."
            add(to_ring(m.group(4)),"whole" if m.group(3)=="True" else "sum",val,mm.group(1) if mm else "",mm.group(2) if mm else "",p)
        elif p.endswith(".tsv"):
            q=l.split("\t")
            if len(q)>=4 and q[0] in("sum","whole"): add(from_cstr(q[1]),q[0],q[2],q[5] if len(q)>5 else "","",p)
# 2. new runs
for l in open("research/sum_vs_whole_families/runs.tsv"):
    k,n,mode,pw,ring,st,val,wall,peak=l.rstrip("\n").split("\t")
    lg=open(f"research/sum_vs_whole_families/logs/{k}_{n}_{mode}.log").read()
    mm=re.search(r"time ([\d.]+)s\s+maxrss (\d+) MB",lg)
    rss=max(int(mm.group(2)) if mm else 0,int(peak))
    fv=[x[8:].split("  time ")[0] for x in lg.splitlines() if x.startswith("value = ")]
    if st=="ok" and fv and len(fv[0])>40:
        import hashlib; val="COMPLEX(len%d,md5 %s)"%(len(fv[0]),hashlib.md5(fv[0].encode()).hexdigest()[:8])
    add(from_cstr(ring),mode,val if st=="ok" else st,f"{wall}",str(rss),"sum_vs_whole_families/runs.tsv",st)
out=open("research/sum_vs_whole_families/table.tsv","w")
out.write("family\tn\tring\tpawns\tsum_value\twhole_value\tsum_s\twhole_s\tsum_rssMB\twhole_rssMB\tsum_eq_whole\tsources\n")
srt=sorted(rows.items(),key=lambda kv:(index.get(kv[0],("zz",0))[0],kv[1]["n"],kv[1]["pawns"]))
for c,d in srt:
    k,n=index.get(c,("other",d["n"]))
    s,w=d["sum"],d["whole"]
    eq="" if not(s and w) else ("yes" if s[0]==w[0] else ("NO" if s[4]=="ok" and w[4]=="ok" else "incomplete"))
    f=lambda x,i:(x[i] if x else "")
    out.write("\t".join([k,str(d["n"]),d["ring"],str(d["pawns"]),f(s,0),f(w,0),f(s,1),f(w,1),f(s,2),f(w,2),eq,";".join(sorted({x[3] for x in(s,w) if x}))])+"\n")
