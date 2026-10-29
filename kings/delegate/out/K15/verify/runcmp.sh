#!/bin/zsh
# usage: runcmp.sh NAME "<grp board args>" "<mysolve board args>" [nopass]
# board args e.g. "--W 7 --H 6 --F 3 --wmax 3 --bmax 3" ; extra flags for both
NAME=$1; GA=$2; MA=$3; NP=$4
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/verify
NPG=""; NPM=""; [[ -n "$NP" ]] && NPG="--nopass" && NPM="--nopass"
KEEP='\t(frozen|dud|over|under)$'
nice -n 15 bin/mysolve ${=MA} ${=NPM} --dump /dev/fd/3 3> >(grep -E "$KEEP" | sort > runs/${NAME}.my.dump) > runs/${NAME}.my.json 2> runs/${NAME}.my.err
nice -n 15 bin/grp ${=GA} ${=NPG} --allow-passer --dumproots /dev/fd/3 3> >(grep -E "$KEEP" | sort > runs/${NAME}.grp.dump) --out runs/${NAME}.grp > runs/${NAME}.grp.json 2> runs/${NAME}.grp.err
sleep 2
python3 - <<PY
import json,collections
def norm(p): return ' '.join(sorted(x for x in p.split() if x[0] in 'KkPp' and len(x)>=3))
def load(fn): return {norm(l.split('\t')[0]):l.rstrip().split('\t')[1] for l in open(fn)}
a=load('runs/${NAME}.grp.dump'); b=load('runs/${NAME}.my.dump')
cg=collections.Counter(a.values()); cm=collections.Counter(b.values())
diff=[k for k in set(a)|set(b) if a.get(k)!=b.get(k)]
print('${NAME}','grp',dict(cg),'mine',dict(cm),'label diffs (frozen/dud/over/under only):',len(diff))
for k in diff[:5]: print('  ',k,a.get(k),b.get(k))
j=json.loads(open('runs/${NAME}.my.json').read()); print('  my roots(no attacked king)',j['roots'],'selfviol',j['selfcheck_violations'],'relaxed_over_under',j['relaxed_over_or_under_roots'])
PY
