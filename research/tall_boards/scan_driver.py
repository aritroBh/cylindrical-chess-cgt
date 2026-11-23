#!/usr/bin/env python3
"""Exhaustive scan driver.  usage: scan_driver.py WORKER_ID BUDGET_S_PER_CASE [pass]
Cases = (board, R).  For each case, pawn counts p = F, F+1, ... ; for each p every split nw<=nb is counted (tw --count) and then
solved (tw --scan) within the case's CPU budget.  A level is 'complete' only if every split finished.
Results: results/levels.tsv, results/hits.tsv, results/raw/*.out.zst, logs/progress.txt.  Cases are claimed with mkdir (results/claims/)."""
import subprocess, sys, os, time, json
T = os.path.dirname(os.path.abspath(__file__))
wid = sys.argv[1]; budget = float(sys.argv[2]); passno = sys.argv[3] if len(sys.argv) > 3 else "1"
TABLOG = os.environ.get("TABLOG", "25")
boards = [(3,0),(3,1),(4,0),(4,1),(5,1)]
cases = [(F,w,R) for R in range(5,13) for (F,w) in boards if F*R <= 64]
if os.environ.get('REVERSE'): cases.reverse()
ONLY = os.environ.get('ONLY')
os.makedirs(T+"/results/raw", exist_ok=True); os.makedirs(T+"/results/claims", exist_ok=True)
open(f"{T}/logs/driver_w{wid}.pid","w").write(str(os.getpid()))
def log(s):
    with open(T+"/logs/progress.txt","a") as f: f.write(time.strftime("%H:%M:%S ")+f"[w{wid} p{passno}] "+s+"\n")
def run(args, tl):
    pr = subprocess.Popen(["nice","-n","15",T+"/tw"]+args+["--tlimit",str(tl),"--maxtab",TABLOG],stdout=subprocess.PIPE,text=True)
    open(f"{T}/logs/scan_w{wid}.pid","w").write(str(pr.pid))
    out = pr.communicate()[0]; return out
def nim(sig):
    q=-1
    for k,c in enumerate(sig):
        if c=="P":
            if q>=0: return -1
            q=k
        elif c!="N": return -1
    return q
for (F,w,R) in cases:
    name = f"F{F}{'c' if w else 'f'}_R{R}"
    if ONLY and name not in ONLY.split(','): continue
    try: os.mkdir(f"{T}/results/claims/{name}_p{passno}")
    except FileExistsError: continue
    stf = f"{T}/results/state_{name}.json"
    st = json.load(open(stf)) if os.path.exists(stf) else {"next_p":F,"min":{},"done":False,"spent":0.0}
    EXT = bool(os.environ.get("EXTEND"))
    if st["done"] and not EXT: continue
    spent = 0.0; raw = open(f"{T}/results/raw/{name}_pass{passno}.out","w")
    log(f"start {name} next_p={st['next_p']}")
    p = st["next_p"]; stop_reason = ""
    zeros = 0; pmax = F*(R-2)
    while p <= pmax:
        hist = {}; roots_total = 0; processed = 0; complete = True; cpu = 0.0; hits = []
        for nw in range(1, p//2+1):
            nb = p-nw
            rem = budget - spent
            c = run(["--scan",str(F),str(w),str(R),str(nw),str(nb),"--count"], 30)
            n = int(c.split("roots=")[1].split()[0]); roots_total += n
            if "INCOMPLETE" in c: complete = False; n = -1
            if rem <= 1 or n == 0:
                if n != 0: complete = False
                continue
            t0 = time.time()
            o = run(["--scan",str(F),str(w),str(R),str(nw),str(nb)], rem)
            dt = time.time()-t0; spent += dt; cpu += dt
            raw.write(f"## {name} p={p} split={nw}+{nb}\n"+o); raw.flush()
            ok = False
            for line in o.splitlines():
                if line.startswith("#hist"):
                    _,s,cn = line.split("\t"); hist[s] = hist.get(s,0)+int(cn)
                elif line.startswith("HIT"): hits.append(line)
                elif line.startswith("#done"):
                    ok = "complete=1" in line; processed += int(line.split("processed=")[1].split()[0])
            if not ok: complete = False
        cnt = {}
        for s,cn in hist.items():
            q = nim(s); key = f"*{q}" if q>=0 else "other"; cnt[key] = cnt.get(key,0)+cn
        with open(T+"/results/levels.tsv","a") as f:
            f.write("\t".join(map(str,[F,w,R,p,roots_total,processed,int(complete),round(cpu,1),json.dumps(cnt,sort_keys=True),passno]))+"\n")
        with open(T+"/results/hits.tsv","a") as f:
            for h in hits: f.write(f"{F}\t{w}\t{R}\t{p}\t{h}\n")
        for k in cnt:
            if k not in ("other",) and int(k[1:])>=2 and k not in st["min"]: st["min"][k] = p
        log(f"{name} p={p} roots={roots_total} processed={processed} complete={int(complete)} cpu={cpu:.0f}s {cnt}")
        if not complete: stop_reason = "budget"; break
        zeros = zeros+1 if roots_total == 0 else 0
        p += 1
        if zeros >= 2: stop_reason = "space exhausted"; break
        if not EXT and "*2" in st["min"] and "*3" in st["min"] and all(int(k[1:])<4 for k in st["min"]) : stop_reason = "both found"; break
        if spent >= budget: stop_reason = "budget"; break
    st["next_p"] = p; st["spent"] += spent
    st["done"] = stop_reason in ("both found","space exhausted") or p > pmax
    st["reason"] = stop_reason
    json.dump(st, open(stf,"w"))
    raw.close()
    rp = f"{T}/results/raw/{name}_pass{passno}.out"
    subprocess.run(["zstd","-q","-19","-f",rp]); 
    if subprocess.run(["zstd","-tq",rp+".zst"]).returncode == 0: os.remove(rp)
    log(f"end {name} reason={stop_reason} min={st['min']} spent={spent:.0f}s")
