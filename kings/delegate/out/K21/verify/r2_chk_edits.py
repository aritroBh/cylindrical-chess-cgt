import re,sys
L=open('/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md').read()
print("LOOPY chars",len(L))
for f in sys.argv[1:]:
    s=open(f).read()
    blocks=re.findall(r'### EDIT ([^\n]*)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW',s,flags=re.S)
    print(f,"blocks",len(blocks), "markers OLD/NEW", s.count('<<<<<<< OLD'), s.count('>>>>>>> NEW'))
    cur=L
    for lab,old,new in blocks:
        print("  ",lab[:60],"| OLD count in LOOPY:",L.count(old),"| in sequentially edited:",cur.count(old),"| NEW len",len(new))
        if cur.count(old)==1: cur=cur.replace(old,new)
    open('/tmp/claude-501/r2_applied_%s.md'%f.split('/')[-1],'w').write(cur) if False else None
