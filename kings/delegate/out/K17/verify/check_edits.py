import re,sys
L=open('/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md').read()
E=open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K17/EDITS.md').read()
blocks=re.findall(r'### EDIT (.*?)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW',E,re.S)
print(len(blocks),'blocks')
for lab,old,new in blocks:
    print(lab,'| OLD occurrences:',L.count(old),'| NEW already in LOOPY:',L.count(new))
