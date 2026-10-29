#!/bin/zsh
# fresh C side (own build of grp.c, reading A = with passes) against the stored output of the independent Python classifier pycheck.py (earlier attempt, K15/pyv/p_*.tsv)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
for cfg in "5 5 3 1 1" "5 5 3 1 2" "5 5 3 2 1" "5 6 3 2 1" "6 5 3 2 2"; do
  set -- ${=cfg}; W=$1;H=$2;F=$3;wm=$4;bm=$5
  for il in 0 1; do for pa in 0 1; do
    fl=""; [[ $il == 1 ]] && fl="$fl --ignore-leak"; [[ $pa == 1 ]] && fl="$fl --allow-passer"
    tag=${W}${H}_${F}_${wm}${bm}_il${il}_pa${pa}
    ( ulimit -t 58; nice -n 15 ./bin/grp --W $W --H $H --F $F --wmax $wm --bmax $bm ${=fl} --dumproots val/cmpA/c_$tag.tsv --out val/cmpA/x > /dev/null 2>&1 )
    python3 - val/cmpA/c_$tag.tsv ../pyv/p_$tag.tsv $tag <<'PY'
import sys
from collections import Counter
def load(fn):
    d={}
    for l in open(fn):
        pos,c=l.rstrip('\n').split('\t'); toks=pos.split()
        d[(toks[0],toks[1],tuple(sorted(toks[2:-2])))]=c
    return d
a=load(sys.argv[1]); b=load(sys.argv[2])
diff=[k for k in a if a.get(k)!=b.get(k)]
print(sys.argv[3],'roots C',len(a),'roots Py',len(b),'label mismatches',len(diff)+len(set(b)-set(a)),'dud',sum(1 for v in a.values() if v=='dud'))
PY
  done; done
done
