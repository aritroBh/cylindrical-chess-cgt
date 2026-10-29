#!/bin/zsh
# K15 r3: independent re-run (rebuilt binary r3/bin/grp) of census runs that fit under one CPU-minute (ulimit -t 58, nice 15, no lock); compares the candidate lists and the JSON counts with fin2/runs.
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/r3
run() { t=$1; shift
  [[ -f runs/$t.done ]] && return
  ( ulimit -t 58; nice -n 15 bin/grp "$@" --out runs/$t > runs/$t.json 2> runs/$t.err )
  e=$?
  r=same; for v in strict passer; do cmp -s runs/${t}_${v}_cands.txt ../fin2/runs/${t}_${v}_cands.txt || r=DIFF_$v; done
  python3 - runs/$t.json ../fin2/runs/$t.json > runs/$t.cmp <<'PY'
import json,sys
def docs(f):
    t=open(f).read(); dec=json.JSONDecoder(); i=0; out=[]
    while i<len(t):
        while i<len(t) and t[i].isspace(): i+=1
        if i>=len(t): break
        try: o,i=dec.raw_decode(t,i)
        except Exception: break
        out.append(o)
    return out
def strip(o): return {k:v for k,v in o.items() if 'time' not in k and 'cpu' not in k and 'sec' not in k}
a=docs(sys.argv[1]); b=docs(sys.argv[2])
print('docs',len(a),len(b),'identical-without-timing', [strip(x)==strip(y) for x,y in zip(a,b)])
PY
  echo "$t exit=$e cands=$r $(cat runs/$t.cmp)" >> logs/rerun.log; touch runs/$t.done; }
run flat76_np --flat --W 7 --H 6 --F 3 --wmax 2 --bmax 2 --nopass --sp-variants
run flatA_7x6_f3_22 --flat --W 7 --H 6 --F 3 --wmax 2 --bmax 2 --sp-variants
for w in 8 7; do
 run pA_${w}x6_f3_33 --W $w --H 6 --F 3 --wmax 3 --bmax 3 --sp-variants
 run npB_${w}x6_f3_33 --nopass --W $w --H 6 --F 3 --wmax 3 --bmax 3 --sp-variants
done
echo rerun_finished >> logs/rerun.log
