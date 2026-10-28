import sys,re
nf=int(sys.argv[1]); files=sys.argv[3:]; var=sys.argv[2]
def msq(s): return chr(97+nf-1-(ord(s[0])-97))+s[1:]
def canon(y):
    t=y.split(); a=tuple(sorted(t[:-2])); b=tuple(sorted(x[0]+msq(x[1:]) for x in t[:-2])); return min(a,b)
anyc={};noesc={}
for f in files:
  for l in open(f):
    if l.startswith('#'): continue
    p=[x.strip() for x in l.split('|')]
    if p[0]!=var: continue
    k=canon(p[1]); anyc[k]=1
    if p[3]=='NOESC': noesc[k]=1
print(f,var,'distinct any',len(anyc),'noesc',len(noesc))
