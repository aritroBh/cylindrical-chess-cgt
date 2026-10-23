import collections, sys
tag=sys.argv[1]
exp={l.split("\t")[0]:(int(l.split("\t")[1]),l.rstrip("\n").split("\t")[2:]) for l in open(f"gs_{tag}.tsv")}
cnt=collections.Counter(); bad=[]; seen=0
for l in open(f"gs_{tag}.out"):
    if l.startswith("#"): continue
    t=l.rstrip("\n").split("\t"); pos=t[0]
    if pos not in exp: continue
    seen+=1
    e,(a,b)=exp[pos]
    got=t[4] if len(t)>4 and t[3] in "NLRP" else t[3]
    cnt[(a,b,got)]+=1
    if got!=str(e): bad.append((pos,e,got,t[-1] if len(t)>5 else ""))
print(tag,"evaluated",seen,"of",len(exp)); print(sorted(cnt.items()))
print("mismatches vs nim-sum:",len(bad))
for b in bad[:15]: print(b)
