import sys, os, json, random, itertools
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames")
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K10v")
import check, run

W,H = 6,6
files=[2,3,4]; ranks=[2,3,4,5]
squares=[(f,r) for f in files for r in ranks]
wk=(0,1); bk=(0,H)
wrap=True

# enumerate all pawn subsets (at most 3)
subsets=[]
for k in range(4):
    for combo in itertools.combinations(squares,k):
        subsets.append(frozenset(combo))

positions=[]  # (pos, stm)
for ws in subsets:
    for bs in subsets:
        if ws & bs: continue
        for stm in ("W","B"):
            ep = run.try_add_ep(W,H,wrap,ws,bs,stm,wk,bk)
            if ep is None:
                continue
            pos = run.make_pos(W,H,ws,bs,wk,bk,ep)
            if not run.legal_pos(W,H,wrap,pos,stm):
                continue
            positions.append((pos,stm))

print("num ep positions", len(positions))
# certify full
instances=[]
cert_pos_stm=set()
key_to_posstm={}
for (pos,stm) in positions:
    for beta in ("W","B"):
        ps=check.certify(W,H,wrap,pos,beta,stm)
        for p in ps:
            instances.append((pos,stm,beta,p))
            cert_pos_stm.add(run.pos_key(pos)+(stm,))
            key_to_posstm[run.pos_key(pos)+(stm,)]=(pos,stm)

# kpsolve
unique=list(cert_pos_stm)
input_lines=[]
for k in unique:
    pos,stm=key_to_posstm[k]
    input_lines.append(check.pos_to_str(W,H,wrap,pos,stm))
in_path=os.path.join(run.OUT,"in_ep.txt")
out_path=os.path.join(run.OUT,"out_ep.txt")
with open(in_path,"w") as f:
    f.write("\n".join(input_lines)+("\n" if input_lines else ""))
cmd=["nice","-n","10",run.KP,"--board",f"cyl:{W}x{H}","--frozen","--cap","1","--threads","2"]
with open(in_path) as fin, open(out_path,"w") as fout:
    import subprocess
    subprocess.run(cmd,stdin=fin,stdout=fout,stderr=subprocess.DEVNULL,check=True)
res={}
with open(out_path) as f:
    for idx,ln in enumerate(f):
        if " | " in ln:
            left,right=ln.rstrip("\n").split(" | ",1)
            parts=right.split()
            res[idx]=(parts[0],parts[1] if len(parts)>1 else parts[0])
key_result={}
for idx,k in enumerate(unique):
    if idx < len(res):
        key_result[k]=res[idx]

viol=0; viols=[]
ep_p_own=0; ep_p_other=0
for (pos,stm,beta,p) in instances:
    k=run.pos_key(pos)+(stm,)
    A,B=key_result.get(k,("?","?"))
    expected="W" if beta=="W" else "L"
    if not (A==expected and B==expected):
        viol+=1
        if len(viols)<10: viols.append(check.pos_to_str(W,H,wrap,pos,stm))
    # classify ep relevance: p's own pawn? ep captured square maybe p? or another beta pawn
    ep=pos.get("ep")
    if ep is not None:
        if ep[1] == p:
            ep_p_own+=1
        else:
            # another beta pawn?
            mine = pos["W"] if beta=="W" else pos["B"]
            if ep[1] in mine:
                ep_p_other+=1

summary={
 "n_positions": len(positions),
 "n_certified_instances": len(instances),
 "n_violations": viol,
 "violations_examples": viols,
 "ep_relevant_own_pawn": ep_p_own,
 "ep_relevant_other_beta_pawn": ep_p_other,
}
with open(os.path.join(run.OUT,"summary_ep.json"),"w") as f:
    json.dump(summary,f,indent=2)
try:
    os.remove(in_path); os.remove(out_path)
except OSError: pass
print(json.dumps(summary,indent=2))
