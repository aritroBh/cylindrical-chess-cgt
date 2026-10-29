import sys, os, itertools, json, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
sys.path.insert(0, os.path.dirname(__file__))
from classify import *

def squares_group(W,H, files):
    return [(f,r) for f in files for r in range(2, H)]  # pawns ranks 2..H-1; kings can be any rank 1..H

def king_squares(W,H, files):
    return [(f,r) for f in files for r in range(1, H+1)]

def enumerate_placements(W,H,group_files,wP,bP):
    GFILES=group_files
    king_sq=king_squares(W,H,GFILES)
    pawn_sq=[(f,r) for f in GFILES for r in range(2,H)]  # ranks 2..H-1
    count=0
    results={'frozen':0,'on':0,'off':0,'dud':0,'over':0,'other':0}
    candidates={'dud':[],'over':[]}
    # king pairs
    for wi in range(len(king_sq)):
        wk=king_sq[wi]
        for bi in range(len(king_sq)):
            bk=king_sq[bi]
            if wk==bk: continue
            # kings not adjacent
            if abs(wk[1]-bk[1])<=1:
                df=(bk[0]-wk[0])%W
                if df>W//2: df-=W
                if abs(df)<=1:
                    continue
            # no passer root check after pawns; but kings irrelevant
            remaining_pawns=[s for s in pawn_sq if s!=wk and s!=bk]
            # choose white pawns
            for wps in itertools.combinations(remaining_pawns, wP):
                wset=set(wps)
                rem2=[s for s in remaining_pawns if s not in wset]
                for bps in itertools.combinations(rem2, bP):
                    wp=list(wps); bp=list(bps)
                    if not root_no_passer(W,H,wp,bp):
                        continue
                    cls=classify_with_files(W,H,wk,bk,wp,bp,GFILES)
                    results[cls]=results.get(cls,0)+1
                    count+=1
                    if cls in ('dud','over'):
                        # store up to maybe 200
                        if len(candidates[cls])<200:
                            candidates[cls].append((wk,bk,wp,bp))
    return count, results, candidates

if __name__=='__main__':
    W=int(sys.argv[1]); H=int(sys.argv[2]); F=int(sys.argv[3])
    wP=int(sys.argv[4]); bP=int(sys.argv[5])
    # group files start positions
    all_starts=list(range(W))
    agg_results={'frozen':0,'on':0,'off':0,'dud':0,'over':0,'other':0}
    total=0
    all_cands={'dud':[],'over':[]}
    t0=time.time()
    for start in all_starts:
        files=[(start+i)%W for i in range(F)]
        c,res,cands=enumerate_placements(W,H,files,wP,bP)
        total+=c
        for k in agg_results:
            agg_results[k]+=res.get(k,0)
        for cls in all_cands:
            for cand in cands[cls]:
                if len(all_cands[cls])<200:
                    all_cands[cls].append((files[:], cand))
    # write summary
    out={'W':W,'H':H,'F':F,'wP':wP,'bP':bP,'total':total,'results':agg_results,
         'dud_n':len(all_cands['dud']),'over_n':len(all_cands['over']),
         'time':time.time()-t0}
    with open(f'summary_W{W}_H{H}_F{F}_w{wP}_b{bP}.json','w') as f:
        json.dump(out,f,indent=2)
    # save candidates
    with open(f'cands_W{W}_H{H}_F{F}_w{wP}_b{bP}.json','w') as f:
        json.dump({'dud':[[ (c[0],c[1],c[2],c[3]) for c in [x[1]] ] for x in all_cands['dud']],
                   'over':[[ (c[0],c[1],c[2],c[3]) for c in [x[1]] ] for x in all_cands['over']]}, f)
    print(json.dumps(out))
