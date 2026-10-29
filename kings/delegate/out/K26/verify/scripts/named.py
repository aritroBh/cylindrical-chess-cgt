import subprocess,sys
sys.argv=[sys.argv[0],'x','flat:7x6','2','2','x']  # not used
GROUPS={"ZB":(["b2","c3"],["a4","b5"],"Pa3 Pb4 pb3 pc4"),
"ZBm":(["a3","b2"],["b5","c4"],"Pb4 Pc3 pa4 pb3"),
"ZC":(["c2","c3"],["a4","a5"],"Pa2 Pc4 pa3 pc5"),
"ZCm":(["a2","a3"],["c4","c5"],"Pa4 Pc2 pa5 pc3")}
boards=sys.stdin.read().split()
def run(bd,g):
    W,B,P=GROUPS[g]; lines=[];meta=[]
    for wi in (0,1):
        for bi in (0,1):
            for stm in (0,1):
                lines.append(f"K{W[wi]} k{B[bi]} {P} {'wb'[stm]} -"); meta.append((W,B,wi,bi,stm))
    bd2=bd if bd.startswith("cyl") else bd.replace(":","")
    out=subprocess.run(["bin/ref3m","--board",bd2,"--moves"],input="\n".join(lines)+"\n",capture_output=True,text=True).stdout.splitlines()
    out=[l for l in out if " | " in l]
    tot=0; rv=""; ill=False
    for l,(W_,B_,wi,bi,stm) in zip(out,meta):
        rest=l.partition(" | ")[2].split()
        if rest[0]=="X": ill=True; continue
        rv+=rest[0]
        kf,kt=(W_[wi],W_[1-wi]) if stm==0 else (B_[bi],B_[1-bi])
        bad="L" if stm==0 else "W"
        for t in rest[1:]:
            mv,v=t.rsplit(":",1)
            if mv=="K"+kf+kt: continue
            if v!=bad: tot+=1
    return "illegal root" if ill else f"{tot} leaks ({rv})"
for bd in boards:
    print(bd, *[f"{g}: {run(bd,g)}" for g in GROUPS], sep=" | ", flush=True)
