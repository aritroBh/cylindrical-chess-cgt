import re,sys
t=open('/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md').read()
e=open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18/EDITS.md').read()
blocks=re.findall(r'### EDIT (.*?)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW',e,re.S)
print(len(blocks),'blocks')
for lab,o,n in blocks:
    print(lab, 'OLD count', t.count(o), 'len',len(o),len(n))
    # prefix check
    if t.count(o)!=1:
        # find longest matching prefix
        lo=0
        for k in range(10,len(o),10):
            if o[:k] in t: lo=k
        print(' longest prefix in file', lo)
        i=t.find(o[:lo]); print(repr(t[i+lo-60:i+lo+120])); print(repr(o[lo-60:lo+120]))
