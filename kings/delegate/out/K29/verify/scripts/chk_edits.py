import re,sys
L=open('/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md').read()
E=open(sys.argv[1]).read()
for m in re.finditer(r'### EDIT (.*?)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW',E,re.S):
    print(m.group(1),'| OLD count =',L.count(m.group(2)),'| NEW len',len(m.group(3)))
