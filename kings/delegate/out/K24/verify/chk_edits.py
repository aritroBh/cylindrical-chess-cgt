import re,sys
L=open('/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md').read()
E=open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K24/EDITS.md').read()
blocks=re.findall(r'### EDIT (.*?)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW',E,re.S)
print(len(blocks),'edits')
for lab,old,new in blocks:
    print(f'{lab!r}: OLD count={L.count(old)}  len(old)={len(old)}  len(new)={len(new)}')
