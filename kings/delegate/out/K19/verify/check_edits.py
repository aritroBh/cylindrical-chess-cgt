import re,sys
L=open('/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md').read()
E=open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K19/EDITS.md').read()
blocks=re.findall(r'### EDIT (.*?)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW',E,re.S)
print(len(blocks),'blocks')
cur=L
for lab,old,new in blocks:
    c=L.count(old); cc=cur.count(old)
    print(f'{lab:25s} count_in_current={c} count_after_prev_edits={cc}')
    if cc==1: cur=cur.replace(old,new)
# overlaps between edits
pos=[(L.find(o),L.find(o)+len(o),l) for l,o,n in blocks if L.count(o)==1]
pos.sort()
for a,b in zip(pos,pos[1:]):
    if a[1]>b[0]: print('OVERLAP',a[2],b[2])
open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K19/verify/LOOPY_after.md','w').write(cur)
