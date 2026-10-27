import re,sys
L=open('/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md').read()
E=open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22/EDITS.md').read()
for m in re.finditer(r'### EDIT (.*?)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW',E,re.S):
    print(m.group(1), L.count(m.group(2)), len(m.group(2)), len(m.group(3)))
