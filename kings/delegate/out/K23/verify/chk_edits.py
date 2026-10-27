import re
L=open('/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md').read()
E=open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K23/EDITS.md').read()
blocks=re.findall(r'### EDIT (.*?)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW',E,re.S)
print(len(blocks),'blocks')
for lab,old,new in blocks:
    print(L.count(old), lab, '| old chars',len(old))
