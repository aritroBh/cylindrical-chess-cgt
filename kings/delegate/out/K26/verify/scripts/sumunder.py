import json,glob,sys
pat=sys.argv[1]
tot={};n=0
for f in sorted(glob.glob(pat)):
    d=json.load(open(f)); n+=1
    for k,v in d.items():
        if k=='exact': tot.setdefault('exact',[]).extend(v)
        else: tot[k]=tot.get(k,0)+v
print(pat,n,'shards',{k:(v if k!='exact' else len(v)) for k,v in tot.items()})
