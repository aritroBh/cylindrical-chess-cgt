import re,sys
f=sys.argv[1]
txt=open(f).read()
src=open("/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md").read()
pat=re.compile(r"^### EDIT ([^\n]*)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW",re.S|re.M)
cur=src; bad=0
for m in pat.finditer(txt):
    lab,old,new=m.groups()
    n0=src.count(old); n=cur.count(old)
    print(("OK " if n==1 and n0==1 else "BAD"),lab[:50],"orig-count",n0,"sequential-count",n)
    if n!=1 or n0!=1: bad+=1
    cur=cur.replace(old,new,1) if n==1 else cur
print("bad",bad); open(sys.argv[2],"w").write(cur)
