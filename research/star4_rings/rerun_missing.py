import subprocess, os
rows=[]
ids_done=set()
with open("wall_results.tsv") as f:
    for line in f: ids_done.add(line.split("\t",1)[0])
with open("wall_candidates.txt") as f:
    for line in f:
        cid,n,pos=line.rstrip("\n").split("\t",2)
        if cid not in ids_done:
            rows.append((cid,n,pos))
print("missing",len(rows))
env=dict(os.environ); env["TBITS"]="23"
with open("wall_results.tsv","a") as out:
    for i in range(0,len(rows),10):
        chunk=rows[i:i+10]
        p=subprocess.run(["nice","-n","15","./rg","solve","7"], input="\n".join(r[2] for r in chunk)+"\n", text=True, capture_output=True, timeout=540, env=env)
        lines=[l for l in p.stdout.splitlines() if l.strip()]
        print("batch",i,"rc",p.returncode,"lines",len(lines),"/",len(chunk), p.stderr.strip()[:100])
        if len(lines)!=len(chunk):
            print("MISMATCH; stdout:",p.stdout[:300])
        for r,line in zip(chunk,lines):
            cid,n,pos=r
            sig=line.split()[0]
            out.write(f"{cid}\t{n}\t{pos}\t{sig}\tnodes={line.split('nodes=')[-1] if 'nodes=' in line else ''}\n")
            out.flush()
