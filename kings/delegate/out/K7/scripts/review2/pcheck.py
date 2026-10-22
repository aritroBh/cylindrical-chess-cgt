import sys, json, subprocess, time
geo=sys.argv[1]; fn=sys.argv[2]; chunk=int(sys.argv[3]) if len(sys.argv)>3 else 20000
found=json.load(open(fn))
keys=sorted(found)
bad=[]; anoms=[]; n=0; t0=time.time()
for i in range(0,len(keys),chunk):
    part=keys[i:i+chunk]
    r=subprocess.run(["./kpm","--board",geo,"--ep","on","--promote","Q","--pmodel","--threads","2"],input="\n".join(part)+"\n",capture_output=True,text=True)
    lines=r.stdout.splitlines()
    assert len(lines)==len(part),(len(lines),len(part),r.stderr[-300:])
    for q,l in zip(part,lines):
        pv=l.split("|")[1].split()
        win = pv[0]==pv[1]=='L'      # s = White to move; sbar=Black wins iff White loses (result from White's view)
        n+=1
        if not win: bad.append((q,found[q],pv))
        if any(isinstance(t,list) or (isinstance(t,list)) for t in found[q][2]): pass
    print("chunk",i,"checked",n,"bad",len(bad),"%.0fs"%(time.time()-t0),file=sys.stderr,flush=True)
print(fn,geo,"checked",n,"NON-WINS (counterexamples):",len(bad))
for b in bad[:10]: print(" CE",b)
an=[(q,v) for q,v in found.items() if any(isinstance(t,list) and t[0]=='ANOM' for t in v[2])]
print("anomaly entries:",len(an), an[:3])
