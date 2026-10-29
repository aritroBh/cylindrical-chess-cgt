import re,sys
L=open('/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md').read()
E=open(sys.argv[1]).read()
blocks=re.findall(r'### EDIT (.*?)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW',E,re.S)
print(len(blocks),"blocks")
for lab,old,new in blocks:
    print(f"{L.count(old)}x  {lab}  (OLD {len(old)} chars, NEW {len(new)} chars)")
