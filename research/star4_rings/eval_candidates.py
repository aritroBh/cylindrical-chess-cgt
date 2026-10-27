import subprocess, math, os

inp = "wall_candidates.txt"
outp = "wall_results.tsv"
rg = "./rg"
batch = 40
# read
rows=[]
with open(inp) as f:
    for line in f:
        line=line.rstrip("\n")
        if not line: continue
        cid,n,pos=line.split("\t",2)
        rows.append((cid,n,pos))

# resume: read existing
done=set()
if os.path.exists(outp):
    with open(outp) as f:
        for line in f:
            parts=line.rstrip("\n").split("\t",3)
            if len(parts)>=4: done.add(parts[0])

remaining=[r for r in rows if r[0] not in done]
print("total",len(rows),"done",len(done),"remaining",len(remaining))

with open(outp,"a") as out:
    for i in range(0,len(remaining),batch):
        chunk=remaining[i:i+batch]
        p=subprocess.run(["nice","-n","15","./rg","solve","7"], input="\n".join(r[2] for r in chunk)+"\n", text=True, capture_output=True, timeout=540)
        if p.returncode != 0:
            print("RG ERROR batch", i, "rc", p.returncode, p.stderr[:500])
            # still parse stdout lines
        lines=[l for l in p.stdout.splitlines() if l.strip()]
        if len(lines) != len(chunk):
            print("COUNT MISMATCH batch", i, "expected", len(chunk), "got", len(lines))
        for r,line in zip(chunk, lines):
            cid,n,pos=r
            sig=line.split()[0]
            out.write(f"{cid}\t{n}\t{pos}\t{sig}\tnodes={line.split('nodes=')[-1] if 'nodes=' in line else ''}\n")
            out.flush()
        print("batch", i, "done", min(i+batch,len(remaining)), "/", len(remaining))
