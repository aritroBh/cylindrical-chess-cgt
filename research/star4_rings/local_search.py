import os, subprocess, time

VENV="/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python"
RG="./rg"

def load_seeds(path):
    out=[]
    with open(path) as f:
        for line in f:
            line=line.strip()
            if line:
                out.append(line)
    return out

# import generator functions from gen_one by exec? Instead reimplement minimal import via runpy not ideal.
# We'll import by exec file content as module.
import importlib.util
spec=importlib.util.spec_from_file_location("gen_one","gen_one.py")
g=importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

def n_of_pos(s): return len(s.split())

def generate_for_seed(seed):
    pl=[tuple(x) for x in g.parse_pos(seed)]
    # parse_pos returns list of (set,set); convert to frozensets
    pl=[(frozenset(w),frozenset(b)) for w,b in pl]
    # generator functions expect list of (set,set) and convert; pass mutable sets
    plm=[(set(w),set(b)) for w,b in pl]
    cands=set()
    cands |= g.add_pawn_candidates(plm)
    cands |= g.add_pair_candidates(plm)
    cands |= g.insert_file_candidates(plm)
    cands |= g.attach_star1_candidates(plm)
    cands.discard(seed)
    return cands

def is_star(sig,k):
    return len(sig)>=8 and all(sig[i]=='N' for i in range(8) if i!=k) and sig[k]=='P'

def eval_positions(positions):
    # group by n
    by_n={}
    for pos in positions:
        by_n.setdefault(n_of_pos(pos),[]).append(pos)
    results={}
    env=dict(os.environ); env["TBITS"]="23"
    for n,pls in by_n.items():
        # batch
        for i in range(0,len(pls),20):
            chunk=pls[i:i+20]
            p=subprocess.run(["nice","-n","15",RG,"solve","7"], input="\n".join(chunk)+"\n",
                            text=True, capture_output=True, timeout=540, env=env, cwd=".")
            lines=[l for l in p.stdout.splitlines() if l.strip()]
            if len(lines)!=len(chunk):
                # rerun individually
                for pos in chunk:
                    p2=subprocess.run(["nice","-n","15",RG,"solve","7"], input=pos+"\n",
                                    text=True, capture_output=True, timeout=540, env=env, cwd=".")
                    l2=[l for l in p2.stdout.splitlines() if l.strip()]
                    if l2:
                        results[pos]=l2[0].split()[0]
                    else:
                        results[pos]="ERROR"
            else:
                for pos,line in zip(chunk,lines):
                    results[pos]=line.split()[0]
            print(f"  n={n} batch {i}/{len(pls)} done", flush=True)
    return results

def main():
    seeds=load_seeds("seeds_star3.txt")
    all_seen=set(seeds)
    # also include original seeds in seen
    seed_set=set(seeds)
    round_no=1
    max_rounds=3
    while round_no<=max_rounds and seed_set:
        print(f"=== ROUND {round_no}: {len(seed_set)} seeds ===", flush=True)
        # generate
        cands=set()
        for s in seed_set:
            cands |= generate_for_seed(s)
        # remove seen
        newcands=[c for c in cands if c not in all_seen and len(c.split())<=14]
        print(f"generated {len(cands)} raw, {len(newcands)} new after dedup", flush=True)
        if not newcands:
            print("no new candidates")
            break
        # write candidates
        with open(f"round{round_no}_candidates.txt","w") as f:
            for c in newcands:
                f.write(c+"\n")
        # eval
        res=eval_positions(newcands)
        # append results
        with open("local_results.tsv","a") as f:
            for pos,sig in res.items():
                f.write(f"{round_no}\t{pos}\t{n_of_pos(pos)}\t{sig}\n")
        # classify
        new_star3=set()
        counts={}
        for pos,sig in res.items():
            all_seen.add(pos)
            key=sig
            counts[key]=counts.get(key,0)+1
            if is_star(sig,3):
                new_star3.add(pos)
            if is_star(sig,4):
                print("FOUND *4:", pos, sig)
        print("round",round_no,"sig counts top:", sorted(counts.items(), key=lambda x:-x[1])[:8])
        print("new *3 count", len(new_star3))
        # save new star3 seeds
        with open(f"round{round_no}_new_star3.txt","w") as f:
            for pos in new_star3:
                f.write(pos+"\n")
        seed_set=new_star3
        round_no+=1

if __name__=="__main__":
    # ensure header
    if not os.path.exists("local_results.tsv"):
        with open("local_results.tsv","w") as f:
            f.write("round\tpos\tn\tsig\n")
    main()
