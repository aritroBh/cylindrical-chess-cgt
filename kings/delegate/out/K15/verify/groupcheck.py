import re,subprocess,sys,collections,json
sec=None; rows=[]
for ln in open('../fin2/dud_groups.md'):
    m=re.match(r'## (cyl):(\d+)x(\d+): (\d+)',ln)
    if m: sec=(int(m.group(2)),int(m.group(3))); continue
    m=re.match(r'\| (\d+) \| `([^`]*)` \| ([^|]*) \| (.*) \|',ln)
    if m and sec: rows.append((sec,int(m.group(1)),m.group(2),m.group(3).strip()))
out=open('runs/groupcheck.tsv','w')
summ=collections.Counter()
for (W,H),idx,root,found in rows:
    files=[ord(t[1])-97 for t in root.split() if len(t)>=3]
    span=max(files)+1
    res={}
    for rd,flag in (('B','--nopass'),('A','')):
        lab=None
        for F in range(span,min(5,W)+1):
            open('gc_tmp.in','w').write(root+'\n')
            cmd=['bin/mysolve','--W',str(W),'--H',str(H),'--F',str(F),'--reach','gc_tmp.in']+([flag] if flag else [])
            r=subprocess.run(['nice','-n','15']+cmd,capture_output=True,text=True)
            l=r.stdout.split('\t')[1] if '\t' in r.stdout else '?'
            if l=='dud': lab=(F,l); break
            if lab is None: lab=(F,l)
        res[rd]=lab
    out.write(f'{W}x{H}\t{idx}\t{root}\t{found}\tB:{res["B"]}\tA:{res["A"]}\n'); out.flush()
    summ[(W,H,res['B'][1]=='dud',found.startswith('A'),res['A'][1]=='dud')]+=1
print(summ)
